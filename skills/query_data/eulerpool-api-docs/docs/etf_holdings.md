---
id: "url-3b6aa85d"
type: "api"
title: "ETF Holdings API"
url: "https://eulerpool.com/developers/api/etf/holdings"
description: "Returns the top holdings of the given ETF"
source: ""
tags: []
crawl_time: "2026-03-18T05:43:03.446Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/etf/holdings/{identifier}"
  responses:
    - {"code":"200","description":"Returns ETF holdings"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/etf/holdings/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"etf_symbol\": \"SWDA.L\",\n  \"symbol\": \"NVDA\",\n  \"name\": \"NVIDIA\",\n  \"isin\": \"US67066G1040\",\n  \"cusip\": \"67066G104\",\n  \"percent\": 5.53806,\n  \"share\": 37247231,\n  \"value\": 6910851240,\n  \"assetType\": \"Equity\",\n  \"logo\": \"US67066G1040.png\"\n}\n]"
  suggestedFilename: "etf_holdings"
---

# ETF Holdings API

## 源URL

https://eulerpool.com/developers/api/etf/holdings

## 描述

Returns the top holdings of the given ETF

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/etf/holdings/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns ETF holdings |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/etf/holdings/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "etf_symbol": "SWDA.L",
  "symbol": "NVDA",
  "name": "NVIDIA",
  "isin": "US67066G1040",
  "cusip": "67066G104",
  "percent": 5.53806,
  "share": 37247231,
  "value": 6910851240,
  "assetType": "Equity",
  "logo": "US67066G1040.png"
}
]
```

## 文档正文

Returns the top holdings of the given ETF

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/etf/holdings/{identifier}`
