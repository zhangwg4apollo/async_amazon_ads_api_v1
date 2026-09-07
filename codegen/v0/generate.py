"""Generate ads_api v0 models and clients from codegen/v0/data/api-spec-v0.

Usage:
    uv run python codegen/v0/generate.py
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
from codegen.schema import (
    EmittedModel,
    NameMap,
    discover_emissions,
    select_shared_models,
    shared_names_for,
)
from codegen.spec import (
    GROUPS,
    TocGroup,
    entities_from_tags,
    filter_operations_by_tag,
    iter_operations,
    load_json,
    load_spec,
    resource_class_name,
    should_split_by_tag,
    unique_tags,
)

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
SPEC_ROOT = HERE / "data" / "api-spec-v0"
PACKAGE_ROOT = PROJECT / "src" / "ads_api"
CLIENT_ROOT = PACKAGE_ROOT / "client" / "v0"
MODELS_ROOT = PACKAGE_ROOT / "models" / "v0"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.relative_to(PROJECT)}")


def _ensure_pkg(path: Path) -> None:
    init = path / "__init__.py"
    if not init.exists():
        _write(init, "")


@dataclass
class EntityWork:
    group: str
    entity: str
    tag: str
    resource_name: str
    spec: dict[str, Any]
    endpoints: list[tuple[str, str, dict[str, Any]]]
    emitted: list[EmittedModel]
    name_map: NameMap

    @property
    def models_import(self) -> str:
        return f"ads_api.models.v0.{self.group}.{self.entity}"


def _spec_file(entity_dir: Path, meta: dict[str, Any]) -> Path:
    items = meta["items"]
    if len(items) != 1:
        raise SystemExit(f"{entity_dir.name}: 期望恰好 1 个 spec 文件，实际 {len(items)}")
    return entity_dir / items[0]["file"]


def _prepare_spec(group: str, entity_dir: Path, reserved: set[str]) -> list[EntityWork]:
    meta = load_json(entity_dir / "meta.json")
    spec = load_spec(_spec_file(entity_dir, meta))
    all_endpoints = iter_operations(spec)
    if not all_endpoints:
        print(f"\n=== {group}/{entity_dir.name} skip: 无操作 ===")
        return []
    fallback_entity = meta["entity"]
    works: list[EntityWork] = []
    if should_split_by_tag(spec):
        tags = unique_tags(spec)
        tag_entities = entities_from_tags(tags, fallback_entity, reserved)
        # 叶子 TOC（如 Portfolios）主 tag 会映射成与分组同名的实体，
        # 再拆会变成 ads.v0.portfolios.portfolios，改为整份挂在分组上。
        if group not in tag_entities.values():
            print(f"\n=== {group}/{fallback_entity} split tags={tags} ===")
            for tag in tags:
                endpoints = filter_operations_by_tag(all_endpoints, tag)
                entity = tag_entities[tag]
                emitted, name_map = discover_emissions(spec, endpoints)
                print(f"  {entity}: {len(endpoints)} operations")
                works.append(
                    EntityWork(
                        group=group,
                        entity=entity,
                        tag=tag,
                        resource_name=resource_class_name(entity),
                        spec=spec,
                        endpoints=endpoints,
                        emitted=emitted,
                        name_map=name_map,
                    )
                )
            return works
    tags = unique_tags(spec)
    tag = tags[0] if len(tags) == 1 else fallback_entity
    emitted, name_map = discover_emissions(spec, all_endpoints)
    print(f"\n=== {group}/{fallback_entity} (tag={tag}) {len(all_endpoints)} operations ===")
    works.append(
        EntityWork(
            group=group,
            entity=fallback_entity,
            tag=tag,
            resource_name=resource_class_name(fallback_entity),
            spec=spec,
            endpoints=all_endpoints,
            emitted=emitted,
            name_map=name_map,
        )
    )
    return works


def _iter_spec_dirs() -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    for group in GROUPS:
        group_root = SPEC_ROOT / group.key
        if not group_root.is_dir():
            continue
        if (group_root / "meta.json").is_file():
            result.append((group.key, group_root))
            continue
        for entity_dir in sorted(p for p in group_root.iterdir() if p.is_dir() and (p / "meta.json").is_file()):
            result.append((group.key, entity_dir))
    return result


def prepare_entities() -> list[EntityWork]:
    spec_dirs = _iter_spec_dirs()
    reserved_by_group: dict[str, set[str]] = defaultdict(set)
    for group in GROUPS:
        reserved_by_group[group.key].add(group.key)
    for group_key, entity_dir in spec_dirs:
        reserved_by_group[group_key].add(load_json(entity_dir / "meta.json")["entity"])

    works: list[EntityWork] = []
    for group_key, entity_dir in spec_dirs:
        works.extend(_prepare_spec(group_key, entity_dir, reserved_by_group[group_key]))
    if not works:
        raise SystemExit("没有可生成的 v0 实体")
    collisions = defaultdict(list)
    for work in works:
        collisions[(work.group, work.entity)].append(work.tag)
    dupes = {key: sources for key, sources in collisions.items() if len(sources) > 1}
    if dupes:
        details = "; ".join(
            f"{group}/{entity} ← {', '.join(sources)}" for (group, entity), sources in sorted(dupes.items())
        )
        raise SystemExit(f"分组内实体名冲突: {details}")
    return works


def render_namespace(class_name: str, doc: str, entities: list[tuple[str, str]]) -> str:
    entities = sorted(entities)
    lines = [
        f'"""{class_name} resource namespace — {doc}."""',
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
    lines.append(f"class {class_name}:")
    lines.append(f'    """Lazy {class_name} resources."""')
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


def _is_singleton_group(group_key: str, entities: list[tuple[str, str]]) -> bool:
    return len(entities) == 1 and entities[0][0] == group_key


def render_singleton_export(entity: str, resource_cls: str) -> str:
    return (
        f'"""{resource_cls} resource — leaf TOC group `{entity}`."""\n'
        "\n"
        f"from .{entity} import {resource_cls}\n"
        "\n"
        f'__all__ = ["{resource_cls}"]\n'
    )


def render_v0_client(groups: list[TocGroup]) -> str:
    lines = [
        '"""Amazon Ads API v0 async client."""',
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
    for group in groups:
        lines.append(f"from ads_api.client.v0.{group.key} import {group.namespace_class}")
    lines.append("")
    lines.append("")
    lines.append("class AdsClientV0:")
    lines.append('    """Async client for Amazon Ads API v0.')
    lines.append("")
    lines.append("        async with AdsClientV0(config) as ads:")
    lines.append("            await ads.accounts.profiles.list_profiles()")
    lines.append("            await ads.reporting.reports.create_async_report(body)")
    lines.append("            await ads.portfolios.list_portfolios(body)")
    lines.append("            await ads.sp_v3.campaigns.create_sponsored_products_campaigns(body)")
    lines.append("            await ads.sd.campaigns.list_campaigns()")
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
    for group in groups:
        lines.append(f"        self.__{group.key}: {group.namespace_class} | None = None")
    lines.append("")
    lines.append("    async def __aenter__(self) -> AdsClientV0:")
    lines.append("        return self")
    lines.append("")
    lines.append("    async def __aexit__(self, *args: Any) -> None:")
    lines.append("        await self.close()")
    lines.append("")
    lines.append("    async def close(self) -> None:")
    lines.append("        if self._owns_ctx:")
    lines.append("            await self._ctx.close()")
    lines.append("")
    for group in groups:
        lines.append("    @property")
        lines.append(f"    def {group.key}(self) -> {group.namespace_class}:")
        lines.append(f"        if self.__{group.key} is None:")
        lines.append(f"            self.__{group.key} = {group.namespace_class}(self._ctx)")
        lines.append(f"        return self.__{group.key}")
        lines.append("")
    return "\n".join(lines)


