# ETF Constituents

## 源URL

https://massive.com/docs/rest/partners/etf-global/constituents

## 描述

Access the underlying holdings and constituents of global ETFs. Get detailed information about what securities ETFs hold, providing transparency into fund composition and investment exposure.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| composite_ticker | string | 否 | The stock ticker symbol of the ETF that holds these constituent securities. |
| constituent_ticker | string | 否 | The stock ticker symbol of the individual security held within the ETF. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. Value must be formatted 'yyyy-mm-dd'. |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. Value must be formatted 'yyyy-mm-dd'. |
| us_code | string | 否 | A unique identifier code for the constituent security in US markets. |
| isin | string | 否 | The International Securities Identification Number, a global standard for identifying securities. |
| figi | string | 否 | The Financial Instrument Global Identifier, an open standard for uniquely identifying financial instruments. |
| sedol | string | 否 | The Stock Exchange Daily Official List code, primarily used for securities trading in the UK. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '5000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'composite_ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| asset_class | string | 否 | The broad category of asset type, such as Equity, Corporate Bond, Municipal Bond, etc. |
| composite_ticker | string | 否 | The stock ticker symbol of the ETF that holds these constituent securities. |
| constituent_name | string | 否 | The full company or security name of the constituent holding. |
| constituent_rank | integer | 否 | The rank of this constituent within the ETF for a given effective_date, ordered by weight (descending), market_value (descending), and constituent_ticker (ascending). A rank of 1 indicates the largest holding. |
| constituent_ticker | string | 否 | The stock ticker symbol of the individual security held within the ETF. |
| country_of_exchange | string | 否 | The country where the exchange that lists this constituent security is located. |
| currency_traded | string | 否 | The local currency in which this constituent security is denominated and traded. |
| effective_date | string | 否 | The date showing when the information was accurate or valid; some issuers, such as Vanguard, release their data on a delay, so the effective_date can be several weeks earlier than the processed_date. |
| exchange | string | 否 | The name of the stock exchange where this constituent security is primarily traded. |
| figi | string | 否 | The Financial Instrument Global Identifier, an open standard for uniquely identifying financial instruments. |
| isin | string | 否 | The International Securities Identification Number, a global standard for identifying securities. |
| market_value | number | 否 | The total market value of this constituent position held by the ETF. |
| processed_date | string | 否 | The date showing when ETF Global received and processed the data. |
| security_type | string | 否 | The specific classification of security type using ETF Global's taxonomy, such as Common Equity, Domestic, Global, etc. |
| sedol | string | 否 | The Stock Exchange Daily Official List code, primarily used for securities trading in the UK. |
| shares_held | number | 否 | The number of shares of this constituent security that the ETF currently owns. |
| us_code | string | 否 | A unique identifier code for the constituent security in US markets. |
| weight | number | 否 | The percentage weight of this constituent security within the ETF's total portfolio. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/etf-global/v1/constituents
```

### Request

```bash
curl -X GET "https://api.massive.com/etf-global/v1/constituents?limit=100&sort=composite_ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "asset_class": "Equity",
      "composite_ticker": "SPY",
      "constituent_name": "CAESARS ENTERTAINMENT INC COMMON STOCK",
      "constituent_rank": 42,
      "constituent_ticker": "CZR",
      "country_of_exchange": "US",
      "currency_traded": "USD",
      "effective_date": "2025-09-18",
      "figi": "BBG0074Q3NK6",
      "isin": "US12769G1004",
      "market_value": 63308625.6,
      "processed_date": "2025-09-19",
      "security_type": "Common Stock",
      "sedol": "BMWWGB0",
      "shares_held": 2398054,
      "us_code": "12769G100",
      "weight": 0.0000958005
    }
  ],
  "status": "OK"
}
```
