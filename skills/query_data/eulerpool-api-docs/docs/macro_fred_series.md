---
id: "url-6041923"
type: "api"
title: "FRED Series List API"
url: "https://eulerpool.com/developers/api/macro/fred/series"
description: "Returns all available FRED (Federal Reserve Economic Data) series with their categories. Covers GDP, unemployment, CPI, interest rates, housing, trade, and 100+ more US macro indicators."
source: ""
tags: []
crawl_time: "2026-03-18T05:59:21.238Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/fred/series"
  responses:
    - {"code":"200","description":"Returns FRED series list"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/fred/series' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"series_id\": \"GDP\",\n  \"name\": \"Gross Domestic Product\",\n  \"frequency\": \"Q\",\n  \"units\": \"string\",\n  \"category\": \"gdp\",\n  \"last_updated\": \"string\"\n}\n]"
  suggestedFilename: "macro_fred_series"
---

# FRED Series List API

## 源URL

https://eulerpool.com/developers/api/macro/fred/series

## 描述

Returns all available FRED (Federal Reserve Economic Data) series with their categories. Covers GDP, unemployment, CPI, interest rates, housing, trade, and 100+ more US macro indicators.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/fred/series`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns FRED series list |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/fred/series' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "series_id": "GDP",
  "name": "Gross Domestic Product",
  "frequency": "Q",
  "units": "string",
  "category": "gdp",
  "last_updated": "string"
}
]
```

## 文档正文

Returns all available FRED (Federal Reserve Economic Data) series with their categories. Covers GDP, unemployment, CPI, interest rates, housing, trade, and 100+ more US macro indicators.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/fred/series`
