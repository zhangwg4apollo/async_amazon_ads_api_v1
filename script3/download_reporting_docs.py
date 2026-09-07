"""从 toc2.json 的 Reporting API (beta) 下载 markdown 与 Reports OpenAPI。"""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
from _json_io import fetch_json_with_etag, read_json, write_json

HERE = Path(__file__).resolve().parent
DATA_ROOT = HERE / "data"
TOC_PATH = DATA_ROOT / "toc2.json"
MD_ROOT = DATA_ROOT / "guides" / "reporting" / "ads-v1"
MD_PREFIX = "guides/reporting/ads-v1/"
MD_META_PATH = MD_ROOT / "meta.json"
BETA_TOC_PATH = DATA_ROOT / "per_entity_toc_beta.json"
BETA_TOC_META_PATH = DATA_ROOT / "per_entity_toc_beta.json.meta.json"

MD_BASE = "https://d3a0d0y2hgofx6.cloudfront.net/en-us/"
YAML_BASE = "https://d3a0d0y2hgofx6.cloudfront.net/openapi/en-us/"
TOC_URL = "https://d3a0d0y2hgofx6.cloudfront.net/en-us/toc2.json"
SECTION_NAME = "Reporting API (beta)"
BETAS_TOC_ID = "toc-betas"
BETA_SPECS_NAME = "Beta specifications"


@dataclass(frozen=True)
class MarkdownDoc:
    path: str
    name: str


@dataclass(frozen=True)
class LinkedSpec:
    link: str
    name: str


def resolve_openapi_url(openapi: str) -> str:
    if openapi.startswith("http://") or openapi.startswith("https://"):
        return openapi
    return YAML_BASE + openapi.lstrip("/")


def resolve_markdown_url(markdown: str) -> str:
    return MD_BASE + markdown.lstrip("/")


def filename_from_url(url: str) -> str:
    name = urlparse(url).path.rsplit("/", 1)[-1]
    if not name:
        raise ValueError(f"无法从 URL 解析文件名: {url}")
    return name


def unwrap_remote_items(items: Any) -> str | None:
    if isinstance(items, str) and items.startswith("$") and items.endswith("$") and len(items) > 2:
        return items[1:-1]
    return None


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


def find_toc(toc2: dict[str, Any], toc_id: str) -> dict[str, Any]:
    for toc in toc2["tocs"]:
        if toc.get("id") == toc_id:
            return toc
    raise LookupError(f"未在 toc2.json 中找到 {toc_id}")


def find_named(items: list[Any], name: str) -> dict[str, Any]:
    for item in items:
        if isinstance(item, dict) and item.get("name") == name:
            return item
    raise LookupError(f"未找到 {name}")


def find_reporting_section(toc2: dict[str, Any]) -> dict[str, Any]:
    betas = find_toc(toc2, BETAS_TOC_ID)
    return find_named(betas.get("items") or [], SECTION_NAME)


def find_beta_spec_toc_url(toc2: dict[str, Any]) -> str:
    betas = find_toc(toc2, BETAS_TOC_ID)
    specs = find_named(betas.get("items") or [], BETA_SPECS_NAME)
    url = unwrap_remote_items(specs.get("items"))
    if url is None:
        raise LookupError(f"{BETA_SPECS_NAME} 没有远程 TOC URL")
    return url


def collect_docs(section: dict[str, Any]) -> tuple[list[MarkdownDoc], list[LinkedSpec]]:
    markdowns: list[MarkdownDoc] = []
    seen_md: set[str] = set()
    links: list[LinkedSpec] = []
    seen_links: set[str] = set()

    def walk(node: dict[str, Any]) -> None:
        markdown = node.get("markdown")
        if isinstance(markdown, str) and markdown not in seen_md:
            seen_md.add(markdown)
            markdowns.append(MarkdownDoc(path=markdown, name=node["name"]))
        link = node.get("link")
        if isinstance(link, str) and link not in seen_links:
            seen_links.add(link)
            links.append(LinkedSpec(link=link, name=node["name"]))
        for child in node.get("items") or []:
            if isinstance(child, dict):
                walk(child)

    walk(section)
    return markdowns, links


