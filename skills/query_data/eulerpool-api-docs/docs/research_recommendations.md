---
id: "url-42871cbb"
type: "api"
title: "Analyst Recommendations"
url: "https://eulerpool.com/developers/api/research/recommendations"
description: "Returns analyst recommendation trends (buy/hold/sell) and consensus price targets"
source: ""
tags: []
crawl_time: "2026-03-18T05:35:41.209Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/research/recommendations/{ticker}"
  responses:
    - {"code":"200","description":"Monthly recommendation history with price targets"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/research/recommendations/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"period\": \"2026-03-01T00:00:00.000Z\",\n  \"strongBuy\": 12,\n  \"buy\": 18,\n  \"hold\": 8,\n  \"sell\": 2,\n  \"strongSell\": 0,\n  \"targetMean\": 210.5,\n  \"targetMedian\": 215,\n  \"targetHigh\": 260,\n  \"targetLow\": 170,\n  \"lastQuote\": 178.72\n}\n]"
  suggestedFilename: "research_recommendations"
---

# Analyst Recommendations

## 源URL

https://eulerpool.com/developers/api/research/recommendations

## 描述

Returns analyst recommendation trends (buy/hold/sell) and consensus price targets

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/research/recommendations/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Monthly recommendation history with price targets |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/research/recommendations/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "period": "2026-03-01T00:00:00.000Z",
  "strongBuy": 12,
  "buy": 18,
  "hold": 8,
  "sell": 2,
  "strongSell": 0,
  "targetMean": 210.5,
  "targetMedian": 215,
  "targetHigh": 260,
  "targetLow": 170,
  "lastQuote": 178.72
}
]
```

## 文档正文

Returns analyst recommendation trends (buy/hold/sell) and consensus price targets

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/research/recommendations/{ticker}`
