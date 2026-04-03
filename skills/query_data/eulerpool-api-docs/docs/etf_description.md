---
id: "url-3840171"
type: "api"
title: "ETF Description API"
url: "https://eulerpool.com/developers/api/etf/description"
description: "Returns a description for the given ETF in the requested language. Currently only English (en) and German (de) is supported"
source: ""
tags: []
crawl_time: "2026-03-18T05:50:45.663Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/etf/description/{identifier}"
  responses:
    - {"code":"200","description":"Returns the description of the ETF in the given language"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/etf/description/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"description\": \"SWDA.L was founded on 25.09.2009 by iShares. The fund primarily focuses on total market equity. The ETF currently has an AUM of 71,729.59m and 1,462 holdings.\"\n}"
  suggestedFilename: "etf_description"
---

# ETF Description API

## 源URL

https://eulerpool.com/developers/api/etf/description

## 描述

Returns a description for the given ETF in the requested language. Currently only English (en) and German (de) is supported

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/etf/description/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns the description of the ETF in the given language |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/etf/description/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "description": "SWDA.L was founded on 25.09.2009 by iShares. The fund primarily focuses on total market equity. The ETF currently has an AUM of 71,729.59m and 1,462 holdings."
}
```

## 文档正文

Returns a description for the given ETF in the requested language. Currently only English (en) and German (de) is supported

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/etf/description/{identifier}`
