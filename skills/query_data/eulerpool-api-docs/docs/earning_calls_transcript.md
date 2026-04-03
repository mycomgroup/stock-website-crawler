---
id: "url-da9e016"
type: "api"
title: "Get earning call transcript by ID"
url: "https://eulerpool.com/developers/api/earning/calls/transcript"
description: "Returns the full content of a specific earning call transcript by its ID."
source: ""
tags: []
crawl_time: "2026-03-18T06:11:04.008Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/earning-calls/transcript/{id}"
  responses:
    - {"code":"200","description":"Returns the full earning call transcript content"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Transcript not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/earning-calls/transcript/3001' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"id\": 3001,\n  \"ticker\": \"AAPL\",\n  \"datePublished\": 1704067200000,\n  \"title\": \"Apple Inc. (AAPL) Q1 2024 Earnings Call Transcript\",\n  \"type\": \"earnings_call\",\n  \"presentationUrl\": \"https://media.eulerpool.com/presentation/3001.pdf\",\n  \"transcriptAudioUrl\": \"https://media.eulerpool.com/audio/3001.mp3\",\n  \"presentationAvailable\": true,\n  \"transcriptAudioAvailable\": true,\n  \"presentationType\": \"pdf\",\n  \"transcriptAudioType\": \"mp3\",\n  \"parsedContent\": {\n    \"companyParticipants\": [\n      \"onathan Neilson - VP, IR\",\n      \"Satya Nadella - Chairman and CEO\"\n    ],\n    \"otherParticipants\": [\n      \"Keith Weiss - Morgan Stanley\",\n      \"Brent Thill - Jefferies\"\n    ],\n    \"entries\": {\n      \"seq\": 1,\n      \"speaker\": \"Operator\",\n      \"content\": \"Greetings, and welcome to the Microsoft Fiscal Year 2025 Third Quarter Earnings Conference Call. At this time, all participants are in a listen-only mode. A question-and-answer session will follow the formal presentation.\"\n    }\n  }\n}"
  suggestedFilename: "earning_calls_transcript"
---

# Get earning call transcript by ID

## 源URL

https://eulerpool.com/developers/api/earning/calls/transcript

## 描述

Returns the full content of a specific earning call transcript by its ID.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/earning-calls/transcript/{id}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns the full earning call transcript content |
| 401 | Token not valid |
| 404 | Transcript not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/earning-calls/transcript/3001' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "id": 3001,
  "ticker": "AAPL",
  "datePublished": 1704067200000,
  "title": "Apple Inc. (AAPL) Q1 2024 Earnings Call Transcript",
  "type": "earnings_call",
  "presentationUrl": "https://media.eulerpool.com/presentation/3001.pdf",
  "transcriptAudioUrl": "https://media.eulerpool.com/audio/3001.mp3",
  "presentationAvailable": true,
  "transcriptAudioAvailable": true,
  "presentationType": "pdf",
  "transcriptAudioType": "mp3",
  "parsedContent": {
    "companyParticipants": [
      "onathan Neilson - VP, IR",
      "Satya Nadella - Chairman and CEO"
    ],
    "otherParticipants": [
      "Keith Weiss - Morgan Stanley",
      "Brent Thill - Jefferies"
    ],
    "entries": {
      "seq": 1,
      "speaker": "Operator",
      "content": "Greetings, and welcome to the Microsoft Fiscal Year 2025 Third Quarter Earnings Conference Call. At this time, all participants are in a listen-only mode. A question-and-answer session will follow the formal presentation."
    }
  }
}
```

## 文档正文

Returns the full content of a specific earning call transcript by its ID.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/earning-calls/transcript/{id}`
