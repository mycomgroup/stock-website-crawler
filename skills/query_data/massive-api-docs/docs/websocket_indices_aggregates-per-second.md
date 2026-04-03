# Aggregates (Per Second)

## 源URL

https://massive.com/docs/websocket/indices/aggregates-per-second

## 描述

Stream second-by-second aggregated OHLC (Open, High, Low, Close) for a specified index via WebSocket. These aggregates update continuously in Eastern Time (ET) and capture changes in the index’s values. Unlike stocks or options, index aggregates are derived from index values rather than individual trades. If no new index updates occur within a given minute, no bar is emitted. By providing an ongoing feed of updated market snapshots, this endpoint enables users to track intraday index movements, refine analysis, and power real-time market visualizations.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify an index ticker using "I:" prefix or use * to subscribe to all index tickers.<br>You can also use a comma separated list to subscribe to multiple index tickers.<br>You can retrieve available index tickers from our Index Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (A) | 否 | The event type. |
| sym | string | 否 | The symbol representing the given index. |
| op | number | 否 | Today's official opening value. |
| o | number | 否 | The opening index value for this aggregate window. |
| c | number | 否 | The closing index value for this aggregate window. |
| h | number | 否 | The highest index value for this aggregate window. |
| l | number | 否 | The lowest index value for this aggregate window. |
| s | integer | 否 | The start timestamp of this aggregate window in Unix Milliseconds. |
| e | integer | 否 | The end timestamp of this aggregate window in Unix Milliseconds. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/indices

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"A.*"}
```

```json
{
  "ev": "A",
  "sym": "I:SPX",
  "op": 3985.67,
  "o": 3985.67,
  "c": 3985.67,
  "h": 3985.67,
  "l": 3985.67,
  "s": 1678220675805,
  "e": 1678220675805
}
```
