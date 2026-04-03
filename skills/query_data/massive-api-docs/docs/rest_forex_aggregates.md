# Custom Bars (OHLC)

## 源URL

https://massive.com/docs/rest/forex/aggregates

## 描述

Retrieve aggregated historical OHLC (Open, High, Low, Close) and volume data for a specified Forex currency pair over a custom date range and time interval in Eastern Time (ET). Unlike stocks or options, these aggregates are generated from quoted bid/ask prices rather than executed trades. If no new quotes occur during a given timeframe, no aggregate bar is produced, resulting in an empty interval that transparently indicates a period without quote updates. Users can customize their data by adjusting the multiplier and timespan parameters (e.g., a 5-minute bar), covering various trading sessions. This approach supports a range of analytical and visualization needs in the Forex market.

## Endpoint

```
GET /v2/aggs/ticker/{forexTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| forexTicker | string | 否 | The ticker symbol of the currency pair. |
| multiplier | integer | 否 | The size of the timespan multiplier. |
| timespan | enum (string) | 否 | The size of the time window. |
| from | string | 否 | The start of the aggregate time window. Either a date with the format YYYY-MM-DD or a millisecond timestamp. |
| to | string | 否 | The end of the aggregate time window. Either a date with the format YYYY-MM-DD or a millisecond timestamp. |
| adjusted | boolean | 否 | Whether or not the results are adjusted for splits.  By default, results are adjusted.<br>Set this to false to get results that are NOT adjusted for splits. |
| sort | enum (string) | 否 | Sort the results by timestamp.<br>`asc` will return results in ascending order (oldest at the top),<br>`desc` will return results in descending order (newest at the top). |
| limit | integer | 否 | Limits the number of base aggregates queried to create the aggregate results. Max 50000 and Default 5000.<br>Read more about how limit is used to calculate aggregate results in our article on<br>Aggregate Data API Improvements. |

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
/v2/aggs/ticker/{forexTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

### Request

```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/C:EURUSD/range/1/day/2025-11-03/2025-11-28?adjusted=true&sort=asc&limit=120&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "adjusted": true,
  "queryCount": 1,
  "request_id": "79c061995d8b627b736170bc9653f15d",
  "results": [
    {
      "c": 1.17721,
      "h": 1.18305,
      "l": 1.1756,
      "n": 125329,
      "o": 1.17921,
      "t": 1626912000000,
      "v": 125329,
      "vw": 1.1789
    }
  ],
  "resultsCount": 1,
  "status": "OK",
  "ticker": "C:EURUSD"
}
```
