---
id: "url-5acd40f"
type: "api"
title: "Options Chain API"
url: "https://eulerpool.com/developers/api/equity/extended/options/chain"
description: "Returns the current options chain (calls and puts) for the given security from CBOE"
source: ""
tags: []
crawl_time: "2026-03-18T06:14:25.578Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/options-chain/{identifier}"
  responses:
    - {"code":"200","description":"Returns options chain data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/options-chain/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "equity_extended_options_chain"
---

# Options Chain API

## 源URL

https://eulerpool.com/developers/api/equity/extended/options/chain

## 描述

Returns the current options chain (calls and puts) for the given security from CBOE

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/options-chain/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns options chain data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/options-chain/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns the current options chain (calls and puts) for the given security from CBOE

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/options-chain/{identifier}`
