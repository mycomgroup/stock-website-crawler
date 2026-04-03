---
id: "url-61971727"
type: "api"
title: "Get Research Task Status"
url: "https://docs.tavily.com/documentation/api-reference/endpoint/research-get"
description: "Retrieve the status and results of a research task using its request ID."
source: ""
tags: []
crawl_time: "2026-03-18T08:21:16.133Z"
metadata:
  method: "GET"
  endpoint: "/research-get"
  baseUrl: "https://api.tavily.com"
  parameters:
    - {"name":"Authorization","type":"string","required":true,"default":"","description":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).","location":"header"}
    - {"name":"request_id","type":"string","required":true,"default":"","description":"The unique identifier of the research task."}
    - {"name":"created_at","type":"string","required":true,"default":"","description":"Timestamp when the research task was created.Example:\"2025-01-15T10:30:00Z\""}
    - {"name":"status","type":"enum<string>","required":true,"default":"","description":"The current status of the research task.Available options: completed"}
    - {"name":"content","type":"","required":false,"default":"","description":""}
    - {"name":"sources.title","type":"string","required":false,"default":"","description":"Title or name of the source.Example:\"Latest AI Developments\""}
    - {"name":"sources.url","type":"string","required":false,"default":"","description":"<uri>URL of the source.Example:\"https://example.com/ai-news\""}
    - {"name":"sources.favicon","type":"string","required":false,"default":"","description":"<uri>URL to the source's favicon.Example:\"https://example.com/favicon.ico\""}
    - {"name":"response_time","type":"integer","required":true,"default":"","description":"Time in seconds it took to complete the request.Example:1.23"}
    - {"name":"CompletedFailed​request_id","type":"string","required":true,"default":"","description":"The unique identifier of the research task.Example:\"123e4567-e89b-12d3-a456-426614174111\"​created_atstringrequiredTimestamp when the research task was created.Example:\"2025-01-15T10:30:00Z\"​statusenum<string>requiredThe current status of the research task.Available options: completed ​content"}
    - {"name":"Hide child attributes​sources.title","type":"string","required":false,"default":"","description":"Title or name of the source.Example:\"Latest AI Developments\"​sources.urlstring<uri>URL of the source.Example:\"https://example.com/ai-news\"​sources.faviconstring<uri>URL to the source's favicon.Example:\"https://example.com/favicon.ico\""}
    - {"name":"sources","type":"object","required":false,"default":"","description":"[]requiredList of sources used in the research.Hide child attributes sources.titlestringTitle or name of the source.Example:\"Latest AI Developments\" sources.urlstring<uri>URL of the source.Example:\"https://example.com/ai-news\" sources.faviconstring<uri>URL to the source's favicon.Example:\"https://example.com/favicon.ico\""}
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.get_research(\"123e4567-e89b-12d3-a456-426614174111\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"created_at\": \"2025-01-15T10:30:00Z\",\n  \"status\": \"completed\",\n  \"content\": \"Research Report: Latest Developments in AI\\n\\n## Executive Summary\\n\\nArtificial Intelligence has seen significant advancements in recent months, with major breakthroughs in large language models, multimodal AI systems, and real-world applications...\",\n  \"sources\": [\n    {\n      \"title\": \"Latest AI Developments\",\n      \"url\": \"https://example.com/ai-news\",\n      \"favicon\": \"https://example.com/favicon.ico\"\n    },\n    {\n      \"title\": \"AI Research Breakthroughs\",\n      \"url\": \"https://example.com/ai-research\",\n      \"favicon\": \"https://example.com/favicon.ico\"\n    }\n  ],\n  \"response_time\": 1.23\n}"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.get_research(\"123e4567-e89b-12d3-a456-426614174111\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"created_at\": \"2025-01-15T10:30:00Z\",\n  \"status\": \"completed\",\n  \"content\": \"Research Report: Latest Developments in AI\\n\\n## Executive Summary\\n\\nArtificial Intelligence has seen significant advancements in recent months, with major breakthroughs in large language models, multimodal AI systems, and real-world applications...\",\n  \"sources\": [\n    {\n      \"title\": \"Latest AI Developments\",\n      \"url\": \"https://example.com/ai-news\",\n      \"favicon\": \"https://example.com/favicon.ico\"\n    },\n    {\n      \"title\": \"AI Research Breakthroughs\",\n      \"url\": \"https://example.com/ai-research\",\n      \"favicon\": \"https://example.com/favicon.ico\"\n    }\n  ],\n  \"response_time\": 1.23\n}"}
  mainContent:
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Path Parameters"}
    - {"type":"paragraph","content":"The unique identifier of the research task."}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Research task is completed or failed."}
    - {"type":"parameter","name":"\"123e4567-e89b-12d3-a456-426614174111\"","paramType":"","description":"CompletedFailed​request_idstringrequiredThe unique identifier of the research task.Example:\"123e4567-e89b-12d3-a456-426614174111\"​created_atstringrequiredTimestamp when the research task was created.Example:\"2025-01-15T10:30:00Z\"​statusenum<string>requiredThe current status of the research task.Available options: completed ​content"}
  rawContent: "Authorizations\n​\nAuthorization\nstringheaderrequired\n\nBearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).\n\nPath Parameters\n​\nrequest_id\nstringrequired\n\nThe unique identifier of the research task.\n\nResponse\n200\napplication/json\n\nResearch task is completed or failed.\n\nCompleted\nFailed\n​\nrequest_id\nstringrequired\n\nThe unique identifier of the research task.\n\nExample:\n\n\"123e4567-e89b-12d3-a456-426614174111\"\n\n​\ncreated_at\nstringrequired\n\nTimestamp when the research task was created.\n\nExample:\n\n\"2025-01-15T10:30:00Z\"\n\n​\nstatus\nenum<string>required\n\nThe current status of the research task.\n\nAvailable options: completed \n​\ncontent\nstring\nobject\nstring\nrequired\n\nThe research report content. Can be a string or a structured object if output_schema was provided.\n\n​\nsources\nobject[]required\n\nList of sources used in the research.\n\nHide child attributes\n\n​\nsources.title\nstring\n\nTitle or name of the source.\n\nExample:\n\n\"Latest AI Developments\"\n\n​\nsources.url\nstring<uri>\n\nURL of the source.\n\nExample:\n\n\"https://example.com/ai-news\"\n\n​\nsources.favicon\nstring<uri>\n\nURL to the source's favicon.\n\nExample:\n\n\"https://example.com/favicon.ico\"\n\n​\nresponse_time\nintegerrequired\n\nTime in seconds it took to complete the request.\n\nExample:\n\n1.23"
  suggestedFilename: "endpoint_research-get"
---

# Get Research Task Status

## 源URL

https://docs.tavily.com/documentation/api-reference/endpoint/research-get

## 描述

Retrieve the status and results of a research task using its request ID.

## API 端点

**Method**: `GET`
**Endpoint**: `/research-get`
**Base URL**: `https://api.tavily.com`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Authorization` | string | 是 | - | Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY). |
| `request_id` | string | 是 | - | The unique identifier of the research task. |
| `created_at` | string | 是 | - | Timestamp when the research task was created.Example:"2025-01-15T10:30:00Z" |
| `status` | enum<string> | 是 | - | The current status of the research task.Available options: completed |
| `content` | - | 否 | - | - |
| `sources.title` | string | 否 | - | Title or name of the source.Example:"Latest AI Developments" |
| `sources.url` | string | 否 | - | <uri>URL of the source.Example:"https://example.com/ai-news" |
| `sources.favicon` | string | 否 | - | <uri>URL to the source's favicon.Example:"https://example.com/favicon.ico" |
| `response_time` | integer | 是 | - | Time in seconds it took to complete the request.Example:1.23 |
| `CompletedFailedrequest_id` | string | 是 | - | The unique identifier of the research task.Example:"123e4567-e89b-12d3-a456-426614174111"created_atstringrequiredTimestamp when the research task was created.Example:"2025-01-15T10:30:00Z"statusenum<string>requiredThe current status of the research task.Available options: completed content |
| `Hide child attributessources.title` | string | 否 | - | Title or name of the source.Example:"Latest AI Developments"sources.urlstring<uri>URL of the source.Example:"https://example.com/ai-news"sources.faviconstring<uri>URL to the source's favicon.Example:"https://example.com/favicon.ico" |
| `sources` | object | 否 | - | []requiredList of sources used in the research.Hide child attributes sources.titlestringTitle or name of the source.Example:"Latest AI Developments" sources.urlstring<uri>URL of the source.Example:"https://example.com/ai-news" sources.faviconstring<uri>URL to the source's favicon.Example:"https://example.com/favicon.ico" |

## 代码示例

### 示例 1 (text)

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.get_research("123e4567-e89b-12d3-a456-426614174111")

print(response)
```

### 示例 2 (json)

```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174111",
  "created_at": "2025-01-15T10:30:00Z",
  "status": "completed",
  "content": "Research Report: Latest Developments in AI\n\n## Executive Summary\n\nArtificial Intelligence has seen significant advancements in recent months, with major breakthroughs in large language models, multimodal AI systems, and real-world applications...",
  "sources": [
    {
      "title": "Latest AI Developments",
      "url": "https://example.com/ai-news",
      "favicon": "https://example.com/favicon.ico"
    },
    {
      "title": "AI Research Breakthroughs",
      "url": "https://example.com/ai-research",
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "response_time": 1.23
}
```

## 文档正文

Retrieve the status and results of a research task using its request ID.

## API 端点

**Method:** `GET`
**Endpoint:** `/research-get`

Authorizations

Authorization
stringheaderrequired

Bearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

Path Parameters

request_id
stringrequired

The unique identifier of the research task.

Response
200
application/json

Research task is completed or failed.

Completed
Failed

request_id
stringrequired

The unique identifier of the research task.

Example:

"123e4567-e89b-12d3-a456-426614174111"

created_at
stringrequired

Timestamp when the research task was created.

Example:

"2025-01-15T10:30:00Z"

status
enum<string>required

The current status of the research task.

Available options: completed 

content
string
object
string
required

The research report content. Can be a string or a structured object if output_schema was provided.

sources
object[]required

List of sources used in the research.

Hide child attributes

sources.title
string

Title or name of the source.

Example:

"Latest AI Developments"

sources.url
string<uri>

URL of the source.

Example:

"https://example.com/ai-news"

sources.favicon
string<uri>

URL to the source's favicon.

Example:

"https://example.com/favicon.ico"

response_time
integerrequired

Time in seconds it took to complete the request.

Example:

1.23
