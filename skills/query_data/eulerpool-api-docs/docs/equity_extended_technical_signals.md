---
id: "url-24eabe98"
type: "api"
title: "Technical Signals API"
url: "https://eulerpool.com/developers/api/equity/extended/technical/signals"
description: "Returns aggregate technical indicator signals (buy/sell/neutral counts) and trend data for the given security"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:20.158Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/technical-signals/{identifier}"
  responses:
    - {"code":"200","description":"Returns technical signals"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/technical-signals/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"buy\": 6,\n  \"neutral\": 7,\n  \"sell\": 4,\n  \"signal\": \"neutral\",\n  \"adx\": 24.46,\n  \"trending\": false\n}"
  suggestedFilename: "equity_extended_technical_signals"
---

# Technical Signals API

## 源URL

https://eulerpool.com/developers/api/equity/extended/technical/signals

## 描述

Returns aggregate technical indicator signals (buy/sell/neutral counts) and trend data for the given security

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/technical-signals/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns technical signals |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/technical-signals/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "buy": 6,
  "neutral": 7,
  "sell": 4,
  "signal": "neutral",
  "adx": 24.46,
  "trending": false
}
```

## 文档正文

Returns aggregate technical indicator signals (buy/sell/neutral counts) and trend data for the given security

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/technical-signals/{identifier}`
