---
id: "url-616b2f0c"
type: "api"
title: "ID Mapping API: CUSIP / ISIN / FIGI / LEI / CIK ↔ Symbol"
url: "https://eodhd.com/financial-apis/id-mapping-api-cusip-isin-figi-lei-cik-↔-symbol"
description: "The ID Mapping API lets you resolve common identifiers (CUSIP, ISIN, OpenFIGI, LEI, CIK) to a tradable symbol (e.g. AAPL) and vice-versa using flexible filters. It’s ideal for onboarding portfolios, normalizing vendor feeds, or building “search-and-resolve” experiences."
source: ""
tags: []
crawl_time: "2026-03-18T12:04:25.401Z"
metadata:
  endpoint: "https://eodhd.com/api/id-mapping"
  parameters:
    - {"name":"filter[symbol]","description":"Yes (if no other filter provided)"}
    - {"name":"filter[ex]","description":"Yes (if no other filter provided)"}
    - {"name":"filter[isin]","description":"Yes (if no other filter provided)"}
    - {"name":"filter[figi]","description":"Yes (if no other filter provided)"}
    - {"name":"filter[lei]","description":"Yes (if no other filter provided)"}
    - {"name":"filter[cusip]","description":"Yes (if no other filter provided)"}
    - {"name":"filter[cik]","description":"Yes (if no other filter provided)"}
    - {"name":"page[limit]","description":"No"}
    - {"name":"page[offset]","description":"No"}
    - {"name":"api_token","description":"Yes"}
  markdownContent: "# ID Mapping API: CUSIP / ISIN / FIGI / LEI / CIK ↔ Symbol\n\nThe ID Mapping API lets you resolve common identifiers (CUSIP, ISIN, OpenFIGI, LEI, CIK) to a tradable symbol (e.g. AAPL) and vice-versa using flexible filters. It’s ideal for onboarding portfolios, normalizing vendor feeds, or building “search-and-resolve” experiences.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/id-mapping?filter[symbol]=AAPL.US&page[limit]=100&page[offset]=0&api_token=YOUR_API_TOKEN&fmt=json\n```\n\n```text\nhttps://eodhd.com/api/id-mapping?filter[isin]=US0378331005&api_token=YOUR_API_TOKEN\n```\n\n```text\nhttps://eodhd.com/api/id-mapping?filter[ex]=US&page[limit]=50&api_token=YOUR_API_TOKEN\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| filter[symbol] | Yes (if no other filter provided) |\n| filter[ex] | Yes (if no other filter provided) |\n| filter[isin] | Yes (if no other filter provided) |\n| filter[figi] | Yes (if no other filter provided) |\n| filter[lei] | Yes (if no other filter provided) |\n| filter[cusip] | Yes (if no other filter provided) |\n| filter[cik] | Yes (if no other filter provided) |\n| page[limit] | No |\n| page[offset] | No |\n| api_token | Yes |\n\n\n## Description\n\nRetrieve common identifiers for a symbol or by a specific identifier. Supports CUSIP, ISIN, OpenFigi, LEI, and CIK. At least one filter value is required.\n\n## Output Format (JSON)\n\nThe response includes meta for pagination, a data array of mapping objects, and links for pagination.\n\n## Additional Examples\n\nLooking by exchange code:\n\nUse our Search API to locate assets filtering by asset category, exchange or ticker name.\n\n## Code Examples\n\n```text\nGET https://eodhd.com/api/id-mapping\n```\n\n```json\n{\n  \"meta\": {\n    \"total\": 1,\n    \"limit\": 100,\n    \"offset\": 0\n  },\n  \"data\": [\n    {\n      \"symbol\": \"AAPL.US\",\n      \"isin\": \"US0378331005\",\n      \"figi\": \"BBG000B9XRY4\",\n      \"lei\": \"HWUPKR0MPOU8FGXBT394\",\n      \"cusip\": \"037833100\",\n      \"cik\": \"0000320193\"\n    }\n  ],\n  \"links\": {\n    \"next\": null\n  }\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "id-mapping-api-cusip-isin-figi-lei-cik-%E2%86%94-symbol"
---

# ID Mapping API: CUSIP / ISIN / FIGI / LEI / CIK ↔ Symbol

## 源URL

https://eodhd.com/financial-apis/id-mapping-api-cusip-isin-figi-lei-cik-↔-symbol

## 描述

The ID Mapping API lets you resolve common identifiers (CUSIP, ISIN, OpenFIGI, LEI, CIK) to a tradable symbol (e.g. AAPL) and vice-versa using flexible filters. It’s ideal for onboarding portfolios, normalizing vendor feeds, or building “search-and-resolve” experiences.

## API 端点

**Endpoint**: `https://eodhd.com/api/id-mapping`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `filter[symbol]` | - | 否 | - | Yes (if no other filter provided) |
| `filter[ex]` | - | 否 | - | Yes (if no other filter provided) |
| `filter[isin]` | - | 否 | - | Yes (if no other filter provided) |
| `filter[figi]` | - | 否 | - | Yes (if no other filter provided) |
| `filter[lei]` | - | 否 | - | Yes (if no other filter provided) |
| `filter[cusip]` | - | 否 | - | Yes (if no other filter provided) |
| `filter[cik]` | - | 否 | - | Yes (if no other filter provided) |
| `page[limit]` | - | 否 | - | No |
| `page[offset]` | - | 否 | - | No |
| `api_token` | - | 否 | - | Yes |

## 文档正文

The ID Mapping API lets you resolve common identifiers (CUSIP, ISIN, OpenFIGI, LEI, CIK) to a tradable symbol (e.g. AAPL) and vice-versa using flexible filters. It’s ideal for onboarding portfolios, normalizing vendor feeds, or building “search-and-resolve” experiences.

## API Endpoint

```text
https://eodhd.com/api/id-mapping?filter[symbol]=AAPL.US&page[limit]=100&page[offset]=0&api_token=YOUR_API_TOKEN&fmt=json
```

```text
https://eodhd.com/api/id-mapping?filter[isin]=US0378331005&api_token=YOUR_API_TOKEN
```

```text
https://eodhd.com/api/id-mapping?filter[ex]=US&page[limit]=50&api_token=YOUR_API_TOKEN
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| filter[symbol] | Yes (if no other filter provided) |
| filter[ex] | Yes (if no other filter provided) |
| filter[isin] | Yes (if no other filter provided) |
| filter[figi] | Yes (if no other filter provided) |
| filter[lei] | Yes (if no other filter provided) |
| filter[cusip] | Yes (if no other filter provided) |
| filter[cik] | Yes (if no other filter provided) |
| page[limit] | No |
| page[offset] | No |
| api_token | Yes |

## Description

Retrieve common identifiers for a symbol or by a specific identifier. Supports CUSIP, ISIN, OpenFigi, LEI, and CIK. At least one filter value is required.

## Output Format (JSON)

The response includes meta for pagination, a data array of mapping objects, and links for pagination.

## Additional Examples

Looking by exchange code:

Use our Search API to locate assets filtering by asset category, exchange or ticker name.

## Code Examples

```text
GET https://eodhd.com/api/id-mapping
```

```json
{
  "meta": {
    "total": 1,
    "limit": 100,
    "offset": 0
  },
  "data": [
    {
      "symbol": "AAPL.US",
      "isin": "US0378331005",
      "figi": "BBG000B9XRY4",
      "lei": "HWUPKR0MPOU8FGXBT394",
      "cusip": "037833100",
      "cik": "0000320193"
    }
  ],
  "links": {
    "next": null
  }
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
