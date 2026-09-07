"""Auto-generated models for Reports from Amazon Ads API v1."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import Field

from ads_api.models._core.base import LenientModel, StrictModel

type ComparisonOperator = Literal["EQUALS", "IN"]
"""
Supported values:
- `EQUALS`: Exact equality match, where exactly a single value has to be provided
- `IN`: Exact equality match, where at least one value has to be provided
"""


type CurrencyCode = Literal[
    "AED",
    "ARS",
    "AUD",
    "AZN",
    "BBD",
    "BGN",
    "BMD",
    "BND",
    "BRL",
    "BSD",
    "CAD",
    "CHF",
    "CLP",
    "CNY",
    "COP",
    "CRC",
    "CZK",
    "DKK",
    "DOP",
    "EGP",
    "EUR",
    "GBP",
    "GHS",
    "GTQ",
    "HKD",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "JMD",
    "JPY",
    "KES",
    "KRW",
    "KYD",
    "KZT",
    "LBP",
    "LKR",
    "MAD",
    "MUR",
    "MXN",
    "MYR",
    "NAD",
    "NGN",
    "NOK",
    "NZD",
    "PAB",
    "PEN",
    "PHP",
    "PKR",
    "PLN",
    "QAR",
    "RON",
    "RUB",
    "SAR",
    "SEK",
    "SGD",
    "THB",
    "TRY",
    "TTD",
    "TWD",
    "TZS",
    "USD",
    "UYU",
    "VND",
    "XAF",
    "XCD",
    "XOF",
    "XPF",
    "ZAR",
]
"""
Supported values:
- `AED`: United Arab Emirates Dirham
- `ARS`: Argentine Peso
- `AUD`: Australian Dollar
- `AZN`: Azerbaijani Manat
- `BBD`: Barbadian Dollar
- `BGN`: Bulgarian Lev
- `BMD`: Bermudian Dollar
- `BND`: Brunei Dollar
- `BRL`: Brazilian Real
- `BSD`: Bahamian Dollar
- `CAD`: Canadian Dollar
- `CHF`: Swiss Franc
- `CLP`: Chilean Peso
- `CNY`: Chinese Yuan
- `COP`: Colombian Peso
- `CRC`: Costa Rican Colón
- `CZK`: Czech Koruna
- `DKK`: Danish Krone
- `DOP`: Dominican Peso
- `EGP`: Egyptian Pound
- `EUR`: Euro
- `GBP`: British Pound Sterling
- `GHS`: Ghanaian Cedi
- `GTQ`: Guatemalan Quetzal
- `HKD`: Hong Kong Dollar
- `HUF`: Hungarian Forint
- `IDR`: Indonesian Rupiah
- `ILS`: Israeli New Shekel
- `INR`: Indian Rupee
- `JMD`: Jamaican Dollar
- `JPY`: Japanese Yen
- `KES`: Kenyan Shilling
- `KRW`: South Korean Won
- `KYD`: Cayman Islands Dollar
- `KZT`: Kazakhstani Tenge
- `LBP`: Lebanese Pound
- `LKR`: Sri Lankan Rupee
- `MAD`: Moroccan Dirham
- `MUR`: Mauritian Rupee
- `MXN`: Mexican Peso
- `MYR`: Malaysian Ringgit
- `NAD`: Namibian Dollar
- `NGN`: Nigerian Naira
- `NOK`: Norwegian Krone
- `NZD`: New Zealand Dollar
- `PAB`: Panamanian Balboa
- `PEN`: Peruvian Sol
- `PHP`: Philippine Peso
- `PKR`: Pakistani Rupee
- `PLN`: Polish Złoty
- `QAR`: Qatari Riyal
- `RON`: Romanian Leu
- `RUB`: Russian Ruble
- `SAR`: Saudi Riyal
- `SEK`: Swedish Krona
- `SGD`: Singapore Dollar
- `THB`: Thai Baht
- `TRY`: Turkish Lira
- `TTD`: Trinidad and Tobago Dollar
- `TWD`: New Taiwan Dollar
- `TZS`: Tanzanian Shilling
- `USD`: United States Dollar
- `UYU`: Uruguayan Peso
- `VND`: Vietnamese Đồng
- `XAF`: Central African CFA Franc
- `XCD`: East Caribbean Dollar
- `XOF`: West African CFA Franc
- `XPF`: CFP Franc
- `ZAR`: South African Rand
"""


type ErrorCode = Literal[
    "BAD_REQUEST", "CONTENT_TOO_LARGE", "FORBIDDEN", "INTERNAL_ERROR", "NOT_FOUND", "TOO_MANY_REQUESTS", "UNAUTHORIZED"
]
"""
Supported values:
- `BAD_REQUEST`: The request is not valid considering the documented schema.
- `CONTENT_TOO_LARGE`: The request is too large. Consider splitting it into multiple requests.
- `FORBIDDEN`: The caller is not authorized to make the given request.
- `INTERNAL_ERROR`: The server encountered an unexpected condition that prevented it from fulfilling the request.
- `NOT_FOUND`: The requested resource does not exist.
- `TOO_MANY_REQUESTS`: There have been too many requests, please slow down your call rate.
- `UNAUTHORIZED`: The request lacks the necessary credentials.
"""


type ReportFormat = Literal["CSV", "GZIP_JSON", "PARTITIONED_CSV", "PARTITIONED_GZIP_JSON"]
"""
Supported values:
- `CSV`: Comma-separated values file containing plain text tabular data
- `GZIP_JSON`: JSON file compressed using GZIP format
- `PARTITIONED_CSV`: Contents split into multiple CSV files
- `PARTITIONED_GZIP_JSON`: Contents split into multiple GZIP-compressed JSON files
"""


type ReportStatus = Literal["COMPLETED", "FAILED", "PENDING", "PROCESSING"]


class ComparisonPredicate(LenientModel):
    comparisonOperator: ComparisonOperator | str
    field: str = Field(pattern="^[a-zA-Z0-9]+\\.[a-zA-Z0-9]+$")
    not_: bool = Field(alias="not")
    values: list[str] = Field(min_length=1, max_length=2000)


class CompositePredicate(LenientModel):
    filters: list[Filter] = Field(min_length=1, max_length=10)


class CreateComparisonPredicate(StrictModel):
    comparisonOperator: ComparisonOperator
    field: str = Field(pattern="^[a-zA-Z0-9]+\\.[a-zA-Z0-9]+$")
    not_: bool = Field(alias="not")
    values: list[str] = Field(min_length=1, max_length=2000)


class CreateCompositePredicate(StrictModel):
    filters: list[CreateFilter] = Field(min_length=1, max_length=10)


class CreateDatePeriod(StrictModel):
    endDate: date
    startDate: date


class CreateFilterAnd(StrictModel):
    and_: CreateCompositePredicate = Field(alias="and")


class CreateFilterOn(StrictModel):
    on: CreateComparisonPredicate


type CreateFilter = CreateFilterAnd | CreateFilterOn


class CreateReportPeriod(StrictModel):
    datePeriod: CreateDatePeriod


class CreateReportRequest(StrictModel):
    accessRequestedAccounts: list[ReportCreateAccessRequestedAccountItem] = Field(min_length=1, max_length=2000)
    reports: list[ReportCreate] = Field(min_length=1, max_length=1)


class CreateReportingQuery(StrictModel):
    fields: list[str] = Field(min_length=1, max_length=1000)
    filter: CreateFilter | None = Field(default=None)


class DatePeriod(LenientModel):
    endDate: date
    startDate: date


class DeleteReportRequest(StrictModel):
    reportIds: list[str] = Field(min_length=1, max_length=1)


class Error(LenientModel):
    code: ErrorCode | str
    fieldLocation: str | None = Field(default=None)
    message: str


class ErrorsIndex(LenientModel):
    errors: list[Error] = Field(min_length=1, max_length=20)
    index: int = Field(ge=0, le=0)


class FilterAnd(LenientModel):
    and_: CompositePredicate = Field(alias="and")


class FilterOn(LenientModel):
    on: ComparisonPredicate


type Filter = FilterAnd | FilterOn


class Report(LenientModel):
    completedDateTime: datetime | None = Field(default=None)
    completedReportParts: list[ReportPart] | None = Field(default=None, min_length=0, max_length=100)
    creationDateTime: datetime
    currencyOfView: CurrencyCode | str | None = Field(default=None)
    failureCode: str | None = Field(default=None)
    failureReason: str | None = Field(default=None)
    format: ReportFormat | str
    lastUpdatedDateTime: datetime
    periods: list[ReportPeriod] = Field(min_length=1, max_length=1)
    query: ReportingQuery
    reportId: str
    status: ReportStatus | str


class ReportCreate(StrictModel):
    currencyOfView: CurrencyCode | None = Field(default=None)
    format: ReportFormat
    periods: list[CreateReportPeriod] = Field(min_length=1, max_length=1)
    query: CreateReportingQuery


class ReportCreateAccessRequestedAccountItemAdvertiserAccountId(StrictModel):
    advertiserAccountId: str


class ReportCreateAccessRequestedAccountItemManagerAccountId(StrictModel):
    managerAccountId: str


type ReportCreateAccessRequestedAccountItem = ReportCreateAccessRequestedAccountItemAdvertiserAccountId | ReportCreateAccessRequestedAccountItemManagerAccountId


class ReportMultiStatusResponse(LenientModel):
    error: list[ErrorsIndex] | None = Field(default=None, min_length=0, max_length=1)
    success: list[ReportMultiStatusSuccess] | None = Field(default=None, min_length=0, max_length=1)


class ReportMultiStatusSuccess(LenientModel):
    index: int = Field(ge=0, le=0)
    report: Report


class ReportPart(LenientModel):
    """A downloadable part of the generated report"""

    sizeInBytes: int = Field(
        ge=0, le=9223372036854776000, description="Size of the part file in bytes, could reach up to 100GB"
    )
    url: str = Field(description="URL of the report part")
    urlExpirationDateTime: datetime = Field(description="Expiration date and time when the above URL expires")


class ReportPeriod(LenientModel):
    datePeriod: DatePeriod


class ReportingQuery(LenientModel):
    fields: list[str] = Field(min_length=1, max_length=1000)
    filter: Filter | None = Field(default=None)


class RetrieveReportRequest(StrictModel):
    reportIds: list[str] = Field(min_length=1, max_length=1)


__all__ = [
    "ComparisonOperator",
    "ComparisonPredicate",
    "CompositePredicate",
    "CreateComparisonPredicate",
    "CreateCompositePredicate",
    "CreateDatePeriod",
    "CreateFilter",
    "CreateReportPeriod",
    "CreateReportRequest",
    "CreateReportingQuery",
    "CurrencyCode",
    "DatePeriod",
    "DeleteReportRequest",
    "Error",
    "ErrorCode",
    "ErrorsIndex",
    "Filter",
    "Report",
    "ReportCreate",
    "ReportCreateAccessRequestedAccountItem",
    "ReportFormat",
    "ReportMultiStatusResponse",
    "ReportMultiStatusSuccess",
    "ReportPart",
    "ReportPeriod",
    "ReportStatus",
    "ReportingQuery",
    "RetrieveReportRequest",
]
