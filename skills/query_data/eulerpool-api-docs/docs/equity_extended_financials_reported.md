---
id: "url-3d00ff09"
type: "api"
title: "As-Reported Financials API"
url: "https://eulerpool.com/developers/api/equity/extended/financials/reported"
description: "Returns raw as-reported financial data from SEC filings (10-K, 10-Q) for the given security. This is the original XBRL data as filed, not standardized. Includes all line items from the filing."
source: ""
tags: []
crawl_time: "2026-03-18T06:17:04.437Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/financials-reported/{identifier}"
  responses:
    - {"code":"200","description":"Returns as-reported financial filings"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/financials-reported/{identifier}?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"accessNumber\": \"0000320193-23-000106\",\n  \"form\": \"10-K\",\n  \"cik\": \"320193\",\n  \"year\": 2023,\n  \"quarter\": 0,\n  \"startDate\": \"2022-10-01T00:00:00.000Z\",\n  \"endDate\": \"2023-09-30T00:00:00.000Z\",\n  \"filedDate\": \"2023-11-03T00:00:00.000Z\",\n  \"report\": {}\n}\n]"
  suggestedFilename: "equity_extended_financials_reported"
---

# As-Reported Financials API

## 源URL

https://eulerpool.com/developers/api/equity/extended/financials/reported

## 描述

Returns raw as-reported financial data from SEC filings (10-K, 10-Q) for the given security. This is the original XBRL data as filed, not standardized. Includes all line items from the filing.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/financials-reported/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns as-reported financial filings |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/financials-reported/{identifier}?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "accessNumber": "0000320193-23-000106",
  "form": "10-K",
  "cik": "320193",
  "year": 2023,
  "quarter": 0,
  "startDate": "2022-10-01T00:00:00.000Z",
  "endDate": "2023-09-30T00:00:00.000Z",
  "filedDate": "2023-11-03T00:00:00.000Z",
  "report": {}
}
]
```

## 文档正文

Returns raw as-reported financial data from SEC filings (10-K, 10-Q) for the given security. This is the original XBRL data as filed, not standardized. Includes all line items from the filing.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/financials-reported/{identifier}`