def write_shared(works: list[EntityWork]) -> list[EmittedModel]:
    shared_items = select_shared_models([work.emitted for work in works])
    shared_dir = MODELS_ROOT
    _ensure_pkg(shared_dir)
    path = shared_dir / "_shared.py"
    if shared_items:
        names = ", ".join(item.python_name for item in shared_items)
        print(f"  shared: {names}")
        _write(path, render_shared_module("v0", shared_items, NameMap(shared_items)))
        return shared_items
    if path.exists():
        path.unlink()
        print(f"  removed {path.relative_to(PROJECT)}")
    return []


def _clean_entity_py(path: Path, generated: set[str]) -> None:
    for child in sorted(path.glob("*.py")):
        if child.name == "__init__.py" or child.stem in generated:
            continue
        child.unlink()
        print(f"  removed {child.relative_to(PROJECT)}")
    pycache = path / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def _clean_group_packages(root: Path, by_group: dict[str, list[tuple[str, str]]]) -> None:
    known_groups = {group.key for group in GROUPS}
    for path in sorted(root.iterdir()):
        if not path.is_dir() or path.name == "__pycache__" or path.name.startswith("_"):
            continue
        if path.name not in known_groups:
            shutil.rmtree(path)
            print(f"  removed {path.relative_to(PROJECT)}")
            continue
        generated = {entity for entity, _ in by_group.get(path.name, [])}
        _clean_entity_py(path, generated)
        for child in sorted(p for p in path.iterdir() if p.is_dir() and p.name != "__pycache__"):
            shutil.rmtree(child)
            print(f"  removed {child.relative_to(PROJECT)}")


