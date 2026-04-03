# Previous Day Bar (OHLC)

## 源URL

https://massive.com/docs/rest/indices/aggregates/previous-day-bar

## 描述

Retrieve the previous trading day's open, high, low, and close (OHLC) data for a specified index ticker. This endpoint provides key pricing metrics, including volume, to help users assess recent performance and inform trading strategies.

## Endpoint

```
GET /v2/aggs/ticker/{indicesTicker}/prev
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| indicesTicker | string | 否 | The ticker symbol of Index. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The exchange symbol that this item is traded under. |
| queryCount | integer | 否 | The number of aggregates (minute or day) used to generate the response. |
| request_id | string | 否 | A request id assigned by the server. |
| resultsCount | integer | 否 | The total number of results for this request. |
| status | string | 否 | The status of this request's response. |
| results | array (object) | 否 | An array of results containing the requested data. |
| c | number | 否 | The close value for the symbol in the given time period. |
| h | number | 否 | The highest value for the symbol in the given time period. |
| l | number | 否 | The lowest value for the symbol in the given time period. |
| o | number | 否 | The open value for the symbol in the given time period. |
| t | integer | 否 | The Unix millisecond timestamp for the start of the aggregate window. |

## 代码示例

```text
/v2/aggs/ticker/{indicesTicker}/prev
```

### Request

```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/I:NDX/prev?apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "queryCount": 1,
  "request_id": "b2170df985474b6d21a6eeccfb6bee67",
  "results": [
    {
      "T": "I:NDX",
      "c": 15070.14948566977,
      "h": 15127.4195807999,
      "l": 14946.7243781848,
      "o": 15036.48391066877,
      "t": 1687291200000
    }
  ],
  "resultsCount": 1,
  "status": "OK",
  "ticker": "I:NDX"
}
```
