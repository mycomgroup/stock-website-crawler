---
id: "url-7a1f61e0"
type: "api"
title: "World Bank Observations API"
url: "https://eulerpool.com/developers/api/macro/worldbank/observations"
description: "Returns time series data for a specific World Bank indicator series"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:34.809Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/worldbank/observations/{seriesId}"
  responses:
    - {"code":"200","description":"Returns time series"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Series not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/worldbank/observations/wb_NY.GDP.PCAP.CD_USA?limit=5' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "macro_worldbank_observations"
---

# World Bank Observations API

## 源URL

https://eulerpool.com/developers/api/macro/worldbank/observations

## 描述

Returns time series data for a specific World Bank indicator series

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/worldbank/observations/{seriesId}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns time series |
| 401 | Token not valid |
| 404 | Series not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/worldbank/observations/wb_NY.GDP.PCAP.CD_USA?limit=5' \
  -H 'Accept: application/json'
```

## 文档正文

Returns time series data for a specific World Bank indicator series

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/worldbank/observations/{seriesId}`
