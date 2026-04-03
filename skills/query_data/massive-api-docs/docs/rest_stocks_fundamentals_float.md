# Float

## 源URL

https://massive.com/docs/rest/stocks/fundamentals/float

## 描述

Retrieve the latest free float for a specified stock ticker. Free float represents the shares outstanding that are considered available for public trading, after accounting for shares held by strategic or long-term holders.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The primary ticker symbol for the stock. |
| free_float_percent | number | 否 | Percentage of total shares outstanding that are available for public trading, rounded to two decimal places. Value must be a floating point number. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '5000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| effective_date | string | 否 | The effective date of the free float measurement. |
| free_float | integer | 否 | Number of shares freely tradable in the market. Free float shares represent the portion of a company's outstanding shares that is freely tradable in the market, excluding any holdings considered strategic, controlling, or long term. This excludes insiders, directors, founders, 5 percent plus shareholders, cross holdings, government stakes except pensions, restricted or locked up shares, employee plans, and any entities with board influence, leaving only shares that are genuinely available for public trading. |
| free_float_percent | number | 否 | Percentage of total shares outstanding that are available for public trading, rounded to two decimal places. |
| ticker | string | 否 | The primary ticker symbol for the stock. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/vX/float
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/vX/float?limit=100&sort=ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": 1,
  "results": [
    {
      "effective_date": "2025-11-01",
      "free_float": 15000000000,
      "free_float_percent": 98.5,
      "ticker": "AAPL"
    }
  ],
  "status": "OK"
}
```
