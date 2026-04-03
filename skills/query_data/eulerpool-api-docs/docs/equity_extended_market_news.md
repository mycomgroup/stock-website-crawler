---
id: "url-241adf7b"
type: "api"
title: "Market News API"
url: "https://eulerpool.com/developers/api/equity/extended/market/news"
description: "Returns the latest general market news from major financial news sources"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:09.130Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity-extended/market-news"
  responses:
    - {"code":"200","description":"Returns market news"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity-extended/market-news?limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"headline\": \"Fed Holds Rates Steady\",\n  \"source\": \"CNBC\",\n  \"url\": \"https://...\",\n  \"summary\": \"...\",\n  \"image\": \"https://...\",\n  \"category\": \"general\",\n  \"datetime\": 1706122800,\n  \"related\": \"AAPL,MSFT\"\n}\n]"
  suggestedFilename: "equity_extended_market_news"
---

# Market News API

## 源URL

https://eulerpool.com/developers/api/equity/extended/market/news

## 描述

Returns the latest general market news from major financial news sources

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity-extended/market-news`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns market news |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity-extended/market-news?limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "headline": "Fed Holds Rates Steady",
  "source": "CNBC",
  "url": "https://...",
  "summary": "...",
  "image": "https://...",
  "category": "general",
  "datetime": 1706122800,
  "related": "AAPL,MSFT"
}
]
```

## 文档正文

Returns the latest general market news from major financial news sources

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity-extended/market-news`
