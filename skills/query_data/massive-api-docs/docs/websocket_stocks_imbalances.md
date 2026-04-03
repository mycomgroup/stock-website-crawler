# Net Order Imbalance (NOI)

## 源URL

https://massive.com/docs/websocket/stocks/imbalances

## 描述

Stream real-time Net Order Imbalance (NOI) events for specified stock tickers via WebSocket. Focused on NYSE listed securities, this feed delivers updates on buy and sell order imbalances during scheduled exchange auctions. Typically, at market open (9:30 AM ET) and close (4:00 PM ET), along with indicative clearing prices, paired quantities, and imbalance amounts. Intraday events may also occur during ticker specific halts or mini-auctions, offering insights into liquidity pressures and auction dynamics.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a stock ticker or use * to subscribe to all stock tickers.<br>You can also use a comma separated list to subscribe to multiple stock tickers.<br>You can retrieve available stock tickers from our Stock Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (NOI) | 否 | The event type. |
| T | string | 否 | The ticker symbol for the given stock. |
| t | integer | 否 | The Timestamp in Unix MS. |
| at | integer | 否 | The time that the auction is planned to take place in the format (hour x 100) + minutes in Eastern Standard Time, <br>for example 930 would be 9:30 am EST, and 1600 would be 4:00 pm EST. |
| a | string | 否 | The auction type.<br>`O` - Early Opening Auction (non-NYSE only)<br>`M` - Core Opening Auction<br>`H` - Reopening Auction (Halt Resume)<br>`C` - Closing Auction<br>`P` - Extreme Closing Imbalance (NYSE only)<br>`R` - Regulatory Closing Imbalance (NYSE only) |
| i | integer | 否 | The symbol sequence. |
| x | integer | 否 | The exchange ID. See Exchanges for Massive's mapping of exchange IDs. |
| o | integer | 否 | The imbalance quantity. |
| p | integer | 否 | The paired quantity. |
| b | number | 否 | The book clearing price. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://socket.massive.com/stocks

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"NOI.*"}
```

```json
{
  "ev": "NOI",
  "T": "NTEST.Q",
  "t": 1601318039223013600,
  "at": 930,
  "a": "M",
  "i": 44,
  "x": 10,
  "o": 480,
  "p": 440,
  "b": 25.03
}
```
