---
id: "url-6aad6432"
type: "api"
title: "Autosuggest"
url: "https://api-dashboard.search.brave.com/documentation/services/suggest"
description: "Brave Search Autosuggest API provides intelligent query autocompletion and search suggestions as\nusers type, helping them formulate better queries and discover relevant content faster. The API\nreturns contextually relevant suggestions based on the partial query input, with optional\nenrichment data for enhanced user experiences. The suggestions provided are resilient to typos\nmade by the user."
source: ""
tags: []
crawl_time: "2026-03-18T02:31:58.265Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/suggest/search?q=hello&country=US&count=5"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Brave Search Autosuggest API provides intelligent query autocompletion and search suggestions as\nusers type, helping them formulate better queries and discover relevant content faster. The API\nreturns contextually relevant suggestions based on the partial query input, with optional\nenrichment data for enhanced user experiences. The suggestions provided are resilient to typos\nmade by the user."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Real-time Suggestions Get instant query completions as users type their search queries   Contextual Results Suggestions adapt based on country and language preferences   Rich Enrichments Enhanced suggestions with titles, descriptions, and images   Entity Detection Identify when suggestions represent specific entities","Rich suggestions with enhanced metadata are included with the Autosuggest\nplan. View pricing for more details."],"codeBlocks":[]}
    - {"level":"H2","title":"Real-time Suggestions","content":["Get instant query completions as users type their search queries"],"codeBlocks":[]}
    - {"level":"H2","title":"Contextual Results","content":["Suggestions adapt based on country and language preferences"],"codeBlocks":[]}
    - {"level":"H2","title":"Rich Enrichments","content":["Enhanced suggestions with titles, descriptions, and images"],"codeBlocks":[]}
    - {"level":"H2","title":"Entity Detection","content":["Identify when suggestions represent specific entities"],"codeBlocks":[]}
    - {"level":"H2","title":"Autosuggest API Documentation","content":["View the complete API reference, including endpoints, parameters, and example\nrequests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Autosuggest API is perfect for:","• Search Boxes: Power autocomplete in search interfaces\n• User Experience: Help users formulate better queries faster\n• Query Refinement: Guide users toward popular or relevant searches\n• Content Discovery: Surface trending or related topics as users type\n• Mobile Applications: Provide touch-friendly query suggestions"],"codeBlocks":[]}
    - {"level":"H2","title":"Endpoint","content":["Brave Autosuggest API is available at the following endpoint:"],"codeBlocks":["https://api.search.brave.com/res/v1/suggest/search"]}
    - {"level":"H2","title":"Getting Started","content":["Get started immediately with a simple cURL request:"],"codeBlocks":["curl \"https://api.search.brave.com/res/v1/suggest/search?q=hello&country=US&count=5\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"","{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello world\"\n    },\n    {\n      \"query\": \"hello kitty\"\n    },\n    {\n      \"query\": \"hello neighbor\"\n    },\n    {\n      \"query\": \"hello fresh\"\n    },\n    {\n      \"query\": \"hello sunshine\"\n    }\n  ]\n}"]}
    - {"level":"H3","title":"Example Response","content":[],"codeBlocks":["{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello world\"\n    },\n    {\n      \"query\": \"hello kitty\"\n    },\n    {\n      \"query\": \"hello neighbor\"\n    },\n    {\n      \"query\": \"hello fresh\"\n    },\n    {\n      \"query\": \"hello sunshine\"\n    }\n  ]\n}"]}
    - {"level":"H2","title":"Rich Suggestions","content":["With the rich=true parameter, suggestions are enhanced with additional metadata:"],"codeBlocks":["curl \"https://api.search.brave.com/res/v1/suggest/search?q=einstein&country=US&count=3&rich=true\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"","{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"einstein\"\n  },\n  \"results\": [\n    {\n      \"query\": \"albert einstein\",\n      \"is_entity\": true,\n      \"title\": \"Albert Einstein\",\n      \"description\": \"Theoretical physicist who developed the theory of relativity\",\n      \"img\": \"https://example.com/einstein.jpg\"\n    },\n    {\n      \"query\": \"einstein theory\",\n      \"is_entity\": false\n    },\n    {\n      \"query\": \"einstein quotes\"\n    }\n  ]\n}"]}
    - {"level":"H3","title":"Enhanced Response Example","content":[],"codeBlocks":["{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"einstein\"\n  },\n  \"results\": [\n    {\n      \"query\": \"albert einstein\",\n      \"is_entity\": true,\n      \"title\": \"Albert Einstein\",\n      \"description\": \"Theoretical physicist who developed the theory of relativity\",\n      \"img\": \"https://example.com/einstein.jpg\"\n    },\n    {\n      \"query\": \"einstein theory\",\n      \"is_entity\": false\n    },\n    {\n      \"query\": \"einstein quotes\"\n    }\n  ]\n}"]}
    - {"level":"H2","title":"Best Practices","content":["• Debounce Requests: Implement debouncing (e.g., 150-300ms) to avoid excessive API calls as users type\n• Progressive Enhancement: Load suggestions asynchronously without blocking the UI","• Only make requests after users pause typing (debouncing)\n• Implement client-side caching for repeated queries\n• Consider your subscription plan’s rate limits when designing your integration"],"codeBlocks":[]}
    - {"level":"H3","title":"Performance Optimization","content":["• Debounce Requests: Implement debouncing (e.g., 150-300ms) to avoid excessive API calls as users type\n• Progressive Enhancement: Load suggestions asynchronously without blocking the UI"],"codeBlocks":[]}
    - {"level":"H3","title":"Rate Limiting","content":["• Only make requests after users pause typing (debouncing)\n• Implement client-side caching for repeated queries\n• Consider your subscription plan’s rate limits when designing your integration"],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave Search Autosuggest API in chronological order.","• 2023-05-01 Add search suggestions endpoint"],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/suggest/search?q=hello&country=US&count=5\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/suggest/search?q=hello&country=US&count=5\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello world\"\n    },\n    {\n      \"query\": \"hello kitty\"\n    },\n    {\n      \"query\": \"hello neighbor\"\n    },\n    {\n      \"query\": \"hello fresh\"\n    },\n    {\n      \"query\": \"hello sunshine\"\n    }\n  ]\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello world\"\n    },\n    {\n      \"query\": \"hello kitty\"\n    },\n    {\n      \"query\": \"hello neighbor\"\n    },\n    {\n      \"query\": \"hello fresh\"\n    },\n    {\n      \"query\": \"hello sunshine\"\n    }\n  ]\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/suggest/search?q=einstein&country=US&count=3&rich=true\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/suggest/search?q=einstein&country=US&count=3&rich=true\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"einstein\"\n  },\n  \"results\": [\n    {\n      \"query\": \"albert einstein\",\n      \"is_entity\": true,\n      \"title\": \"Albert Einstein\",\n      \"description\": \"Theoretical physicist who developed the theory of relativity\",\n      \"img\": \"https://example.com/einstein.jpg\"\n    },\n    {\n      \"query\": \"einstein theory\",\n      \"is_entity\": false\n    },\n    {\n      \"query\": \"einstein quotes\"\n    }\n  ]\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"suggest\",\n  \"query\": {\n    \"original\": \"einstein\"\n  },\n  \"results\": [\n    {\n      \"query\": \"albert einstein\",\n      \"is_entity\": true,\n      \"title\": \"Albert Einstein\",\n      \"description\": \"Theoretical physicist who developed the theory of relativity\",\n      \"img\": \"https://example.com/einstein.jpg\"\n    },\n    {\n      \"query\": \"einstein theory\",\n      \"is_entity\": false\n    },\n    {\n      \"query\": \"einstein quotes\"\n    }\n  ]\n}"}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nReal-time query autocompletion and suggestions to enhance search experiences\n\nOverview\n\nBrave Search Autosuggest API provides intelligent query autocompletion and search suggestions as\nusers type, helping them formulate better queries and discover relevant content faster. The API\nreturns contextually relevant suggestions based on the partial query input, with optional\nenrichment data for enhanced user experiences. The suggestions provided are resilient to typos\nmade by the user.\n\nKey Features\n\nReal-time Suggestions\n\nGet instant query completions as users type their search queries\n\nContextual Results\n\nSuggestions adapt based on country and language preferences\n\nRich Enrichments\n\nEnhanced suggestions with titles, descriptions, and images\n\nEntity Detection\n\nIdentify when suggestions represent specific entities\n\nRich suggestions with enhanced metadata are included with the Autosuggest\nplan. View pricing for more details.\n\nAPI Reference\n\nAutosuggest API Documentation\n\nView the complete API reference, including endpoints, parameters, and example\nrequests\n\nUse Cases\n\nAutosuggest API is perfect for:\n\nSearch Boxes: Power autocomplete in search interfaces\n\nUser Experience: Help users formulate better queries faster\n\nQuery Refinement: Guide users toward popular or relevant searches\n\nContent Discovery: Surface trending or related topics as users type\n\nMobile Applications: Provide touch-friendly query suggestions\n\nEndpoint\n\nBrave Autosuggest API is available at the following endpoint:\n\nGetting Started\n\nGet started immediately with a simple cURL request:\n\nExample Response\n\nRich Suggestions\n\nWith the rich=true parameter, suggestions are enhanced with additional metadata:\n\nEnhanced Response Example\n\nIntegration Examples\n\nNode.js\n\nPython\n\nBest Practices\n\nPerformance Optimization\n\nDebounce Requests: Implement debouncing (e.g., 150-300ms) to avoid excessive API calls as users type\n\nProgressive Enhancement: Load suggestions asynchronously without blocking the UI\n\nRate Limiting\n\nOnly make requests after users pause typing (debouncing)\n\nImplement client-side caching for repeated queries\n\nConsider your subscription plan’s rate limits when designing your integration\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave Search Autosuggest API in chronological order.\n\n2023-05-01 Add search suggestions endpoint\n\nOn this page\n\nReal-time Suggestions Get instant query completions as users type their search queries\n\nContextual Results Suggestions adapt based on country and language preferences\n\nRich Enrichments Enhanced suggestions with titles, descriptions, and images\n\nEntity Detection Identify when suggestions represent specific entities\n\nAutosuggest API Documentation View the complete API reference, including endpoints, parameters, and example\nrequests"
  suggestedFilename: "services-suggest"
---

# Autosuggest

## 源URL

https://api-dashboard.search.brave.com/documentation/services/suggest

## 描述

Brave Search Autosuggest API provides intelligent query autocompletion and search suggestions as
users type, helping them formulate better queries and discover relevant content faster. The API
returns contextually relevant suggestions based on the partial query input, with optional
enrichment data for enhanced user experiences. The suggestions provided are resilient to typos
made by the user.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/suggest/search?q=hello&country=US&count=5`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/suggest/search?q=hello&country=US&count=5" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "suggest",
  "query": {
    "original": "hello"
  },
  "results": [
    {
      "query": "hello world"
    },
    {
      "query": "hello kitty"
    },
    {
      "query": "hello neighbor"
    },
    {
      "query": "hello fresh"
    },
    {
      "query": "hello sunshine"
    }
  ]
}
```

## 文档正文

Brave Search Autosuggest API provides intelligent query autocompletion and search suggestions as
users type, helping them formulate better queries and discover relevant content faster. The API
returns contextually relevant suggestions based on the partial query input, with optional
enrichment data for enhanced user experiences. The suggestions provided are resilient to typos
made by the user.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/suggest/search?q=hello&country=US&count=5`

Quickstart

Pricing

Authentication

Versioning

Rate limiting

Web search

LLM Context New

News search

Video search

Image search

Summarizer search

Place search New

Answers

Autosuggest

Spellcheck

Skills

Help & Feedback

Goggles

Search operators

Status updates

Security

Privacy notice

Terms of service

Service APIs

Real-time query autocompletion and suggestions to enhance search experiences

Overview

Brave Search Autosuggest API provides intelligent query autocompletion and search suggestions as
users type, helping them formulate better queries and discover relevant content faster. The API
returns contextually relevant suggestions based on the partial query input, with optional
enrichment data for enhanced user experiences. The suggestions provided are resilient to typos
made by the user.

Key Features

Real-time Suggestions

Get instant query completions as users type their search queries

Contextual Results

Suggestions adapt based on country and language preferences

Rich Enrichments

Enhanced suggestions with titles, descriptions, and images

Entity Detection

Identify when suggestions represent specific entities

Rich suggestions with enhanced metadata are included with the Autosuggest
plan. View pricing for more details.

API Reference

Autosuggest API Documentation

View the complete API reference, including endpoints, parameters, and example
requests

Use Cases

Autosuggest API is perfect for:

Search Boxes: Power autocomplete in search interfaces

User Experience: Help users formulate better queries faster

Query Refinement: Guide users toward popular or relevant searches

Content Discovery: Surface trending or related topics as users type

Mobile Applications: Provide touch-friendly query suggestions

Endpoint

Brave Autosuggest API is available at the following endpoint:

Getting Started

Get started immediately with a simple cURL request:

Example Response

Rich Suggestions

With the rich=true parameter, suggestions are enhanced with additional metadata:

Enhanced Response Example

Integration Examples

Node.js

Python

Best Practices

Performance Optimization

Debounce Requests: Implement debouncing (e.g., 150-300ms) to avoid excessive API calls as users type

Progressive Enhancement: Load suggestions asynchronously without blocking the UI

Rate Limiting

Only make requests after users pause typing (debouncing)

Implement client-side caching for repeated queries

Consider your subscription plan’s rate limits when designing your integration

Changelog

This changelog outlines all significant changes to the Brave Search Autosuggest API in chronological order.

2023-05-01 Add search suggestions endpoint

On this page

Real-time Suggestions Get instant query completions as users type their search queries

Contextual Results Suggestions adapt based on country and language preferences

Rich Enrichments Enhanced suggestions with titles, descriptions, and images

Entity Detection Identify when suggestions represent specific entities

Autosuggest API Documentation View the complete API reference, including endpoints, parameters, and example
requests
