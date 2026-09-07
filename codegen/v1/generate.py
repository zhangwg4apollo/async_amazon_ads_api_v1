"""Generate ads_api v1 models and clients from codegen/v1/data/openapi.

Usage:
    uv run python codegen/v1/generate.py
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from codegen.emit import render_client_module, render_models_module, render_shared_module
from codegen.schema import EmittedModel, NameMap, discover_emissions, select_shared_models
from codegen.spec import (
    AD_PRODUCTS,
    ALL,
    PRODUCT_ORDER,
    Product,
    apply_schema_prefix,
    camel_to_snake,
    drop_covered_operations,
    filter_operations_by_tag,
    iter_operations,
    load_json,
    operation_keys,
    unique_tags,
)

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
SPEC_ROOT = HERE / "data" / "openapi"
PACKAGE_ROOT = PROJECT / "src" / "ads_api"
CLIENT_ROOT = PACKAGE_ROOT / "client" / "v1"
MODELS_ROOT = PACKAGE_ROOT / "models" / "v1"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.relative_to(PROJECT)}")


def _ensure_pkg(path: Path) -> None:
    init = path / "__init__.py"
    if not init.exists():
        _write(init, "")


_PRODUCT_MODULES = {product.module for product in PRODUCT_ORDER if product.prefix}


def render_product_namespace(product: Product, entities: list[tuple[str, str]]) -> str:
    """entities: list of (entity_snake, resource_class)."""
    entities = sorted(entities)
    cls = product.prefix
    lines = [
        f'"""{product.prefix} resource namespace — entity-specific clients."""',
        "",
        "from __future__ import annotations",
        "",
        "from ads_api.base import ClientContext",
        "",
    ]
    for module, resource_cls in entities:
        lines.append(f"from .{module} import {resource_cls}")
    lines.append("")
    lines.append("")
    lines.append(f"class {cls}:")
    lines.append(f'    """Lazy entity-specific {product.prefix} resources."""')
    lines.append("")
    lines.append("    def __init__(self, ctx: ClientContext) -> None:")
    lines.append("        self._ctx = ctx")
    for module, resource_cls in entities:
        lines.append(f"        self.__{module}: {resource_cls} | None = None")
    lines.append("")
    for module, resource_cls in entities:
        lines.append("    @property")
        lines.append(f"    def {module}(self) -> {resource_cls}:")
        lines.append(f"        if self.__{module} is None:")
        lines.append(f"            self.__{module} = {resource_cls}(self._ctx)")
        lines.append(f"        return self.__{module}")
        lines.append("")
    return "\n".join(lines)


def _append_lazy_properties(lines: list[str], attrs: list[tuple[str, str]]) -> None:
    for name, cls in attrs:
        lines.append("    @property")
        lines.append(f"    def {name}(self) -> {cls}:")
        lines.append(f"        if self.__{name} is None:")
        lines.append(f"            self.__{name} = {cls}(self._ctx)")
        lines.append(f"        return self.__{name}")
        lines.append("")


def render_v1_client(products: list[Product], entities: list[tuple[str, str]]) -> str:
    """entities: top-level ALL resources as (module, resource_class)."""
    attrs = [(product.module, product.prefix) for product in products] + sorted(entities)
    lines = [
        '"""Amazon Ads API v1 async client."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any, overload",
        "",
        "from ads_api.base import ClientContext",
        "from ads_api.config.settings import AmazonAdsConfig",
        "from ads_api.errors import MissingConfigError",
        "",
    ]
    for product in products:
        lines.append(f"from ads_api.client.v1.{product.module} import {product.prefix}")
    for module, cls in entities:
        lines.append(f"from ads_api.client.v1.{module} import {cls}")
    lines.append("")
    lines.append("")
    lines.append("class AdsClientV1:")
    lines.append('    """Async client for Amazon Ads API v1.')
    lines.append("")
    lines.append("    Ad products are nested; unscoped APIs hang off the client:")
    lines.append("")
    lines.append("        async with AdsClientV1(config) as ads:")
    lines.append("            await ads.sp.campaigns.create_campaign(body)")
    lines.append("            await ads.selling_accounts.query_selling_account(body)")
    lines.append('    """')
    lines.append("")
    lines.append("    @overload")
    lines.append("    def __init__(self, config: AmazonAdsConfig) -> None: ...")
    lines.append("")
    lines.append("    @overload")
    lines.append("    def __init__(self, *, ctx: ClientContext) -> None: ...")
    lines.append("")
    lines.append(
        "    def __init__(\n"
        "        self,\n"
        "        config: AmazonAdsConfig | None = None,\n"
        "        *,\n"
        "        ctx: ClientContext | None = None,\n"
        "    ) -> None:"
    )
    lines.append("        if ctx is not None:")
    lines.append("            self._ctx = ctx")
    lines.append("            self._owns_ctx = False")
    lines.append("        elif config is not None:")
    lines.append("            self._ctx = ClientContext(config)")
    lines.append("            self._owns_ctx = True")
    lines.append("        else:")
    lines.append("            raise MissingConfigError()")
    for name, cls in attrs:
        lines.append(f"        self.__{name}: {cls} | None = None")
    lines.append("")
    lines.append("    async def __aenter__(self) -> AdsClientV1:")
    lines.append("        return self")
    lines.append("")
    lines.append("    async def __aexit__(self, *args: Any) -> None:")
    lines.append("        await self.close()")
    lines.append("")
    lines.append("    async def close(self) -> None:")
    lines.append("        if self._owns_ctx:")
    lines.append("            await self._ctx.close()")
    lines.append("")
    _append_lazy_properties(lines, attrs)
    return "\n".join(lines)


