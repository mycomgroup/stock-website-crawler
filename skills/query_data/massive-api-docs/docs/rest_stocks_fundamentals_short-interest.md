# Short Interest

## 源URL

https://massive.com/docs/rest/stocks/fundamentals/short-interest

## 描述

Retrieve bi-monthly aggregated short interest data reported to FINRA by broker-dealers for a specified stock ticker. Short interest represents the total number of shares sold short but not yet covered or closed out, serving as an indicator of market sentiment and potential price movements. High short interest can signal bearish sentiment or highlight opportunities such as potential short squeezes. This endpoint provides essential insights for investors monitoring market positioning and sentiment.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The primary ticker symbol for the stock. |
| days_to_cover | number | 否 | Calculated as short_interest divided by avg_daily_volume, representing the estimated number of days it would take to cover all short positions based on average trading volume. Value must be a floating point number. |
| settlement_date | string | 否 | The date (formatted as YYYY-MM-DD) on which the short interest data is considered settled, typically based on exchange reporting schedules. |
| avg_daily_volume | integer | 否 | The average daily trading volume for the stock over a specified period, typically used to contextualize short interest. Value must be an integer. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '10' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| avg_daily_volume | integer | 否 | The average daily trading volume for the stock over a specified period, typically used to contextualize short interest. |
| days_to_cover | number | 否 | Calculated as short_interest divided by avg_daily_volume, representing the estimated number of days it would take to cover all short positions based on average trading volume. |
| settlement_date | string | 否 | The date (formatted as YYYY-MM-DD) on which the short interest data is considered settled, typically based on exchange reporting schedules. |
| short_interest | integer | 否 | The total number of shares that have been sold short but have not yet been covered or closed out. |
| ticker | string | 否 | The primary ticker symbol for the stock. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/v1/short-interest
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/v1/short-interest?limit=10&sort=ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "avg_daily_volume": 2340158,
      "days_to_cover": 1.67,
      "settlement_date": "2025-03-14",
      "short_interest": 3906231,
      "ticker": "A"
    }
  ],
  "status": "OK"
}
```
