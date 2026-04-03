---
id: "url-4f35cd"
type: "api"
title: "Goggles"
url: "https://api-dashboard.search.brave.com/documentation/resources/goggles"
description: "Goggles are a powerful feature that allows you to customize how search results are ranked. Using\na simple domain-specific language, you can create instructions to boost, downrank, or completely\nfilter results based on URL patterns, domains, and other criteria. This enables you to build\npersonalized search experiences tailored to specific use cases or audiences."
source: ""
tags: []
crawl_time: "2026-03-18T02:32:20.206Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Goggles are a powerful feature that allows you to customize how search results are ranked. Using\na simple domain-specific language, you can create instructions to boost, downrank, or completely\nfilter results based on URL patterns, domains, and other criteria. This enables you to build\npersonalized search experiences tailored to specific use cases or audiences.","Goggles work with both Web Search and News Search APIs, giving you\nfine-grained control over result ranking across different content types."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Custom Ranking Boost, downrank, or completely discard results based on your criteria   URL Pattern Matching Target specific domains, paths, or URL patterns with flexible matching rules   Multiple Sources Combine multiple hosted Goggles or use inline definitions for flexibility   Open & Shareable Host Goggles on GitLab, GitHub repositories, or Gists and share them with others"],"codeBlocks":[]}
    - {"level":"H2","title":"Custom Ranking","content":["Boost, downrank, or completely discard results based on your criteria"],"codeBlocks":[]}
    - {"level":"H2","title":"URL Pattern Matching","content":["Target specific domains, paths, or URL patterns with flexible matching rules"],"codeBlocks":[]}
    - {"level":"H2","title":"Multiple Sources","content":["Combine multiple hosted Goggles or use inline definitions for flexibility"],"codeBlocks":[]}
    - {"level":"H2","title":"Open & Shareable","content":["Host Goggles on GitLab, GitHub repositories, or Gists and share them with others"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Goggles are perfect for:","• Specialized Search Engines: Create vertical search experiences (e.g., tech blogs, academic sources only)\n• Content Curation: Boost trusted sources and demote undesired content\n• Brand Monitoring: Focus on specific news outlets or exclude competitors\n• Research Applications: Filter scholarly sources or specific geographic regions\n• Community Tools: Build search experiences tailored to specific communities or interests"],"codeBlocks":[]}
    - {"level":"H2","title":"Using Goggles with the API","content":["Both Web Search and News Search APIs accept the goggles query parameter. You can provide Goggles in three ways:","• Hosted Goggles URL: A link to a Goggles file hosted on GitHub, GitLab, or Gist\n• Inline Specification: Include Goggles rules directly in the request\n• Mixed: Combine multiple hosted Goggles and inline rules by passing multiple URLs and inline rules","Goggles must be submitted to Brave Search before they can be used with the API. Visit search.brave.com/goggles/create to register your Goggle.","Hosted Goggles are ideal for complex rule sets as they avoid URL length limitations. Simply pass\nthe URL of your hosted Goggles file:","You can combine multiple hosted Goggles by passing multiple goggles parameters:","For simple use cases, you can pass Goggles rules directly in the query parameter. This is useful\nfor quick experiments or simple filtering rules:","Delimit the rules with \\n (encoded to %0A) to include multiple inline\nrules in one goggles parameter.","For complex Goggles with many rules, use hosted files instead of inline specifications. URL\nlength limits can restrict the number of rules you can include inline."],"codeBlocks":[]}
    - {"level":"H3","title":"Using a Hosted Goggles","content":["Hosted Goggles are ideal for complex rule sets as they avoid URL length limitations. Simply pass\nthe URL of your hosted Goggles file:"],"codeBlocks":[]}
    - {"level":"H3","title":"Using Multiple Goggles","content":["You can combine multiple hosted Goggles by passing multiple goggles parameters:"],"codeBlocks":[]}
    - {"level":"H3","title":"Using Inline Goggles Specifications","content":["For simple use cases, you can pass Goggles rules directly in the query parameter. This is useful\nfor quick experiments or simple filtering rules:","Delimit the rules with \\n (encoded to %0A) to include multiple inline\nrules in one goggles parameter.","For complex Goggles with many rules, use hosted files instead of inline specifications. URL\nlength limits can restrict the number of rules you can include inline."],"codeBlocks":[]}
    - {"level":"H2","title":"Using Goggles with News Search","content":["Goggles work the same way with the News Search API. This allows you to customize news result\nrankings based on your preferred sources:"],"codeBlocks":["curl \"https://api.search.brave.com/res/v1/news/search?q=technology&goggles=https%3A%2F%2Fexample.com%2Fmy-news-sources.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""]}
    - {"level":"H2","title":"Goggles Syntax Overview","content":["Goggles use a simple domain-specific language (DSL) to express ranking instructions. Each\ninstruction targets URLs and specifies how matching results should be treated.","ActionDescriptionExample$boostIncrease ranking of matching results$boost,site=example.com$boost=NBoost with specific strength (1-10)$boost=5,site=example.com$downrankDecrease ranking of matching results$downrank,site=example.com$downrank=NDownrank with specific strength (1-10)$downrank=3,site=example.com$discardCompletely remove matching results$discard,site=example.com","PatternDescriptionExamplesite=Match specific domain$boost,site=dev.toPath patternsMatch URL paths/blog/$boostWildcards (*)Match any characters*/api/*$boost","When multiple instructions match the same URL, Goggles follow this precedence:","• $discard takes highest priority (unless generic)\n• $boost takes precedence over $downrank\n• Higher strength values take precedence over lower ones","For example, if one rule says $downrank=3,site=example.com and another says $boost=2,site=example.com, the boost rule wins."],"codeBlocks":["! name: Tech Blogs\n! description: Boost results from popular tech blogs\n! public: true\n! author: Your Name\n\n! Boost popular tech blogs\n$boost=3,site=dev.to\n$boost=3,site=medium.com\n$boost=3,site=hashnode.dev\n$boost=2,site=css-tricks.com\n\n! Downrank content farms\n$downrank=5,site=w3schools.com\n\n! Discard specific domains entirely\n$discard,site=spam-example.com"]}
    - {"level":"H3","title":"Basic Actions","content":["ActionDescriptionExample$boostIncrease ranking of matching results$boost,site=example.com$boost=NBoost with specific strength (1-10)$boost=5,site=example.com$downrankDecrease ranking of matching results$downrank,site=example.com$downrank=NDownrank with specific strength (1-10)$downrank=3,site=example.com$discardCompletely remove matching results$discard,site=example.com"],"codeBlocks":[]}
    - {"level":"H3","title":"URL Targeting","content":["PatternDescriptionExamplesite=Match specific domain$boost,site=dev.toPath patternsMatch URL paths/blog/$boostWildcards (*)Match any characters*/api/*$boost"],"codeBlocks":[]}
    - {"level":"H3","title":"Example Goggles File","content":[],"codeBlocks":["! name: Tech Blogs\n! description: Boost results from popular tech blogs\n! public: true\n! author: Your Name\n\n! Boost popular tech blogs\n$boost=3,site=dev.to\n$boost=3,site=medium.com\n$boost=3,site=hashnode.dev\n$boost=2,site=css-tricks.com\n\n! Downrank content farms\n$downrank=5,site=w3schools.com\n\n! Discard specific domains entirely\n$discard,site=spam-example.com"]}
    - {"level":"H3","title":"Conflict Resolution","content":["When multiple instructions match the same URL, Goggles follow this precedence:","• $discard takes highest priority (unless generic)\n• $boost takes precedence over $downrank\n• Higher strength values take precedence over lower ones","For example, if one rule says $downrank=3,site=example.com and another says $boost=2,site=example.com, the boost rule wins."],"codeBlocks":[]}
    - {"level":"H2","title":"Creating and Hosting Goggles","content":["To use a hosted Goggles with the API, you need to:","• Create a Goggles file — Write your rules in a plain text file (.goggle extension recommended)\n• Add metadata — Include required metadata at the top of your file\n• Host the file — Upload to one of the supported platforms:GitHub Gist (public or secret) GitHub (public repositories) GitLab (public files or snippets)\n• GitHub Gist (public or secret)\n• GitHub (public repositories)\n• GitLab (public files or snippets)\n• Submit for validation — Register your Goggles at search.brave.com/goggles/create","Every Goggles file must include these metadata fields at the top:","Optional metadata can be added to your Goggles file to provide additional information about the Goggles.","Goggles must be submitted to Brave Search before they can be used with the API. Visit search.brave.com/goggles/create to register your Goggle."],"codeBlocks":["! name: My Custom Goggles\n! description: Brief description of what this Goggles does\n! public: false\n! author: Your Name","! homepage: https://example.com\n! issues: https://github.com/user/repo/issues\n! avatar: #FF5733\n! license: MIT"]}
    - {"level":"H3","title":"Required Metadata","content":["Every Goggles file must include these metadata fields at the top:"],"codeBlocks":["! name: My Custom Goggles\n! description: Brief description of what this Goggles does\n! public: false\n! author: Your Name"]}
    - {"level":"H3","title":"Optional Metadata","content":["Optional metadata can be added to your Goggles file to provide additional information about the Goggles.","Goggles must be submitted to Brave Search before they can be used with the API. Visit search.brave.com/goggles/create to register your Goggle."],"codeBlocks":["! homepage: https://example.com\n! issues: https://github.com/user/repo/issues\n! avatar: #FF5733\n! license: MIT"]}
    - {"level":"H2","title":"Limitations","content":["Keep these limitations in mind when creating Goggles:","• File size: Maximum 2MB per Goggles file\n• Instruction count: Maximum 100,000 instructions per file\n• Instruction length: Maximum 500 characters per instruction\n• Wildcards: Maximum 2 * characters per instruction\n• Carets: Maximum 2 ^ characters per instruction","These limits are designed to ensure good performance while still allowing complex re-ranking\nlogic. Most use cases fit well within these constraints."],"codeBlocks":[]}
    - {"level":"H2","title":"Example Goggles","content":["Brave provides several example Goggles for learning purposes:","GogglesDescriptionTech BlogsBoosts content from popular tech blogsHacker NewsPrioritizes domains popular with the HN communityNo PinterestRemoves Pinterest results1K ShortRemoves top 1,000 most-viewed websites","Browse more community-created Goggles on the Goggles Discovery page."],"codeBlocks":[]}
    - {"level":"H2","title":"Related Resources","content":["Goggles Quickstart Guide Complete guide to creating Goggles with syntax reference and examples    Web Search API Learn about the Web Search API and all available parameters    News Search API Learn about the News Search API and filtering options    Search Operators Combine Goggles with search operators for even more control"],"codeBlocks":[]}
    - {"level":"H2","title":"Goggles Quickstart Guide","content":["Complete guide to creating Goggles with syntax reference and examples"],"codeBlocks":[]}
    - {"level":"H2","title":"Web Search API","content":["Learn about the Web Search API and all available parameters"],"codeBlocks":[]}
    - {"level":"H2","title":"News Search API","content":["Learn about the News Search API and filtering options"],"codeBlocks":[]}
    - {"level":"H2","title":"Search Operators","content":["Combine Goggles with search operators for even more control"],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Action","Description","Example"],"rows":[["$boost","Increase ranking of matching results","$boost,site=example.com"],["$boost=N","Boost with specific strength (1-10)","$boost=5,site=example.com"],["$downrank","Decrease ranking of matching results","$downrank,site=example.com"],["$downrank=N","Downrank with specific strength (1-10)","$downrank=3,site=example.com"],["$discard","Completely remove matching results","$discard,site=example.com"]]}
    - {"index":1,"headers":["Pattern","Description","Example"],"rows":[["site=","Match specific domain","$boost,site=dev.to"],["Path patterns","Match URL paths","/blog/$boost"],["Wildcards (*)","Match any characters","*/api/*$boost"]]}
    - {"index":2,"headers":["Goggles","Description"],"rows":[["Tech Blogs","Boosts content from popular tech blogs"],["Hacker News","Prioritizes domains popular with the HN community"],["No Pinterest","Removes Pinterest results"],["1K Short","Removes top 1,000 most-viewed websites"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search\" \\\n  --url-query \"q=programming tutorials\" \\\n  --url-query \"goggles=https://raw.githubusercontent.com/brave/goggles-quickstart/main/goggles/tech_blogs.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search\" \\\n  --url-query \"q=programming tutorials\" \\\n  --url-query \"goggles=https://raw.githubusercontent.com/brave/goggles-quickstart/main/goggles/tech_blogs.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=rust+programming&goggles=https%3A%2F%2Fexample.com%2Fgoggle1.goggle&goggles=https%3A%2F%2Fexample.com%2Fgoggle2.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=rust+programming&goggles=https%3A%2F%2Fexample.com%2Fgoggle1.goggle&goggles=https%3A%2F%2Fexample.com%2Fgoggle2.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=rust+programming&goggles=https%3A%2F%2Fexample.com%2Fgoggle1.goggle&goggles=https%3A%2F%2Fexample.com%2Fgoggle2.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=rust+programming&goggles=https%3A%2F%2Fexample.com%2Fgoggle1.goggle&goggles=https%3A%2F%2Fexample.com%2Fgoggle2.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=technology&goggles=https%3A%2F%2Fexample.com%2Fmy-news-sources.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/news/search?q=technology&goggles=https%3A%2F%2Fexample.com%2Fmy-news-sources.goggle\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nResources\n\nCustomize search rankings with Goggles to create personalized search experiences\n\nOverview\n\nGoggles are a powerful feature that allows you to customize how search results are ranked. Using\na simple domain-specific language, you can create instructions to boost, downrank, or completely\nfilter results based on URL patterns, domains, and other criteria. This enables you to build\npersonalized search experiences tailored to specific use cases or audiences.\n\nGoggles work with both Web Search and News Search APIs, giving you\nfine-grained control over result ranking across different content types.\n\nKey Features\n\nCustom Ranking\n\nBoost, downrank, or completely discard results based on your criteria\n\nURL Pattern Matching\n\nTarget specific domains, paths, or URL patterns with flexible matching rules\n\nMultiple Sources\n\nCombine multiple hosted Goggles or use inline definitions for flexibility\n\nOpen & Shareable\n\nHost Goggles on GitLab, GitHub repositories, or Gists and share them with others\n\nUse Cases\n\nGoggles are perfect for:\n\nSpecialized Search Engines: Create vertical search experiences (e.g., tech blogs, academic sources only)\n\nContent Curation: Boost trusted sources and demote undesired content\n\nBrand Monitoring: Focus on specific news outlets or exclude competitors\n\nResearch Applications: Filter scholarly sources or specific geographic regions\n\nCommunity Tools: Build search experiences tailored to specific communities or interests\n\nUsing Goggles with the API\n\nBoth Web Search and News Search APIs accept the goggles query parameter. You can provide Goggles in three ways:\n\nHosted Goggles URL: A link to a Goggles file hosted on GitHub, GitLab, or Gist\n\nInline Specification: Include Goggles rules directly in the request\n\nMixed: Combine multiple hosted Goggles and inline rules by passing multiple URLs and inline rules\n\nGoggles must be submitted to Brave Search before they can be used with the API. Visit search.brave.com/goggles/create to register your Goggle.\n\nUsing a Hosted Goggles\n\nHosted Goggles are ideal for complex rule sets as they avoid URL length limitations. Simply pass\nthe URL of your hosted Goggles file:\n\nPython\n\nNode.js\n\nUsing Multiple Goggles\n\nYou can combine multiple hosted Goggles by passing multiple goggles parameters:\n\nUsing Inline Goggles Specifications\n\nFor simple use cases, you can pass Goggles rules directly in the query parameter. This is useful\nfor quick experiments or simple filtering rules:\n\nDelimit the rules with \\n (encoded to %0A) to include multiple inline\nrules in one goggles parameter.\n\nFor complex Goggles with many rules, use hosted files instead of inline specifications. URL\nlength limits can restrict the number of rules you can include inline.\n\nUsing Goggles with News Search\n\nGoggles work the same way with the News Search API. This allows you to customize news result\nrankings based on your preferred sources:\n\nGoggles Syntax Overview\n\nGoggles use a simple domain-specific language (DSL) to express ranking instructions. Each\ninstruction targets URLs and specifies how matching results should be treated.\n\nBasic Actions\n\nURL Targeting\n\nExample Goggles File\n\nConflict Resolution\n\nWhen multiple instructions match the same URL, Goggles follow this precedence:\n\n$discard takes highest priority (unless generic)\n\n$boost takes precedence over $downrank\n\nHigher strength values take precedence over lower ones\n\nFor example, if one rule says $downrank=3,site=example.com and another says $boost=2,site=example.com, the boost rule wins.\n\nCreating and Hosting Goggles\n\nTo use a hosted Goggles with the API, you need to:\n\nCreate a Goggles file — Write your rules in a plain text file (.goggle extension recommended)\n\nAdd metadata — Include required metadata at the top of your file\n\nHost the file — Upload to one of the supported platforms:GitHub Gist (public or secret) GitHub (public repositories) GitLab (public files or snippets)\n\nGitHub Gist (public or secret)\n\nGitHub (public repositories)\n\nGitLab (public files or snippets)\n\nSubmit for validation — Register your Goggles at search.brave.com/goggles/create\n\nRequired Metadata\n\nEvery Goggles file must include these metadata fields at the top:\n\nOptional Metadata\n\nOptional metadata can be added to your Goggles file to provide additional information about the Goggles.\n\nLimitations\n\nKeep these limitations in mind when creating Goggles:\n\nFile size: Maximum 2MB per Goggles file\n\nInstruction count: Maximum 100,000 instructions per file\n\nInstruction length: Maximum 500 characters per instruction\n\nWildcards: Maximum 2 * characters per instruction\n\nCarets: Maximum 2 ^ characters per instruction\n\nThese limits are designed to ensure good performance while still allowing complex re-ranking\nlogic. Most use cases fit well within these constraints.\n\nBest Practices\n\nBegin with a few key rules and test their effect on search results. Gradually add more rules as\nyou understand how they interact.\n\nInline Goggles specifications are convenient for simple cases, but URL length limits restrict\ntheir complexity. For production applications with many rules, always use hosted Goggles files.\n\nA Goggles that works well for one query might behave unexpectedly for others. Test your Goggles\nwith a variety of queries to ensure consistent behavior across different use cases.\n\nSince Brave Search doesn’t maintain version history, use Git to track changes to your Goggles\nfiles. This allows you to roll back changes if needed and understand how your rules have\nevolved.\n\nExample Goggles\n\nBrave provides several example Goggles for learning purposes:\n\nBrowse more community-created Goggles on the Goggles Discovery page.\n\nRelated Resources\n\nGoggles Quickstart Guide\n\nComplete guide to creating Goggles with syntax reference and examples\n\nWeb Search API\n\nLearn about the Web Search API and all available parameters\n\nNews Search API\n\nLearn about the News Search API and filtering options\n\nSearch Operators\n\nCombine Goggles with search operators for even more control\n\nOn this page\n\nCustom Ranking Boost, downrank, or completely discard results based on your criteria\n\nURL Pattern Matching Target specific domains, paths, or URL patterns with flexible matching rules\n\nMultiple Sources Combine multiple hosted Goggles or use inline definitions for flexibility\n\nOpen & Shareable Host Goggles on GitLab, GitHub repositories, or Gists and share them with others\n\nGoggles Quickstart Guide Complete guide to creating Goggles with syntax reference and examples\n\nWeb Search API Learn about the Web Search API and all available parameters\n\nNews Search API Learn about the News Search API and filtering options\n\nSearch Operators Combine Goggles with search operators for even more control"
  suggestedFilename: "resources-goggles"
---

# Goggles

## 源URL

https://api-dashboard.search.brave.com/documentation/resources/goggles

## 描述

Goggles are a powerful feature that allows you to customize how search results are ranked. Using
a simple domain-specific language, you can create instructions to boost, downrank, or completely
filter results based on URL patterns, domains, and other criteria. This enables you to build
personalized search experiences tailored to specific use cases or audiences.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/web/search" \
  --url-query "q=programming tutorials" \
  --url-query "goggles=https://raw.githubusercontent.com/brave/goggles-quickstart/main/goggles/tech_blogs.goggle" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

### 示例 2 (bash)

```bash
curl "https://api.search.brave.com/res/v1/news/search?q=technology&goggles=https%3A%2F%2Fexample.com%2Fmy-news-sources.goggle" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

## 文档正文

Goggles are a powerful feature that allows you to customize how search results are ranked. Using
a simple domain-specific language, you can create instructions to boost, downrank, or completely
filter results based on URL patterns, domains, and other criteria. This enables you to build
personalized search experiences tailored to specific use cases or audiences.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search`

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

Resources

Customize search rankings with Goggles to create personalized search experiences

Overview

Goggles are a powerful feature that allows you to customize how search results are ranked. Using
a simple domain-specific language, you can create instructions to boost, downrank, or completely
filter results based on URL patterns, domains, and other criteria. This enables you to build
personalized search experiences tailored to specific use cases or audiences.

Goggles work with both Web Search and News Search APIs, giving you
fine-grained control over result ranking across different content types.

Key Features

Custom Ranking

Boost, downrank, or completely discard results based on your criteria

URL Pattern Matching

Target specific domains, paths, or URL patterns with flexible matching rules

Multiple Sources

Combine multiple hosted Goggles or use inline definitions for flexibility

Open & Shareable

Host Goggles on GitLab, GitHub repositories, or Gists and share them with others

Use Cases

Goggles are perfect for:

Specialized Search Engines: Create vertical search experiences (e.g., tech blogs, academic sources only)

Content Curation: Boost trusted sources and demote undesired content

Brand Monitoring: Focus on specific news outlets or exclude competitors

Research Applications: Filter scholarly sources or specific geographic regions

Community Tools: Build search experiences tailored to specific communities or interests

Using Goggles with the API

Both Web Search and News Search APIs accept the goggles query parameter. You can provide Goggles in three ways:

Hosted Goggles URL: A link to a Goggles file hosted on GitHub, GitLab, or Gist

Inline Specification: Include Goggles rules directly in the request

Mixed: Combine multiple hosted Goggles and inline rules by passing multiple URLs and inline rules

Goggles must be submitted to Brave Search before they can be used with the API. Visit search.brave.com/goggles/create to register your Goggle.

Using a Hosted Goggles

Hosted Goggles are ideal for complex rule sets as they avoid URL length limitations. Simply pass
the URL of your hosted Goggles file:

Python

Node.js

Using Multiple Goggles

You can combine multiple hosted Goggles by passing multiple goggles parameters:

Using Inline Goggles Specifications

For simple use cases, you can pass Goggles rules directly in the query parameter. This is useful
for quick experiments or simple filtering rules:

Delimit the rules with \n (encoded to %0A) to include multiple inline
rules in one goggles parameter.

For complex Goggles with many rules, use hosted files instead of inline specifications. URL
length limits can restrict the number of rules you can include inline.

Using Goggles with News Search

Goggles work the same way with the News Search API. This allows you to customize news result
rankings based on your preferred sources:

Goggles Syntax Overview

Goggles use a simple domain-specific language (DSL) to express ranking instructions. Each
instruction targets URLs and specifies how matching results should be treated.

Basic Actions

URL Targeting

Example Goggles File

Conflict Resolution

When multiple instructions match the same URL, Goggles follow this precedence:

$discard takes highest priority (unless generic)

$boost takes precedence over $downrank

Higher strength values take precedence over lower ones

For example, if one rule says $downrank=3,site=example.com and another says $boost=2,site=example.com, the boost rule wins.

Creating and Hosting Goggles

To use a hosted Goggles with the API, you need to:

Create a Goggles file — Write your rules in a plain text file (.goggle extension recommended)

Add metadata — Include required metadata at the top of your file

Host the file — Upload to one of the supported platforms:GitHub Gist (public or secret) GitHub (public repositories) GitLab (public files or snippets)

GitHub Gist (public or secret)

GitHub (public repositories)

GitLab (public files or snippets)

Submit for validation — Register your Goggles at search.brave.com/goggles/create

Required Metadata

Every Goggles file must include these metadata fields at the top:

Optional Metadata

Optional metadata can be added to your Goggles file to provide additional information about the Goggles.

Limitations

Keep these limitations in mind when creating Goggles:

File size: Maximum 2MB per Goggles file

Instruction count: Maximum 100,000 instructions per file

Instruction length: Maximum 500 characters per instruction

Wildcards: Maximum 2 * characters per instruction

Carets: Maximum 2 ^ characters per instruction

These limits are designed to ensure good performance while sti
