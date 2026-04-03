# Splits

## 源URL

https://massive.com/docs/rest/stocks/corporate-actions/splits

## 描述

Retrieve historical stock split events, including execution dates and ratio factors, to understand changes in a company’s share structure over time. Also find adjustment factors that can be used to normalize historical prices to today's share basis.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Stock symbol for the company that executed the split |
| execution_date | string | 否 | Date when the stock split was applied and shares adjusted Value must be formatted 'yyyy-mm-dd'. |
| adjustment_type | enum (string) | 否 | Classification of the share-change event. Possible values include: forward_split (share count increases), reverse_split (share count decreases), stock_dividend (shares issued as a dividend) |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '5000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'execution_date' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| adjustment_type | string | 否 | Classification of the share-change event. Possible values include: forward_split (share count increases), reverse_split (share count decreases), stock_dividend (shares issued as a dividend) |
| execution_date | string | 否 | Date when the stock split was applied and shares adjusted |
| historical_adjustment_factor | number | 否 | Cumulative adjustment factor used to offset split effects on historical prices. To adjust a historical price for splits: for a price on date D, find the first split whose `execution_date` is after date D and multiply the unadjusted price by the `historical_adjustment_factor`. |
| id | string | 否 | Unique identifier for each stock split event |
| split_from | number | 否 | Denominator of the split ratio (old shares) |
| split_to | number | 否 | Numerator of the split ratio (new shares) |
| ticker | string | 否 | Stock symbol for the company that executed the split |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/v1/splits
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/v1/splits?limit=100&sort=execution_date.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": 1,
  "results": [
    {
      "adjustment_type": "forward_split",
      "execution_date": "2005-02-28",
      "historical_adjustment_factor": 0.017857,
      "id": "E90a77bdf742661741ed7c8fc086415f0457c2816c45899d73aaa88bdc8ff6025",
      "split_from": 1,
      "split_to": 2,
      "ticker": "AAPL"
    }
  ],
  "status": "OK"
}
```
