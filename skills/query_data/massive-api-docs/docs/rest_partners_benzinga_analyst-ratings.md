# Analyst Ratings

## 源URL

https://massive.com/docs/rest/partners/benzinga/analyst-ratings

## 描述

Retrieve structured historical analyst ratings, including rating actions, price target changes, and firm names for publicly traded companies. Each record captures key attributes such as the rating date, action type (e.g., downgrade, maintain), and firm issuing the rating, along with optional price target changes and surprise indicators. Data can be filtered by ticker, firm, rating action, and date range. Price targets are optionally adjusted for corporate actions like splits and dividends. Records are timestamped and sortable for flexible integration into downstream applications.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| date | string | 否 | The calendar date (formatted as YYYY-MM-DD) when the rating was issued. |
| ticker | string | 否 | The stock symbol of the company being rated. |
| importance | integer | 否 | A subjective indicator of the importance of the earnings event, on a scale from 0 (lowest) to 5 (highest). Value must be an integer. |
| last_updated | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the rating was last updated in the system. Value must be an integer timestamp in seconds, formatted 'yyyy-mm-dd', or ISO 8601/RFC 3339 (e.g. '2024-05-28T20:27:41Z'). |
| rating_action | string | 否 | The description of the change in rating from the firm's last rating. Possible values include: downgrades, maintains, reinstates, reiterates, upgrades, assumes, initiates_coverage_on, terminates_coverage_on, removes, suspends, firm_dissolved. |
| price_target_action | string | 否 | The description of the directional change in price target. Possible values include: raises, lowers, maintains, announces, sets. |
| benzinga_id | string | 否 | The identifer used by Benzinga for this record. |
| benzinga_analyst_id | string | 否 | The identifer used by Benzinga for this analyst. |
| benzinga_firm_id | string | 否 | The identifer used by Benzinga for this firm. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'last_updated' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| adjusted_price_target | number | 否 | The current price target adjusted for stock splits and dividends. |
| analyst | string | 否 | The name of the individual analyst who issued the rating. |
| benzinga_analyst_id | string | 否 | The identifer used by Benzinga for this analyst. |
| benzinga_calendar_url | string | 否 | A link to the Benzinga calendar page for this ticker |
| benzinga_firm_id | string | 否 | The identifer used by Benzinga for this firm. |
| benzinga_id | string | 否 | The identifer used by Benzinga for this record. |
| benzinga_news_url | string | 否 | A link to the Benzinga articles page for this ticker |
| company_name | string | 否 | The name of the company being rated. |
| currency | string | 否 | The ISO 4217 currency code in which the price target is denominated. |
| date | string | 否 | The calendar date (formatted as YYYY-MM-DD) when the rating was issued. |
| firm | string | 否 | The name of the research firm or investment bank issuing the rating. |
| importance | integer | 否 | A subjective indicator of the importance of the earnings event, on a scale from 0 (lowest) to 5 (highest). |
| last_updated | string | 否 | The timestamp (formatted as an ISO 8601 timestamp) when the rating was last updated in the system. |
| notes | string | 否 | Additional context or commentary. |
| previous_adjusted_price_target | number | 否 | The previous price target adjusted for stock splits and dividends. |
| previous_price_target | number | 否 | The previous price target set by the analyst. |
| previous_rating | string | 否 | The previous rating set by the analyst. |
| price_percent_change | number | 否 | The percentage change in price target if price target and previous price target exists |
| price_target | number | 否 | The current price target set by the analyst. |
| price_target_action | string | 否 | The description of the directional change in price target. Possible values include: raises, lowers, maintains, announces, sets. |
| rating | string | 否 | The current rating set by the analyst. |
| rating_action | string | 否 | The description of the change in rating from the firm's last rating. Possible values include: downgrades, maintains, reinstates, reiterates, upgrades, assumes, initiates_coverage_on, terminates_coverage_on, removes, suspends, firm_dissolved. |
| ticker | string | 否 | The stock symbol of the company being rated. |
| time | string | 否 | The time (formatted as 24-hour HH:MM:SS UTC) when the rating was issued. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/benzinga/v1/ratings
```

### Request

```bash
curl -X GET "https://api.massive.com/benzinga/v1/ratings?limit=100&sort=last_updated.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "adjusted_price_target": 15,
      "analyst": "Alexander Potter",
      "benzinga_analyst_id": "58933b2043eaaa0001698f4a",
      "benzinga_calendar_url": "https://www.benzinga.com/quote/RIVN/analyst-ratings",
      "benzinga_firm_id": "5e147c6b7da4190001b287b4",
      "benzinga_id": "682f29b0e5343b000100a619",
      "benzinga_news_url": "https://www.benzinga.com/stock-articles/RIVN/analyst-ratings",
      "company_name": "Rivian Automotive",
      "currency": "USD",
      "date": "2025-05-22",
      "firm": "Piper Sandler",
      "importance": 0,
      "last_updated": "2025-05-22T13:42:30Z",
      "previous_adjusted_price_target": 13,
      "previous_price_target": 13,
      "previous_rating": "neutral",
      "price_percent_change": 15.38,
      "price_target": 15,
      "price_target_action": "raises",
      "rating": "neutral",
      "rating_action": "maintains",
      "ticker": "RIVN",
      "time": "09:42:08"
    }
  ],
  "status": "OK"
}
```
