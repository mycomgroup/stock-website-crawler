# Inflation

## 源URL

https://massive.com/docs/rest/economy/inflation

## 描述

Retrieve key indicators of realized inflation, reflecting actual changes in consumer prices and spending behavior in the U.S. economy. This endpoint provides both headline and core inflation measures from the CPI and PCE indexes, offering a well-rounded view of historical price trends.

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
| cpi | number | 否 | Consumer Price Index (CPI) for All Urban Consumers — a standard measure of headline inflation based on a fixed basket of goods and services, not seasonally adjusted. |
| cpi_core | number | 否 | Core Consumer Price Index — the CPI excluding food and energy, used to understand underlying inflation trends without short-term volatility. |
| cpi_year_over_year | number | 否 | Year-over-year percentage change in the headline CPI — the most commonly cited inflation rate in public discourse and economic policy. |
| date | string | 否 | Calendar date of the observation (YYYY‑MM‑DD). |
| pce | number | 否 | Personal Consumption Expenditures (PCE) Price Index — a broader measure of inflation used by the Federal Reserve, reflecting actual consumer spending patterns and updated basket weights. |
| pce_core | number | 否 | Core PCE Price Index — excludes food and energy prices from the PCE index, and is the Fed's preferred measure of underlying inflation. |
| pce_spending | number | 否 | Nominal Personal Consumption Expenditures — total dollar value of consumer spending in the U.S. economy, reported in billions of dollars and not adjusted for inflation. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/fed/v1/inflation
```

### Request

```bash
curl -X GET "https://api.massive.com/fed/v1/inflation?limit=100&sort=date.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "cpi": 310.45,
      "cpi_core": 320.1,
      "cpi_year_over_year": 3.18,
      "date": "2025-06-01",
      "pce": 132.73,
      "pce_core": 131.9,
      "pce_spending": 20345.6
    }
  ],
  "status": "OK"
}
```
