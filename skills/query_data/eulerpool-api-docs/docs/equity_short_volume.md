---
id: "url-5629bca2"
type: "api"
title: "Short Volume API"
url: "https://eulerpool.com/developers/api/equity/short/volume"
description: "Returns FINRA short volume data for the given ISIN (US equities)"
source: ""
tags: []
crawl_time: "2026-03-18T06:02:19.921Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/short-volume/{identifier}"
  responses:
    - {"code":"200","description":"Returns short volume data by trading day."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/short-volume/{identifier}?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"date\": \"2026-02-20T00:00:00.000Z\",\n  \"shortVolume\": 5234000,\n  \"shortExemptVolume\": 120000,\n  \"totalVolume\": 12500000,\n  \"shortRatio\": 0.4283,\n  \"market\": \"Q\"\n}\n]"
  suggestedFilename: "equity_short_volume"
---

# Short Volume API

## 源URL

https://eulerpool.com/developers/api/equity/short/volume

## 描述

Returns FINRA short volume data for the given ISIN (US equities)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/short-volume/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns short volume data by trading day. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/short-volume/{identifier}?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "date": "2026-02-20T00:00:00.000Z",
  "shortVolume": 5234000,
  "shortExemptVolume": 120000,
  "totalVolume": 12500000,
  "shortRatio": 0.4283,
  "market": "Q"
}
]
```

## 文档正文

Returns FINRA short volume data for the given ISIN (US equities)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/short-volume/{identifier}`
