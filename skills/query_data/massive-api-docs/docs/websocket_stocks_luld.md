# Limit Up - Limit Down (LULD)

## 源URL

https://massive.com/docs/websocket/stocks/luld

## 描述

Stream real-time Limit Up - Limit Down (LULD) events for specified stock tickers via WebSocket across multiple U.S. exchanges (including NYSE, Nasdaq, Cboe BZX, NYSE Arca, and NYSE American). Events signal when securities approach or breach dynamic price bands, triggering pauses, halts, or resumptions to curb volatility. Halt and resumption messages (indicators 17 and 18) are only available for NASDAQ listed securities. This high-volume feed provides continuous intraday coverage during regular trading hours, with details on price limits, indicators, and timestamps for proactive market response.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a stock ticker or use * to subscribe to all stock tickers.<br>You can also use a comma separated list to subscribe to multiple stock tickers.<br>You can retrieve available stock tickers from our Stock Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (LULD) | 否 | The event type. |
| T | string | 否 | The ticker symbol for the given stock. |
| h | number | 否 | The high price. |
| l | number | 否 | The low price. |
| i | array (integer) | 否 | The Indicators. See Conditions and Indicators for a glossary (LULD indicators are located near the bottom). |
| z | integer | 否 | The tape. (1 = NYSE, 2 = AMEX, 3 = Nasdaq). |
| t | integer | 否 | The Timestamp in Unix MS. |
| q | integer | 否 | The sequence number represents the sequence in which message events happened.<br>These are increasing and unique per ticker symbol, but will not always be<br>sequential (e.g., 1, 2, 6, 9, 10, 11). |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://socket.massive.com/stocks

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"LULD.*"}
```

```json
{
  "ev": "LULD",
  "T": "MSFT",
  "h": 492.99,
  "l": 446.04,
  "i": [
    16
  ],
  "z": 3,
  "t": 1764086430905642800,
  "q": 5925769
}
```
