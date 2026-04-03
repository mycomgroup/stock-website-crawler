# Value

## 源URL

https://massive.com/docs/websocket/indices/value

## 描述

Stream real-time index value updates for specified index tickers via WebSocket. Each message provides the index’s current value and timestamp, allowing users to monitor fluctuations in key market benchmarks or sectors throughout the trading session. This continuous feed supports live market analysis, trend identification, and integration of index-based signals into trading strategies and research.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify an index ticker using "I:" prefix or use * to subscribe to all index tickers.<br>You can also use a comma separated list to subscribe to multiple index tickers.<br>You can retrieve available index tickers from our Index Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (V) | 否 | The event type. |
| val | number | 否 | The value of the index. |
| T | string | 否 | The assigned ticker of the index. |
| t | integer | 否 | The Timestamp in Unix MS. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://business.massive.com/indices

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"V.I:SPX"}
```

```json
{
  "ev": "V",
  "val": 3988.5,
  "T": "I:SPX",
  "t": 1678220098130
}
```
