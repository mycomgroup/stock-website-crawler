# Filings

## 源URL

https://docs.financialdatasets.ai/api/filings/ticker

## 描述

The Central Index Key (CIK) of the company.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/filings`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `cik` | string | 否 | - | The Central Index Key (CIK) of the company. |
| `ticker` | string | 否 | - | The ticker symbol. |

## 响应字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `cik` | integer | The Central Index Key (CIK) of the company. |
| `accession_number` | string | The accession number of the filing. |
| `filing_type` | string | The type of the SEC filing (e.g., 10-Q, 8-K). |
| `report_date` | string | <date> |
| `filing_date` | string | <date> |
| `ticker` | string | The ticker symbol. |
| `url` | string | <uri> |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url 'https://api.financialdatasets.ai/filings?limit=10' \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "filings": [
    {
      "cik": 123,
      "accession_number": "<string>",
      "filing_type": "<string>",
      "report_date": "2023-12-25",
      "filing_date": "2023-12-25",
      "ticker": "<string>",
      "url": "<string>"
    }
  ]
}
```

### 示例 3 (python)

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'
limit = 10

# create the URL
url = (
    f'https://api.financialdatasets.ai/filings'
    f'?ticker={ticker}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse filings from the response
filings = response.json().get('filings')
```

### 示例 4 (python)

```python
import requests

headers = {"X-API-KEY": "your_api_key_here"}
url = "https://api.financialdatasets.ai/filings"
params = [
    ("ticker", "AAPL"),
    ("filing_type", "10-Q"),
    ("filing_type", "10-K"),
]

response = requests.get(url, headers=headers, params=params)
filings = response.json().get("filings")
```
