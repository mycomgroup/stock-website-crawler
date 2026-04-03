---
id: "url-7439b825"
type: "api"
title: "DeFi Fees & Revenue API"
url: "https://eulerpool.com/developers/api/crypto/extended/defi/fees"
description: "Returns daily protocol fees and revenue for DeFi protocols. Protocol revenue is the \"earnings\" equivalent for DeFi — critical for fundamental analysis."
source: ""
tags: []
crawl_time: "2026-03-18T06:12:10.096Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/defi-fees"
  responses:
    - {"code":"200","description":"Returns DeFi fees/revenue"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/defi-fees' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"protocol\": \"uniswap\",\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"total_fees\": 2500000,\n  \"total_revenue\": 500000\n}\n]"
  suggestedFilename: "crypto_extended_defi_fees"
---

# DeFi Fees & Revenue API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/defi/fees

## 描述

Returns daily protocol fees and revenue for DeFi protocols. Protocol revenue is the "earnings" equivalent for DeFi — critical for fundamental analysis.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/defi-fees`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns DeFi fees/revenue |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/defi-fees' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "protocol": "uniswap",
  "date": "2024-01-15T00:00:00.000Z",
  "total_fees": 2500000,
  "total_revenue": 500000
}
]
```

## 文档正文

Returns daily protocol fees and revenue for DeFi protocols. Protocol revenue is the "earnings" equivalent for DeFi — critical for fundamental analysis.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/defi-fees`
