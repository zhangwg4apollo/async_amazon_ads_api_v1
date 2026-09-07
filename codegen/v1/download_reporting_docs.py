"""从 toc2.json 的 Reporting API (beta) 下载 markdown 指南。

产物：codegen/v1/data/guides/reporting/ads-v1/

OpenAPI 由 download_openapi.py 下载，不在本脚本处理。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from _json_io import read_json, write_json

HERE = Path(__file__).resolve().parent
DATA_ROOT = HERE / "data"
TOC_PATH = DATA_ROOT / "toc2.json"
V0_TOC_PATH = HERE.parent / "v0" / "data" / "toc2.json"
MD_ROOT = DATA_ROOT / "guides" / "reporting" / "ads-v1"
MD_PREFIX = "guides/reporting/ads-v1/"
MD_META_PATH = MD_ROOT / "meta.json"

MD_BASE = "https://d3a0d0y2hgofx6.cloudfront.net/en-us/"
TOC_URL = "https://d3a0d0y2hgofx6.cloudfront.net/en-us/toc2.json"
SECTION_NAME = "Reporting API (beta)"
BETAS_TOC_ID = "toc-betas"


@dataclass(frozen=True)
class MarkdownDoc:
    path: str
    name: str


def resolve_markdown_url(markdown: str) -> str:
    return MD_BASE + markdown.lstrip("/")


def load_toc() -> dict[str, Any]:
    for path in (TOC_PATH, V0_TOC_PATH):
        if path.is_file():
            print(f"toc: {path}")
            return read_json(path)
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


def collect_docs(section: dict[str, Any]) -> list[MarkdownDoc]:
    markdowns: list[MarkdownDoc] = []
    seen_md: set[str] = set()

    def walk(node: dict[str, Any]) -> None:
        markdown = node.get("markdown")
        if isinstance(markdown, str) and markdown not in seen_md:
            seen_md.add(markdown)
            markdowns.append(MarkdownDoc(path=markdown, name=node["name"]))
        for child in node.get("items") or []:
            if isinstance(child, dict):
                walk(child)

    walk(section)
    return markdowns


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


def main() -> None:
    toc2 = load_toc()
    section = find_reporting_section(toc2)
    docs = collect_docs(section)
    print(f"{SECTION_NAME}: {len(docs)} markdown")
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        failures = download_markdowns(client, docs)
    if failures:
        print(f"完成，失败 {failures} 项")
        sys.exit(1)
    print("完成")


if __name__ == "__main__":
    main()
