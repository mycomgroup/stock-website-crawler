---
id: "url-7eb9688d"
type: "api"
title: "FRED Observations API"
url: "https://eulerpool.com/developers/api/macro/fred/observations"
description: "Returns time series data for a specific FRED series (e.g. GDP, UNRATE, CPIAUCSL, FEDFUNDS, DGS10)"
source: ""
tags: []
crawl_time: "2026-03-18T06:08:24.456Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/fred/observations/{seriesId}"
  responses:
    - {"code":"200","description":"Returns time series observations"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Series not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/fred/observations/GDP?limit=5' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"series_id\": \"GDP\",\n  \"name\": \"Gross Domestic Product\",\n  \"frequency\": \"Q\",\n  \"units\": \"string\",\n  \"observations\": {\n    \"date\": \"2024-01-01T00:00:00.000Z\",\n    \"value\": 28628.1\n  }\n}"
  suggestedFilename: "macro_fred_observations"
---

# FRED Observations API

## 源URL

https://eulerpool.com/developers/api/macro/fred/observations

## 描述

Returns time series data for a specific FRED series (e.g. GDP, UNRATE, CPIAUCSL, FEDFUNDS, DGS10)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/fred/observations/{seriesId}`

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
  'https://api.eulerpool.com/api/1/macro/fred/observations/GDP?limit=5' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "series_id": "GDP",
  "name": "Gross Domestic Product",
  "frequency": "Q",
  "units": "string",
  "observations": {
    "date": "2024-01-01T00:00:00.000Z",
    "value": 28628.1
  }
}
```

## 文档正文

Returns time series data for a specific FRED series (e.g. GDP, UNRATE, CPIAUCSL, FEDFUNDS, DGS10)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/fred/observations/{seriesId}`
