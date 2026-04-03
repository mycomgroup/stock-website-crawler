# ETF Fund Flows

## 源URL

https://massive.com/docs/rest/partners/etf-global/fundflows

## 描述

Track capital movements and investor activity across global ETFs. Access fund flow data that reveals market trends, investor sentiment, and the popularity of different ETF strategies over time.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. Value must be formatted 'yyyy-mm-dd'. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. Value must be formatted 'yyyy-mm-dd'. |
| composite_ticker | string | 否 | The stock ticker symbol used to identify this ETF on exchanges. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '5000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'composite_ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| composite_ticker | string | 否 | The stock ticker symbol used to identify this ETF on exchanges. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. |
| fund_flow | number | 否 | The net daily capital flow into or out of the ETF through the creation and redemption process, where positive values indicate inflows and negative values indicate outflows. |
| nav | number | 否 | The net asset value per share, representing the per-share value of the ETF's underlying holdings. |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. |
| shares_outstanding | number | 否 | The total number of ETF shares currently issued and outstanding in the market. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/etf-global/v1/fund-flows
```

### Request

```bash
curl -X GET "https://api.massive.com/etf-global/v1/fund-flows?limit=100&sort=composite_ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "composite_ticker": "SPY",
      "effective_date": "2025-01-29",
      "fund_flow": -30235124.7,
      "nav": 601.877341,
      "processed_date": "2025-01-29",
      "shares_outstanding": 1047232116
    },
    {
      "composite_ticker": "SPY",
      "effective_date": "2025-01-30",
      "fund_flow": -2798729635.65,
      "nav": 605.0574,
      "processed_date": "2025-01-30",
      "shares_outstanding": 1042582116
    },
    {
      "composite_ticker": "SPY",
      "effective_date": "2025-01-31",
      "fund_flow": -3358068570,
      "nav": 602.044248,
      "processed_date": "2025-01-31",
      "shares_outstanding": 1037032116
    }
  ],
  "status": "OK"
}
```
