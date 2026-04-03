---
id: "url-61d7b7f3"
type: "api"
title: "Eurostat Series List API"
url: "https://eulerpool.com/developers/api/macro/eurostat/series"
description: "Returns all available Eurostat data series for European Union statistics"
source: ""
tags: []
crawl_time: "2026-03-18T06:04:22.021Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/eurostat/series"
  responses:
    - {"code":"200","description":"Returns Eurostat series list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/eurostat/series?country=US' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "macro_eurostat_series"
---

# Eurostat Series List API

## 源URL

https://eulerpool.com/developers/api/macro/eurostat/series

## 描述

Returns all available Eurostat data series for European Union statistics

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/eurostat/series`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns Eurostat series list |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/eurostat/series?country=US' \
  -H 'Accept: application/json'
```

## 文档正文

Returns all available Eurostat data series for European Union statistics

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/eurostat/series`
