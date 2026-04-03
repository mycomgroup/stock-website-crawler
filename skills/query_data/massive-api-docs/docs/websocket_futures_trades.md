# Trades

## 源URL

https://massive.com/docs/websocket/futures/trades

## 描述

Stream tick-level trade data for futures tickers via WebSocket. Each message delivers key trade details (price, size, exchange, conditions, and timestamps) as they occur, enabling users to track market activity, power live dashboards, and inform rapid decision-making.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a future ticker or use * to subscribe to all future tickers.<br>You can also use a comma separated list to subscribe to multiple future tickers.<br>You can retrieve available future tickers from our Futures Contracts API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (T) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given future. |
| p | number | 否 | The trade price is quoted per unit of the underlying asset, with the total contract value determined by multiplying by the contract’s specific multiplier. |
| s | integer | 否 | The trade size shows the number of futures contracts actually exchanged. |
| t | integer | 否 | The timestamp in Unix MS. |
| q | integer | 否 | The sequence number represents the sequence in which message events happened.<br>These are increasing and unique per ticker symbol, but will not always be<br>sequential (e.g., 1, 2, 6, 9, 10, 11). |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/futures

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"T.*"}
```

```json
{
  "ev": "T",
  "sym": "ESZ4",
  "z": 3,
  "p": 606450,
  "s": 100,
  "t": 1734103628363,
  "q": 32599300
}
```
