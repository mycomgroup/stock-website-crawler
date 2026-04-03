# Fair Market Value

## 源URL

https://massive.com/docs/websocket/options/fair-market-value

## 描述

Stream real-time Fair Market Value (FMV) data for a specified options contract via WebSocket. This proprietary metric, available exclusively to Business plan users, provides an algorithmically derived, real-time estimate of an option’s fair market price. By delivering accurate, continuous valuation data, this feed supports more informed options trading decisions, enhanced analytics, and improved risk management.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify an option contract. You're only allowed to subscribe to 1,000 option contracts per connection.<br>You can also use a comma separated list to subscribe to multiple option contracts.<br>You can retrieve active options contracts from our Options Contracts API. |

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
npx wscat -c wss://business.massive.com/options

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"FMV.O:SPY251219C00650000"}
```

```json
{
  "ev": "FMV",
  "fmv": 7.2,
  "sym": "O:TSLA210903C00700000",
  "t": 1401715883806000000
}
```
