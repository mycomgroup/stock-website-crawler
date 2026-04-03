---
id: "url-2ad65cb6"
type: "api"
title: "Risk & Return Analytics"
url: "https://eulerpool.com/developers/api/market/analytics/risk"
description: "Returns volatility, max drawdown, Sharpe ratio, and return statistics for a stock"
source: ""
tags: []
crawl_time: "2026-03-18T06:05:23.121Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/analytics/risk/{identifier}"
  responses:
    - {"code":"200","description":"Risk and return analytics"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/analytics/risk/{identifier}?range=1y&riskFreeRate=4.5' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"string\",\n  \"range\": \"string\",\n  \"dataPoints\": 0,\n  \"totalReturn\": 15.3,\n  \"annualizedReturn\": 15.3,\n  \"dailyVolatility\": 1.82,\n  \"annualizedVolatility\": 28.9,\n  \"sharpeRatio\": 0.85,\n  \"sortinoRatio\": 1.12,\n  \"maxDrawdown\": -18.4,\n  \"maxDrawdownStart\": 0,\n  \"maxDrawdownEnd\": 0,\n  \"variance\": 0,\n  \"skewness\": 0,\n  \"kurtosis\": 0,\n  \"bestDay\": 5.2,\n  \"worstDay\": -4.8\n}"
  suggestedFilename: "market_analytics_risk"
---

# Risk & Return Analytics

## 源URL

https://eulerpool.com/developers/api/market/analytics/risk

## 描述

Returns volatility, max drawdown, Sharpe ratio, and return statistics for a stock

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/analytics/risk/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Risk and return analytics |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/analytics/risk/{identifier}?range=1y&riskFreeRate=4.5' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "string",
  "range": "string",
  "dataPoints": 0,
  "totalReturn": 15.3,
  "annualizedReturn": 15.3,
  "dailyVolatility": 1.82,
  "annualizedVolatility": 28.9,
  "sharpeRatio": 0.85,
  "sortinoRatio": 1.12,
  "maxDrawdown": -18.4,
  "maxDrawdownStart": 0,
  "maxDrawdownEnd": 0,
  "variance": 0,
  "skewness": 0,
  "kurtosis": 0,
  "bestDay": 5.2,
  "worstDay": -4.8
}
```

## 文档正文

Returns volatility, max drawdown, Sharpe ratio, and return statistics for a stock

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/analytics/risk/{identifier}`
