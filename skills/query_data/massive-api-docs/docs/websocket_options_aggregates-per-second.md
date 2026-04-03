# Aggregates (Per Second)

## 源URL

https://massive.com/docs/websocket/options/aggregates-per-second

## 描述

Stream second-by-second aggregated OHLC (Open, High, Low, Close) and volume data for a specified options contract via WebSocket. These aggregates are updated continuously in Eastern Time (ET). Each bar is constructed solely from qualifying trades that meet specific conditions; if no eligible trades occur within a given minute, no bar is emitted. By delivering an ongoing feed of updated market snapshots, this endpoint enables users to closely monitor intraday price movements, enhance trading strategies, and support live data visualizations in the options market.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify an option contract or use * to subscribe to all option contracts.<br>You can also use a comma separated list to subscribe to multiple option contracts.<br>You can retrieve active options contracts from our Options Contracts API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (A) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given option contract. |
| v | integer | 否 | The tick volume. |
| av | integer | 否 | Today's accumulated volume. |
| op | number | 否 | Today's official opening price. |
| vw | number | 否 | The tick's volume weighted average price. |
| o | number | 否 | The opening tick price for this aggregate window. |
| c | number | 否 | The closing tick price for this aggregate window. |
| h | number | 否 | The highest tick price for this aggregate window. |
| l | number | 否 | The lowest tick price for this aggregate window. |
| a | number | 否 | Today's volume weighted average price. |
| z | integer | 否 | The average trade size for this aggregate window. |
| s | integer | 否 | The start timestamp of this aggregate window in Unix Milliseconds. |
| e | integer | 否 | The end timestamp of this aggregate window in Unix Milliseconds. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/options

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"A.O:SPY251219C00650000"}
```

```json
{
  "ev": "AM",
  "sym": "O:ONEM220121C00025000",
  "v": 2,
  "av": 8,
  "op": 2.2,
  "vw": 2.05,
  "o": 2.05,
  "c": 2.05,
  "h": 2.05,
  "l": 2.05,
  "a": 2.1312,
  "z": 2,
  "s": 1632419640000,
  "e": 1632419700000
}
```
