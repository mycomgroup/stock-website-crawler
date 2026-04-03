---
id: "url-5605f76f"
type: "api"
title: "KPI Bundle API"
url: "https://eulerpool.com/developers/api/equity/kpi"
description: "Returns a comprehensive bundle of key performance indicators in a single call: growth metrics, margins, valuation ratios, dividend data, AAQS score, and financial highlights. Ideal for AI agents and screeners."
source: ""
tags: []
crawl_time: "2026-03-18T05:40:41.161Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/kpi/{identifier}"
  responses:
    - {"code":"200","description":"Returns comprehensive KPI data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/kpi/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "equity_kpi"
---

# KPI Bundle API

## 源URL

https://eulerpool.com/developers/api/equity/kpi

## 描述

Returns a comprehensive bundle of key performance indicators in a single call: growth metrics, margins, valuation ratios, dividend data, AAQS score, and financial highlights. Ideal for AI agents and screeners.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/kpi/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns comprehensive KPI data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/kpi/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns a comprehensive bundle of key performance indicators in a single call: growth metrics, margins, valuation ratios, dividend data, AAQS score, and financial highlights. Ideal for AI agents and screeners.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/kpi/{identifier}`
