"""Emit Pydantic models and async client resource modules."""

from __future__ import annotations

import keyword
import re
from typing import Any

from codegen.schema import (
    SUCCESS_CODES,
    EmittedModel,
    ExtraMode,
    NameMap,
    SchemaRole,
    collapse_single_oneof,
    flatten_allof,
    is_enum,
    is_type_alias,
)
from codegen.spec import camel_to_snake, snake_to_pascal, unique_method_names

_CONSTRAINTS = (
    ("minimum", "ge"),
    ("maximum", "le"),
    ("minLength", "min_length"),
    ("maxLength", "max_length"),
    ("minItems", "min_length"),
    ("maxItems", "max_length"),
)

_ENUM_HEADER_RE = re.compile(r"^\s*\*\*[^*]+ Enum:\*\*\s*$")
_ENUM_PLAIN_RE = re.compile(r"^\s*Enum:\s*")
_TABLE_LINE_RE = re.compile(r"^\s*\|")
_ENUM_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|$")
_LENIENT_ENUM_RE = re.compile(r"^Annotated\[(.+?) \| str, lenient_enum\(.+\)\]$")
_PYDANTIC_SHADOW = frozenset(
    {
        "schema",
        "copy",
        "dict",
        "json",
        "validate",
        "construct",
        "fields",
        "config",
        "parse_obj",
        "parse_raw",
        "from_orm",
        "schema_json",
    }
)


class ImportSet:
    def __init__(self) -> None:
        self.names: set[str] = set()

    def add(self, *names: str) -> None:
        self.names.update(names)


def safe_ident(name: str, used: set[str] | None = None) -> str:
    """Turn an OpenAPI name into a valid Python identifier."""
    safe = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    safe = re.sub(r"_+", "_", safe).strip("_")
    if not safe or safe[0].isdigit():
        safe = f"_{safe}" if safe else "_"
    if keyword.iskeyword(safe):
        safe = f"{safe}_"
    if safe in _PYDANTIC_SHADOW:
        safe = f"{safe}_"
    if used is not None:
        while safe in used:
            safe = f"{safe}_"
        used.add(safe)
    return safe


def _is_id_field(name: str | None) -> bool:
    """Check if a field/parameter name represents an ID that should be integer rather than float."""
    if not name:
        return False
    lower = name.lower()
    if lower in ("id", "ids"):
        return True
    if name.endswith(("Id", "Ids", "_id", "_ids")):
        if lower.endswith(("bid", "bids")):
            return False
        return True
    return False


def schema_type(
    schema: dict[str, Any],
    openapi_schemas: dict[str, Any],
    name_map: NameMap,
    context_role: SchemaRole,
    imports: ImportSet,
    field_name: str | None = None,
) -> str:
    if "$ref" in schema:
        openapi_name = schema["$ref"].split("/")[-1]
        python_name = name_map.resolve(openapi_name, context_role)
        ref = openapi_schemas.get(openapi_name, {})
        if ref.get("enum"):
            if context_role == SchemaRole.INPUT:
                return python_name
            return f"{python_name} | str"
        return python_name
    if "enum" in schema and all(isinstance(v, str) for v in schema["enum"]):
        imports.add("Literal")
        items = ", ".join(f'"{v}"' for v in schema["enum"])
        lit = f"Literal[{items}]"
        if context_role == SchemaRole.INPUT:
            return lit
        return f"{lit} | str"
    t = schema.get("type", "object")
    fmt = schema.get("format", "")
    if t == "array":
        items_schema = schema.get("items", {})
        if "enum" in items_schema and all(isinstance(v, str) for v in items_schema["enum"]):
            imports.add("Literal")
            items = ", ".join(f'"{v}"' for v in items_schema["enum"])
            if context_role == SchemaRole.INPUT:
                return f"list[Literal[{items}]]"
            return f"list[Literal[{items}] | str]"
        if "$ref" in items_schema:
            ref_name = items_schema["$ref"].split("/")[-1]
            if openapi_schemas.get(ref_name, {}).get("enum"):
                py_name = name_map.resolve(ref_name, context_role)
                if context_role == SchemaRole.INPUT:
                    return f"list[{py_name}]"
                return f"list[{py_name} | str]"
        inner = schema_type(items_schema, openapi_schemas, name_map, context_role, imports, field_name=field_name)
        return f"list[{inner}]"
    if t == "object":
        additional = schema.get("additionalProperties")
        if isinstance(additional, dict):
            val = schema_type(additional, openapi_schemas, name_map, context_role, imports)
            return f"dict[str, {val}]"
        imports.add("Any")
        return "dict[str, Any]"
    if t == "string":
        if fmt == "date-time":
            imports.add("datetime")
            return "datetime"
        if fmt == "date":
            imports.add("date")
            return "date"
        return "str"
    if t == "integer":
        return "int"
    if t == "number":
        if field_name and _is_id_field(field_name) and fmt not in ("float", "double"):
            return "int"
        return "float"
    if t == "boolean":
        return "bool"
    imports.add("Any")
    return "Any"


