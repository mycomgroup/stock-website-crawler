---
id: "url-43926892"
type: "api"
title: "Company News"
url: "https://eulerpool.com/developers/api/research/news"
description: "Returns the latest news articles mentioning a specific company"
source: ""
tags: []
crawl_time: "2026-03-18T05:47:02.822Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/research/news/{ticker}"
  responses:
    - {"code":"200","description":"Recent company news articles"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/research/news/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"headline\": \"Apple Reports Record Q4 Revenue\",\n  \"summary\": \"string\",\n  \"source\": \"Reuters\",\n  \"url\": \"https://example.com/article\",\n  \"datetime\": \"2026-03-01T10:30:00.000Z\",\n  \"category\": \"string\",\n  \"image\": \"string\"\n}\n]"
  suggestedFilename: "research_news"
---

# Company News

## 源URL

https://eulerpool.com/developers/api/research/news

## 描述

Returns the latest news articles mentioning a specific company

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/research/news/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Recent company news articles |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/research/news/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "headline": "Apple Reports Record Q4 Revenue",
  "summary": "string",
  "source": "Reuters",
  "url": "https://example.com/article",
  "datetime": "2026-03-01T10:30:00.000Z",
  "category": "string",
  "image": "string"
}
]
```

## 文档正文

Returns the latest news articles mentioning a specific company

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/research/news/{ticker}`
