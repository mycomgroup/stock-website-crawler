---
id: "url-7d189abd"
type: "api"
title: "Price Target History API"
url: "https://eulerpool.com/developers/api/equity/extended/price/target/history"
description: "Returns historical analyst price target consensus over time for the given security. Up to 5 years of weekly snapshots including high, low, mean, median targets and analyst count."
source: ""
tags: []
crawl_time: "2026-03-18T06:17:10.437Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/price-target-history/{identifier}"
  responses:
    - {"code":"200","description":"Returns price target history"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/price-target-history/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"last_updated\": \"2024-01-15T00:00:00.000Z\",\n  \"target_high\": 250,\n  \"target_low\": 150,\n  \"target_mean\": 200,\n  \"target_median\": 195,\n  \"num_analysts\": 38\n}\n]"
  suggestedFilename: "equity_extended_price_target_history"
---

# Price Target History API

## 源URL

https://eulerpool.com/developers/api/equity/extended/price/target/history

## 描述

Returns historical analyst price target consensus over time for the given security. Up to 5 years of weekly snapshots including high, low, mean, median targets and analyst count.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/price-target-history/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns price target history |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/price-target-history/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "last_updated": "2024-01-15T00:00:00.000Z",
  "target_high": 250,
  "target_low": 150,
  "target_mean": 200,
  "target_median": 195,
  "num_analysts": 38
}
]
```

## 文档正文

Returns historical analyst price target consensus over time for the given security. Up to 5 years of weekly snapshots including high, low, mean, median targets and analyst count.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/price-target-history/{identifier}`
