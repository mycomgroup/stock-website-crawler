# Trades

## 源URL

https://massive.com/docs/websocket/stocks/trades

## 描述

Stream tick-level trade data for stock tickers via WebSocket. Each message delivers key trade details (price, size, exchange, conditions, and timestamps) as they occur, enabling users to track market activity, power live dashboards, and inform rapid decision-making.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a stock ticker or use * to subscribe to all stock tickers.<br>You can also use a comma separated list to subscribe to multiple stock tickers.<br>You can retrieve available stock tickers from our Stock Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (T) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given stock. |
| x | integer | 否 | The exchange ID. See Exchanges for Massive's mapping of exchange IDs. |
| i | string | 否 | The trade ID. |
| z | integer | 否 | The tape. (1 = NYSE, 2 = AMEX, 3 = Nasdaq). |
| p | number | 否 | The price. |
| s | integer | 否 | The trade size. |
| ds | string | 否 | The trade size including fractional shares, respresented as a string |
| c | array (integer) | 否 | The trade conditions. See Conditions and Indicators for Massive's trade conditions glossary. |
| t | integer | 否 | The SIP timestamp in Unix MS. |
| q | integer | 否 | The sequence number represents the sequence in which message events happened.<br>These are increasing and unique per ticker symbol, but will not always be<br>sequential (e.g., 1, 2, 6, 9, 10, 11). |
| trfi | integer | 否 | The ID for the Trade Reporting Facility where the trade took place. |
| trft | integer | 否 | The TRF (Trade Reporting Facility) Timestamp in Unix MS. <br>This is the timestamp of when the trade reporting facility received this trade. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/stocks

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"T.*"}
```

```json
{
  "ev": "T",
  "sym": "MSFT",
  "x": 4,
  "i": "12345",
  "z": 3,
  "p": 114.125,
  "s": 100,
  "c": [
    0,
    12
  ],
  "t": 1536036818784,
  "q": 3681328
}
```
