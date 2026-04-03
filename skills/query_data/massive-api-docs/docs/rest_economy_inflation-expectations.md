# Inflation Expectations

## 源URL

https://massive.com/docs/rest/economy/inflation-expectations

## 描述

Retrieve a broad view of how inflation is expected to evolve over time in the U.S. economy. This endpoint combines signals from financial markets and economic models to capture both near-term and long-term inflation outlooks. Each data point helps contextualize how inflation risk is perceived by investors and forecasters across different time horizons.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| date | string | 否 | Calendar date of the observation (YYYY‑MM‑DD). |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'date' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| date | string | 否 | Calendar date of the observation (YYYY‑MM‑DD). |
| forward_years_5_to_10 | number | 否 | 5-Year, 5-Year Forward Inflation Expectation Rate — the market's expectation of average annual inflation for the 5-year period beginning 5 years from now, based on the spread between forward nominal and real yields. |
| market_10_year | number | 否 | 10-Year Breakeven Inflation Rate — the market's expectation of average annual inflation over the next 10 years, based on the spread between 10-year nominal Treasury yields and 10-year TIPS yields. |
| market_5_year | number | 否 | 5-Year Breakeven Inflation Rate — the market's expectation of average annual inflation over the next 5 years, based on the spread between 5-year nominal Treasury yields and 5-year TIPS yields. |
| model_10_year | number | 否 | The Cleveland Fed’s 10-year inflation expectations data estimated expected inflation, risk premiums, and the real interest rate using a model based on Treasury yields, inflation data, swaps, and surveys. |
| model_1_year | number | 否 | The Cleveland Fed’s 1-year inflation expectations data estimated expected inflation, risk premiums, and the real interest rate using a model based on Treasury yields, inflation data, swaps, and surveys. |
| model_30_year | number | 否 | The Cleveland Fed’s 30-year inflation expectations data estimated expected inflation, risk premiums, and the real interest rate using a model based on Treasury yields, inflation data, swaps, and surveys. |
| model_5_year | number | 否 | The Cleveland Fed’s 5-year inflation expectations data estimated expected inflation, risk premiums, and the real interest rate using a model based on Treasury yields, inflation data, swaps, and surveys. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/fed/v1/inflation-expectations
```

### Request

```bash
curl -X GET "https://api.massive.com/fed/v1/inflation-expectations?limit=100&sort=date.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "date": "2025-06-17",
      "forward_years_5_to_10": 2.6,
      "market_10_year": 2.36,
      "market_5_year": 2.12,
      "model_10_year": 2.95,
      "model_1_year": 2.85,
      "model_30_year": 3,
      "model_5_year": 2.91
    }
  ],
  "status": "OK"
}
```
