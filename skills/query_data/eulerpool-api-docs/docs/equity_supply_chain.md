---
id: "url-4337d236"
type: "api"
title: "Supply Chain API"
url: "https://eulerpool.com/developers/api/equity/supply/chain"
description: "Returns supply chain relationships for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:01:59.750Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/supply-chain/{identifier}"
  responses:
    - {"code":"200","description":"Returns supply chain data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/supply-chain/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"parentSymbol\": \"AAPL\",\n  \"customer\": true,\n  \"name\": \"Supplier Company\",\n  \"oneMonthCorrelation\": 0.75,\n  \"oneYearCorrelation\": 0.82,\n  \"sixMonthCorrelation\": 0.78,\n  \"supplier\": false,\n  \"symbol\": \"SUPP\",\n  \"threeMonthCorrelation\": 0.76,\n  \"twoWeekCorrelation\": 0.73,\n  \"twoYearCorrelation\": 0.85,\n  \"country\": \"US\",\n  \"industry\": \"Technology\"\n}\n]"
  suggestedFilename: "equity_supply_chain"
---

# Supply Chain API

## 源URL

https://eulerpool.com/developers/api/equity/supply/chain

## 描述

Returns supply chain relationships for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/supply-chain/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns supply chain data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/supply-chain/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "parentSymbol": "AAPL",
  "customer": true,
  "name": "Supplier Company",
  "oneMonthCorrelation": 0.75,
  "oneYearCorrelation": 0.82,
  "sixMonthCorrelation": 0.78,
  "supplier": false,
  "symbol": "SUPP",
  "threeMonthCorrelation": 0.76,
  "twoWeekCorrelation": 0.73,
  "twoYearCorrelation": 0.85,
  "country": "US",
  "industry": "Technology"
}
]
```

## 文档正文

Returns supply chain relationships for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/supply-chain/{identifier}`
