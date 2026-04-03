---
id: "url-74f5331"
type: "api"
title: "US Treasury (UST) Interest Rates API (beta)"
url: "https://eodhd.com/financial-apis/us-treasury-ust-interest-rates-api-beta"
description: "This API provides structured, user-friendly access to official US Treasury interest rate datasets (Treasury bills, par yield curve rates, long-term rates, and real yield curve rates). These time series are widely used for macro research, fixed-income analytics, discounting/cost of capital, yield curve modeling, and building risk-free rate baselines in trading/portfolio systems. This API includes four base endpoints: Bill Rates, Long-Term Rates, Yield Rates, Real Yield Rates."
source: ""
tags: []
crawl_time: "2026-03-18T04:41:36.542Z"
metadata:
  endpoint: "https://eodhd.com/api/ust/bill-rates"
  parameters:
    - {"name":"api_token","description":"Yes"}
    - {"name":"filter[year]","description":"No"}
  markdownContent: "# US Treasury (UST) Interest Rates API (beta)\n\nThis API provides structured, user-friendly access to official US Treasury interest rate datasets (Treasury bills, par yield curve rates, long-term rates, and real yield curve rates). These time series are widely used for macro research, fixed-income analytics, discounting/cost of capital, yield curve modeling, and building risk-free rate baselines in trading/portfolio systems. This API includes four base endpoints: Bill Rates, Long-Term Rates, Yield Rates, Real Yield Rates.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/ust/bill-rates?api_token=YOUR_TOKEN&filter[year]=2012&page[limit]=100&page[offset]=0\n```\n\n```text\nhttps://eodhd.com/api/ust/long-term-rates?api_token=YOUR_TOKEN&filter[year]=2020\n```\n\n```text\nhttps://eodhd.com/api/ust/yield-rates?api_token=YOUR_TOKEN&filter[year]=2023\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| api_token | Yes |\n| filter[year] | No |\n\n\n## Description\n\nProvides Daily Treasury Bill Rates (T-Bills): discount and coupon rates, average rates, maturity, and CUSIP.\n\n## Description\n\nLong-term Treasury rates. This feed combines “Daily Treasury Real Long-Term Rate Averages” and “Daily Treasury Long-Term Rates” into one dataset.\n\n## Description\n\nDaily Treasury Par Yield Curve Rates (nominal yield curve by tenor).\n\n## Description\n\nDaily Treasury Par Real Yield Curve Rates (real yield curve by tenor).\n\n## Code Examples\n\n```text\nhttps://eodhd.com/api/ust/bill-rates\n```\n\n```json\n{\n  \"meta\": {\n    \"total\": 120\n  },\n  \"data\": [\n    {\n      \"date\": \"2026-01-02\",\n      \"tenor\": \"4WK\",\n      \"discount\": 3.58,\n      \"coupon\": 3.64,\n      \"avg_discount\": 3.58,\n      \"avg_coupon\": 3.64,\n      \"maturity_date\": \"2026-02-03\",\n      \"cusip\": \"912797SJ7\"\n    },\n    {\n      \"date\": \"2026-01-02\",\n      \"tenor\": \"8WK\",\n      \"discount\": 3.57,\n      \"coupon\": 3.64,\n      \"avg_discount\": 3.57,\n      \"avg_coupon\": 3.64,\n      \"maturity_date\": \"2026-03-03\",\n      \"cusip\": \"912797ST5\"\n    },\n    {\n      \"date\": \"2026-01-02\",\n      \"tenor\": \"13WK\",\n      \"discount\": 3.54,\n      \"coupon\": 3.62,\n      \"avg_discount\": 3.54,\n      \"avg_coupon\": 3.62,\n      \"maturity_date\": \"2026-04-02\",\n      \"cusip\": \"912797SD0\"\n    },\n    {\n      \"date\": \"2026-01-02\",\n      \"tenor\": \"17WK\",\n      \"discount\": 3.54,\n      \"coupon\": 3.63,\n      \"avg_discount\": 3.54,\n      \"avg_coupon\": 3.63,\n      \"maturity_date\": \"2026-05-05\",\n      \"cusip\": \"912797TL1\"\n    },\n......\n```\n\n```text\nhttps://eodhd.com/api/ust/long-term-rates\n```\n\n```json\n{\n  \"meta\": {\n    \"total\": 60\n  },\n  \"data\": [\n    {\n      \"date\": \"2026-01-02\",\n      \"rate_type\": \"BC_20year\",\n      \"rate\": 4.81,\n      \"extrapolation_factor\": null\n    },\n    {\n      \"date\": \"2026-01-02\",\n      \"rate_type\": \"Over_10_Years\",\n      \"rate\": 4.78,\n      \"extrapolation_factor\": null\n    },\n    {\n      \"date\": \"2026-01-02\",\n      \"rate_type\": \"Real_Rate\",\n      \"rate\": 2.55,\n      \"extrapolation_factor\": null\n    },\n    {\n      \"date\": \"2026-01-05\",\n      \"rate_type\": \"BC_20year\",\n      \"rate\": 4.79,\n      \"extrapolation_factor\": null\n    },\n    {\n      \"date\": \"2026-01-05\",\n      \"rate_type\": \"Over_10_Years\",\n      \"rate\": 4.76,\n      \"extrapolation_factor\": null\n    },\n    {\n      \"date\": \"2026-01-05\",\n      \"rate_type\": \"Real_Rate\",\n      \"rate\": 2.53,\n      \"extrapolation_factor\": null\n.......\n```\n\n```text\nhttps://eodhd.com/api/ust/yield-rates\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "us-treasury-ust-interest-rates-api-beta"
