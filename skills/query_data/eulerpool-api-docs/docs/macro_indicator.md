---
id: "url-1b29f169"
type: "api"
title: "Indicator Profile API"
url: "https://eulerpool.com/developers/api/macro/indicator"
description: "Returns the full profile for a macro economic indicator in a specific country, including metadata and description"
source: ""
tags: []
crawl_time: "2026-03-18T05:53:24.660Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/indicator/{country}/{slug}"
  responses:
    - {"code":"200","description":"Returns indicator profile"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Indicator not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/indicator/US/gdp' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "macro_indicator"
---

# Indicator Profile API

## 源URL

https://eulerpool.com/developers/api/macro/indicator

## 描述

Returns the full profile for a macro economic indicator in a specific country, including metadata and description

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/indicator/{country}/{slug}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns indicator profile |
| 401 | Token not valid |
| 404 | Indicator not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/indicator/US/gdp' \
  -H 'Accept: application/json'
```

## 文档正文

Returns the full profile for a macro economic indicator in a specific country, including metadata and description

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/indicator/{country}/{slug}`
