---
id: "url-10c529dc"
type: "api"
title: "IMF Series List API"
url: "https://eulerpool.com/developers/api/macro/imf/series"
description: "Returns all available IMF (International Monetary Fund) data series by country: CPI, GDP, unemployment, exchange rates, policy rates, trade balances"
source: ""
tags: []
crawl_time: "2026-03-18T05:55:42.523Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/imf/series"
  responses:
    - {"code":"200","description":"Returns IMF series list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/imf/series?country=US' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "macro_imf_series"
---

# IMF Series List API

## 源URL

https://eulerpool.com/developers/api/macro/imf/series

## 描述

Returns all available IMF (International Monetary Fund) data series by country: CPI, GDP, unemployment, exchange rates, policy rates, trade balances

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/imf/series`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns IMF series list |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/imf/series?country=US' \
  -H 'Accept: application/json'
```

## 文档正文

Returns all available IMF (International Monetary Fund) data series by country: CPI, GDP, unemployment, exchange rates, policy rates, trade balances

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/imf/series`
