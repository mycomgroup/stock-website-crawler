---
id: "url-12e89be"
type: "api"
title: "Bond Tick Data API"
url: "https://eulerpool.com/developers/api/bonds/ticks"
description: "Returns FINRA TRACE trade-level tick data for the given bond identifier (4h delayed). Paginated by date."
source: ""
tags: []
crawl_time: "2026-03-18T05:41:42.832Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/bonds/ticks/{identifier}"
  responses:
    - {"code":"200","description":"Returns bond tick data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/bonds/ticks/{identifier}?date=2025-12-31&limit=10&offset=0' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US693475BF18\",\n  \"date\": \"2024-01-15T00:00:00.000Z\",\n  \"ticks\": {\n    \"t\": 1705316400000,\n    \"p\": 100.234,\n    \"v\": 50000,\n    \"si\": \"2\",\n    \"rp\": \"1\",\n    \"c\": []\n  },\n  \"total\": 211,\n  \"offset\": 0,\n  \"limit\": 200\n}"
  suggestedFilename: "bonds_ticks"
---

# Bond Tick Data API

## 源URL

https://eulerpool.com/developers/api/bonds/ticks

## 描述

Returns FINRA TRACE trade-level tick data for the given bond identifier (4h delayed). Paginated by date.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/bonds/ticks/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns bond tick data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/bonds/ticks/{identifier}?date=2025-12-31&limit=10&offset=0' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US693475BF18",
  "date": "2024-01-15T00:00:00.000Z",
  "ticks": {
    "t": 1705316400000,
    "p": 100.234,
    "v": 50000,
    "si": "2",
    "rp": "1",
    "c": []
  },
  "total": 211,
  "offset": 0,
  "limit": 200
}
```

## 文档正文

Returns FINRA TRACE trade-level tick data for the given bond identifier (4h delayed). Paginated by date.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/bonds/ticks/{identifier}`
