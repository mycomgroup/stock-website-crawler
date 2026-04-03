---
id: "url-328745bc"
type: "api"
title: "ETF Profile API"
url: "https://eulerpool.com/developers/api/etf/profile"
description: "Returns comprehensive profile information for the given ETF identifier"
source: ""
tags: []
crawl_time: "2026-03-18T05:29:41.730Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/etf/profile/{identifier}"
  responses:
    - {"code":"200","description":"Returns comprehensive ETF profile information"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/etf/profile/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"IE00B4L5Y983\",\n  \"symbol\": \"SWDA.L\",\n  \"name\": \"iShares Core MSCI World UCITS ETF\",\n  \"description\": \"SWDA.L was created on 2009-09-25 by iShares. The fund's investment portfolio concentrates primarily on total market equity. The ETF currently has 121372.55m in AUM and 1322 holdings.\",\n  \"assetClass\": \"Equity\",\n  \"investmentSegment\": \"Total Market\",\n  \"etfCompany\": \"iShares\",\n  \"expenseRatio\": 0.2,\n  \"aum\": 121372550000,\n  \"nav\": 124.4348,\n  \"currency\": \"USD\",\n  \"exchangeRate\": 0.85,\n  \"latestQuotes\": 124.4348,\n  \"inceptionDate\": \"2009-09-25T00:00:00.000Z\",\n  \"domicile\": \"Ireland\",\n  \"trackingIndex\": \"MSCI World\",\n  \"isLeveraged\": false,\n  \"isInverse\": false,\n  \"leverageFactor\": 1,\n  \"dividendYield\": 1.4,\n  \"website\": \"https://www.ishares.com\",\n  \"tickers\": {\n    \"ticker\": \"SWDA.L\",\n    \"exchange\": \"LSE\"\n  }\n}"
  suggestedFilename: "etf_profile"
---

# ETF Profile API

## 源URL

https://eulerpool.com/developers/api/etf/profile

## 描述

Returns comprehensive profile information for the given ETF identifier

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/etf/profile/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns comprehensive ETF profile information |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/etf/profile/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "IE00B4L5Y983",
  "symbol": "SWDA.L",
  "name": "iShares Core MSCI World UCITS ETF",
  "description": "SWDA.L was created on 2009-09-25 by iShares. The fund's investment portfolio concentrates primarily on total market equity. The ETF currently has 121372.55m in AUM and 1322 holdings.",
  "assetClass": "Equity",
  "investmentSegment": "Total Market",
  "etfCompany": "iShares",
  "expenseRatio": 0.2,
  "aum": 121372550000,
  "nav": 124.4348,
  "currency": "USD",
  "exchangeRate": 0.85,
  "latestQuotes": 124.4348,
  "inceptionDate": "2009-09-25T00:00:00.000Z",
  "domicile": "Ireland",
  "trackingIndex": "MSCI World",
  "isLeveraged": false,
  "isInverse": false,
  "leverageFactor": 1,
  "dividendYield": 1.4,
  "website": "https://www.ishares.com",
  "tickers": {
    "ticker": "SWDA.L",
    "exchange": "LSE"
  }
}
```

## 文档正文

Returns comprehensive profile information for the given ETF identifier

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/etf/profile/{identifier}`
