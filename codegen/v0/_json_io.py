"""codegen/v0 共用的 JSON 读写与带 ETag 的条件下载。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _load_meta(meta_path: Path) -> dict[str, Any] | None:
    if not meta_path.is_file():
        return None
    return read_json(meta_path)


def fetch_json_with_etag(
    client: httpx.Client,
    url: str,
    dest: Path,
    meta_path: Path,
) -> bool:
    """条件 GET；200 写入 dest+meta，304 跳过写入。

    Returns:
        True 表示内容已更新并写入；False 表示 304 复用本地文件。
    """
    old = _load_meta(meta_path)
    headers: dict[str, str] = {}
    if dest.is_file() and old is not None and "etag" in old and old["etag"]:
        headers["If-None-Match"] = old["etag"]

    resp = client.get(url, headers=headers)

    if resp.status_code == 304:
        if not dest.is_file():
            raise RuntimeError(f"收到 304 但本地文件不存在: {dest}")
        print(f"skip(304): {dest}")
        return False

    resp.raise_for_status()
    write_json(dest, resp.json())
    etag = resp.headers["etag"] if "etag" in resp.headers else None
    last_modified = resp.headers["last-modified"] if "last-modified" in resp.headers else None
    write_json(
        meta_path,
        {
            "url": url,
            "etag": etag,
            "last_modified": last_modified,
            "size": dest.stat().st_size,
        },
    )
    print(f"saved: {dest} ({dest.stat().st_size} bytes)")
    return True
