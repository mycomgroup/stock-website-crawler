---
id: "url-31b5d89d"
type: "api"
title: "AAQS (Quality Score) API"
url: "https://eulerpool.com/developers/api/equity/extended/aaqs"
description: "Returns the AlleAktien Quality Score (AAQS) for the given security. Evaluates companies across 10 dimensions including revenue growth, EBIT growth, profit continuity, leverage, ROE, and ROCE. Score ranges from 0 to 10."
source: ""
tags: []
crawl_time: "2026-03-18T05:33:29.456Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/aaqs/{identifier}"
  responses:
    - {"code":"200","description":"Returns AAQS data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/aaqs/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"ticker\": \"MSFT\",\n  \"score\": 9,\n  \"revenueGrowth10Y\": 0,\n  \"ebitGrowth10Y\": 0,\n  \"profitContinuity10Y\": 0,\n  \"revenueGrowth3Y\": 0,\n  \"ebitGrowth3Y\": 0,\n  \"netDebtToEBIT\": 0,\n  \"ebitMaxDrawdown10Y\": 0,\n  \"returnOnEquity\": 0,\n  \"roce\": 0,\n  \"expectedReturn\": 0\n}"
  suggestedFilename: "equity_extended_aaqs"
---

# AAQS (Quality Score) API

## 源URL

https://eulerpool.com/developers/api/equity/extended/aaqs

## 描述

Returns the AlleAktien Quality Score (AAQS) for the given security. Evaluates companies across 10 dimensions including revenue growth, EBIT growth, profit continuity, leverage, ROE, and ROCE. Score ranges from 0 to 10.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/aaqs/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns AAQS data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/aaqs/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "ticker": "MSFT",
  "score": 9,
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

Returns the AlleAktien Quality Score (AAQS) for the given security. Evaluates companies across 10 dimensions including revenue growth, EBIT growth, profit continuity, leverage, ROE, and ROCE. Score ranges from 0 to 10.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/aaqs/{identifier}`
