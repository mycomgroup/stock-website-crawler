# SEC EDGAR Index

## 源URL

https://massive.com/docs/rest/stocks/filings/index

## 描述

SEC EDGAR master index providing metadata for all SEC filings including form types, filing dates, and direct links to source documents.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| cik | string | 否 | SEC Central Index Key (CIK) identifying the filing entity. |
| ticker | string | 否 | Stock ticker symbol for the filing entity, if available. |
| form_type | string | 否 | SEC form type (e.g., '10-K', '10-Q', '8-K', 'S-1', '4', etc.). |
| filing_date | string | 否 | Date when the filing was submitted to the SEC (formatted as YYYY-MM-DD). Value must be formatted 'yyyy-mm-dd'. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '1000' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'filing_date' if not specified. The sort order defaults to 'desc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| accession_number | string | 否 | SEC accession number uniquely identifying the filing (e.g., '0000320193-24-000123'). |
| cik | string | 否 | SEC Central Index Key (CIK) identifying the filing entity. |
| filing_date | string | 否 | Date when the filing was submitted to the SEC (formatted as YYYY-MM-DD). |
| filing_url | string | 否 | Direct URL to the filing on the SEC EDGAR website. |
| form_type | string | 否 | SEC form type (e.g., '10-K', '10-Q', '8-K', 'S-1', '4', etc.). |
| issuer_name | string | 否 | Name of the company or entity that submitted the filing. |
| ticker | string | 否 | Stock ticker symbol for the filing entity, if available. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/filings/vX/index
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/filings/vX/index?limit=1000&sort=filing_date.desc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 2,
  "next_url": "https://api.massive.com/stocks/filings/vX/index?cursor=eyJsaW1pd...",
  "request_id": "1daccfd9794e482e96d104dee6ed432b",
  "results": [
    {
      "accession_number": "0000320193-25-000079",
      "cik": "0000320193",
      "filing_date": "2025-10-31",
      "filing_url": "https://www.sec.gov/Archives/edgar/data/320193/0000320193-25-000079.txt",
      "form_type": "10-K",
      "issuer_name": "Apple Inc.",
      "ticker": "AAPL"
    },
    {
      "accession_number": "0000950170-25-010491",
      "cik": "0000789019",
      "filing_date": "2025-01-29",
      "filing_url": "https://www.sec.gov/Archives/edgar/data/789019/0000950170-25-010491.txt",
      "form_type": "10-Q",
      "issuer_name": "MICROSOFT CORP",
      "ticker": "MSFT"
    }
  ],
  "status": "OK"
}
```
