---
id: "url-61a558cf"
type: "api"
title: "Commitments of Traders (COT) API"
url: "https://eulerpool.com/developers/api/alternative/cot"
description: "Returns CFTC Commitments of Traders report data for the given futures symbol"
source: ""
tags: []
crawl_time: "2026-03-18T05:54:04.018Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/cot/{symbol}"
  responses:
    - {"code":"200","description":"Returns COT data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Symbol not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/cot/CRUDE?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "alternative_cot"
---

# Commitments of Traders (COT) API

## 源URL

https://eulerpool.com/developers/api/alternative/cot

## 描述

Returns CFTC Commitments of Traders report data for the given futures symbol

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/cot/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns COT data |
| 401 | Token not valid |
| 404 | Symbol not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/cot/CRUDE?limit=10' \
  -H 'Accept: application/json'
```

## 文档正文

Returns CFTC Commitments of Traders report data for the given futures symbol

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/cot/{symbol}`
