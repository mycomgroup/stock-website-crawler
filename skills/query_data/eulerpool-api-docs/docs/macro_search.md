---
id: "url-6a12220"
type: "api"
title: "Macro Data Search API"
url: "https://eulerpool.com/developers/api/macro/search"
description: "Search across all macro data sources (FRED, ECB, IMF, World Bank, Eurostat) by keyword. Returns matching series from all providers."
source: ""
tags: []
crawl_time: "2026-03-18T05:44:03.179Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/macro/search"
  responses:
    - {"code":"200","description":"Returns matching series grouped by source"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/macro/search?q=GDP&limit=5' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"fred\": [],\n  \"ecb\": [],\n  \"imf\": [],\n  \"worldbank\": [],\n  \"eurostat\": []\n}"
  suggestedFilename: "macro_search"
---

# Macro Data Search API

## 源URL

https://eulerpool.com/developers/api/macro/search

## 描述

Search across all macro data sources (FRED, ECB, IMF, World Bank, Eurostat) by keyword. Returns matching series from all providers.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/macro/search`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns matching series grouped by source |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/macro/search?q=GDP&limit=5' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "fred": [],
  "ecb": [],
  "imf": [],
  "worldbank": [],
  "eurostat": []
}
```

## 文档正文

Search across all macro data sources (FRED, ECB, IMF, World Bank, Eurostat) by keyword. Returns matching series from all providers.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/macro/search`
