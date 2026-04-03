---
id: "url-6eb7d5e2"
type: "api"
title: "Country Indicators API"
url: "https://eulerpool.com/developers/api/macro/country"
description: "Returns all macro economic indicators available for a given country (GDP, unemployment, inflation, etc.)"
source: ""
tags: []
crawl_time: "2026-03-18T05:46:43.053Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/country/{country}"
  responses:
    - {"code":"200","description":"Returns country indicators"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Country not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/country/US' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"indicators\": {\n    \"slug\": \"gdp\",\n    \"name\": \"Gross Domestic Product\",\n    \"mainCategory\": \"GDP & Output\",\n    \"category\": \"string\",\n    \"country_code\": \"us\"\n  },\n  \"countryAlternatives\": []\n}"
  suggestedFilename: "macro_country"
---

# Country Indicators API

## 源URL

https://eulerpool.com/developers/api/macro/country

## 描述

Returns all macro economic indicators available for a given country (GDP, unemployment, inflation, etc.)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/country/{country}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns country indicators |
| 401 | Token not valid |
| 404 | Country not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/country/US' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "indicators": {
    "slug": "gdp",
    "name": "Gross Domestic Product",
    "mainCategory": "GDP & Output",
    "category": "string",
    "country_code": "us"
  },
  "countryAlternatives": []
}
```

## 文档正文

Returns all macro economic indicators available for a given country (GDP, unemployment, inflation, etc.)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/country/{country}`
