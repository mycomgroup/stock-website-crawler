# Quotes

## 源URL

https://massive.com/docs/websocket/forex/quotes

## 描述

Stream real-time Best Bid and Offer (BBO) quote data for specified Forex currency pairs via WebSocket. Each message provides the current bid/ask prices, sizes, and associated metadata as they update, enabling users to monitor evolving market conditions, guide trading decisions, and power responsive, data-driven applications.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a forex pair in the format {from}-{to} or use * to subscribe to all forex pairs.<br>You can also use a comma separated list to subscribe to multiple forex pairs.<br>You can retrieve active forex tickers from our Forex Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (C) | 否 | The event type. |
| p | string | 否 | The current pair. |
| x | integer | 否 | The exchange ID. See Exchanges for Massive's mapping of exchange IDs. |
| a | number | 否 | The ask price. |
| b | number | 否 | The bid price. |
| t | integer | 否 | The Timestamp in Unix MS. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://socket.massive.com/forex

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"C.*"}
```

```json
{
  "ev": "C",
  "p": "USD/CNH",
  "x": "44",
  "a": 6.83366,
  "b": 6.83363,
  "t": 1536036818784
}
```
