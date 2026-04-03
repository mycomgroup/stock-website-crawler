# Custom Bars (OHLC)

## 源URL

https://massive.com/docs/rest/options/aggregates

## 描述

Retrieve aggregated historical OHLC (Open, High, Low, Close) and volume data for a specified options contract over a custom date range and time interval in Eastern Time (ET). Aggregates are derived exclusively from qualifying trades that meet specific conditions. If no eligible trades occur within a given timeframe, no aggregate bar is produced, resulting in an empty interval that indicates a lack of trading activity during that period. Users can tailor their data by adjusting the multiplier and timespan parameters (e.g., a 5-minute bar). This flexibility supports a broad range of analytical and visualization needs for options markets.

## Endpoint

```
GET /v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| optionsTicker | string | 否 | The ticker symbol of the options contract. |
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
/v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

### Request

```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/O:SPY251219C00650000/range/1/day/2025-11-03/2025-11-28?adjusted=true&sort=asc&limit=120&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "adjusted": true,
  "count": 2,
  "queryCount": 2,
  "request_id": "5585acde-5085-42d6-95b2-2e388a28370a",
  "results": [
    {
      "c": 26.2,
      "h": 26.2,
      "l": 26.2,
      "n": 1,
      "o": 26.2,
      "t": 1632369600000,
      "v": 2,
      "vw": 26.2
    },
    {
      "c": 28.3,
      "h": 28.3,
      "l": 28.3,
      "n": 1,
      "o": 28.3,
      "t": 1632456000000,
      "v": 2,
      "vw": 28.3
    }
  ],
  "resultsCount": 2,
  "status": "OK",
  "ticker": "O:RDFN211119C00025000"
}
```
