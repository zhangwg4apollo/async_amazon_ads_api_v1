"""OpenAPI spec loading, product detection, and ALL-vs-product operation filtering."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "head", "options", "trace"})

# Longest-first so SPGLOBAL wins over SP.
_PRODUCT_RE = re.compile(r"^AmazonAdsAPI(ALL|SPGLOBAL|SP|SB|SD|DSP|ST)")

PRODUCTS: dict[str, Product] = {}


@dataclass(frozen=True)
class Product:
    key: str
    module: str
    prefix: str
    spec_filename: str


def _register(key: str, module: str, prefix: str, spec_filename: str | None = None) -> Product:
    product = Product(
        key=key,
        module=module,
        prefix=prefix,
        spec_filename=spec_filename or f"AmazonAdsAPI{key}Merged_prod_3p.json",
    )
    PRODUCTS[key] = product
    return product


ALL = _register("ALL", "general", "")
SP = _register("SP", "sp", "SP")
SPGLOBAL = _register("SPGLOBAL", "sp_global", "SPGlobal")
SB = _register("SB", "sb", "SB")
SD = _register("SD", "sd", "SD")
DSP = _register("DSP", "dsp", "DSP")
ST = _register("ST", "st", "ST")
REPORTS = _register(
    "REPORTS",
    "general",
    "",
    "AmazonAdsAPIALLReportsContract_prod_3p_BETA.json",
)

PRODUCT_ORDER = (ALL, SP, SPGLOBAL, SB, SD, DSP, ST, REPORTS)
AD_PRODUCTS = (SP, SPGLOBAL, SB, SD, DSP, ST)
_PREFIXES_FOR_STRIP = tuple(
    p.prefix for p in sorted((SP, SPGLOBAL, SB, SD, DSP, ST), key=lambda x: -len(x.prefix)) if p.prefix
)
_OP_ID_PREFIXES = ("AdsApiv1",) + _PREFIXES_FOR_STRIP


def product_from_filename(filename: str) -> Product:
    m = _PRODUCT_RE.match(filename)
    if not m:
        raise ValueError(f"无法从文件名解析产品: {filename}")
    return PRODUCTS[m.group(1)]


def strip_product_prefix(name: str) -> str:
    for prefix in _PREFIXES_FOR_STRIP:
        if name.startswith(prefix) and len(name) > len(prefix) and name[len(prefix)].isupper():
            return name[len(prefix) :]
    return name


def strip_operation_id_prefix(name: str) -> str:
    for prefix in _OP_ID_PREFIXES:
        if name.startswith(prefix) and len(name) > len(prefix) and name[len(prefix)].isupper():
            return name[len(prefix) :]
    return name


def camel_to_snake(name: str) -> str:
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)
    return s.lower().strip("_")


def snake_to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_operations(spec: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    """Return operations in a stable order for reproducible client modules.

    Operations marked ``deprecated: true`` are skipped (legacy ad-product path
    aliases, etc.) so they are not emitted as client methods.
    """
    result: list[tuple[str, str, dict[str, Any]]] = []
    for path, methods in spec.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            if operation.get("deprecated") is True:
                continue
            result.append((method.upper(), path, operation))
    return sorted(
        result,
        key=lambda item: (
            camel_to_snake(strip_operation_id_prefix(item[2].get("operationId", "endpoint"))),
            item[1],
            item[0],
        ),
    )


def filter_operations_by_tag(
    endpoints: list[tuple[str, str, dict[str, Any]]], tag: str
) -> list[tuple[str, str, dict[str, Any]]]:
    return [op for op in endpoints if tag in op[2].get("tags", [])]


def operation_keys(spec: dict[str, Any]) -> set[tuple[str, str]]:
    return {(method, path) for method, path, _ in iter_operations(spec)}


def unique_tags(spec: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for _method, _path, operation in iter_operations(spec):
        for tag in operation.get("tags", []):
            if tag not in seen:
                seen.add(tag)
                tags.append(tag)
    return tags


def drop_covered_operations(all_spec: dict[str, Any], covered: set[tuple[str, str]]) -> dict[str, Any]:
    """Remove ALL operations whose (method, path) already exist on a product spec."""
    paths = all_spec.get("paths", {})
    for path in list(paths):
        item = paths[path]
        if not isinstance(item, dict):
            continue
        for method in list(item):
            if method.lower() not in HTTP_METHODS:
                continue
            if (method.upper(), path) in covered:
                del item[method]
        if not any(k.lower() in HTTP_METHODS for k in item):
            del paths[path]
    return all_spec


def is_prefixed(name: str, prefix: str) -> bool:
    """True if *name* already uses *prefix* as a PascalCase product prefix."""
    if not name.startswith(prefix):
        return False
    if len(name) == len(prefix):
        return True
    return name[len(prefix)].isupper()


def apply_schema_prefix(spec: dict[str, Any], prefix: str) -> dict[str, Any]:
    """Prefix unprefixed component schema names and rewrite $ref targets."""
    if not prefix:
        return spec
    schemas = spec.get("components", {}).get("schemas", {})
    rename: dict[str, str] = {}
    for name in list(schemas):
        rename[name] = name if is_prefixed(name, prefix) else f"{prefix}{name}"

    def rewrite(obj: Any) -> Any:
        if isinstance(obj, dict):
            if "$ref" in obj and isinstance(obj["$ref"], str):
                ref = obj["$ref"]
                marker = "#/components/schemas/"
                if ref.startswith(marker):
                    old = ref[len(marker) :]
                    if old in rename:
                        obj["$ref"] = marker + rename[old]
            for value in obj.values():
                rewrite(value)
        elif isinstance(obj, list):
            for item in obj:
                rewrite(item)
        return obj

    rewrite(spec)
    spec["components"]["schemas"] = {rename[name]: schema for name, schema in schemas.items()}
    return spec