@dataclass
class ProductTagWork:
    product: Product
    tag: str
    entity_snake: str
    resource_name: str
    spec: dict[str, Any]
    endpoints: list[tuple[str, str, dict[str, Any]]]
    emitted: list[EmittedModel]
    name_map: NameMap


def prepare_specs() -> list[ProductTagWork]:
    specs: dict[Product, dict[str, Any]] = {}
    for product in PRODUCT_ORDER:
        spec_path = SPEC_ROOT / product.spec_filename
        if not spec_path.is_file():
            raise SystemExit(f"找不到 spec 文件: {spec_path}")
        specs[product] = load_json(spec_path)

    # 1. 收集所有广告产品的操作，用于从 ALL 中去重
    covered_by_products: set[tuple[str, str]] = set()
    for product in AD_PRODUCTS:
        if product in specs:
            covered_by_products |= operation_keys(specs[product])

    # 2. 为广告产品的 schema 补前缀
    for product in AD_PRODUCTS:
        if product in specs and product.prefix:
            apply_schema_prefix(specs[product], product.prefix)

    # 3. 从 ALL 中剔除已被具体产品覆盖的操作
    if ALL in specs:
        drop_covered_operations(specs[ALL], covered_by_products)

    # 4. 按产品与 tag 解析生成工作单元
    works: list[ProductTagWork] = []
    for product in PRODUCT_ORDER:
        if product not in specs:
            continue
        spec = specs[product]
        all_endpoints = iter_operations(spec)
        if not all_endpoints:
            print(f"=== {product.key} ({product.module}): 0 operations (跳过) ===")
            continue

        tags = unique_tags(spec)
        print(f"\n=== {product.key} ({product.module}): {len(all_endpoints)} operations across {len(tags)} tags ===")
        for tag in tags:
            tag_endpoints = filter_operations_by_tag(all_endpoints, tag)
            if not tag_endpoints:
                continue
            entity_snake = camel_to_snake(tag)
            emitted, name_map = discover_emissions(spec, tag_endpoints)
            resource_name = f"{product.prefix}{tag}" if product.prefix else tag
            print(f"  [{tag} -> {entity_snake}] {len(tag_endpoints)} ops, {len(emitted)} models -> {resource_name}")
            works.append(
                ProductTagWork(
                    product=product,
                    tag=tag,
                    entity_snake=entity_snake,
                    resource_name=resource_name,
                    spec=spec,
                    endpoints=tag_endpoints,
                    emitted=emitted,
                    name_map=name_map,
                )
            )

    return works


