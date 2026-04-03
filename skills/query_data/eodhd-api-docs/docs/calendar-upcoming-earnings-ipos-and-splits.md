---
id: "url-c513d3d"
type: "api"
title: "Calendar API: Upcoming Dividends, Earnings, Trends, IPOs and Splits"
url: "https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits/"
description: "With our Financial Calendar data feed, we provide information about upcoming earnings, IPOs, and splits. If you are looking for an economic calendar, including an earnings calendar API and an IPOs calendar, this API is for you."
source: ""
tags: []
crawl_time: "2026-03-18T09:21:34.415Z"
metadata:
  endpoint: "https://eodhd.com/api/calendar/earnings"
  parameters:
    - {"name":"api_token","description":"Yes"}
    - {"name":"filter[symbol]","description":"Conditional"}
    - {"name":"filter[date_eq]","description":"Conditional"}
    - {"name":"filter[date_from]","description":"No"}
    - {"name":"filter[date_to]","description":"No"}
    - {"name":"page[limit]","description":"No"}
    - {"name":"page[offset]","description":"No"}
    - {"name":"fmt","description":"No"}
  markdownContent: "# Calendar API: Upcoming Dividends, Earnings, Trends, IPOs and Splits\n\nWith our Financial Calendar data feed, we provide information about upcoming earnings, IPOs, and splits. If you are looking for an economic calendar, including an earnings calendar API and an IPOs calendar, this API is for you.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/calendar/earnings?symbols=AAPL.US,MSFT.US,AI.PA&api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/calendar/earnings?from=2018-12-02&to=2018-12-06&api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/calendar/trends?symbols=AAPL.US,MSFT.US,AI.PA&api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| api_token | Yes |\n| filter[symbol] | Conditional |\n| filter[date_eq] | Conditional |\n| filter[date_from] | No |\n| filter[date_to] | No |\n| page[limit] | No |\n| page[offset] | No |\n| fmt | No |\n\n\n## Description\n\nReturns historical and upcoming earnings dates with key fields (company symbol, report date/time, and additional metadata when available). Use either a date window or a symbol list.\n\n## Request example\n\nNote: Without dates, default window – “today +7 days”.\n\n## Output Format\n\n“earnings” section:\n\n## Description\n\nReturns forward-looking and historical earnings trend points for one or more symbols. Each symbol returns a list of dated items that indicate whether that point is an estimate or an actual. The endpoint is JSON-only.\n\n## Output Format\n\nTrend item fields\n\n## Output Response Example\n\nNotes• JSON-only due to nested structure.• If a provided symbol has no data, it may be omitted from the response.• To paginate large symbol sets, split your symbols into batches (for example, 50–100 per call).\n\n## Description\n\nReturns historical and upcoming IPOs in a date window. Items may include filing/amended dates, expected or effective first trading date, price range or offer price, and share count. The response supports JSON (recommended for full field coverage).\n\n## Output Format\n\nIPO record fields\n\nNotes• Numbers may be 0 when the value is unknown or not yet set (for example before pricing).• start_date may be null for filings without a scheduled first trading date.• Use deal_type to track lifecycle changes (for example, Amended or Priced updates).\n\n## Description\n\nReturns historical and upcoming stock splits and reverse splits for selected symbols or a date window. Each item includes the effective split date and the ratio (for example 4:1).\n\n## Request Example\n\nBy symbol (with date window) as csv:\n\nAll symbols (with date window) as json:\n\n## Output Format\n\nSplit record fields\n\n## Description\n\nReturns a calendar of dividend dates filtered by symbol or by date. Supports pagination. To get dividend details navigate to our Corporate Actions: Splits and Dividends API.\n\n## Output Format\n\nDividend record fields (items inside data)\n\nNotes• At least one of filter[symbol] or filter[date_eq] must be provided.• Use page[limit] and page[offset] for large datasets.• filter[date_from] and filter[date_to] can be used together (with filter[symbol]) to narrow the range.\n\n## Code Examples\n\n```text\nhttps://eodhd.com/api/calendar/earnings\n```\n\n```json\n{\n\"type\": \"Earnings\",\n\"description\": \"Historical and upcoming Earnings\",\n\"from\": \"2018-12-02\",\n\"to\": \"2018-12-06\",\n\"earnings\": [\n{\n\"code\": \"PIGEF.US\",\n\"report_date\": \"2018-12-02\",\n\"date\": \"2018-09-30\",\n\"before_after_market\": \"AfterMarket\",\n\"currency\": \"USD\",\n\"actual\": 34.52,\n\"estimate\": 36.73,\n\"difference\": -2.21,\n\"percent\": -6.0169\n},\n{\n\"code\": \"ANTM.JK\",\n\"report_date\": \"2018-12-02\",\n\"date\": \"2018-09-30\",\n\"before_after_market\": \"AfterMarket\",\n\"currency\": \"IDR\",\n\"actual\": 11.9295,\n\"estimate\": null,\n\"difference\": 0,\n\"percent\": null\n},\n{\n\"code\": \"ITOEF.US\",\n\"report_date\": \"2018-12-02\",\n\"date\": \"2018-10-31\",\n\"before_after_market\": \"AfterMarket\",\n\"currency\": \"JPY\",\n\"actual\": 59.48,\n\"estimate\": null,\n\"difference\": 0,\n\"percent\": null\n},\n{\n\"code\": \"2910.TSE\",\n\"report_date\": \"2018-12-02\",\n\"date\": \"2018-10-31\",\n\"before_after_market\": \"AfterMarket\",\n\"currency\": \"JPY\",\n\"actual\": 15.95,\n\"estimate\": 14.68,\n\"difference\": 1.27,\n\"percent\": 8.6512\n},\n```\n\n```text\nhttps://eodhd.com/api/calendar/trends\n```\n\n```json\n{\n\"type\": \"Trends\",\n\"description\": \"Historical and upcoming earning trends\",\n\"symbols\": \"AAPL.US,MSFT.US,AI.PA\",\n\"trends\": [\n[\n{\n\"code\": \"AAPL.US\",\n\"date\": \"2026-09-30\",\n\"period\": \"+1y\",\n\"growth\": \"0.0846\",\n\"earningsEstimateAvg\": \"7.9816\",\n\"earningsEstimateLow\": \"7.1300\",\n\"earningsEstimateHigh\": \"9.0000\",\n\"earningsEstimateYearAgoEps\": \"7.3676\",\n\"earningsEstimateNumberOfAnalysts\": \"40.0000\",\n\"earningsEstimateGrowth\": \"0.0833\",\n\"revenueEstimateAvg\": \"437035017610.00\",\n\"revenueEstimateLow\": \"408100000000.00\",\n\"revenueEstimateHigh\": \"477463000000.00\",\n\"revenueEstimateYearAgoEps\": null,\n\"revenueEstimateNumberOfAnalysts\": \"41.00\",\n\"revenueEstimateGrowth\": \"0.0527\",\n\"epsTrendCurrent\": \"7.9816\",\n\"epsTrend7daysAgo\": \"7.9628\",\n\"epsTrend30daysAgo\": \"7.9665\",\n\"epsTrend60daysAgo\": \"7.8069\",\n\"epsTrend90daysAgo\": \"7.8143\",\n\"epsRevisionsUpLast7days\": \"1.0000\",\n\"epsRevisionsUpLast30days\": \"4.0000\",\n\"epsRevisionsDownLast30days\": \"2.0000\"\n},\n{\n\"code\": \"AAPL.US\",\n\"date\": \"2025-12-31\",\n\"period\": \"+1q\",\n\"growth\": \"0.0355\",\n\"earningsEstimateAvg\": \"2.4851\",\n\"earningsEstimateLow\": \"2.2900\",\n\"earningsEstimateHigh\": \"2.6700\",\n\"earningsEstimateYearAgoEps\": \"2.4000\",\n\"earningsEstimateNumberOfAnalysts\": \"23.0000\",\n\"earningsEstimateGrowth\": \"0.0355\",\n\"revenueEstimateAvg\": \"130076630320.00\",\n\"revenueEstimateLow\": \"125551070150.00\",\n\"revenueEstimateHigh\": \"137497000000.00\",\n\"revenueEstimateYearAgoEps\": null,\n\"revenueEstimateNumberOfAnalysts\": \"19.00\",\n\"revenueEstimateGrowth\": \"0.0465\",\n\"epsTrendCurrent\": \"2.4851\",\n\"epsTrend7daysAgo\": \"2.4712\",\n\"epsTrend30daysAgo\": \"2.4749\",\n\"epsTrend60daysAgo\": \"2.4228\",\n\"epsTrend90daysAgo\": \"2.4232\",\n\"epsRevisionsUpLast7days\": \"1.0000\",\n\"epsRevisionsUpLast30days\": \"2.0000\",\n\"epsRevisionsDownLast30days\": \"3.0000\"\n},\n{\n\"code\": \"AAPL.US\",\n\"date\": \"2025-09-30\",\n\"period\": \"+1q\",\n\"growth\": \"0.0135\",\n\"earningsEstimateAvg\": \"1.6556\",\n\"earningsEstimateLow\": \"1.5100\",\n\"earningsEstimateHigh\": \"1.8200\",\n\"earningsEstimateYearAgoEps\": \"0.9700\",\n\"earningsEstimateNumberOfAnalysts\": \"28.0000\",\n\"earningsEstimateGrowth\": \"0.7068\",\n\"revenueEstimateAvg\": \"97853199420.00\",\n\"revenueEstimateLow\": \"93352000000.00\",\n\"revenueEstimateHigh\": \"102366000000.00\",\n\"revenueEstimateYearAgoEps\": null,\n\"revenueEstimateNumberOfAnalysts\": \"27.00\",\n\"revenueEstimateGrowth\": \"0.0308\",\n\"epsTrendCurrent\": \"1.6556\",\n\"epsTrend7daysAgo\": \"1.6552\",\n\"epsTrend30daysAgo\": \"1.6573\",\n\"epsTrend60daysAgo\": \"1.6587\",\n\"epsTrend90daysAgo\": \"1.7167\",\n\"epsRevisionsUpLast7days\": \"3.0000\",\n\"epsRevisionsUpLast30days\": \"3.0000\",\n\"epsRevisionsDownLast30days\": \"4.0000\"\n```\n\n```text\nhttps://eodhd.com/api/calendar/ipos\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "calendar-upcoming-earnings-ipos-and-splits"
