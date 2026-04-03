---
id: "url-13b6bf8b"
type: "api"
title: "Forex Rates API"
url: "https://eulerpool.com/developers/api/forex/rates"
description: "Returns current exchange rates for the specified base currency"
source: ""
tags: []
crawl_time: "2026-03-18T05:41:02.490Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/forex/rates/{basecurrency}"
  responses:
    - {"code":"200","description":"Returns exchange rates for the base currency"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Base currency not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/forex/rates/USD' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"base\": \"EUR\",\n  \"rates\": {\n    \"AED\": 3.9825,\n    \"AFN\": 74.88,\n    \"ALL\": 104.21,\n    \"AMD\": 436.8848,\n    \"ANG\": 1.9542,\n    \"AOA\": 907.8905,\n    \"ARS\": 382.5698,\n    \"AUD\": 1.6664,\n    \"AWG\": 1.9626,\n    \"AZN\": 1.8433\n  }\n}"
  suggestedFilename: "forex_rates"
---

# Forex Rates API

## 源URL

https://eulerpool.com/developers/api/forex/rates

## 描述

Returns current exchange rates for the specified base currency

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/forex/rates/{basecurrency}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns exchange rates for the base currency |
| 401 | Token not valid |
| 404 | Base currency not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/forex/rates/USD' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "base": "EUR",
  "rates": {
    "AED": 3.9825,
    "AFN": 74.88,
    "ALL": 104.21,
    "AMD": 436.8848,
    "ANG": 1.9542,
    "AOA": 907.8905,
    "ARS": 382.5698,
    "AUD": 1.6664,
    "AWG": 1.9626,
    "AZN": 1.8433
  }
}
```

## 文档正文

Returns current exchange rates for the specified base currency

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/forex/rates/{basecurrency}`
