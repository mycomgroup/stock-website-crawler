---
id: "url-5f89642e"
type: "api"
title: "Short Volume API"
url: "https://eulerpool.com/developers/api/equity/extended/short/volume"
description: "Returns daily short volume data from FINRA: short volume, exempt volume, total volume, and short ratio"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:53.683Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/short-volume/{identifier}"
  responses:
    - {"code":"200","description":"Returns daily short volume"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/short-volume/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"short_volume\": 5000000,\n  \"total_volume\": 12000000,\n  \"short_ratio\": 0.42\n}\n]"
  suggestedFilename: "equity_extended_short_volume"
---

# Short Volume API

## 源URL

https://eulerpool.com/developers/api/equity/extended/short/volume

## 描述

Returns daily short volume data from FINRA: short volume, exempt volume, total volume, and short ratio

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/short-volume/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns daily short volume |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/short-volume/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "date": "2024-01-15T00:00:00.000Z",
  "short_volume": 5000000,
  "total_volume": 12000000,
  "short_ratio": 0.42
}
]
```

## 文档正文

Returns daily short volume data from FINRA: short volume, exempt volume, total volume, and short ratio

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/short-volume/{identifier}`
