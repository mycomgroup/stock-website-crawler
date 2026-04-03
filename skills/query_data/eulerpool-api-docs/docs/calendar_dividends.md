---
id: "url-69d859e8"
type: "api"
title: "Dividend Calendar"
url: "https://eulerpool.com/developers/api/calendar/dividends"
description: "Returns ex-dividend dates and amounts for a given year"
source: ""
tags: []
crawl_time: "2026-03-18T06:00:20.605Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/calendar/dividends/{year}"
  responses:
    - {"code":"200","description":"Nested object: { year: { month: { day: [entries] } } }"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/calendar/dividends/2025' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "calendar_dividends"
---

# Dividend Calendar

## 源URL

https://eulerpool.com/developers/api/calendar/dividends

## 描述

Returns ex-dividend dates and amounts for a given year

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/calendar/dividends/{year}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Nested object: { year: { month: { day: [entries] } } } |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/calendar/dividends/2025' \
  -H 'Accept: application/json'
```

## 文档正文

Returns ex-dividend dates and amounts for a given year

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/calendar/dividends/{year}`
