---
id: "url-245ced19"
type: "api"
title: "Intraday Historical Stock Price Data API"
url: "https://eodhd.com/financial-apis/intraday-historical-data-api/"
description: "Intraday data refers to stock price movements and market activity captured within the trading day, often at minute-by-minute or hourly intervals. Intraday historical data allows you to track these fluctuations in great detail, offering insights into market trends, trading volume, and price changes over shorter time frames. This is particularly valuable for day traders, algorithmic traders, and financial analysts who need to make fast, data-driven decisions based on short-term trends."
source: ""
tags: []
crawl_time: "2026-03-18T04:23:46.054Z"
metadata:
  endpoint: "https://eodhd.com/api/intraday/AAPL.US"
  parameters:
    - {"name":"datetime (or “date / time separately”)","description":"Timestamp of the data (UTC)*"}
  markdownContent: "# Intraday Historical Stock Price Data API\n\nIntraday data refers to stock price movements and market activity captured within the trading day, often at minute-by-minute or hourly intervals. Intraday historical data allows you to track these fluctuations in great detail, offering insights into market trends, trading volume, and price changes over shorter time frames. This is particularly valuable for day traders, algorithmic traders, and financial analysts who need to make fast, data-driven decisions based on short-term trends.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=json&from=1627896900&to=1630575300\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| datetime (or “date / time separately”) | Timestamp of the data (UTC)* |\n\n\n## Time Range Limitations\n\nNote: If no “from/to” is specified, the default is last 120 days.\n\n## Intraday API Endpoint\n\nTo access intraday historical stock prices, use the following endpoint:\n\n## Parameters\n\n* For/to example: “from=1627896900&to=1630575300” corresponds to “2021-08-02 09:35:00” and “2021-09-02 09:35:00”\n\n## Response Fields\n\nNote: all data is provided in UTC timezone. Timestamps are in Unix format.\n\nResponse example:\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "intraday-historical-data-api"
---

# Intraday Historical Stock Price Data API

## 源URL

https://eodhd.com/financial-apis/intraday-historical-data-api/

## 描述

Intraday data refers to stock price movements and market activity captured within the trading day, often at minute-by-minute or hourly intervals. Intraday historical data allows you to track these fluctuations in great detail, offering insights into market trends, trading volume, and price changes over shorter time frames. This is particularly valuable for day traders, algorithmic traders, and financial analysts who need to make fast, data-driven decisions based on short-term trends.

## API 端点

**Endpoint**: `https://eodhd.com/api/intraday/AAPL.US`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `datetime (or “date / time separately”)` | - | 否 | - | Timestamp of the data (UTC)* |

## 文档正文

Intraday data refers to stock price movements and market activity captured within the trading day, often at minute-by-minute or hourly intervals. Intraday historical data allows you to track these fluctuations in great detail, offering insights into market trends, trading volume, and price changes over shorter time frames. This is particularly valuable for day traders, algorithmic traders, and financial analysts who need to make fast, data-driven decisions based on short-term trends.

## API Endpoint

```text
https://eodhd.com/api/intraday/AAPL.US?api_token=demo&fmt=json&from=1627896900&to=1630575300
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| datetime (or “date / time separately”) | Timestamp of the data (UTC)* |

## Time Range Limitations

Note: If no “from/to” is specified, the default is last 120 days.

## Intraday API Endpoint

To access intraday historical stock prices, use the following endpoint:

## Parameters

* For/to example: “from=1627896900&to=1630575300” corresponds to “2021-08-02 09:35:00” and “2021-09-02 09:35:00”

## Response Fields

Note: all data is provided in UTC timezone. Timestamps are in Unix format.

Response example:

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