def _consume_table(lines: list[str], start: int) -> tuple[list[str], int]:
    end = start
    while end < len(lines) and _TABLE_LINE_RE.match(lines[end]):
        end += 1
    return lines[start:end], end


def _is_enum_member_table(block: list[str]) -> bool:
    """True when rows look like ``| `VALUE` | description |``."""
    return any(_ENUM_ROW_RE.match(line.strip()) for line in block)


def strip_markdown_tables(text: str) -> str:
    """Drop enum member catalogs; keep other markdown tables.

    Strips ``**Xxx Enum:**`` / ``Enum: ...`` headers and tables whose cells are
    backtick-wrapped enum values. Business tables (thresholds, field maps) stay.
    """
    lines = text.splitlines()
    kept: list[str] = []
    skip_next_table = False
    i = 0
    while i < len(lines):
        raw = lines[i]
        if _ENUM_HEADER_RE.match(raw) or _ENUM_PLAIN_RE.match(raw):
            skip_next_table = True
            i += 1
            continue
        if _TABLE_LINE_RE.match(raw):
            block, i = _consume_table(lines, i)
            if skip_next_table or _is_enum_member_table(block):
                skip_next_table = False
                continue
            skip_next_table = False
            kept.extend(line.rstrip() for line in block)
            continue
        if skip_next_table and not raw.strip():
            i += 1
            continue
        skip_next_table = False
        kept.append(raw.rstrip())
        i += 1
    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    collapsed: list[str] = []
    prev_blank = False
    for line in kept:
        blank = not line.strip()
        if blank and prev_blank:
            continue
        collapsed.append(line)
        prev_blank = blank
    return "\n".join(collapsed).strip()