def collect_route_openapis(node: Any, route: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    if isinstance(node, list):
        for child in node:
            found.extend(collect_route_openapis(child, route))
        return found
    if not isinstance(node, dict):
        return found
    for entry in node.get("routes") or []:
        if entry.get("route") != route:
            continue
        if "openapi" in entry:
            found.append({"name": entry.get("name") or route, "openapi": entry["openapi"]})
        for item in entry.get("items") or []:
            if isinstance(item, dict) and "openapi" in item:
                found.append({"name": item.get("name") or route, "openapi": item["openapi"]})
    for child in node.get("items") or []:
        found.extend(collect_route_openapis(child, route))
    return found


def download_text(
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
    dest.write_text(resp.text, encoding="utf-8")
    etag = resp.headers["etag"] if "etag" in resp.headers else None
    last_modified = resp.headers["last-modified"] if "last-modified" in resp.headers else None
    return True, etag, last_modified


def download_spec_file(
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
    if dest.suffix.lower() in {".yaml", ".yml", ".md"}:
        dest.write_text(resp.text, encoding="utf-8")
    else:
        write_json(dest, resp.json())
    etag = resp.headers["etag"] if "etag" in resp.headers else None
    last_modified = resp.headers["last-modified"] if "last-modified" in resp.headers else None
    return True, etag, last_modified


def local_markdown_path(markdown: str) -> Path:
    if not markdown.startswith(MD_PREFIX) or ".." in Path(markdown).parts:
        raise ValueError(f"markdown 路径超出 {MD_PREFIX}: {markdown}")
    return DATA_ROOT / markdown


def download_markdowns(client: httpx.Client, docs: list[MarkdownDoc]) -> int:
    prev = read_json(MD_META_PATH) if MD_META_PATH.is_file() else {"items": []}
    old_items = {entry["markdown"]: entry for entry in prev.get("items", [])}
    failures = 0
    new_items: list[dict[str, Any]] = []
    active: set[Path] = {MD_META_PATH}

    for doc in docs:
        dest = local_markdown_path(doc.path)
        active.add(dest)
        url = resolve_markdown_url(doc.path)
        old = old_items[doc.path] if doc.path in old_items else None
        old_etag = old["etag"] if old is not None and old.get("etag") else None
        try:
            changed, etag, last_modified = download_text(client, url, dest, old_etag)
        except (httpx.HTTPError, OSError, ValueError) as exc:
            failures += 1
            print(f"fail: {doc.path} ({exc})")
            continue
        rel = dest.relative_to(DATA_ROOT)
        if not changed:
            print(f"skip(304): {rel}")
            etag = old["etag"] if old is not None else etag
            last_modified = old["last_modified"] if old is not None else last_modified
        else:
            print(f"saved: {rel} ({dest.stat().st_size} bytes)")
        new_items.append(
            {
                "name": doc.name,
                "markdown": doc.path,
                "etag": etag,
                "last_modified": last_modified,
                "size": dest.stat().st_size,
            }
        )

    meta = {"section": SECTION_NAME, "base": MD_BASE, "items": new_items}
    write_json(MD_META_PATH, meta)

    if MD_ROOT.is_dir():
        for path in sorted(MD_ROOT.rglob("*"), reverse=True):
            if path in active:
                continue
            if path.is_file():
                path.unlink()
                print(f"removed: {path.relative_to(DATA_ROOT)}")
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                print(f"removed: {path.relative_to(DATA_ROOT)}")

    return failures


def download_linked_specs(client: httpx.Client, toc2: dict[str, Any], links: list[LinkedSpec]) -> int:
    if not links:
        return 0
    beta_toc_url = find_beta_spec_toc_url(toc2)
    print(f"下载 Beta specifications TOC → {BETA_TOC_PATH}")
    fetch_json_with_etag(client, beta_toc_url, BETA_TOC_PATH, BETA_TOC_META_PATH)
    beta_toc = read_json(BETA_TOC_PATH)

    failures = 0
    for spec in links:
        entries = collect_route_openapis(beta_toc, spec.link)
        if not entries:
            failures += 1
            print(f"fail: {spec.link} 未在 Beta specifications 中找到 openapi")
            continue
        out_dir = DATA_ROOT / spec.link
        out_dir.mkdir(parents=True, exist_ok=True)
        meta_path = out_dir / "meta.json"
        prev = read_json(meta_path) if meta_path.is_file() else {"items": []}
        old_items = {entry["openapi"]: entry for entry in prev.get("items", [])}
        keep: set[str] = {"meta.json"}
        meta_items: list[dict[str, Any]] = []
        for entry in entries:
            url = resolve_openapi_url(entry["openapi"])
            filename = filename_from_url(url)
            dest = out_dir / filename
            keep.add(filename)
            old = old_items[url] if url in old_items else None
            old_etag = old["etag"] if old is not None and old.get("etag") else None
            try:
                changed, etag, last_modified = download_spec_file(client, url, dest, old_etag)
            except (httpx.HTTPError, OSError, ValueError) as exc:
                failures += 1
                print(f"fail: {spec.link} {filename} ({exc})")
                continue
            rel = dest.relative_to(DATA_ROOT)
            if not changed:
                print(f"skip(304): {rel}")
                etag = old["etag"] if old is not None else etag
                last_modified = old["last_modified"] if old is not None else last_modified
            else:
                print(f"saved: {rel} ({dest.stat().st_size} bytes)")
            meta_items.append(
                {
                    "name": entry["name"],
                    "openapi": url,
                    "file": filename,
                    "etag": etag,
                    "last_modified": last_modified,
                    "size": dest.stat().st_size,
                }
            )
        write_json(
            meta_path,
            {
                "group": spec.link,
                "route": spec.link,
                "toc_name": spec.name,
                "items": meta_items,
            },
        )
        for path in sorted(out_dir.iterdir()):
            if path.name in keep:
                continue
            if path.is_file():
                path.unlink()
                print(f"removed: {path.relative_to(DATA_ROOT)}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"removed: {path.relative_to(DATA_ROOT)}")
    return failures


def main() -> None:
    toc2 = load_toc()
    section = find_reporting_section(toc2)
    docs, links = collect_docs(section)
    print(f"{SECTION_NAME}: {len(docs)} markdown, {len(links)} OpenAPI link")
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        failures = download_markdowns(client, docs)
        failures += download_linked_specs(client, toc2, links)
    if failures:
        print(f"完成，失败 {failures} 项")
        sys.exit(1)
    print("完成")


if __name__ == "__main__":
    main()
