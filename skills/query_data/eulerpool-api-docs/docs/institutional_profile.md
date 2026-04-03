---
id: "url-690a1db8"
type: "api"
title: "Institutional Investor Profile API"
url: "https://eulerpool.com/developers/api/institutional/profile"
description: "Returns the profile of an institutional investor (hedge fund, asset manager) by their SEC CIK number. Includes fund name, manager, and AUM."
source: ""
tags: []
crawl_time: "2026-03-18T05:34:31.592Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/institutional/profile/{cik}"
  responses:
    - {"code":"200","description":"Returns institutional profile"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"CIK not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/institutional/profile/0001067983' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"cik\": \"1067983\",\n  \"name\": \"BERKSHIRE HATHAWAY INC\",\n  \"manager\": \"Warren Buffett\",\n  \"filingDate\": \"2024-02-14T00:00:00.000Z\",\n  \"portfolioValue\": 0,\n  \"holdingsCount\": 0\n}"
  suggestedFilename: "institutional_profile"
---

# Institutional Investor Profile API

## 源URL

https://eulerpool.com/developers/api/institutional/profile

## 描述

Returns the profile of an institutional investor (hedge fund, asset manager) by their SEC CIK number. Includes fund name, manager, and AUM.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/institutional/profile/{cik}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns institutional profile |
| 401 | Token not valid |
| 404 | CIK not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/institutional/profile/0001067983' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "cik": "1067983",
  "name": "BERKSHIRE HATHAWAY INC",
  "manager": "Warren Buffett",
  "filingDate": "2024-02-14T00:00:00.000Z",
  "portfolioValue": 0,
  "holdingsCount": 0
}
```

## 文档正文

Returns the profile of an institutional investor (hedge fund, asset manager) by their SEC CIK number. Includes fund name, manager, and AUM.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/institutional/profile/{cik}`
