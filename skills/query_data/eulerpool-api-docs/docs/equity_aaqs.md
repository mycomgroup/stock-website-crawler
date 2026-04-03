---
id: "url-6ab433d7"
type: "api"
title: "AAQS Quality Score API"
url: "https://eulerpool.com/developers/api/equity/aaqs"
description: "Returns the AlleAktien Quality Score (AAQS) for the given ISIN -- a proprietary 0-10 quality score evaluating revenue growth, earnings stability, profitability, balance sheet strength, and dividend track record. This metric is unique to Eulerpool and not available from any other financial data provider."
source: ""
tags: []
crawl_time: "2026-03-18T05:42:22.810Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/aaqs/{identifier}"
  responses:
    - {"code":"200","description":"Returns AAQS score and component breakdown."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found or no AAQS available"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/aaqs/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US0378331005\",\n  \"ticker\": \"AAPL\",\n  \"score\": 7,\n  \"revenueGrowth10Y\": 0,\n  \"ebitGrowth10Y\": 0,\n  \"profitContinuity10Y\": 0,\n  \"revenueGrowth3Y\": 0,\n  \"ebitGrowth3Y\": 0,\n  \"netDebtToEBIT\": 0,\n  \"ebitMaxDrawdown10Y\": 0,\n  \"returnOnEquity\": 0,\n  \"roce\": 0,\n  \"expectedReturn\": 0\n}"
  suggestedFilename: "equity_aaqs"
---

# AAQS Quality Score API

## 源URL

https://eulerpool.com/developers/api/equity/aaqs

## 描述

Returns the AlleAktien Quality Score (AAQS) for the given ISIN -- a proprietary 0-10 quality score evaluating revenue growth, earnings stability, profitability, balance sheet strength, and dividend track record. This metric is unique to Eulerpool and not available from any other financial data provider.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/aaqs/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns AAQS score and component breakdown. |
| 401 | Token not valid |
| 404 | Security not found or no AAQS available |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/aaqs/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US0378331005",
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

Returns the AlleAktien Quality Score (AAQS) for the given ISIN -- a proprietary 0-10 quality score evaluating revenue growth, earnings stability, profitability, balance sheet strength, and dividend track record. This metric is unique to Eulerpool and not available from any other financial data provider.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/aaqs/{identifier}`
