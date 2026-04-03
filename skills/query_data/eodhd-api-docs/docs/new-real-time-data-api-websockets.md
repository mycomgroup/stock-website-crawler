---
id: "url-32c12c98"
type: "api"
title: "Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies"
url: "https://eodhd.com/financial-apis/new-real-time-data-api-websockets/"
description: "EODHD offers one of the best ways for investors, developers, and data analysts to incorporate real-time finance data for the US market, 1100+ Forex pairs, 1000+ Digital Currencies into their decision-making projects with a delay of less than 50ms via WebSockets. For US stocks our real-time data API supports pre-market and post-market hours (from 4 am to 8 pm EST)."
source: ""
tags: []
crawl_time: "2026-03-18T04:37:35.045Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies\n\nEODHD offers one of the best ways for investors, developers, and data analysts to incorporate real-time finance data for the US market, 1100+ Forex pairs, 1000+ Digital Currencies into their decision-making projects with a delay of less than 50ms via WebSockets. For US stocks our real-time data API supports pre-market and post-market hours (from 4 am to 8 pm EST).\n\n\n## What is WebSocket protocol\n\nWebSockets is a communication protocol that provides full-duplex communication channels over a single TCP connection. It enables real-time communication between a client and a server, allowing them to exchange messages continuously without the overhead of repeatedly establishing new connections. In the case of financial data providers, Websockets API provides real-time stock market information with minimal delay.\n\nProviding clients with the WebSocket protocol for real-time data answers the question: ‘What is the best stock market data API?”. Since websocket technology is quite resource consuming, “free stock API for real-time market data” stays as feature impossible to find. EODHD provides real-time data in paid plans EOD+Intraday and ALL-IN-ONE. Read more about plans here.\n\n## What you get (Data availability)\n\nUS Stocks (full list of US tickers available)• Trade stream (last price, size, conditions, etc.)• Quote stream (bid/ask, sizes)• Covers primary US exchanges (e.g., NASDAQ, NYSE)• Extended hours supported (pre‑ and post‑market)\n\nFOREX (full list of available currency pairs)• Bid/ask + day change/difference• Tickers like EURUSD, AUDUSD, etc.\n\nDigital Currencies (Full list of available crypto pairs)• Last price, quantity, day change/difference• Tickers like ETH-USD, BTC-USDLists of available tickers and pairs for Real-Time feeds can be retrieved in JSON format via this API endpoint, providing the full list of exchange or asset class components (use “US” for US stocks, “CC” for cryptocurrencies, “FOREX” for currency pairs).\n\nDemo access is available with API key “demo” for: AAPL, MSFT, TSLA, EURUSD, ETH-USD, BTC-USD.\n\n## Endpoints\n\nOpen connection – use wss:// in production. ws:// is available for local testing.\n\n## Subscribe / Unsubscribe\n\nAfter the socket is open, send JSON commands.\n\nMultiple symbols (comma‑separated):\n\n## US Trades (endpoint: /ws/us):\n\nNote: US trade messages include “c” (numeric) that maps to a condition code. See the downloadable glossary in the docs (pdf).\n\n## Symbol Limits & Usage Notes\n\nConcurrent subscriptions: up to 50 symbols per connection by default (upgradeable in user dashboard for extra fee).Tickers:\n\nResubscribe on reconnect: if the socket reconnects, re‑send your current subscriptions.Compression/Throughput: consider batching symbol lists in a single subscribe call for efficiency.\n\n## Examples (copy‑paste ready)\n\nOpen connection for US trades:\n\n## \n\nOpen connection for Forex pairs:\n\n## \n\nOpen connection for Crypto:\n\n## Tools for Testing\n\nChrome: Simple WebSocket Client extension (open a socket, paste open URL, send JSON quote).\n\nEODHD Chrome extension: free mini ticker window for live Stocks/FX/Crypto. Perfect to see our real-time data feed. No commands needed. Install from here.\n\nPostman (or Insomnia) – point-and-click:\n\nPython (minimal script):\n\nMac Os Terminal – websocat (via Homebrew):\n\nInstall websocat:\n\nOne-liner command:\n\n## Quick Comparison with Live (Delayed) API and Intraday API\n\n* Get the full list of covered tickers.\n\n## Code Examples\n\n```text\nwss://ws.eodhistoricaldata.com/ws/us?api_token=YOUR_API_KEY\n```\n\n```text\nwss://ws.eodhistoricaldata.com/ws/us-quote?api_token=YOUR_API_KEY\n```\n\n```text\nwss://ws.eodhistoricaldata.com/ws/forex?api_token=YOUR_API_KEY\n```\n\n```text\nwss://ws.eodhistoricaldata.com/ws/crypto?api_token=YOUR_API_KEY\n```\n\n```json\n{\"action\": \"subscribe\", \"symbols\": \"ETH-USD\"}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "new-real-time-data-api-websockets"
---

# Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies

## 源URL

https://eodhd.com/financial-apis/new-real-time-data-api-websockets/

## 描述

EODHD offers one of the best ways for investors, developers, and data analysts to incorporate real-time finance data for the US market, 1100+ Forex pairs, 1000+ Digital Currencies into their decision-making projects with a delay of less than 50ms via WebSockets. For US stocks our real-time data API supports pre-market and post-market hours (from 4 am to 8 pm EST).

## 文档正文

EODHD offers one of the best ways for investors, developers, and data analysts to incorporate real-time finance data for the US market, 1100+ Forex pairs, 1000+ Digital Currencies into their decision-making projects with a delay of less than 50ms via WebSockets. For US stocks our real-time data API supports pre-market and post-market hours (from 4 am to 8 pm EST).

## What is WebSocket protocol

WebSockets is a communication protocol that provides full-duplex communication channels over a single TCP connection. It enables real-time communication between a client and a server, allowing them to exchange messages continuously without the overhead of repeatedly establishing new connections. In the case of financial data providers, Websockets API provides real-time stock market information with minimal delay.

Providing clients with the WebSocket protocol for real-time data answers the question: ‘What is the best stock market data API?”. Since websocket technology is quite resource consuming, “free stock API for real-time market data” stays as feature impossible to find. EODHD provides real-time data in paid plans EOD+Intraday and ALL-IN-ONE. Read more about plans here.

## What you get (Data availability)

US Stocks (full list of US tickers available)• Trade stream (last price, size, conditions, etc.)• Quote stream (bid/ask, sizes)• Covers primary US exchanges (e.g., NASDAQ, NYSE)• Extended hours supported (pre‑ and post‑market)

FOREX (full list of available currency pairs)• Bid/ask + day change/difference• Tickers like EURUSD, AUDUSD, etc.

Digital Currencies (Full list of available crypto pairs)• Last price, quantity, day change/difference• Tickers like ETH-USD, BTC-USDLists of available tickers and pairs for Real-Time feeds can be retrieved in JSON format via this API endpoint, providing the full list of exchange or asset class components (use “US” for US stocks, “CC” for cryptocurrencies, “FOREX” for currency pairs).

Demo access is available with API key “demo” for: AAPL, MSFT, TSLA, EURUSD, ETH-USD, BTC-USD.

## Endpoints

Open connection – use wss:// in production. ws:// is available for local testing.

## Subscribe / Unsubscribe

After the socket is open, send JSON commands.

Multiple symbols (comma‑separated):

## US Trades (endpoint: /ws/us):

Note: US trade messages include “c” (numeric) that maps to a condition code. See the downloadable glossary in the docs (pdf).

## Symbol Limits & Usage Notes

Concurrent subscriptions: up to 50 symbols per connection by default (upgradeable in user dashboard for extra fee).Tickers:

Resubscribe on reconnect: if the socket reconnects, re‑send your current subscriptions.Compression/Throughput: consider batching symbol lists in a single subscribe call for efficiency.

## Examples (copy‑paste ready)

Open connection for US trades:

## 

Open connection for Forex pairs:

## 

Open connection for Crypto:

## Tools for Testing

Chrome: Simple WebSocket Client extension (open a socket, paste open URL, send JSON quote).

EODHD Chrome extension: free mini ticker window for live Stocks/FX/Crypto. Perfect to see our real-time data feed. No commands needed. Install from here.

Postman (or Insomnia) – point-and-click:

Python (minimal script):

Mac Os Terminal – websocat (via Homebrew):

Install websocat:

One-liner command:

## Quick Comparison with Live (Delayed) API and Intraday API

* Get the full list of covered tickers.

## Code Examples

```text
wss://ws.eodhistoricaldata.com/ws/us?api_token=YOUR_API_KEY
```

```text
wss://ws.eodhistoricaldata.com/ws/us-quote?api_token=YOUR_API_KEY
```

```text
wss://ws.eodhistoricaldata.com/ws/forex?api_token=YOUR_API_KEY
```

```text
wss://ws.eodhistoricaldata.com/ws/crypto?api_token=YOUR_API_KEY
```

```json
{"action": "subscribe", "symbols": "ETH-USD"}
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
