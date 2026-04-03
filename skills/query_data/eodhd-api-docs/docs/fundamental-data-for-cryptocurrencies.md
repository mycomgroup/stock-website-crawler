---
id: "url-4efb702e"
type: "api"
title: "Fundamental Data: Cryptocurrencies"
url: "https://eodhd.com/financial-apis/fundamental-data-for-cryptocurrencies"
description: "We provide a unified, structured, and expanded fundamental dataset for major cryptocurrencies.This dataset includes supply metrics, market capitalization, all-time levels, technical resources, project metadata, community links, and more. All responses follow a consistent JSON schema across all crypto assets."
source: ""
tags: []
crawl_time: "2026-03-18T04:39:41.774Z"
metadata:
  endpoint: "https://eodhd.com/api/fundamentals/BTC-USD.CC"
  parameters:
    - {"name":"Type","description":"string"}
    - {"name":"Category","description":"string"}
    - {"name":"WebURL","description":"string"}
    - {"name":"Description","description":"string"}
  markdownContent: "# Fundamental Data: Cryptocurrencies\n\nWe provide a unified, structured, and expanded fundamental dataset for major cryptocurrencies.This dataset includes supply metrics, market capitalization, all-time levels, technical resources, project metadata, community links, and more. All responses follow a consistent JSON schema across all crypto assets.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| Type | string |\n| Category | string |\n| WebURL | string |\n| Description | string |\n\n\n## Overview\n\nThe EODHD Cryptocurrency Fundamentals API provides point-in-time, project-level metadata and supply metrics for major cryptocurrencies.Data includes:\n\nThis feeds use the unified .CC virtual crypto exchange, enabling consistent access across all symbols.\n\n## Output fields\n\nArray of known developers, founders, maintainers.\n\nMultiple categories of resource URLs.\n\n## Code Examples\n\n```text\nhttps://eodhd.com/api/fundamentals/{SYMBOL}.CC\n```\n\n```json\n{\n  \"General\": {\n    \"Name\": \"Bitcoin\",\n    \"Type\": \"Crypto\",\n    \"Category\": \"coin\",\n    \"WebURL\": \"https://bitcoin.org/\",\n    \"Description\": \"Bitcoin is a cryptocurrency and worldwide payment system. It is the first decentralized digital currency, as the system works without a central bank or single administrator.\"\n  },\n  \"Tech\": {\n    \"Developers\": {\n      \"0\": \"Satoshi Nakamoto - Founder\",\n      \"1\": \"Wladimir J. van der Laan - Blockchain Developer\",\n      \"2\": \"Jonas Schnelli - Blockchain Developer\",\n      \"3\": \"Marco Falke - Blockchain Developer\"\n    }\n  },\n  \"Resources\": {\n    \"Links\": {\n      \"reddit\": { \"0\": \"https://www.reddit.com/r/bitcoin\" },\n      \"website\": { \"0\": \"https://bitcoin.org/\" },\n      \"youtube\": { \"0\": \"https://www.youtube.com/watch?v=Gc2en3nHxA4&\" },\n      \"explorer\": {\n        \"0\": \"http://blockchain.com/explorer\",\n        \"1\": \"https://blockstream.info/\",\n        \"2\": \"https://blockchair.com/bitcoin\",\n        \"3\": \"https://live.blockcypher.com/btc/\",\n        \"4\": \"https://btc.cryptoid.info/btc/\"\n      },\n      \"facebook\": { \"0\": \"https://www.facebook.com/bitcoins/\" },\n      \"source_code\": { \"0\": \"https://github.com/bitcoin/bitcoin\" }\n    },\n    \"Thumbnail\": \"https://finage.s3.eu-west-2.amazonaws.com/cryptocurrency/128x128/bitcoin.png\"\n  },\n  \"Statistics\": {\n    \"MarketCapitalization\": 1815098270500.7,\n    \"MarketCapitalizationDiluted\": 1910222531533.24,\n    \"CirculatingSupply\": 19954253,\n    \"TotalSupply\": 19954253,\n    \"MaxSupply\": 21000000,\n    \"MarketCapDominance\": 58.3905,\n    \"TechnicalDoc\": \"https://bitcoin.org/bitcoin.pdf\",\n    \"Explorer\": \"https://blockchain.info/\",\n    \"SourceCode\": \"https://github.com/bitcoin/bitcoin\",\n    \"MessageBoard\": \"https://coinmarketcap.com/community/search/top/bitcoin\",\n    \"LowAllTime\": 0.04864654,\n    \"HighAllTime\": 126198.06960343386\n  }\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "fundamental-data-for-cryptocurrencies"
