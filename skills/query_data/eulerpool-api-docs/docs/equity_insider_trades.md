---
id: "url-500d971d"
type: "api"
title: "Insider Trades API"
url: "https://eulerpool.com/developers/api/equity/insider/trades"
description: "Returns insider trading activity for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:04:01.855Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/insider-trades/{identifier}"
  responses:
    - {"code":"200","description":"Returns insider trades data."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/insider-trades/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"name\": \"John Doe\",\n  \"relationship\": \"CEO\",\n  \"transaction\": \"Buy\",\n  \"security\": \"Common Stock\",\n  \"price\": 150.25,\n  \"shares\": 1000,\n  \"volume\": 150250,\n  \"transactionDate\": \"2023-12-15T00:00:00.000Z\",\n  \"announcementDate\": \"2023-12-16T00:00:00.000Z\",\n  \"source\": \"SEC\"\n}\n]"
  suggestedFilename: "equity_insider_trades"
---

# Insider Trades API

## 源URL

https://eulerpool.com/developers/api/equity/insider/trades

## 描述

Returns insider trading activity for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/insider-trades/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns insider trades data. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/insider-trades/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "name": "John Doe",
  "relationship": "CEO",
  "transaction": "Buy",
  "security": "Common Stock",
  "price": 150.25,
  "shares": 1000,
  "volume": 150250,
  "transactionDate": "2023-12-15T00:00:00.000Z",
  "announcementDate": "2023-12-16T00:00:00.000Z",
  "source": "SEC"
}
]
```

## 文档正文

Returns insider trading activity for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/insider-trades/{identifier}`
