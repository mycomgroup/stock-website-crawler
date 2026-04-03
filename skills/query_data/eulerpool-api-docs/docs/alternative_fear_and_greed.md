---
id: "url-24661aa7"
type: "api"
title: "Fear & Greed Index API"
url: "https://eulerpool.com/developers/api/alternative/fear/and/greed"
description: "Returns the current market Fear & Greed Index value and historical data"
source: ""
tags: []
crawl_time: "2026-03-18T06:12:27.907Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/fear-and-greed"
  responses:
    - {"code":"200","description":"Returns Fear & Greed index data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/fear-and-greed' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"value\": 65,\n  \"classification\": \"Greed\",\n  \"timestamp\": \"2024-01-15T00:00:00.000Z\"\n}"
  suggestedFilename: "alternative_fear_and_greed"
---

# Fear & Greed Index API

## 源URL

https://eulerpool.com/developers/api/alternative/fear/and/greed

## 描述

Returns the current market Fear & Greed Index value and historical data

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/fear-and-greed`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns Fear & Greed index data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/fear-and-greed' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "value": 65,
  "classification": "Greed",
  "timestamp": "2024-01-15T00:00:00.000Z"
}
```

## 文档正文

Returns the current market Fear & Greed Index value and historical data

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/fear-and-greed`
