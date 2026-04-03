# Previous Day Bar (OHLC)

## 源URL

https://massive.com/docs/rest/forex/aggregates/previous-day-bar

## 描述

Retrieve the previous trading day's open, high, low, and close (OHLC) data for a specified forex pair. This endpoint provides key pricing metrics, including volume, to help users assess recent performance and inform trading strategies.

## Endpoint

```
GET /v2/aggs/ticker/{forexTicker}/prev
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| forexTicker | string | 否 | The ticker symbol of the currency pair. |
| adjusted | boolean | 否 | Whether or not the results are adjusted for splits.  By default, results are adjusted.<br>Set this to false to get results that are NOT adjusted for splits. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The exchange symbol that this item is traded under. |
| adjusted | boolean | 否 | Whether or not this response was adjusted for splits. |
| queryCount | integer | 否 | The number of aggregates (minute or day) used to generate the response. |
| request_id | string | 否 | A request id assigned by the server. |
| resultsCount | integer | 否 | The total number of results for this request. |
| status | string | 否 | The status of this request's response. |
| results | array (object) | 否 | An array of results containing the requested data. |
| T | string | 否 | The exchange symbol that this item is traded under. |
| c | number | 否 | The close price for the symbol in the given time period. |
| h | number | 否 | The highest price for the symbol in the given time period. |
| l | number | 否 | The lowest price for the symbol in the given time period. |
| n | integer | 否 | The number of transactions in the aggregate window. |
| o | number | 否 | The open price for the symbol in the given time period. |
| t | integer | 否 | The Unix millisecond timestamp for the start of the aggregate window. |
| v | number | 否 | The trading volume of the symbol in the given time period. |
| vw | number | 否 | The volume weighted average price. |

## 代码示例

```text
/v2/aggs/ticker/{forexTicker}/prev
```

### Request

```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/C:EURUSD/prev?adjusted=true&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "adjusted": true,
  "queryCount": 1,
  "request_id": "08ec061fb85115678d68452c0a609cb7",
  "results": [
    {
      "T": "C:EURUSD",
      "c": 1.06206,
      "h": 1.0631,
      "l": 1.0505,
      "n": 180300,
      "o": 1.05252,
      "t": 1651708799999,
      "v": 180300,
      "vw": 1.055
    }
  ],
  "resultsCount": 1,
  "status": "OK",
  "ticker": "C:EURUSD"
}
```
