---
id: "url-66670316"
type: "api"
title: "Stablecoin Market Caps API"
url: "https://eulerpool.com/developers/api/crypto/extended/stablecoins"
description: "Returns current and historical market capitalizations for major stablecoins (USDT, USDC, DAI, etc.)"
source: ""
tags: []
crawl_time: "2026-03-18T06:12:52.076Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/stablecoins"
  responses:
    - {"code":"200","description":"Returns stablecoin data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/stablecoins' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"current\": [],\n  \"history\": []\n}"
  suggestedFilename: "crypto_extended_stablecoins"
---

# Stablecoin Market Caps API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/stablecoins

## 描述

Returns current and historical market capitalizations for major stablecoins (USDT, USDC, DAI, etc.)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/stablecoins`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns stablecoin data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/stablecoins' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "current": [],
  "history": []
}
```

## 文档正文

Returns current and historical market capitalizations for major stablecoins (USDT, USDC, DAI, etc.)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/stablecoins`
