---
id: "url-3dd9c4f2"
type: "api"
title: "Financial Metrics & Ratios API"
url: "https://eulerpool.com/developers/api/equity/metrics"
description: "Returns 40+ computed financial ratios for the given ISIN: valuation (P/E, P/B, P/S, EV/EBITDA), profitability (ROE, ROA, ROIC, margins), per-share data (EPS, BPS, SPS, DPS), leverage (D/E, current ratio), and growth rates (3Y, 5Y, 10Y revenue/earnings/EBIT growth)"
source: ""
tags: []
crawl_time: "2026-03-18T05:48:24.153Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/metrics/{identifier}"
  responses:
    - {"code":"200","description":"Returns comprehensive financial metrics."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/metrics/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US0378331005\",\n  \"ticker\": \"AAPL\",\n  \"currency\": \"USD\",\n  \"valuation\": {\n    \"pe\": 28.5,\n    \"ps\": 7.2,\n    \"pb\": 45.1,\n    \"pebit\": 22.3,\n    \"evEbitda\": 19.8,\n    \"marketCap\": 0,\n    \"enterpriseValue\": 0\n  },\n  \"profitability\": {\n    \"roe\": 147.5,\n    \"roa\": 28.3,\n    \"roic\": 45.2,\n    \"roce\": 55.1,\n    \"grossMargin\": 45.2,\n    \"operatingMargin\": 30.1,\n    \"netMargin\": 25.3\n  },\n  \"perShare\": {\n    \"eps\": 6.13,\n    \"sps\": 24.32,\n    \"bps\": 3.95,\n    \"dps\": 0.96,\n    \"dividendYield\": 0.55\n  },\n  \"leverage\": {\n    \"debtToEquity\": 1.87,\n    \"netDebt\": 0,\n    \"currentRatio\": 0.99\n  },\n  \"growth\": {\n    \"revenueGrowth3Y\": 8.5,\n    \"revenueGrowth5Y\": 11.2,\n    \"earningsGrowth3Y\": 12.1,\n    \"earningsGrowth5Y\": 15.8\n  },\n  \"other\": {\n    \"shares\": 0,\n    \"employees\": 0,\n    \"aaqs\": 0\n  },\n  \"historical\": []\n}"
  suggestedFilename: "equity_metrics"
---

# Financial Metrics & Ratios API

## 源URL

https://eulerpool.com/developers/api/equity/metrics

## 描述

Returns 40+ computed financial ratios for the given ISIN: valuation (P/E, P/B, P/S, EV/EBITDA), profitability (ROE, ROA, ROIC, margins), per-share data (EPS, BPS, SPS, DPS), leverage (D/E, current ratio), and growth rates (3Y, 5Y, 10Y revenue/earnings/EBIT growth)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/metrics/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns comprehensive financial metrics. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/metrics/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US0378331005",
  "ticker": "AAPL",
  "currency": "USD",
  "valuation": {
    "pe": 28.5,
    "ps": 7.2,
    "pb": 45.1,
    "pebit": 22.3,
    "evEbitda": 19.8,
    "marketCap": 0,
    "enterpriseValue": 0
  },
  "profitability": {
    "roe": 147.5,
    "roa": 28.3,
    "roic": 45.2,
    "roce": 55.1,
    "grossMargin": 45.2,
    "operatingMargin": 30.1,
    "netMargin": 25.3
  },
  "perShare": {
    "eps": 6.13,
    "sps": 24.32,
    "bps": 3.95,
    "dps": 0.96,
    "dividendYield": 0.55
  },
  "leverage": {
    "debtToEquity": 1.87,
    "netDebt": 0,
    "currentRatio": 0.99
  },
  "growth": {
    "revenueGrowth3Y": 8.5,
    "revenueGrowth5Y": 11.2,
    "earningsGrowth3Y": 12.1,
    "earningsGrowth5Y": 15.8
  },
  "other": {
    "shares": 0,
    "employees": 0,
    "aaqs": 0
  },
  "historical": []
}
```

## 文档正文

Returns 40+ computed financial ratios for the given ISIN: valuation (P/E, P/B, P/S, EV/EBITDA), profitability (ROE, ROA, ROIC, margins), per-share data (EPS, BPS, SPS, DPS), leverage (D/E, current ratio), and growth rates (3Y, 5Y, 10Y revenue/earnings/EBIT growth)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/metrics/{identifier}`
