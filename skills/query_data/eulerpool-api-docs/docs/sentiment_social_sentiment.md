---
id: "url-6685f5fe"
type: "api"
title: "Social Sentiment API"
url: "https://eulerpool.com/developers/api/sentiment/social/sentiment"
description: "Returns social media sentiment data from Reddit and Twitter for the given security"
source: ""
tags: []
crawl_time: "2026-03-18T06:12:16.780Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/sentiment/social-sentiment/{identifier}"
  responses:
    - {"code":"200","description":"Returns social sentiment data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/sentiment/social-sentiment/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"source\": \"reddit\",\n  \"at_time\": \"2024-01-15T14:00:00.000Z\",\n  \"mention\": 32,\n  \"positive_mention\": 20,\n  \"negative_mention\": 12,\n  \"positive_score\": 0.92,\n  \"negative_score\": -0.98,\n  \"score\": -0.03\n}\n]"
  suggestedFilename: "sentiment_social_sentiment"
---

# Social Sentiment API

## 源URL

https://eulerpool.com/developers/api/sentiment/social/sentiment

## 描述

Returns social media sentiment data from Reddit and Twitter for the given security

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/sentiment/social-sentiment/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns social sentiment data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/sentiment/social-sentiment/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "source": "reddit",
  "at_time": "2024-01-15T14:00:00.000Z",
  "mention": 32,
  "positive_mention": 20,
  "negative_mention": 12,
  "positive_score": 0.92,
  "negative_score": -0.98,
  "score": -0.03
}
]
```

## 文档正文

Returns social media sentiment data from Reddit and Twitter for the given security

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/sentiment/social-sentiment/{identifier}`