---

# Calendar API: Upcoming Dividends, Earnings, Trends, IPOs and Splits

## 源URL

https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits/

## 描述

With our Financial Calendar data feed, we provide information about upcoming earnings, IPOs, and splits. If you are looking for an economic calendar, including an earnings calendar API and an IPOs calendar, this API is for you.

## API 端点

**Endpoint**: `https://eodhd.com/api/calendar/earnings`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `api_token` | - | 否 | - | Yes |
| `filter[symbol]` | - | 否 | - | Conditional |
| `filter[date_eq]` | - | 否 | - | Conditional |
| `filter[date_from]` | - | 否 | - | No |
| `filter[date_to]` | - | 否 | - | No |
| `page[limit]` | - | 否 | - | No |
| `page[offset]` | - | 否 | - | No |
| `fmt` | - | 否 | - | No |

## 文档正文

With our Financial Calendar data feed, we provide information about upcoming earnings, IPOs, and splits. If you are looking for an economic calendar, including an earnings calendar API and an IPOs calendar, this API is for you.

## API Endpoint

```text
https://eodhd.com/api/calendar/earnings?symbols=AAPL.US,MSFT.US,AI.PA&api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/calendar/earnings?from=2018-12-02&to=2018-12-06&api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/calendar/trends?symbols=AAPL.US,MSFT.US,AI.PA&api_token={YOUR_API_TOKEN}&fmt=json
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| api_token | Yes |
| filter[symbol] | Conditional |
| filter[date_eq] | Conditional |
| filter[date_from] | No |
| filter[date_to] | No |
| page[limit] | No |
| page[offset] | No |
| fmt | No |

## Description

Returns historical and upcoming earnings dates with key fields (company symbol, report date/time, and additional metadata when available). Use either a date window or a symbol list.

## Request example

Note: Without dates, default window – “today +7 days”.

## Output Format

“earnings” section:

## Description

Returns forward-looking and historical earnings trend points for one or more symbols. Each symbol returns a list of dated items that indicate whether that point is an estimate or an actual. The endpoint is JSON-only.

## Output Format

Trend item fields

## Output Response Example

Notes• JSON-only due to nested structure.• If a provided symbol has no data, it may be omitted from the response.• To paginate large symbol sets, split your symbols into batches (for example, 50–100 per call).

## Description

Returns historical and upcoming IPOs in a date window. Items may include filing/amended dates, expected or effective first trading date, price range or offer price, and share count. The response supports JSON (recommended for full field coverage).

## Output Format

IPO record fields

Notes• Numbers may be 0 when the value is unknown or not yet set (for example before pricing).• start_date may be null for filings without a scheduled first trading date.• Use deal_type to track lifecycle changes (for example, Amended or Priced updates).

## Description

Returns historical and upcoming stock splits and reverse splits for selected symbols or a date window. Each item includes the effective split date and the ratio (for example 4:1).

## Request Example

By symbol (with date window) as csv:

All symbols (with date window) as json:

## Output Format

Split record fields

## Description

Returns a calendar of dividend dates filtered by symbol or by date. Supports pagination. To get dividend details navigate to our Corporate Actions: Splits and Dividends API.

## Output Format

Dividend record fields (items inside data)

Notes• At least one of filter[symbol] or filter[date_eq] must be provided.• Use page[limit] and page[offset] for large datasets.• filter[date_from] and filter[date_to] can be used together (with filter[symbol]) to narrow the range.

## Code Examples

```text
https://eodhd.com/api/calendar/earnings
```

```json
{
"type": "Earnings",
"description": "Historical and upcoming Earnings",
"from": "2018-12-02",
"to": "2018-12-06",
"earnings": [
{
"code": "PIGEF.US",
"report_date": "2018-12-02",
"date": "2018-09-30",
"before_after_market": "AfterMarket",
"currency": "USD",
"actual": 34.52,
"estimate": 36.73,
"difference": -2.21,
"percent": -6.0169
},
{
"code": "ANTM.JK",
"report_date": "2018-12-02",
"date": "2018-09-30",
"before_after_market": "AfterMarket",
"currency": "IDR",
"actual": 11.9295,
"estimate": null,
"difference": 0,
"percent": null
},
{
"code": "ITOEF.US",
"report_date": "2018-12-02",
"date": "2018-10-31",
"before_after_market": "AfterMarket",
"currency": "JPY",
"actual": 59.48,
"estimate": null,
"difference": 0,
"percent": null
},
{
"code": "2910.TSE",
"report_date": "2018-12-02",
"date": "2018-10-31",
"before_after_market": "AfterMarket",
"currency": "JPY",
"actual": 15.95,
"estimate": 14.68,
"difference": 1.27,
"percent": 8.6512
},
```

```text
https://eodhd.com/api/calendar/trends
```

```json
{
"type": "Trends",
"description": "Historical and upcoming earning trends",
"symbols": "AAPL.US,MSFT.US,AI.PA",
"trends": [
[
{
"code": "AAPL.US",
"date": "2026-09-30",
"period": "+1y",
"growth": "0.0846",
"earningsEstimateAvg": "7.9816",
"earningsEstimateLow": "7.1300",
"earningsEstimateHigh": "9.0000",
"earningsEstimateYearAgoEps": "7.3676",
"earningsEstimateNumberOfAnalysts": "40.0000",
"earningsEstimateGrowth": "0.0833",
"revenueEstimateAvg": "437035017610.00",
"revenueEstimateLow": "408100000000.00",
"revenueEstimateHigh": "477463000000.00",
"revenueEstimateYearAgoEps": null,
"revenueEstimateNumberOfAnalysts": "41.00",
"revenueEstimateGrowth": "0.0527",
"epsTrendCurrent": "7.9816",
"epsTrend7daysAgo": "7.9628",
"epsTrend30daysAgo": "7.9665",
"epsTrend60daysAgo": "7.8069",
"epsTrend90daysAgo": "7.8143",
"epsRevisionsUpLast7days": "1.0000",
"epsRevisionsUpLast30days": "4.0000",
"epsRevisionsDownLast30days": "2.0000"
},
{
"code": "AAPL.US",
"date": "2025-12-31",
"period": "+1q",
"growth": "0.0355",
"earningsEstimateAvg": "2.4851",
"earningsEstimateLow": "2.2900",
"earningsEstimateHigh": "2.6700",
"earningsEstimateYearAgoEps": "2.4000",
"earningsEstimateNumberOfAnalysts": "23.0000",
"earningsEstimateGrowth": "0.0355",
"revenueEstimateAvg": "130076630320.00",
"revenueEstimateLow": "125551070150.00",
"revenueEstimateHigh": "137497000000.00",
"revenueEstimateYearAgoEps": null,
"revenueEstimateNumberOfAnalysts": "19.00",
"revenueEstimateGrowth": "0.0465",
"epsTrendCurrent": "2.4851",
"epsTrend7daysAgo": "2.4712",
"epsTrend30daysAgo": "2.4749",
"epsTrend60daysAgo": "2.4228",
"epsTrend90daysAgo": "2.4232",
"epsRevisionsUpLast7days": "1.0000",
"epsRevisionsUpLast30days": "2.0000",
"epsRevisionsDownLast30days": "3.0000"
},
{
"code": "AAPL.US",
"date": "2025-09-30",
"period": "+1q",
"growth": "0.0135",
"earningsEstimateAvg": "1.6556",
"earningsEstimateLow": "1.5100",
"earningsEstimateHigh": "1.8200",
"earningsEstimateYearAgoEps": "0.9700",
"earningsEstimateNumberOfAnalysts": "28.0000",
"earningsEstimateGrowth": "0.7068",
"revenueEstimateAvg": "97853199420.00",
"revenueEstimateLow": "93352000000.00",
"revenueEstimateHigh": "102366000000.00",
"revenueEstimateYearAgoEps": null,
"revenueEstimateNumberOfAnalysts": "27.00",
"revenueEstimateGrowth": "0.0308",
"epsTrendCurrent": "1.6556",
"epsTrend7daysAgo": "1.6552",
"epsTrend30daysAgo": "1.6573",
"epsTrend60daysAgo": "1.6587",
"epsTrend90daysAgo": "1.7167",
"epsRevisionsUpLast7days": "3.0000",
"epsRevisionsUpLast30days": "3.0000",
"epsRevisionsDownLast30days": "4.0000"
```

```text
https://eodhd.com/api/calendar/ipos
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
