---
id: "url-76bc03f4"
type: "api"
title: "Profile API"
url: "https://eulerpool.com/developers/api/equity/profile"
description: "Returns the profile for the given ISIN. All numbers are in millions."
source: ""
tags: []
crawl_time: "2026-03-18T05:47:43.788Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/profile/{identifier}"
  responses:
    - {"code":"200","description":"Returns a the profile for the given ISIN."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/profile/{identifier}?language=en' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US5949181045\",\n  \"ticker\": \"MSFT\",\n  \"name\": \"Microsoft\",\n  \"logo\": \"/api/logo/isin/US5949181045\",\n  \"country\": \"US\",\n  \"currency\": \"USD\",\n  \"employees\": 100000,\n  \"sector\": \"Information Technology\",\n  \"industry\": \"Software\",\n  \"ipo\": \"1986-03-13T00:00:00.000Z\",\n  \"mcap\": 3000000000,\n  \"shares\": 7433.33,\n  \"website\": \"https://www.microsoft.com/en-us\",\n  \"wkn\": \"870747\",\n  \"description\": \"Microsoft is a software company founded in ....\"\n}"
  suggestedFilename: "equity_profile"
---

# Profile API

## 源URL

https://eulerpool.com/developers/api/equity/profile

## 描述

Returns the profile for the given ISIN. All numbers are in millions.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/profile/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns a the profile for the given ISIN. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/profile/{identifier}?language=en' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US5949181045",
  "ticker": "MSFT",
  "name": "Microsoft",
  "logo": "/api/logo/isin/US5949181045",
  "country": "US",
  "currency": "USD",
  "employees": 100000,
  "sector": "Information Technology",
  "industry": "Software",
  "ipo": "1986-03-13T00:00:00.000Z",
  "mcap": 3000000000,
  "shares": 7433.33,
  "website": "https://www.microsoft.com/en-us",
  "wkn": "870747",
  "description": "Microsoft is a software company founded in ...."
}
```

## 文档正文

Returns the profile for the given ISIN. All numbers are in millions.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/profile/{identifier}`
