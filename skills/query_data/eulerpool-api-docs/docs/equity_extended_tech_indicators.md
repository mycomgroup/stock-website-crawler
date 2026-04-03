---
id: "url-4eb2d59c"
type: "api"
title: "Technical Indicators Time Series API"
url: "https://eulerpool.com/developers/api/equity/extended/tech/indicators"
description: "Returns technical indicator time series (SMA, EMA, RSI, MACD, Bollinger Bands) for the given security. Data from Finnhub."
source: ""
tags: []
crawl_time: "2026-03-18T06:15:29.170Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/tech-indicators/{identifier}"
  responses:
    - {"code":"200","description":"Returns tech indicator data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/tech-indicators/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"indicator\": \"sma\",\n  \"resolution\": \"D\",\n  \"timestamps\": [],\n  \"values\": {},\n  \"last_updated\": \"string\"\n}\n]"
  suggestedFilename: "equity_extended_tech_indicators"
---

# Technical Indicators Time Series API

## 源URL

https://eulerpool.com/developers/api/equity/extended/tech/indicators

## 描述

Returns technical indicator time series (SMA, EMA, RSI, MACD, Bollinger Bands) for the given security. Data from Finnhub.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/tech-indicators/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns tech indicator data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/tech-indicators/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "indicator": "sma",
  "resolution": "D",
  "timestamps": [],
  "values": {},
  "last_updated": "string"
}
]
```

## 文档正文

Returns technical indicator time series (SMA, EMA, RSI, MACD, Bollinger Bands) for the given security. Data from Finnhub.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/tech-indicators/{identifier}`
