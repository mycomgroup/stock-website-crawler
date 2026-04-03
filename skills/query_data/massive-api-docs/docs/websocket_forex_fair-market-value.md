# Fair Market Value

## 源URL

https://massive.com/docs/websocket/forex/fair-market-value

## 描述

Stream real-time Fair Market Value (FMV) data for a specified Forex currency pair via WebSocket. This proprietary metric, available exclusively to Business plan users, provides an algorithmically derived, real-time estimate of the currency pair’s fair market price. By delivering accurate, continuous valuation data, this feed supports more informed trading decisions, enhanced analytics, and improved risk management.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a forex pair in the format {from}-{to} or use * to subscribe to all forex pairs.<br>You can also use a comma separated list to subscribe to multiple forex pairs.<br>You can retrieve active forex tickers from our Forex Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (FMV) | 否 | The event type. |
| fmv | number | 否 | Fair market value is only available on Business plans. It is our proprietary algorithm to generate a real-time, accurate, fair market value of a tradable security. For more information, contact us. |
| sym | string | 否 | The ticker symbol for the given security. |
| t | integer | 否 | The nanosecond timestamp. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://business.massive.com/forex

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"FMV.*"}
```

```json
{
  "ev": "FMV",
  "fmv": 1.0631,
  "sym": "C:EURUSD",
  "t": 1678220098130
}
```
