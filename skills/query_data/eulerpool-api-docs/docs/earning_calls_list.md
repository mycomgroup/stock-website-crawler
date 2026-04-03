---
id: "url-65ddf02e"
type: "api"
title: "List earning call transcripts by ticker"
url: "https://eulerpool.com/developers/api/earning/calls/list"
description: "Returns a list of all earning call transcripts for a given ticker symbol."
source: ""
tags: []
crawl_time: "2026-03-18T05:32:03.915Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/earning-calls/list/{ticker}"
  responses:
    - {"code":"200","description":"Returns an array of earning call transcript summaries for the given ticker"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/earning-calls/list/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"id\": 3001,\n  \"ticker\": \"AAPL\",\n  \"datePublished\": 1704067200000,\n  \"title\": \"Apple Inc. (AAPL) Q1 2024 Earnings Call Transcript\",\n  \"type\": \"earnings_call\",\n  \"presentationUrl\": \"https://media.eulerpool.com/presentation/3001.pdf\",\n  \"transcriptAudioUrl\": \"https://media.eulerpool.com/audio/3001.mp3\",\n  \"presentationAvailable\": true,\n  \"transcriptAudioAvailable\": true\n}\n]"
  suggestedFilename: "earning_calls_list"
---

# List earning call transcripts by ticker

## 源URL

https://eulerpool.com/developers/api/earning/calls/list

## 描述

Returns a list of all earning call transcripts for a given ticker symbol.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/earning-calls/list/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns an array of earning call transcript summaries for the given ticker |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/earning-calls/list/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "id": 3001,
  "ticker": "AAPL",
  "datePublished": 1704067200000,
  "title": "Apple Inc. (AAPL) Q1 2024 Earnings Call Transcript",
  "type": "earnings_call",
  "presentationUrl": "https://media.eulerpool.com/presentation/3001.pdf",
  "transcriptAudioUrl": "https://media.eulerpool.com/audio/3001.mp3",
  "presentationAvailable": true,
  "transcriptAudioAvailable": true
}
]
```

## 文档正文

Returns a list of all earning call transcripts for a given ticker symbol.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/earning-calls/list/{ticker}`
