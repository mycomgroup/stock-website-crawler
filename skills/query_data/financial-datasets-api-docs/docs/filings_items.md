# Items

## 源URL

https://docs.financialdatasets.ai/api/filings/items

## 描述

Get the raw text Items from an SEC filing.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/filings/items`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol. |
| `filing_type` | enum | 是 | - | The type of filing. |
| `year` | integer | 是 | - | The year of the filing. |
| `quarter` | integer | 否 | - | The quarter of the filing if 10-Q. |
| `item` | enum | 否 | - | The item to get. |
| `accession_number` | string | 否 | - | The accession number of the filing if 8-K. |
| `resource` | string | 否 | - | The resource type identifier. |
| `cik` | string | 否 | - | The Central Index Key (CIK) of the company. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/filings/items \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "resource": "<string>",
  "ticker": "<string>",
  "cik": "<string>",
  "filing_type": "<string>",
  "accession_number": "<string>",
  "year": 123,
  "quarter": 123,
  "items": [
    {
      "number": "<string>",
      "name": "<string>",
      "text": "<string>",
      "exhibits": [
        {
          "number": "<string>",
          "description": "<string>",
          "url": "<string>",
          "text": "<string>"
        }
      ]
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
filing_type = '10-K'
year = 2023

# create the URL
url = (
    f'https://api.financialdatasets.ai/filings/items'
    f'?ticker={ticker}'
    f'&filing_type={filing_type}'
    f'&year={year}'
)

# make API request
response = requests.get(url, headers=headers)

# parse filings from the response
items = response.json().get('items')
```

## 详细内容

Financial Datasets home page
Search...
⌘K
Support
Dashboard
Dashboard
Pricing
Discord
Overview
Introduction
Data Provenance
Market Coverage
MCP Server
Support
APIs
Analyst Estimates
Company
Earnings
Financial Metrics
Financial Statements
Insider Trades
News
Institutional Ownership
Interest Rates
Search
SEC Filings
GET
Filings
GET
Items
Segmented Financials
Stock Prices
Get SEC filing items

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/filings/items \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "resource": "<string>",
  "ticker": "<string>",
  "cik": "<string>",
  "filing_type": "<string>",
  "accession_number": "<string>",
  "year": 123,
  "quarter": 123,
  "items": [
    {
      "number": "<string>",
      "name": "<string>",
      "text": "<string>",
      "exhibits": [
        {
          "number": "<string>",
          "description": "<string>",
          "url": "<string>",
          "text": "<string>"
        }
      ]
    }
  ]
}
SEC Filings
Items

Get the raw text Items from an SEC filing.

GET
/
filings
/
items
Try it
​
Overview
The Items endpoint allows you to retrieve the raw text from the sections (called items) from a given 10-K, 10-Q, or 8-K filing.
This lets you easily extract data from a filing without having to parse the entire document on your own.
For 8-K filings, items may include an exhibits array when exhibits are present. Use the include_exhibits parameter to retrieve the raw text content of linked exhibits.
​
Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/filings/tickers/
​
Valid Item Types
You can fetch a list of valid item types for 10-K and 10-Q filings with a GET request to: https://api.financialdatasets.ai/filings/items/types/
You can optionally filter by filing type using the filing_type query parameter:
https://api.financialdatasets.ai/filings/items/types/?filing_type=10-K - returns only 10-K item types
https://api.financialdatasets.ai/filings/items/types/?filing_type=10-Q - returns only 10-Q item types
The response includes the item name and title for each valid item type.
​
Examples
10-K Filing
10-Q Filing
8-K Filing
Specific Items
Copy
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'
filing_type = '10-K'
year = 2023

# create the URL
url = (
    f'https://api.financialdatasets.ai/filings/items'
    f'?ticker={ticker}'
    f'&filing_type={filing_type}'
    f'&year={year}'
)

# make API request
response = requests.get(url, headers=headers)

# parse filings from the response
items = response.json().get('items')

Authorizations
​
X-API-KEY
stringheaderrequired

API key for authentication.

Query Parameters
​
ticker
stringrequired

The ticker symbol.

​
filing_type
enum<string>required

The type of filing.

Available options: 10-K, 10-Q, 8-K 
​
year
integerrequired

The year of the filing.

​
quarter
integer

The quarter of the filing if 10-Q.

​
item
enum<string>

The item to get.

Available options: Item-1, Item-1A, Item-1B, Item-2, Item-3, Item-4, Item-5, Item-6, Item-7, Item-7A, Item-8, Item-9, Item-9A, Item-9B, Item-10, Item-11, Item-12, Item-13, Item-14, Item-15, Item-16, Item-1.01, Item-1.02, Item-1.03, Item-1.04, Item-2.01, Item-2.02, Item-2.03, Item-2.04, Item-2.05, Item-2.06, Item-3.01, Item-3.02, Item-3.03, Item-4.01, Item-4.02, Item-5.01, Item-5.02, Item-5.03, Item-5.04, Item-5.05, Item-5.06, Item-5.07, Item-5.08, Item-6.01, Item-6.02, Item-6.03, Item-6.04, Item-6.05, Item-7.01, Item-8.01, Item-9.01 
​
accession_number
string

The accession number of the filing if 8-K.

​
include_exhibits
booleandefault:false

Whether to include the raw text from linked exhibits. Only applicable for 8-K filings. When true, exhibit objects will include the 'text' field containing the full exhibit content.

Response
200
application/json

SEC filing items response

​
resource
string

The resource type identifier.

​
ticker
string

The ticker symbol of the company.

​
cik
string

The Central Index Key (CIK) of the company.

​
filing_type
string

The type of filing.

​
accession_number
string

The accession number of the filing.

​
year
integer

The year of the filing.

​
quarter
integer

The quarter of the filing.

​
items
object[]

Hide child attributes

​
items.number
string

The item number.

​
items.name
string

The item name.

​
items.text
string

The item text.

​
items.exhibits
object[]

An array of exhibits linked to this item. Only present for 8-K filings when exhibits exist.

Show child attributes

Filings
Segmented Revenues
x
github
Powered by
This documentation is built and hosted on Mintlify, a developer documentation platform
