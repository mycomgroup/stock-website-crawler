---
id: "url-62a90506"
type: "api"
title: "Aggregate Technical Signals API"
url: "https://eulerpool.com/developers/api/equity/extended/aggregate/signals"
description: "Returns consolidated technical indicator signals (buy/sell/neutral counts, ADX trend strength, overall signal) across multiple resolutions (1min, 5min, 15min, 30min, 1h, D, W, M)"
source: ""
tags: []
crawl_time: "2026-03-18T06:16:32.816Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/aggregate-signals/{identifier}"
  responses:
    - {"code":"200","description":"Returns aggregate signals by resolution"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/aggregate-signals/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"string\",\n  \"symbol\": \"string\",\n  \"signals\": {\n    \"resolution\": \"D\",\n    \"signal\": \"buy\",\n    \"buy\": 8,\n    \"neutral\": 3,\n    \"sell\": 1,\n    \"adx\": 32.5,\n    \"trending\": true\n  },\n  \"summary\": {\n    \"signal\": \"buy\",\n    \"buyCount\": 0,\n    \"sellCount\": 0,\n    \"neutralCount\": 0\n  }\n}"
  suggestedFilename: "equity_extended_aggregate_signals"
---

# Aggregate Technical Signals API

## 源URL

https://eulerpool.com/developers/api/equity/extended/aggregate/signals

## 描述

Returns consolidated technical indicator signals (buy/sell/neutral counts, ADX trend strength, overall signal) across multiple resolutions (1min, 5min, 15min, 30min, 1h, D, W, M)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/aggregate-signals/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns aggregate signals by resolution |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/aggregate-signals/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "string",
  "symbol": "string",
  "signals": {
    "resolution": "D",
    "signal": "buy",
    "buy": 8,
    "neutral": 3,
    "sell": 1,
    "adx": 32.5,
    "trending": true
  },
  "summary": {
    "signal": "buy",
    "buyCount": 0,
    "sellCount": 0,
    "neutralCount": 0
  }
}
```

## 文档正文

Returns consolidated technical indicator signals (buy/sell/neutral counts, ADX trend strength, overall signal) across multiple resolutions (1min, 5min, 15min, 30min, 1h, D, W, M)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/aggregate-signals/{identifier}`
