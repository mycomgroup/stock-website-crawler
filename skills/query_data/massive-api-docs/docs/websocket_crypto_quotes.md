# Quotes

## 源URL

https://massive.com/docs/websocket/crypto/quotes

## 描述

Stream quote data for specified cryptocurrency pairs via WebSocket. Each message delivers current bid/ask prices, sizes, and relevant metadata from multiple exchanges as they update, allowing users to monitor evolving market conditions, guide trading decisions, and support responsive, data-driven applications.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a crypto pair in the format {from}-{to} or use * to subscribe to all crypto pairs.<br>You can also use a comma separated list to subscribe to multiple crypto pairs.<br>You can retrieve active crypto tickers from our Crypto Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (XQ) | 否 | The event type. |
| pair | string | 否 | The crypto pair. |
| bp | number | 否 | The bid price. |
| bs | number | 否 | The bid size. |
| ap | number | 否 | The ask price. |
| as | number | 否 | The ask size. |
| t | integer | 否 | The Timestamp in Unix MS. |
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
{"action":"subscribe", "params":"XQ.*"}
```

```json
{
  "ev": "XQ",
  "pair": "BTC-USD",
  "bp": 33052.79,
  "bs": 0.48,
  "ap": 33073.19,
  "as": 0.601,
  "t": 1610462411115,
  "x": 1,
  "r": 1610462411128
}
```
