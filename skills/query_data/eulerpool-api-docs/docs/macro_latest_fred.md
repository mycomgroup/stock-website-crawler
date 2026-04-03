---
id: "url-6e41c27b"
type: "api"
title: "FRED Latest Values API"
url: "https://eulerpool.com/developers/api/macro/latest/fred"
description: "Returns the latest observation for all FRED series in a single request -- snapshot of current US macro conditions"
source: ""
tags: []
crawl_time: "2026-03-18T05:59:41.013Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/latest/fred"
  responses:
    - {"code":"200","description":"Returns latest FRED values"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/latest/fred' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "macro_latest_fred"
---

# FRED Latest Values API

## 源URL

https://eulerpool.com/developers/api/macro/latest/fred

## 描述

Returns the latest observation for all FRED series in a single request -- snapshot of current US macro conditions

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/latest/fred`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns latest FRED values |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/latest/fred' \
  -H 'Accept: application/json'
```

## 文档正文

Returns the latest observation for all FRED series in a single request -- snapshot of current US macro conditions

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/latest/fred`
