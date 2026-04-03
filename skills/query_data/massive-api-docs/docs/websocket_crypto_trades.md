# Trades

## 源URL

https://massive.com/docs/websocket/crypto/trades

## 描述

Stream trade data for crypto pairs via WebSocket. Each message delivers key trade details (price, size, exchange, conditions, and timestamps) as they occur, enabling users to track market activity, power live dashboards, and inform rapid decision-making.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a crypto pair in the format {from}-{to} or use * to subscribe to all crypto pairs.<br>You can also use a comma separated list to subscribe to multiple crypto pairs.<br>You can retrieve active crypto tickers from our Crypto Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (XT) | 否 | The event type. |
| pair | string | 否 | The crypto pair. |
| p | number | 否 | The price. |
| t | integer | 否 | The Timestamp in Unix MS. |
| s | number | 否 | The size. |
| c | array (integer) | 否 | The conditions.<br>0 (or empty array): empty<br>1: sellside<br>2: buyside |
| i | integer | 否 | The ID of the trade (optional). |
| x | integer | 否 | The crypto exchange ID.  See Exchanges for a list of exchanges and their IDs. |
| r | integer | 否 | The timestamp that the tick was received by Massive. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://socket.massive.com/crypto

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"XT.*"}
```

```json
{
  "ev": "XT",
  "pair": "BTC-USD",
  "p": 33021.9,
  "t": 1610462007425,
  "s": 0.01616617,
  "c": [
    2
  ],
  "i": 14272084,
  "x": 3,
  "r": 1610462007576
}
```
