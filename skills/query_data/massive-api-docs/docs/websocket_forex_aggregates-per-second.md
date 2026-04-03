# Aggregates (Per Second)

## 源URL

https://massive.com/docs/websocket/forex/aggregates-per-second

## 描述

Stream second-by-second aggregated OHLC (Open, High, Low, Close) and volume data for a specified Forex currency pair via WebSocket. These aggregates update continuously in Eastern Time (ET) and are derived from the best bid/offer quotes rather than executed trades. If no new quotes occur within a given minute, no bar is emitted, transparently indicating a period without market updates. By providing a continuous feed of updated market snapshots, this endpoint supports intraday analysis, dynamic charting, and the refinement of real-time Forex trading strategies.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a forex pair in the format {from}-{to} or use * to subscribe to all forex pairs.<br>You can also use a comma separated list to subscribe to multiple forex pairs.<br>You can retrieve active forex tickers from our Forex Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (CAS) | 否 | The event type. |
| pair | string | 否 | The currency pair. |
| o | number | 否 | The open price for this aggregate window. |
| c | number | 否 | The close price for this aggregate window. |
| h | number | 否 | The high price for this aggregate window. |
| l | number | 否 | The low price for this aggregate window. |
| v | integer | 否 | The volume of trades during this aggregate window. |
| s | integer | 否 | The start timestamp of this aggregate window in Unix Milliseconds. |
| e | integer | 否 | The end timestamp of this aggregate window in Unix Milliseconds. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://socket.massive.com/forex

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"CAS.*"}
```

```json
{
  "ev": "CAS",
  "pair": "USD/EUR",
  "o": 0.8687,
  "c": 0.86889,
  "h": 0.86889,
  "l": 0.8686,
  "v": 20,
  "s": 1539145740000
}
```
