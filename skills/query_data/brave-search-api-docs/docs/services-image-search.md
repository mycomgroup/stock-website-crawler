---
id: "url-541e13b0"
type: "api"
title: "Image search"
url: "https://api-dashboard.search.brave.com/documentation/services/image-search"
description: "Image Search provides access to a vast index of images from across the internet.\nOur service continuously crawls and indexes images from various sources, enabling\nyou to retrieve relevant visual content for your applications with powerful\nfiltering and customization options."
source: ""
tags: []
crawl_time: "2026-03-18T03:28:12.943Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/images/search?q=mountain+landscape"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Image Search provides access to a vast index of images from across the internet.\nOur service continuously crawls and indexes images from various sources, enabling\nyou to retrieve relevant visual content for your applications with powerful\nfiltering and customization options."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Extensive Image Index Search across billions of indexed images from diverse sources worldwide   High Volume Results Retrieve up to 200 images per request for comprehensive coverage   Country & Language Options Target images from specific countries and in preferred languages   Strict Safe Search Default strict filtering ensures family-friendly results"],"codeBlocks":[]}
    - {"level":"H2","title":"Extensive Image Index","content":["Search across billions of indexed images from diverse sources worldwide"],"codeBlocks":[]}
    - {"level":"H2","title":"High Volume Results","content":["Retrieve up to 200 images per request for comprehensive coverage"],"codeBlocks":[]}
    - {"level":"H2","title":"Country & Language Options","content":["Target images from specific countries and in preferred languages"],"codeBlocks":[]}
    - {"level":"H2","title":"Strict Safe Search","content":["Default strict filtering ensures family-friendly results"],"codeBlocks":[]}
    - {"level":"H2","title":"Image Search API Documentation","content":["View the complete API reference, including endpoints, parameters, and example\nrequests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Image Search is perfect for:","• Visual Content Discovery: Build image galleries and discovery features\n• E-commerce Applications: Find product images and visual inspiration\n• Creative Tools: Source images for design and creative projects\n• Content Management: Discover and aggregate visual content\n• Research and Analysis: Gather visual data for analysis and research"],"codeBlocks":[]}
    - {"level":"H2","title":"Basic Search","content":["Get started with a simple image search request:"],"codeBlocks":[]}
    - {"level":"H2","title":"Country and Language Targeting","content":["Customize your image search results by specifying:","• Country: Prefer images from specific countries using country codes (or ALL for worldwide)\n• Search Language: Prefer results by content language","Example request for images from Japan in Japanese:"],"codeBlocks":[]}
    - {"level":"H2","title":"Result Count Control","content":["Image Search supports retrieving large batches of results:","• Default: 50 images per request\n• Maximum: 200 images per request\n• Higher limits than other search types for comprehensive visual content discovery","Example request for 100 images:","The actual number of images returned may be less than requested based on\navailable results for the query."],"codeBlocks":[]}
    - {"level":"H2","title":"Safe Search","content":["Image Search prioritizes safe content with strict filtering by default:","• strict: Drops all adult content from search results (default)\n• off: No filtering applied (except for illegal content)","This default setting ensures that image results are appropriate for all audiences out of the box.","Example request with safe search disabled:","Disabling safe search may return adult or inappropriate content. Use with\ncaution and only when appropriate for your use case."],"codeBlocks":[]}
    - {"level":"H2","title":"Spellcheck","content":["Image Search includes automatic spellcheck functionality to improve search accuracy:","• Enabled by default\n• Automatically corrects common misspellings\n• The modified query is used for search and available in the response\n• Particularly useful for visual searches where terminology matters","To disable spellcheck:"],"codeBlocks":[]}
    - {"level":"H2","title":"Example: Complete Search Request","content":["Here’s a comprehensive example combining multiple parameters:","This request:","• Searches for “modern architecture”\n• Targets US content\n• Returns English language results\n• Retrieves up to 150 images\n• Applies strict safe search filtering"],"codeBlocks":[]}
    - {"level":"H2","title":"Response Format","content":["Each image result typically includes:","• Image URL and thumbnail\n• Source page URL\n• Image dimensions\n• Title and description\n• Publisher information","See the API Reference for complete response schema details."],"codeBlocks":[]}
    - {"level":"H2","title":"Image Proxy and Thumbnails","content":["Each image result includes a thumbnail URL that is served through the Brave Search image proxy. The thumbnail is resized to have a width of 500 pixels while maintaining the original aspect ratio.","Brave Search uses proxied image URLs for two important reasons:","• Reduced load on source servers: By caching and serving images through our proxy, we reduce the number of requests to the original image hosts.\n• User privacy protection: Proxied URLs prevent image source servers from tracking end users, as all requests originate from Brave’s infrastructure rather than user devices.","The properties field in each image result contains additional URL information:","• url: The original image URL from the source website\n• placeholder: A small placeholder URL, also served through the Brave Search image proxy\n• Properties often include width and height values, though these are not always available","This allows you to choose between the standard 500px thumbnail in the main response or access the original source URL when needed."],"codeBlocks":[]}
    - {"level":"H3","title":"Why Brave Uses Proxied Image URLs","content":["Brave Search uses proxied image URLs for two important reasons:","• Reduced load on source servers: By caching and serving images through our proxy, we reduce the number of requests to the original image hosts.\n• User privacy protection: Proxied URLs prevent image source servers from tracking end users, as all requests originate from Brave’s infrastructure rather than user devices."],"codeBlocks":[]}
    - {"level":"H3","title":"Properties Field","content":["The properties field in each image result contains additional URL information:","• url: The original image URL from the source website\n• placeholder: A small placeholder URL, also served through the Brave Search image proxy\n• Properties often include width and height values, though these are not always available","This allows you to choose between the standard 500px thumbnail in the main response or access the original source URL when needed."],"codeBlocks":[]}
    - {"level":"H2","title":"Best Practices","content":["• Use descriptive, specific terms for better results\n• Combine multiple keywords to narrow down results\n• Consider language and regional variations in terminology","• Request only the number of images you need\n• Use appropriate country and language filters to reduce noise\n• Implement caching on your end to minimize API calls","• Keep strict safe search enabled for public-facing applications\n• Implement additional content moderation if needed for your specific use case\n• Be aware of copyright and licensing when using discovered images"],"codeBlocks":[]}
    - {"level":"H3","title":"Query Optimization","content":["• Use descriptive, specific terms for better results\n• Combine multiple keywords to narrow down results\n• Consider language and regional variations in terminology"],"codeBlocks":[]}
    - {"level":"H3","title":"Performance","content":["• Request only the number of images you need\n• Use appropriate country and language filters to reduce noise\n• Implement caching on your end to minimize API calls"],"codeBlocks":[]}
    - {"level":"H3","title":"Content Safety","content":["• Keep strict safe search enabled for public-facing applications\n• Implement additional content moderation if needed for your specific use case\n• Be aware of copyright and licensing when using discovered images"],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave Image Search API in chronological order.","• 2023-05-10 Add Brave Image Search API resource.\n• 2024-01-20 Increase maximum result count to 200 images.\n• 2024-08-15 Improve spellcheck accuracy for visual search terms."],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=mountain+landscape\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=mountain+landscape\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=桜&country=JP&search_lang=ja\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=桜&country=JP&search_lang=ja\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=wildlife+photography&count=100\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=wildlife+photography&count=100\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=art&safesearch=off\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=art&safesearch=off\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=architecure&spellcheck=false\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=architecure&spellcheck=false\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=modern+architecture&country=US&search_lang=en&count=150&safesearch=strict\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/images/search?q=modern+architecture&country=US&search_lang=en&count=150&safesearch=strict\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nSearch from a comprehensive index of images across the web with advanced filtering options\n\nOverview\n\nImage Search provides access to a vast index of images from across the internet.\nOur service continuously crawls and indexes images from various sources, enabling\nyou to retrieve relevant visual content for your applications with powerful\nfiltering and customization options.\n\nKey Features\n\nExtensive Image Index\n\nSearch across billions of indexed images from diverse sources worldwide\n\nHigh Volume Results\n\nRetrieve up to 200 images per request for comprehensive coverage\n\nCountry & Language Options\n\nTarget images from specific countries and in preferred languages\n\nStrict Safe Search\n\nDefault strict filtering ensures family-friendly results\n\nAPI Reference\n\nImage Search API Documentation\n\nView the complete API reference, including endpoints, parameters, and example\nrequests\n\nUse Cases\n\nImage Search is perfect for:\n\nVisual Content Discovery: Build image galleries and discovery features\n\nE-commerce Applications: Find product images and visual inspiration\n\nCreative Tools: Source images for design and creative projects\n\nContent Management: Discover and aggregate visual content\n\nResearch and Analysis: Gather visual data for analysis and research\n\nBasic Search\n\nGet started with a simple image search request:\n\nCountry and Language Targeting\n\nCustomize your image search results by specifying:\n\nCountry: Prefer images from specific countries using country codes (or ALL for worldwide)\n\nSearch Language: Prefer results by content language\n\nExample request for images from Japan in Japanese:\n\nResult Count Control\n\nImage Search supports retrieving large batches of results:\n\nDefault: 50 images per request\n\nMaximum: 200 images per request\n\nHigher limits than other search types for comprehensive visual content discovery\n\nExample request for 100 images:\n\nThe actual number of images returned may be less than requested based on\navailable results for the query.\n\nSafe Search\n\nImage Search prioritizes safe content with strict filtering by default:\n\nstrict: Drops all adult content from search results (default)\n\noff: No filtering applied (except for illegal content)\n\nThis default setting ensures that image results are appropriate for all audiences out of the box.\n\nExample request with safe search disabled:\n\nDisabling safe search may return adult or inappropriate content. Use with\ncaution and only when appropriate for your use case.\n\nImage Search includes automatic spellcheck functionality to improve search accuracy:\n\nEnabled by default\n\nAutomatically corrects common misspellings\n\nThe modified query is used for search and available in the response\n\nParticularly useful for visual searches where terminology matters\n\nTo disable spellcheck:\n\nExample: Complete Search Request\n\nHere’s a comprehensive example combining multiple parameters:\n\nThis request:\n\nSearches for “modern architecture”\n\nTargets US content\n\nReturns English language results\n\nRetrieves up to 150 images\n\nApplies strict safe search filtering\n\nResponse Format\n\nEach image result typically includes:\n\nImage URL and thumbnail\n\nSource page URL\n\nImage dimensions\n\nTitle and description\n\nPublisher information\n\nSee the API Reference for complete response schema details.\n\nImage Proxy and Thumbnails\n\nEach image result includes a thumbnail URL that is served through the Brave Search image proxy. The thumbnail is resized to have a width of 500 pixels while maintaining the original aspect ratio.\n\nWhy Brave Uses Proxied Image URLs\n\nBrave Search uses proxied image URLs for two important reasons:\n\nReduced load on source servers: By caching and serving images through our proxy, we reduce the number of requests to the original image hosts.\n\nUser privacy protection: Proxied URLs prevent image source servers from tracking end users, as all requests originate from Brave’s infrastructure rather than user devices.\n\nProperties Field\n\nThe properties field in each image result contains additional URL information:\n\nurl: The original image URL from the source website\n\nplaceholder: A small placeholder URL, also served through the Brave Search image proxy\n\nProperties often include width and height values, though these are not always available\n\nThis allows you to choose between the standard 500px thumbnail in the main response or access the original source URL when needed.\n\nBest Practices\n\nQuery Optimization\n\nUse descriptive, specific terms for better results\n\nCombine multiple keywords to narrow down results\n\nConsider language and regional variations in terminology\n\nPerformance\n\nRequest only the number of images you need\n\nUse appropriate country and language filters to reduce noise\n\nImplement caching on your end to minimize API calls\n\nContent Safety\n\nKeep strict safe search enabled for public-facing applications\n\nImplement additional content moderation if needed for your specific use case\n\nBe aware of copyright and licensing when using discovered images\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave Image Search API in chronological order.\n\n2023-05-10 Add Brave Image Search API resource.\n\n2024-01-20 Increase maximum result count to 200 images.\n\n2024-08-15 Improve spellcheck accuracy for visual search terms.\n\nOn this page\n\nExtensive Image Index Search across billions of indexed images from diverse sources worldwide\n\nHigh Volume Results Retrieve up to 200 images per request for comprehensive coverage\n\nCountry & Language Options Target images from specific countries and in preferred languages\n\nStrict Safe Search Default strict filtering ensures family-friendly results\n\nImage Search API Documentation View the complete API reference, including endpoints, parameters, and example\nrequests"
  suggestedFilename: "services-image-search"
---

# Image search

## 源URL

https://api-dashboard.search.brave.com/documentation/services/image-search

## 描述

Image Search provides access to a vast index of images from across the internet.
Our service continuously crawls and indexes images from various sources, enabling
you to retrieve relevant visual content for your applications with powerful
filtering and customization options.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/images/search?q=mountain+landscape`

## 代码示例

```bash
curl "https://api.search.brave.com/res/v1/images/search?q=mountain+landscape" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

## 文档正文

Image Search provides access to a vast index of images from across the internet.
Our service continuously crawls and indexes images from various sources, enabling
you to retrieve relevant visual content for your applications with powerful
filtering and customization options.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/images/search?q=mountain+landscape`

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

Search from a comprehensive index of images across the web with advanced filtering options

Overview

Image Search provides access to a vast index of images from across the internet.
Our service continuously crawls and indexes images from various sources, enabling
you to retrieve relevant visual content for your applications with powerful
filtering and customization options.

Key Features

Extensive Image Index

Search across billions of indexed images from diverse sources worldwide

High Volume Results

Retrieve up to 200 images per request for comprehensive coverage

Country & Language Options

Target images from specific countries and in preferred languages

Strict Safe Search

Default strict filtering ensures family-friendly results

API Reference

Image Search API Documentation

View the complete API reference, including endpoints, parameters, and example
requests

Use Cases

Image Search is perfect for:

Visual Content Discovery: Build image galleries and discovery features

E-commerce Applications: Find product images and visual inspiration

Creative Tools: Source images for design and creative projects

Content Management: Discover and aggregate visual content

Research and Analysis: Gather visual data for analysis and research

Basic Search

Get started with a simple image search request:

Country and Language Targeting

Customize your image search results by specifying:

Country: Prefer images from specific countries using country codes (or ALL for worldwide)

Search Language: Prefer results by content language

Example request for images from Japan in Japanese:

Result Count Control

Image Search supports retrieving large batches of results:

Default: 50 images per request

Maximum: 200 images per request

Higher limits than other search types for comprehensive visual content discovery

Example request for 100 images:

The actual number of images returned may be less than requested based on
available results for the query.

Safe Search

Image Search prioritizes safe content with strict filtering by default:

strict: Drops all adult content from search results (default)

off: No filtering applied (except for illegal content)

This default setting ensures that image results are appropriate for all audiences out of the box.

Example request with safe search disabled:

Disabling safe search may return adult or inappropriate content. Use with
caution and only when appropriate for your use case.

Image Search includes automatic spellcheck functionality to improve search accuracy:

Enabled by default

Automatically corrects common misspellings

The modified query is used for search and available in the response

Particularly useful for visual searches where terminology matters

To disable spellcheck:

Example: Complete Search Request

Here’s a comprehensive example combining multiple parameters:

This request:

Searches for “modern architecture”

Targets US content

Returns English language results

Retrieves up to 150 images

Applies strict safe search filtering

Response Format

Each image result typically includes:

Image URL and thumbnail

Source page URL

Image dimensions

Title and description

Publisher information

See the API Reference for complete response schema details.

Image Proxy and Thumbnails

Each image result includes a thumbnail URL that is served through the Brave Search image proxy. The thumbnail is resized to have a width of 500 pixels while maintaining the original aspect ratio.

Why Brave Uses Proxied Image URLs

Brave Search uses proxied image URLs for two important reasons:

Reduced load on source servers: By caching and serving images through our proxy, we reduce the number of requests to the original image hosts.

User privacy protection: Proxied URLs prevent image source servers from tracking end users, as all requests originate from Brave’s infrastructure rather than user devices.

Properties Field

The properties field in each image result contains additional URL information:

url: The original image URL from the source website

placeholder: A small placeholder URL, also served through the Brave Search image proxy

Properties often include width and height values, though these are not always available

This allows you to choose between the standard 500px thumbnail in the main response or access the original source URL when needed.

Best Practices

Query Optimization

Use descriptive, specific terms for better results

Combine multiple keywords to narrow down results

Consider language and regional variations in terminology

Performance

Request only the number of images you need

Use appropriate country and language filters to reduce noise

Implem
