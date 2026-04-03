# Quotes

## 源URL

https://massive.com/docs/websocket/options/quotes

## 描述

Stream quote data for specified options contracts via WebSocket. Each message delivers current best bid/ask prices, sizes, and associated metadata as they update, enabling users to monitor dynamic market conditions and inform trading decisions. Due to the high bandwidth and message rates associated with options quotes, users can subscribe to a maximum of 1,000 option contracts per connection.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify an option contract. You're only allowed to subscribe to 1,000 option contracts per connection.<br>You can also use a comma separated list to subscribe to multiple option contracts.<br>You can retrieve active options contracts from our Options Contracts API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (Q) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given option contract. |
| bx | integer | 否 | The bid exchange ID. See Exchanges for Massive's mapping of exchange IDs. |
| ax | integer | 否 | The ask exchange ID. See Exchanges for Massive's mapping of exchange IDs. |
| bp | number | 否 | The bid price. |
| ap | number | 否 | The ask price. |
| bs | integer | 否 | The bid size. |
| as | integer | 否 | The ask size. |
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
{"action":"subscribe", "params":"Q.O:SPY251219C00650000"}
```

```json
{
  "ev": "Q",
  "sym": "O:SPY241220P00720000",
  "bx": 302,
  "ax": 302,
  "bp": 9.71,
  "ap": 9.81,
  "bs": 17,
  "as": 24,
  "t": 1644506128351,
  "q": 844090872
}
```
