# Risk Factors

## 源URL

https://massive.com/docs/rest/stocks/filings/risk-factors

## 描述

Standardized, machine-readable risk factor disclosures from SEC filings. Each risk factor is categorized using a consistent taxonomy, enabling direct comparison across time periods or between different companies. For details on the methodology used, see our research paper.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| filing_date | string | 否 | Date when the filing was submitted to the SEC (formatted as YYYY-MM-DD). |
| ticker | string | 否 | Stock ticker symbol for the company. |
| cik | string | 否 | SEC Central Index Key (10 digits, zero-padded). |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '49999'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'filing_date' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| cik | string | 否 | SEC Central Index Key (10 digits, zero-padded). |
| filing_date | string | 否 | Date when the filing was submitted to the SEC (formatted as YYYY-MM-DD). |
| primary_category | string | 否 | Top-level risk category |
| secondary_category | string | 否 | Mid-level risk category |
| supporting_text | string | 否 | Snippet of text to support the given label |
| tertiary_category | string | 否 | Most specific risk classification |
| ticker | string | 否 | Stock ticker symbol for the company. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/filings/vX/risk-factors
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/filings/vX/risk-factors?limit=100&sort=filing_date.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "request_id": "c7856101f86c20d855b0ea1c5a6d6efa",
  "results": [
    {
      "cik": "0001005101",
      "filing_date": "2025-09-19",
      "primary_category": "financial_and_market",
      "secondary_category": "credit_and_liquidity",
      "supporting_text": "In addition to the net proceeds we received from our recent equity and debt financings, we may need to raise additional equity or debt financing to continue the development and marketing of our Fintech app, to fund ongoing operations, invest in acquisitions, and for working capital purposes. Our inability to raise such additional financing may limit our ability to continue the development of our Fintech app.",
      "tertiary_category": "access_to_capital_and_financing",
      "ticker": "MGLD"
    }
  ],
  "status": "OK"
}
```
