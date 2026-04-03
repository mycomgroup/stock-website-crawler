---
id: "url-4b80b884"
type: "api"
title: "Crypto Funding Rates API"
url: "https://eulerpool.com/developers/api/crypto/extended/funding/rates"
description: "Returns Binance perpetual futures funding rate time series for the given crypto pair. Funding rate is the #1 signal for crypto futures traders."
source: ""
tags: []
crawl_time: "2026-03-18T06:14:37.266Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/crypto-extended/funding-rates/{symbol}"
  responses:
    - {"code":"200","description":"Returns funding rate time series"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/crypto-extended/funding-rates/BTC' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"BTCUSDT\",\n  \"funding_time\": 1705276800000,\n  \"funding_rate\": 0.0001\n}\n]"
  suggestedFilename: "crypto_extended_funding_rates"
---

# Crypto Funding Rates API

## 源URL

https://eulerpool.com/developers/api/crypto/extended/funding/rates

## 描述

Returns Binance perpetual futures funding rate time series for the given crypto pair. Funding rate is the #1 signal for crypto futures traders.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/crypto-extended/funding-rates/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns funding rate time series |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/crypto-extended/funding-rates/BTC' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "BTCUSDT",
  "funding_time": 1705276800000,
  "funding_rate": 0.0001
}
]
```

## 文档正文

Returns Binance perpetual futures funding rate time series for the given crypto pair. Funding rate is the #1 signal for crypto futures traders.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/crypto-extended/funding-rates/{symbol}`
