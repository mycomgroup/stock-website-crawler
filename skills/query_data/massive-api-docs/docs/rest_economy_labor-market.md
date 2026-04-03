# Labor Market

## 源URL

https://massive.com/docs/rest/economy/labor-market

## 描述

Retrieve key labor market indicators from the Federal Reserve, including unemployment rate, labor force participation, average hourly earnings, and job openings data.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| date | string | 否 | Calendar date of the observation (YYYY-MM-DD). |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'date' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| avg_hourly_earnings | number | 否 | Average hourly earnings of all employees on private nonfarm payrolls in USD (CES0500000003 series from FRED). |
| date | string | 否 | Calendar date of the observation (YYYY-MM-DD). |
| job_openings | number | 否 | Total nonfarm job openings in thousands (JTSJOL series from FRED). |
| labor_force_participation_rate | number | 否 | Civilian labor force participation rate as a percentage of the civilian noninstitutional population (CIVPART series from FRED). |
| unemployment_rate | number | 否 | Civilian unemployment rate as a percentage of the labor force (UNRATE series from FRED). |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/fed/v1/labor-market
```

### Request

```bash
curl -X GET "https://api.massive.com/fed/v1/labor-market?limit=100&sort=date.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "avg_hourly_earnings": 35.06,
      "date": "2024-12-01",
      "job_openings": 8098,
      "labor_force_participation_rate": 62.5,
      "unemployment_rate": 4.2
    }
  ],
  "status": "OK"
}
```