def _collect_shared(works: list[ProductTagWork]) -> dict[Product, list[EmittedModel]]:
    groups: dict[Product, list[list[EmittedModel]]] = defaultdict(list)
    for work in works:
        groups[work.product].append(work.emitted)

    shared: dict[Product, list[EmittedModel]] = {}
    for product, emitted_groups in groups.items():
        items = select_shared_models(emitted_groups)
        if items:
            shared[product] = items
            names = ", ".join(item.python_name for item in items)
            print(f"  shared {product.key}: {names}")
    return shared


def _write_shared(shared_by_product: dict[Product, list[EmittedModel]], generated_modules: set[str]) -> None:
    shared_dir = MODELS_ROOT / "_shared"
    _ensure_pkg(MODELS_ROOT)
    _ensure_pkg(shared_dir)
    shared_modules = {product.module for product in shared_by_product}
    for product, items in shared_by_product.items():
        _write(shared_dir / f"{product.module}.py", render_shared_module(product.module, items, NameMap(items)))
    valid_modules = {product.module for product in PRODUCT_ORDER if product.prefix} | {"general"}
    for module in generated_modules:
        path = shared_dir / f"{module}.py"
        if module not in shared_modules and path.exists():
            path.unlink()
            print(f"  removed {path.relative_to(PROJECT)}")
    for path in sorted(shared_dir.glob("*.py")):
        if path.name != "__init__.py" and path.stem not in valid_modules:
            path.unlink()
            print(f"  removed {path.relative_to(PROJECT)}")


def write_models_and_clients(works: list[ProductTagWork], shared_by_product: dict[Product, list[EmittedModel]]) -> None:
    _ensure_pkg(MODELS_ROOT)
    _ensure_pkg(CLIENT_ROOT)

    # 统计各实体下生成了哪些 product 模块
    entity_modules: dict[str, set[str]] = defaultdict(set)
    all_entity_snakes: set[str] = set()

    for work in works:
        entity_snake = work.entity_snake
        all_entity_snakes.add(entity_snake)
        module = work.product.module
        entity_modules[entity_snake].add(module)

        model_dir = MODELS_ROOT / entity_snake
        _ensure_pkg(model_dir)

        shared_items = shared_by_product.get(work.product, [])
        shared_names = {item.python_name for item in shared_items}
        models_import = f"ads_api.models.v1.{entity_snake}.{module}"

        _write(
            model_dir / f"{module}.py",
            render_models_module(
                work.tag,
                work.emitted,
                work.name_map,
                shared_names=shared_names,
                shared_module=module if shared_names else None,
            ),
        )

        if not work.product.prefix:
            client_path = CLIENT_ROOT / f"{entity_snake}.py"
        else:
            client_dir = CLIENT_ROOT / module
            _ensure_pkg(client_dir)
            client_path = client_dir / f"{entity_snake}.py"

        _write(
            client_path,
            render_client_module(
                spec=work.spec,
                tag=work.tag,
                resource_name=work.resource_name,
                models_import=models_import,
                endpoints=work.endpoints,
                emitted=work.emitted,
                name_map=work.name_map,
            ),
        )

    # 清理 models 目录下多余的文件
    for entity_snake, modules in entity_modules.items():
        model_dir = MODELS_ROOT / entity_snake
        _write(model_dir / "__init__.py", "")
        for path in sorted(model_dir.glob("*.py")):
            if path.name == "__init__.py" or path.stem in modules:
                continue
            path.unlink()
            print(f"  removed {path.relative_to(PROJECT)}")

    # 清理多余的 entity 目录
    for path in sorted(MODELS_ROOT.iterdir()):
        if not path.is_dir() or path.name in ("_shared", "__pycache__"):
            continue
        if path.name not in all_entity_snakes:
            shutil.rmtree(path)
            print(f"  removed stale model dir {path.relative_to(PROJECT)}")


