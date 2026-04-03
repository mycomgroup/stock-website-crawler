---
id: "url-445821d5"
type: "api"
title: "Search API for Stocks, ETFs, Mutual Funds, and Indices"
url: "https://eodhd.com/financial-apis/search-api-for-stocks-etfs-mutual-funds"
description: "The Search API allows you to quickly locate assets such as stocks, ETFs, mutual funds, bonds, and indices by using a flexible query engine. You can search by ticker code, company name, or ISIN. This API is particularly useful for applications requiring user-friendly asset lookups or autocomplete suggestions."
source: ""
tags: []
crawl_time: "2026-03-18T04:41:24.416Z"
metadata:
  endpoint: "https://eodhd.com/api/search/{query_string}"
  parameters:
    - {"name":"Type","description":"Type of asset (e.g., Common Stock, ETF, Fund, Bond)"}
    - {"name":"Country","description":"Country of the exchange"}
    - {"name":"Currency","description":"Currency in which the asset is traded"}
    - {"name":"ISIN","description":"ISIN code, if available"}
    - {"name":"previousClose","description":"Previous closing price"}
    - {"name":"previousCloseDate","description":"Date of the previous close price"}
    - {"name":"isPrimary","description":"True if this is the primary exchange for the asset, otherwise false"}
  markdownContent: "# Search API for Stocks, ETFs, Mutual Funds, and Indices\n\nThe Search API allows you to quickly locate assets such as stocks, ETFs, mutual funds, bonds, and indices by using a flexible query engine. You can search by ticker code, company name, or ISIN. This API is particularly useful for applications requiring user-friendly asset lookups or autocomplete suggestions.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/search/{query_string}?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/search/AAPL?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/search/Apple Inc?api_token={YOUR_API_TOKEN}&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| Type | Type of asset (e.g., Common Stock, ETF, Fund, Bond) |\n| Country | Country of the exchange |\n| Currency | Currency in which the asset is traded |\n| ISIN | ISIN code, if available |\n| previousClose | Previous closing price |\n| previousCloseDate | Date of the previous close price |\n| isPrimary | True if this is the primary exchange for the asset, otherwise false |\n\n\n## API Endpoint\n\nTo search for financial instruments, use the following endpoint:\n\n## Parameters\n\nNote: The demo API key does not work for the Search API. Please register to get your free API token.Note: The API makes a search among active tickers only.\n\n## Response Fields\n\nThe response is returned in JSON format as a list of matching instruments.\n\n## Examples\n\nSearch by ticker code:\n\nSearch by company name:\n\nSearch with a limit of 1 result:\n\n## Code Examples\n\n```json\n{\n\"Code\": \"AAPL\",\n\"Exchange\": \"US\",\n\"Name\": \"Apple Inc\",\n\"Type\": \"Common Stock\",\n\"Country\": \"USA\",\n\"Currency\": \"USD\",\n\"ISIN\": \"US0378331005\",\n\"previousClose\": 229.65,\n\"previousCloseDate\": \"2025-08-12\",\n\"isPrimary\": true\n},\n{\n\"Code\": \"AAPL\",\n\"Exchange\": \"TO\",\n\"Name\": \"Apple CDR (CAD Hedged)\",\n\"Type\": \"Common Stock\",\n\"Country\": \"Canada\",\n\"Currency\": \"CAD\",\n\"ISIN\": null,\n\"previousClose\": 33.14,\n\"previousCloseDate\": \"2025-08-12\",\n\"isPrimary\": false\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "search-api-for-stocks-etfs-mutual-funds"
---

# Search API for Stocks, ETFs, Mutual Funds, and Indices

## 源URL

https://eodhd.com/financial-apis/search-api-for-stocks-etfs-mutual-funds

## 描述

The Search API allows you to quickly locate assets such as stocks, ETFs, mutual funds, bonds, and indices by using a flexible query engine. You can search by ticker code, company name, or ISIN. This API is particularly useful for applications requiring user-friendly asset lookups or autocomplete suggestions.

## API 端点

**Endpoint**: `https://eodhd.com/api/search/{query_string}`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Type` | - | 否 | - | Type of asset (e.g., Common Stock, ETF, Fund, Bond) |
| `Country` | - | 否 | - | Country of the exchange |
| `Currency` | - | 否 | - | Currency in which the asset is traded |
| `ISIN` | - | 否 | - | ISIN code, if available |
| `previousClose` | - | 否 | - | Previous closing price |
| `previousCloseDate` | - | 否 | - | Date of the previous close price |
| `isPrimary` | - | 否 | - | True if this is the primary exchange for the asset, otherwise false |

## 文档正文

The Search API allows you to quickly locate assets such as stocks, ETFs, mutual funds, bonds, and indices by using a flexible query engine. You can search by ticker code, company name, or ISIN. This API is particularly useful for applications requiring user-friendly asset lookups or autocomplete suggestions.

## API Endpoint

```text
https://eodhd.com/api/search/{query_string}?api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/search/AAPL?api_token={YOUR_API_TOKEN}&fmt=json
```

```text
https://eodhd.com/api/search/Apple Inc?api_token={YOUR_API_TOKEN}&fmt=json
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| Type | Type of asset (e.g., Common Stock, ETF, Fund, Bond) |
| Country | Country of the exchange |
| Currency | Currency in which the asset is traded |
| ISIN | ISIN code, if available |
| previousClose | Previous closing price |
| previousCloseDate | Date of the previous close price |
| isPrimary | True if this is the primary exchange for the asset, otherwise false |

## API Endpoint

To search for financial instruments, use the following endpoint:

## Parameters

Note: The demo API key does not work for the Search API. Please register to get your free API token.Note: The API makes a search among active tickers only.

## Response Fields

The response is returned in JSON format as a list of matching instruments.

## Examples

Search by ticker code:

Search by company name:

Search with a limit of 1 result:

## Code Examples

```json
{
"Code": "AAPL",
"Exchange": "US",
"Name": "Apple Inc",
"Type": "Common Stock",
"Country": "USA",
"Currency": "USD",
"ISIN": "US0378331005",
"previousClose": 229.65,
"previousCloseDate": "2025-08-12",
"isPrimary": true
},
{
"Code": "AAPL",
"Exchange": "TO",
"Name": "Apple CDR (CAD Hedged)",
"Type": "Common Stock",
"Country": "Canada",
"Currency": "CAD",
"ISIN": null,
"previousClose": 33.14,
"previousCloseDate": "2025-08-12",
"isPrimary": false
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
