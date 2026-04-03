---
id: "url-31795c02"
type: "api"
title: "List of Supported Tickers: API for All Asset Classes"
url: "https://eodhd.com/financial-apis/covered-tickers-eodhd"
description: "Use this endpoint to retrieve all currently active tickers covered by EODHD, grouped by asset type:"
source: ""
tags: []
crawl_time: "2026-03-18T03:05:11.389Z"
metadata:
  endpoint: "https://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}"
  parameters:
    - {"name":"Country","description":"Country of listing"}
    - {"name":"Exchange","description":"Exchange code"}
    - {"name":"Currency","description":"Trading currency"}
    - {"name":"Type","description":"Type of asset (e.g. Common Stock, ETF, Fund)"}
    - {"name":"Isin","description":"International Securities Identification Number (if available)"}
  markdownContent: "# List of Supported Tickers: API for All Asset Classes\n\nUse this endpoint to retrieve all currently active tickers covered by EODHD, grouped by asset type:\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| Country | Country of listing |\n| Exchange | Exchange code |\n| Currency | Trading currency |\n| Type | Type of asset (e.g. Common Stock, ETF, Fund) |\n| Isin | International Securities Identification Number (if available) |\n\n\n## Get List of Tickers by Asset Category\n\nUse this endpoint to retrieve all currently active tickers covered by EODHD, grouped by asset type:\n\nReplace {EXCHANGE_CODE} with values like US, LSE, CC, FOREX, GBOND etc.\n\nBy default, only tickers that have been active in the past month are included.\n\n## Parameters\n\nNote: For US stocks, use the unified exchange code ‘US‘ which includes NYSE, NASDAQ, NYSE ARCA, and OTC markets. Or use separate codes for US exchanges: ‘NYSE’, ‘NASDAQ’, ‘BATS’, ‘OTCQB’, ‘PINK’, ‘OTCQX’, ‘OTCMKTS’, ‘NMFQS’, ‘NYSE MKT’,’OTCBB’, ‘OTCGREY’, ‘BATS’, ‘OTC’.\n\n## Example Response (Snippet for Ticker List for WAR exchange)\n\nNote: You can also get the full list of supported tickers on our Site.\n\n## Code Examples\n\n```json\n{\n\"Code\": \"CDR\",\n\"Name\": \"CD PROJEKT SA\",\n\"Country\": \"Poland\",\n\"Exchange\": \"WAR\",\n\"Currency\": \"PLN\",\n\"Type\": \"Common Stock\",\n\"Isin\": \"PLOPTTC00011\"\n},\n{\n\"Code\": \"PKN\",\n\"Name\": \"PKN Orlen SA\",\n\"Country\": \"Poland\",\n\"Exchange\": \"WAR\",\n\"Currency\": \"PLN\",\n\"Type\": \"Common Stock\",\n\"Isin\": \"PLPKN0000018\"\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "covered-tickers-eodhd"
---

# List of Supported Tickers: API for All Asset Classes

## 源URL

https://eodhd.com/financial-apis/covered-tickers-eodhd

## 描述

Use this endpoint to retrieve all currently active tickers covered by EODHD, grouped by asset type:

## API 端点

**Endpoint**: `https://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Country` | - | 否 | - | Country of listing |
| `Exchange` | - | 否 | - | Exchange code |
| `Currency` | - | 否 | - | Trading currency |
| `Type` | - | 否 | - | Type of asset (e.g. Common Stock, ETF, Fund) |
| `Isin` | - | 否 | - | International Securities Identification Number (if available) |

## 文档正文

Use this endpoint to retrieve all currently active tickers covered by EODHD, grouped by asset type:

## API Endpoint

```text
https://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}?api_token={YOUR_API_TOKEN}&fmt=json
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| Country | Country of listing |
| Exchange | Exchange code |
| Currency | Trading currency |
| Type | Type of asset (e.g. Common Stock, ETF, Fund) |
| Isin | International Securities Identification Number (if available) |

## Get List of Tickers by Asset Category

Use this endpoint to retrieve all currently active tickers covered by EODHD, grouped by asset type:

Replace {EXCHANGE_CODE} with values like US, LSE, CC, FOREX, GBOND etc.

By default, only tickers that have been active in the past month are included.

## Parameters

Note: For US stocks, use the unified exchange code ‘US‘ which includes NYSE, NASDAQ, NYSE ARCA, and OTC markets. Or use separate codes for US exchanges: ‘NYSE’, ‘NASDAQ’, ‘BATS’, ‘OTCQB’, ‘PINK’, ‘OTCQX’, ‘OTCMKTS’, ‘NMFQS’, ‘NYSE MKT’,’OTCBB’, ‘OTCGREY’, ‘BATS’, ‘OTC’.

## Example Response (Snippet for Ticker List for WAR exchange)

Note: You can also get the full list of supported tickers on our Site.

## Code Examples

```json
{
"Code": "CDR",
"Name": "CD PROJEKT SA",
"Country": "Poland",
"Exchange": "WAR",
"Currency": "PLN",
"Type": "Common Stock",
"Isin": "PLOPTTC00011"
},
{
"Code": "PKN",
"Name": "PKN Orlen SA",
"Country": "Poland",
"Exchange": "WAR",
"Currency": "PLN",
"Type": "Common Stock",
"Isin": "PLPKN0000018"
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
