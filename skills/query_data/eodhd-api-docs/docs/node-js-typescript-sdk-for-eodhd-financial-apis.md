---
id: "url-7f78069d"
type: "api"
title: "Node.js/TypeScript SDK for EODHD Financial APIs"
url: "https://eodhd.com/financial-apis/node-js-typescript-sdk-for-eodhd-financial-apis"
description: "The official EODHD Node.js/TypeScript library gives you a single, typed client for every EODHD API — historical prices, fundamentals, real-time WebSocket streaming, options, news, screener, macro indicators, and more. It covers 150,000+ tickers across 70+ exchanges, ships with built-in retry logic, rate-limit handling, and works in Node.js, Deno, Bun, and modern browsers."
source: ""
tags: []
crawl_time: "2026-03-18T12:03:21.679Z"
metadata:
  endpoint: ""
  parameters:
    - {"name":"WebSocket (Node.js)","description":"Optional ws package (browsers use native WebSocket)"}
  markdownContent: "# Node.js/TypeScript SDK for EODHD Financial APIs\n\nThe official EODHD Node.js/TypeScript library gives you a single, typed client for every EODHD API — historical prices, fundamentals, real-time WebSocket streaming, options, news, screener, macro indicators, and more. It covers 150,000+ tickers across 70+ exchanges, ships with built-in retry logic, rate-limit handling, and works in Node.js, Deno, Bun, and modern browsers.\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| WebSocket (Node.js) | Optional ws package (browsers use native WebSocket) |\n\n\n## Installation\n\nThe package has zero runtime dependencies. For WebSocket streaming in Node.js, install the optional ws peer dependency:\n\n## Quick Start\n\nYou can also set the EODHD_API_TOKEN environment variable instead of passing it directly:\n\n## End-of-Day Prices\n\nFetch daily, weekly, or monthly OHLCV data for any ticker. The ticker format is SYMBOL.EXCHANGE (e.g. AAPL.US, VOD.LSE, BTC-USD.CC).\n\n## Live (Delayed) Prices\n\nGet the latest 1-minute OHLCV bar with a 15-20 minute delay. Supports multiple tickers in a single request.\n\n## US Extended Delayed Quotes\n\nBatch delayed quotes for US equities with bid/ask, last trade, 52-week extremes, market cap, P/E, dividends, and more. See the Live API docs for the full field list.\n\n## Bulk EOD Data\n\nDownload end-of-day prices for an entire exchange in a single request.\n\n## Fundamentals\n\nRetrieve full company fundamentals — general info, financial statements, valuation metrics, earnings, and more. You can filter specific sections to reduce payload size.\n\n## Calendar Events\n\nAccess upcoming and historical earnings, IPOs, splits, and dividends through the calendar API.\n\n## Technical Indicators\n\nCalculate over 20 technical indicators directly through the API: SMA, EMA, WMA, MACD, RSI, Stochastic, Bollinger Bands, ADX, ATR, CCI, SAR, and more.\n\n## WebSocket (Real-Time Streaming)\n\nStream real-time market data via WebSocket. Four feeds are available: us (US trades), us-quote (US quotes), forex, and crypto. The client auto-reconnects with exponential backoff on connection loss.\n\nWebSocket options:\n\n## Marketplace APIs\n\nAccess third-party data providers through the EODHD Marketplace: Unicorn Bay (options, S&P Global indices, tick data, logos), Trading Hours, PRAAMS (investment analytics), and InvestVerte (ESG data).\n\n## Error Handling\n\nThe SDK provides a structured error hierarchy. All API errors extend EODHDError with status code, error code, and retryability information. Transient errors (429, 5xx) are automatically retried with exponential backoff.\n\n## TypeScript Support\n\nThe library is written in TypeScript with strict mode enabled. All methods, parameters, and responses are fully typed — you get autocompletion and compile-time checks out of the box.\n\n## API Coverage\n\nThe SDK provides typed methods for every EODHD API endpoint:\n\n## Code Examples\n\n```text\nnpm install eodhd\n```\n\n```text\nnpm install ws\n```\n\n```text\nimport { EODHDClient } from 'eodhd';\n\nconst client = new EODHDClient({ apiToken: 'YOUR_API_TOKEN' });\n\n// Get historical end-of-day prices\nconst prices = await client.eod('AAPL.US', { from: '2024-01-01', to: '2024-12-31' });\nconsole.log(prices[0]);\n// { date: '2024-01-02', open: 187.15, high: 188.44, low: 183.89, close: 185.64, adjusted_close: 184.53, volume: 82488700 }\n\n// Get live (delayed) stock price\nconst quote = await client.realTime('AAPL.US');\nconsole.log(`${quote.code}: $${quote.close} (${quote.change_p}%)`);\n\n// Search for stocks\nconst results = await client.search('Tesla', { limit: 5 });\n```\n\n```text\nexport EODHD_API_TOKEN=your_token_here\n```\n\n```text\n// Token is read from EODHD_API_TOKEN automatically\nconst client = new EODHDClient({});\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "node-js-typescript-sdk-for-eodhd-financial-apis"
