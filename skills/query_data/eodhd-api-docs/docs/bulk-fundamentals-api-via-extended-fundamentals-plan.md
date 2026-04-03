---
id: "url-64ec2af9"
type: "api"
title: "Bulk Fundamentals API (via Extended Fundamentals Plan)"
url: "https://eodhd.com/financial-apis/bulk-fundamentals-api-via-extended-fundamentals-plan"
description: "With the Bulk Fundamentals API endpoint, you can download fundamental data for hundreds of companies in a single request."
source: ""
tags: []
crawl_time: "2026-03-18T12:11:09.866Z"
metadata:
  endpoint: "https://eodhd.com/api/bulk-fundamentals/NASDAQ"
  parameters: []
  markdownContent: "# Bulk Fundamentals API (via Extended Fundamentals Plan)\n\nWith the Bulk Fundamentals API endpoint, you can download fundamental data for hundreds of companies in a single request.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/bulk-fundamentals/NASDAQ?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/bulk-fundamentals/NASDAQ?offset=500&limit=100&api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/bulk-fundamentals/NASDAQ?&symbols=AAPL.US,MSFT.US&api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n\n## Limitations\n\nDue to the high load of these requests and other technical reasons, the Bulk Fundamentals API has the following limitations:\n\n## Request Examples\n\nGet fundamentals for an entire exchange:\n\nThe default output format is CSV. To receive data in JSON format, you must add &fmt=json. We strongly recommend using the JSON format.\n\n## Pagination with offset and limit\n\nTo reduce the amount of data returned in a single request, you can use the “offset” and “limit” parameters, which work like pagination:\n\nExample: “to retrieve 200 symbols starting from symbol #1000”:\n\n## Request data for specific symbols\n\nYou can also retrieve fundamentals data for specific symbols instead of an entire exchange by using the “symbols” parameter.When “symbols” is specified, the exchange code is ignored.\n\n## Bulk Fundamentals Output\n\nHere is an example of the Bulk Fundamentals API output for Apple Inc. (AAPL.US) and Microsoft Corporation (MSFT.US) in CSV format.\n\nMost fields are the same as in the standard Fundamentals API, with the following differences:\n\n## Version 1.2 Output\n\nIf you need the output to be as close as possible to the current Fundamentals API template, you can add the parameter:\n\nWith version 1.2:\n\n## Code Examples\n\n```text\n&version=1.2\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "bulk-fundamentals-api-via-extended-fundamentals-plan"
---

# Bulk Fundamentals API (via Extended Fundamentals Plan)

## 源URL

https://eodhd.com/financial-apis/bulk-fundamentals-api-via-extended-fundamentals-plan

## 描述

With the Bulk Fundamentals API endpoint, you can download fundamental data for hundreds of companies in a single request.

## API 端点

**Endpoint**: `https://eodhd.com/api/bulk-fundamentals/NASDAQ`

## 文档正文

With the Bulk Fundamentals API endpoint, you can download fundamental data for hundreds of companies in a single request.

## API Endpoint

```text
https://eodhd.com/api/bulk-fundamentals/NASDAQ?api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/bulk-fundamentals/NASDAQ?offset=500&limit=100&api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/bulk-fundamentals/NASDAQ?&symbols=AAPL.US,MSFT.US&api_token={YOUR_API_TOKEN}&fmt=json
```

## Limitations

Due to the high load of these requests and other technical reasons, the Bulk Fundamentals API has the following limitations:

## Request Examples

Get fundamentals for an entire exchange:

The default output format is CSV. To receive data in JSON format, you must add &fmt=json. We strongly recommend using the JSON format.

## Pagination with offset and limit

To reduce the amount of data returned in a single request, you can use the “offset” and “limit” parameters, which work like pagination:

Example: “to retrieve 200 symbols starting from symbol #1000”:

## Request data for specific symbols

You can also retrieve fundamentals data for specific symbols instead of an entire exchange by using the “symbols” parameter.When “symbols” is specified, the exchange code is ignored.

## Bulk Fundamentals Output

Here is an example of the Bulk Fundamentals API output for Apple Inc. (AAPL.US) and Microsoft Corporation (MSFT.US) in CSV format.

Most fields are the same as in the standard Fundamentals API, with the following differences:

## Version 1.2 Output

If you need the output to be as close as possible to the current Fundamentals API template, you can add the parameter:

With version 1.2:

## Code Examples

```text
&version=1.2
```

## Related APIs

- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)
- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)
- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)
- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)
- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)
- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)
- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)
- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)
- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)
- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)
