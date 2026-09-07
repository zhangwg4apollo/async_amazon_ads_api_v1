---
title: Limits and best practices
description: Limits and best practices
type: guide
interface: api
tags:
  - Reporting
keywords: []
---

# Limits and best practices

Amazon Ads places limits on how its APIs can be accessed, and how data is generated.  It is important to be aware of these limits, as well as how APIs will react when those limits are breached so that you can account for that as part of your API integration.

## Request frequency

Amazon places limits on the frequency of requests to its APIs in general, as well as specific endpoints.  There are limits both on concurrent calls to its endpoints, as well as how frequent those calls are made.  If those limits are breached the system will return an HTTP `429` error code.  It is recommended to implement adaptive integrations which will react to these errors and reduce the number of calls made to the service.

## Report size and complexity

Reporting API v1 introduces the idea of flexible reporting, allowing a choice from an extensive list of metrics and dimensions, while also extending date ranges and historical look-back capabilities.  While these are powerful capabilities, when combined it can result in extremely large data files.

When a report is submitted that will result in a file that is too large, that report request may fail immediately, or may fail after a period of attempting to process that report.  It is important to ensure that your download integration considers failure modes and how to react to them.  Repeating the same request may result in repetitive failures if the report is too large to process.

## Best practices

> [TIP] Begin with the [Amazon Ads Well-Architected Framework](guides/amazon-ads-well-architected-framework/fundamental-component#fundamental-best-practices), which provides general guidelines and best practices.


To avoid report request or generation failures, it is recommended to use the appropriate tools for specific use cases.

* **Consider Amazon Marketing Stream as a primary data acquisition tool**
    * Amazon Marketing Stream is a push-based programmatic reporting solution that allows customers to subscribe to datasets and receive automatic updates to metrics as often as every 15 minutes. With parity with API in metrics/dimensions and historical look-back, Stream is the ideal surface for businesses requiring data at scale and want to avoid traditional API constraints such as throttling. It is recommended that most use cases shift to Amazon Marketing Stream.
* **Optimize for Performance and Efficiency**
    * Please note that Reporting API is not intended for near real-time data updates. To keep your metrics updated with near real-time data access, consider using Amazon Marketing Stream
    * Generate smaller data sets, and work to combine them after downloading each segment.  This is the simplest way to ensure that reports are regularly successful despite seasonal increases in cardinality.
    * The Unified Reporting API enforces limits on “concurrent report generation requests” and “request rates” to ensure system stability. The concurrency limit restricts the number of simultaneously running report generation requests to as low as 1, while the rate limit can be as low as 1 request per second (both limits may vary per client). When either limit is exceeded, new requests will receive an HTTP `429` (Too Many Requests) error until previous requests complete or the rate limit window resets. To handle throttling gracefully, implement exponential backoff retry logic starting with a 1-second delay and doubling with each subsequent retry, distribute requests evenly over time (normally a day) rather than sending bursts. Systems should be designed to pace requests and handle `429` responses to avoid repeated throttling.
    * If your application requires higher concurrency limits than provided, submit a [support ticket](support/overview) outlining your use case and expected request patterns. Requests are reviewed on a case-by-case basis, and approval is not guaranteed.
* **Test and Validate Before Automating**
    * Experiment with data generation manually before automating requests to understand the size and cardinality of the data you request.  Smaller, simpler data sets will be generated more quickly, and will be easier to process resulting in reduced time to effective use of that data.
* **Handle Error Modes and Failures Properly**
    * Implement exponential backoff circuit breakers to respond to `429` error codes, and `500` series HTTP error codes.  Immediately repeating requests may result in continued error codes until the bottleneck subsides.
    * Monitor failures, HTTP error responses and react accordingly.  Establish appropriate alarms to ensure that data access is available for your use cases.
