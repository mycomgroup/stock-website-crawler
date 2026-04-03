---
id: "url-1a7dd52c"
type: "api"
title: "Basic Financials (Key Ratios) API"
url: "https://eulerpool.com/developers/api/equity/extended/basic/financials"
description: "Returns key financial ratios and metrics including P/E, P/B, dividend yield, margins, debt ratios, and time-series data"
source: ""
tags: []
crawl_time: "2026-03-18T06:15:45.811Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/basic-financials/{identifier}"
  responses:
    - {"code":"200","description":"Returns basic financials"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/basic-financials/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"metrics_json\": {},\n  \"series_annual\": {},\n  \"series_quarterly\": {}\n}"
  suggestedFilename: "equity_extended_basic_financials"
---

# Basic Financials (Key Ratios) API

## 源URL

https://eulerpool.com/developers/api/equity/extended/basic/financials

## 描述

Returns key financial ratios and metrics including P/E, P/B, dividend yield, margins, debt ratios, and time-series data

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/basic-financials/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns basic financials |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/basic-financials/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "metrics_json": {},
  "series_annual": {},
  "series_quarterly": {}
}
```

## 文档正文

Returns key financial ratios and metrics including P/E, P/B, dividend yield, margins, debt ratios, and time-series data

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/basic-financials/{identifier}`
