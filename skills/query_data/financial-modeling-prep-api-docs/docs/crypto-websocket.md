---
id: "url-2c0e7305"
type: "api"
title: "Crypto Web Socket API"
url: "https://site.financialmodelingprep.com/developer/docs/crypto-websocket"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:34:59.232Z"
metadata:
  markdownContent: "# Crypto Web Socket API\n\n**Response Example:**\n\n```json\n{\n\t\"s\": \"btcusd\",\n\t\"t\": 16487238632060000000,\n\t\"e\": \"binance\",\n\t\"type\": \"Q\",\n\t\"bs\": 0.00689248,\n\t\"bp\": 47244.8,\n\t\"as\": 1.72784126,\n\t\"ap\": 47244.9\n}\n```\n\n\n## About Crypto Web Socket API\n\nA WebSocket is a type of communication protocol that allows for real-time updates, such as crypto stock prices and quote data.  Login: { \"event\": \"login\", \"data\": { \"apiKey\": \"your_api_key\" } } Subscribe: { \"event\": \"subscribe\", \"data\": { \"ticker\": [\"btcusd\", \"ethusd\"] } }  Unsubscribe: { \"event\": \"unsubscribe\", \"data\": { \"ticker\": [\"btcusd\", \"ethusd\"] } } Parameter: ticker: Subscribe to single ticker by providing as a string, or Subscribe to multiple tickers by providing list of tickers as following example. data: { \"ticker\": \"ethusd\" } or { \"ticker\": [\"btcusd\", \"ethusd\"] }. Response: s: Ticker related to the asset. t: Timestamp type: Trade type (Communicates what type of price update this is. Will always be 'T' for last trade message, 'Q' for top-of-book update message, and 'B' for trade break messages.)ap: The current lowest ask price. Only available for Quote updates, null otherwise.as: The number of shares at the ask price. Only available for Quote updates, null otherwise.bs: The number shares at the bid price. Only available for Quote updates, null otherwise.bp: The current highest bid price. Only available for Quote updates, null otherwise.lp: The last price the last trade was executed at. Only available for Trade and Break updates, null otherwise.ls: The amount of shares (volume) traded at the last price. Only available for Trade and Break updates, null otherwise.\n\n\n## Related Crypto Web Socket APIs\n\n\n## Crypto Web Socket API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "crypto-websocket"
---

# Crypto Web Socket API

## 源URL

https://site.financialmodelingprep.com/developer/docs/crypto-websocket

## 文档正文

**Response Example:**

```json
{
	"s": "btcusd",
	"t": 16487238632060000000,
	"e": "binance",
	"type": "Q",
	"bs": 0.00689248,
	"bp": 47244.8,
	"as": 1.72784126,
	"ap": 47244.9
}
```

## About Crypto Web Socket API

A WebSocket is a type of communication protocol that allows for real-time updates, such as crypto stock prices and quote data.  Login: { "event": "login", "data": { "apiKey": "your_api_key" } } Subscribe: { "event": "subscribe", "data": { "ticker": ["btcusd", "ethusd"] } }  Unsubscribe: { "event": "unsubscribe", "data": { "ticker": ["btcusd", "ethusd"] } } Parameter: ticker: Subscribe to single ticker by providing as a string, or Subscribe to multiple tickers by providing list of tickers as following example. data: { "ticker": "ethusd" } or { "ticker": ["btcusd", "ethusd"] }. Response: s: Ticker related to the asset. t: Timestamp type: Trade type (Communicates what type of price update this is. Will always be 'T' for last trade message, 'Q' for top-of-book update message, and 'B' for trade break messages.)ap: The current lowest ask price. Only available for Quote updates, null otherwise.as: The number of shares at the ask price. Only available for Quote updates, null otherwise.bs: The number shares at the bid price. Only available for Quote updates, null otherwise.bp: The current highest bid price. Only available for Quote updates, null otherwise.lp: The last price the last trade was executed at. Only available for Trade and Break updates, null otherwise.ls: The amount of shares (volume) traded at the last price. Only available for Trade and Break updates, null otherwise.

## Related Crypto Web Socket APIs

## Crypto Web Socket API FAQs

## Unlock Premium Financial Insights Today!