---

# Fundamental Data: Cryptocurrencies

## 源URL

https://eodhd.com/financial-apis/fundamental-data-for-cryptocurrencies

## 描述

We provide a unified, structured, and expanded fundamental dataset for major cryptocurrencies.This dataset includes supply metrics, market capitalization, all-time levels, technical resources, project metadata, community links, and more. All responses follow a consistent JSON schema across all crypto assets.

## API 端点

**Endpoint**: `https://eodhd.com/api/fundamentals/BTC-USD.CC`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Type` | - | 否 | - | string |
| `Category` | - | 否 | - | string |
| `WebURL` | - | 否 | - | string |
| `Description` | - | 否 | - | string |

## 文档正文

We provide a unified, structured, and expanded fundamental dataset for major cryptocurrencies.This dataset includes supply metrics, market capitalization, all-time levels, technical resources, project metadata, community links, and more. All responses follow a consistent JSON schema across all crypto assets.

## API Endpoint

```text
https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| Type | string |
| Category | string |
| WebURL | string |
| Description | string |

## Overview

The EODHD Cryptocurrency Fundamentals API provides point-in-time, project-level metadata and supply metrics for major cryptocurrencies.Data includes:

This feeds use the unified .CC virtual crypto exchange, enabling consistent access across all symbols.

## Output fields

Array of known developers, founders, maintainers.

Multiple categories of resource URLs.

## Code Examples

```text
https://eodhd.com/api/fundamentals/{SYMBOL}.CC
```

```json
{
  "General": {
    "Name": "Bitcoin",
    "Type": "Crypto",
    "Category": "coin",
    "WebURL": "https://bitcoin.org/",
    "Description": "Bitcoin is a cryptocurrency and worldwide payment system. It is the first decentralized digital currency, as the system works without a central bank or single administrator."
  },
  "Tech": {
    "Developers": {
      "0": "Satoshi Nakamoto - Founder",
      "1": "Wladimir J. van der Laan - Blockchain Developer",
      "2": "Jonas Schnelli - Blockchain Developer",
      "3": "Marco Falke - Blockchain Developer"
    }
  },
  "Resources": {
    "Links": {
      "reddit": { "0": "https://www.reddit.com/r/bitcoin" },
      "website": { "0": "https://bitcoin.org/" },
      "youtube": { "0": "https://www.youtube.com/watch?v=Gc2en3nHxA4&" },
      "explorer": {
        "0": "http://blockchain.com/explorer",
        "1": "https://blockstream.info/",
        "2": "https://blockchair.com/bitcoin",
        "3": "https://live.blockcypher.com/btc/",
        "4": "https://btc.cryptoid.info/btc/"
      },
      "facebook": { "0": "https://www.facebook.com/bitcoins/" },
      "source_code": { "0": "https://github.com/bitcoin/bitcoin" }
    },
    "Thumbnail": "https://finage.s3.eu-west-2.amazonaws.com/cryptocurrency/128x128/bitcoin.png"
  },
  "Statistics": {
    "MarketCapitalization": 1815098270500.7,
    "MarketCapitalizationDiluted": 1910222531533.24,
    "CirculatingSupply": 19954253,
    "TotalSupply": 19954253,
    "MaxSupply": 21000000,
    "MarketCapDominance": 58.3905,
    "TechnicalDoc": "https://bitcoin.org/bitcoin.pdf",
    "Explorer": "https://blockchain.info/",
    "SourceCode": "https://github.com/bitcoin/bitcoin",
    "MessageBoard": "https://coinmarketcap.com/community/search/top/bitcoin",
    "LowAllTime": 0.04864654,
    "HighAllTime": 126198.06960343386
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
