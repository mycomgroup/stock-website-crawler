---
id: "url-8670451"
type: "api"
title: "Crypto Market Overview API"
url: "https://eulerpool.com/developers/api/crypto/extended/market/overview"
description: "Returns a comprehensive crypto market overview: Fear & Greed index, top gainers/losers, DeFi TVL by chain, top DeFi protocols, stablecoin market caps, and bridge volumes"
source: ""
tags: []
crawl_time: "2026-03-18T06:15:36.738Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/market-overview"
  responses:
    - {"code":"200","description":"Returns market overview"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/market-overview' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"fearGreed\": [],\n  \"topGainers\": [],\n  \"topLosers\": [],\n  \"defiProtocols\": [],\n  \"stablecoins\": [],\n  \"bridges\": [],\n  \"totalTvlHistory\": [],\n  \"chainTvl\": []\n}"
  suggestedFilename: "crypto_extended_market_overview"
---

# Crypto Market Overview API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/market/overview

## 描述

Returns a comprehensive crypto market overview: Fear & Greed index, top gainers/losers, DeFi TVL by chain, top DeFi protocols, stablecoin market caps, and bridge volumes

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/market-overview`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns market overview |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/market-overview' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "fearGreed": [],
  "topGainers": [],
  "topLosers": [],
  "defiProtocols": [],
  "stablecoins": [],
  "bridges": [],
  "totalTvlHistory": [],
  "chainTvl": []
}
```

## 文档正文

Returns a comprehensive crypto market overview: Fear & Greed index, top gainers/losers, DeFi TVL by chain, top DeFi protocols, stablecoin market caps, and bridge volumes

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/market-overview`
