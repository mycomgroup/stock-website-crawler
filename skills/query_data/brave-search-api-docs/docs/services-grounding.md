---
id: "url-1fcfbec5"
type: "api"
title: "Documentation"
url: "https://api-dashboard.search.brave.com/documentation/services/grounding"
description: "Brave AI Answers API provides state-of-the-art AI-generated answers backed\nby verifiable sources from the web. This technology improves the accuracy,\nrelevance, and trustworthiness of AI responses by grounding them in real-time\nsearch results. Under the hood, this same service powers Brave’s Ask Brave feature, which serves millions\nof answers every day."
source: ""
tags: []
crawl_time: "2026-03-18T02:32:42.106Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/chat/completions"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Brave AI Answers API provides state-of-the-art AI-generated answers backed\nby verifiable sources from the web. This technology improves the accuracy,\nrelevance, and trustworthiness of AI responses by grounding them in real-time\nsearch results. Under the hood, this same service powers Brave’s Ask Brave feature, which serves millions\nof answers every day.","Brave’s grounded answers demonstrate strong performance across a wide range of\nqueries, from simple trivia questions to complex research inquiries. Notably,\nBrave achieves state-of-the-art (SOTA) performance on the SimpleQA benchmark without being specifically optimized for it—the performance emerges naturally\nfrom the system’s design.","Access to the API is available through the Answers plan. Subscribe to Answers to unlock these capabilities."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Web-Grounded Answers AI responses backed by real-time web search with verifiable citations   OpenAI SDK Compatible Use the familiar OpenAI SDK for seamless integration   SOTA Performance State-of-the-art results on SimpleQA benchmark   Streaming Support Stream answers in real-time with progressive citations   Research Mode Enable multi-search for thorough, research-grade answers   Rich Response Data Get entities, citations, and structured data with answers"],"codeBlocks":[]}
    - {"level":"H2","title":"Web-Grounded Answers","content":["AI responses backed by real-time web search with verifiable citations"],"codeBlocks":[]}
    - {"level":"H2","title":"OpenAI SDK Compatible","content":["Use the familiar OpenAI SDK for seamless integration"],"codeBlocks":[]}
    - {"level":"H2","title":"SOTA Performance","content":["State-of-the-art results on SimpleQA benchmark"],"codeBlocks":[]}
    - {"level":"H2","title":"Streaming Support","content":["Stream answers in real-time with progressive citations"],"codeBlocks":[]}
    - {"level":"H2","title":"Research Mode","content":["Enable multi-search for thorough, research-grade answers"],"codeBlocks":[]}
    - {"level":"H2","title":"Rich Response Data","content":["Get entities, citations, and structured data with answers"],"codeBlocks":[]}
    - {"level":"H2","title":"Answers API Documentation","content":["View the complete API reference, including parameters and response schemas"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Answers is perfect for:","• AI Assistants & Chatbots: Build intelligent conversational interfaces with factual, cited responses\n• Research Applications: Conduct thorough research with multi-search capabilities\n• Question Answering Systems: Provide accurate answers with source attribution\n• Knowledge Applications: Create tools that need up-to-date, verifiable information\n• Content Generation: Generate well-researched content with citations"],"codeBlocks":[]}
    - {"level":"H2","title":"Endpoint","content":["Answers uses a single, OpenAI-compatible endpoint:"],"codeBlocks":["https://api.search.brave.com/res/v1/chat/completions"]}
    - {"level":"H2","title":"Quick Start","content":["For real-time responses, enable streaming with AsyncOpenAI:","While the OpenAI SDK is recommended, you can also use cURL:"],"codeBlocks":[]}
    - {"level":"H3","title":"Streaming Example","content":["For real-time responses, enable streaming with AsyncOpenAI:"],"codeBlocks":[]}
    - {"level":"H3","title":"Using cURL","content":["While the OpenAI SDK is recommended, you can also use cURL:"],"codeBlocks":[]}
    - {"level":"H2","title":"Single vs Multiple Searches","content":["The decision between single-search and multi-search significantly influences\nboth cost efficiency and response time.","• Speed: Answers typically stream in under 4.5 seconds on average\n• Cost: Lower cost with minimal computational overhead\n• Use Case: Ideal for real-time applications and most queries\n• Performance: Median SimpleQA benchmark question answered with single search","• Thoroughness: Model iteratively refines strategy with sequential searches\n• Cost: Higher due to multiple API calls and larger context processing\n• Time: Response times can extend to minutes\n• Use Case: Best for background tasks prioritizing thoroughness over speed","Enable research mode by adding enable_research: true:","Performance note: On the SimpleQA benchmark, p99 questions required 53\nqueries analyzing 1000 pages over ~300 seconds. However, reasonable limits are\nin place based on real-world use cases."],"codeBlocks":[]}
    - {"level":"H3","title":"Single Search (Default)","content":["• Speed: Answers typically stream in under 4.5 seconds on average\n• Cost: Lower cost with minimal computational overhead\n• Use Case: Ideal for real-time applications and most queries\n• Performance: Median SimpleQA benchmark question answered with single search"],"codeBlocks":[]}
    - {"level":"H3","title":"Multiple Searches (Research Mode)","content":["• Thoroughness: Model iteratively refines strategy with sequential searches\n• Cost: Higher due to multiple API calls and larger context processing\n• Time: Response times can extend to minutes\n• Use Case: Best for background tasks prioritizing thoroughness over speed","Enable research mode by adding enable_research: true:","Performance note: On the SimpleQA benchmark, p99 questions required 53\nqueries analyzing 1000 pages over ~300 seconds. However, reasonable limits are\nin place based on real-world use cases."],"codeBlocks":[]}
    - {"level":"H2","title":"Advanced Parameters","content":["When using the OpenAI SDK, pass additional parameters via extra_body:","All advanced parameters: entities, citations and research mode require streaming\nmode to be true.","• country (string): Target country for search results (default: us)\n• language (string): Response language (default: en)\n• enable_entities (bool): Include entity information in responses (default: false)\n• enable_citations (bool): Include inline citations (default: false)\n• enable_research (bool): Enable multi-search research mode (default: false)"],"codeBlocks":[]}
    - {"level":"H3","title":"Available Parameters","content":["• country (string): Target country for search results (default: us)\n• language (string): Response language (default: en)\n• enable_entities (bool): Include entity information in responses (default: false)\n• enable_citations (bool): Include inline citations (default: false)\n• enable_research (bool): Enable multi-search research mode (default: false)"],"codeBlocks":[]}
    - {"level":"H2","title":"Response Format","content":["Because Answers uses custom messages with richer data than standard OpenAI responses, messages are stringified with special tags. When streaming, you’ll receive:","Regular answer content streamed as text."],"codeBlocks":["<citation>{\"start_index\": 0, \"end_index\": 10, \"number\": 1, \"url\": \"https://...\", \"favicon\": \"...\", \"snippet\": \"...\"}</citation>","<enum_item>{\"uuid\": \"...\", \"name\": \"...\", \"href\": \"...\", \"original_tokens\": \"...\", \"citations\": [...]}</enum_item>","<usage>{ \"X-Request-Requests\": 1, \"X-Request-Queries\": 2, \"X-Request-Tokens-In\": 1234, \"X-Request-Tokens-Out\": 300, \"X-Request-Requests-Cost\": 0, \"X-Request-Queries-Cost\": 0.008, \"X-Request-Tokens-In-Cost\": 0.00617, \"X-Request-Tokens-Out-Cost\": 0.0015, \"X-Request-Total-Cost\": 0.01567 }</usage>"]}
    - {"level":"H3","title":"Standard Text","content":["Regular answer content streamed as text."],"codeBlocks":[]}
    - {"level":"H3","title":"Citations","content":[],"codeBlocks":["<citation>{\"start_index\": 0, \"end_index\": 10, \"number\": 1, \"url\": \"https://...\", \"favicon\": \"...\", \"snippet\": \"...\"}</citation>"]}
    - {"level":"H3","title":"Entity Items","content":[],"codeBlocks":["<enum_item>{\"uuid\": \"...\", \"name\": \"...\", \"href\": \"...\", \"original_tokens\": \"...\", \"citations\": [...]}</enum_item>"]}
    - {"level":"H3","title":"Usage Metadata","content":[],"codeBlocks":["<usage>{ \"X-Request-Requests\": 1, \"X-Request-Queries\": 2, \"X-Request-Tokens-In\": 1234, \"X-Request-Tokens-Out\": 300, \"X-Request-Requests-Cost\": 0, \"X-Request-Queries-Cost\": 0.008, \"X-Request-Tokens-In-Cost\": 0.00617, \"X-Request-Tokens-Out-Cost\": 0.0015, \"X-Request-Total-Cost\": 0.01567 }</usage>"]}
    - {"level":"H2","title":"Complete Streaming Example","content":["Here’s a full example that handles all message types:"],"codeBlocks":[]}
    - {"level":"H2","title":"Pricing & Spending Limits","content":["Answers uses a usage-based pricing model:","Cost Calculation:","• 2 searches\n• 1,234 input tokens\n• 300 output tokens","With each answer, you’ll receive metadata on resource usage:","When streaming, this metadata comes as the last message. For synchronous requests, the keys above are included in response headers.","Control your spending by setting monthly credit limits in your account.","Limit behavior: Limits are checked before answering. If limits aren’t\nexceeded when a question starts, it will be answered in full even if it\nexceeds limits during processing. You’ll only be charged up to your imposed\nlimit.","• Default: 2 requests per second\n• Need more? Contact searchapi-support@brave.com"],"codeBlocks":["cost = (searches × $4/1000) + (input_tokens × $5/1000000) + (output_tokens × $5/1000000)","Cost = 2 × (4/1000) + (5/1000000) × 1234 + (5/1000000) × 300\n     = $0.01567","{\n  \"X-Request-Requests\": 1,\n  \"X-Request-Queries\": 2,\n  \"X-Request-Tokens-In\": 1234,\n  \"X-Request-Tokens-Out\": 300,\n  \"X-Request-Requests-Cost\": 0,\n  \"X-Request-Queries-Cost\": 0.008,\n  \"X-Request-Tokens-In-Cost\": 0.00617,\n  \"X-Request-Tokens-Out-Cost\": 0.0015,\n  \"X-Request-Total-Cost\": 0.01567\n}"]}
    - {"level":"H3","title":"Usage Metadata","content":["With each answer, you’ll receive metadata on resource usage:","When streaming, this metadata comes as the last message. For synchronous requests, the keys above are included in response headers."],"codeBlocks":["{\n  \"X-Request-Requests\": 1,\n  \"X-Request-Queries\": 2,\n  \"X-Request-Tokens-In\": 1234,\n  \"X-Request-Tokens-Out\": 300,\n  \"X-Request-Requests-Cost\": 0,\n  \"X-Request-Queries-Cost\": 0.008,\n  \"X-Request-Tokens-In-Cost\": 0.00617,\n  \"X-Request-Tokens-Out-Cost\": 0.0015,\n  \"X-Request-Total-Cost\": 0.01567\n}"]}
    - {"level":"H3","title":"Setting Limits","content":["Control your spending by setting monthly credit limits in your account.","Limit behavior: Limits are checked before answering. If limits aren’t\nexceeded when a question starts, it will be answered in full even if it\nexceeds limits during processing. You’ll only be charged up to your imposed\nlimit."],"codeBlocks":[]}
    - {"level":"H3","title":"Rate Limits","content":["• Default: 2 requests per second\n• Need more? Contact searchapi-support@brave.com"],"codeBlocks":[]}
    - {"level":"H2","title":"Best Practices","content":["• Always handle special message tags (<citation>, <enum_item>, <usage>)\n• Parse JSON content within tags to extract structured data\n• Display citations inline for better user trust","• Use AsyncOpenAI for streaming responses\n• Display content progressively for better UX\n• Handle usage metadata at the end of the stream","• Enable only when thoroughness is more important than speed\n• Best for background processing or complex research queries\n• Monitor usage as it can incur higher costs","• Implement retry logic for transient failures\n• Check spending limits before critical operations\n• Handle rate limit errors gracefully","• Use single-search mode (default) for most queries\n• Cache responses when appropriate to minimize API calls\n• Monitor usage metadata to optimize costs"],"codeBlocks":[]}
    - {"level":"H3","title":"Message Handling","content":["• Always handle special message tags (<citation>, <enum_item>, <usage>)\n• Parse JSON content within tags to extract structured data\n• Display citations inline for better user trust"],"codeBlocks":[]}
    - {"level":"H3","title":"Streaming","content":["• Use AsyncOpenAI for streaming responses\n• Display content progressively for better UX\n• Handle usage metadata at the end of the stream"],"codeBlocks":[]}
    - {"level":"H3","title":"Research Mode","content":["• Enable only when thoroughness is more important than speed\n• Best for background processing or complex research queries\n• Monitor usage as it can incur higher costs"],"codeBlocks":[]}
    - {"level":"H3","title":"Error Handling","content":["• Implement retry logic for transient failures\n• Check spending limits before critical operations\n• Handle rate limit errors gracefully"],"codeBlocks":[]}
    - {"level":"H3","title":"Performance","content":["• Use single-search mode (default) for most queries\n• Cache responses when appropriate to minimize API calls\n• Monitor usage metadata to optimize costs"],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave Answers API in chronological order.","• Launch Brave Answers API resource\n• OpenAI SDK compatibility\n• Support for single and multi-search modes\n• SOTA performance on SimpleQA benchmark"],"codeBlocks":[]}
    - {"level":"H3","title":"2025-08-05","content":["• Launch Brave Answers API resource\n• OpenAI SDK compatibility\n• Support for single and multi-search modes\n• SOTA performance on SimpleQA benchmark"],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl -X POST \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"stream\": false, \"messages\": [{\"role\": \"user\", \"content\": \"What is the second highest mountain?\"}]}' \\\n  -H \"x-subscription-token: <YOUR_BRAVE_SEARCH_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl -X POST \"https://api.search.brave.com/res/v1/chat/completions\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"stream\": false, \"messages\": [{\"role\": \"user\", \"content\": \"What is the second highest mountain?\"}]}' \\\n  -H \"x-subscription-token: <YOUR_BRAVE_SEARCH_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"X-Request-Requests\": 1,\n  \"X-Request-Queries\": 2,\n  \"X-Request-Tokens-In\": 1234,\n  \"X-Request-Tokens-Out\": 300,\n  \"X-Request-Requests-Cost\": 0,\n  \"X-Request-Queries-Cost\": 0.008,\n  \"X-Request-Tokens-In-Cost\": 0.00617,\n  \"X-Request-Tokens-Out-Cost\": 0.0015,\n  \"X-Request-Total-Cost\": 0.01567\n}"}
    - {"type":"response","language":"json","code":"{\n  \"X-Request-Requests\": 1,\n  \"X-Request-Queries\": 2,\n  \"X-Request-Tokens-In\": 1234,\n  \"X-Request-Tokens-Out\": 300,\n  \"X-Request-Requests-Cost\": 0,\n  \"X-Request-Queries-Cost\": 0.008,\n  \"X-Request-Tokens-In-Cost\": 0.00617,\n  \"X-Request-Tokens-Out-Cost\": 0.0015,\n  \"X-Request-Total-Cost\": 0.01567\n}"}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nAPI for AI-generated answers backed by real-time web search and verifiable sources\n\nOverview\n\nBrave AI Answers API provides state-of-the-art AI-generated answers backed\nby verifiable sources from the web. This technology improves the accuracy,\nrelevance, and trustworthiness of AI responses by grounding them in real-time\nsearch results. Under the hood, this same service powers Brave’s Ask Brave feature, which serves millions\nof answers every day.\n\nBrave’s grounded answers demonstrate strong performance across a wide range of\nqueries, from simple trivia questions to complex research inquiries. Notably,\nBrave achieves state-of-the-art (SOTA) performance on the SimpleQA benchmark without being specifically optimized for it—the performance emerges naturally\nfrom the system’s design.\n\nAccess to the API is available through the Answers plan. Subscribe to Answers to unlock these capabilities.\n\nKey Features\n\nWeb-Grounded Answers\n\nAI responses backed by real-time web search with verifiable citations\n\nOpenAI SDK Compatible\n\nUse the familiar OpenAI SDK for seamless integration\n\nSOTA Performance\n\nState-of-the-art results on SimpleQA benchmark\n\nStreaming Support\n\nStream answers in real-time with progressive citations\n\nResearch Mode\n\nEnable multi-search for thorough, research-grade answers\n\nRich Response Data\n\nGet entities, citations, and structured data with answers\n\nAPI Reference\n\nAnswers API Documentation\n\nView the complete API reference, including parameters and response schemas\n\nUse Cases\n\nAnswers is perfect for:\n\nAI Assistants & Chatbots: Build intelligent conversational interfaces with factual, cited responses\n\nResearch Applications: Conduct thorough research with multi-search capabilities\n\nQuestion Answering Systems: Provide accurate answers with source attribution\n\nKnowledge Applications: Create tools that need up-to-date, verifiable information\n\nContent Generation: Generate well-researched content with citations\n\nEndpoint\n\nAnswers uses a single, OpenAI-compatible endpoint:\n\nQuick Start\n\nBasic Example with OpenAI SDK\n\nPython\n\nStreaming Example\n\nFor real-time responses, enable streaming with AsyncOpenAI:\n\nUsing cURL\n\nWhile the OpenAI SDK is recommended, you can also use cURL:\n\nSingle vs Multiple Searches\n\nThe decision between single-search and multi-search significantly influences\nboth cost efficiency and response time.\n\nSingle Search (Default)\n\nSpeed: Answers typically stream in under 4.5 seconds on average\n\nCost: Lower cost with minimal computational overhead\n\nUse Case: Ideal for real-time applications and most queries\n\nPerformance: Median SimpleQA benchmark question answered with single search\n\nMultiple Searches (Research Mode)\n\nThoroughness: Model iteratively refines strategy with sequential searches\n\nCost: Higher due to multiple API calls and larger context processing\n\nTime: Response times can extend to minutes\n\nUse Case: Best for background tasks prioritizing thoroughness over speed\n\nEnable research mode by adding enable_research: true:\n\nPerformance note: On the SimpleQA benchmark, p99 questions required 53\nqueries analyzing 1000 pages over ~300 seconds. However, reasonable limits are\nin place based on real-world use cases.\n\nAdvanced Parameters\n\nWhen using the OpenAI SDK, pass additional parameters via extra_body:\n\nAll advanced parameters: entities, citations and research mode require streaming\nmode to be true.\n\nAvailable Parameters\n\ncountry (string): Target country for search results (default: us)\n\nlanguage (string): Response language (default: en)\n\nenable_entities (bool): Include entity information in responses (default: false)\n\nenable_citations (bool): Include inline citations (default: false)\n\nenable_research (bool): Enable multi-search research mode (default: false)\n\nResponse Format\n\nBecause Answers uses custom messages with richer data than standard OpenAI responses, messages are stringified with special tags. When streaming, you’ll receive:\n\nStandard Text\n\nRegular answer content streamed as text.\n\nCitations\n\nEntity Items\n\nUsage Metadata\n\nComplete Streaming Example\n\nHere’s a full example that handles all message types:\n\nPricing & Spending Limits\n\nAnswers uses a usage-based pricing model:\n\nCost Calculation:\n\nExample:\n\n2 searches\n\n1,234 input tokens\n\n300 output tokens\n\nWith each answer, you’ll receive metadata on resource usage:\n\nWhen streaming, this metadata comes as the last message. For synchronous requests, the keys above are included in response headers.\n\nSetting Limits\n\nControl your spending by setting monthly credit limits in your account.\n\nLimit behavior: Limits are checked before answering. If limits aren’t\nexceeded when a question starts, it will be answered in full even if it\nexceeds limits during processing. You’ll only be charged up to your imposed\nlimit.\n\nRate Limits\n\nDefault: 2 requests per second\n\nNeed more? Contact searchapi-support@brave.com\n\nBest Practices\n\nMessage Handling\n\nAlways handle special message tags (<citation>, <enum_item>, <usage>)\n\nParse JSON content within tags to extract structured data\n\nDisplay citations inline for better user trust\n\nStreaming\n\nUse AsyncOpenAI for streaming responses\n\nDisplay content progressively for better UX\n\nHandle usage metadata at the end of the stream\n\nEnable only when thoroughness is more important than speed\n\nBest for background processing or complex research queries\n\nMonitor usage as it can incur higher costs\n\nError Handling\n\nImplement retry logic for transient failures\n\nCheck spending limits before critical operations\n\nHandle rate limit errors gracefully\n\nPerformance\n\nUse single-search mode (default) for most queries\n\nCache responses when appropriate to minimize API calls\n\nMonitor usage metadata to optimize costs\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave Answers API in chronological order.\n\n2025-08-05\n\nLaunch Brave Answers API resource\n\nOpenAI SDK compatibility\n\nSupport for single and multi-search modes\n\nSOTA performance on SimpleQA benchmark\n\nOn this page\n\nWeb-Grounded Answers AI responses backed by real-time web search with verifiable citations\n\nOpenAI SDK Compatible Use the familiar OpenAI SDK for seamless integration\n\nSOTA Performance State-of-the-art results on SimpleQA benchmark\n\nStreaming Support Stream answers in real-time with progressive citations\n\nResearch Mode Enable multi-search for thorough, research-grade answers\n\nRich Response Data Get entities, citations, and structured data with answers\n\nAnswers API Documentation View the complete API reference, including parameters and response schemas"
  suggestedFilename: "services-grounding"
---

# Documentation

## 源URL

https://api-dashboard.search.brave.com/documentation/services/grounding

## 描述

Brave AI Answers API provides state-of-the-art AI-generated answers backed
by verifiable sources from the web. This technology improves the accuracy,
relevance, and trustworthiness of AI responses by grounding them in real-time
search results. Under the hood, this same service powers Brave’s Ask Brave feature, which serves millions
of answers every day.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/chat/completions`

## 代码示例

### 示例 1 (bash)

```bash
curl -X POST "https://api.search.brave.com/res/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"stream": false, "messages": [{"role": "user", "content": "What is the second highest mountain?"}]}' \
  -H "x-subscription-token: <YOUR_BRAVE_SEARCH_API_KEY>"
```

### 示例 2 (json)

```json
{
  "X-Request-Requests": 1,
  "X-Request-Queries": 2,
  "X-Request-Tokens-In": 1234,
  "X-Request-Tokens-Out": 300,
  "X-Request-Requests-Cost": 0,
  "X-Request-Queries-Cost": 0.008,
  "X-Request-Tokens-In-Cost": 0.00617,
  "X-Request-Tokens-Out-Cost": 0.0015,
  "X-Request-Total-Cost": 0.01567
}
```

## 文档正文

Brave AI Answers API provides state-of-the-art AI-generated answers backed
by verifiable sources from the web. This technology improves the accuracy,
relevance, and trustworthiness of AI responses by grounding them in real-time
search results. Under the hood, this same service powers Brave’s Ask Brave feature, which serves millions
of answers every day.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/chat/completions`

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

API for AI-generated answers backed by real-time web search and verifiable sources

Overview

Brave AI Answers API provides state-of-the-art AI-generated answers backed
by verifiable sources from the web. This technology improves the accuracy,
relevance, and trustworthiness of AI responses by grounding them in real-time
search results. Under the hood, this same service powers Brave’s Ask Brave feature, which serves millions
of answers every day.

Brave’s grounded answers demonstrate strong performance across a wide range of
queries, from simple trivia questions to complex research inquiries. Notably,
Brave achieves state-of-the-art (SOTA) performance on the SimpleQA benchmark without being specifically optimized for it—the performance emerges naturally
from the system’s design.

Access to the API is available through the Answers plan. Subscribe to Answers to unlock these capabilities.

Key Features

Web-Grounded Answers

AI responses backed by real-time web search with verifiable citations

OpenAI SDK Compatible

Use the familiar OpenAI SDK for seamless integration

SOTA Performance

State-of-the-art results on SimpleQA benchmark

Streaming Support

Stream answers in real-time with progressive citations

Research Mode

Enable multi-search for thorough, research-grade answers

Rich Response Data

Get entities, citations, and structured data with answers

API Reference

Answers API Documentation

View the complete API reference, including parameters and response schemas

Use Cases

Answers is perfect for:

AI Assistants & Chatbots: Build intelligent conversational interfaces with factual, cited responses

Research Applications: Conduct thorough research with multi-search capabilities

Question Answering Systems: Provide accurate answers with source attribution

Knowledge Applications: Create tools that need up-to-date, verifiable information

Content Generation: Generate well-researched content with citations

Endpoint

Answers uses a single, OpenAI-compatible endpoint:

Quick Start

Basic Example with OpenAI SDK

Python

Streaming Example

For real-time responses, enable streaming with AsyncOpenAI:

Using cURL

While the OpenAI SDK is recommended, you can also use cURL:

Single vs Multiple Searches

The decision between single-search and multi-search significantly influences
both cost efficiency and response time.

Single Search (Default)

Speed: Answers typically stream in under 4.5 seconds on average

Cost: Lower cost with minimal computational overhead

Use Case: Ideal for real-time applications and most queries

Performance: Median SimpleQA benchmark question answered with single search

Multiple Searches (Research Mode)

Thoroughness: Model iteratively refines strategy with sequential searches

Cost: Higher due to multiple API calls and larger context processing

Time: Response times can extend to minutes

Use Case: Best for background tasks prioritizing thoroughness over speed

Enable research mode by adding enable_research: true:

Performance note: On the SimpleQA benchmark, p99 questions required 53
queries analyzing 1000 pages over ~300 seconds. However, reasonable limits are
in place based on real-world use cases.

Advanced Parameters

When using the OpenAI SDK, pass additional parameters via extra_body:

All advanced parameters: entities, citations and research mode require streaming
mode to be true.

Available Parameters

country (string): Target country for search results (default: us)

language (string): Response language (default: en)

enable_entities (bool): Include entity information in responses (default: false)

enable_citations (bool): Include inline citations (default: false)

enable_research (bool): Enable multi-search research mode (default: false)

Response Format

Because Answers uses custom messages with richer data than standard OpenAI responses, messages are stringified with special tags. When streaming, you’ll receive:

Standard Text

Regular answer content streamed as text.

Citations

Entity Items

Usage Metadata

Complete Streaming Example

Here’s a full example that handles all message types:

Pricing & Spending Limits

Answers uses a usage-based pricing model:

Cost Calculation:

Example:

2 searches

1,234 input tokens

300 output tokens

With each answer, you’ll receive metadata on resource usage:

When streaming, this metadata comes as the last message. For synchronous requests, the keys above are included in response headers.

Setting Limits

Control your spending by setting monthly credit limits in your account.

Limit behavior: Limits are checked before answering. If limits aren’t
exceeded when a question starts, it will be answered in full eve
