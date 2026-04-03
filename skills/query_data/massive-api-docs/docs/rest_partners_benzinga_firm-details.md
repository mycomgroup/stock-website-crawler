# Firm Details

## 源URL

https://massive.com/docs/rest/partners/benzinga/firm-details

## 描述

Retrieve structured data on analyst firms, including firm names and identifiers. Each record can be linked to associated analysts and ratings to provide context around the sources of equity research. This dataset helps map coverage across institutions and supports analysis of firm-level activity in the market.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| benzinga_id | string | 否 | The identifer used by Benzinga for this record. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'name' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| benzinga_id | string | 否 | The identifer used by Benzinga for this record. |
| currency | string | 否 | Primary currency used by the financial firm, with some entries having null values. |
| last_updated | string | 否 | Timestamp indicating when the firm's information was last modified or verified in the database. |
| name | string | 否 | The name of a research firm or investment bank which issues ratings. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/benzinga/v1/firms
```

### Request

```bash
curl -X GET "https://api.massive.com/benzinga/v1/firms?limit=100&sort=name.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "benzinga_id": "5e147c6b7da4190001b287b4",
      "currency": "USD",
      "last_updated": "2020-01-07T12:41:25Z",
      "name": "Piper Sandler"
    }
  ],
  "status": "OK"
}
```
