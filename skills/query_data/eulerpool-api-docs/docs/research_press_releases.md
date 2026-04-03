---
id: "url-72b5ac97"
type: "api"
title: "Press Releases"
url: "https://eulerpool.com/developers/api/research/press/releases"
description: "Returns official company press releases"
source: ""
tags: []
crawl_time: "2026-03-18T06:09:24.104Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/research/press-releases/{ticker}"
  responses:
    - {"code":"200","description":"Company press releases"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/research/press-releases/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"symbol\": \"AAPL\",\n  \"datetime\": \"2026-03-01T08:00:00.000Z\",\n  \"title\": \"Apple Announces New Product Launch\",\n  \"text\": \"string\"\n}\n]"
  suggestedFilename: "research_press_releases"
---

# Press Releases

## 源URL

https://eulerpool.com/developers/api/research/press/releases

## 描述

Returns official company press releases

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/research/press-releases/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Company press releases |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/research/press-releases/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "symbol": "AAPL",
  "datetime": "2026-03-01T08:00:00.000Z",
  "title": "Apple Announces New Product Launch",
  "text": "string"
}
]
```

## 文档正文

Returns official company press releases

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/research/press-releases/{ticker}`
