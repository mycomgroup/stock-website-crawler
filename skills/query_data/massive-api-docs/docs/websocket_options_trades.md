# Trades

## 源URL

https://massive.com/docs/websocket/options/trades

## 描述

Stream tick-level trade data for option contracts via WebSocket. Each message delivers key trade details (price, size, exchange, conditions, and timestamps) as they occur, enabling users to track market activity, power live dashboards, and inform rapid decision-making.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify an option contract or use * to subscribe to all option contracts.<br>You can also use a comma separated list to subscribe to multiple option contracts.<br>You can retrieve active options contracts from our Options Contracts API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (T) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given option contract. |
| x | integer | 否 | The exchange ID. See Exchanges for Massive's mapping of exchange IDs. |
| p | number | 否 | The price. |
| s | integer | 否 | The trade size. |
| c | array (integer) | 否 | The trade conditions |
| t | integer | 否 | The Timestamp in Unix MS. |
| q | integer | 否 | The sequence number represents the sequence in which trade events happened. These are increasing and unique per ticker symbol, but will not always be sequential (e.g., 1, 2, 6, 9, 10, 11). |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/options

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"T.O:SPY251219C00650000"}
```

```json
{
  "ev": "T",
  "sym": "O:AMC210827C00037000",
  "x": 65,
  "p": 1.54,
  "s": 1,
  "c": [
    233
  ],
  "t": 1629820676333,
  "q": 651921857
}
```
