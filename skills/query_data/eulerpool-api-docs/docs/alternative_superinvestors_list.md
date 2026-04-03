---
id: "url-29138cca"
type: "api"
title: "Superinvestors List API"
url: "https://eulerpool.com/developers/api/alternative/superinvestors/list"
description: "Returns a list of tracked superinvestors (e.g. Warren Buffett, Ray Dalio) with their profiles"
source: ""
tags: []
crawl_time: "2026-03-18T05:36:42.112Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/alternative/superinvestors/list"
  responses:
    - {"code":"200","description":"Returns list of superinvestors"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/alternative/superinvestors/list' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"name\": \"Warren Buffett\",\n  \"slug\": \"warren-buffett\",\n  \"cik\": \"1067983\",\n  \"firm\": \"Berkshire Hathaway\"\n}\n]"
  suggestedFilename: "alternative_superinvestors_list"
---

# Superinvestors List API

## 源URL

https://eulerpool.com/developers/api/alternative/superinvestors/list

## 描述

Returns a list of tracked superinvestors (e.g. Warren Buffett, Ray Dalio) with their profiles

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/alternative/superinvestors/list`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns list of superinvestors |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/alternative/superinvestors/list' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "name": "Warren Buffett",
  "slug": "warren-buffett",
  "cik": "1067983",
  "firm": "Berkshire Hathaway"
}
]
```

## 文档正文

Returns a list of tracked superinvestors (e.g. Warren Buffett, Ray Dalio) with their profiles

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/alternative/superinvestors/list`
