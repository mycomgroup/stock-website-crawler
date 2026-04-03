---
id: "url-27826edd"
type: "api"
title: "Eurostat Observations API"
url: "https://eulerpool.com/developers/api/macro/eurostat/observations"
description: "Returns time series data for a specific Eurostat series"
source: ""
tags: []
crawl_time: "2026-03-18T06:12:40.798Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/eurostat/observations/{seriesId}"
  responses:
    - {"code":"200","description":"Returns time series"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Series not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/eurostat/observations/eurostat_current_account_DE?limit=5' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "macro_eurostat_observations"
---

# Eurostat Observations API

## 源URL

https://eulerpool.com/developers/api/macro/eurostat/observations

## 描述

Returns time series data for a specific Eurostat series

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/eurostat/observations/{seriesId}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns time series |
| 401 | Token not valid |
| 404 | Series not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/eurostat/observations/eurostat_current_account_DE?limit=5' \
  -H 'Accept: application/json'
```

## 文档正文

Returns time series data for a specific Eurostat series

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/eurostat/observations/{seriesId}`
