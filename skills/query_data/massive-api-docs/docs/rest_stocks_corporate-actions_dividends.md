# Dividends

## 源URL

https://massive.com/docs/rest/stocks/corporate-actions/dividends

## 描述

Retrieve a historical record of cash dividend distributions for a given ticker, including declaration, ex-dividend, record, and pay dates, as well as payout amounts and adjustment factors for normalizing historical data to offset the effects of dividends. This endpoint consolidates key dividend information, enabling users to account for dividend income in returns, develop dividend-focused strategies, and support tax reporting needs.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Stock symbol for the company issuing the dividend |
| ex_dividend_date | string | 否 | Date when the stock begins trading without the dividend value Value must be formatted 'yyyy-mm-dd'. |
| frequency | integer | 否 | How many times per year this dividend is expected to occur. A value of 0 means the distribution is non-recurring or irregular (e.g., special, supplemental, or a one-off dividend). Other possible values include 1 (annual), 2 (semi-annual), 3 (trimester), 4 (quarterly), 12 (monthly), 24 (bi-monthly), 52 (weekly), 104 (bi-weekly), and 365 (daily) depending on the issuer's declared or inferred payout cadence. Value must be an integer. |
| distribution_type | enum (string) | 否 | Classification describing the nature of this dividend's recurrence pattern: recurring (paid on a regular schedule), special (one-time or commemorative), supplemental (extra beyond the regular schedule), irregular (unpredictable or non-recurring), unknown (cannot be classified from available data) |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '5000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| cash_amount | number | 否 | Original dividend amount per share in the specified currency |
| currency | string | 否 | Currency code for the dividend payment (e.g., USD, CAD) |
| declaration_date | string | 否 | Date when the company officially announced the dividend |
| distribution_type | string | 否 | Classification describing the nature of this dividend's recurrence pattern: recurring (paid on a regular schedule), special (one-time or commemorative), supplemental (extra beyond the regular schedule), irregular (unpredictable or non-recurring), unknown (cannot be classified from available data) |
| ex_dividend_date | string | 否 | Date when the stock begins trading without the dividend value |
| frequency | integer | 否 | How many times per year this dividend is expected to occur. A value of 0 means the distribution is non-recurring or irregular (e.g., special, supplemental, or a one-off dividend). Other possible values include 1 (annual), 2 (semi-annual), 3 (trimester), 4 (quarterly), 12 (monthly), 24 (bi-monthly), 52 (weekly), 104 (bi-weekly), and 365 (daily) depending on the issuer's declared or inferred payout cadence. |
| historical_adjustment_factor | number | 否 | Cumulative adjustment factor used to offset dividend effects on historical prices. To adjust a historical price for dividends: for a price on date D, find the first dividend whose `ex_dividend_date` is after date D and multiply the price by that dividend's `historical_adjustment_factor`. |
| id | string | 否 | Unique identifier for each dividend record |
| pay_date | string | 否 | Date when the dividend payment is distributed to shareholders |
| record_date | string | 否 | Date when shareholders must be on record to be eligible for the dividend payment |
| split_adjusted_cash_amount | number | 否 | Dividend amount adjusted for stock splits that occurred after the dividend was paid, expressed on a current share basis |
| ticker | string | 否 | Stock symbol for the company issuing the dividend |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/v1/dividends
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/v1/dividends?limit=100&sort=ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": 1,
  "results": [
    {
      "cash_amount": 0.26,
      "currency": "USD",
      "declaration_date": "2025-07-31",
      "distribution_type": "recurring",
      "ex_dividend_date": "2025-08-11",
      "frequency": 4,
      "historical_adjustment_factor": 0.997899,
      "id": "Ed2c9da60abda1e3f0e99a43f6465863c137b671e1f5cd3f833d1fcb4f4eb27fe",
      "pay_date": "2025-08-14",
      "record_date": "2025-08-11",
      "split_adjusted_cash_amount": 0.26,
      "ticker": "AAPL"
    }
  ],
  "status": "OK"
}
```
