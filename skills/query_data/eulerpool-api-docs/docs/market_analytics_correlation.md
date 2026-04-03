---
id: "url-417bfe45"
type: "api"
title: "Stock Correlation"
url: "https://eulerpool.com/developers/api/market/analytics/correlation"
description: "Returns the correlation coefficient and beta between two stocks over a given time range"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:41.132Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/analytics/correlation"
  responses:
    - {"code":"200","description":"Correlation data"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/analytics/correlation?isin1=US0378331005&isin2=US5949181045&range=1y' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin1\": \"string\",\n  \"isin2\": \"string\",\n  \"range\": \"string\",\n  \"correlation\": 0.72,\n  \"beta\": 1.15,\n  \"covariance\": 0,\n  \"dataPoints\": 0\n}"
  suggestedFilename: "market_analytics_correlation"
---

# Stock Correlation

## 源URL

https://eulerpool.com/developers/api/market/analytics/correlation

## 描述

Returns the correlation coefficient and beta between two stocks over a given time range

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/analytics/correlation`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Correlation data |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/analytics/correlation?isin1=US0378331005&isin2=US5949181045&range=1y' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin1": "string",
  "isin2": "string",
  "range": "string",
  "correlation": 0.72,
  "beta": 1.15,
  "covariance": 0,
  "dataPoints": 0
}
```

## 文档正文

Returns the correlation coefficient and beta between two stocks over a given time range

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/analytics/correlation`
