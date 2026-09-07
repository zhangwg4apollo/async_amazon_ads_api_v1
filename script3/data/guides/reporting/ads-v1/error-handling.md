---
title: Handling errors
description: Handling errors
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Handling errors

When errors occur, the API provides all available context to support troubleshooting of that error. The API uses a common structure to model all request errors, regardless of the type. The shape of the API response will be:

```json
{
  "code": "{THE_ERROR_CODE}",
  "message": "{THE_ERROR_MESSAGE}"
}
```

The response also includes a specific HTTP status code related to the type of error:

* `400: Bad Request`
    * This is a generic bad request, and more details will be provided about what went wrong (including error codes) within the JSON response (see below).
* `401: Unauthorized`
    * The mechanism used to provide identity and authorization was not recognized.
* `403: Forbidden`
    * The data requested is not authorized for the account provided. Do not re-request the data until permissions have been explored and adjusted for the account.
* `429: Too Many Requests`
    * Requests are too frequent or too large. Implement backoff mechanisms to ensure quotas are adhered to.
* `500: Internal Server Error`
    * An internal error, please reach out to support to better understand this failure.
* `503: Service Unavailable`
    * An internal error, please reach out to support to better understand this failure.

> [NOTE] The new API uses a bulk request model, and that also allows for partial failure scenarios via the `207: Multi-Status` status code. Currently, bulk requests only support a single sub-request, so the `207` status code is not used for errors. This may change in the future.

## Handling bad requests

When you receive a `400: Bad Request` HTTP status code, you can inspect the `code` and `message` in the JSON response to understand what went wrong.

* `code`: If the request contained a single error (e.g. an unknown field) the `code` will be set to the related error code (e.g. `400005`). However, if the request contained multiple errors (e.g. an unknown field and a malformed period), the `code` will be set to the multi-error code (i.e. `400100`).
* `message`: The message will include comma-separated error messages for each error in the request. With this detail, you can adjust your request accordingly. For example: `400007: {MESSAGE_1}, 400015: {MESSAGE_2}, 400019: {MESSAGE_3}`.

For instance, you would receive the following error if you attempted to request an unknown metric:

```json
{
  "code": "400005",
  "message": "400005: field metric.foo is unknown"
}
```

All of the possible error codes are documented below. This list may grow over time as use cases are expanded.

### Available error codes

| Code   | Reason                                                                                                  |
|--------|---------------------------------------------------------------------------------------------------------|
| 400000 | The JSON request body provided was malformed.                                                           |
| 400001 | A generic client-related error occurred.                                                                |
| 400004 | The fields included fields that are incompatible with one another.                                      |
| 400005 | The fields included a reporting field ID that does not exist.                                           |
| 400006 | The fields included a field without also including its required field.                                  |
| 400007 | The period start date was after the period end date.                                                    |
| 400009 | The period was in the future.                                                                           |
| 400011 | The fields included the same field multiple times.                                                      |
| 400013 | The fields included a value that is not a properly formatted reporting field ID.                        |
| 400014 | The fields did not include at least one metric (e.g. `metric.impressions`).                               |
| 400015 | The fields did not include at least one Level of Detail dimension (e.g. `campaign.id`).                   |
| 400016 | The fields did not include at least one Time dimension (e.g. `date.value`).                               |
| 400017 | The provided format is not supported.                                                                   |
| 400019 | The number of `accessRequestedAccounts` exceeds the available limit.                                      |
| 400020 | The filter provided references invalid, unknown, or unallowed fields.                                   |
| 400021 | The filter may only have `and` or `on` provided at the root level.                                      |
| 400022 | The filter provided included an incomplete `and` filter.                                                |
| 400023 | The filter provided an invalid `and` filter.                                                            |
| 400025 | The period exceeded the available look-back for the included time dimensions.                           |
| 400026 | The `accessRequestedAccounts` provided are either unauthorized or do not have linked advertiser accounts. |
| 400027 | The included `convertedCurrency.value` field requires `currencyOfView` to be set.                           |
| 400100 | The request had multiple different errors.                                                              |
| 404001 | The requested `reportId` was not found.                                                                   |
| 500100 | An unhandled internal error occurred.                                                                   |

## Handling asynchronous failures

In the event of a failure, all available information is communicated about the failure in the retrieve report API response in the `failureCode` and `failureReason` attributes:

```json
{
  "error": null,
  "success": [
    {
      "index": 0,
      "report": {
        "creationDateTime": "2025-11-05T00:00:38.285Z",
        "format": "CSV",
        "failureCode": "{SPECIFIC_FAILURE_CODE}",
        "failureReason": "{SPECIFIC_FAILURE_REASON}"
        "lastUpdatedDateTime": "2025-11-05T00:00:38.285Z",
        "periods": [
          {
            "datePeriod": {
              "startDate": "2025-10-28",
              "endDate": "2025-11-04"
            }
          }
        ],
        "query": {
          "fields": [
            "dateRange.value",
            "advertiserAccount.id",
            "advertiserAccount.name",
            "metric.sales"
          ]
        },
        "reportId": "{YOUR_REPORT_ID}",
        "status": "FAILED"
      }
    }
  ]
}
```

### Available failure codes

| Code | Reason |
|------|--------|
| 001  | An unhandled internal failure occurred. Try again, and if the issue persists, contact support. |
| 002  | The report you requested was too large. Adjust your request to reduce the date period, number of accounts, or included fields. |
