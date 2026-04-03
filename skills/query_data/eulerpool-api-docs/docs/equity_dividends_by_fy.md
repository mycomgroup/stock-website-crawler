---
id: "url-24072a95"
type: "api"
title: "Dividends by Fiscal Year API"
url: "https://eulerpool.com/developers/api/equity/dividends/by/fy"
description: "Returns dividends grouped by fiscal year for the given ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T06:07:24.646Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/dividends-by-fy/{identifier}"
  responses:
    - {"code":"200","description":"Returns dividends by fiscal year."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/dividends-by-fy/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"ticker\": \"MSFT\",\n  \"fiscal_year_start\": \"2025-06-30T22:00:00.000Z\",\n  \"fiscal_year_end\": \"2026-06-29T22:00:00.000Z\",\n  \"total_dividends_per_fy\": 0.91,\n  \"dividend_count\": 1,\n  \"expected_freq\": 4,\n  \"fully_paid\": \"NO\",\n  \"fully_paid_current_fy\": \"NO\"\n}\n]"
  suggestedFilename: "equity_dividends_by_fy"
---

# Dividends by Fiscal Year API

## 源URL

https://eulerpool.com/developers/api/equity/dividends/by/fy

## 描述

Returns dividends grouped by fiscal year for the given ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/dividends-by-fy/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns dividends by fiscal year. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/dividends-by-fy/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "ticker": "MSFT",
  "fiscal_year_start": "2025-06-30T22:00:00.000Z",
  "fiscal_year_end": "2026-06-29T22:00:00.000Z",
  "total_dividends_per_fy": 0.91,
  "dividend_count": 1,
  "expected_freq": 4,
  "fully_paid": "NO",
  "fully_paid_current_fy": "NO"
}
]
```

## 文档正文

Returns dividends grouped by fiscal year for the given ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/dividends-by-fy/{identifier}`
