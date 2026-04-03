---
id: "url-7f73bd30"
type: "api"
title: "Video search"
url: "https://api-dashboard.search.brave.com/documentation/services/video-search"
description: "Video Search lets you send queries and receive relevant video results from a\ndedicated index spanning various platforms and sources across the web. With\ncontinuous indexing, your applications can retrieve tutorials, entertainment,\nnews clips, and more—all through a simple search."
source: ""
tags: []
crawl_time: "2026-03-18T03:28:07.719Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial&freshness=pw"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Video Search lets you send queries and receive relevant video results from a\ndedicated index spanning various platforms and sources across the web. With\ncontinuous indexing, your applications can retrieve tutorials, entertainment,\nnews clips, and more—all through a simple search."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Video-Specific Index Search across a curated index of video content from multiple platforms and\nsources   Freshness Filtering Filter results by discovery date - from last 24 hours to custom date ranges   Country & Language Options Target videos from specific countries and in preferred languages   Safe Search Filtering Control adult content filtering with flexible options"],"codeBlocks":[]}
    - {"level":"H2","title":"Video-Specific Index","content":["Search across a curated index of video content from multiple platforms and\nsources"],"codeBlocks":[]}
    - {"level":"H2","title":"Freshness Filtering","content":["Filter results by discovery date - from last 24 hours to custom date ranges"],"codeBlocks":[]}
    - {"level":"H2","title":"Country & Language Options","content":["Target videos from specific countries and in preferred languages"],"codeBlocks":[]}
    - {"level":"H2","title":"Safe Search Filtering","content":["Control adult content filtering with flexible options"],"codeBlocks":[]}
    - {"level":"H2","title":"Video Search API Documentation","content":["View the complete API reference, including endpoints, parameters, and example\nrequests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Video Search is perfect for:","• Video Platforms: Build video discovery and recommendation features\n• Educational Applications: Find tutorials, lectures, and instructional content\n• Content Aggregation: Gather video content from across the web\n• Entertainment Apps: Discover movies, shows, and entertainment content\n• Media Monitoring: Track video mentions and brand coverage across platforms"],"codeBlocks":[]}
    - {"level":"H2","title":"Freshness Filtering","content":["Video Search offers powerful date-based filtering to help you find the most relevant content:","• Last 24 Hours (pd): Get the latest uploaded videos\n• Last 7 Days (pw): Track weekly video content\n• Last 31 Days (pm): Monitor monthly uploads\n• Last Year (py): Search annual video coverage\n• Custom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)","Example request filtering for videos from the past week:"],"codeBlocks":[]}
    - {"level":"H2","title":"Country and Language Targeting","content":["Customize your video search results by specifying:","• Country: Target videos from specific countries using 2-character country codes\n• Search Language: Filter results by content language\n• UI Language: Set the preferred language for response metadata","Example request for Spanish videos from Spain:"],"codeBlocks":[]}
    - {"level":"H2","title":"Search Operators","content":["Video Search supports search operators to refine your queries:","• Use quotes for exact phrase matching: \"python programming\"\n• Exclude terms with minus: cooking -vegan\n• Site-specific searches: site:youtube.com fitness workout"],"codeBlocks":[]}
    - {"level":"H2","title":"Pagination","content":["Efficiently paginate through video results:","• count: Number of results per page (max 50, default 20)\n• offset: Page number to retrieve (0-based, max 9)","Example request for page 2 with 20 results per page:"],"codeBlocks":[]}
    - {"level":"H2","title":"Safe Search","content":["Control adult content filtering with the safesearch parameter:","• off: No filtering\n• moderate: Filter explicit content (default)\n• strict: Filter explicit and suggestive content","This is particularly important for applications targeting family-friendly or educational audiences."],"codeBlocks":[]}
    - {"level":"H2","title":"Spellcheck","content":["Video Search includes automatic spellcheck functionality to improve search accuracy:","• Enabled by default\n• Automatically corrects common misspellings\n• The modified query is used for search and available in the response","To disable spellcheck:"],"codeBlocks":[]}
    - {"level":"H2","title":"Example: Complete Search Request","content":["Here’s a comprehensive example combining multiple parameters:","This request:","• Searches for “photography tips”\n• Targets US content\n• Returns English language results\n• Retrieves 25 results\n• Filters to videos from the past month\n• Applies strict safe search filtering"],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave Video Search API in chronological order.","• 2023-06-20 Add Brave Video Search API resource.\n• 2024-02-15 Add freshness filtering with custom date ranges.\n• 2024-11-05 Improve search operators support."],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial&freshness=pw\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial&freshness=pw\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=recetas+de+cocina&country=ES&search_lang=es\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=recetas+de+cocina&country=ES&search_lang=es\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=travel+vlog&count=20&offset=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=travel+vlog&count=20&offset=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=tutorial&spellcheck=false\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=tutorial&spellcheck=false\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=photography+tips&country=US&search_lang=en&count=25&freshness=pm&safesearch=strict\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/videos/search?q=photography+tips&country=US&search_lang=en&count=25&freshness=pm&safesearch=strict\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nDedicated search for videos, with advanced filtering and freshness options\n\nOverview\n\nVideo Search lets you send queries and receive relevant video results from a\ndedicated index spanning various platforms and sources across the web. With\ncontinuous indexing, your applications can retrieve tutorials, entertainment,\nnews clips, and more—all through a simple search.\n\nKey Features\n\nVideo-Specific Index\n\nSearch across a curated index of video content from multiple platforms and\nsources\n\nFreshness Filtering\n\nFilter results by discovery date - from last 24 hours to custom date ranges\n\nCountry & Language Options\n\nTarget videos from specific countries and in preferred languages\n\nSafe Search Filtering\n\nControl adult content filtering with flexible options\n\nAPI Reference\n\nVideo Search API Documentation\n\nView the complete API reference, including endpoints, parameters, and example\nrequests\n\nUse Cases\n\nVideo Search is perfect for:\n\nVideo Platforms: Build video discovery and recommendation features\n\nEducational Applications: Find tutorials, lectures, and instructional content\n\nContent Aggregation: Gather video content from across the web\n\nEntertainment Apps: Discover movies, shows, and entertainment content\n\nMedia Monitoring: Track video mentions and brand coverage across platforms\n\nVideo Search offers powerful date-based filtering to help you find the most relevant content:\n\nLast 24 Hours (pd): Get the latest uploaded videos\n\nLast 7 Days (pw): Track weekly video content\n\nLast 31 Days (pm): Monitor monthly uploads\n\nLast Year (py): Search annual video coverage\n\nCustom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)\n\nExample request filtering for videos from the past week:\n\nCountry and Language Targeting\n\nCustomize your video search results by specifying:\n\nCountry: Target videos from specific countries using 2-character country codes\n\nSearch Language: Filter results by content language\n\nUI Language: Set the preferred language for response metadata\n\nExample request for Spanish videos from Spain:\n\nSearch Operators\n\nVideo Search supports search operators to refine your queries:\n\nUse quotes for exact phrase matching: \"python programming\"\n\nExclude terms with minus: cooking -vegan\n\nSite-specific searches: site:youtube.com fitness workout\n\nPagination\n\nEfficiently paginate through video results:\n\ncount: Number of results per page (max 50, default 20)\n\noffset: Page number to retrieve (0-based, max 9)\n\nExample request for page 2 with 20 results per page:\n\nSafe Search\n\nControl adult content filtering with the safesearch parameter:\n\noff: No filtering\n\nmoderate: Filter explicit content (default)\n\nstrict: Filter explicit and suggestive content\n\nThis is particularly important for applications targeting family-friendly or educational audiences.\n\nVideo Search includes automatic spellcheck functionality to improve search accuracy:\n\nEnabled by default\n\nAutomatically corrects common misspellings\n\nThe modified query is used for search and available in the response\n\nTo disable spellcheck:\n\nExample: Complete Search Request\n\nHere’s a comprehensive example combining multiple parameters:\n\nThis request:\n\nSearches for “photography tips”\n\nTargets US content\n\nReturns English language results\n\nRetrieves 25 results\n\nFilters to videos from the past month\n\nApplies strict safe search filtering\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave Video Search API in chronological order.\n\n2023-06-20 Add Brave Video Search API resource.\n\n2024-02-15 Add freshness filtering with custom date ranges.\n\n2024-11-05 Improve search operators support.\n\nOn this page\n\nVideo-Specific Index Search across a curated index of video content from multiple platforms and\nsources\n\nFreshness Filtering Filter results by discovery date - from last 24 hours to custom date ranges\n\nCountry & Language Options Target videos from specific countries and in preferred languages\n\nSafe Search Filtering Control adult content filtering with flexible options\n\nVideo Search API Documentation View the complete API reference, including endpoints, parameters, and example\nrequests"
  suggestedFilename: "services-video-search"
---

# Video search

## 源URL

https://api-dashboard.search.brave.com/documentation/services/video-search

## 描述

Video Search lets you send queries and receive relevant video results from a
dedicated index spanning various platforms and sources across the web. With
continuous indexing, your applications can retrieve tutorials, entertainment,
news clips, and more—all through a simple search.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial&freshness=pw`

## 代码示例

```bash
curl "https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial&freshness=pw" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

## 文档正文

Video Search lets you send queries and receive relevant video results from a
dedicated index spanning various platforms and sources across the web. With
continuous indexing, your applications can retrieve tutorials, entertainment,
news clips, and more—all through a simple search.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/videos/search?q=machine+learning+tutorial&freshness=pw`

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

Dedicated search for videos, with advanced filtering and freshness options

Overview

Video Search lets you send queries and receive relevant video results from a
dedicated index spanning various platforms and sources across the web. With
continuous indexing, your applications can retrieve tutorials, entertainment,
news clips, and more—all through a simple search.

Key Features

Video-Specific Index

Search across a curated index of video content from multiple platforms and
sources

Freshness Filtering

Filter results by discovery date - from last 24 hours to custom date ranges

Country & Language Options

Target videos from specific countries and in preferred languages

Safe Search Filtering

Control adult content filtering with flexible options

API Reference

Video Search API Documentation

View the complete API reference, including endpoints, parameters, and example
requests

Use Cases

Video Search is perfect for:

Video Platforms: Build video discovery and recommendation features

Educational Applications: Find tutorials, lectures, and instructional content

Content Aggregation: Gather video content from across the web

Entertainment Apps: Discover movies, shows, and entertainment content

Media Monitoring: Track video mentions and brand coverage across platforms

Video Search offers powerful date-based filtering to help you find the most relevant content:

Last 24 Hours (pd): Get the latest uploaded videos

Last 7 Days (pw): Track weekly video content

Last 31 Days (pm): Monitor monthly uploads

Last Year (py): Search annual video coverage

Custom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)

Example request filtering for videos from the past week:

Country and Language Targeting

Customize your video search results by specifying:

Country: Target videos from specific countries using 2-character country codes

Search Language: Filter results by content language

UI Language: Set the preferred language for response metadata

Example request for Spanish videos from Spain:

Search Operators

Video Search supports search operators to refine your queries:

Use quotes for exact phrase matching: "python programming"

Exclude terms with minus: cooking -vegan

Site-specific searches: site:youtube.com fitness workout

Pagination

Efficiently paginate through video results:

count: Number of results per page (max 50, default 20)

offset: Page number to retrieve (0-based, max 9)

Example request for page 2 with 20 results per page:

Safe Search

Control adult content filtering with the safesearch parameter:

off: No filtering

moderate: Filter explicit content (default)

strict: Filter explicit and suggestive content

This is particularly important for applications targeting family-friendly or educational audiences.

Video Search includes automatic spellcheck functionality to improve search accuracy:

Enabled by default

Automatically corrects common misspellings

The modified query is used for search and available in the response

To disable spellcheck:

Example: Complete Search Request

Here’s a comprehensive example combining multiple parameters:

This request:

Searches for “photography tips”

Targets US content

Returns English language results

Retrieves 25 results

Filters to videos from the past month

Applies strict safe search filtering

Changelog

This changelog outlines all significant changes to the Brave Video Search API in chronological order.

2023-06-20 Add Brave Video Search API resource.

2024-02-15 Add freshness filtering with custom date ranges.

2024-11-05 Improve search operators support.

On this page

Video-Specific Index Search across a curated index of video content from multiple platforms and
sources

Freshness Filtering Filter results by discovery date - from last 24 hours to custom date ranges

Country & Language Options Target videos from specific countries and in preferred languages

Safe Search Filtering Control adult content filtering with flexible options

Video Search API Documentation View the complete API reference, including endpoints, parameters, and example
requests
