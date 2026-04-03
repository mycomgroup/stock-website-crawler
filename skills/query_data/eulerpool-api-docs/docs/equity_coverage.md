---
id: "url-7875bb03"
type: "api"
title: "Data Coverage API"
url: "https://eulerpool.com/developers/api/equity/coverage"
description: "Returns data availability flags for the given ISIN, indicating which data types are available (balance sheet, estimates, ESG, supply chain, etc.). Use before other calls to avoid 404s."
source: ""
tags: []
crawl_time: "2026-03-18T05:52:45.341Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/coverage/{identifier}"
  responses:
    - {"code":"200","description":"Returns data availability flags"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/coverage/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"ticker\": \"AAPL\",\n  \"hasBalanceSheet\": false,\n  \"hasEstimates\": false,\n  \"hasESG\": false,\n  \"hasSupplyChain\": false,\n  \"hasOwnership\": false\n}"
  suggestedFilename: "equity_coverage"
---

# Data Coverage API

## 源URL

https://eulerpool.com/developers/api/equity/coverage

## 描述

Returns data availability flags for the given ISIN, indicating which data types are available (balance sheet, estimates, ESG, supply chain, etc.). Use before other calls to avoid 404s.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/coverage/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns data availability flags |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/coverage/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "ticker": "AAPL",
  "hasBalanceSheet": false,
  "hasEstimates": false,
  "hasESG": false,
  "hasSupplyChain": false,
  "hasOwnership": false
}
```

## 文档正文

Returns data availability flags for the given ISIN, indicating which data types are available (balance sheet, estimates, ESG, supply chain, etc.). Use before other calls to avoid 404s.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/coverage/{identifier}`
