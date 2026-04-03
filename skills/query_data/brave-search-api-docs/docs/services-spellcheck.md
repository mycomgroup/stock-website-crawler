---
id: "url-36b45456"
type: "api"
title: "Spellcheck"
url: "https://api-dashboard.search.brave.com/documentation/services/spellcheck"
description: "Brave Search Spellcheck API provides advanced spell checking capabilities for\nsearch queries. It analyzes queries to detect spelling errors and suggests corrected\nalternatives, helping users get better search results even when they make typos or\nspelling mistakes."
source: ""
tags: []
crawl_time: "2026-03-18T02:33:03.913Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/spellcheck/search?q=helo&country=US"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Brave Search Spellcheck API provides advanced spell checking capabilities for\nsearch queries. It analyzes queries to detect spelling errors and suggests corrected\nalternatives, helping users get better search results even when they make typos or\nspelling mistakes."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Query Correction Automatically detect and correct spelling errors in search queries   Contextual Suggestions Intelligent corrections based on query context and search patterns   Fast Response Low-latency spell checking for real-time query processing   Language Support Multi-language spell checking with country-specific corrections"],"codeBlocks":[]}
    - {"level":"H2","title":"Query Correction","content":["Automatically detect and correct spelling errors in search queries"],"codeBlocks":[]}
    - {"level":"H2","title":"Contextual Suggestions","content":["Intelligent corrections based on query context and search patterns"],"codeBlocks":[]}
    - {"level":"H2","title":"Fast Response","content":["Low-latency spell checking for real-time query processing"],"codeBlocks":[]}
    - {"level":"H2","title":"Language Support","content":["Multi-language spell checking with country-specific corrections"],"codeBlocks":[]}
    - {"level":"H2","title":"Spellcheck API Documentation","content":["View the complete API reference, including endpoints, parameters, and example\nrequests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Spellcheck API is perfect for:","• Search Applications: Improve user experience by correcting typos before searching\n• Query Suggestions: Offer spelling corrections in search interfaces\n• Data Quality: Clean and normalize user-generated queries\n• Autocorrect: Implement “Did you mean?” functionality\n• Query Analysis: Identify and track common misspellings"],"codeBlocks":[]}
    - {"level":"H2","title":"Endpoint","content":["Brave Spellcheck API is available at the following endpoint:"],"codeBlocks":["https://api.search.brave.com/res/v1/spellcheck/search"]}
    - {"level":"H2","title":"Getting Started","content":["Get started immediately with a simple cURL request:"],"codeBlocks":["curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=helo&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"","{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"helo\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello\"\n    }\n  ]\n}"]}
    - {"level":"H3","title":"Example Response","content":[],"codeBlocks":["{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"helo\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello\"\n    }\n  ]\n}"]}
    - {"level":"H2","title":"Common Examples","content":["When the query is already spelled correctly:","The API handles corrections in multi-word queries:"],"codeBlocks":["curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=hello&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"","{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": []\n}","curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=articifial+inteligence&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"","{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"articifial inteligence\"\n  },\n  \"results\": [\n    {\n      \"query\": \"artificial intelligence\"\n    }\n  ]\n}"]}
    - {"level":"H3","title":"No Correction Needed","content":["When the query is already spelled correctly:"],"codeBlocks":["curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=hello&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"","{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": []\n}"]}
    - {"level":"H3","title":"Multi-word Correction","content":["The API handles corrections in multi-word queries:"],"codeBlocks":["curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=articifial+inteligence&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"","{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"articifial inteligence\"\n  },\n  \"results\": [\n    {\n      \"query\": \"artificial intelligence\"\n    }\n  ]\n}"]}
    - {"level":"H2","title":"Best Practices","content":["• Show Suggestions Gracefully: Display “Did you mean?” suggestions without forcing corrections\n• Preserve User Intent: Allow users to search for their original query if desired\n• Highlight Differences: Visually indicate which parts of the query were corrected","• Debounce Requests: Implement debouncing (e.g., 200-300ms) to avoid excessive API calls\n• Cache Results: Cache spell check results for frequently typed queries\n• Async Loading: Check spelling asynchronously without blocking user input","• Implement client-side throttling to avoid hitting API rate limits\n• Consider combining spell check with other search operations\n• Monitor your API usage and adjust debounce timings accordingly"],"codeBlocks":["// Debounced spell check implementation\nfunction debounce(func, wait) {\n  let timeout;\n  return function executedFunction(...args) {\n    const later = () => {\n      clearTimeout(timeout);\n      func(...args);\n    };\n    clearTimeout(timeout);\n    timeout = setTimeout(later, wait);\n  };\n}\n\nconst debouncedSpellcheck = debounce(async (query) => {\n  const result = await checkSpelling(query);\n  if (result.results.length > 0) {\n    // Show correction suggestion\n    showSuggestion(result.results[0].query);\n  }\n}, 300);\n\n// Call on input change\ninputElement.addEventListener(\"input\", (e) => {\n  debouncedSpellcheck(e.target.value);\n});"]}
    - {"level":"H3","title":"User Experience","content":["• Show Suggestions Gracefully: Display “Did you mean?” suggestions without forcing corrections\n• Preserve User Intent: Allow users to search for their original query if desired\n• Highlight Differences: Visually indicate which parts of the query were corrected"],"codeBlocks":[]}
    - {"level":"H3","title":"Performance Optimization","content":["• Debounce Requests: Implement debouncing (e.g., 200-300ms) to avoid excessive API calls\n• Cache Results: Cache spell check results for frequently typed queries\n• Async Loading: Check spelling asynchronously without blocking user input"],"codeBlocks":[]}
    - {"level":"H3","title":"Integration Patterns","content":[],"codeBlocks":["// Debounced spell check implementation\nfunction debounce(func, wait) {\n  let timeout;\n  return function executedFunction(...args) {\n    const later = () => {\n      clearTimeout(timeout);\n      func(...args);\n    };\n    clearTimeout(timeout);\n    timeout = setTimeout(later, wait);\n  };\n}\n\nconst debouncedSpellcheck = debounce(async (query) => {\n  const result = await checkSpelling(query);\n  if (result.results.length > 0) {\n    // Show correction suggestion\n    showSuggestion(result.results[0].query);\n  }\n}, 300);\n\n// Call on input change\ninputElement.addEventListener(\"input\", (e) => {\n  debouncedSpellcheck(e.target.value);\n});"]}
    - {"level":"H3","title":"Rate Limiting","content":["• Implement client-side throttling to avoid hitting API rate limits\n• Consider combining spell check with other search operations\n• Monitor your API usage and adjust debounce timings accordingly"],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave Search Spellcheck API in chronological order.","• 2023-05-01 Initial launch of Brave Search Spellcheck API"],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=helo&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=helo&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"helo\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello\"\n    }\n  ]\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"helo\"\n  },\n  \"results\": [\n    {\n      \"query\": \"hello\"\n    }\n  ]\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=hello&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=hello&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": []\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"hello\"\n  },\n  \"results\": []\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=articifial+inteligence&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/spellcheck/search?q=articifial+inteligence&country=US\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"articifial inteligence\"\n  },\n  \"results\": [\n    {\n      \"query\": \"artificial intelligence\"\n    }\n  ]\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"spellcheck\",\n  \"query\": {\n    \"original\": \"articifial inteligence\"\n  },\n  \"results\": [\n    {\n      \"query\": \"artificial intelligence\"\n    }\n  ]\n}"}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nIntelligent spellchecking to improve query quality and help users find what they're looking for\n\nOverview\n\nBrave Search Spellcheck API provides advanced spell checking capabilities for\nsearch queries. It analyzes queries to detect spelling errors and suggests corrected\nalternatives, helping users get better search results even when they make typos or\nspelling mistakes.\n\nKey Features\n\nQuery Correction\n\nAutomatically detect and correct spelling errors in search queries\n\nContextual Suggestions\n\nIntelligent corrections based on query context and search patterns\n\nFast Response\n\nLow-latency spell checking for real-time query processing\n\nLanguage Support\n\nMulti-language spell checking with country-specific corrections\n\nAPI Reference\n\nSpellcheck API Documentation\n\nView the complete API reference, including endpoints, parameters, and example\nrequests\n\nUse Cases\n\nSpellcheck API is perfect for:\n\nSearch Applications: Improve user experience by correcting typos before searching\n\nQuery Suggestions: Offer spelling corrections in search interfaces\n\nData Quality: Clean and normalize user-generated queries\n\nAutocorrect: Implement “Did you mean?” functionality\n\nQuery Analysis: Identify and track common misspellings\n\nEndpoint\n\nBrave Spellcheck API is available at the following endpoint:\n\nGetting Started\n\nGet started immediately with a simple cURL request:\n\nExample Response\n\nCommon Examples\n\nNo Correction Needed\n\nWhen the query is already spelled correctly:\n\nResponse:\n\nMulti-word Correction\n\nThe API handles corrections in multi-word queries:\n\nIntegration Examples\n\nNode.js\n\nPython\n\nBest Practices\n\nUser Experience\n\nShow Suggestions Gracefully: Display “Did you mean?” suggestions without forcing corrections\n\nPreserve User Intent: Allow users to search for their original query if desired\n\nHighlight Differences: Visually indicate which parts of the query were corrected\n\nPerformance Optimization\n\nDebounce Requests: Implement debouncing (e.g., 200-300ms) to avoid excessive API calls\n\nCache Results: Cache spell check results for frequently typed queries\n\nAsync Loading: Check spelling asynchronously without blocking user input\n\nIntegration Patterns\n\nRate Limiting\n\nImplement client-side throttling to avoid hitting API rate limits\n\nConsider combining spell check with other search operations\n\nMonitor your API usage and adjust debounce timings accordingly\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave Search Spellcheck API in chronological order.\n\n2023-05-01 Initial launch of Brave Search Spellcheck API\n\nOn this page\n\nQuery Correction Automatically detect and correct spelling errors in search queries\n\nContextual Suggestions Intelligent corrections based on query context and search patterns\n\nFast Response Low-latency spell checking for real-time query processing\n\nLanguage Support Multi-language spell checking with country-specific corrections\n\nSpellcheck API Documentation View the complete API reference, including endpoints, parameters, and example\nrequests"
  suggestedFilename: "services-spellcheck"
---

# Spellcheck

## 源URL

https://api-dashboard.search.brave.com/documentation/services/spellcheck

## 描述

Brave Search Spellcheck API provides advanced spell checking capabilities for
search queries. It analyzes queries to detect spelling errors and suggests corrected
alternatives, helping users get better search results even when they make typos or
spelling mistakes.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/spellcheck/search?q=helo&country=US`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/spellcheck/search?q=helo&country=US" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "spellcheck",
  "query": {
    "original": "helo"
  },
  "results": [
    {
      "query": "hello"
    }
  ]
}
```

## 文档正文

Brave Search Spellcheck API provides advanced spell checking capabilities for
search queries. It analyzes queries to detect spelling errors and suggests corrected
alternatives, helping users get better search results even when they make typos or
spelling mistakes.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/spellcheck/search?q=helo&country=US`

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

Intelligent spellchecking to improve query quality and help users find what they're looking for

Overview

Brave Search Spellcheck API provides advanced spell checking capabilities for
search queries. It analyzes queries to detect spelling errors and suggests corrected
alternatives, helping users get better search results even when they make typos or
spelling mistakes.

Key Features

Query Correction

Automatically detect and correct spelling errors in search queries

Contextual Suggestions

Intelligent corrections based on query context and search patterns

Fast Response

Low-latency spell checking for real-time query processing

Language Support

Multi-language spell checking with country-specific corrections

API Reference

Spellcheck API Documentation

View the complete API reference, including endpoints, parameters, and example
requests

Use Cases

Spellcheck API is perfect for:

Search Applications: Improve user experience by correcting typos before searching

Query Suggestions: Offer spelling corrections in search interfaces

Data Quality: Clean and normalize user-generated queries

Autocorrect: Implement “Did you mean?” functionality

Query Analysis: Identify and track common misspellings

Endpoint

Brave Spellcheck API is available at the following endpoint:

Getting Started

Get started immediately with a simple cURL request:

Example Response

Common Examples

No Correction Needed

When the query is already spelled correctly:

Response:

Multi-word Correction

The API handles corrections in multi-word queries:

Integration Examples

Node.js

Python

Best Practices

User Experience

Show Suggestions Gracefully: Display “Did you mean?” suggestions without forcing corrections

Preserve User Intent: Allow users to search for their original query if desired

Highlight Differences: Visually indicate which parts of the query were corrected

Performance Optimization

Debounce Requests: Implement debouncing (e.g., 200-300ms) to avoid excessive API calls

Cache Results: Cache spell check results for frequently typed queries

Async Loading: Check spelling asynchronously without blocking user input

Integration Patterns

Rate Limiting

Implement client-side throttling to avoid hitting API rate limits

Consider combining spell check with other search operations

Monitor your API usage and adjust debounce timings accordingly

Changelog

This changelog outlines all significant changes to the Brave Search Spellcheck API in chronological order.

2023-05-01 Initial launch of Brave Search Spellcheck API

On this page

Query Correction Automatically detect and correct spelling errors in search queries

Contextual Suggestions Intelligent corrections based on query context and search patterns

Fast Response Low-latency spell checking for real-time query processing

Language Support Multi-language spell checking with country-specific corrections

Spellcheck API Documentation View the complete API reference, including endpoints, parameters, and example
requests
