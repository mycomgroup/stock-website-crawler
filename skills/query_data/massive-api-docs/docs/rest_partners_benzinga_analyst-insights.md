# Analyst Insights

## 源URL

https://massive.com/docs/rest/partners/benzinga/analyst-insights

## 描述

Retrieve insights from financial analysts, including ratings, price targets, and the rationale behind their recommendations. Each record captures key drivers such as valuation metrics, strategic initiatives, and sector positioning. This data offers a structured view of analyst sentiment over time and supports deeper analysis of company outlook and market expectations.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| date | string | 否 | The calendar date (formatted as YYYY-MM-DD) when the rating was issued. |
| ticker | string | 否 | The stock symbol of the company being rated. |
| last_updated | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the rating was last updated in the system. Value must be an integer timestamp in seconds, formatted 'yyyy-mm-dd', or ISO 8601/RFC 3339 (e.g. '2024-05-28T20:27:41Z'). |
| firm | string | 否 | The name of the research firm or investment bank issuing the rating. |
| rating_action | string | 否 | The description of the change in rating from the firm's last rating. Possible values include: downgrades, maintains, reinstates, reiterates, upgrades, assumes, initiates_coverage_on, terminates_coverage_on, removes, suspends, firm_dissolved. |
| benzinga_firm_id | string | 否 | The identifer used by Benzinga for the firm record. |
| benzinga_rating_id | string | 否 | The identifier used by Benzinga for the rating record. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'last_updated' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| benzinga_firm_id | string | 否 | The identifer used by Benzinga for the firm record. |
| benzinga_id | string | 否 | The identifer used by Benzinga for this record. |
| benzinga_rating_id | string | 否 | The identifier used by Benzinga for the rating record. |
| company_name | string | 否 | The name of the company being rated. |
| date | string | 否 | The calendar date (formatted as YYYY-MM-DD) when the rating was issued. |
| firm | string | 否 | The name of the research firm or investment bank issuing the rating. |
| insight | string | 否 | Narrative commentary or reasoning provided by the analyst or firm to explain the rating or price target. |
| last_updated | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the rating was last updated in the system. |
| price_target | number | 否 | The current price target set by the analyst. |
| rating | string | 否 | The current rating set by the analyst. |
| rating_action | string | 否 | The description of the change in rating from the firm's last rating. Possible values include: downgrades, maintains, reinstates, reiterates, upgrades, assumes, initiates_coverage_on, terminates_coverage_on, removes, suspends, firm_dissolved. |
| ticker | string | 否 | The stock symbol of the company being rated. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/benzinga/v1/analyst-insights
```

### Request

```bash
curl -X GET "https://api.massive.com/benzinga/v1/analyst-insights?limit=100&sort=last_updated.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "benzinga_firm_id": "606af0aa6538960001bced21",
      "benzinga_id": "681363c1fd0258abcbedc074",
      "benzinga_rating_id": "6813624c09c1f6000103ac25",
      "date": "2025-05-01",
      "firm": "Needham",
      "insight": "Needham maintained their Buy rating on Etsy's stock with a price target of $55.00.  \n\n **Growth Initiatives and Market Penetration**: Etsy's focus on growth initiatives, including leveraging its app for a more personalized shopping experience and marketing, has been a key factor in maintaining its Buy rating. The company's ability to drive greater consideration and purchase frequency through technology and product initiatives, alongside its significant app penetration of gross merchandise sales (GMS), showcases its strong position to capture more of the consumer wallet.\n\n**Resilience Amid Economic Uncertainty**: Despite the economic uncertainty, including potential impacts from tariffs, Etsy's asset-light model and strategic focus on product enhancements position it to navigate macro headwinds effectively. The company's efforts to lean into paid social channels for marketing and its ability to adapt to changes in consumer behavior underline its resilience and potential for sustained growth, supporting the Buy rating.",
      "last_updated": "2025-05-01T12:06:36Z",
      "price_target": 55,
      "rating": "buy",
      "rating_action": "maintains"
    }
  ],
  "status": "OK"
}
```
