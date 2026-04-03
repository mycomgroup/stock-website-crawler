---
id: "url-64775267"
type: "api"
title: "CBOE Europe Indices API (beta)"
url: "https://eodhd.com/financial-apis/cboe-europe-indices-api-beta"
description: "The CBOE Indices Data API provides structured access to daily CBOE index data (European stocks) across multiple European and regional index families. Each index includes complete metadata such as region, index code, calculation date, closing level, divisor, and a full list of constituents with prices, weights, currency, and classification details."
source: ""
tags: []
crawl_time: "2026-03-18T03:08:46.388Z"
metadata:
  endpoint: "https://eodhd.com/api/cboe/indices"
  parameters:
    - {"name":"filter[index_code]","description":"Yes"}
    - {"name":"filter[feed_type]","description":"Yes"}
    - {"name":"filter[date]","description":"Yes"}
    - {"name":"api_token","description":"Yes"}
    - {"name":"fmt","description":"No"}
  markdownContent: "# CBOE Europe Indices API (beta)\n\nThe CBOE Indices Data API provides structured access to daily CBOE index data (European stocks) across multiple European and regional index families. Each index includes complete metadata such as region, index code, calculation date, closing level, divisor, and a full list of constituents with prices, weights, currency, and classification details.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/cboe/indices?api_token=DEMO&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/cboe/index?filter[index_code]=BDE30P&filter[feed_type]=snapshot_official_closing&filter[date]=2017-02-01&api_token=YOUR_API_KEY&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| filter[index_code] | Yes |\n| filter[feed_type] | Yes |\n| filter[date] | Yes |\n| api_token | Yes |\n| fmt | No |\n\n\n## Description\n\nThis endpoint returns the full list of CBOE indices available via EODHD, including:\n\nUse this endpoint when you need to:\n\nPagination is handled via the “links.next” field – if it is not null, call the URL provided there to get the next page.\n\n## Request Example\n\nNote: Pagination is controlled via the “links.next” field in the response. You don’t need to construct pagination parameters manually – just follow the URL in “links.next” until it becomes null.\n\n## Description\n\nThis endpoint returns detailed feed data for a single CBOE index on a specific date and feed type, including:\n\nUse it when you need:\n\n## Parameters\n\nAll filter parameters are passed as filter[…] query parameters (deep object style).\n\n## Code Examples\n\n```text\nhttps://eodhd.com/api/cboe/indices\n```\n\n```text\n...\n{\n\"id\": \"BAT20P\",\n\"type\": \"cboe-index\",\n\"attributes\": {\n\"region\": \"Austria\",\n\"index_code\": \"BAT20P\",\n\"feed_type\": \"snapshot_official_closing\",\n\"date\": \"2017-04-12\",\n\"index_close\": 10549.68,\n\"index_divisor\": 4269150.786625\n}\n},\n{\n\"id\": \"BDE30P\",\n\"type\": \"cboe-index\",\n\"attributes\": {\n\"region\": \"Germany\",\n\"index_code\": \"BDE30P\",\n\"feed_type\": \"snapshot_official_closing\",\n\"date\": \"2017-02-01\",\n\"index_close\": 13915.57,\n\"index_divisor\": 68033376.886244\n}\n},\n{\n\"id\": \"BDES50N\",\n\"type\": \"cboe-index\",\n\"attributes\": {\n\"region\": \"Germany\",\n\"index_code\": \"BDES50N\",\n\"feed_type\": \"snapshot_official_closing\",\n\"date\": \"2017-02-01\",\n\"index_close\": 20143.79,\n\"index_divisor\": 2246357.472101\n}\n...\n```\n\n```text\nhttps://eodhd.com/api/cboe/index\n```\n\n```json\n{\n\"meta\": {\n\"total\": 1\n},\n\"data\": [\n{\n\"id\": \"BDE30P-2017-02-01-snapshot_official_closing\",\n\"type\": \"cboe-index\",\n\"attributes\": {\n\"region\": \"Germany\",\n\"index_code\": \"BDE30P\",\n\"feed_type\": \"snapshot_official_closing\",\n\"date\": \"2017-02-01\",\n\"index_close\": 13915.57,\n\"index_divisor\": 68033376.886244,\n\"effective_date\": null,\n\"review_date\": null\n},\n\"components\": [\n{\n\"id\": \"BDE30P-2017-02-01-snapshot_official_closing-HEI.DU\",\n\"type\": \"cboe-index-component\",\n\"attributes\": {\n\"symbol\": \"HEI.DU\",\n\"isin\": \"DE0006047004\",\n\"name\": \"HEIDELBERGCEMENT AG\",\n\"equity\": \"HEIG IX Equity\",\n\"sedol\": null,\n\"cusip\": \"HEId\",\n\"country\": \"GERMANY\",\n\"revenue_country\": null,\n\"closing_price\": 90.15,\n\"currency\": \"EUR\",\n\"closing_factor\": 1,\n\"total_shares\": 198416477,\n\"market_cap\": 17887245401.55,\n\"market_cap_free_float\": 12878816689.116,\n\"free_float_factor\": 0.72,\n\"weighting_cap_factor\": 1,\n\"index_weighting\": 1.360357,\n\"index_shares\": 2.09985,\n\"index_value\": 189.301447,\n\"sector\": \"Non-Energy Materials\"\n}\n},\n{\n\"id\": \"BDE30P-2017-02-01-snapshot_official_closing-SIE.DU\",\n\"type\": \"cboe-index-component\",\n\"attributes\": {\n\"symbol\": \"SIE.DU\",\n\"isin\": \"DE0007236101\",\n\"name\": \"SIEMENS AG\",\n\"equity\": \"SIED IX Equity\",\n\"sedol\": null,\n\"cusip\": \"SIEd\",\n\"country\": \"GERMANY\",\n\"revenue_country\": null,\n\"closing_price\": 122.4,\n\"currency\": \"EUR\",\n\"closing_factor\": 1,\n\"total_shares\": 808278318,\n\"market_cap\": 98933266123.20001,\n\"market_cap_free_float\": 93986602817.04001,\n\"free_float_factor\": 0.95,\n\"weighting_cap_factor\": 1,\n\"index_weighting\": 9.927568,\n\"index_shares\": 11.286584,\n\"index_value\": 1381.477844,\n\"sector\": \"Industrials\"\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "cboe-europe-indices-api-beta"
