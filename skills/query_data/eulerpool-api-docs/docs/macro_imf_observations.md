---
id: "url-555c796c"
type: "api"
title: "IMF Observations API"
url: "https://eulerpool.com/developers/api/macro/imf/observations"
description: "Returns time series data for a specific IMF series"
source: ""
tags: []
crawl_time: "2026-03-18T06:06:23.741Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/imf/observations/{seriesId}"
  responses:
    - {"code":"200","description":"Returns time series observations"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Series not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/imf/observations/GDP?limit=5' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "macro_imf_observations"
---

# IMF Observations API

## 源URL

https://eulerpool.com/developers/api/macro/imf/observations

## 描述

Returns time series data for a specific IMF series

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/imf/observations/{seriesId}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns time series observations |
| 401 | Token not valid |
| 404 | Series not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/imf/observations/GDP?limit=5' \
  -H 'Accept: application/json'
```

## 文档正文

Returns time series data for a specific IMF series

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/imf/observations/{seriesId}`
