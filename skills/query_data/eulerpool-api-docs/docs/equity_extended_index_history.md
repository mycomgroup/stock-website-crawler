---
id: "url-3bff856"
type: "api"
title: "Index Historical Constituents API"
url: "https://eulerpool.com/developers/api/equity/extended/index/history"
description: "Returns historical additions and removals from a stock market index (S&P 500, etc.)"
source: ""
tags: []
crawl_time: "2026-03-18T06:14:31.276Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/index-history/{symbol}"
  responses:
    - {"code":"200","description":"Returns index constituent changes"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/index-history/sp500' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"action\": \"add\",\n  \"ticker\": \"UBER\",\n  \"name\": \"Uber Technologies\",\n  \"effective_date\": \"2023-12-18T00:00:00.000Z\"\n}\n]"
  suggestedFilename: "equity_extended_index_history"
---

# Index Historical Constituents API

## 源URL

https://eulerpool.com/developers/api/equity/extended/index/history

## 描述

Returns historical additions and removals from a stock market index (S&P 500, etc.)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/index-history/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns index constituent changes |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/index-history/sp500' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "action": "add",
  "ticker": "UBER",
  "name": "Uber Technologies",
  "effective_date": "2023-12-18T00:00:00.000Z"
}
]
```

## 文档正文

Returns historical additions and removals from a stock market index (S&P 500, etc.)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/index-history/{symbol}`
