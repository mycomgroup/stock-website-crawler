---
id: "url-3c63d7"
type: "api"
title: "Mutual Fund Sectors"
url: "https://eulerpool.com/developers/api/mutual/fund/sectors"
description: "Returns sector allocation breakdown"
source: ""
tags: []
crawl_time: "2026-03-18T06:02:40.625Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/mutual-fund/sectors/{symbol}"
  responses:
    - {"code":"200","description":"Sector breakdown"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/mutual-fund/sectors/VFINX' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "mutual_fund_sectors"
---

# Mutual Fund Sectors

## 源URL

https://eulerpool.com/developers/api/mutual/fund/sectors

## 描述

Returns sector allocation breakdown

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/mutual-fund/sectors/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Sector breakdown |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/mutual-fund/sectors/VFINX' \
  -H 'Accept: application/json'
```

## 文档正文

Returns sector allocation breakdown

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/mutual-fund/sectors/{symbol}`
