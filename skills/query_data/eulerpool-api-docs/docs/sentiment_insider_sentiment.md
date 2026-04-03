---
id: "url-1f4e2701"
type: "api"
title: "Insider Sentiment API"
url: "https://eulerpool.com/developers/api/sentiment/insider/sentiment"
description: "Returns monthly insider sentiment (MSPR - Monthly Share Purchase Ratio) for the given security. Ranges from -100 (very negative) to 100 (very positive)"
source: ""
tags: []
crawl_time: "2026-03-18T05:36:21.190Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/sentiment/insider-sentiment/{identifier}"
  responses:
    - {"code":"200","description":"Returns insider sentiment data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/sentiment/insider-sentiment/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"year\": 2024,\n  \"month\": 3,\n  \"change\": 5540,\n  \"mspr\": 12.21\n}\n]"
  suggestedFilename: "sentiment_insider_sentiment"
---

# Insider Sentiment API

## 源URL

https://eulerpool.com/developers/api/sentiment/insider/sentiment

## 描述

Returns monthly insider sentiment (MSPR - Monthly Share Purchase Ratio) for the given security. Ranges from -100 (very negative) to 100 (very positive)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/sentiment/insider-sentiment/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns insider sentiment data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/sentiment/insider-sentiment/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "year": 2024,
  "month": 3,
  "change": 5540,
  "mspr": 12.21
}
]
```

## 文档正文

Returns monthly insider sentiment (MSPR - Monthly Share Purchase Ratio) for the given security. Ranges from -100 (very negative) to 100 (very positive)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/sentiment/insider-sentiment/{identifier}`
