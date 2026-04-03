# Custom Bars (OHLC)

## 源URL

https://massive.com/docs/rest/crypto/aggregates/custom-bars

## 描述

Retrieve aggregated historical OHLC (Open, High, Low, Close) and volume data for a specified cryptocurrency pair over a custom date range and time interval in Coordinated Universal Time (UTC). These aggregates are derived from qualifying crypto trades that meet specific conditions. If no eligible trades occur within a given timeframe, no aggregate bar is generated, resulting in an empty interval that transparently indicates a period without trading activity. Users can adjust the multiplier and timespan parameters (e.g., a 5-minute bar) to tailor their analysis. This flexibility supports a wide range of analytical and visualization needs within the crypto markets.

## Endpoint

```
GET /v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| cryptoTicker | string | 否 | The ticker symbol of the currency pair. |
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
/v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}
```

### Request

```bash
curl -X GET "https://api.massive.com/v2/aggs/ticker/X:BTCUSD/range/1/day/2025-11-03/2025-11-28?adjusted=true&sort=asc&limit=120&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "adjusted": true,
  "queryCount": 2,
  "request_id": "0cf72b6da685bcd386548ffe2895904a",
  "results": [
    {
      "c": 10094.75,
      "h": 10429.26,
      "l": 9490,
      "n": 1,
      "o": 9557.9,
      "t": 1590984000000,
      "v": 303067.6562332156,
      "vw": 9874.5529
    },
    {
      "c": 9492.62,
      "h": 10222.72,
      "l": 9135.68,
      "n": 1,
      "o": 10096.87,
      "t": 1591070400000,
      "v": 323339.6922892879,
      "vw": 9729.5701
    }
  ],
  "resultsCount": 2,
  "status": "OK",
  "ticker": "X:BTCUSD"
}
```