def _cleanup_legacy_entity_client_dirs(valid_top_level_files: set[str]) -> None:
    client_root = CLIENT_ROOT
    if not client_root.exists():
        return
    for path in sorted(client_root.iterdir()):
        if path.is_dir():
            if path.name not in _PRODUCT_MODULES and path.name != "__pycache__":
                shutil.rmtree(path)
                print(f"  removed legacy client dir {path.relative_to(PROJECT)}")
        elif path.is_file():
            if path.name not in valid_top_level_files and path.name != "__init__.py":
                path.unlink()
                print(f"  removed stale top-level client file {path.relative_to(PROJECT)}")


def _remove_empty_product_dirs(products: list[Product]) -> None:
    client_root = CLIENT_ROOT
    if not client_root.exists():
        return
    active_modules = {product.module for product in products}
    for product in PRODUCT_ORDER:
        if not product.prefix or product.module in active_modules:
            continue
        product_dir = client_root / product.module
        if not product_dir.is_dir():
            continue
        shutil.rmtree(product_dir)
        print(f"  removed {product_dir.relative_to(PROJECT)}")


def write_client_namespaces(works: list[ProductTagWork]) -> None:
    product_entities: dict[Product, list[tuple[str, str]]] = defaultdict(list)
    top_level_entities: list[tuple[str, str]] = []

    for work in works:
        entity = (work.entity_snake, work.resource_name)
        if not work.product.prefix:
            top_level_entities.append(entity)
        else:
            product_entities[work.product].append(entity)

    products = [product for product in PRODUCT_ORDER if product in product_entities]
    valid_top_level_files = {f"{entity_snake}.py" for entity_snake, _ in top_level_entities}
    _cleanup_legacy_entity_client_dirs(valid_top_level_files)
    _remove_empty_product_dirs(products)

    for product, entities in product_entities.items():
        client_dir = CLIENT_ROOT / product.module
        _ensure_pkg(client_dir)
        _write(client_dir / "__init__.py", render_product_namespace(product, entities))
        print(f"  {product.module}/__init__.py: {len(entities)} resources")

    _write(CLIENT_ROOT / "__init__.py", render_v1_client(products, top_level_entities))
    print(f"  client/v1/__init__.py: {len(products)} products, {len(top_level_entities)} top-level resources")


def _run_formatter() -> None:
    for cmd in (
        ["uv", "run", "ruff", "check", "--fix", str(CLIENT_ROOT), str(MODELS_ROOT)],
        ["uv", "run", "black", str(CLIENT_ROOT), str(MODELS_ROOT)],
    ):
        print(f"\n$ {' '.join(cmd)}")
        res = subprocess.run(cmd, cwd=PROJECT)
        if res.returncode != 0:
            sys.exit(res.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ads_api v1 models and clients from Merged OpenAPI specs.")
    parser.add_argument("--no-format", action="store_true", help="Skip ruff and black formatting")
    args = parser.parse_args()

    print("=== 解析 Merged OpenAPI 规范 ===")
    works = prepare_specs()

    print("\n=== 收集产品间跨实体共享 Schema ===")
    shared_by_product = _collect_shared(works)
    generated_modules = {work.product.module for work in works}
    _write_shared(shared_by_product, generated_modules)

    print("\n=== 生成 Models 与 Clients ===")
    write_models_and_clients(works, shared_by_product)

    print("\n=== 生成 Client Namespaces ===")
    write_client_namespaces(works)

    if not args.no_format:
        _run_formatter()

    print("\n[OK] v1 代码生成完成！")


if __name__ == "__main__":
    main()
