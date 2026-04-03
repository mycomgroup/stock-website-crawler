# Aggregates (Per Minute)

## 源URL

https://massive.com/docs/websocket/crypto/aggregates-per-minute

## 描述

Stream minute-by-minute aggregated OHLC (Open, High, Low, Close) and volume data for a specified cryptocurrency pair via WebSocket. These aggregates update continuously in Coordinated Universal Time (UTC). If no trades occur within a given minute, no bar is emitted, transparently indicating a period without trading activity. This endpoint provides a live feed of aggregated bars, enabling users to monitor intraday price movements, refine trading strategies, and power real-time crypto market visualizations.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a crypto pair in the format {from}-{to} or use * to subscribe to all crypto pairs.<br>You can also use a comma separated list to subscribe to multiple crypto pairs.<br>You can retrieve active crypto tickers from our Crypto Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (XA) | 否 | The event type. |
| pair | string | 否 | The crypto pair. |
| o | number | 否 | The open price for this aggregate window. |
| c | number | 否 | The close price for this aggregate window. |
| h | number | 否 | The high price for this aggregate window. |
| l | number | 否 | The low price for this aggregate window. |
| v | integer | 否 | The volume of trades during this aggregate window. |
| s | integer | 否 | The start timestamp of this aggregate window in Unix Milliseconds. |
| e | integer | 否 | The end timestamp of this aggregate window in Unix Milliseconds. |
| vw | number | 否 | The volume weighted average price. |
| z | integer | 否 | The average trade size for this aggregate window. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://socket.massive.com/crypto

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"XA.*"}
```

```json
{
  "ev": "XA",
  "pair": "BCD-USD",
  "v": 951.6112,
  "vw": 0.7756,
  "z": 73,
  "o": 0.772,
  "c": 0.784,
  "h": 0.784,
  "l": 0.771,
  "s": 1610463240000,
  "e": 1610463300000
}
```
