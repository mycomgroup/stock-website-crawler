---
id: "url-5e8758cc"
type: "api"
title: "Mutual Fund Holdings"
url: "https://eulerpool.com/developers/api/mutual/fund/holdings"
description: "Returns top holdings for a mutual fund"
source: ""
tags: []
crawl_time: "2026-03-18T06:03:01.040Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/mutual-fund/holdings/{symbol}"
  responses:
    - {"code":"200","description":"Fund holdings"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/mutual-fund/holdings/VFINX' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"name\": \"Apple Inc\",\n  \"symbol\": \"AAPL\",\n  \"weight\": 5.2,\n  \"shares\": 0\n}\n]"
  suggestedFilename: "mutual_fund_holdings"
---

# Mutual Fund Holdings

## 源URL

https://eulerpool.com/developers/api/mutual/fund/holdings

## 描述

Returns top holdings for a mutual fund

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/mutual-fund/holdings/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Fund holdings |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/mutual-fund/holdings/VFINX' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "name": "Apple Inc",
  "symbol": "AAPL",
  "weight": 5.2,
  "shares": 0
}
]
```

## 文档正文

Returns top holdings for a mutual fund

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/mutual-fund/holdings/{symbol}`
