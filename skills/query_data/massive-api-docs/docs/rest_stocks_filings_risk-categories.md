# Risk Categories

## 源URL

https://massive.com/docs/rest/stocks/filings/risk-categories

## 描述

The full taxonomy used to classify risk factors in the Risk Factors API. This includes the complete set of standardized categories applied across filings.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| taxonomy | number | 否 | Version identifier (e.g., '1.0', '1.1') for the taxonomy Value must be a floating point number. |
| primary_category | string | 否 | Top-level risk category |
| secondary_category | string | 否 | Mid-level risk category |
| tertiary_category | string | 否 | Most specific risk classification |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '200' if not specified. The maximum allowed limit is '999'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'taxonomy' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| description | string | 否 | Detailed explanation of what this risk category encompasses, including specific examples and potential impacts |
| primary_category | string | 否 | Top-level risk category |
| secondary_category | string | 否 | Mid-level risk category |
| taxonomy | number | 否 | Version identifier (e.g., '1.0', '1.1') for the taxonomy |
| tertiary_category | string | 否 | Most specific risk classification |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/taxonomies/vX/risk-factors
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/taxonomies/vX/risk-factors?limit=200&sort=taxonomy.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "daac836f71724420b66011d55d88b30b",
  "results": [
    {
      "description": "Risk from inadequate performance management systems, unclear accountability structures, or ineffective measurement and incentive systems that could affect employee performance, goal achievement, and organizational effectiveness.",
      "primary_category": "Governance & Stakeholder",
      "secondary_category": "Organizational & Management",
      "taxonomy": "1.0",
      "tertiary_category": "Performance management and accountability"
    },
    {
      "description": "Risk from requirements to monitor, document, and report on compliance with privacy and data protection regulations including risks from compliance program effectiveness, record-keeping requirements, and breach notification obligations.",
      "primary_category": "Regulatory & Compliance",
      "secondary_category": "Data & Privacy",
      "taxonomy": "1.0",
      "tertiary_category": "Compliance monitoring and reporting"
    }
  ],
  "status": "OK"
}
```
