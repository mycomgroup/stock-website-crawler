# 10-K Sections

## 源URL

https://massive.com/docs/rest/stocks/filings/10-k-sections

## 描述

Plain-text content of specific sections from SEC filings. Currently supports the Risk Factors and Business sections, providing clean, structured text extracted directly from the filing.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| cik | string | 否 | SEC Central Index Key (10 digits, zero-padded). |
| ticker | string | 否 | Stock ticker symbol for the company. |
| section | enum (string) | 否 | Standardized section identifier from the filing (e.g. 'business', 'risk_factors', etc.). |
| filing_date | string | 否 | Date when the filing was submitted to the SEC (formatted as YYYY-MM-DD). Value must be formatted 'yyyy-mm-dd'. |
| period_end | string | 否 | Period end date that the filing relates to (formatted as YYYY-MM-DD). Value must be formatted 'yyyy-mm-dd'. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '9999'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'period_end' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| cik | string | 否 | SEC Central Index Key (10 digits, zero-padded). |
| filing_date | string | 否 | Date when the filing was submitted to the SEC (formatted as YYYY-MM-DD). |
| filing_url | string | 否 | SEC URL source for the full filing. |
| period_end | string | 否 | Period end date that the filing relates to (formatted as YYYY-MM-DD). |
| section | string | 否 | Standardized section identifier from the filing (e.g. 'business', 'risk_factors', etc.). |
| text | string | 否 | Full raw text content of the section, including headers and formatting. |
| ticker | string | 否 | Stock ticker symbol for the company. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/filings/10-K/vX/sections
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/filings/10-K/vX/sections?limit=100&sort=period_end.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 2,
  "next_url": "https://api.massive.com/stocks/filings/10-K/vX/sections?cursor=eyJsaW1pd...",
  "request_id": "a3f8b2c1d4e5f6g7",
  "results": [
    {
      "cik": "0000320193",
      "filing_date": "2023-11-03",
      "filing_url": "https://www.sec.gov/Archives/edgar/data/320193/0000320193-23-000106.txt",
      "period_end": "2023-09-30",
      "section": "risk_factors",
      "text": "Item 1A. Risk Factors\n\nInvesting in our stock involves risk. In addition to the other information in this Annual Report on Form 10-K, the following risk factors should be carefully considered...",
      "ticker": "AAPL"
    },
    {
      "cik": "0000789019",
      "filing_date": "2023-07-27",
      "filing_url": "https://www.sec.gov/Archives/edgar/data/789019/0000950170-23-035122.txt",
      "period_end": "2023-06-30",
      "section": "risk_factors",
      "text": "Item 1A. RISK FACTORS\n\nOur operations and financial results are subject to various risks and uncertainties...",
      "ticker": "MSFT"
    }
  ],
  "status": "OK"
}
```
