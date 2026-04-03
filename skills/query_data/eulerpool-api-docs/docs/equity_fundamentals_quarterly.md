---
id: "url-c26e48d"
type: "api"
title: "Quarterly Fundamentals API"
url: "https://eulerpool.com/developers/api/equity/fundamentals/quarterly"
description: "Returns quarterly fundamental data (revenue, earnings, EPS, margins) in a consolidated view for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:14:07.983Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/fundamentals-quarterly/{identifier}"
  responses:
    - {"code":"200","description":"Returns quarterly fundamentals."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/fundamentals-quarterly/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "equity_fundamentals_quarterly"
---

# Quarterly Fundamentals API

## 源URL

https://eulerpool.com/developers/api/equity/fundamentals/quarterly

## 描述

Returns quarterly fundamental data (revenue, earnings, EPS, margins) in a consolidated view for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/fundamentals-quarterly/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns quarterly fundamentals. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/fundamentals-quarterly/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns quarterly fundamental data (revenue, earnings, EPS, margins) in a consolidated view for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/fundamentals-quarterly/{identifier}`
