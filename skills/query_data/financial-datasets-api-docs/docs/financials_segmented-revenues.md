# Segmented Revenues

## 源URL

https://docs.financialdatasets.ai/api/financials/segmented-revenues

## 描述

Get detailed, segmented revenue data for a ticker.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.financialdatasets.ai/financials/segmented-revenues`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `X-API-KEY` | string | 是 | - | API key for authentication. (Header参数) |
| `ticker` | string | 是 | - | The ticker symbol. |
| `period` | enum | 是 | - | The date or time period to which the reported revenue data relates in ISO 8601 format (YYYY-MM-DD). |
| `limit` | integer | 否 | - | The maximum number of revenue statements to return. |
| `cik` | string | 否 | - | The Central Index Key (CIK) of the company. |
| `report_period` | string | 否 | - | Filter by exact report period date in YYYY-MM-DD format. |
| `report_period_gte` | string | 否 | - | Filter by report period greater than or equal to date in YYYY-MM-DD format. |
| `report_period_lte` | string | 否 | - | Filter by report period less than or equal to date in YYYY-MM-DD format. |
| `report_period_gt` | string | 否 | - | Filter by report period greater than date in YYYY-MM-DD format. |
| `report_period_lt` | string | 否 | - | Filter by report period less than date in YYYY-MM-DD format. |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.financialdatasets.ai/financials/segmented-revenues \
  --header 'X-API-KEY: <api-key>'
```

### 示例 2 (json)

```json
{
  "segmented_revenues": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "period": "quarterly",
      "items": [
        {
          "name": "<string>",
          "amount": 123,
          "end_period": "2023-12-25",
          "start_period": "2023-12-25",
          "segments": [
            {
              "label": "<string>",
              "type": "<string>"
            }
          ]
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
ticker = "AAPL"     # stock ticker
period = "annual"   # possible values are "annual" or "quarterly"
limit = 5           # number of statements to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/segmented-revenues/'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse segmented_revenues from the response
segmented_revenues = response.json().get('segmented_revenues')
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
Segmented Financials
GET
Segmented Revenues
Stock Prices
Get segmented revenue data

cURL

Copy
curl --request GET \
  --url https://api.financialdatasets.ai/financials/segmented-revenues \
  --header 'X-API-KEY: <api-key>'
200
400
401
402
404
Copy
{
  "segmented_revenues": [
    {
      "ticker": "<string>",
      "report_period": "2023-12-25",
      "period": "quarterly",
      "items": [
        {
          "name": "<string>",
          "amount": 123,
          "end_period": "2023-12-25",
          "start_period": "2023-12-25",
          "segments": [
            {
              "label": "<string>",
              "type": "<string>"
            }
          ]
        }
      ]
    }
  ]
}
Segmented Financials
Segmented Revenues

Get detailed, segmented revenue data for a ticker.

GET
/
financials
/
segmented-revenues
Try it
​
Overview
The segmented revenues API provides as-reported, granular revenue data for a given stock ticker.
I finally launched the segmented revenues API, which lets your AI financial agent access segmented revenue data by product lines, business segments, and geographical regions for a given stock ticker.
This includes revenue data segmented by:
product lines
business segments
geographical regions
For example, Apple Inc. reports segmented revenue for its different product lines like iPhone, Mac, iPad, and wearables.
Apple also reports segmented revenue for its different geographical regions like the Americas, Europe, and China.
The segmented revenues API lets you easily access this data in a structured format:
Copy
{
  "segmented_revenues": [
    {
      "ticker": "AAPL",
      "report_period": "2023-09-30",
      "period": "annual",
      "items": [
        "...",
        {
          "line_item": "Revenue From Contract With Customer Excluding Assessed Tax",
          "amount": 201183000000.0,
          "end_period": "2024-09-28",
          "start_period": "2023-10-01",
          "segments": [
              {
                  "label": "IPhone",
                  "type": "Product or Service"
              }
          ]
        },
        {
          "line_item": "Revenue From Contract With Customer Excluding Assessed Tax",
          "amount": 29984000000.0,
          "end_period": "2024-09-28",
          "start_period": "2023-10-01",
          "segments": [
              {
                  "label": "Mac",
                  "type": "Product or Service"
              }
          ]
        },
        {
            "line_item": "Revenue From Contract With Customer Excluding Assessed Tax",
            "amount": 167045000000.0,
            "end_period": "2024-09-28",
            "start_period": "2023-10-01",
            "segments": [
                {
                    "label": "Americas",
                    "type": "Statement Business Segments"
                }
            ]
        },
        {
          "line_item": "Revenue From Contract With Customer Excluding Assessed Tax",
          "amount": 101328000000.0,
          "end_period": "2024-09-28",
          "start_period": "2023-10-01",
          "segments": [
              {
                  "label": "Europe",
                  "type": "Statement Business Segments"
              }
          ]
        },
        {
            "line_item": "Revenue From Contract With Customer Excluding Assessed Tax",
            "amount": 66952000000.0,
            "end_period": "2024-09-28",
            "start_period": "2023-10-01",
            "segments": [
                {
                    "label": "Greater China",
                    "type": "Statement Business Segments"
                }
            ]
        },
        ...
      ]
    }
  ]
}

This data is pulled directly from XBRL filings (10-Ks and 10-Qs). We have included the original XBRL tags like key and axis in the response for your reference.
To get started, please create an account and grab your API key at financialdatasets.ai.
You will use the API key to authenticate your API requests.
​
Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/financials/segmented-revenues/tickers/
​
Getting Started
There are only 3 steps for making a successful API call:
Add your API key to the header of the request as X-API-KEY.
Add query params like ticker, period and limit to filter the data.
Execute the API request.
You can filter the data by ticker, period, limit, and cik.
The period parameter can be set to "annual" or "quarterly". The limit parameter is used to specify the number of statements to return.
Note: ticker and period are required. Alternatively, you can use cik instead of ticker as a company identifier in your
