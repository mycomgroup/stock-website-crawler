---
id: "url-31736c2a"
type: "api"
title: "Analyst Estimates API"
url: "https://eulerpool.com/developers/api/equity/estimates"
description: "Returns analyst estimates for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:54:23.726Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/estimates/{identifier}"
  responses:
    - {"code":"200","description":"Returns analyst estimates."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/estimates/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"period\": \"2030-06-30T00:00:00.000Z\",\n  \"year\": 2030,\n  \"revenueEstimate\": 516905000000,\n  \"revenueHigh\": 586236000000,\n  \"revenueLow\": 464520000000,\n  \"revenueAnalysts\": 5,\n  \"epsEstimate\": 27.7134,\n  \"epsHigh\": 28.5285,\n  \"epsLow\": 26.6266,\n  \"epsAnalysts\": 3,\n  \"ebitEstimate\": 255176000000,\n  \"ebitHigh\": 269372000000,\n  \"ebitLow\": 238454000000,\n  \"ebitAnalysts\": 4\n}\n]"
  suggestedFilename: "equity_estimates"
---

# Analyst Estimates API

## 源URL

https://eulerpool.com/developers/api/equity/estimates

## 描述

Returns analyst estimates for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/estimates/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns analyst estimates. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/estimates/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "period": "2030-06-30T00:00:00.000Z",
  "year": 2030,
  "revenueEstimate": 516905000000,
  "revenueHigh": 586236000000,
  "revenueLow": 464520000000,
  "revenueAnalysts": 5,
  "epsEstimate": 27.7134,
  "epsHigh": 28.5285,
  "epsLow": 26.6266,
  "epsAnalysts": 3,
  "ebitEstimate": 255176000000,
  "ebitHigh": 269372000000,
  "ebitLow": 238454000000,
  "ebitAnalysts": 4
}
]
```

## 文档正文

Returns analyst estimates for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/estimates/{identifier}`
