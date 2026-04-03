---
id: "url-55fe12b9"
type: "api"
title: "Bond Yield Curve API"
url: "https://eulerpool.com/developers/api/bonds/yield/curve"
description: "Returns the latest Treasury yield curve data across maturities"
source: ""
tags: []
crawl_time: "2026-03-18T05:58:21.474Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/bonds/yield-curve"
  responses:
    - {"code":"200","description":"Returns yield curve data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/bonds/yield-curve' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"code\": \"10y\",\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"maturity_json\": {}\n}\n]"
  suggestedFilename: "bonds_yield_curve"
---

# Bond Yield Curve API

## 源URL

https://eulerpool.com/developers/api/bonds/yield/curve

## 描述

Returns the latest Treasury yield curve data across maturities

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/bonds/yield-curve`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns yield curve data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/bonds/yield-curve' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "code": "10y",
  "date": "2024-01-15T00:00:00.000Z",
  "maturity_json": {}
}
]
```

## 文档正文

Returns the latest Treasury yield curve data across maturities

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/bonds/yield-curve`
