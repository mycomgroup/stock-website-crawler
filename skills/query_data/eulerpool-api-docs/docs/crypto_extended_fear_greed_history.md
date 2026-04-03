---
id: "url-2105443c"
type: "api"
title: "Crypto Fear & Greed History API"
url: "https://eulerpool.com/developers/api/crypto/extended/fear/greed/history"
description: "Returns daily Crypto Fear & Greed Index values with classification (Extreme Fear to Extreme Greed)"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:44.907Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/fear-greed-history"
  responses:
    - {"code":"200","description":"Returns F&G history"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/fear-greed-history' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"value\": 72,\n  \"classification\": \"Greed\"\n}\n]"
  suggestedFilename: "crypto_extended_fear_greed_history"
---

# Crypto Fear & Greed History API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/fear/greed/history

## 描述

Returns daily Crypto Fear & Greed Index values with classification (Extreme Fear to Extreme Greed)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/fear-greed-history`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns F&G history |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/fear-greed-history' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "date": "2024-01-15T00:00:00.000Z",
  "value": 72,
  "classification": "Greed"
}
]
```

## 文档正文

Returns daily Crypto Fear & Greed Index values with classification (Extreme Fear to Extreme Greed)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/fear-greed-history`