---

# CBOE Europe Indices API (beta)

## 源URL

https://eodhd.com/financial-apis/cboe-europe-indices-api-beta

## 描述

The CBOE Indices Data API provides structured access to daily CBOE index data (European stocks) across multiple European and regional index families. Each index includes complete metadata such as region, index code, calculation date, closing level, divisor, and a full list of constituents with prices, weights, currency, and classification details.

## API 端点

**Endpoint**: `https://eodhd.com/api/cboe/indices`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `filter[index_code]` | - | 否 | - | Yes |
| `filter[feed_type]` | - | 否 | - | Yes |
| `filter[date]` | - | 否 | - | Yes |
| `api_token` | - | 否 | - | Yes |
| `fmt` | - | 否 | - | No |

## 文档正文

The CBOE Indices Data API provides structured access to daily CBOE index data (European stocks) across multiple European and regional index families. Each index includes complete metadata such as region, index code, calculation date, closing level, divisor, and a full list of constituents with prices, weights, currency, and classification details.

## API Endpoint

```text
https://eodhd.com/api/cboe/indices?api_token=DEMO&fmt=json
```

```text
https://eodhd.com/api/cboe/index?filter[index_code]=BDE30P&filter[feed_type]=snapshot_official_closing&filter[date]=2017-02-01&api_token=YOUR_API_KEY&fmt=json
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| filter[index_code] | Yes |
| filter[feed_type] | Yes |
| filter[date] | Yes |
| api_token | Yes |
| fmt | No |

## Description

This endpoint returns the full list of CBOE indices available via EODHD, including:

Use this endpoint when you need to:

Pagination is handled via the “links.next” field – if it is not null, call the URL provided there to get the next page.

## Request Example

Note: Pagination is controlled via the “links.next” field in the response. You don’t need to construct pagination parameters manually – just follow the URL in “links.next” until it becomes null.

## Description

This endpoint returns detailed feed data for a single CBOE index on a specific date and feed type, including:

Use it when you need:

## Parameters

All filter parameters are passed as filter[…] query parameters (deep object style).

## Code Examples

```text
https://eodhd.com/api/cboe/indices
```

```text
...
{
"id": "BAT20P",
"type": "cboe-index",
"attributes": {
"region": "Austria",
"index_code": "BAT20P",
"feed_type": "snapshot_official_closing",
"date": "2017-04-12",
"index_close": 10549.68,
"index_divisor": 4269150.786625
}
},
{
"id": "BDE30P",
"type": "cboe-index",
"attributes": {
"region": "Germany",
"index_code": "BDE30P",
"feed_type": "snapshot_official_closing",
"date": "2017-02-01",
"index_close": 13915.57,
"index_divisor": 68033376.886244
}
},
{
"id": "BDES50N",
"type": "cboe-index",
"attributes": {
"region": "Germany",
"index_code": "BDES50N",
"feed_type": "snapshot_official_closing",
"date": "2017-02-01",
"index_close": 20143.79,
"index_divisor": 2246357.472101
}
...
```

```text
https://eodhd.com/api/cboe/index
```

```json
{
"meta": {
"total": 1
},
"data": [
{
"id": "BDE30P-2017-02-01-snapshot_official_closing",
"type": "cboe-index",
"attributes": {
"region": "Germany",
"index_code": "BDE30P",
"feed_type": "snapshot_official_closing",
"date": "2017-02-01",
"index_close": 13915.57,
"index_divisor": 68033376.886244,
"effective_date": null,
"review_date": null
},
"components": [
{
"id": "BDE30P-2017-02-01-snapshot_official_closing-HEI.DU",
"type": "cboe-index-component",
"attributes": {
"symbol": "HEI.DU",
"isin": "DE0006047004",
"name": "HEIDELBERGCEMENT AG",
"equity": "HEIG IX Equity",
"sedol": null,
"cusip": "HEId",
"country": "GERMANY",
"revenue_country": null,
"closing_price": 90.15,
"currency": "EUR",
"closing_factor": 1,
"total_shares": 198416477,
"market_cap": 17887245401.55,
"market_cap_free_float": 12878816689.116,
"free_float_factor": 0.72,
"weighting_cap_factor": 1,
"index_weighting": 1.360357,
"index_shares": 2.09985,
"index_value": 189.301447,
"sector": "Non-Energy Materials"
}
},
{
"id": "BDE30P-2017-02-01-snapshot_official_closing-SIE.DU",
"type": "cboe-index-component",
"attributes": {
"symbol": "SIE.DU",
"isin": "DE0007236101",
"name": "SIEMENS AG",
"equity": "SIED IX Equity",
"sedol": null,
"cusip": "SIEd",
"country": "GERMANY",
"revenue_country": null,
"closing_price": 122.4,
"currency": "EUR",
"closing_factor": 1,
"total_shares": 808278318,
"market_cap": 98933266123.20001,
"market_cap_free_float": 93986602817.04001,
"free_float_factor": 0.95,
"weighting_cap_factor": 1,
"index_weighting": 9.927568,
"index_shares": 11.286584,
"index_value": 1381.477844,
"sector": "Industrials"
}
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
