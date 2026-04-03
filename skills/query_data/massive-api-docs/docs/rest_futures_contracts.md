# Contracts

## 源URL

https://massive.com/docs/rest/futures/contracts

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| date | string | 否 | A date string in the format YYYY-MM-DD. This parameter will return point-in-time information about contracts for the specified day. Value must be formatted 'yyyy-mm-dd'. |
| product_code | string | 否 | The identifier for the contract's product. |
| ticker | string | 否 | The ticker for the contract. |
| active | boolean | 否 | Whether or not a given contract was tradeable at the given point in time. Active is true when (first_trade_date <= date >= last_trade_date) and false otherwise. |
| type | enum (string) | 否 | The type of contract, one of 'single' or 'combo'. Leaving this filter blank will query for contracts where type is 'single', 'combo' or empty. This field only exists on contracts as of 2025-03-12 and later. It will be null when date < 2025-03-12. |
| first_trade_date | string | 否 | The first day on which the contract was tradeable. Value must be formatted 'yyyy-mm-dd'. |
| last_trade_date | string | 否 | The last day on which the contract was tradeable. Value must be formatted 'yyyy-mm-dd'. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '1000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'product_code' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| active | boolean | 否 | Whether or not a given contract was tradeable at the given point in time. Active is true when (first_trade_date <= date >= last_trade_date) and false otherwise. |
| date | string | 否 | A date string in the format YYYY-MM-DD. This parameter will return point-in-time information about contracts for the specified day. |
| days_to_maturity | integer | 否 | The number of calendar days between the 'date' and the contract's final settlement date. |
| first_trade_date | string | 否 | The first day on which the contract was tradeable. |
| group_code | string | 否 | An identifier used to identify logical groups of products. The group_code is only populated for contracts listed for trading on CME Globex. |
| last_trade_date | string | 否 | The last day on which the contract was tradeable. |
| max_order_quantity | integer | 否 | The maximum order quantity. |
| min_order_quantity | integer | 否 | The minimum order quantity. |
| name | string | 否 | The name of this contract. |
| product_code | string | 否 | The identifier for the contract's product. |
| settlement_date | string | 否 | The date on which this contract settles. |
| settlement_tick_size | number | 否 | The tick size for settlement. |
| spread_tick_size | number | 否 | The tick size for spreads. |
| ticker | string | 否 | The ticker for the contract. |
| trade_tick_size | number | 否 | The tick size for trades. |
| trading_venue | string | 否 | The trading venue (MIC) for the exchange on which this contract trades. |
| type | string | 否 | The type of contract, one of 'single' or 'combo'. Leaving this filter blank will query for contracts where type is 'single', 'combo' or empty. This field only exists on contracts as of 2025-03-12 and later. It will be null when date < 2025-03-12. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/futures/vX/contracts
```

### Request

```bash
curl -X GET "https://api.massive.com/futures/vX/contracts?limit=100&sort=product_code.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "next_url": "https://api.massive.com/futures/vX/contracts?cursor=YWN0aXZlPXRydWUmZGF0ZT0yMDIxLTA0LTI1JmxpbWl0PTEmb3JkZXI9YXNjJnBhZ2VfbWFya2VyPUElN0M5YWRjMjY0ZTgyM2E1ZjBiOGUyNDc5YmZiOGE1YmYwNDVkYzU0YjgwMDcyMWE2YmI1ZjBjMjQwMjU4MjFmNGZiJnNvcnQ9dGlja2Vy",
  "request_id": "000a000a0a0a000a0a0aa00a0a0000a0",
  "results": [
    {
      "active": true,
      "date": "2025-02-26",
      "days_to_maturity": 138,
      "first_trade_date": "2025-01-15",
      "group_code": "CN",
      "last_trade_date": "2025-07-14",
      "max_order_quantity": 1999,
      "min_order_quantity": 1,
      "name": "00CN5 Future",
      "product_code": "00C",
      "settlement_date": "2025-07-14",
      "settlement_tick_size": 0.0025,
      "spread_tick_size": 0.0025,
      "ticker": "00CN5",
      "trade_tick_size": 0.0025,
      "trading_venue": "XCBT",
      "type": "single"
    }
  ],
  "status": "OK"
}
```
