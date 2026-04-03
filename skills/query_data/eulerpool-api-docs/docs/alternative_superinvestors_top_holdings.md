---
id: "url-7e023de"
type: "api"
title: "Superinvestor Top Holdings API"
url: "https://eulerpool.com/developers/api/alternative/superinvestors/top/holdings"
description: "Returns the most popular holdings across all tracked superinvestors"
source: ""
tags: []
crawl_time: "2026-03-18T06:17:16.243Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/superinvestors/top-holdings"
  responses:
    - {"code":"200","description":"Returns top holdings across superinvestors"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/superinvestors/top-holdings?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "alternative_superinvestors_top_holdings"
---

# Superinvestor Top Holdings API

## 源URL

https://eulerpool.com/developers/api/alternative/superinvestors/top/holdings

## 描述

Returns the most popular holdings across all tracked superinvestors

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/superinvestors/top-holdings`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns top holdings across superinvestors |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/superinvestors/top-holdings?limit=10' \
  -H 'Accept: application/json'
```

## 文档正文

Returns the most popular holdings across all tracked superinvestors

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/superinvestors/top-holdings`
