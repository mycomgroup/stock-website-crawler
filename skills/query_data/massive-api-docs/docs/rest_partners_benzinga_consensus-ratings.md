# Consensus Ratings

## 源URL

https://massive.com/docs/rest/partners/benzinga/consensus-ratings

## 描述

Retrieve consensus ratings from financial analysts, including aggregated rating distributions and price target ranges. Each record reflects the collective outlook for a security, summarizing sentiment across firms and analysts. This dataset supports trend analysis and offers a high-level view of market expectations.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The requested ticker. |
| date | string | 否 | The date range to aggregate analyst ratings over. For example, date.gte=2024-10-01 and date.lt=2025-01-01 for ratings published in Q4 2024. By default, all ratings are aggregated regardless of date. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| buy_ratings | integer | 否 | The count of 'Buy' ratings from contributing analysts. |
| consensus_price_target | number | 否 | The average price target across all analysts, rounded to 2 decimal places. |
| consensus_rating | string | 否 | The overall rating category determined by the average consensus weight. Possible values: 'strong_buy', 'buy', 'hold', 'sell', 'strong_sell'. |
| consensus_rating_value | number | 否 | The numerical average of all consensus weights, rounded to 2 decimal places. Scale ranges from 1 (Strong Sell) to 5 (Strong Buy). |
| high_price_target | number | 否 | The highest price target among all contributing analysts. |
| hold_ratings | integer | 否 | The count of 'Hold' ratings from contributing analysts. |
| low_price_target | number | 否 | The lowest price target among all contributing analysts. |
| price_target_contributors | integer | 否 | The number of unique analysts contributing price targets. |
| ratings_contributors | integer | 否 | The number of unique analysts contributing to the overall ratings consensus. |
| sell_ratings | integer | 否 | The count of 'Sell' ratings from contributing analysts. |
| strong_buy_ratings | integer | 否 | The count of 'Strong Buy' ratings from contributing analysts. |
| strong_sell_ratings | integer | 否 | The count of 'Strong Sell' ratings from contributing analysts. |
| ticker | string | 否 | The requested ticker. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/benzinga/v1/consensus-ratings/{ticker}
```

### Request

```bash
curl -X GET "https://api.massive.com/benzinga/v1/consensus-ratings/ARM?limit=100&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "buy_ratings": 6,
      "consensus_price_target": 23.28,
      "consensus_rating": "hold",
      "consensus_rating_value": 4.14,
      "high_price_target": 32.14,
      "hold_ratings": 3,
      "low_price_target": 6.34,
      "price_target_contributors": 15,
      "ratings_contributors": 14,
      "sell_ratings": 0,
      "strong_buy_ratings": 5,
      "strong_sell_ratings": 0,
      "ticker": "AAPL"
    }
  ],
  "status": "OK"
}
```
