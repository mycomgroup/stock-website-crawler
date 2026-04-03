---
id: "url-7b9ae31"
type: "api"
title: "Sector Metrics API"
url: "https://eulerpool.com/developers/api/sentiment/sector/metrics"
description: "Returns average and median financial ratios by sector for a given region"
source: ""
tags: []
crawl_time: "2026-03-18T06:11:37.025Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/sentiment/sector-metrics"
  responses:
    - {"code":"200","description":"Returns sector metrics keyed by sector name"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/sentiment/sector-metrics' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "sentiment_sector_metrics"
---

# Sector Metrics API

## 源URL

https://eulerpool.com/developers/api/sentiment/sector/metrics

## 描述

Returns average and median financial ratios by sector for a given region

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/sentiment/sector-metrics`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns sector metrics keyed by sector name |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/sentiment/sector-metrics' \
  -H 'Accept: application/json'
```

## 文档正文

Returns average and median financial ratios by sector for a given region

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/sentiment/sector-metrics`
