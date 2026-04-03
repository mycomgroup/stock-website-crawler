---
id: "url-f04d36b"
type: "api"
title: "Live v2 for US Stocks: Extended Quotes (2025)"
url: "https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025"
description: "Add real-time-style quote snapshots for US stocks to your product with a single request. This API returns a delayed (exchange-compliant) quote for each requested symbol, including last trade, bid/ask with sizes and timestamps, intraday change, rolling averages, 52-week extremes, market cap, and other reference fields."
source: ""
tags: []
crawl_time: "2026-03-18T08:31:44.970Z"
metadata:
  endpoint: "https://eodhd.com/api/us-quote-delayed"
  parameters:
    - {"name":"companyStandardName","description":"string"}
    - {"name":"description","description":"string"}
    - {"name":"sector","description":"string"}
    - {"name":"industry","description":"string"}
    - {"name":"open","description":"float"}
    - {"name":"high","description":"float"}
    - {"name":"low","description":"float"}
    - {"name":"bidPrice","description":"float"}
    - {"name":"bidSize","description":"integer"}
    - {"name":"bidTime","description":"integer (ms)"}
    - {"name":"askPrice","description":"float"}
    - {"name":"askSize","description":"integer"}
    - {"name":"askTime","description":"integer (ms)"}
    - {"name":"size","description":"integer"}
    - {"name":"lastTradePrice","description":"float"}
    - {"name":"lastTradeTime","description":"integer (ms)"}
    - {"name":"volume","description":"float"}
    - {"name":"change","description":"float"}
    - {"name":"changePercent","description":"float"}
    - {"name":"previousClosePrice","description":"float"}
    - {"name":"previousCloseDate","description":"string (YYYY-MM-DD HH:MM:SS)"}
    - {"name":"fiftyDayAveragePrice","description":"float"}
    - {"name":"hundredDayAveragePrice","description":"float"}
    - {"name":"twoHundredDayAveragePrice","description":"float"}
    - {"name":"averageVolume","description":"integer"}
    - {"name":"fiftyTwoWeekHigh","description":"float"}
    - {"name":"fiftyTwoWeekLow","description":"float"}
    - {"name":"marketCap","description":"integer"}
    - {"name":"sharesOutstanding","description":"integer"}
    - {"name":"sharesFloat","description":"integer"}
    - {"name":"pe","description":"float"}
    - {"name":"forwardPE","description":"float"}
    - {"name":"dividendYield","description":"float"}
    - {"name":"dividend","description":"float"}
    - {"name":"payoutRatio","description":"float"}
    - {"name":"ethPrice","description":"float"}
    - {"name":"ethVolume","description":"integer"}
    - {"name":"ethTime","description":"integer (ms)"}
    - {"name":"currency","description":"string"}
    - {"name":"issuerName","description":"string"}
    - {"name":"primary","description":"boolean"}
    - {"name":"shortDescription","description":"string"}
    - {"name":"issuerShortName","description":"string"}
    - {"name":"timestamp","description":"integer (s)"}
  markdownContent: "# Live v2 for US Stocks: Extended Quotes (2025)\n\nAdd real-time-style quote snapshots for US stocks to your product with a single request. This API returns a delayed (exchange-compliant) quote for each requested symbol, including last trade, bid/ask with sizes and timestamps, intraday change, rolling averages, 52-week extremes, market cap, and other reference fields.\n\n## API Endpoint\n\n```text\nhttps://eodhd.com/api/us-quote-delayed?s=AAPL.US&api_token=YOUR_API_TOKEN&fmt=json\n```\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| companyStandardName | string |\n| description | string |\n| sector | string |\n| industry | string |\n| open | float |\n| high | float |\n| low | float |\n| bidPrice | float |\n| bidSize | integer |\n| bidTime | integer (ms) |\n| askPrice | float |\n| askSize | integer |\n| askTime | integer (ms) |\n| size | integer |\n| lastTradePrice | float |\n| lastTradeTime | integer (ms) |\n| volume | float |\n| change | float |\n| changePercent | float |\n| previousClosePrice | float |\n| previousCloseDate | string (YYYY-MM-DD HH:MM:SS) |\n| fiftyDayAveragePrice | float |\n| hundredDayAveragePrice | float |\n| twoHundredDayAveragePrice | float |\n| averageVolume | integer |\n| fiftyTwoWeekHigh | float |\n| fiftyTwoWeekLow | float |\n| marketCap | integer |\n| sharesOutstanding | integer |\n| sharesFloat | integer |\n| pe | float |\n| forwardPE | float |\n| dividendYield | float |\n| dividend | float |\n| payoutRatio | float |\n| ethPrice | float |\n| ethVolume | integer |\n| ethTime | integer (ms) |\n| currency | string |\n| issuerName | string |\n| primary | boolean |\n| shortDescription | string |\n| issuerShortName | string |\n| timestamp | integer (s) |\n\n\n## Description\n\nThe API returns delayed quote data for one or more US stock symbols. Batch requests are supported via a comma-separated list of tickers. Pagination is available for large lists. Responses are delivered in JSON by default, with CSV supported as well. The top-level JSON contains meta, data (a per-symbol object), and links for pagination. Field names and types are listed in the tables below.\n\n## Output Format\n\nOutput fields per symbol (data[symbol]):\n\n## Live v2 vs Live v1\n\nLive v2 for US Stocks gives you an extended quote snapshot per symbol: last trade (with event time), full bid/ask with sizes and their event times, plus richer context like rolling averages, 52-week high/low, market cap, P/E, dividends, and issuer fields. It’s focused on US equities and is ideal for quote tiles, watchlists, and any UI that needs bid/ask and timing detail.\n\nLive v1 (“Live OHLCV Stock Prices API”) gives you the latest 1-minute OHLCV bar (open/high/low/close/volume) refreshed each minute. It doesn’t include bid/ask or trade event timestamps. It’s multi-asset (US and global stocks, Forex, crypto) and best when you only need the “last bar” for simple intraday charts or cross-asset tickers.\n\nIn short: choose Live v2 when you need quote-level details (bid/ask, last trade times, richer fundamentals) for US stocks; choose Live v1 when you need minute bars across multiple asset classes and don’t need quote microstructure.\n\n## Code Examples\n\n```text\nGET https://eodhd.com/api/us-quote-delayed\n```\n\n```json\n{\n  \"meta\": { \"count\": 2 },\n  \"data\": {\n    \"AAPL.US\": {\n      \"symbol\": \"AAPL.US\",\n      \"exchange\": \"XNAS\",\n      \"name\": \"Apple Inc\",\n      \"open\": 204.505,\n      \"high\": 207.88,\n      \"low\": 201.675,\n      \"lastTradePrice\": 203.32,\n      \"lastTradeTime\": 1754339340000,\n      \"bidPrice\": 203.28,\n      \"bidSize\": 4,\n      \"bidTime\": 1754339351000,\n      \"askPrice\": 203.32,\n      \"askSize\": 1,\n      \"askTime\": 1754339341000,\n      \"volume\": 73006032,\n      \"change\": 0.94,\n      \"changePercent\": 0.46,\n      \"previousClosePrice\": 202.38,\n      \"fiftyDayAveragePrice\": 205.28,\n      \"hundredDayAveragePrice\": 206.37,\n      \"twoHundredDayAveragePrice\": 221.53,\n      \"fiftyTwoWeekHigh\": 260.1,\n      \"fiftyTwoWeekLow\": 169.2101,\n      \"marketCap\": 3054287882360,\n      \"pe\": 30.710167,\n      \"forwardPE\": 25.974,\n      \"dividendYield\": 0.51,\n      \"currency\": \"USD\",\n      \"timestamp\": 1754339340\n    },\n    \"TSLA.US\": {\n      \"symbol\": \"TSLA.US\",\n      \"exchange\": \"XNAS\",\n      \"name\": \"Tesla Inc\",\n      \"lastTradePrice\": 245.11,\n      \"lastTradeTime\": 1754339340000,\n      \"bidPrice\": 245.09,\n      \"askPrice\": 245.12,\n      \"volume\": 51234567,\n      \"change\": -1.22,\n      \"changePercent\": -0.49,\n      \"currency\": \"USD\",\n      \"timestamp\": 1754339340\n    }\n  },\n  \"links\": { \"next\": null }\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "live-v2-for-us-stocks-extended-quotes-2025"
