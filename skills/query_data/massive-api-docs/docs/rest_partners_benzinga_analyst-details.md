# Analyst Details

## 源URL

https://massive.com/docs/rest/partners/benzinga/analyst-details

## 描述

Retrieve structured data on financial analysts, including names, affiliated firms, and historical rating activity. Each record includes performance metrics such as success rate, average return, and percentile rankings. This data provides transparency into the analysts behind equity ratings and enables deeper evaluation of their track records.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| benzinga_id | string | 否 | The identifier used by Benzinga for this record. |
| benzinga_firm_id | string | 否 | The unique identifier assigned by Benzinga to the research firm or investment bank. |
| firm_name | string | 否 | The name of the research firm or investment bank issuing the ratings. |
| full_name | string | 否 | The full name of the analyst associated with the ratings. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'full_name' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| benzinga_firm_id | string | 否 | The unique identifier assigned by Benzinga to the research firm or investment bank. |
| benzinga_id | string | 否 | The identifier used by Benzinga for this record. |
| firm_name | string | 否 | The name of the research firm or investment bank issuing the ratings. |
| full_name | string | 否 | The full name of the analyst associated with the ratings. |
| last_updated | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the analyst record was last updated in the system. |
| overall_avg_return | number | 否 | The average percent price difference per rating since the date of recommendation. |
| overall_avg_return_percentile | number | 否 | The analyst's percentile rank based on average return, relative to other analysts. |
| overall_success_rate | number | 否 | The percentage of gain/loss ratings that resulted in a gain overall. |
| smart_score | number | 否 | A weighted average of the total_ratings_percentile, overall_avg_return_percentile, and overall_success_rate. |
| total_ratings | number | 否 | The total number of ratings issued by the analyst included in the performance calculation. |
| total_ratings_percentile | number | 否 | The analyst's percentile rank based on the total number of ratings issued, relative to other analysts. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/benzinga/v1/analysts
```

### Request

```bash
curl -X GET "https://api.massive.com/benzinga/v1/analysts?limit=100&sort=full_name.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "benzinga_firm_id": "5e17143f7da4190001b2eaa6",
      "benzinga_id": "65eb18289b25ca0001b34332",
      "firm_name": "B of A Securities",
      "full_name": "Alice Xiao",
      "last_updated": "2025-05-19T04:31:12Z",
      "overall_avg_return": 12.48,
      "overall_avg_return_percentile": 66.53,
      "overall_success_rate": 100,
      "smart_score": 67.94,
      "total_ratings": 4,
      "total_ratings_percentile": 32.17
    }
  ],
  "status": "OK"
}
```
