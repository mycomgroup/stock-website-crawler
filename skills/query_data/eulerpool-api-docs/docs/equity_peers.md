---
id: "url-1358b3a4"
type: "api"
title: "Company Peers API"
url: "https://eulerpool.com/developers/api/equity/peers"
description: "Returns similar companies/peers for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:43:43.322Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/peers/{identifier}"
  responses:
    - {"code":"200","description":"Returns peer companies."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/peers/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"ticker\": \"MSFT\",\n  \"peer_name\": \"Microsoft Corporation\",\n  \"peer_isin\": \"US5949181045\",\n  \"logo\": \"/api/logo/isin/US9285634021\"\n}\n]"
  suggestedFilename: "equity_peers"
---

# Company Peers API

## 源URL

https://eulerpool.com/developers/api/equity/peers

## 描述

Returns similar companies/peers for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/peers/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns peer companies. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/peers/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "ticker": "MSFT",
  "peer_name": "Microsoft Corporation",
  "peer_isin": "US5949181045",
  "logo": "/api/logo/isin/US9285634021"
}
]
```

## 文档正文

Returns similar companies/peers for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/peers/{identifier}`
