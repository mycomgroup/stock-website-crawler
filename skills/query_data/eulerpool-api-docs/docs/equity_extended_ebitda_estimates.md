---
id: "url-3df8a09e"
type: "api"
title: "EBITDA Estimates API"
url: "https://eulerpool.com/developers/api/equity/extended/ebitda/estimates"
description: "Returns analyst EBITDA estimates for the given security"
source: ""
tags: []
crawl_time: "2026-03-18T06:15:54.348Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/ebitda-estimates/{identifier}"
  responses:
    - {"code":"200","description":"Returns EBITDA estimates"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/ebitda-estimates/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"period\": \"2024-12-31T00:00:00.000Z\",\n  \"ebitda_avg\": 58800000000,\n  \"ebitda_high\": 64060000000,\n  \"ebitda_low\": 54072000000,\n  \"number_analysts\": 31\n}\n]"
  suggestedFilename: "equity_extended_ebitda_estimates"
---

# EBITDA Estimates API

## 源URL

https://eulerpool.com/developers/api/equity/extended/ebitda/estimates

## 描述

Returns analyst EBITDA estimates for the given security

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/ebitda-estimates/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns EBITDA estimates |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/ebitda-estimates/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "period": "2024-12-31T00:00:00.000Z",
  "ebitda_avg": 58800000000,
  "ebitda_high": 64060000000,
  "ebitda_low": 54072000000,
  "number_analysts": 31
}
]
```

## 文档正文

Returns analyst EBITDA estimates for the given security

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/ebitda-estimates/{identifier}`
