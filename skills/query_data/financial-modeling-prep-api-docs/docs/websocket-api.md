---
id: "url-2df5a20a"
type: "api"
title: "Company Web Socket API"
url: "https://site.financialmodelingprep.com/developer/docs/websocket-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:23:49.608Z"
metadata:
  markdownContent: "# Company Web Socket API\n\n**Response Example:**\n\n```json\n{\n\t\"s\": \"aapl\",\n\t\"t\": 1645216790788174600,\n\t\"type\": \"Q\",\n\t\"ap\": 152.46,\n\t\"as\": 200,\n\t\"bp\": 152.31,\n\t\"bs\": 100,\n\t\"lp\": 152.17,\n\t\"ls\": 100\n}\n```\n\n\n## About Company Web Socket API\n\nA WebSocket is a type of communication protocol that allows for real-time updates, such as company stock prices and quote data.  Login: { \"event\": \"login\", \"data\": { \"apiKey\": \"your_api_key\" } } Subscribe: { \"event\": \"subscribe\", \"data\": { \"ticker\": [\"aapl\", \"msft\"] } }  Unsubscribe: { \"event\": \"unsubscribe\", \"data\": { \"ticker\": [\"aapl\", \"msft\"] } } Parameter: ticker: Subscribe to single ticker by providing as a string, or Subscribe to multiple tickers by providing list of tickers as following example. data: { \"ticker\": \"aapl\" } or { \"ticker\": [\"aapl\", \"msft\"] }. Response: s: Ticker related to the asset. t: Timestamp type: Trade type (Communicates what type of price update this is. Will always be 'T' for last trade message, 'Q' for top-of-book update message, and 'B' for trade break messages.)ap: The current lowest ask price. Only available for Quote updates, null otherwise.as: The number of shares at the ask price. Only available for Quote updates, null otherwise.bs: The number shares at the bid price. Only available for Quote updates, null otherwise.bp: The current highest bid price. Only available for Quote updates, null otherwise.lp: The last price the last trade was executed at. Only available for Trade and Break updates, null otherwise.ls: The amount of shares (volume) traded at the last price. Only available for Trade and Break updates, null otherwise.\n\n\n## Related Company Web Socket APIs\n\n\n## Company Web Socket API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "websocket-api"
---

# Company Web Socket API

## 源URL

https://site.financialmodelingprep.com/developer/docs/websocket-api

## 文档正文

**Response Example:**

```json
{
	"s": "aapl",
	"t": 1645216790788174600,
	"type": "Q",
	"ap": 152.46,
	"as": 200,
	"bp": 152.31,
	"bs": 100,
	"lp": 152.17,
	"ls": 100
}
```

## About Company Web Socket API

A WebSocket is a type of communication protocol that allows for real-time updates, such as company stock prices and quote data.  Login: { "event": "login", "data": { "apiKey": "your_api_key" } } Subscribe: { "event": "subscribe", "data": { "ticker": ["aapl", "msft"] } }  Unsubscribe: { "event": "unsubscribe", "data": { "ticker": ["aapl", "msft"] } } Parameter: ticker: Subscribe to single ticker by providing as a string, or Subscribe to multiple tickers by providing list of tickers as following example. data: { "ticker": "aapl" } or { "ticker": ["aapl", "msft"] }. Response: s: Ticker related to the asset. t: Timestamp type: Trade type (Communicates what type of price update this is. Will always be 'T' for last trade message, 'Q' for top-of-book update message, and 'B' for trade break messages.)ap: The current lowest ask price. Only available for Quote updates, null otherwise.as: The number of shares at the ask price. Only available for Quote updates, null otherwise.bs: The number shares at the bid price. Only available for Quote updates, null otherwise.bp: The current highest bid price. Only available for Quote updates, null otherwise.lp: The last price the last trade was executed at. Only available for Trade and Break updates, null otherwise.ls: The amount of shares (volume) traded at the last price. Only available for Trade and Break updates, null otherwise.

## Related Company Web Socket APIs

## Company Web Socket API FAQs

## Unlock Premium Financial Insights Today!
