---
id: "url-720828d4"
type: "api"
title: "Macro Calendar properties API"
url: "https://eulerpool.com/developers/api/macro/calendar/properties"
description: "Get the the available options to filter the calendar API."
source: ""
tags: []
crawl_time: "2026-03-18T06:11:56.903Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/calendar/properties"
  responses:
    - {"code":"200","description":"Returns a array of min/max timestamp values together with a country code"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/calendar/properties' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"min\": 1722498600000,\n  \"max\": 1728974700000,\n  \"country_code\": \"fr\"\n}\n]"
  suggestedFilename: "macro_calendar_properties"
---

# Macro Calendar properties API

## 源URL

https://eulerpool.com/developers/api/macro/calendar/properties

## 描述

Get the the available options to filter the calendar API.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/calendar/properties`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a array of min/max timestamp values together with a country code |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/calendar/properties' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "min": 1722498600000,
  "max": 1728974700000,
  "country_code": "fr"
}
]
```

## 文档正文

Get the the available options to filter the calendar API.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/calendar/properties`
