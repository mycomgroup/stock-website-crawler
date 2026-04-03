---
id: "url-33705c8f"
type: "api"
title: "AAQS Score"
url: "https://eulerpool.com/developers/api/aaqs/by/isin"
description: "Returns the AlleAktien Quality Score (AAQS) for a stock by identifier"
source: ""
tags: []
crawl_time: "2026-03-18T05:44:23.151Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/aaqs/by-isin/{identifier}"
  responses:
    - {"code":"200","description":"AAQS data"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/aaqs/by-isin/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"ticker\": \"AAPL\",\n  \"score\": 7,\n  \"revenueGrowth10Y\": 0,\n  \"ebitGrowth10Y\": 0,\n  \"profitContinuity10Y\": 0,\n  \"revenueGrowth3Y\": 0,\n  \"ebitGrowth3Y\": 0,\n  \"netDebtToEBIT\": 0,\n  \"ebitMaxDrawdown10Y\": 0,\n  \"returnOnEquity\": 0,\n  \"roce\": 0,\n  \"expectedReturn\": 0\n}"
  suggestedFilename: "aaqs_by_isin"
---

# AAQS Score

## 源URL

https://eulerpool.com/developers/api/aaqs/by/isin

## 描述

Returns the AlleAktien Quality Score (AAQS) for a stock by identifier

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/aaqs/by-isin/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | AAQS data |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/aaqs/by-isin/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "ticker": "AAPL",
  "score": 7,
  "revenueGrowth10Y": 0,
  "ebitGrowth10Y": 0,
  "profitContinuity10Y": 0,
  "revenueGrowth3Y": 0,
  "ebitGrowth3Y": 0,
  "netDebtToEBIT": 0,
  "ebitMaxDrawdown10Y": 0,
  "returnOnEquity": 0,
  "roce": 0,
  "expectedReturn": 0
}
```

## 文档正文

Returns the AlleAktien Quality Score (AAQS) for a stock by identifier

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/aaqs/by-isin/{identifier}`