---

# Live v2 for US Stocks: Extended Quotes (2025)

## 源URL

https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025

## 描述

Add real-time-style quote snapshots for US stocks to your product with a single request. This API returns a delayed (exchange-compliant) quote for each requested symbol, including last trade, bid/ask with sizes and timestamps, intraday change, rolling averages, 52-week extremes, market cap, and other reference fields.

## API 端点

**Endpoint**: `https://eodhd.com/api/us-quote-delayed`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `companyStandardName` | - | 否 | - | string |
| `description` | - | 否 | - | string |
| `sector` | - | 否 | - | string |
| `industry` | - | 否 | - | string |
| `open` | - | 否 | - | float |
| `high` | - | 否 | - | float |
| `low` | - | 否 | - | float |
| `bidPrice` | - | 否 | - | float |
| `bidSize` | - | 否 | - | integer |
| `bidTime` | - | 否 | - | integer (ms) |
| `askPrice` | - | 否 | - | float |
| `askSize` | - | 否 | - | integer |
| `askTime` | - | 否 | - | integer (ms) |
| `size` | - | 否 | - | integer |
| `lastTradePrice` | - | 否 | - | float |
| `lastTradeTime` | - | 否 | - | integer (ms) |
| `volume` | - | 否 | - | float |
| `change` | - | 否 | - | float |
| `changePercent` | - | 否 | - | float |
| `previousClosePrice` | - | 否 | - | float |
| `previousCloseDate` | - | 否 | - | string (YYYY-MM-DD HH:MM:SS) |
| `fiftyDayAveragePrice` | - | 否 | - | float |
| `hundredDayAveragePrice` | - | 否 | - | float |
| `twoHundredDayAveragePrice` | - | 否 | - | float |
| `averageVolume` | - | 否 | - | integer |
| `fiftyTwoWeekHigh` | - | 否 | - | float |
| `fiftyTwoWeekLow` | - | 否 | - | float |
| `marketCap` | - | 否 | - | integer |
| `sharesOutstanding` | - | 否 | - | integer |
| `sharesFloat` | - | 否 | - | integer |
| `pe` | - | 否 | - | float |
| `forwardPE` | - | 否 | - | float |
| `dividendYield` | - | 否 | - | float |
| `dividend` | - | 否 | - | float |
| `payoutRatio` | - | 否 | - | float |
| `ethPrice` | - | 否 | - | float |
| `ethVolume` | - | 否 | - | integer |
| `ethTime` | - | 否 | - | integer (ms) |
| `currency` | - | 否 | - | string |
| `issuerName` | - | 否 | - | string |
| `primary` | - | 否 | - | boolean |
| `shortDescription` | - | 否 | - | string |
| `issuerShortName` | - | 否 | - | string |
| `timestamp` | - | 否 | - | integer (s) |

