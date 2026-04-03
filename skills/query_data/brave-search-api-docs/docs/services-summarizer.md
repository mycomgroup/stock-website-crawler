---
id: "url-7e08f6c7"
type: "api"
title: "Summarizer search"
url: "https://api-dashboard.search.brave.com/documentation/services/summarizer"
description: "Brave Summarizer Search API leverages advanced AI to provide intelligent summaries and\nanswers based on real-time web search results. Our “AI Answers” feature goes beyond\ntraditional search by understanding your query, gathering relevant information from across\nthe web, and synthesizing it into clear, comprehensive responses with citations."
source: ""
tags: []
crawl_time: "2026-03-18T02:32:58.483Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search?q=what+is+the+second+highest+mountain&summary=1"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Brave Summarizer Search API leverages advanced AI to provide intelligent summaries and\nanswers based on real-time web search results. Our “AI Answers” feature goes beyond\ntraditional search by understanding your query, gathering relevant information from across\nthe web, and synthesizing it into clear, comprehensive responses with citations.","Access to Summarizer is available through the discontinued Pro AI plan.\nUsers who are subscribed to the Pro AI plan can continue using the API with the same\nfunctionality and price."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["AI-Generated Answers Get comprehensive, AI-synthesized answers to your questions with citations   Modular Output Access answers through various specialized endpoints for different use\ncases   Entity Enrichment Get detailed information about entities mentioned in summaries   Inline Citations Answers include inline references to source materials"],"codeBlocks":[]}
    - {"level":"H2","title":"AI-Generated Answers","content":["Get comprehensive, AI-synthesized answers to your questions with citations"],"codeBlocks":[]}
    - {"level":"H2","title":"Modular Output","content":["Access answers through various specialized endpoints for different use\ncases"],"codeBlocks":[]}
    - {"level":"H2","title":"Entity Enrichment","content":["Get detailed information about entities mentioned in summaries"],"codeBlocks":[]}
    - {"level":"H2","title":"Inline Citations","content":["Answers include inline references to source materials"],"codeBlocks":[]}
    - {"level":"H2","title":"Summarizer API Documentation","content":["View the complete API reference, including endpoints, parameters, and example\nrequests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Summarizer Search is perfect for:","• AI Assistants: Build intelligent chat interfaces with web-grounded answers\n• Research Tools: Quickly synthesize information from multiple sources\n• Question Answering: Provide direct answers to user questions\n• Content Summarization: Generate summaries of web content on any topic\n• Knowledge Applications: Create applications that need factual, cited information"],"codeBlocks":[]}
    - {"level":"H2","title":"Available Endpoints","content":["The Summarizer API provides multiple specialized endpoints:","Looking for the OpenAI-compatible endpoint? Check out AI\nGrounding for direct AI answers using the /res/v1/chat/completions endpoint with OpenAI SDK compatibility."],"codeBlocks":["# Main endpoints\nhttps://api.search.brave.com/res/v1/web/search\nhttps://api.search.brave.com/res/v1/summarizer/search\nhttps://api.search.brave.com/res/v1/summarizer/summary\nhttps://api.search.brave.com/res/v1/summarizer/summary_streaming\n\n# Specialized endpoints\nhttps://api.search.brave.com/res/v1/summarizer/title\nhttps://api.search.brave.com/res/v1/summarizer/enrichments\nhttps://api.search.brave.com/res/v1/summarizer/followups\nhttps://api.search.brave.com/res/v1/summarizer/entity_info"]}
    - {"level":"H2","title":"How Summarizer Works","content":["This method gives you full control over the search results and summary generation:","First, make a web search request with the summary=1 parameter:","If the query is eligible for summarization, the response includes a summarizer object with a key:","Treat the key as an opaque string. The format may change in the future, so\nalways pass it as-is without parsing.","Use the key to retrieve the complete summary:","Summarizer requests are not billed - only the initial web search request\ncounts toward your plan limits."],"codeBlocks":["{\n  \"summarizer\": {\n    \"type\": \"summarizer\",\n    \"key\": \"{\\\"query\\\": \\\"what is the second highest mountain\\\", \\\"country\\\": \\\"us\\\", \\\"language\\\": \\\"en\\\", \\\"safesearch\\\": \\\"moderate\\\", \\\"results_hash\\\": \\\"a51e129180225a2f4fe1a00984bcbf58f0ae0625c97723aae43c2c6e3440715b}\"\n  }\n}"]}
    - {"level":"H3","title":"The Traditional Flow (Web Search + Summarizer)","content":["This method gives you full control over the search results and summary generation:","First, make a web search request with the summary=1 parameter:","If the query is eligible for summarization, the response includes a summarizer object with a key:","Treat the key as an opaque string. The format may change in the future, so\nalways pass it as-is without parsing.","Use the key to retrieve the complete summary:","Summarizer requests are not billed - only the initial web search request\ncounts toward your plan limits."],"codeBlocks":["{\n  \"summarizer\": {\n    \"type\": \"summarizer\",\n    \"key\": \"{\\\"query\\\": \\\"what is the second highest mountain\\\", \\\"country\\\": \\\"us\\\", \\\"language\\\": \\\"en\\\", \\\"safesearch\\\": \\\"moderate\\\", \\\"results_hash\\\": \\\"a51e129180225a2f4fe1a00984bcbf58f0ae0625c97723aae43c2c6e3440715b}\"\n  }\n}"]}
    - {"level":"H2","title":"Advanced Features","content":["Get inline citations within the summary text:","Including inline_references=true query parameter will add reference markers throughout the summary text,\nallowing users to see which sources support each statement.","Retrieve detailed information about entities mentioned in the summary:","The response includes descriptions, images, and metadata about key entities."],"codeBlocks":[]}
    - {"level":"H3","title":"Inline References","content":["Get inline citations within the summary text:","Including inline_references=true query parameter will add reference markers throughout the summary text,\nallowing users to see which sources support each statement."],"codeBlocks":[]}
    - {"level":"H3","title":"Entity Information","content":["Retrieve detailed information about entities mentioned in the summary:","The response includes descriptions, images, and metadata about key entities."],"codeBlocks":[]}
    - {"level":"H2","title":"Complete Python Example","content":["Here’s a full example demonstrating the traditional flow:"],"codeBlocks":["import asyncio\nimport json\nfrom urllib.parse import urljoin\nfrom aiohttp import ClientSession, ClientTimeout, TCPConnector\nfrom aiolimiter import AsyncLimiter\n\n# Configuration\nAPI_KEY = \"your_api_key\"\nAPI_HOST = \"https://api.search.brave.com\"\nAPI_RATE_LIMIT = AsyncLimiter(1, 1)\n\nAPI_PATH = {\n    \"web\": urljoin(API_HOST, \"res/v1/web/search\"),\n    \"summarizer_search\": urljoin(API_HOST, \"res/v1/summarizer/search\"),\n}\n\nAPI_HEADERS = {\n    \"web\": {\"X-Subscription-Token\": API_KEY},\n    \"summarizer\": {\"X-Subscription-Token\": API_KEY},\n}\n\nasync def get_summary(session: ClientSession) -> None:\n    # Step 1: Get web search results with summary flag\n    async with session.get(\n        API_PATH[\"web\"],\n        params={\"q\": \"what is the second highest mountain\", \"summary\": 1},\n        headers=API_HEADERS[\"web\"],\n    ) as response:\n        data = await response.json()\n\n        if response.status != 200:\n            print(\"Error fetching web results\")\n            return\n\n    # Step 2: Extract summary key\n    summary_key = data.get(\"summarizer\", {}).get(\"key\")\n\n    if not summary_key:\n        print(\"No summary available for this query\")\n        return\n\n    # Step 3: Fetch the summary\n    async with session.get(\n        url=API_PATH[\"summarizer_search\"],\n        params={\"key\": summary_key, \"entity_info\": 1},\n        headers=API_HEADERS[\"summarizer\"],\n    ) as response:\n        summary_data = await response.json()\n        print(json.dumps(summary_data, indent=2))\n\nasync def main():\n    async with API_RATE_LIMIT:\n        async with ClientSession(\n            connector=TCPConnector(limit=1),\n            timeout=ClientTimeout(20),\n        ) as session:\n            await get_summary(session=session)\n\nasyncio.run(main())"]}
    - {"level":"H2","title":"Response Structure","content":["Summarizer responses include:","• status: Current status (complete or failed)\n• title: A title for the summary\n• summary: The main summary content with text and entities\n• enrichments: Additional data including:Raw text summary Related images Q&A pairs Entity details Source references\n• Raw text summary\n• Related images\n• Q&A pairs\n• Entity details\n• Source references\n• followups: Suggested follow-up queries\n• entities_info: Detailed entity information (when requested)"],"codeBlocks":[]}
    - {"level":"H2","title":"Best Practices","content":["• Summary results are cached for a limited time\n• After cache expiration, restart the flow with a new web search","• Check if summarizer.key exists in web search response\n• Handle failed status in summarizer response\n• Implement retry logic for transient failures","• Only web search requests count toward rate limits\n• Summarizer endpoint calls are free\n• Implement rate limiting on your end to avoid throttling"],"codeBlocks":[]}
    - {"level":"H3","title":"Caching","content":["• Summary results are cached for a limited time\n• After cache expiration, restart the flow with a new web search"],"codeBlocks":[]}
    - {"level":"H3","title":"Error Handling","content":["• Check if summarizer.key exists in web search response\n• Handle failed status in summarizer response\n• Implement retry logic for transient failures"],"codeBlocks":[]}
    - {"level":"H3","title":"Rate Limiting","content":["• Only web search requests count toward rate limits\n• Summarizer endpoint calls are free\n• Implement rate limiting on your end to avoid throttling"],"codeBlocks":[]}
    - {"level":"H2","title":"Specialized Endpoints","content":["The API provides additional endpoints for specific use cases:","• /summarizer/summary: Get just the summary without full search results\n• /summarizer/summary_streaming: Stream the summary in real-time\n• /summarizer/title: Fetch only the summary title\n• /summarizer/enrichments: Get enrichment data separately\n• /summarizer/followups: Retrieve follow-up question suggestions\n• /summarizer/entity_info: Fetch entity information independently","These endpoints all use the same key parameter obtained from the initial web search."],"codeBlocks":[]}
    - {"level":"H2","title":"Summarizer Search vs Answers","content":["Brave offers two complementary approaches for AI-powered search:","Summarizer Search Two-step workflow that first retrieves search results, then generates\nsummaries. Best when you need control over search results or want to use\nspecialized summarizer endpoints.    Answers Direct AI answers using OpenAI-compatible endpoint. Best for building\nchat interfaces and applications that need instant, grounded AI responses.","When to use Summarizer Search:","• Need access to underlying search results\n• Want to use specialized endpoints (title, enrichments, followups, etc.)\n• Building applications with custom search result processing\n• Prefer the traditional web search + summarization flow","When to use Answers:","• Building conversational AI applications\n• Need OpenAI SDK compatibility\n• Want simple, single-endpoint integration\n• Require research mode for thorough answers","Learn more about Answers."],"codeBlocks":[]}
    - {"level":"H2","title":"Summarizer Search","content":["Two-step workflow that first retrieves search results, then generates\nsummaries. Best when you need control over search results or want to use\nspecialized summarizer endpoints."],"codeBlocks":[]}
    - {"level":"H2","title":"Answers","content":["Direct AI answers using OpenAI-compatible endpoint. Best for building\nchat interfaces and applications that need instant, grounded AI responses."],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave Summarizer Search API in chronological order.","• Add inline references to summarizer answers via inline_references=true query parameter\n• Available on /res/v1/summarizer/search and /res/v1/summarizer/summary endpoints","• Launch “AI Answers” resource\n• Replaces previous Summarizer API with enhanced capabilities","• Initial Brave Summarizer Search API release (now deprecated)"],"codeBlocks":[]}
    - {"level":"H3","title":"2025-06-13","content":["• Add inline references to summarizer answers via inline_references=true query parameter\n• Available on /res/v1/summarizer/search and /res/v1/summarizer/summary endpoints"],"codeBlocks":[]}
    - {"level":"H3","title":"2024-04-23","content":["• Launch “AI Answers” resource\n• Replaces previous Summarizer API with enhanced capabilities"],"codeBlocks":[]}
    - {"level":"H3","title":"2023-08-25","content":["• Initial Brave Summarizer Search API release (now deprecated)"],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=what+is+the+second+highest+mountain&summary=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=what+is+the+second+highest+mountain&summary=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"summarizer\": {\n    \"type\": \"summarizer\",\n    \"key\": \"{\\\"query\\\": \\\"what is the second highest mountain\\\", \\\"country\\\": \\\"us\\\", \\\"language\\\": \\\"en\\\", \\\"safesearch\\\": \\\"moderate\\\", \\\"results_hash\\\": \\\"a51e129180225a2f4fe1a00984bcbf58f0ae0625c97723aae43c2c6e3440715b}\"\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"summarizer\": {\n    \"type\": \"summarizer\",\n    \"key\": \"{\\\"query\\\": \\\"what is the second highest mountain\\\", \\\"country\\\": \\\"us\\\", \\\"language\\\": \\\"en\\\", \\\"safesearch\\\": \\\"moderate\\\", \\\"results_hash\\\": \\\"a51e129180225a2f4fe1a00984bcbf58f0ae0625c97723aae43c2c6e3440715b}\"\n  }\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/summarizer/search?key=<URL_ENCODED_KEY>&entity_info=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/summarizer/search?key=<URL_ENCODED_KEY>&entity_info=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/summarizer/search?key=<KEY>&inline_references=true\" \\\n  -H \"Accept: application/json\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/summarizer/search?key=<KEY>&inline_references=true\" \\\n  -H \"Accept: application/json\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/summarizer/search?key=<KEY>&entity_info=1\" \\\n  -H \"Accept: application/json\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/summarizer/search?key=<KEY>&entity_info=1\" \\\n  -H \"Accept: application/json\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nState-of-the-art AI-powered search that generates comprehensive answers and summaries from web search results\n\nSummarizer Search API is deprecated in favor of new and improved Answers API.\n\nOverview\n\nBrave Summarizer Search API leverages advanced AI to provide intelligent summaries and\nanswers based on real-time web search results. Our “AI Answers” feature goes beyond\ntraditional search by understanding your query, gathering relevant information from across\nthe web, and synthesizing it into clear, comprehensive responses with citations.\n\nAccess to Summarizer is available through the discontinued Pro AI plan.\nUsers who are subscribed to the Pro AI plan can continue using the API with the same\nfunctionality and price.\n\nKey Features\n\nAI-Generated Answers\n\nGet comprehensive, AI-synthesized answers to your questions with citations\n\nModular Output\n\nAccess answers through various specialized endpoints for different use\ncases\n\nEntity Enrichment\n\nGet detailed information about entities mentioned in summaries\n\nInline Citations\n\nAnswers include inline references to source materials\n\nAPI Reference\n\nSummarizer API Documentation\n\nView the complete API reference, including endpoints, parameters, and example\nrequests\n\nUse Cases\n\nSummarizer Search is perfect for:\n\nAI Assistants: Build intelligent chat interfaces with web-grounded answers\n\nResearch Tools: Quickly synthesize information from multiple sources\n\nQuestion Answering: Provide direct answers to user questions\n\nContent Summarization: Generate summaries of web content on any topic\n\nKnowledge Applications: Create applications that need factual, cited information\n\nAvailable Endpoints\n\nThe Summarizer API provides multiple specialized endpoints:\n\nLooking for the OpenAI-compatible endpoint? Check out AI\nGrounding for direct AI answers using the /res/v1/chat/completions endpoint with OpenAI SDK compatibility.\n\nHow Summarizer Works\n\nThe Traditional Flow (Web Search + Summarizer)\n\nThis method gives you full control over the search results and summary generation:\n\nStep 1: Web Search with Summary Flag\n\nFirst, make a web search request with the summary=1 parameter:\n\nStep 2: Extract the Summarizer Key\n\nIf the query is eligible for summarization, the response includes a summarizer object with a key:\n\nTreat the key as an opaque string. The format may change in the future, so\nalways pass it as-is without parsing.\n\nStep 3: Fetch the Summary\n\nUse the key to retrieve the complete summary:\n\nSummarizer requests are not billed - only the initial web search request\ncounts toward your plan limits.\n\nAdvanced Features\n\nInline References\n\nGet inline citations within the summary text:\n\nIncluding inline_references=true query parameter will add reference markers throughout the summary text,\nallowing users to see which sources support each statement.\n\nEntity Information\n\nRetrieve detailed information about entities mentioned in the summary:\n\nThe response includes descriptions, images, and metadata about key entities.\n\nComplete Python Example\n\nHere’s a full example demonstrating the traditional flow:\n\nResponse Structure\n\nSummarizer responses include:\n\nstatus: Current status (complete or failed)\n\ntitle: A title for the summary\n\nsummary: The main summary content with text and entities\n\nenrichments: Additional data including:Raw text summary Related images Q&A pairs Entity details Source references\n\nRaw text summary\n\nRelated images\n\nQ&A pairs\n\nEntity details\n\nSource references\n\nfollowups: Suggested follow-up queries\n\nentities_info: Detailed entity information (when requested)\n\nBest Practices\n\nCaching\n\nSummary results are cached for a limited time\n\nAfter cache expiration, restart the flow with a new web search\n\nError Handling\n\nCheck if summarizer.key exists in web search response\n\nHandle failed status in summarizer response\n\nImplement retry logic for transient failures\n\nRate Limiting\n\nOnly web search requests count toward rate limits\n\nSummarizer endpoint calls are free\n\nImplement rate limiting on your end to avoid throttling\n\nSpecialized Endpoints\n\nThe API provides additional endpoints for specific use cases:\n\n/summarizer/summary: Get just the summary without full search results\n\n/summarizer/summary_streaming: Stream the summary in real-time\n\n/summarizer/title: Fetch only the summary title\n\n/summarizer/enrichments: Get enrichment data separately\n\n/summarizer/followups: Retrieve follow-up question suggestions\n\n/summarizer/entity_info: Fetch entity information independently\n\nThese endpoints all use the same key parameter obtained from the initial web search.\n\nSummarizer Search vs Answers\n\nBrave offers two complementary approaches for AI-powered search:\n\nSummarizer Search\n\nTwo-step workflow that first retrieves search results, then generates\nsummaries. Best when you need control over search results or want to use\nspecialized summarizer endpoints.\n\nDirect AI answers using OpenAI-compatible endpoint. Best for building\nchat interfaces and applications that need instant, grounded AI responses.\n\nWhen to use Summarizer Search:\n\nNeed access to underlying search results\n\nWant to use specialized endpoints (title, enrichments, followups, etc.)\n\nBuilding applications with custom search result processing\n\nPrefer the traditional web search + summarization flow\n\nWhen to use Answers:\n\nBuilding conversational AI applications\n\nNeed OpenAI SDK compatibility\n\nWant simple, single-endpoint integration\n\nRequire research mode for thorough answers\n\nLearn more about Answers.\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave Summarizer Search API in chronological order.\n\n2025-06-13\n\nAdd inline references to summarizer answers via inline_references=true query parameter\n\nAvailable on /res/v1/summarizer/search and /res/v1/summarizer/summary endpoints\n\n2024-04-23\n\nLaunch “AI Answers” resource\n\nReplaces previous Summarizer API with enhanced capabilities\n\n2023-08-25\n\nInitial Brave Summarizer Search API release (now deprecated)\n\nOn this page\n\nAI-Generated Answers Get comprehensive, AI-synthesized answers to your questions with citations\n\nModular Output Access answers through various specialized endpoints for different use\ncases\n\nEntity Enrichment Get detailed information about entities mentioned in summaries\n\nInline Citations Answers include inline references to source materials\n\nSummarizer API Documentation View the complete API reference, including endpoints, parameters, and example\nrequests\n\nSummarizer Search Two-step workflow that first retrieves search results, then generates\nsummaries. Best when you need control over search results or want to use\nspecialized summarizer endpoints.\n\nAnswers Direct AI answers using OpenAI-compatible endpoint. Best for building\nchat interfaces and applications that need instant, grounded AI responses."
  suggestedFilename: "services-summarizer"
---

# Summarizer search

## 源URL

https://api-dashboard.search.brave.com/documentation/services/summarizer

## 描述

Brave Summarizer Search API leverages advanced AI to provide intelligent summaries and
answers based on real-time web search results. Our “AI Answers” feature goes beyond
traditional search by understanding your query, gathering relevant information from across
the web, and synthesizing it into clear, comprehensive responses with citations.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search?q=what+is+the+second+highest+mountain&summary=1`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=what+is+the+second+highest+mountain&summary=1" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "summarizer": {
    "type": "summarizer",
    "key": "{\"query\": \"what is the second highest mountain\", \"country\": \"us\", \"language\": \"en\", \"safesearch\": \"moderate\", \"results_hash\": \"a51e129180225a2f4fe1a00984bcbf58f0ae0625c97723aae43c2c6e3440715b}"
  }
}
```

### 示例 3 (bash)

```bash
curl "https://api.search.brave.com/res/v1/summarizer/search?key=<URL_ENCODED_KEY>&entity_info=1" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

## 文档正文

Brave Summarizer Search API leverages advanced AI to provide intelligent summaries and
answers based on real-time web search results. Our “AI Answers” feature goes beyond
traditional search by understanding your query, gathering relevant information from across
the web, and synthesizing it into clear, comprehensive responses with citations.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search?q=what+is+the+second+highest+mountain&summary=1`

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

State-of-the-art AI-powered search that generates comprehensive answers and summaries from web search results

Summarizer Search API is deprecated in favor of new and improved Answers API.

Overview

Brave Summarizer Search API leverages advanced AI to provide intelligent summaries and
answers based on real-time web search results. Our “AI Answers” feature goes beyond
traditional search by understanding your query, gathering relevant information from across
the web, and synthesizing it into clear, comprehensive responses with citations.

Access to Summarizer is available through the discontinued Pro AI plan.
Users who are subscribed to the Pro AI plan can continue using the API with the same
functionality and price.

Key Features

AI-Generated Answers

Get comprehensive, AI-synthesized answers to your questions with citations

Modular Output

Access answers through various specialized endpoints for different use
cases

Entity Enrichment

Get detailed information about entities mentioned in summaries

Inline Citations

Answers include inline references to source materials

API Reference

Summarizer API Documentation

View the complete API reference, including endpoints, parameters, and example
requests

Use Cases

Summarizer Search is perfect for:

AI Assistants: Build intelligent chat interfaces with web-grounded answers

Research Tools: Quickly synthesize information from multiple sources

Question Answering: Provide direct answers to user questions

Content Summarization: Generate summaries of web content on any topic

Knowledge Applications: Create applications that need factual, cited information

Available Endpoints

The Summarizer API provides multiple specialized endpoints:

Looking for the OpenAI-compatible endpoint? Check out AI
Grounding for direct AI answers using the /res/v1/chat/completions endpoint with OpenAI SDK compatibility.

How Summarizer Works

The Traditional Flow (Web Search + Summarizer)

This method gives you full control over the search results and summary generation:

Step 1: Web Search with Summary Flag

First, make a web search request with the summary=1 parameter:

Step 2: Extract the Summarizer Key

If the query is eligible for summarization, the response includes a summarizer object with a key:

Treat the key as an opaque string. The format may change in the future, so
always pass it as-is without parsing.

Step 3: Fetch the Summary

Use the key to retrieve the complete summary:

Summarizer requests are not billed - only the initial web search request
counts toward your plan limits.

Advanced Features

Inline References

Get inline citations within the summary text:

Including inline_references=true query parameter will add reference markers throughout the summary text,
allowing users to see which sources support each statement.

Entity Information

Retrieve detailed information about entities mentioned in the summary:

The response includes descriptions, images, and metadata about key entities.

Complete Python Example

Here’s a full example demonstrating the traditional flow:

Response Structure

Summarizer responses include:

status: Current status (complete or failed)

title: A title for the summary

summary: The main summary content with text and entities

enrichments: Additional data including:Raw text summary Related images Q&A pairs Entity details Source references

Raw text summary

Related images

Q&A pairs

Entity details

Source references

followups: Suggested follow-up queries

entities_info: Detailed entity information (when requested)

Best Practices

Caching

Summary results are cached for a limited time

After cache expiration, restart the flow with a new web search

Error Handling

Check if summarizer.key exists in web search response

Handle failed status in summarizer response

Implement retry logic for transient failures

Rate Limiting

Only web search requests count toward rate limits

Summarizer endpoint calls are free

Implement rate limiting on your end to avoid throttling

Specialized Endpoints

The API provides additional endpoints for specific use cases:

/summarizer/summary: Get just the summary without full search results

/summarizer/summary_streaming: Stream the summary in real-time

/summarizer/title: Fetch only the summary title

/summarizer/enrichments: Get enrichment data separately

/summarizer/followups: Retrieve follow-up question suggestions

/summarizer/entity_info: Fetch entity information independently

These endpoints all use the same key parameter obtained from the initial web search.

Summarizer Search vs Answers

Brave offers two complementary approaches for AI-powered search:

Summarizer Search

Two-ste
