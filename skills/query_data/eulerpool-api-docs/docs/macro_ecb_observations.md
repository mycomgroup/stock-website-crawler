---
id: "url-3af44b16"
type: "api"
title: "ECB Observations API"
url: "https://eulerpool.com/developers/api/macro/ecb/observations"
description: "Returns time series data for a specific ECB series. Use the series_key from the ECB series list endpoint."
source: ""
tags: []
crawl_time: "2026-03-18T06:06:03.532Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/ecb/observations/{seriesKey}"
  responses:
    - {"code":"200","description":"Returns time series observations"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Series not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/ecb/observations/EXR%2FD.USD.EUR.SP00.A?limit=5' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"series_key\": \"string\",\n  \"name\": \"string\",\n  \"observations\": {\n    \"date\": \"string\",\n    \"value\": 0\n  }\n}"
  suggestedFilename: "macro_ecb_observations"
---

# ECB Observations API

## 源URL

https://eulerpool.com/developers/api/macro/ecb/observations

## 描述

Returns time series data for a specific ECB series. Use the series_key from the ECB series list endpoint.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/ecb/observations/{seriesKey}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns time series observations |
| 401 | Token not valid |
| 404 | Series not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/ecb/observations/EXR%2FD.USD.EUR.SP00.A?limit=5' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "series_key": "string",
  "name": "string",
  "observations": {
    "date": "string",
    "value": 0
  }
}
```

## 文档正文

Returns time series data for a specific ECB series. Use the series_key from the ECB series list endpoint.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/ecb/observations/{seriesKey}`
