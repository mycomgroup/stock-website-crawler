---
id: "url-6d5806d4"
type: "api"
title: "News search"
url: "https://api-dashboard.search.brave.com/documentation/services/news-search"
description: "News Search lets you send queries and receive relevant news from a specialized index\nof articles sourced from trusted outlets worldwide. With continuous crawling and indexing,\nyou get access to breaking news, historical articles, and comprehensive coverage for your\napplications."
source: ""
tags: []
crawl_time: "2026-03-18T02:33:25.771Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/news/search?q=climate+summit&freshness=pw"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["News Search lets you send queries and receive relevant news from a specialized index\nof articles sourced from trusted outlets worldwide. With continuous crawling and indexing,\nyou get access to breaking news, historical articles, and comprehensive coverage for your\napplications."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["News-Specific Index Search across a curated index of news articles from reputable news outlets\nworldwide   Freshness Filtering Filter results by discovery date - from last 24 hours to custom date ranges   Country & Language Options Target news from specific countries and in preferred languages   Extra Snippets Get up to 5 additional alternative excerpts per result"],"codeBlocks":[]}
    - {"level":"H2","title":"News-Specific Index","content":["Search across a curated index of news articles from reputable news outlets\nworldwide"],"codeBlocks":[]}
    - {"level":"H2","title":"Freshness Filtering","content":["Filter results by discovery date - from last 24 hours to custom date ranges"],"codeBlocks":[]}
    - {"level":"H2","title":"Country & Language Options","content":["Target news from specific countries and in preferred languages"],"codeBlocks":[]}
    - {"level":"H2","title":"Extra Snippets","content":["Get up to 5 additional alternative excerpts per result"],"codeBlocks":[]}
    - {"level":"H2","title":"News Search API Documentation","content":["View the complete API reference, including endpoints, parameters, and example\nrequests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["News Search is perfect for:","• News Aggregation: Build news applications and aggregators with real-time content\n• Media Monitoring: Track news mentions, brand coverage, and industry trends\n• Current Events Analysis: Monitor breaking news and emerging stories\n• Content Discovery: Find news articles for research and content curation\n• Historical News Research: Access archived news articles with date filtering"],"codeBlocks":[]}
    - {"level":"H2","title":"Freshness Filtering","content":["News Search offers powerful date-based filtering to help you find the most relevant content:","• Last 24 Hours (pd): Get breaking news and latest updates\n• Last 7 Days (pw): Track weekly news trends\n• Last 31 Days (pm): Monitor monthly developments\n• Last Year (py): Search annual news coverage\n• Custom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)","Example request filtering for news from the past week:"],"codeBlocks":[]}
    - {"level":"H2","title":"Country and Language Targeting","content":["Customize your news search results by specifying:","• Country: Target news from specific countries using 2-character country codes\n• Search Language: Filter results by content language\n• UI Language: Set the preferred language for response metadata","Example request for French news from France:"],"codeBlocks":[]}
    - {"level":"H2","title":"Extra Snippets","content":["The extra snippets feature provides up to 5 additional excerpts per search result, giving you more context and alternative perspectives from each article. This is particularly useful for:","• Comprehensive content preview\n• Better relevance assessment\n• Enhanced user experience in news applications","To enable extra snippets:"],"codeBlocks":[]}
    - {"level":"H2","title":"Goggles Support","content":["News Search supports Goggles, which allow you to apply custom re-ranking on top of search results. You can:","• Boost or demote specific news sources\n• Filter by custom criteria\n• Create personalized news ranking algorithms","Goggles can be provided as a URL or inline definition, and multiple goggles can be combined."],"codeBlocks":[]}
    - {"level":"H2","title":"Search Operators","content":["News Search supports search operators to refine your queries:","• Use quotes for exact phrase matching: \"climate change\"\n• Exclude terms with minus: technology -cryptocurrency\n• Site-specific searches: site:reuters.com elections"],"codeBlocks":[]}
    - {"level":"H2","title":"Pagination","content":["Efficiently paginate through news results:","• count: Number of results per page (max 50, default 20)\n• offset: Page number to retrieve (0-based, max 9)","Example request for page 2 with 20 results per page:"],"codeBlocks":[]}
    - {"level":"H2","title":"Safe Search","content":["Control adult content filtering with the safesearch parameter:","• off: No filtering\n• moderate: Filter explicit content\n• strict: Filter explicit and suggestive content (default)"],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave News Search API in chronological order.","• 2023-08-15 Add Brave News Search API resource.\n• 2024-03-20 Add freshness filtering with custom date ranges.\n• 2024-09-10 Add extra snippets feature for AI and Data plans.\n• 2025-01-15 Add Goggles support for custom re-ranking."],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=climate+summit&freshness=pw\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=climate+summit&freshness=pw\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=élections&country=FR&search_lang=fr\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=élections&country=FR&search_lang=fr\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=artificial+intelligence&extra_snippets=true\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=artificial+intelligence&extra_snippets=true\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=sports&count=20&offset=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=sports&count=20&offset=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nDedicated search for news, with advanced filtering and freshness options\n\nOverview\n\nNews Search lets you send queries and receive relevant news from a specialized index\nof articles sourced from trusted outlets worldwide. With continuous crawling and indexing,\nyou get access to breaking news, historical articles, and comprehensive coverage for your\napplications.\n\nKey Features\n\nNews-Specific Index\n\nSearch across a curated index of news articles from reputable news outlets\nworldwide\n\nFreshness Filtering\n\nFilter results by discovery date - from last 24 hours to custom date ranges\n\nCountry & Language Options\n\nTarget news from specific countries and in preferred languages\n\nExtra Snippets\n\nGet up to 5 additional alternative excerpts per result\n\nAPI Reference\n\nNews Search API Documentation\n\nView the complete API reference, including endpoints, parameters, and example\nrequests\n\nUse Cases\n\nNews Search is perfect for:\n\nNews Aggregation: Build news applications and aggregators with real-time content\n\nMedia Monitoring: Track news mentions, brand coverage, and industry trends\n\nCurrent Events Analysis: Monitor breaking news and emerging stories\n\nContent Discovery: Find news articles for research and content curation\n\nHistorical News Research: Access archived news articles with date filtering\n\nNews Search offers powerful date-based filtering to help you find the most relevant content:\n\nLast 24 Hours (pd): Get breaking news and latest updates\n\nLast 7 Days (pw): Track weekly news trends\n\nLast 31 Days (pm): Monitor monthly developments\n\nLast Year (py): Search annual news coverage\n\nCustom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)\n\nExample request filtering for news from the past week:\n\nCountry and Language Targeting\n\nCustomize your news search results by specifying:\n\nCountry: Target news from specific countries using 2-character country codes\n\nSearch Language: Filter results by content language\n\nUI Language: Set the preferred language for response metadata\n\nExample request for French news from France:\n\nThe extra snippets feature provides up to 5 additional excerpts per search result, giving you more context and alternative perspectives from each article. This is particularly useful for:\n\nComprehensive content preview\n\nBetter relevance assessment\n\nEnhanced user experience in news applications\n\nTo enable extra snippets:\n\nGoggles Support\n\nNews Search supports Goggles, which allow you to apply custom re-ranking on top of search results. You can:\n\nBoost or demote specific news sources\n\nFilter by custom criteria\n\nCreate personalized news ranking algorithms\n\nGoggles can be provided as a URL or inline definition, and multiple goggles can be combined.\n\nSearch Operators\n\nNews Search supports search operators to refine your queries:\n\nUse quotes for exact phrase matching: \"climate change\"\n\nExclude terms with minus: technology -cryptocurrency\n\nSite-specific searches: site:reuters.com elections\n\nPagination\n\nEfficiently paginate through news results:\n\ncount: Number of results per page (max 50, default 20)\n\noffset: Page number to retrieve (0-based, max 9)\n\nExample request for page 2 with 20 results per page:\n\nSafe Search\n\nControl adult content filtering with the safesearch parameter:\n\noff: No filtering\n\nmoderate: Filter explicit content\n\nstrict: Filter explicit and suggestive content (default)\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave News Search API in chronological order.\n\n2023-08-15 Add Brave News Search API resource.\n\n2024-03-20 Add freshness filtering with custom date ranges.\n\n2024-09-10 Add extra snippets feature for AI and Data plans.\n\n2025-01-15 Add Goggles support for custom re-ranking.\n\nOn this page\n\nNews-Specific Index Search across a curated index of news articles from reputable news outlets\nworldwide\n\nFreshness Filtering Filter results by discovery date - from last 24 hours to custom date ranges\n\nCountry & Language Options Target news from specific countries and in preferred languages\n\nExtra Snippets Get up to 5 additional alternative excerpts per result\n\nNews Search API Documentation View the complete API reference, including endpoints, parameters, and example\nrequests"
  suggestedFilename: "services-news-search"
---

# News search

## 源URL

https://api-dashboard.search.brave.com/documentation/services/news-search

## 描述

News Search lets you send queries and receive relevant news from a specialized index
of articles sourced from trusted outlets worldwide. With continuous crawling and indexing,
you get access to breaking news, historical articles, and comprehensive coverage for your
applications.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/news/search?q=climate+summit&freshness=pw`

## 代码示例

```bash
curl "https://api.search.brave.com/res/v1/news/search?q=climate+summit&freshness=pw" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

## 文档正文

News Search lets you send queries and receive relevant news from a specialized index
of articles sourced from trusted outlets worldwide. With continuous crawling and indexing,
you get access to breaking news, historical articles, and comprehensive coverage for your
applications.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/news/search?q=climate+summit&freshness=pw`

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

Dedicated search for news, with advanced filtering and freshness options

Overview

News Search lets you send queries and receive relevant news from a specialized index
of articles sourced from trusted outlets worldwide. With continuous crawling and indexing,
you get access to breaking news, historical articles, and comprehensive coverage for your
applications.

Key Features

News-Specific Index

Search across a curated index of news articles from reputable news outlets
worldwide

Freshness Filtering

Filter results by discovery date - from last 24 hours to custom date ranges

Country & Language Options

Target news from specific countries and in preferred languages

Extra Snippets

Get up to 5 additional alternative excerpts per result

API Reference

News Search API Documentation

View the complete API reference, including endpoints, parameters, and example
requests

Use Cases

News Search is perfect for:

News Aggregation: Build news applications and aggregators with real-time content

Media Monitoring: Track news mentions, brand coverage, and industry trends

Current Events Analysis: Monitor breaking news and emerging stories

Content Discovery: Find news articles for research and content curation

Historical News Research: Access archived news articles with date filtering

News Search offers powerful date-based filtering to help you find the most relevant content:

Last 24 Hours (pd): Get breaking news and latest updates

Last 7 Days (pw): Track weekly news trends

Last 31 Days (pm): Monitor monthly developments

Last Year (py): Search annual news coverage

Custom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)

Example request filtering for news from the past week:

Country and Language Targeting

Customize your news search results by specifying:

Country: Target news from specific countries using 2-character country codes

Search Language: Filter results by content language

UI Language: Set the preferred language for response metadata

Example request for French news from France:

The extra snippets feature provides up to 5 additional excerpts per search result, giving you more context and alternative perspectives from each article. This is particularly useful for:

Comprehensive content preview

Better relevance assessment

Enhanced user experience in news applications

To enable extra snippets:

Goggles Support

News Search supports Goggles, which allow you to apply custom re-ranking on top of search results. You can:

Boost or demote specific news sources

Filter by custom criteria

Create personalized news ranking algorithms

Goggles can be provided as a URL or inline definition, and multiple goggles can be combined.

Search Operators

News Search supports search operators to refine your queries:

Use quotes for exact phrase matching: "climate change"

Exclude terms with minus: technology -cryptocurrency

Site-specific searches: site:reuters.com elections

Pagination

Efficiently paginate through news results:

count: Number of results per page (max 50, default 20)

offset: Page number to retrieve (0-based, max 9)

Example request for page 2 with 20 results per page:

Safe Search

Control adult content filtering with the safesearch parameter:

off: No filtering

moderate: Filter explicit content

strict: Filter explicit and suggestive content (default)

Changelog

This changelog outlines all significant changes to the Brave News Search API in chronological order.

2023-08-15 Add Brave News Search API resource.

2024-03-20 Add freshness filtering with custom date ranges.

2024-09-10 Add extra snippets feature for AI and Data plans.

2025-01-15 Add Goggles support for custom re-ranking.

On this page

News-Specific Index Search across a curated index of news articles from reputable news outlets
worldwide

Freshness Filtering Filter results by discovery date - from last 24 hours to custom date ranges

Country & Language Options Target news from specific countries and in preferred languages

Extra Snippets Get up to 5 additional alternative excerpts per result

News Search API Documentation View the complete API reference, including endpoints, parameters, and example
requests
