---
id: "url-3d332ab"
type: "api"
title: "Superinvestor Recent Activity API"
url: "https://eulerpool.com/developers/api/alternative/superinvestors/recent/activity"
description: "Returns recent buy/sell activity from tracked superinvestors"
source: ""
tags: []
crawl_time: "2026-03-18T06:17:21.867Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/superinvestors/recent-activity"
  responses:
    - {"code":"200","description":"Returns recent superinvestor trades"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/superinvestors/recent-activity?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "alternative_superinvestors_recent_activity"
---

# Superinvestor Recent Activity API

## 源URL

https://eulerpool.com/developers/api/alternative/superinvestors/recent/activity

## 描述

Returns recent buy/sell activity from tracked superinvestors

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/superinvestors/recent-activity`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns recent superinvestor trades |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/superinvestors/recent-activity?limit=10' \
  -H 'Accept: application/json'
```

## 文档正文

Returns recent buy/sell activity from tracked superinvestors

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/superinvestors/recent-activity`
