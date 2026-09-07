"""从 toc2.json 的 Amazon Ads API v0 分组下载 OpenAPI。"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from _json_io import read_json, write_json
from codegen.spec import (
    GROUP_KEY_OVERRIDES,
    GROUPS,
    INCLUDED_VERSIONS,
    TocGroup,
    collect_all_routes,
    spec_folder_from_toc_name,
    version_from_toc_name,
)

_PRODUCT_GROUP_KEYS = frozenset(GROUP_KEY_OVERRIDES.values())

HERE = Path(__file__).resolve().parent
TOC_PATH = HERE / "data" / "toc2.json"
SPEC_ROOT = HERE / "data" / "api-spec-v0"
YAML_BASE = "https://d3a0d0y2hgofx6.cloudfront.net/openapi/en-us/"
TOC_URL = "https://d3a0d0y2hgofx6.cloudfront.net/en-us/toc2.json"


def resolve_openapi_url(openapi: str) -> str:
    if openapi.startswith("http://") or openapi.startswith("https://"):
        return openapi
    return YAML_BASE + openapi.lstrip("/")


def filename_from_url(url: str) -> str:
    path = urlparse(url).path
    name = path.rsplit("/", 1)[-1]
    if not name:
        raise ValueError(f"无法从 URL 解析文件名: {url}")
    return name


def find_v0_section(toc2: dict[str, Any]) -> dict[str, Any]:
    for toc in toc2["tocs"]:
        if toc.get("id") != "toc-reference":
            continue
        for section in toc.get("items", []):
            if section.get("name") == "Amazon Ads API v0":
                return section
    raise LookupError("未在 toc2.json 中找到 Amazon Ads API v0")


def _section_by_name(v0: dict[str, Any], name: str) -> dict[str, Any] | None:
    for item in v0["items"]:
        if item.get("name") == name:
            return item
    return None


def collect_group_specs(toc2: dict[str, Any], group: TocGroup) -> list[dict[str, str]]:
    v0 = find_v0_section(toc2)
    section = _section_by_name(v0, group.toc_name)
    if section is None:
        raise LookupError(f"未在 Amazon Ads API v0 中找到 {group.toc_name}")

    routes = collect_all_routes(v0)
    children = list(section.get("items") or [])
    if not children and section.get("link"):
        children = [{"name": section["name"], "link": section["link"]}]

    result: list[dict[str, str]] = []
    for child in children:
        name = child["name"]
        link = child.get("link")
        if not link:
            continue
        version = version_from_toc_name(name)
        if group.version:
            if version != group.version:
                continue
        elif version and INCLUDED_VERSIONS.get(group.toc_name) is not None:
            continue
        if link not in routes:
            raise LookupError(f"{group.toc_name} 项 {name} link={link} 没有 openapi")
        entity = group.key if group.version else spec_folder_from_toc_name(name)
        result.append(
            {
                "name": name,
                "entity": entity,
                "route": link,
                "openapi": resolve_openapi_url(routes[link]),
                "group": group.key,
                **({"version": version} if version else {}),
            }
        )
    return result


def load_toc() -> dict[str, Any]:
    if TOC_PATH.is_file():
        print(f"toc: {TOC_PATH}")
        return read_json(TOC_PATH)
    TOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"下载 toc2.json → {TOC_PATH}")
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        resp = client.get(TOC_URL)
        resp.raise_for_status()
        write_json(TOC_PATH, resp.json())
    return read_json(TOC_PATH)


def download_spec(
    client: httpx.Client, url: str, dest: Path, old_etag: str | None
) -> tuple[bool, str | None, str | None]:
    headers: dict[str, str] = {}
    if dest.is_file() and old_etag:
        headers["If-None-Match"] = old_etag
    resp = client.get(url, headers=headers)
    if resp.status_code == 304:
        if not dest.is_file():
            raise RuntimeError(f"收到 304 但本地文件不存在: {dest}")
        return False, old_etag, None
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() in {".yaml", ".yml"}:
        dest.write_text(resp.text, encoding="utf-8")
    else:
        write_json(dest, resp.json())
    etag = resp.headers["etag"] if "etag" in resp.headers else None
    last_modified = resp.headers["last-modified"] if "last-modified" in resp.headers else None
    return True, etag, last_modified


def download_group(client: httpx.Client, group: TocGroup, specs: list[dict[str, str]]) -> None:
    group_root = SPEC_ROOT / group.key
    group_root.mkdir(parents=True, exist_ok=True)
    active: set[str] = set()
    for item in specs:
        entity = item["entity"]
        active.add(entity)
        at_group_root = bool(group.version) or (entity == group.key and group.key in _PRODUCT_GROUP_KEYS)
        out_dir = group_root if at_group_root else group_root / entity
        out_dir.mkdir(parents=True, exist_ok=True)
        meta_path = out_dir / "meta.json"
        prev = read_json(meta_path) if meta_path.is_file() else {"items": []}
        old_items = {entry["openapi"]: entry for entry in prev.get("items", [])}

        url = item["openapi"]
        filename = filename_from_url(url)
        dest = out_dir / filename
        old = old_items[url] if url in old_items else None
        old_etag = old["etag"] if old is not None and old.get("etag") else None
        changed, etag, last_modified = download_spec(client, url, dest, old_etag)
        rel = dest.relative_to(SPEC_ROOT)
        if not changed:
            print(f"skip(304): {rel}")
            etag = old["etag"] if old is not None else etag
            last_modified = old["last_modified"] if old is not None else last_modified
        else:
            print(f"saved: {rel} ({dest.stat().st_size} bytes)")

        meta = {
            "group": group.key,
            "route": item["route"],
            "entity": entity,
            "toc_name": item["name"],
            **({"version": item["version"]} if item.get("version") else {}),
            "items": [
                {
                    "name": item["name"],
                    "openapi": url,
                    "file": filename,
                    "etag": etag,
                    "last_modified": last_modified,
                    "size": dest.stat().st_size,
                }
            ],
        }
        if changed or not meta_path.is_file() or read_json(meta_path) != meta:
            write_json(meta_path, meta)
        keep = {"meta.json", filename}
        for path in sorted(out_dir.iterdir()):
            if path.name in keep:
                continue
            if at_group_root and path.is_dir():
                shutil.rmtree(path)
                print(f"removed: {path.relative_to(SPEC_ROOT)}")
                continue
            if path.is_file():
                path.unlink()
                print(f"removed: {path.relative_to(SPEC_ROOT)}")

    if not group.version:
        for path in sorted(group_root.iterdir()):
            if path.is_dir() and path.name not in active:
                shutil.rmtree(path)
                print(f"removed: {path.relative_to(SPEC_ROOT)}")


def main() -> None:
    toc2 = load_toc()
    SPEC_ROOT.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        for group in GROUPS:
            specs = collect_group_specs(toc2, group)
            download_group(client, group, specs)

    known = {group.key for group in GROUPS}
    for path in sorted(SPEC_ROOT.iterdir()):
        if path.is_dir() and path.name not in known:
            shutil.rmtree(path)
            print(f"removed: {path.relative_to(SPEC_ROOT)}")


if __name__ == "__main__":
    main()
