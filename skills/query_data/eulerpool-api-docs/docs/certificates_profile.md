---
id: "url-74a053d5"
type: "api"
title: "Certificate Profile API"
url: "https://eulerpool.com/developers/api/certificates/profile"
description: "Returns profile data for a structured product / certificate by identifier (ISIN), including underlying, strike, barrier, and issuer"
source: ""
tags: []
crawl_time: "2026-03-18T05:33:09.306Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/certificates/profile/{identifier}"
  responses:
    - {"code":"200","description":"Returns certificate profile"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/certificates/profile/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "certificates_profile"
---

# Certificate Profile API

## 源URL

https://eulerpool.com/developers/api/certificates/profile

## 描述

Returns profile data for a structured product / certificate by identifier (ISIN), including underlying, strike, barrier, and issuer

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/certificates/profile/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns certificate profile |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/certificates/profile/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns profile data for a structured product / certificate by identifier (ISIN), including underlying, strike, barrier, and issuer

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/certificates/profile/{identifier}`
