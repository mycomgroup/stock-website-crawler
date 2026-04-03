# Corporate Events

## 源URL

https://massive.com/docs/rest/partners/tmx/corporate-events

## 描述

Retrieve structured corporate event data from Wall Street Horizon's comprehensive global events calendar, including earnings announcements, dividend dates, investor conferences, and stock splits. Each event record includes essential attributes such as event type, scheduled date, event status (e.g., confirmed, pending, canceled), ISIN, ticker, and direct links to primary announcement sources when available. Data can be filtered (by ticker, event type, etc.), and records are timestamped for seamless integration into trading and analysis workflows.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| date | string | 否 | Scheduled date of the corporate event, formatted as YYYY-MM-DD. |
| type | string | 否 | The normalized type of corporate event. Possible values include: analyst_day, business_update, capital_markets_day, conference, dividend, earnings_announcement_date, earnings_conference_call, earnings_results_announcement, forum, interim_statement, other_interim_announcement, production_update, research_and_development_day, seminar, shareholder_meeting, sales_update, stock_split, summit, service_level_update, tradeshow, company_travel, and workshop. |
| status | string | 否 | The current status of the event. Possible values include: approved, canceled, confirmed, historical, pending_approval, postponed, and unconfirmed. |
| ticker | string | 否 | The company's stock symbol. |
| isin | string | 否 | Standard international identifier for the company's common stock. |
| trading_venue | string | 否 | MIC (Market Identifier Code) of the exchange where the company's stock is listed. |
| tmx_company_id | integer | 否 | Unique numeric identifier for the company used by TMX. Value must be an integer. |
| tmx_record_id | string | 否 | The unique alphanumeric identifier for the event record used by TMX. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'date' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| company_name | string | 否 | Full name of the company. |
| date | string | 否 | Scheduled date of the corporate event, formatted as YYYY-MM-DD. |
| isin | string | 否 | Standard international identifier for the company's common stock. |
| name | string | 否 | Name or title of the event. |
| status | string | 否 | The current status of the event. Possible values include: approved, canceled, confirmed, historical, pending_approval, postponed, and unconfirmed. |
| ticker | string | 否 | The company's stock symbol. |
| tmx_company_id | integer | 否 | Unique numeric identifier for the company used by TMX. |
| tmx_record_id | string | 否 | The unique alphanumeric identifier for the event record used by TMX. |
| trading_venue | string | 否 | MIC (Market Identifier Code) of the exchange where the company's stock is listed. |
| type | string | 否 | The normalized type of corporate event. Possible values include: analyst_day, business_update, capital_markets_day, conference, dividend, earnings_announcement_date, earnings_conference_call, earnings_results_announcement, forum, interim_statement, other_interim_announcement, production_update, research_and_development_day, seminar, shareholder_meeting, sales_update, stock_split, summit, service_level_update, tradeshow, company_travel, and workshop. |
| url | string | 否 | URL linking to the primary public source of the event announcement, if available. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/tmx/v1/corporate-events
```

### Request

```bash
curl -X GET "https://api.massive.com/tmx/v1/corporate-events?limit=100&sort=date.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "company_name": "Rollins Inc.",
      "date": "2025-07-23",
      "isin": "US7757111049",
      "name": "Q2 2025 Earnings Announcement-After Mkt",
      "status": "unconfirmed",
      "ticker": "ROL",
      "tmx_company_id": "2208",
      "tmx_record_id": "4XMW4E9G",
      "trading_venue": "XNYS",
      "type": "earnings_announcement_date"
    }
  ],
  "status": "OK"
}
```