## 文档正文

Add real-time-style quote snapshots for US stocks to your product with a single request. This API returns a delayed (exchange-compliant) quote for each requested symbol, including last trade, bid/ask with sizes and timestamps, intraday change, rolling averages, 52-week extremes, market cap, and other reference fields.

## API Endpoint

```text
https://eodhd.com/api/us-quote-delayed?s=AAPL.US&api_token=YOUR_API_TOKEN&fmt=json
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| companyStandardName | string |
| description | string |
| sector | string |
| industry | string |
| open | float |
| high | float |
| low | float |
| bidPrice | float |
| bidSize | integer |
| bidTime | integer (ms) |
| askPrice | float |
| askSize | integer |
| askTime | integer (ms) |
| size | integer |
| lastTradePrice | float |
| lastTradeTime | integer (ms) |
| volume | float |
| change | float |
| changePercent | float |
| previousClosePrice | float |
| previousCloseDate | string (YYYY-MM-DD HH:MM:SS) |
| fiftyDayAveragePrice | float |
| hundredDayAveragePrice | float |
| twoHundredDayAveragePrice | float |
| averageVolume | integer |
| fiftyTwoWeekHigh | float |
| fiftyTwoWeekLow | float |
| marketCap | integer |
| sharesOutstanding | integer |
| sharesFloat | integer |
| pe | float |
| forwardPE | float |
| dividendYield | float |
| dividend | float |
| payoutRatio | float |
| ethPrice | float |
| ethVolume | integer |
| ethTime | integer (ms) |
| currency | string |
| issuerName | string |
| primary | boolean |
| shortDescription | string |
| issuerShortName | string |
| timestamp | integer (s) |

## Description

The API returns delayed quote data for one or more US stock symbols. Batch requests are supported via a comma-separated list of tickers. Pagination is available for large lists. Responses are delivered in JSON by default, with CSV supported as well. The top-level JSON contains meta, data (a per-symbol object), and links for pagination. Field names and types are listed in the tables below.

## Output Format

Output fields per symbol (data[symbol]):

## Live v2 vs Live v1

Live v2 for US Stocks gives you an extended quote snapshot per symbol: last trade (with event time), full bid/ask with sizes and their event times, plus richer context like rolling averages, 52-week high/low, market cap, P/E, dividends, and issuer fields. It’s focused on US equities and is ideal for quote tiles, watchlists, and any UI that needs bid/ask and timing detail.

Live v1 (“Live OHLCV Stock Prices API”) gives you the latest 1-minute OHLCV bar (open/high/low/close/volume) refreshed each minute. It doesn’t include bid/ask or trade event timestamps. It’s multi-asset (US and global stocks, Forex, crypto) and best when you only need the “last bar” for simple intraday charts or cross-asset tickers.

In short: choose Live v2 when you need quote-level details (bid/ask, last trade times, richer fundamentals) for US stocks; choose Live v1 when you need minute bars across multiple asset classes and don’t need quote microstructure.

## Code Examples

```text
GET https://eodhd.com/api/us-quote-delayed
```

```json
{
  "meta": { "count": 2 },
  "data": {
    "AAPL.US": {
      "symbol": "AAPL.US",
      "exchange": "XNAS",
      "name": "Apple Inc",
      "open": 204.505,
      "high": 207.88,
      "low": 201.675,
      "lastTradePrice": 203.32,
      "lastTradeTime": 1754339340000,
      "bidPrice": 203.28,
      "bidSize": 4,
      "bidTime": 1754339351000,
      "askPrice": 203.32,
      "askSize": 1,
      "askTime": 1754339341000,
      "volume": 73006032,
      "change": 0.94,
      "changePercent": 0.46,
      "previousClosePrice": 202.38,
      "fiftyDayAveragePrice": 205.28,
      "hundredDayAveragePrice": 206.37,
      "twoHundredDayAveragePrice": 221.53,
      "fiftyTwoWeekHigh": 260.1,
      "fiftyTwoWeekLow": 169.2101,
      "marketCap": 3054287882360,
      "pe": 30.710167,
      "forwardPE": 25.974,
      "dividendYield": 0.51,
      "currency": "USD",
      "timestamp": 1754339340
    },
    "TSLA.US": {
      "symbol": "TSLA.US",
      "exchange": "XNAS",
      "name": "Tesla Inc",
      "lastTradePrice": 245.11,
      "lastTradeTime": 1754339340000,
      "bidPrice": 245.09,
      "askPrice": 245.12,
      "volume": 51234567,
      "change": -1.22,
      "changePercent": -0.49,
      "currency": "USD",
      "timestamp": 1754339340
    }
  },
  "links": { "next": null }
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
