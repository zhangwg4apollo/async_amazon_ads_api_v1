"""下载 Amazon Ads API v1 OpenAPI 规范到 codegen/v1/data/openapi/。

包含 7 个 Merged spec，以及 Reporting API (beta) Contract。
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import httpx
from _json_io import fetch_json_with_etag

DATA_DIR = Path(__file__).resolve().parent / "data"
OPENAPI_DIR = DATA_DIR / "openapi"


class SpecSource(NamedTuple):
    name: str
    product: str
    url: str
    filename: str


SPECS = [
    SpecSource(
        name="All Products",
        product="ALL",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPIALLMerged_prod_3p.json",
        filename="AmazonAdsAPIALLMerged_prod_3p.json",
    ),
    SpecSource(
        name="Sponsored Products (SP)",
        product="SP",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPISPMerged_prod_3p.json",
        filename="AmazonAdsAPISPMerged_prod_3p.json",
    ),
    SpecSource(
        name="SP Global",
        product="SPGLOBAL",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPISPGLOBALMerged_prod_3p.json",
        filename="AmazonAdsAPISPGLOBALMerged_prod_3p.json",
    ),
    SpecSource(
        name="Sponsored Brands (SB)",
        product="SB",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPISBMerged_prod_3p.json",
        filename="AmazonAdsAPISBMerged_prod_3p.json",
    ),
    SpecSource(
        name="Demand-Side Platform (DSP)",
        product="DSP",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPIDSPMerged_prod_3p.json",
        filename="AmazonAdsAPIDSPMerged_prod_3p.json",
    ),
    SpecSource(
        name="Sponsored Television (ST)",
        product="ST",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPISTMerged_prod_3p.json",
        filename="AmazonAdsAPISTMerged_prod_3p.json",
    ),
    SpecSource(
        name="Sponsored Display (SD)",
        product="SD",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPISDMerged_prod_3p.json",
        filename="AmazonAdsAPISDMerged_prod_3p.json",
    ),
    SpecSource(
        name="Reporting API (beta)",
        product="REPORTS",
        url="https://d1y2lf8k3vrkfu.cloudfront.net/openapi/en-us/dest/AmazonAdsAPIALLReportsContract_prod_3p_BETA.json",
        filename="AmazonAdsAPIALLReportsContract_prod_3p_BETA.json",
    ),
]


def main() -> None:
    OPENAPI_DIR.mkdir(parents=True, exist_ok=True)
    print(f"正在下载 {len(SPECS)} 个 OpenAPI 文件到 {OPENAPI_DIR} ...")

    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        for spec in SPECS:
            dest = OPENAPI_DIR / spec.filename
            meta_path = OPENAPI_DIR / f"{spec.filename}.meta.json"
            print(f"下载 [{spec.product}] {spec.name} -> {spec.filename}")
            fetch_json_with_etag(client, spec.url, dest, meta_path)

    print("下载完成！")


if __name__ == "__main__":
    main()
