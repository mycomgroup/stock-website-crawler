---
id: "url-44ce5530"
type: "api"
title: "Margin Data API"
url: "https://eulerpool.com/developers/api/equity/margins"
description: "Returns current profitability margins: gross margin, operating margin, net margin, and FCF margin"
source: ""
tags: []
crawl_time: "2026-03-18T05:49:24.242Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/margins/{identifier}"
  responses:
    - {"code":"200","description":"Returns margin data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/margins/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US0378331005\",\n  \"grossMargin\": 45.6,\n  \"operatingMargin\": 30.2,\n  \"netMargin\": 25.1,\n  \"fcfMargin\": 28.3\n}"
  suggestedFilename: "equity_margins"
---

# Margin Data API

## 源URL

https://eulerpool.com/developers/api/equity/margins

## 描述

Returns current profitability margins: gross margin, operating margin, net margin, and FCF margin

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/margins/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns margin data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/margins/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US0378331005",
  "grossMargin": 45.6,
  "operatingMargin": 30.2,
  "netMargin": 25.1,
  "fcfMargin": 28.3
}
```

## 文档正文

Returns current profitability margins: gross margin, operating margin, net margin, and FCF margin

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/margins/{identifier}`
