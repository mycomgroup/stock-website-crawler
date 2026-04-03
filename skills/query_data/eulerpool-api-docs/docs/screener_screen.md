---
id: "url-1262a02d"
type: "api"
title: "Stock Screener"
url: "https://eulerpool.com/developers/api/screener/screen"
description: "Filter stocks by fundamental criteria (market cap, P/E, sector, country, etc.)"
source: ""
tags: []
crawl_time: "2026-03-18T05:30:41.179Z"
metadata:
  requestMethod: "POST"
  endpoint: "/api/1/screener/screen"
  responses:
    - {"code":"200","description":"Screener results"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X POST \\\n  'https://api.eulerpool.com/api/1/screener/screen' \\\n  -H 'Accept: application/json' \\\n  -H 'Content-Type: application/json'"
  jsonExample: "[\n  {\n  \"isin\": \"US0378331005\",\n  \"ticker\": \"AAPL\",\n  \"name\": \"Apple\",\n  \"country\": \"string\",\n  \"sector\": \"string\",\n  \"industry\": \"string\",\n  \"marketCap\": 0\n}\n]"
  suggestedFilename: "screener_screen"
---

# Stock Screener

## 源URL

https://eulerpool.com/developers/api/screener/screen

## 描述

Filter stocks by fundamental criteria (market cap, P/E, sector, country, etc.)

## API 端点

**Method**: `POST`
**Endpoint**: `/api/1/screener/screen`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Screener results |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X POST \
  'https://api.eulerpool.com/api/1/screener/screen' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json'
```

### 示例 2 (json)

```json
[
  {
  "isin": "US0378331005",
  "ticker": "AAPL",
  "name": "Apple",
  "country": "string",
  "sector": "string",
  "industry": "string",
  "marketCap": 0
}
]
```

## 文档正文

Filter stocks by fundamental criteria (market cap, P/E, sector, country, etc.)

## API 端点

**Method:** `POST`
**Endpoint:** `/api/1/screener/screen`
