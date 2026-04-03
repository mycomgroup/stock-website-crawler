# Quotes

## 源URL

https://massive.com/docs/websocket/stocks/quotes

## 描述

Stream NBBO (National Best Bid and Offer) quote data for stock tickers via WebSocket. Each message provides the current best bid/ask prices, sizes, and related metadata as they update, allowing users to monitor evolving market conditions, inform trading decisions, and maintain responsive, data-driven applications.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a stock ticker or use * to subscribe to all stock tickers.<br>You can also use a comma separated list to subscribe to multiple stock tickers.<br>You can retrieve available stock tickers from our Stock Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (Q) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given stock. |
| bx | integer | 否 | The bid exchange ID. |
| bp | number | 否 | The bid price. |
| bs | integer | 否 | The bid size. This represents the number of round lot orders at the given bid price. The normal round lot size is 100 shares. A bid size of 2 means there are 200 shares for purchase at the given bid price. |
| ax | integer | 否 | The ask exchange ID. |
| ap | number | 否 | The ask price. |
| as | integer | 否 | The ask size. This represents the number of round lot orders at the given ask price. The normal round lot size is 100 shares. An ask size of 2 means there are 200 shares available to purchase at the given ask price. |
| c | integer | 否 | The condition. |
| i | array (integer) | 否 | The indicators. For more information, see our glossary of Conditions and<br>Indicators. |
| t | integer | 否 | The SIP timestamp in Unix MS. |
| q | integer | 否 | The sequence number represents the sequence in which quote events happened.<br>These are increasing and unique per ticker symbol, but will not always be<br>sequential (e.g., 1, 2, 6, 9, 10, 11). Values reset after each trading session/day. |
| z | integer | 否 | The tape. (1 = NYSE, 2 = AMEX, 3 = Nasdaq). |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/stocks

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"Q.*"}
```

```json
{
  "ev": "Q",
  "sym": "MSFT",
  "bx": 4,
  "bp": 114.125,
  "bs": 100,
  "ax": 7,
  "ap": 114.128,
  "as": 160,
  "c": 0,
  "i": [
    604
  ],
  "t": 1536036818784,
  "q": 50385480,
  "z": 3
}
```
