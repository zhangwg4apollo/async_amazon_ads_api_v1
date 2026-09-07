"""OpenAPI schema discovery: request vs response closures and Python names."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Literal

from codegen.spec import camel_to_snake, strip_product_prefix

SUCCESS_CODES = frozenset({"200", "201", "207"})
_ENTITY_FIELDS = frozenset(
    {
        "ruleDetails",
        "accountInfo",
        "countryCode",
        "currencyCode",
        "timezone",
        "dailyBudget",
        "budgetRulesDetails",
        "associatedRules",
        "budgetRule",
    }
)


class SchemaRole(StrEnum):
    INPUT = "input"
    OUTPUT = "output"
    MUTATION_RESULT = "mutation_result"
    NEUTRAL = "neutral"


ExtraMode = Literal["forbid", "allow"]


@dataclass(frozen=True)
class SchemaKey:
    openapi_name: str
    role: SchemaRole


@dataclass(frozen=True)
class EmittedModel:
    key: SchemaKey
    python_name: str
    schema: dict[str, Any]
    extra: ExtraMode


def is_enum(schema: dict[str, Any]) -> bool:
    return bool(schema.get("enum"))


def is_type_alias(schema: dict[str, Any]) -> bool:
    return (
        "type" in schema
        and schema["type"] in ("string", "integer", "boolean", "number")
        and "properties" not in schema
        and "allOf" not in schema
        and not schema.get("enum")
    )


def extract_refs(schema: Any) -> set[str]:
    refs: set[str] = set()

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            if "$ref" in obj:
                refs.add(obj["$ref"].split("/")[-1])
                return
            for key in ("properties", "additionalProperties", "items"):
                if key in obj:
                    walk(obj[key])
            for key in ("oneOf", "anyOf", "allOf"):
                if key in obj:
                    for item in obj[key]:
                        walk(item)
            for value in obj.values():
                if isinstance(value, (dict, list)):
                    walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(schema)
    return refs


def flatten_allof(schema: dict[str, Any], schemas: dict[str, Any]) -> dict[str, Any]:
    if "allOf" not in schema:
        return schema

    merged_props: dict[str, Any] = {}
    merged_required: set[str] = set()
    for entry in schema["allOf"]:
        if "$ref" in entry:
            ref_schema = schemas.get(entry["$ref"].split("/")[-1], {})
            resolved = flatten_allof(ref_schema, schemas)
            for key, value in resolved.get("properties", {}).items():
                merged_props.setdefault(key, value)
            merged_required.update(resolved.get("required", []))
        else:
            for key, value in entry.get("properties", {}).items():
                merged_props.setdefault(key, value)
            merged_required.update(entry.get("required", []))

    merged_required.update(schema.get("required", []))
    result = dict(schema)
    result["properties"] = merged_props
    result["required"] = list(merged_required)
    return result


def collapse_single_oneof(schema: dict[str, Any]) -> dict[str, Any]:
    """If oneOf has a single object variant, treat it as that object."""
    variants = schema.get("oneOf")
    if not variants or "properties" in schema or len(variants) != 1:
        return schema
    variant = variants[0]
    if variant.get("type") == "object" and "properties" in variant:
        merged = dict(schema)
        del merged["oneOf"]
        merged["properties"] = variant["properties"]
        if "required" in variant:
            merged["required"] = variant["required"]
        merged["type"] = "object"
        return merged
    return schema


def _schema_ref_seeds(schema: dict[str, Any]) -> set[str]:
    if "$ref" in schema:
        return {schema["$ref"].split("/")[-1]}
    if schema.get("type") == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            return {items["$ref"].split("/")[-1]}
    return set()


def _collect_seeds(
    endpoints: list[tuple[str, str, dict[str, Any]]],
    spec: dict[str, Any],
    *,
    from_request: bool,
    from_response: bool,
) -> set[str]:
    seeds: set[str] = set()
    spec_params = spec.get("components", {}).get("parameters", {})
    for _method, _path, operation in endpoints:
        if from_request:
            for media in operation.get("requestBody", {}).get("content", {}).values():
                seeds |= _schema_ref_seeds(media.get("schema", {}))
            for param in operation.get("parameters", []):
                if "$ref" in param:
                    param = spec_params.get(param["$ref"].split("/")[-1], param)
                seeds |= _schema_ref_seeds(param.get("schema", {}))
        if from_response:
            for code, resp in operation.get("responses", {}).items():
                if str(code) in SUCCESS_CODES:
                    for media in resp.get("content", {}).values():
                        seeds |= _schema_ref_seeds(media.get("schema", {}))
    return seeds


def _bfs(all_schemas: dict[str, Any], seeds: set[str]) -> set[str]:
    closure: set[str] = set(seeds)
    queue = list(seeds)
    while queue:
        name = queue.pop(0)
        schema = all_schemas.get(name, {})
        for dep in extract_refs(schema):
            if dep not in closure:
                closure.add(dep)
                queue.append(dep)
    return closure


def discover_schema_sets(
    spec: dict[str, Any],
    endpoints: list[tuple[str, str, dict[str, Any]]],
) -> tuple[set[str], set[str]]:
    all_schemas = spec.get("components", {}).get("schemas", {})
    request_names = _bfs(all_schemas, _collect_seeds(endpoints, spec, from_request=True, from_response=False))
    response_names = _bfs(all_schemas, _collect_seeds(endpoints, spec, from_request=False, from_response=True))
    return request_names, response_names


def is_mutation_result_schema(schema: dict[str, Any]) -> bool:
    props = set(schema.get("properties", {}))
    if "code" not in props or "details" not in props:
        return False
    return not bool(props & _ENTITY_FIELDS)


def _assert_unique_python_names(emitted: list[EmittedModel]) -> None:
    by_python: dict[str, list[SchemaKey]] = {}
    for item in emitted:
        by_python.setdefault(item.python_name, []).append(item.key)
    collisions = {name: ks for name, ks in by_python.items() if len(ks) > 1}
    if collisions:
        details = "; ".join(
            f"{target} ← {', '.join(f'{k.openapi_name}[{k.role}]' for k in ks)}"
            for target, ks in sorted(collisions.items())
        )
        raise RuntimeError(f"Schema naming collisions: {details}")


def python_name_for(openapi_name: str, role: SchemaRole, shared_entities: set[str]) -> str:
    if role == SchemaRole.NEUTRAL:
        return openapi_name
    if role == SchemaRole.INPUT:
        return openapi_name
    if role == SchemaRole.MUTATION_RESULT:
        if openapi_name.endswith("Result"):
            return openapi_name
        stem = openapi_name[: -len("Response")] if openapi_name.endswith("Response") else openapi_name
        return f"{stem}Result"
    if role == SchemaRole.OUTPUT:
        if openapi_name in shared_entities:
            return f"{openapi_name}Out"
        return openapi_name
    raise ValueError(f"Unknown role: {role}")


class NameMap:
    def __init__(self, emitted: list[EmittedModel]) -> None:
        self._by_key = {item.key: item.python_name for item in emitted}
        self._by_openapi: dict[str, dict[SchemaRole, str]] = {}
        self._neutral: set[str] = set()
        for item in emitted:
            self._by_openapi.setdefault(item.key.openapi_name, {})[item.key.role] = item.python_name
            if item.key.role == SchemaRole.NEUTRAL:
                self._neutral.add(item.key.openapi_name)

    def resolve(self, openapi_name: str, context_role: SchemaRole) -> str:
        if openapi_name in self._neutral:
            return self._by_key[SchemaKey(openapi_name, SchemaRole.NEUTRAL)]
        roles = self._by_openapi.get(openapi_name, {})
        for role in (context_role, SchemaRole.OUTPUT, SchemaRole.INPUT, SchemaRole.NEUTRAL, SchemaRole.MUTATION_RESULT):
            if role in roles:
                return roles[role]
        return openapi_name

    def resolve_request(self, openapi_name: str) -> str:
        return self.resolve(openapi_name, SchemaRole.INPUT)

    def resolve_response(self, openapi_name: str, schema: dict[str, Any]) -> str:
        if is_mutation_result_schema(schema):
            return self.resolve(openapi_name, SchemaRole.MUTATION_RESULT)
        return self.resolve(openapi_name, SchemaRole.OUTPUT)


def discover_emissions(
    spec: dict[str, Any],
    endpoints: list[tuple[str, str, dict[str, Any]]],
) -> tuple[list[EmittedModel], NameMap]:
    all_schemas = spec.get("components", {}).get("schemas", {})
    request_names, response_names = discover_schema_sets(spec, endpoints)
    shared_entities = request_names & response_names

    keys: list[SchemaKey] = []
    for name in sorted(request_names | response_names):
        schema = all_schemas.get(name, {})
        if not schema:
            continue
        if (is_enum(schema) and schema.get("enum")) or is_type_alias(schema):
            keys.append(SchemaKey(name, SchemaRole.NEUTRAL))
            continue
        if name in request_names:
            keys.append(SchemaKey(name, SchemaRole.INPUT))
        if name in response_names:
            role = SchemaRole.MUTATION_RESULT if is_mutation_result_schema(schema) else SchemaRole.OUTPUT
            keys.append(SchemaKey(name, role))

    emitted: list[EmittedModel] = []
    for key in keys:
        schema = all_schemas[key.openapi_name]
        python_name = python_name_for(key.openapi_name, key.role, shared_entities)
        extra: ExtraMode = "forbid" if key.role == SchemaRole.INPUT else "allow"
        emitted.append(EmittedModel(key=key, python_name=python_name, schema=schema, extra=extra))

    _assert_unique_python_names(emitted)
    return emitted, NameMap(emitted)


def method_name(operation_id: str) -> str:
    return camel_to_snake(strip_product_prefix(operation_id))


def _item_fingerprint(item: EmittedModel) -> str:
    return repr(
        (
            item.python_name,
            item.extra,
            item.key.role.value,
            item.schema,
        )
    )


def select_shared_models(entity_emissions: list[list[EmittedModel]]) -> list[EmittedModel]:
    """Return models identical across 2+ entities whose $ref deps are also shared."""
    if len(entity_emissions) < 2:
        return []

    by_name: dict[str, list[tuple[EmittedModel, str]]] = {}
    openapi_to_python: dict[str, str] = {}
    for emitted in entity_emissions:
        seen: set[str] = set()
        for item in emitted:
            if item.python_name in seen:
                continue
            seen.add(item.python_name)
            by_name.setdefault(item.python_name, []).append((item, _item_fingerprint(item)))
            openapi_to_python.setdefault(item.key.openapi_name, item.python_name)

    candidates: dict[str, EmittedModel] = {}
    for name, occ in by_name.items():
        entities_hit = len(occ)
        if entities_hit < 2:
            continue
        fingerprints = {fp for _, fp in occ}
        if len(fingerprints) != 1:
            continue
        candidates[name] = occ[0][0]

    emitted_names = set(by_name)
    changed = True
    while changed:
        changed = False
        for name in list(candidates):
            item = candidates[name]
            for ref in extract_refs(item.schema):
                dep = openapi_to_python.get(ref)
                if dep is None or dep not in emitted_names:
                    continue
                if dep not in candidates:
                    del candidates[name]
                    changed = True
                    break

    return sorted(candidates.values(), key=lambda x: x.python_name)