---

# US Treasury (UST) Interest Rates API (beta)

## 源URL

https://eodhd.com/financial-apis/us-treasury-ust-interest-rates-api-beta

## 描述

This API provides structured, user-friendly access to official US Treasury interest rate datasets (Treasury bills, par yield curve rates, long-term rates, and real yield curve rates). These time series are widely used for macro research, fixed-income analytics, discounting/cost of capital, yield curve modeling, and building risk-free rate baselines in trading/portfolio systems. This API includes four base endpoints: Bill Rates, Long-Term Rates, Yield Rates, Real Yield Rates.

## API 端点

**Endpoint**: `https://eodhd.com/api/ust/bill-rates`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `api_token` | - | 否 | - | Yes |
| `filter[year]` | - | 否 | - | No |

## 文档正文

This API provides structured, user-friendly access to official US Treasury interest rate datasets (Treasury bills, par yield curve rates, long-term rates, and real yield curve rates). These time series are widely used for macro research, fixed-income analytics, discounting/cost of capital, yield curve modeling, and building risk-free rate baselines in trading/portfolio systems. This API includes four base endpoints: Bill Rates, Long-Term Rates, Yield Rates, Real Yield Rates.

## API Endpoint

```text
https://eodhd.com/api/ust/bill-rates?api_token=YOUR_TOKEN&filter[year]=2012&page[limit]=100&page[offset]=0
```

```text
https://eodhd.com/api/ust/long-term-rates?api_token=YOUR_TOKEN&filter[year]=2020
```

```text
https://eodhd.com/api/ust/yield-rates?api_token=YOUR_TOKEN&filter[year]=2023
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| api_token | Yes |
| filter[year] | No |

## Description

Provides Daily Treasury Bill Rates (T-Bills): discount and coupon rates, average rates, maturity, and CUSIP.

## Description

Long-term Treasury rates. This feed combines “Daily Treasury Real Long-Term Rate Averages” and “Daily Treasury Long-Term Rates” into one dataset.

## Description

Daily Treasury Par Yield Curve Rates (nominal yield curve by tenor).

## Description

Daily Treasury Par Real Yield Curve Rates (real yield curve by tenor).

## Code Examples

```text
https://eodhd.com/api/ust/bill-rates
```

```json
{
  "meta": {
    "total": 120
  },
  "data": [
    {
      "date": "2026-01-02",
      "tenor": "4WK",
      "discount": 3.58,
      "coupon": 3.64,
      "avg_discount": 3.58,
      "avg_coupon": 3.64,
      "maturity_date": "2026-02-03",
      "cusip": "912797SJ7"
    },
    {
      "date": "2026-01-02",
      "tenor": "8WK",
      "discount": 3.57,
      "coupon": 3.64,
      "avg_discount": 3.57,
      "avg_coupon": 3.64,
      "maturity_date": "2026-03-03",
      "cusip": "912797ST5"
    },
    {
      "date": "2026-01-02",
      "tenor": "13WK",
      "discount": 3.54,
      "coupon": 3.62,
      "avg_discount": 3.54,
      "avg_coupon": 3.62,
      "maturity_date": "2026-04-02",
      "cusip": "912797SD0"
    },
    {
      "date": "2026-01-02",
      "tenor": "17WK",
      "discount": 3.54,
      "coupon": 3.63,
      "avg_discount": 3.54,
      "avg_coupon": 3.63,
      "maturity_date": "2026-05-05",
      "cusip": "912797TL1"
    },
......
```

```text
https://eodhd.com/api/ust/long-term-rates
```

```json
{
  "meta": {
    "total": 60
  },
  "data": [
    {
      "date": "2026-01-02",
      "rate_type": "BC_20year",
      "rate": 4.81,
      "extrapolation_factor": null
    },
    {
      "date": "2026-01-02",
      "rate_type": "Over_10_Years",
      "rate": 4.78,
      "extrapolation_factor": null
    },
    {
      "date": "2026-01-02",
      "rate_type": "Real_Rate",
      "rate": 2.55,
      "extrapolation_factor": null
    },
    {
      "date": "2026-01-05",
      "rate_type": "BC_20year",
      "rate": 4.79,
      "extrapolation_factor": null
    },
    {
      "date": "2026-01-05",
      "rate_type": "Over_10_Years",
      "rate": 4.76,
      "extrapolation_factor": null
    },
    {
      "date": "2026-01-05",
      "rate_type": "Real_Rate",
      "rate": 2.53,
      "extrapolation_factor": null
.......
```

```text
https://eodhd.com/api/ust/yield-rates
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
