---
id: "url-466a9bec"
type: "api"
title: "Forex Web Socket API"
url: "https://site.financialmodelingprep.com/developer/docs/forex-websocket"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:31:15.791Z"
metadata:
  markdownContent: "# Forex Web Socket API\n\n**Response Example:**\n\n```json\n{\n\t\"s\": \"eurusd\",\n\t\"t\": 1701958248213,\n\t\"type\": \"Q\",\n\t\"ap\": 1.07865,\n\t\"as\": 1000000,\n\t\"bp\": 1.07856,\n\t\"bs\": 1000000\n}\n```\n\n\n## About Forex Web Socket API\n\nA WebSocket is a type of communication protocol that allows for real-time updates, such as forex stock prices and quote data.  Login: { \"event\": \"login\", \"data\": { \"apiKey\": \"your_api_key\" } } Subscribe: { \"event\": \"subscribe\", \"data\": { \"ticker\": [\"eurusd\", \"cndusd\"] } }  Unsubscribe: { \"event\": \"unsubscribe\", \"data\": { \"ticker\": [\"eurusd\", \"cndusd\"] } } Parameter: ticker: Subscribe to single ticker by providing as a string, or Subscribe to multiple tickers by providing list of tickers as following example. data: { \"ticker\": \"eurusd\" } or { \"ticker\": [\"eurusd\", \"cndusd\"] }. Response: s: Ticker related to the asset. t: Timestamp type: Trade type (Communicates what type of price update this is. Will always be 'T' for last trade message, 'Q' for top-of-book update message, and 'B' for trade break messages.)ap: The current lowest ask price. Only available for Quote updates, null otherwise.as: The number of shares at the ask price. Only available for Quote updates, null otherwise.bs: The number shares at the bid price. Only available for Quote updates, null otherwise.bp: The current highest bid price. Only available for Quote updates, null otherwise.lp: The last price the last trade was executed at. Only available for Trade and Break updates, null otherwise.ls: The amount of shares (volume) traded at the last price. Only available for Trade and Break updates, null otherwise.\n\n\n## Related Forex Web Socket APIs\n\n\n## Forex Web Socket API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "forex-websocket"
---

# Forex Web Socket API

## 源URL

https://site.financialmodelingprep.com/developer/docs/forex-websocket

## 文档正文

**Response Example:**

```json
{
	"s": "eurusd",
	"t": 1701958248213,
	"type": "Q",
	"ap": 1.07865,
	"as": 1000000,
	"bp": 1.07856,
	"bs": 1000000
}
```

## About Forex Web Socket API

A WebSocket is a type of communication protocol that allows for real-time updates, such as forex stock prices and quote data.  Login: { "event": "login", "data": { "apiKey": "your_api_key" } } Subscribe: { "event": "subscribe", "data": { "ticker": ["eurusd", "cndusd"] } }  Unsubscribe: { "event": "unsubscribe", "data": { "ticker": ["eurusd", "cndusd"] } } Parameter: ticker: Subscribe to single ticker by providing as a string, or Subscribe to multiple tickers by providing list of tickers as following example. data: { "ticker": "eurusd" } or { "ticker": ["eurusd", "cndusd"] }. Response: s: Ticker related to the asset. t: Timestamp type: Trade type (Communicates what type of price update this is. Will always be 'T' for last trade message, 'Q' for top-of-book update message, and 'B' for trade break messages.)ap: The current lowest ask price. Only available for Quote updates, null otherwise.as: The number of shares at the ask price. Only available for Quote updates, null otherwise.bs: The number shares at the bid price. Only available for Quote updates, null otherwise.bp: The current highest bid price. Only available for Quote updates, null otherwise.lp: The last price the last trade was executed at. Only available for Trade and Break updates, null otherwise.ls: The amount of shares (volume) traded at the last price. Only available for Trade and Break updates, null otherwise.

## Related Forex Web Socket APIs

## Forex Web Socket API FAQs

## Unlock Premium Financial Insights Today!
