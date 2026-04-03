---
id: "url-77e29005"
type: "api"
title: "Mutual Fund Profile"
url: "https://eulerpool.com/developers/api/mutual/fund/profile"
description: "Returns profile/overview for a mutual fund by ISIN or symbol"
source: ""
tags: []
crawl_time: "2026-03-18T05:32:45.994Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/mutual-fund/profile/{identifier}"
  responses:
    - {"code":"200","description":"Mutual fund profile"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/mutual-fund/profile/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"LU0099575291\",\n  \"name\": \"Fidelity Global Fund\",\n  \"category\": \"string\",\n  \"family\": \"string\",\n  \"currency\": \"USD\",\n  \"nav\": 42.15,\n  \"totalAssets\": 0,\n  \"expenseRatio\": 0,\n  \"inceptionDate\": \"string\"\n}"
  suggestedFilename: "mutual_fund_profile"
---

# Mutual Fund Profile

## 源URL

https://eulerpool.com/developers/api/mutual/fund/profile

## 描述

Returns profile/overview for a mutual fund by ISIN or symbol

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/mutual-fund/profile/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Mutual fund profile |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/mutual-fund/profile/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "LU0099575291",
  "name": "Fidelity Global Fund",
  "category": "string",
  "family": "string",
  "currency": "USD",
  "nav": 42.15,
  "totalAssets": 0,
  "expenseRatio": 0,
  "inceptionDate": "string"
}
```

## 文档正文

Returns profile/overview for a mutual fund by ISIN or symbol

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/mutual-fund/profile/{identifier}`
