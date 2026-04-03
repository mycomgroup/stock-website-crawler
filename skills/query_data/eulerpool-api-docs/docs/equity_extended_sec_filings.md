---
id: "url-4718705b"
type: "api"
title: "SEC Filings API"
url: "https://eulerpool.com/developers/api/equity/extended/sec/filings"
description: "Returns recent SEC filings (10-K, 10-Q, 8-K, etc.) for the given security"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:03.331Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/sec-filings/{identifier}"
  responses:
    - {"code":"200","description":"Returns SEC filing data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/sec-filings/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"form\": \"10-K\",\n  \"filedDate\": \"2024-10-31T00:00:00.000Z\",\n  \"acceptedDate\": \"2024-10-30T18:12:36.000Z\",\n  \"reportUrl\": \"https://www.sec.gov/...\",\n  \"filingUrl\": \"https://www.sec.gov/...\"\n}\n]"
  suggestedFilename: "equity_extended_sec_filings"
---

# SEC Filings API

## 源URL

https://eulerpool.com/developers/api/equity/extended/sec/filings

## 描述

Returns recent SEC filings (10-K, 10-Q, 8-K, etc.) for the given security

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/sec-filings/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns SEC filing data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/sec-filings/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "form": "10-K",
  "filedDate": "2024-10-31T00:00:00.000Z",
  "acceptedDate": "2024-10-30T18:12:36.000Z",
  "reportUrl": "https://www.sec.gov/...",
  "filingUrl": "https://www.sec.gov/..."
}
]
```

## 文档正文

Returns recent SEC filings (10-K, 10-Q, 8-K, etc.) for the given security

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/sec-filings/{identifier}`
