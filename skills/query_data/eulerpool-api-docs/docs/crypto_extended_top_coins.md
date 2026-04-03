---
id: "url-7040dd35"
type: "api"
title: "Top Cryptocurrencies API"
url: "https://eulerpool.com/developers/api/crypto/extended/top/coins"
description: "Returns top 100 cryptocurrencies ranked by market cap with price, volume, 24h/7d change, sparklines, and supply data"
source: ""
tags: []
crawl_time: "2026-03-18T05:36:01.294Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/top-coins"
  responses:
    - {"code":"200","description":"Returns top coins"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/top-coins' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"rank\": 1,\n  \"symbol\": \"BTC\",\n  \"name\": \"Bitcoin\",\n  \"price\": 62345,\n  \"market_cap\": 0,\n  \"volume_24h\": 0,\n  \"change_24h\": 2.5,\n  \"change_7d\": -1.2,\n  \"circulating_supply\": 0,\n  \"sparkline_7d\": []\n}\n]"
  suggestedFilename: "crypto_extended_top_coins"
---

# Top Cryptocurrencies API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/top/coins

## 描述

Returns top 100 cryptocurrencies ranked by market cap with price, volume, 24h/7d change, sparklines, and supply data

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/top-coins`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns top coins |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/top-coins' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "rank": 1,
  "symbol": "BTC",
  "name": "Bitcoin",
  "price": 62345,
  "market_cap": 0,
  "volume_24h": 0,
  "change_24h": 2.5,
  "change_7d": -1.2,
  "circulating_supply": 0,
  "sparkline_7d": []
}
]
```

## 文档正文

Returns top 100 cryptocurrencies ranked by market cap with price, volume, 24h/7d change, sparklines, and supply data

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/top-coins`
