# Aggregates (Per Second)

## 源URL

https://massive.com/docs/websocket/stocks/aggregates-per-second

## 描述

Stream second-by-second aggregated OHLC (Open, High, Low, Close) and volume data for specified tickers via WebSocket. These aggregates are updated continuously in Eastern Time (ET) and cover pre-market, regular, and after-hours sessions. Each bar is constructed solely from qualifying trades that meet specific conditions; if no eligible trades occur within a given minute, no bar is emitted. By providing a steady flow of aggregate bars, this endpoint enables users to track intraday price movements, refine trading strategies, and power live data visualizations.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a stock ticker or use * to subscribe to all stock tickers.<br>You can also use a comma separated list to subscribe to multiple stock tickers.<br>You can retrieve available stock tickers from our Stock Tickers API. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ev | enum (A) | 否 | The event type. |
| sym | string | 否 | The ticker symbol for the given stock. |
| v | integer | 否 | The tick volume. |
| dv | string | 否 | The tick volume including fractional shares, respresented as a string decimal number |
| av | integer | 否 | Today's accumulated volume. |
| dav | string | 否 | Today's accumulated volume including fractional shares, respresented as a string decimal number |
| op | number | 否 | Today's official opening price. |
| vw | number | 否 | The tick's volume weighted average price. |
| o | number | 否 | The opening tick price for this aggregate window. |
| c | number | 否 | The closing tick price for this aggregate window. |
| h | number | 否 | The highest tick price for this aggregate window. |
| l | number | 否 | The lowest tick price for this aggregate window. |
| a | number | 否 | Today's volume weighted average price. |
| z | integer | 否 | The average trade size for this aggregate window. |
| s | integer | 否 | The start timestamp of this aggregate window in Unix Milliseconds. |
| e | integer | 否 | The end timestamp of this aggregate window in Unix Milliseconds. |
| otc | boolean | 否 | Whether or not this aggregate is for an OTC ticker. This field will be left off if false. |

## 代码示例

### Websocket

```text
# Connect to the websocket
npx wscat -c wss://delayed.massive.com/stocks

# Authenticate
{"action":"auth","params":"YOUR_API_KEY"}

# Subscribe to the topic
{"action":"subscribe", "params":"A.*"}
```

```json
{
  "ev": "A",
  "sym": "SPCE",
  "v": 200,
  "av": 8642007,
  "op": 25.66,
  "vw": 25.3981,
  "o": 25.39,
  "c": 25.39,
  "h": 25.39,
  "l": 25.39,
  "a": 25.3714,
  "z": 50,
  "s": 1610144868000,
  "e": 1610144869000
}
```