def parse_enum_member_docs(doc: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in doc.splitlines():
        match = _ENUM_ROW_RE.match(line.strip())
        if not match:
            continue
        desc = match.group(2).strip()
        if desc:
            result[match.group(1)] = desc
    return result


def _format_type_doc(doc: str, member_docs: dict[str, str] | None = None) -> str:
    cleaned = strip_markdown_tables(doc).strip()
    doc_sections: list[str] = []
    if cleaned:
        doc_sections.append(cleaned)
    if member_docs:
        options = [f"- `{k}`: {v}" for k, v in member_docs.items()]
        doc_sections.append("Supported values:\n" + "\n".join(options))
    if not doc_sections:
        return ""
    full_doc = "\n\n".join(doc_sections)
    safe = full_doc.replace('"""', '\\"\\"\\"')
    return f'\n"""\n{safe}\n"""'


def generate_enum(name: str, schema: dict[str, Any], imports: ImportSet) -> str:
    imports.add("Literal")
    raw_doc = schema.get("description", "")
    member_docs = parse_enum_member_docs(raw_doc)
    docstring = _format_type_doc(raw_doc, member_docs)
    values = schema.get("enum", [])
    if not values:
        imports.add("Any")
        return f"type {name} = Any\n"

    items = ", ".join(f'"{v}"' for v in values)
    return f"type {name} = Literal[{items}]{docstring}\n"


def generate_type_alias(name: str, schema: dict[str, Any], imports: ImportSet) -> str:
    t = schema["type"]
    if t == "number":
        fmt = schema.get("format", "")
        if _is_id_field(name) and fmt not in ("float", "double"):
            py_type = "int"
        else:
            py_type = "float"
    else:
        py_type = {"string": "str", "integer": "int", "boolean": "bool"}.get(t, "Any")
        if py_type == "Any":
            imports.add("Any")
    doc = strip_markdown_tables(schema.get("description", ""))
    if doc and "\n" not in doc:
        return f"type {name} = {py_type}  # {doc}"
    return f"type {name} = {py_type}"


def _format_default(default_val: Any, typ: str) -> str:
    if default_val is None or isinstance(default_val, list):
        return "default=None"
    if "bool" in typ:
        if isinstance(default_val, str) and default_val.lower() in ("true", "false"):
            return f"default={default_val.lower() == 'true'}"
        if isinstance(default_val, list):
            converted_bools = [
                (x.lower() == "true") if isinstance(x, str) and x.lower() in ("true", "false") else bool(x)
                for x in default_val
            ]
            return f"default={converted_bools!r}"
    if "int" in typ:
        if isinstance(default_val, str):
            try:
                return f"default={int(default_val)}"
            except ValueError:
                pass
        if isinstance(default_val, list):
            try:
                converted_ints = [int(x) if isinstance(x, str) else x for x in default_val]
                return f"default={converted_ints!r}"
            except ValueError:
                pass
    if "float" in typ:
        if isinstance(default_val, str):
            try:
                return f"default={float(default_val)}"
            except ValueError:
                pass
        if isinstance(default_val, list):
            try:
                converted_floats = [float(x) if isinstance(x, str) else x for x in default_val]
                return f"default={converted_floats!r}"
            except ValueError:
                pass
    return f"default={default_val!r}"


def _escape_desc(desc: str) -> str:
    return desc.replace("\\", "\\\\").replace('"', '\\"')


def _model_docstring(schema: dict[str, Any]) -> str:
    doc = strip_markdown_tables(schema.get("description", ""))
    if not doc:
        return ""
    safe = doc.replace('"""', '\\"\\"\\"')
    return f'\n    """{safe}"""'


def _base_class(extra: ExtraMode, imports: ImportSet) -> str:
    if extra == "forbid":
        imports.add("StrictModel")
        return "StrictModel"
    imports.add("LenientModel")
    return "LenientModel"


def _variant_class_name(parent: str, variant: dict[str, Any], index: int) -> str:
    title = variant.get("title")
    if title:
        return f"{parent}{snake_to_pascal(camel_to_snake(str(title)))}"
    return f"{parent}Variant{index}"


def _field_lines(
    props: dict[str, Any],
    required: set[str],
    openapi_schemas: dict[str, Any],
    name_map: NameMap,
    context_role: SchemaRole,
    imports: ImportSet,
) -> list[str]:
    fields: list[str] = []
    used: set[str] = set()
    for fname, fschema in props.items():
        typ = schema_type(fschema, openapi_schemas, name_map, context_role, imports, field_name=fname)
        is_required = fname in required
        if not is_required and typ != "Any":
            typ = f"{typ} | None"
        ident = safe_ident(fname)
        if ident in name_map.python_names:
            ident = camel_to_snake(fname)
        py_name = safe_ident(ident, used)
        kwargs: list[str] = []
        if py_name != fname:
            kwargs.append(f"alias={fname!r}")
        for attr, kw in _CONSTRAINTS:
            if attr in fschema:
                kwargs.append(f"{kw}={fschema[attr]}")
        if "pattern" in fschema and not re.search(r"\(\?[=!<]", fschema["pattern"]):
            kwargs.append(f"pattern={fschema['pattern']!r}")
        if not is_required:
            kwargs.insert(0, _format_default(fschema.get("default"), typ))
        desc = strip_markdown_tables(fschema.get("description", ""))
        if desc:
            imports.add("Field")
            if "\n" in desc:
                desc_safe = desc.replace('"""', '\\"\\"\\"')
                kwargs.append(f'description="""\n{desc_safe}\n"""')
            else:
                kwargs.append(f'description="{_escape_desc(desc)}"')
        if kwargs:
            imports.add("Field")
            fields.append(f"    {py_name}: {typ} = Field({', '.join(kwargs)})")
        else:
            fields.append(f"    {py_name}: {typ}")
    return fields


def generate_model(
    name: str,
    schema: dict[str, Any],
    openapi_schemas: dict[str, Any],
    name_map: NameMap,
    context_role: SchemaRole,
    extra: ExtraMode,
    imports: ImportSet,
) -> str:
    schema = collapse_single_oneof(flatten_allof(schema, openapi_schemas))
    docstring = _model_docstring(schema)
    base = _base_class(extra, imports)
    required = set(schema.get("required", []))

    if not schema.get("properties") and schema.get("oneOf"):
        variants = [v for v in schema["oneOf"] if isinstance(v, dict)]
        object_variants = [v for v in variants if v.get("type") == "object" and v.get("properties")]
        if len(object_variants) > 1:
            blocks: list[str] = []
            variant_names: list[str] = []
            for index, variant in enumerate(object_variants):
                vname = _variant_class_name(name, variant, index)
                variant_names.append(vname)
                blocks.append(generate_model(vname, variant, openapi_schemas, name_map, context_role, extra, imports))
            blocks.append(f"type {name} = {' | '.join(variant_names)}")
            return "\n\n".join(blocks)
        fields = _field_lines(
            {fname: fschema for variant in object_variants for fname, fschema in variant.get("properties", {}).items()},
            set(),
            openapi_schemas,
            name_map,
            context_role,
            imports,
        )
        field_block = "\n".join(fields) if fields else "    pass"
        glue = "\n\n" if docstring else "\n"
        return f"class {name}({base}):{docstring}{glue}{field_block}\n"

    if not schema.get("properties") and schema.get("anyOf"):
        parents: list[str] = []
        for entry in schema["anyOf"]:
            if "$ref" not in entry:
                break
            parents.append(name_map.resolve(entry["$ref"].split("/")[-1], context_role))
        else:
            return f"class {name}({', '.join(parents)}):{docstring}\n    pass\n"

    props = schema.get("properties", {})
    if not props:
        return f"class {name}({base}):{docstring}\n    pass\n"

    fields = _field_lines(props, required, openapi_schemas, name_map, context_role, imports)
    glue = "\n\n" if docstring else "\n"
    return f"class {name}({base}):{docstring}{glue}" + "\n".join(fields) + "\n"


def emit_model(
    item: EmittedModel,
    openapi_schemas: dict[str, Any],
    name_map: NameMap,
    imports: ImportSet,
) -> str:
    if is_type_alias(item.schema):
        return generate_type_alias(item.python_name, item.schema, imports)
    if is_enum(item.schema) and item.schema.get("enum"):
        return generate_enum(item.python_name, item.schema, imports)
    return generate_model(
        item.python_name,
        item.schema,
        openapi_schemas,
        name_map,
        item.key.role,
        item.extra,
        imports,
    )


def is_anyof_composition(schema: dict[str, Any]) -> bool:
    if schema.get("properties") or not schema.get("anyOf"):
        return False
    return all("$ref" in entry for entry in schema["anyOf"])


def split_types(
    emitted: list[EmittedModel],
) -> tuple[list[EmittedModel], list[EmittedModel], list[EmittedModel]]:
    enums: list[EmittedModel] = []
    regular: list[EmittedModel] = []
    composition: list[EmittedModel] = []
    for item in sorted(emitted, key=lambda x: x.python_name):
        if is_type_alias(item.schema):
            regular.append(item)
        elif is_enum(item.schema) and item.schema.get("enum"):
            enums.append(item)
        elif is_anyof_composition(item.schema):
            composition.append(item)
        else:
            regular.append(item)
    return enums, regular, composition


def _render_import_header(tag: str, imports: ImportSet, shared_module: str | None, shared_names: list[str]) -> str:
    lines = [
        f'"""Auto-generated models for {tag} from Amazon Ads API v0."""',
        "",
        "from __future__ import annotations",
        "",
    ]
    datetime_parts = [n for n in ("date", "datetime") if n in imports.names]
    if datetime_parts:
        lines.append(f"from datetime import {', '.join(datetime_parts)}")
    if "StrEnum" in imports.names:
        lines.append("from enum import StrEnum")
    typing_parts = [n for n in ("Annotated", "Any", "Literal") if n in imports.names]
    if typing_parts:
        lines.append(f"from typing import {', '.join(typing_parts)}")
    if datetime_parts or "StrEnum" in imports.names or typing_parts:
        lines.append("")

    pydantic_parts: list[str] = []
    if "Field" in imports.names:
        pydantic_parts.append("Field")
    if pydantic_parts:
        lines.append(f"from pydantic import {', '.join(pydantic_parts)}")
        lines.append("")

    core_imports: list[str] = []
    if "LenientModel" in imports.names:
        core_imports.append("LenientModel")
    if "StrictModel" in imports.names:
        core_imports.append("StrictModel")
    if core_imports:
        lines.append(f"from ads_api.models._core.base import {', '.join(core_imports)}")
    if "lenient_enum" in imports.names:
        lines.append("from ads_api.models._core.lenient_enum import lenient_enum")
    if core_imports or "lenient_enum" in imports.names:
        lines.append("")

    if shared_names:
        lines.append("from ads_api.models.v0._shared import (")
        for name in shared_names:
            lines.append(f"    {name},")
        lines.append(")")
        lines.append("")

    lines.append("")
    return "\n".join(lines)


def render_models_module(
    tag: str,
    emitted: list[EmittedModel],
    name_map: NameMap,
    *,
    shared_names: set[str] | None = None,
    shared_module: str | None = None,
) -> str:
    shared = shared_names or set()
    local = [item for item in emitted if item.python_name not in shared]
    openapi_schemas = {item.key.openapi_name: item.schema for item in emitted}
    enums, regular, composition = split_types(local)
    imports = ImportSet()
    body = ""
    for group in (enums, regular, composition):
        for item in group:
            body += emit_model(item, openapi_schemas, name_map, imports) + "\n\n"
    public = sorted({item.python_name for item in emitted})
    if public:
        body += f"__all__ = [{', '.join(repr(n) for n in public)}]\n"
    header = _render_import_header(tag, imports, shared_module, sorted(shared))
    return header + body


def render_shared_module(product_module: str, emitted: list[EmittedModel], name_map: NameMap) -> str:
    return render_models_module(
        f"{product_module} (shared)",
        emitted,
        name_map,
    ).replace(
        f'"""Auto-generated models for {product_module} (shared) from Amazon Ads API v0."""',
        '"""Shared models reused across Amazon Ads API v0 entities."""',
    )


def _resolve_params(spec: dict[str, Any], operation: dict[str, Any]) -> list[dict[str, Any]]:
    spec_params = spec.get("components", {}).get("parameters", {})
    resolved: list[dict[str, Any]] = []
    for param in operation.get("parameters", []):
        if "$ref" in param:
            resolved.append(spec_params.get(param["$ref"].split("/")[-1], {}))
        else:
            resolved.append(param)
    return [p for p in resolved if p]


def _first_schema_seed(schema: dict[str, Any]) -> tuple[str | None, bool]:
    if schema.get("type") == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            return items["$ref"].split("/")[-1], True
        return None, True
    if "$ref" in schema:
        return schema["$ref"].split("/")[-1], False
    return None, False


def _vendor_stem(media_type: str) -> str:
    rest = media_type.removeprefix("application/vnd.").split("+", 1)[0]
    return re.sub(r"\.v[\d.]+$", "", rest)


def _same_vendor_family(media_types: list[str]) -> bool:
    return len({_vendor_stem(item) for item in media_types}) == 1


def _vendor_headers(operation: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    """Static vendor headers plus Accept choices when the caller must pick one.

    Request vendor Content-Type is also used as Accept: Amazon often rejects
    ``Accept: application/json`` even when the body type is already vendor JSON.
    """
    headers: dict[str, str] = {}
    request_content = operation.get("requestBody", {}).get("content", {})
    if request_content:
        content_type = next(iter(request_content))
        if content_type != "application/json":
            headers["Content-Type"] = content_type
            headers["Accept"] = content_type

    response_accepts: list[str] = []
    for code, resp in operation.get("responses", {}).items():
        if str(code) not in SUCCESS_CODES:
            continue
        for media_type in resp.get("content", {}):
            if media_type != "application/json" and media_type not in response_accepts:
                response_accepts.append(media_type)

    if "Accept" not in headers:
        if len(response_accepts) == 1:
            headers["Accept"] = response_accepts[0]
            return headers, []
        if len(response_accepts) > 1:
            return headers, response_accepts
    return headers, []


def render_client_module(
    *,
    spec: dict[str, Any],
    tag: str,
    resource_name: str,
    models_import: str,
    endpoints: list[tuple[str, str, dict[str, Any]]],
    emitted: list[EmittedModel],
    name_map: NameMap,
) -> str:
    all_schemas = spec.get("components", {}).get("schemas", {})
    openapi_schemas = {item.key.openapi_name: item.schema for item in emitted}

    sig_imports: set[str] = set()
    for _method, _path, operation in endpoints:
        for media in operation.get("requestBody", {}).get("content", {}).values():
            seed, _ = _first_schema_seed(media.get("schema", {}))
            if seed:
                sig_imports.add(name_map.resolve_request(seed))
        for code, resp in operation.get("responses", {}).items():
            if str(code) in SUCCESS_CODES:
                for media in resp.get("content", {}).values():
                    seed, _ = _first_schema_seed(media.get("schema", {}))
                    if seed:
                        sig_imports.add(name_map.resolve_response(seed, all_schemas.get(seed, {})))
        for param in _resolve_params(spec, operation):
            seed, _ = _first_schema_seed(param.get("schema", {}))
            if seed:
                sig_imports.add(name_map.resolve(seed, SchemaRole.OUTPUT))

    lines = [
        f'"""{resource_name} resource operations.',
        "",
        f"Generated from OpenAPI spec (tag: {tag}).",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any, Literal, overload",
        "",
        "import httpx",
        "",
        "from ads_api.base import BaseResource",
        "",
    ]
    if sig_imports:
        lines.append(f"from {models_import} import (")
        for name in sorted(sig_imports):
            lines.append(f"    {name},")
        lines.append(")")
        lines.append("")
    lines.append("")
    lines.append(f"class {resource_name}(BaseResource):")
    if resource_name.startswith("Test"):
        lines.append("    __test__ = False")
    lines.append("")

    unused = ImportSet()
    if not endpoints:
        lines.append("    pass")
        lines.append("")
    method_names = unique_method_names(endpoints)
    for (http_method, path, operation), mname in zip(endpoints, method_names, strict=True):
        _append_method(
            lines,
            spec=spec,
            http_method=http_method,
            path=path,
            operation=operation,
            method_name=mname,
            all_schemas=all_schemas,
            openapi_schemas=openapi_schemas,
            name_map=name_map,
            imports=unused,
        )

    return "\n".join(lines)


def _append_method(
    lines: list[str],
    *,
    spec: dict[str, Any],
    http_method: str,
    path: str,
    operation: dict[str, Any],
    method_name: str,
    all_schemas: dict[str, Any],
    openapi_schemas: dict[str, Any],
    name_map: NameMap,
    imports: ImportSet,
) -> None:
    mname = method_name
    desc = operation.get("description", "").strip().split("\n")[0] if operation.get("description") else ""
    desc = desc.replace('"""', "").replace('"', "'")
    extra_headers, accept_choices = _vendor_headers(operation)

    req_model = None
    is_array_req = False
    for media in operation.get("requestBody", {}).get("content", {}).values():
        seed, is_array_req = _first_schema_seed(media.get("schema", {}))
        if seed:
            req_model = name_map.resolve_request(seed)
            break

    resp_model = None
    is_array_resp = False
    for code, resp in operation.get("responses", {}).items():
        if str(code) in SUCCESS_CODES:
            for media in resp.get("content", {}).values():
                seed, is_array_resp = _first_schema_seed(media.get("schema", {}))
                if seed:
                    resp_model = name_map.resolve_response(seed, all_schemas.get(seed, {}))
                    break
            if resp_model:
                break

    resolved_params = _resolve_params(spec, operation)
    path_params = [p for p in resolved_params if p.get("in") == "path"]
    query_params = [p for p in resolved_params if p.get("in") == "query"]

    def type_fn(s: dict[str, Any], field_name: str | None = None) -> str:
        t = schema_type(s, openapi_schemas, name_map, SchemaRole.OUTPUT, imports, field_name=field_name)
        match = _LENIENT_ENUM_RE.match(t)
        if match:
            return match.group(1)
        if t.startswith("Annotated[") and "lenient_enum(" in t:
            inner = t.removeprefix("Annotated[").split(",", 1)[0].strip()
            return inner
        return t

    pos_args = ["self"]
    for p in path_params:
        pos_args.append(f"{camel_to_snake(p['name'])}: {type_fn(p.get('schema', {}), field_name=p.get('name'))}")

    opt_query: list[str] = []
    for p in query_params:
        py_name = camel_to_snake(p["name"])
        ptype = type_fn(p.get("schema", {}), field_name=p.get("name"))
        if p.get("required", False):
            pos_args.append(f"{py_name}: {ptype}")
        else:
            opt_query.append(f"{py_name}: {ptype} | None = None")

    # OpenAPI requestBody.required 默认 false；未标 true 的 list 类接口允许省略 body。
    body_required = bool(operation.get("requestBody", {}).get("required", False))
    if req_model:
        req_type = f"list[{req_model}]" if is_array_req else req_model
        if body_required:
            pos_args.append(f"body: {req_type}")
        else:
            pos_args.append(f"body: {req_type} | None = None")

    url_expr = path
    for p in path_params:
        url_expr = url_expr.replace(f"{{{p['name']}}}", f"{{{camel_to_snake(p['name'])}}}")
    url_str = f'f"{url_expr}"' if path_params else f'"{url_expr}"'

    if resp_model:
        model_ret = f"list[{resp_model}]" if is_array_resp else resp_model
        dict_ret = "list[dict[str, Any]]" if is_array_resp else "dict[str, Any]"
    else:
        model_ret = "Any"
        dict_ret = "Any"

    extra_kw: list[str] = []
    if accept_choices:
        lit = ", ".join(repr(item) for item in accept_choices)
        if _same_vendor_family(accept_choices):
            extra_kw.append(f"accept: Literal[{lit}] = {accept_choices[0]!r}")
        else:
            extra_kw.append(f"accept: Literal[{lit}]")

    def make_sig(mode_type: str, ret_type: str, default_mode: bool = False) -> str:
        kw = list(extra_kw)
        kw.append('mode: Literal["dict"] = "dict"' if default_mode else f"mode: {mode_type}")
        kw.extend(opt_query)
        return f"    async def {mname}({', '.join(pos_args + ['*'] + kw)}) -> {ret_type}: ..."

    lines.append("    @overload")
    lines.append(make_sig('Literal["dict"]', dict_ret, default_mode=True))
    lines.append("    @overload")
    lines.append(make_sig('Literal["pydantic"]', model_ret))
    lines.append("    @overload")
    lines.append(make_sig('Literal["raw"]', "httpx.Response"))

    impl_kw = extra_kw + ['mode: Literal["pydantic", "dict", "raw"] = "dict"'] + opt_query
    impl_ret = f"{model_ret} | {dict_ret} | httpx.Response" if resp_model else "Any"
    lines.append(f"    async def {mname}({', '.join(pos_args + ['*'] + impl_kw)}) -> {impl_ret}:")
    lines.append(f'        """{desc}"""' if desc else '        """"""')
    lines.append("")

    extra_parts: list[str] = []
    if http_method == "GET" or query_params:
        if query_params:
            lines.append("        params = {")
            for p in query_params:
                lines.append(f'            "{p["name"]}": {camel_to_snake(p["name"])},')
            lines.append("        }")
            if any(not p.get("required", False) for p in query_params):
                lines.append("        params = {k: v for k, v in params.items() if v is not None}")
            extra_parts.append("params=params")
        if req_model:
            extra_parts.append("json=self.dump_json(body)")
    elif req_model:
        extra_parts.append("json=self.dump_json(body)")
    if accept_choices:
        static = dict(extra_headers)
        lines.append(f"        headers = {static!r}")
        lines.append('        headers["Accept"] = accept')
        extra_parts.append("headers=headers")
    elif extra_headers:
        extra_parts.append(f"headers={extra_headers!r}")
    extra = f", {', '.join(extra_parts)}" if extra_parts else ""
    lines.append(f'        resp = await self._request("{http_method}", {url_str}{extra})')

    if is_array_resp and resp_model:
        lines.append(f"        return self._response_list({resp_model}, resp, mode=mode)")
    elif resp_model:
        lines.append(f"        return self._response({resp_model}, resp, mode=mode)")
    else:
        lines.append("        if mode == 'raw':")
        lines.append("            return resp")
        lines.append("        return resp.json()")
    lines.append("")
    lines.append("")
