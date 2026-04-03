---
id: "url-10d0707f"
type: "api"
title: "Congress Trading API"
url: "https://eulerpool.com/developers/api/alternative/congress/trading"
description: "Returns recent stock trades disclosed by members of US Congress"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:47.529Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/congress-trading"
  responses:
    - {"code":"200","description":"Returns congress trading data"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/congress-trading?symbol=AAPL&limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"politician\": \"Nancy Pelosi\",\n  \"symbol\": \"NVDA\",\n  \"transaction_type\": \"Purchase\",\n  \"amount_from\": 100001,\n  \"amount_to\": 250000,\n  \"transaction_date\": \"2024-01-15T00:00:00.000Z\",\n  \"filing_date\": \"2024-02-01T00:00:00.000Z\",\n  \"chamber\": \"House\"\n}\n]"
  suggestedFilename: "alternative_congress_trading"
---

# Congress Trading API

## 源URL

https://eulerpool.com/developers/api/alternative/congress/trading

## 描述

Returns recent stock trades disclosed by members of US Congress

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/congress-trading`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns congress trading data |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/congress-trading?symbol=AAPL&limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "politician": "Nancy Pelosi",
  "symbol": "NVDA",
  "transaction_type": "Purchase",
  "amount_from": 100001,
  "amount_to": 250000,
  "transaction_date": "2024-01-15T00:00:00.000Z",
  "filing_date": "2024-02-01T00:00:00.000Z",
  "chamber": "House"
}
]
```

## 文档正文

Returns recent stock trades disclosed by members of US Congress

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/congress-trading`
