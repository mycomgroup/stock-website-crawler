---
id: "url-1264b2fb"
type: "api"
title: "On-Chain Metrics API"
url: "https://eulerpool.com/developers/api/crypto/extended/onchain"
description: "Returns 90-day on-chain metrics for BTC or ETH: hash rate, difficulty, active addresses, transaction count, fees, block size, supply, miner revenue, mempool, NVT ratio"
source: ""
tags: []
crawl_time: "2026-03-18T06:09:48.142Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/onchain/{symbol}"
  responses:
    - {"code":"200","description":"Returns on-chain metrics"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Symbol not found (only BTC, ETH supported)"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/onchain/BTC' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"symbol\": \"BTC\",\n  \"metrics\": {\n    \"date\": \"2024-01-15T00:00:00.000Z\",\n    \"hash_rate\": 0,\n    \"active_addresses\": 0,\n    \"tx_count\": 0,\n    \"avg_tx_fee\": 0,\n    \"miner_revenue\": 0,\n    \"market_cap\": 0\n  }\n}"
  suggestedFilename: "crypto_extended_onchain"
---

# On-Chain Metrics API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/onchain

## 描述

Returns 90-day on-chain metrics for BTC or ETH: hash rate, difficulty, active addresses, transaction count, fees, block size, supply, miner revenue, mempool, NVT ratio

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/onchain/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns on-chain metrics |
| 401 | Token not valid |
| 404 | Symbol not found (only BTC, ETH supported) |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/onchain/BTC' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "symbol": "BTC",
  "metrics": {
    "date": "2024-01-15T00:00:00.000Z",
    "hash_rate": 0,
    "active_addresses": 0,
    "tx_count": 0,
    "avg_tx_fee": 0,
    "miner_revenue": 0,
    "market_cap": 0
  }
}
```

## 文档正文

Returns 90-day on-chain metrics for BTC or ETH: hash rate, difficulty, active addresses, transaction count, fees, block size, supply, miner revenue, mempool, NVT ratio

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/onchain/{symbol}`
