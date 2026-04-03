---
id: "url-3349a58b"
type: "api"
title: "Bond Profile API"
url: "https://eulerpool.com/developers/api/bonds/profile"
description: "Returns profile information for the given bond identifier, including coupon, maturity, and issuer details"
source: ""
tags: []
crawl_time: "2026-03-18T05:30:21.427Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/bonds/profile/{identifier}"
  responses:
    - {"code":"200","description":"Returns bond profile data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/bonds/profile/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US912810TD00\",\n  \"figi\": \"BBG0152KFHS6\",\n  \"cusip\": \"string\",\n  \"coupon\": 2.25,\n  \"maturityDate\": \"2052-02-15T00:00:00.000Z\",\n  \"bondType\": \"US Government\",\n  \"issueDate\": \"2022-03-15T00:00:00.000Z\",\n  \"offeringPrice\": 100,\n  \"paymentFrequency\": \"Semi-Annual\",\n  \"industryGroup\": \"Government\",\n  \"industrySubGroup\": \"U.S. Treasuries\"\n}"
  suggestedFilename: "bonds_profile"
---

# Bond Profile API

## 源URL

https://eulerpool.com/developers/api/bonds/profile

## 描述

Returns profile information for the given bond identifier, including coupon, maturity, and issuer details

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/bonds/profile/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns bond profile data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/bonds/profile/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US912810TD00",
  "figi": "BBG0152KFHS6",
  "cusip": "string",
  "coupon": 2.25,
  "maturityDate": "2052-02-15T00:00:00.000Z",
  "bondType": "US Government",
  "issueDate": "2022-03-15T00:00:00.000Z",
  "offeringPrice": 100,
  "paymentFrequency": "Semi-Annual",
  "industryGroup": "Government",
  "industrySubGroup": "U.S. Treasuries"
}
```

## 文档正文

Returns profile information for the given bond identifier, including coupon, maturity, and issuer details

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/bonds/profile/{identifier}`