---

# Node.js/TypeScript SDK for EODHD Financial APIs

## 源URL

https://eodhd.com/financial-apis/node-js-typescript-sdk-for-eodhd-financial-apis

## 描述

The official EODHD Node.js/TypeScript library gives you a single, typed client for every EODHD API — historical prices, fundamentals, real-time WebSocket streaming, options, news, screener, macro indicators, and more. It covers 150,000+ tickers across 70+ exchanges, ships with built-in retry logic, rate-limit handling, and works in Node.js, Deno, Bun, and modern browsers.

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `WebSocket (Node.js)` | - | 否 | - | Optional ws package (browsers use native WebSocket) |

## 文档正文

The official EODHD Node.js/TypeScript library gives you a single, typed client for every EODHD API — historical prices, fundamentals, real-time WebSocket streaming, options, news, screener, macro indicators, and more. It covers 150,000+ tickers across 70+ exchanges, ships with built-in retry logic, rate-limit handling, and works in Node.js, Deno, Bun, and modern browsers.

## Parameters

| Parameter | Description |
|-----------|-------------|
| WebSocket (Node.js) | Optional ws package (browsers use native WebSocket) |

## Installation

The package has zero runtime dependencies. For WebSocket streaming in Node.js, install the optional ws peer dependency:

## Quick Start

You can also set the EODHD_API_TOKEN environment variable instead of passing it directly:

## End-of-Day Prices

Fetch daily, weekly, or monthly OHLCV data for any ticker. The ticker format is SYMBOL.EXCHANGE (e.g. AAPL.US, VOD.LSE, BTC-USD.CC).

## Live (Delayed) Prices

Get the latest 1-minute OHLCV bar with a 15-20 minute delay. Supports multiple tickers in a single request.

## US Extended Delayed Quotes

Batch delayed quotes for US equities with bid/ask, last trade, 52-week extremes, market cap, P/E, dividends, and more. See the Live API docs for the full field list.

## Bulk EOD Data

Download end-of-day prices for an entire exchange in a single request.

## Fundamentals

Retrieve full company fundamentals — general info, financial statements, valuation metrics, earnings, and more. You can filter specific sections to reduce payload size.

## Calendar Events

Access upcoming and historical earnings, IPOs, splits, and dividends through the calendar API.

## Technical Indicators

Calculate over 20 technical indicators directly through the API: SMA, EMA, WMA, MACD, RSI, Stochastic, Bollinger Bands, ADX, ATR, CCI, SAR, and more.

## WebSocket (Real-Time Streaming)

Stream real-time market data via WebSocket. Four feeds are available: us (US trades), us-quote (US quotes), forex, and crypto. The client auto-reconnects with exponential backoff on connection loss.

WebSocket options:

## Marketplace APIs

Access third-party data providers through the EODHD Marketplace: Unicorn Bay (options, S&P Global indices, tick data, logos), Trading Hours, PRAAMS (investment analytics), and InvestVerte (ESG data).

## Error Handling

The SDK provides a structured error hierarchy. All API errors extend EODHDError with status code, error code, and retryability information. Transient errors (429, 5xx) are automatically retried with exponential backoff.

## TypeScript Support

The library is written in TypeScript with strict mode enabled. All methods, parameters, and responses are fully typed — you get autocompletion and compile-time checks out of the box.

## API Coverage

The SDK provides typed methods for every EODHD API endpoint:

## Code Examples

```text
npm install eodhd
```

```text
npm install ws
```

```text
import { EODHDClient } from 'eodhd';

const client = new EODHDClient({ apiToken: 'YOUR_API_TOKEN' });

// Get historical end-of-day prices
const prices = await client.eod('AAPL.US', { from: '2024-01-01', to: '2024-12-31' });
console.log(prices[0]);
// { date: '2024-01-02', open: 187.15, high: 188.44, low: 183.89, close: 185.64, adjusted_close: 184.53, volume: 82488700 }

// Get live (delayed) stock price
const quote = await client.realTime('AAPL.US');
console.log(`${quote.code}: $${quote.close} (${quote.change_p}%)`);

// Search for stocks
const results = await client.search('Tesla', { limit: 5 });
```

```text
export EODHD_API_TOKEN=your_token_here
```

```text
// Token is read from EODHD_API_TOKEN automatically
const client = new EODHDClient({});
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