def write_entities(works: list[EntityWork], shared_items: list[EmittedModel]) -> dict[str, list[tuple[str, str]]]:
    models_root = MODELS_ROOT
    _ensure_pkg(models_root)
    _ensure_pkg(CLIENT_ROOT)

    by_group: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for work in works:
        by_group[work.group].append((work.entity, work.resource_name))
        models_dir = models_root / work.group
        client_dir = CLIENT_ROOT / work.group
        _ensure_pkg(models_dir)
        _ensure_pkg(client_dir)
        names = shared_names_for(work.emitted, shared_items)
        _write(
            models_dir / f"{work.entity}.py",
            render_models_module(
                work.tag,
                work.emitted,
                work.name_map,
                shared_names=names,
                shared_module="shared" if names else None,
            ),
        )
        _write(
            client_dir / f"{work.entity}.py",
            render_client_module(
                spec=work.spec,
                tag=work.tag,
                resource_name=work.resource_name,
                models_import=work.models_import,
                endpoints=work.endpoints,
                emitted=work.emitted,
                name_map=work.name_map,
            ),
        )

    keep_root = {"__init__.py", "_shared.py"}
    for path in sorted(models_root.glob("*.py")):
        if path.name in keep_root:
            continue
        path.unlink()
        print(f"  removed {path.relative_to(PROJECT)}")

    _clean_group_packages(MODELS_ROOT, by_group)
    _clean_group_packages(CLIENT_ROOT, by_group)
    return by_group


def generate_all() -> None:
    works = prepare_entities()
    shared_items = write_shared(works)
    by_group = write_entities(works, shared_items)
    active_groups = [group for group in GROUPS if group.key in by_group]
    for group in active_groups:
        entities = by_group[group.key]
        if _is_singleton_group(group.key, entities):
            entity, resource_cls = entities[0]
            content = render_singleton_export(entity, resource_cls)
        else:
            content = render_namespace(group.namespace_class, group.namespace_doc, entities)
        _write(CLIENT_ROOT / group.key / "__init__.py", content)
    _write(CLIENT_ROOT / "__init__.py", render_v0_client(active_groups))


def run_format() -> None:
    src = str(PACKAGE_ROOT)
    generator = str(HERE)
    for cmd, label in (
        (["uv", "run", "black", src, generator], "black"),
        (["uv", "run", "ruff", "check", "--fix", src, generator], "ruff"),
    ):
        print(f"\n── {label}")
        result = subprocess.run(cmd, cwd=PROJECT, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        print(f"  ✓ {label}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ads_api v0 from v0 OpenAPI specs")
    parser.add_argument("--no-format", action="store_true", help="跳过 black/ruff")
    args = parser.parse_args()

    generate_all()
    if not args.no_format:
        run_format()
    print("\nDone.")


if __name__ == "__main__":
    main()
