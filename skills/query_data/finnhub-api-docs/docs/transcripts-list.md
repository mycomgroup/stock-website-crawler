---
id: "url-199d4b59"
type: "api"
title: "transcripts-list"
url: "https://finnhub.io/docs/api/transcripts-list"
description: "List earnings call transcripts' metadata. This endpoint is available for US, UK, European, Australian and Canadian companies."
source: ""
tags: []
crawl_time: "2026-03-18T08:11:53.035Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/stock/transcripts/list"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol: AAPL. Leave empty to list the latest transcripts"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.transcriptsList(\"AAPL\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.transcripts_list('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.TranscriptsList(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->transcriptsList(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.transcripts_list('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.transcriptsList(\"AAPL\"))"}
  sampleResponse: "{\n  \"symbol\": \"AAPL\",\n  \"transcripts\": [\n    {\n      \"id\": \"AAPL_326091\",\n      \"quarter\": 1,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2020-01-28 21:35:45\",\n      \"title\": \"AAPL - Earnings Call Transcript Q1 2020\",\n      \"year\": 2020\n    },\n    {\n      \"id\": \"AAPL_322579\",\n      \"quarter\": 4,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-10-30 22:27:15\",\n      \"title\": \"AAPL - Earnings Call Transcript Q4 2019\",\n      \"year\": 2019\n    },\n    {\n      \"id\": \"AAPL_318112\",\n      \"quarter\": 3,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-07-30 22:26:28\",\n      \"title\": \"AAPL - Earnings Call Transcript Q3 2019\",\n      \"year\": 2019\n    },\n    {\n      \"id\": \"AAPL_313737\",\n      \"quarter\": 2,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-04-30 19:55:19\",\n      \"title\": \"AAPL - Earnings Call Transcript Q2 2019\",\n      \"year\": 2019\n    },\n    {\n      \"id\": \"AAPL_308757\",\n      \"quarter\": 1,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-01-29 21:06:06\",\n      \"title\": \"AAPL - Earnings Call Transcript Q1 2019\",\n      \"year\": 2019\n    }\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"symbol\": \"AAPL\",\n  \"transcripts\": [\n    {\n      \"id\": \"AAPL_326091\",\n      \"quarter\": 1,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2020-01-28 21:35:45\",\n      \"title\": \"AAPL - Earnings Call Transcript Q1 2020\",\n      \"year\": 2020\n    },\n    {\n      \"id\": \"AAPL_322579\",\n      \"quarter\": 4,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-10-30 22:27:15\",\n      \"title\": \"AAPL - Earnings Call Transcript Q4 2019\",\n      \"year\": 2019\n    },\n    {\n      \"id\": \"AAPL_318112\",\n      \"quarter\": 3,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-07-30 22:26:28\",\n      \"title\": \"AAPL - Earnings Call Transcript Q3 2019\",\n      \"year\": 2019\n    },\n    {\n      \"id\": \"AAPL_313737\",\n      \"quarter\": 2,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-04-30 19:55:19\",\n      \"title\": \"AAPL - Earnings Call Transcript Q2 2019\",\n      \"year\": 2019\n    },\n    {\n      \"id\": \"AAPL_308757\",\n      \"quarter\": 1,\n      \"symbol\": \"AAPL\",\n      \"time\": \"2019-01-29 21:06:06\",\n      \"title\": \"AAPL - Earnings Call Transcript Q1 2019\",\n      \"year\": 2019\n    }\n  ]\n}"
  rawContent: ""
  suggestedFilename: "transcripts-list"
---

# transcripts-list

## 源URL

https://finnhub.io/docs/api/transcripts-list

## 描述

List earnings call transcripts' metadata. This endpoint is available for US, UK, European, Australian and Canadian companies.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/stock/transcripts/list`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol: AAPL. Leave empty to list the latest transcripts |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.transcriptsList("AAPL", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.transcripts_list('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.TranscriptsList(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->transcriptsList("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.transcripts_list('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.transcriptsList("AAPL"))
```

### 示例 7 (json)

```json
{
  "symbol": "AAPL",
  "transcripts": [
    {
      "id": "AAPL_326091",
      "quarter": 1,
      "symbol": "AAPL",
      "time": "2020-01-28 21:35:45",
      "title": "AAPL - Earnings Call Transcript Q1 2020",
      "year": 2020
    },
    {
      "id": "AAPL_322579",
      "quarter": 4,
      "symbol": "AAPL",
      "time": "2019-10-30 22:27:15",
      "title": "AAPL - Earnings Call Transcript Q4 2019",
      "year": 2019
    },
    {
      "id": "AAPL_318112",
      "quarter": 3,
      "symbol": "AAPL",
      "time": "2019-07-30 22:26:28",
      "title": "AAPL - Earnings Call Transcript Q3 2019",
      "year": 2019
    },
    {
      "id": "AAPL_313737",
      "quarter": 2,
      "symbol": "AAPL",
      "time": "2019-04-30 19:55:19",
      "title": "AAPL - Earnings Call Transcript Q2 2019",
      "year": 2019
    },
    {
      "id": "AAPL_308757",
      "quarter": 1,
      "symbol": "AAPL",
      "time": "2019-01-29 21:06:06",
      "title": "AAPL - Earnings Call Transcript Q1 2019",
      "year": 2019
    }
  ]
}
```

## 文档正文

List earnings call transcripts' metadata. This endpoint is available for US, UK, European, Australian and Canadian companies.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/stock/transcripts/list`
