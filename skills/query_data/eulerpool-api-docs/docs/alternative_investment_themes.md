---
id: "url-520f386f"
type: "api"
title: "Investment Themes API"
url: "https://eulerpool.com/developers/api/alternative/investment/themes"
description: "Returns curated portfolios of stocks grouped by investment themes (e.g. AI, Clean Energy, Robotics)"
source: ""
tags: []
crawl_time: "2026-03-18T06:14:13.957Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/investment-themes"
  responses:
    - {"code":"200","description":"Returns investment themes"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/investment-themes' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"theme\": \"financialExchangesData\",\n  \"symbols_json\": [],\n  \"last_updated\": \"2024-01-15T00:00:00.000Z\"\n}\n]"
  suggestedFilename: "alternative_investment_themes"
---

# Investment Themes API

## 源URL

https://eulerpool.com/developers/api/alternative/investment/themes

## 描述

Returns curated portfolios of stocks grouped by investment themes (e.g. AI, Clean Energy, Robotics)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/investment-themes`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns investment themes |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/investment-themes' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "theme": "financialExchangesData",
  "symbols_json": [],
  "last_updated": "2024-01-15T00:00:00.000Z"
}
]
```

## 文档正文

Returns curated portfolios of stocks grouped by investment themes (e.g. AI, Clean Energy, Robotics)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/investment-themes`
