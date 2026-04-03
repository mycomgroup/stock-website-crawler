---
id: "url-140cbca4"
type: "api"
title: "ISIN Change History API"
url: "https://eulerpool.com/developers/api/equity/extended/isin/changes"
description: "Returns ISIN changes over the past year. Useful for tracking security identifier changes after corporate actions."
source: ""
tags: []
crawl_time: "2026-03-18T06:14:00.048Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/isin-changes"
  responses:
    - {"code":"200","description":"Returns ISIN changes"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/isin-changes?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"old_isin\": \"US30303M1027\",\n  \"new_isin\": \"US30303M1036\",\n  \"at_date\": \"2022-06-09T00:00:00.000Z\"\n}\n]"
  suggestedFilename: "equity_extended_isin_changes"
---

# ISIN Change History API

## 源URL

https://eulerpool.com/developers/api/equity/extended/isin/changes

## 描述

Returns ISIN changes over the past year. Useful for tracking security identifier changes after corporate actions.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/isin-changes`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns ISIN changes |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/isin-changes?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "old_isin": "US30303M1027",
  "new_isin": "US30303M1036",
  "at_date": "2022-06-09T00:00:00.000Z"
}
]
```

## 文档正文

Returns ISIN changes over the past year. Useful for tracking security identifier changes after corporate actions.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/isin-changes`
