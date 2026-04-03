# Aggregates (Per Second)

## 源URL

https://massive.com/docs/websocket/futures/aggregates-per-second

## 描述

Stream second-by-second aggregated OHLC (Open, High, Low, Close) and volume data for a specified futures contract ticker via WebSocket. Aggregates are continuously updated in Central Time (CT) and are constructed from all trades occurring within each defined aggregation window. If no trades occur during the window, no aggregate bar is emitted, indicating a period of inactivity. The response includes key metrics such as open, high, low, close, trade volume, and the start and end timestamps for each window.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a future ticker or use * to subscribe to all future tickers.<br>You can also use a comma separated list to subscribe to multiple future tickers.<br>You can retrieve available future tickers from our Futures Contracts API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (A) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given future. |
| v | number | 否 | The tick volume. |
| dv | number | 否 | The total US dollar value of shares traded within the aggregate window. |
| o | number | 否 | The opening tick price for this aggregate window. |
| c | number | 否 | The closing tick price for this aggregate window. |
| h | number | 否 | The highest tick price for this aggregate window. |
| l | number | 否 | The lowest tick price for this aggregate window. |
| n | number | 否 | The total number of transactions that occurred within the aggregate window |
| s | integer | 否 | The start timestamp of this aggregate window in Unix Milliseconds. |
| e | integer | 否 | The end timestamp of this aggregate window in Unix Milliseconds. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/futures

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"A.*"}
```

```json
{
  "ev": "AM",
  "sym": "6CH5",
  "v": 91,
  "dv": 1353.1,
  "o": 6994.5,
  "c": 6995,
  "h": 6995,
  "l": 6994.5,
  "n": 10,
  "s": 1734717060000,
  "e": 1734717120000
}
```
