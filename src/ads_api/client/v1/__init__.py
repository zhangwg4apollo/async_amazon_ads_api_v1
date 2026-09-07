"""Amazon Ads API v1 async client."""

from __future__ import annotations

from typing import Any, overload

from ads_api.base import ClientContext
from ads_api.client.v1.advertiser_accounts import AdvertiserAccounts
from ads_api.client.v1.brand_store_edition_publish_versions import BrandStoreEditionPublishVersions
from ads_api.client.v1.brand_store_editions import BrandStoreEditions
from ads_api.client.v1.brand_store_pages import BrandStorePages
from ads_api.client.v1.brand_stores import BrandStores
from ads_api.client.v1.dsp import DSP
from ads_api.client.v1.manager_accounts import ManagerAccounts
from ads_api.client.v1.reports import Reports
from ads_api.client.v1.sb import SB
from ads_api.client.v1.sd import SD
from ads_api.client.v1.selling_accounts import SellingAccounts
from ads_api.client.v1.sp import SP
from ads_api.client.v1.sp_global import SPGlobal
from ads_api.client.v1.st import ST
from ads_api.config.settings import AmazonAdsConfig
from ads_api.errors import MissingConfigError


class AdsClientV1:
    """Async client for Amazon Ads API v1.

    Ad products are nested; unscoped APIs hang off the client:

        async with AdsClientV1(config) as ads:
            await ads.sp.campaigns.create_campaign(body)
            await ads.selling_accounts.query_selling_account(body)
    """

    @overload
    def __init__(self, config: AmazonAdsConfig) -> None: ...

    @overload
    def __init__(self, *, ctx: ClientContext) -> None: ...

    def __init__(
        self,
        config: AmazonAdsConfig | None = None,
        *,
        ctx: ClientContext | None = None,
    ) -> None:
        if ctx is not None:
            self._ctx = ctx
            self._owns_ctx = False
        elif config is not None:
            self._ctx = ClientContext(config)
            self._owns_ctx = True
        else:
            raise MissingConfigError()
        self.__sp: SP | None = None
        self.__sp_global: SPGlobal | None = None
        self.__sb: SB | None = None
        self.__sd: SD | None = None
        self.__dsp: DSP | None = None
        self.__st: ST | None = None
        self.__advertiser_accounts: AdvertiserAccounts | None = None
        self.__brand_store_edition_publish_versions: BrandStoreEditionPublishVersions | None = None
        self.__brand_store_editions: BrandStoreEditions | None = None
        self.__brand_store_pages: BrandStorePages | None = None
        self.__brand_stores: BrandStores | None = None
        self.__manager_accounts: ManagerAccounts | None = None
        self.__reports: Reports | None = None
        self.__selling_accounts: SellingAccounts | None = None

    async def __aenter__(self) -> AdsClientV1:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def close(self) -> None:
        if self._owns_ctx:
            await self._ctx.close()

    @property
    def sp(self) -> SP:
        if self.__sp is None:
            self.__sp = SP(self._ctx)
        return self.__sp

    @property
    def sp_global(self) -> SPGlobal:
        if self.__sp_global is None:
            self.__sp_global = SPGlobal(self._ctx)
        return self.__sp_global

    @property
    def sb(self) -> SB:
        if self.__sb is None:
            self.__sb = SB(self._ctx)
        return self.__sb

    @property
    def sd(self) -> SD:
        if self.__sd is None:
            self.__sd = SD(self._ctx)
        return self.__sd

    @property
    def dsp(self) -> DSP:
        if self.__dsp is None:
            self.__dsp = DSP(self._ctx)
        return self.__dsp

    @property
    def st(self) -> ST:
        if self.__st is None:
            self.__st = ST(self._ctx)
        return self.__st

    @property
    def advertiser_accounts(self) -> AdvertiserAccounts:
        if self.__advertiser_accounts is None:
            self.__advertiser_accounts = AdvertiserAccounts(self._ctx)
        return self.__advertiser_accounts

    @property
    def brand_store_edition_publish_versions(self) -> BrandStoreEditionPublishVersions:
        if self.__brand_store_edition_publish_versions is None:
            self.__brand_store_edition_publish_versions = BrandStoreEditionPublishVersions(self._ctx)
        return self.__brand_store_edition_publish_versions

    @property
    def brand_store_editions(self) -> BrandStoreEditions:
        if self.__brand_store_editions is None:
            self.__brand_store_editions = BrandStoreEditions(self._ctx)
        return self.__brand_store_editions

    @property
    def brand_store_pages(self) -> BrandStorePages:
        if self.__brand_store_pages is None:
            self.__brand_store_pages = BrandStorePages(self._ctx)
        return self.__brand_store_pages

    @property
    def brand_stores(self) -> BrandStores:
        if self.__brand_stores is None:
            self.__brand_stores = BrandStores(self._ctx)
        return self.__brand_stores

    @property
    def manager_accounts(self) -> ManagerAccounts:
        if self.__manager_accounts is None:
            self.__manager_accounts = ManagerAccounts(self._ctx)
        return self.__manager_accounts

    @property
    def reports(self) -> Reports:
        if self.__reports is None:
            self.__reports = Reports(self._ctx)
        return self.__reports

    @property
    def selling_accounts(self) -> SellingAccounts:
        if self.__selling_accounts is None:
            self.__selling_accounts = SellingAccounts(self._ctx)
        return self.__selling_accounts
