---
id: "url-43e54372"
type: "api"
title: "Company Overview API"
url: "https://eulerpool.com/developers/api/equity/overview"
description: "Returns a comprehensive company overview combining profile data, key financial ratios (P/E, P/S, dividend yield), 52-week price range, fair value, and market data in a single response"
source: ""
tags: []
crawl_time: "2026-03-18T05:52:25.667Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/overview/{identifier}"
  responses:
    - {"code":"200","description":"Returns comprehensive company overview."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/overview/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"string\",\n  \"ticker\": \"string\",\n  \"name\": \"string\",\n  \"description\": \"string\",\n  \"currency\": \"string\",\n  \"country\": \"string\",\n  \"sector\": \"string\",\n  \"industry\": \"string\",\n  \"website\": \"string\",\n  \"ipo\": \"string\",\n  \"employees\": 0,\n  \"marketCap\": 0,\n  \"sharesOutstanding\": 0,\n  \"price\": 0,\n  \"week52High\": 0,\n  \"week52Low\": 0,\n  \"pe\": 0,\n  \"ps\": 0,\n  \"dividendYield\": 0,\n  \"fairValueIncome\": 0,\n  \"fairValueRevenue\": 0,\n  \"aaqs\": 0\n}"
  suggestedFilename: "equity_overview"
---

# Company Overview API

## 源URL

https://eulerpool.com/developers/api/equity/overview

## 描述

Returns a comprehensive company overview combining profile data, key financial ratios (P/E, P/S, dividend yield), 52-week price range, fair value, and market data in a single response

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/overview/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns comprehensive company overview. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/overview/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "string",
  "ticker": "string",
  "name": "string",
  "description": "string",
  "currency": "string",
  "country": "string",
  "sector": "string",
  "industry": "string",
  "website": "string",
  "ipo": "string",
  "employees": 0,
  "marketCap": 0,
  "sharesOutstanding": 0,
  "price": 0,
  "week52High": 0,
  "week52Low": 0,
  "pe": 0,
  "ps": 0,
  "dividendYield": 0,
  "fairValueIncome": 0,
  "fairValueRevenue": 0,
  "aaqs": 0
}
```

## 文档正文

Returns a comprehensive company overview combining profile data, key financial ratios (P/E, P/S, dividend yield), 52-week price range, fair value, and market data in a single response

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/overview/{identifier}`
