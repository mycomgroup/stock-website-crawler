---
id: "url-35591c72"
type: "api"
title: "Stock Returns API"
url: "https://eulerpool.com/developers/api/equity/returns"
description: "Returns annual price returns (absolute and relative) with dividend-adjusted total return for the given ISIN over a configurable lookback period"
source: ""
tags: []
crawl_time: "2026-03-18T05:49:04.120Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/returns/{identifier}"
  responses:
    - {"code":"200","description":"Returns annual performance data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/returns/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"quoteReturns\": {\n    \"year\": 2024,\n    \"returnRate\": 12.5,\n    \"startPrice\": 0,\n    \"endPrice\": 0\n  },\n  \"mean\": 15.2,\n  \"variance\": 120.5\n}"
  suggestedFilename: "equity_returns"
---

# Stock Returns API

## 源URL

https://eulerpool.com/developers/api/equity/returns

## 描述

Returns annual price returns (absolute and relative) with dividend-adjusted total return for the given ISIN over a configurable lookback period

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/returns/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns annual performance data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/returns/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "quoteReturns": {
    "year": 2024,
    "returnRate": 12.5,
    "startPrice": 0,
    "endPrice": 0
  },
  "mean": 15.2,
  "variance": 120.5
}
```

## 文档正文

Returns annual price returns (absolute and relative) with dividend-adjusted total return for the given ISIN over a configurable lookback period

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/returns/{identifier}`
