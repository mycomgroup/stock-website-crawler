---
id: "url-1267e94b"
type: "api"
title: "Certificate Quotes API"
url: "https://eulerpool.com/developers/api/certificates/quotes"
description: "Returns historical price data for a certificate by identifier (ISIN)"
source: ""
tags: []
crawl_time: "2026-03-18T06:01:39.810Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/certificates/quotes/{identifier}"
  responses:
    - {"code":"200","description":"Returns certificate price history"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/certificates/quotes/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"timestamp\": 1705276800000,\n  \"price\": 102.5\n}\n]"
  suggestedFilename: "certificates_quotes"
---

# Certificate Quotes API

## 源URL

https://eulerpool.com/developers/api/certificates/quotes

## 描述

Returns historical price data for a certificate by identifier (ISIN)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/certificates/quotes/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns certificate price history |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/certificates/quotes/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "timestamp": 1705276800000,
  "price": 102.5
}
]
```

## 文档正文

Returns historical price data for a certificate by identifier (ISIN)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/certificates/quotes/{identifier}`
