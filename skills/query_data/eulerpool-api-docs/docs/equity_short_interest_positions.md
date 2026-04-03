---
id: "url-401f554d"
type: "api"
title: "Short Interest Positions API"
url: "https://eulerpool.com/developers/api/equity/short/interest/positions"
description: "Returns FINRA bi-monthly short interest data (outstanding short positions, days to cover) for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:15:19.969Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/short-interest-positions/{identifier}"
  responses:
    - {"code":"200","description":"Returns short interest position data by settlement date (bi-monthly)."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/short-interest-positions/{identifier}?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"settlementDate\": \"2026-01-31T00:00:00.000Z\",\n  \"shortShares\": 15234000,\n  \"prevShortShares\": 14120000,\n  \"changeShares\": 1114000,\n  \"changePct\": 7.89,\n  \"avgDailyVolume\": 5800000,\n  \"daysToCover\": 2.63\n}\n]"
  suggestedFilename: "equity_short_interest_positions"
---

# Short Interest Positions API

## 源URL

https://eulerpool.com/developers/api/equity/short/interest/positions

## 描述

Returns FINRA bi-monthly short interest data (outstanding short positions, days to cover) for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/short-interest-positions/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns short interest position data by settlement date (bi-monthly). |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/short-interest-positions/{identifier}?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "settlementDate": "2026-01-31T00:00:00.000Z",
  "shortShares": 15234000,
  "prevShortShares": 14120000,
  "changeShares": 1114000,
  "changePct": 7.89,
  "avgDailyVolume": 5800000,
  "daysToCover": 2.63
}
]
```

## 文档正文

Returns FINRA bi-monthly short interest data (outstanding short positions, days to cover) for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/short-interest-positions/{identifier}`
