---
id: "url-4d36cf28"
type: "api"
title: "News Sentiment API"
url: "https://eulerpool.com/developers/api/sentiment/news/sentiment"
description: "Returns aggregated news sentiment scores for the given security, including buzz metrics and bullish/bearish percentages"
source: ""
tags: []
crawl_time: "2026-03-18T06:11:22.102Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/sentiment/news-sentiment/{identifier}"
  responses:
    - {"code":"200","description":"Returns news sentiment data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/sentiment/news-sentiment/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"symbol\": \"AAPL\",\n  \"company_news_score\": 0.92,\n  \"sector_avg_news_score\": 0.52,\n  \"bullish_percent\": 0.85,\n  \"bearish_percent\": 0.15,\n  \"articles_in_last_week\": 20\n}"
  suggestedFilename: "sentiment_news_sentiment"
---

# News Sentiment API

## 源URL

https://eulerpool.com/developers/api/sentiment/news/sentiment

## 描述

Returns aggregated news sentiment scores for the given security, including buzz metrics and bullish/bearish percentages

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/sentiment/news-sentiment/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns news sentiment data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/sentiment/news-sentiment/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "symbol": "AAPL",
  "company_news_score": 0.92,
  "sector_avg_news_score": 0.52,
  "bullish_percent": 0.85,
  "bearish_percent": 0.15,
  "articles_in_last_week": 20
}
```

## 文档正文

Returns aggregated news sentiment scores for the given security, including buzz metrics and bullish/bearish percentages

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/sentiment/news-sentiment/{identifier}`
