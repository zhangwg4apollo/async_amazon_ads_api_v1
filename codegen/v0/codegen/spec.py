"""v0 OpenAPI loading, entity naming, and operation helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "head", "options", "trace"})
_PRODUCT_PREFIXES = ("SPGlobal", "SP", "SB", "SD", "DSP", "ST")

# 产品选择：生成哪些 Amazon Ads API v0 TOC 分组。其余字段由 toc_name 推断。
INCLUDED_TOC_SECTIONS: tuple[str, ...] = (
    "Accounts",
    "Reporting",
    "Ads data manager",
    "Exports",
    "Discovery",
    "Portfolios",
    "Products",
    "Sponsored Products",
    "Sponsored Brands",
    "Sponsored Display",
)

# TOC 分组目录名。未列出的用 camel_to_snake(toc_name)。
GROUP_KEY_OVERRIDES: dict[str, str] = {
    "Sponsored Products": "sp",
    "Sponsored Brands": "sb",
    "Sponsored Display": "sd",
}

# TOC 项名为 Version N 时落到 <product>_vN（如 sp_v3）。列出的分组只下载这些版本。
INCLUDED_VERSIONS: dict[str, frozenset[str]] = {
    "Sponsored Products": frozenset({"v3"}),
    "Sponsored Brands": frozenset({"v4"}),
}

# TOC 项名无法得到稳定 SDK 路径时才手写。默认是去括号 / Version N 后转 snake。
ENTITY_OVERRIDES: dict[str, str] = {
    "Account management (beta)": "advertising_accounts",
    "DSP Advertiser Accounts": "dsp_advertisers",
    "Version 3 reporting": "reports",
    # 整份 SD spec；若用 campaign_management，Campaigns tag 会被当成父实体。
    "Campaign management": "sd",
}

_VERSION_ITEM_RE = re.compile(r"(?i)^version\s+(\d+)$")
_SHORT_PRODUCT_KEYS = frozenset({"sp", "sb", "sd", "st"})
_VERSION_KEY_RE = re.compile(r"^v\d+$")


@dataclass(frozen=True)
class TocGroup:
    key: str
    toc_name: str
    namespace_class: str
    namespace_doc: str
    version: str | None = None

    @classmethod
    def from_toc_name(cls, toc_name: str) -> TocGroup:
        key = GROUP_KEY_OVERRIDES.get(toc_name) or camel_to_snake(toc_name)
        return cls(
            key=key,
            toc_name=toc_name,
            namespace_class=group_class_name(key),
            namespace_doc=f"v0 {toc_name} APIs",
        )


def strip_product_prefix(name: str) -> str:
    for prefix in _PRODUCT_PREFIXES:
        if name.startswith(prefix) and len(name) > len(prefix) and name[len(prefix)].isupper():
            return name[len(prefix) :]
    return name


def camel_to_snake(name: str) -> str:
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s)
    return s.lower().strip("_")


def snake_to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_") if part)


def group_class_name(key: str) -> str:
    """sp → SP，sp_v3 → SPV3，accounts → Accounts。"""
    parts = key.split("_")
    if parts[0] in _SHORT_PRODUCT_KEYS:
        rest = "".join(part.upper() if _VERSION_KEY_RE.fullmatch(part) else snake_to_pascal(part) for part in parts[1:])
        return parts[0].upper() + rest
    return snake_to_pascal(key)


def pascalize_schema_name(name: str) -> str:
    if name and name[0].islower():
        return name[0].upper() + name[1:]
    return name


def resource_class_name(entity_snake: str) -> str:
    if entity_snake.startswith("dsp_"):
        return "DSP" + snake_to_pascal(entity_snake.removeprefix("dsp_"))
    return snake_to_pascal(entity_snake)


def _build_groups() -> tuple[TocGroup, ...]:
    groups: list[TocGroup] = []
    for toc_name in INCLUDED_TOC_SECTIONS:
        versions = INCLUDED_VERSIONS.get(toc_name)
        if not versions:
            groups.append(TocGroup.from_toc_name(toc_name))
            continue
        product = GROUP_KEY_OVERRIDES.get(toc_name) or camel_to_snake(toc_name)
        for version in sorted(versions):
            key = f"{product}_{version}"
            groups.append(
                TocGroup(
                    key=key,
                    toc_name=toc_name,
                    namespace_class=group_class_name(key),
                    namespace_doc=f"v0 {toc_name} {version} APIs",
                    version=version,
                )
            )
    return tuple(groups)


GROUPS: tuple[TocGroup, ...] = _build_groups()


def version_from_toc_name(name: str) -> str | None:
    """TOC 项名为 ``Version 3`` 时返回 ``v3``；``Version 3 reporting`` 不算版本目录。"""
    match = _VERSION_ITEM_RE.fullmatch(name.strip())
    if match is None:
        return None
    return f"v{match.group(1)}"


def spec_folder_from_toc_name(name: str) -> str:
    """非版本 TOC 项的 spec 目录名。版本项由 TocGroup.key（如 sp_v3）承接。"""
    return entity_from_toc_name(name)


def entity_from_toc_name(name: str) -> str:
    if name in ENTITY_OVERRIDES:
        return ENTITY_OVERRIDES[name]
    cleaned = re.sub(r"\s*\([^)]*\)", "", name).strip()
    cleaned = re.sub(r"(?i)^version\s+\d+\s+", "", cleaned).strip()
    return camel_to_snake(cleaned) or camel_to_snake(name)


def _abbreviate_entity(snake: str) -> str:
    return "".join(part[0] for part in snake.split("_") if part)


def _tag_entity(tag: str, fallback: str) -> str:
    snake = camel_to_snake(tag)
    if not snake:
        return fallback
    parent_tokens = set(fallback.split("_"))
    stem = snake[:-1] if snake.endswith("s") and not snake.endswith("ss") else snake
    plural = snake if snake.endswith("s") else f"{snake}s"
    if stem in parent_tokens or snake in parent_tokens or plural in parent_tokens:
        return fallback
    return snake


def entities_from_tags(tags: list[str], fallback: str, reserved: set[str]) -> dict[str, str]:
    """Map resource tags to entity names.

    Primary tag (stem / singular / plural appears in the parent entity) keeps
    the parent name. Other tags are snake_case of the tag. If any sibling would
    collide with another spec's entity, all non-primary siblings get the parent
    abbreviation prefix (marketing_mix_modeling → mmm_).
    """
    mapping: dict[str, str] = {}
    children: list[str] = []
    for tag in tags:
        entity = _tag_entity(tag, fallback)
        mapping[tag] = entity
        if entity != fallback:
            children.append(tag)

    occupied = set(reserved) - {fallback}
    if any(mapping[tag] in occupied for tag in children):
        prefix = _abbreviate_entity(fallback)
        for tag in children:
            name = mapping[tag]
            if prefix and not name.startswith(f"{prefix}_"):
                mapping[tag] = f"{prefix}_{name}"
    return mapping


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_spec(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        import yaml

        spec = yaml.safe_load(text)
    else:
        spec = json.loads(text)
    if not isinstance(spec, dict):
        raise ValueError(f"OpenAPI spec 不是 object: {path}")
    return normalize_openapi(spec)


def normalize_openapi(spec: dict[str, Any]) -> dict[str, Any]:
    """YAML 会把 200 解析成 int，统一成 str 以便和 SUCCESS_CODES 对齐。"""
    for methods in spec.get("paths", {}).values():
        if not isinstance(methods, dict):
            continue
        for operation in methods.values():
            if not isinstance(operation, dict):
                continue
            responses = operation.get("responses")
            if isinstance(responses, dict):
                operation["responses"] = {str(code): body for code, body in responses.items()}
    return spec


def iter_operations(spec: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    result: list[tuple[str, str, dict[str, Any]]] = []
    for path, methods in spec.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            result.append((method.upper(), path, operation))
    return sorted(
        result,
        key=lambda item: (
            operation_method_name(item[0], item[1], item[2]),
            item[1],
            item[0],
        ),
    )


def unique_tags(spec: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for _method, _path, operation in iter_operations(spec):
        for tag in operation.get("tags", []):
            tag = str(tag).strip()
            if tag and tag not in seen:
                seen.add(tag)
                tags.append(tag)
    return tags


def filter_operations_by_tag(
    endpoints: list[tuple[str, str, dict[str, Any]]], tag: str
) -> list[tuple[str, str, dict[str, Any]]]:
    wanted = tag.strip()
    return [
        (method, path, operation)
        for method, path, operation in endpoints
        if wanted in [str(t).strip() for t in operation.get("tags", [])]
    ]


def should_split_by_tag(spec: dict[str, Any]) -> bool:
    """True when tags look like resource groups, not one-tag-per-operation."""
    tags = unique_tags(spec)
    ops = iter_operations(spec)
    return len(tags) > 1 and len(tags) < len(ops)


def collect_all_routes(section: dict[str, Any]) -> dict[str, str]:
    """Flatten route → openapi across a TOC node and its descendants."""
    routes: dict[str, str] = {}

    def walk(node: dict[str, Any]) -> None:
        for entry in node.get("routes", []):
            route = entry["route"]
            if route not in routes:
                routes[route] = entry["openapi"]
        for child in node.get("items", []):
            if isinstance(child, dict):
                walk(child)

    walk(section)
    return routes


def path_method_name(http_method: str, path: str) -> str:
    """HTTP method + path；缺 operationId 或同资源撞名时用。"""
    parts = [p for p in path.strip("/").split("/") if p and not p.startswith("{")]
    if parts and parts[0].lower() in _SHORT_PRODUCT_KEYS:
        parts = parts[1:]
    last = camel_to_snake(parts[-1]) if parts else "resource"
    has_path_param = "{" in path
    if http_method == "GET" and not has_path_param:
        return last if last.startswith("list_") else f"list_{last}"
    verb = {
        "GET": "get",
        "POST": "create",
        "PUT": "update",
        "PATCH": "patch",
        "DELETE": "delete",
    }.get(http_method, http_method.lower())
    stem = last[:-1] if last.endswith("s") and not last.endswith("ss") else last
    if len(parts) >= 2:
        prefix = "_".join(camel_to_snake(p) for p in parts[:-1])
        return f"{verb}_{prefix}_{stem}"
    return f"{verb}_{stem}"


def operation_method_name(http_method: str, path: str, operation: dict[str, Any]) -> str:
    op_id = operation.get("operationId")
    if isinstance(op_id, str) and op_id.strip():
        return camel_to_snake(strip_product_prefix(op_id.strip()))
    return path_method_name(http_method, path)


def unique_method_names(endpoints: list[tuple[str, str, dict[str, Any]]]) -> list[str]:
    """同一资源内方法名撞车时，缺 operationId 的一侧改用更长的 path 名。"""
    names = [operation_method_name(method, path, operation) for method, path, operation in endpoints]
    counts: dict[str, int] = {}
    for name in names:
        counts[name] = counts.get(name, 0) + 1
    if all(count == 1 for count in counts.values()):
        return names

    resolved: list[str] = []
    for name, (method, path, _operation) in zip(names, endpoints, strict=True):
        resolved.append(path_method_name(method, path) if counts[name] > 1 else name)

    again: dict[str, int] = {}
    for name in resolved:
        again[name] = again.get(name, 0) + 1
    if all(count == 1 for count in again.values()):
        return resolved

    final: list[str] = []
    for name, (_method, path, _operation) in zip(resolved, endpoints, strict=True):
        if again[name] == 1:
            final.append(name)
            continue
        params = "_".join(camel_to_snake(p[1:-1]) for p in path.split("/") if p.startswith("{"))
        final.append(f"{name}_by_{params}" if params else name)
    return final
