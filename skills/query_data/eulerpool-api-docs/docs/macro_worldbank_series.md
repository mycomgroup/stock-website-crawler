---
id: "url-1a2c7950"
type: "api"
title: "World Bank Series List API"
url: "https://eulerpool.com/developers/api/macro/worldbank/series"
description: "Returns all available World Bank indicator series: GDP, population, unemployment, inflation, trade, education, health across all countries"
source: ""
tags: []
crawl_time: "2026-03-18T06:06:44.378Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/worldbank/series"
  responses:
    - {"code":"200","description":"Returns World Bank series list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/worldbank/series?country=US' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "macro_worldbank_series"
---

# World Bank Series List API

## 源URL

https://eulerpool.com/developers/api/macro/worldbank/series

## 描述

Returns all available World Bank indicator series: GDP, population, unemployment, inflation, trade, education, health across all countries

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/worldbank/series`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns World Bank series list |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/worldbank/series?country=US' \
  -H 'Accept: application/json'
```

## 文档正文

Returns all available World Bank indicator series: GDP, population, unemployment, inflation, trade, education, health across all countries

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/worldbank/series`
