# Quotes

## 源URL

https://massive.com/docs/websocket/futures/quotes

## 描述

Stream BBO (Best Bid and Offer) quote data for futures tickers via WebSocket. Each message provides the current best bid/ask prices, sizes, and related metadata as they update, allowing users to monitor evolving market conditions, inform trading decisions, and maintain responsive, data-driven applications.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a future ticker or use * to subscribe to all future tickers.<br>You can also use a comma separated list to subscribe to multiple future tickers.<br>You can retrieve available future tickers from our Futures Contracts API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (Q) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given future. |
| bp | number | 否 | The bid price is expressed per unit of the underlying asset, and you apply the contract multiplier to get the full contract value. |
| bs | integer | 否 | The quote size represents the number of futures contracts available at the given bid price. |
| bt | integer | 否 | The timestamp when the bid was submitted to the exchange. |
| ap | number | 否 | The ask price is expressed per unit of the underlying asset, and you apply the contract multiplier to get the full contract value. |
| as | integer | 否 | The quote size represents the number of futures contracts available at the given ask price. |
| at | integer | 否 | The timestamp when the ask was submitted to the exchange. |
| t | integer | 否 | The timestamp in Unix MS. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/futures

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"Q.*"}
```

```json
{
  "ev": "Q",
  "sym": "ESZ4",
  "bp": 114.125,
  "bs": 100,
  "bt": 1734103628360,
  "ap": 114.128,
  "as": 160,
  "at": 1734103628350,
  "t": 1536036818784
}
```
