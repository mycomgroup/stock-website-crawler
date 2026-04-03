---
id: "url-5fed60e6"
type: "api"
title: "Exchanges API: Get List of Supported Exchanges"
url: "https://eodhd.com/financial-apis/exchanges-api-list-of-tickers-and-trading-hours/"
description: "Two endpoints of the Exchanges API give you a list of over 60 global financial exchanges, covered by EODHD and their listed assets. It includes metadata such as exchange codes, countries, operating MICs, and supported currencies."
source: ""
tags: []
crawl_time: "2026-03-18T12:07:05.620Z"
metadata:
  endpoint: "https://eodhd.com/api/exchanges-list/"
  parameters:
    - {"name":"Country","description":"Country of listing"}
    - {"name":"Exchange","description":"Exchange code"}
    - {"name":"Currency","description":"Trading currency"}
    - {"name":"Type","description":"Type of asset (e.g. Common Stock, ETF, Fund)"}
    - {"name":"Isin","description":"International Securities Identification Number (if available)"}
  markdownContent: "# Exchanges API: Get List of Supported Exchanges\n\nTwo endpoints of the Exchanges API give you a list of over 60 global financial exchanges, covered by EODHD and their listed assets. It includes metadata such as exchange codes, countries, operating MICs, and supported currencies.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/exchanges-list/?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/exchange-symbol-list/{EXCHANGE_CODE}?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| Country | Country of listing |\n| Exchange | Exchange code |\n| Currency | Trading currency |\n| Type | Type of asset (e.g. Common Stock, ETF, Fund) |\n| Isin | International Securities Identification Number (if available) |\n\n\n## Get List of Exchanges API\n\nUse this endpoint to retrieve the full list of supported stock exchanges along with basic metadata.Endpoint:\n\nThis endpoint has no parameters. It returns a JSON array of exchanges.\n\n## Example Response (Exchange List)\n\nNote: The API returns not only stock exchanges but also several other asset classes available via EODHD endpoints:\n\n## Get List of Tickers (Exchange Symbols) API\n\nUse this endpoint to get all currently active tickers listed on a specific exchange.\n\nReplace {EXCHANGE_CODE} with values like US, LSE, XETRA, etc.\n\nBy default, only tickers that have been active in the past month are included.\n\n## Parameters\n\nNote: For US stocks, use the unified exchange code ‘US‘ which includes NYSE, NASDAQ, NYSE ARCA, and OTC markets. Or use separate codes for US exchanges: ‘NYSE’, ‘NASDAQ’, ‘BATS’, ‘OTCQB’, ‘PINK’, ‘OTCQX’, ‘OTCMKTS’, ‘NMFQS’, ‘NYSE MKT’,’OTCBB’, ‘OTCGREY’, ‘BATS’, ‘OTC’.\n\n## Example Response (Snippet for Ticker List for WAR exchange)\n\nNote: You can also get the full list of supported tickers on our Site.\n\nWe recommend to check our Exchange Trading Hours and Holidays API as well.\n\n## Code Examples\n\n```json\n{\n\"Name\": \"USAStocks\",\n\"Code\": \"US\",\n\"OperatingMIC\": \"XNAS,XNYS\",\n\"Country\": \"USA\",\n\"Currency\": \"USD\",\n\"CountryISO2\": \"US\",\n\"CountryISO3\": \"USA\"\n},\n{\n\"Name\": \"LondonExchange\",\n\"Code\": \"LSE\",\n\"OperatingMIC\": \"XLON\",\n\"Country\": \"UK\",\n\"Currency\": \"GBP\",\n\"CountryISO2\": \"GB\",\n\"CountryISO3\": \"GBR\"\n}\n```\n\n```json\n{\n\"Code\": \"CDR\",\n\"Name\": \"CD PROJEKT SA\",\n\"Country\": \"Poland\",\n\"Exchange\": \"WAR\",\n\"Currency\": \"PLN\",\n\"Type\": \"Common Stock\",\n\"Isin\": \"PLOPTTC00011\"\n},\n{\n\"Code\": \"PKN\",\n\"Name\": \"PKN Orlen SA\",\n\"Country\": \"Poland\",\n\"Exchange\": \"WAR\",\n\"Currency\": \"PLN\",\n\"Type\": \"Common Stock\",\n\"Isin\": \"PLPKN0000018\"\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "exchanges-api-list-of-tickers-and-trading-hours"
---

# Exchanges API: Get List of Supported Exchanges

## 源URL

https://eodhd.com/financial-apis/exchanges-api-list-of-tickers-and-trading-hours/

## 描述

Two endpoints of the Exchanges API give you a list of over 60 global financial exchanges, covered by EODHD and their listed assets. It includes metadata such as exchange codes, countries, operating MICs, and supported currencies.

## API 端点

**Endpoint**: `https://eodhd.com/api/exchanges-list/`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Country` | - | 否 | - | Country of listing |
| `Exchange` | - | 否 | - | Exchange code |
| `Currency` | - | 否 | - | Trading currency |
| `Type` | - | 否 | - | Type of asset (e.g. Common Stock, ETF, Fund) |
| `Isin` | - | 否 | - | International Securities Identification Number (if available) |

## 文档正文

Two endpoints of the Exchanges API give you a list of over 60 global financial exchanges, covered by EODHD and their listed assets. It includes metadata such as exchange codes, countries, operating MICs, and supported currencies.

## API Endpoint

```text
https://eodhd.com/api/exchanges-list/?api_token={YOUR_API_TOKEN}&fmt=json
```

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

## Get List of Exchanges API

Use this endpoint to retrieve the full list of supported stock exchanges along with basic metadata.Endpoint:

This endpoint has no parameters. It returns a JSON array of exchanges.

## Example Response (Exchange List)

Note: The API returns not only stock exchanges but also several other asset classes available via EODHD endpoints:

## Get List of Tickers (Exchange Symbols) API

Use this endpoint to get all currently active tickers listed on a specific exchange.

Replace {EXCHANGE_CODE} with values like US, LSE, XETRA, etc.

By default, only tickers that have been active in the past month are included.

## Parameters

Note: For US stocks, use the unified exchange code ‘US‘ which includes NYSE, NASDAQ, NYSE ARCA, and OTC markets. Or use separate codes for US exchanges: ‘NYSE’, ‘NASDAQ’, ‘BATS’, ‘OTCQB’, ‘PINK’, ‘OTCQX’, ‘OTCMKTS’, ‘NMFQS’, ‘NYSE MKT’,’OTCBB’, ‘OTCGREY’, ‘BATS’, ‘OTC’.

## Example Response (Snippet for Ticker List for WAR exchange)

Note: You can also get the full list of supported tickers on our Site.

We recommend to check our Exchange Trading Hours and Holidays API as well.

## Code Examples

```json
{
"Name": "USAStocks",
"Code": "US",
"OperatingMIC": "XNAS,XNYS",
"Country": "USA",
"Currency": "USD",
"CountryISO2": "US",
"CountryISO3": "USA"
},
{
"Name": "LondonExchange",
"Code": "LSE",
"OperatingMIC": "XLON",
"Country": "UK",
"Currency": "GBP",
"CountryISO2": "GB",
"CountryISO3": "GBR"
}
```

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
