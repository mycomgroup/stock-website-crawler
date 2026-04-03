---
id: "url-587a5d2d"
type: "api"
title: "Symbol Change History API"
url: "https://eulerpool.com/developers/api/equity/extended/symbol/changes"
description: "Returns ticker symbol changes (renames, mergers) over the past year. Useful for data quality and corporate action tracking."
source: ""
tags: []
crawl_time: "2026-03-18T06:14:54.966Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/symbol-changes"
  responses:
    - {"code":"200","description":"Returns symbol changes"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/symbol-changes?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"old_symbol\": \"FB\",\n  \"new_symbol\": \"META\",\n  \"at_date\": \"2022-06-09T00:00:00.000Z\"\n}\n]"
  suggestedFilename: "equity_extended_symbol_changes"
---

# Symbol Change History API

## 源URL

https://eulerpool.com/developers/api/equity/extended/symbol/changes

## 描述

Returns ticker symbol changes (renames, mergers) over the past year. Useful for data quality and corporate action tracking.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/symbol-changes`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns symbol changes |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/symbol-changes?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "old_symbol": "FB",
  "new_symbol": "META",
  "at_date": "2022-06-09T00:00:00.000Z"
}
]
```

## 文档正文

Returns ticker symbol changes (renames, mergers) over the past year. Useful for data quality and corporate action tracking.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/symbol-changes`
