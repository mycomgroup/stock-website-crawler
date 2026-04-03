---
id: "url-455f9931"
type: "api"
title: "Introduction"
url: "https://docs.tavily.com/documentation/api-reference/introduction"
description: "Easily integrate our APIs with your services."
source: ""
tags: []
crawl_time: "2026-03-18T02:55:36.687Z"
metadata:
  method: ""
  endpoint: "/research"
  baseUrl: "https://api.tavily.com"
  parameters: []
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"text","code":"https://api.tavily.com"}
    - {"language":"bash","code":"curl -X POST https://api.tavily.com/search \\\n  -H \"Content-Type: application/json\" \\\n  -H \"Authorization: Bearer tvly-YOUR_API_KEY\" \\\n  -d '{\"query\": \"Who is Leo Messi?\"}'"}
    - {"language":"bash","code":"curl -X POST https://api.tavily.com/search \\\n  -H \"Content-Type: application/json\" \\\n  -H \"Authorization: Bearer tvly-YOUR_API_KEY\" \\\n  -H \"X-Project-ID: your-project-id\" \\\n  -d '{\"query\": \"Who is Leo Messi?\"}'"}
  mainContent:
    - {"type":"heading","level":2,"content":"​Base URL"}
    - {"type":"codeblock","language":"text","content":"https://api.tavily.com"}
    - {"type":"heading","level":2,"content":"​Authentication"}
    - {"type":"codeblock","language":"bash","content":"curl -X POST https://api.tavily.com/search \\\n  -H \"Content-Type: application/json\" \\\n  -H \"Authorization: Bearer tvly-YOUR_API_KEY\" \\\n  -d '{\"query\": \"Who is Leo Messi?\"}'"}
    - {"type":"heading","level":2,"content":"​Endpoints"}
    - {"type":"heading","level":2,"content":"​Project Tracking"}
    - {"type":"codeblock","language":"bash","content":"curl -X POST https://api.tavily.com/search \\\n  -H \"Content-Type: application/json\" \\\n  -H \"Authorization: Bearer tvly-YOUR_API_KEY\" \\\n  -H \"X-Project-ID: your-project-id\" \\\n  -d '{\"query\": \"Who is Leo Messi?\"}'"}
    - {"type":"list","listType":"ul","items":["An API key can be associated with multiple projects","Filter requests by project in the /logs endpoint and platform usage dashboard","Helps organize and track where requests originate from"]}
  rawContent: "​\nBase URL\nThe base URL for all requests to the Tavily API is:\n\n\nhttps://api.tavily.com\n\n​\nAuthentication\nAll Tavily endpoints are authenticated using API keys. Get your free API key.\n\n\ncurl -X POST https://api.tavily.com/search \\\n  -H \"Content-Type: application/json\" \\\n  -H \"Authorization: Bearer tvly-YOUR_API_KEY\" \\\n  -d '{\"query\": \"Who is Leo Messi?\"}'\n\n​\nEndpoints\n/search\nTavily’s powerful web search API.\n/extract\nTavily’s powerful content extraction API.\n/crawl , /map\nTavily’s intelligent sitegraph navigation and extraction tools.\n/research\nTavily’s comprehensive research API for in-depth analysis.\n​\nProject Tracking\nYou can optionally attach a Project ID to your API requests to organize and track usage by project. This is useful when a single API key is used across multiple projects or applications.\nTo attach a project to your request, add the X-Project-ID header:\n\n\ncurl -X POST https://api.tavily.com/search \\\n  -H \"Content-Type: application/json\" \\\n  -H \"Authorization: Bearer tvly-YOUR_API_KEY\" \\\n  -H \"X-Project-ID: your-project-id\" \\\n  -d '{\"query\": \"Who is Leo Messi?\"}'\n\nKey features:\nAn API key can be associated with multiple projects\nFilter requests by project in the /logs endpoint and platform usage dashboard\nHelps organize and track where requests originate from\nWhen using the SDKs, you can specify a project using the project_id parameter when instantiating the client, or by setting the TAVILY_PROJECT environment variable."
  suggestedFilename: "introduction"
---

# Introduction

## 源URL

https://docs.tavily.com/documentation/api-reference/introduction

## 描述

Easily integrate our APIs with your services.

## API 端点

**Endpoint**: `/research`
**Base URL**: `https://api.tavily.com`

## 代码示例

### 示例 1 (text)

```text
https://api.tavily.com
```

### 示例 2 (bash)

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tvly-YOUR_API_KEY" \
  -d '{"query": "Who is Leo Messi?"}'
```

## 文档正文

Easily integrate our APIs with your services.

## API 端点

**Endpoint:** `/research`

Base URL
The base URL for all requests to the Tavily API is:

https://api.tavily.com

Authentication
All Tavily endpoints are authenticated using API keys. Get your free API key.

curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tvly-YOUR_API_KEY" \
  -d '{"query": "Who is Leo Messi?"}'

Endpoints
/search
Tavily’s powerful web search API.
/extract
Tavily’s powerful content extraction API.
/crawl , /map
Tavily’s intelligent sitegraph navigation and extraction tools.
/research
Tavily’s comprehensive research API for in-depth analysis.

Project Tracking
You can optionally attach a Project ID to your API requests to organize and track usage by project. This is useful when a single API key is used across multiple projects or applications.
To attach a project to your request, add the X-Project-ID header:

curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tvly-YOUR_API_KEY" \
  -H "X-Project-ID: your-project-id" \
  -d '{"query": "Who is Leo Messi?"}'

Key features:
An API key can be associated with multiple projects
Filter requests by project in the /logs endpoint and platform usage dashboard
Helps organize and track where requests originate from
When using the SDKs, you can specify a project using the project_id parameter when instantiating the client, or by setting the TAVILY_PROJECT environment variable.
