# Custom Bars (OHLC)

## 源URL

https://massive.com/docs/rest/indices/aggregates/custom-bars

## 描述

Retrieve aggregated historical OHLC (Open, High, Low, Close) and value data for a specified index over a custom date range and time interval in Eastern Time (ET). Unlike stocks or options, these aggregates are derived from index values rather than individual trades, reflecting the performance of a market segment, sector, or benchmark. If no index updates occur within a given timeframe, no aggregate bar is produced, resulting in an empty interval that indicates a period without new index data. Users can customize their view by adjusting the multiplier and timespan parameters (e.g., a 5-minute interval). This approach supports various analytical and visualization needs related to broad market or sector performance.

## Endpoint

```
GET /v2/aggs/ticker/{indicesTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| indicesTicker | string | 否 | The ticker symbol of Index. |
| multiplier | integer | 否 | The size of the timespan multiplier. |
| timespan | enum (string) | 否 | The size of the time window. |
| from | string | 否 | The start of the aggregate time window. Either a date with the format YYYY-MM-DD or a millisecond timestamp. |
| to | string | 否 | The end of the aggregate time window. Either a date with the format YYYY-MM-DD or a millisecond timestamp. |
| sort | enum (string) | 否 | Sort the results by timestamp.<br>`asc` will return results in ascending order (oldest at the top),<br>`desc` will return results in descending order (newest at the top). |
| limit | integer | 否 | Limits the number of base aggregates queried to create the aggregate results. Max 50000 and Default 5000.<br>Read more about how limit is used to calculate aggregate results in our article on<br>Aggregate Data API Improvements. |

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
/v2/aggs/ticker/{indicesTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

### Request

```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/I:NDX/range/1/day/2025-11-03/2025-11-28?sort=asc&limit=120&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 2,
  "queryCount": 2,
  "request_id": "0cf72b6da685bcd386548ffe2895904a",
  "results": [
    {
      "c": 11995.88235998666,
      "h": 12340.44936267155,
      "l": 11970.34221717375,
      "o": 12230.83658266843,
      "t": 1678341600000
    },
    {
      "c": 11830.28178808306,
      "h": 12069.62262033557,
      "l": 11789.85923449393,
      "o": 12001.69552583921,
      "t": 1678428000000
    }
  ],
  "status": "OK",
  "ticker": "I:NDX"
}
```
