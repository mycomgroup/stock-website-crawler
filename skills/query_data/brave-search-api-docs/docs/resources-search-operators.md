---
id: "url-2f0bebb1"
type: "api"
title: "Search operators"
url: "https://api-dashboard.search.brave.com/documentation/resources/search-operators"
description: "Search operators are special commands that you can add to your search queries to filter and refine results. They help you find exactly what you’re looking for by limiting and focusing your search with precision. You can place them anywhere in your query string to gain better control over the returned results."
source: ""
tags: []
crawl_time: "2026-03-18T03:28:55.292Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf+lang:en"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Search operators are special commands that you can add to your search queries to filter and refine results. They help you find exactly what you’re looking for by limiting and focusing your search with precision. You can place them anywhere in your query string to gain better control over the returned results.","Whether you’re building a specialized search application, filtering results by file type, or narrowing down results to specific websites, search operators give you the power to create more targeted searches."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Precise Filtering Narrow down results by file type, location, language, and more   Flexible Placement Add operators anywhere in your query for natural query construction   Content Targeting Search within specific parts of web pages (title, body, or both)   Logical Combinations Combine multiple operators with AND, OR, NOT for complex queries"],"codeBlocks":[]}
    - {"level":"H2","title":"Precise Filtering","content":["Narrow down results by file type, location, language, and more"],"codeBlocks":[]}
    - {"level":"H2","title":"Flexible Placement","content":["Add operators anywhere in your query for natural query construction"],"codeBlocks":[]}
    - {"level":"H2","title":"Content Targeting","content":["Search within specific parts of web pages (title, body, or both)"],"codeBlocks":[]}
    - {"level":"H2","title":"Logical Combinations","content":["Combine multiple operators with AND, OR, NOT for complex queries"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Search operators are perfect for:","• Research Applications: Filter academic papers, PDFs, and documents by file type\n• Competitive Analysis: Monitor specific domains while excluding others\n• Multilingual Search: Target content in specific languages and regions\n• Content Discovery: Find exact phrases and specific keyword placements\n• Advanced Filtering: Build complex search logic with operator combinations"],"codeBlocks":[]}
    - {"level":"H2","title":"Basic Search Operators","content":["Returns web pages with a specific file extension.","Example: To find the Honda GX120 Owner’s manual in PDF format:","Returns web pages created in the specified file type.","Example: To find documentation about cognitive changes in PDF format:","Returns web pages containing the specified term in the page title.","Example: To find SEO conference pages with “2023” in the title:","Returns web pages containing the specified term in the body of the page.","Example: To find information about the Nvidia GeForce GTX 1080 Ti with “founders edition” in the body:","Returns web pages containing the specified term either in the title or in the body.","Example: To find pages about the 2024 Oscars with “best costume design” anywhere on the page:","Returns web pages written in the specified language. The language code must be in ISO 639-1 two-letter format.","Example: To find information about visas only in Spanish:","Common language codes:","• en - English\n• es - Spanish\n• fr - French\n• de - German\n• ja - Japanese\n• zh - Chinese","Returns web pages from a specific country or region. The country code must be in ISO 3166-1 alpha-2 format.","Example: To find Canadian web pages about Niagara Falls:","Common country codes:","• us - United States\n• gb - United Kingdom\n• ca - Canada\n• au - Australia\n• de - Germany\n• fr - France","Returns web pages from only a specific website or domain.","Example: To find information about Goggles only on Brave pages:","You can also use subdomains (e.g., site:blog.example.com) or partial domains\n(e.g., site:example.com will include all subdomains)."],"codeBlocks":["Honda GX120 owners manual ext:pdf","evaluation of age cognitive changes filetype:pdf","seo conference intitle:2023","nvidia 1080 ti inbody:\"founders edition\"","oscars 2024 inpage:\"best costume design\"","visas lang:es","niagara falls loc:ca","goggles site:brave.com"]}
    - {"level":"H3","title":"File Extension and Type","content":["Returns web pages with a specific file extension.","Example: To find the Honda GX120 Owner’s manual in PDF format:","Returns web pages created in the specified file type.","Example: To find documentation about cognitive changes in PDF format:"],"codeBlocks":["Honda GX120 owners manual ext:pdf","evaluation of age cognitive changes filetype:pdf"]}
    - {"level":"H3","title":"Content Location","content":["Returns web pages containing the specified term in the page title.","Example: To find SEO conference pages with “2023” in the title:","Returns web pages containing the specified term in the body of the page.","Example: To find information about the Nvidia GeForce GTX 1080 Ti with “founders edition” in the body:","Returns web pages containing the specified term either in the title or in the body.","Example: To find pages about the 2024 Oscars with “best costume design” anywhere on the page:"],"codeBlocks":["seo conference intitle:2023","nvidia 1080 ti inbody:\"founders edition\"","oscars 2024 inpage:\"best costume design\""]}
    - {"level":"H3","title":"Language and Location","content":["Returns web pages written in the specified language. The language code must be in ISO 639-1 two-letter format.","Example: To find information about visas only in Spanish:","Common language codes:","• en - English\n• es - Spanish\n• fr - French\n• de - German\n• ja - Japanese\n• zh - Chinese","Returns web pages from a specific country or region. The country code must be in ISO 3166-1 alpha-2 format.","Example: To find Canadian web pages about Niagara Falls:","Common country codes:","• us - United States\n• gb - United Kingdom\n• ca - Canada\n• au - Australia\n• de - Germany\n• fr - France"],"codeBlocks":["visas lang:es","niagara falls loc:ca"]}
    - {"level":"H3","title":"Domain Filtering","content":["Returns web pages from only a specific website or domain.","Example: To find information about Goggles only on Brave pages:","You can also use subdomains (e.g., site:blog.example.com) or partial domains\n(e.g., site:example.com will include all subdomains)."],"codeBlocks":["goggles site:brave.com"]}
    - {"level":"H2","title":"Advanced Search Operators","content":["Forces the inclusion of a term in the title or body of the page. Ensures that the specified keyword appears in results.","Example: To find information about FreeSync GPU technology, ensuring “FreeSync” appears:","Excludes web pages containing the specified term from results.","Example: To search for office-related content while excluding Microsoft:","The minus operator is particularly useful for filtering out common but\nunwanted terms from your search results.","Returns web pages containing exact matches to your query in the specified order.","Example: To find pages about Harry Potter with the exact phrase “order of the phoenix”:"],"codeBlocks":["gpu +freesync","office -microsoft","harry potter \"order of the phoenix\""]}
    - {"level":"H3","title":"Inclusion and Exclusion","content":["Forces the inclusion of a term in the title or body of the page. Ensures that the specified keyword appears in results.","Example: To find information about FreeSync GPU technology, ensuring “FreeSync” appears:","Excludes web pages containing the specified term from results.","Example: To search for office-related content while excluding Microsoft:","The minus operator is particularly useful for filtering out common but\nunwanted terms from your search results."],"codeBlocks":["gpu +freesync","office -microsoft"]}
    - {"level":"H3","title":"Exact Matching","content":["Returns web pages containing exact matches to your query in the specified order.","Example: To find pages about Harry Potter with the exact phrase “order of the phoenix”:"],"codeBlocks":["harry potter \"order of the phoenix\""]}
    - {"level":"H2","title":"Logical Operators","content":["Logical operators allow you to combine and refine search operators for complex queries. These operators enable advanced search logic and must be written in uppercase.","Returns only web pages meeting all specified conditions. All criteria must be satisfied.","Example: To search for visa information in English from UK websites:","Returns web pages meeting any of the conditions. At least one criterion must be satisfied.","Example: To search for travel requirements for either Australia or New Zealand:","Returns web pages that do not meet the specified condition(s). Excludes results matching the criteria.","Example: To search for information about Brave Search while excluding brave.com:","Logical operators can be combined to create sophisticated search queries. For\nexample: coffee OR tea recipe NOT starbucks"],"codeBlocks":["visa loc:gb AND lang:en","travel requirements inpage:australia OR inpage:\"new zealand\"","brave search NOT site:brave.com"]}
    - {"level":"H3","title":"AND","content":["Returns only web pages meeting all specified conditions. All criteria must be satisfied.","Example: To search for visa information in English from UK websites:"],"codeBlocks":["visa loc:gb AND lang:en"]}
    - {"level":"H3","title":"OR","content":["Returns web pages meeting any of the conditions. At least one criterion must be satisfied.","Example: To search for travel requirements for either Australia or New Zealand:"],"codeBlocks":["travel requirements inpage:australia OR inpage:\"new zealand\""]}
    - {"level":"H3","title":"NOT","content":["Returns web pages that do not meet the specified condition(s). Excludes results matching the criteria.","Example: To search for information about Brave Search while excluding brave.com:","Logical operators can be combined to create sophisticated search queries. For\nexample: coffee OR tea recipe NOT starbucks"],"codeBlocks":["brave search NOT site:brave.com"]}
    - {"level":"H2","title":"Using Search Operators with the API","content":["Search operators work seamlessly with the Brave Search API. Simply include them in your query parameter:"],"codeBlocks":[]}
    - {"level":"H2","title":"Practical Examples","content":["Here are some real-world examples combining multiple operators:","Find recent academic papers about climate change in PDF format from educational institutions:","Search for cooking recipes in French from Canadian websites:","Find information about AI startups while excluding major tech companies:","Search for Python documentation on specific topics with exact terms:","Find news articles about electric vehicles from multiple specific sources:"],"codeBlocks":["climate change filetype:pdf site:edu intitle:2024","recettes cuisine loc:ca lang:fr","AI startup -google -microsoft -amazon -meta","python \"asyncio\" intitle:documentation site:docs.python.org","electric vehicles site:reuters.com OR site:bloomberg.com 2025"]}
    - {"level":"H3","title":"Academic Research","content":["Find recent academic papers about climate change in PDF format from educational institutions:"],"codeBlocks":["climate change filetype:pdf site:edu intitle:2024"]}
    - {"level":"H3","title":"Multilingual Content Discovery","content":["Search for cooking recipes in French from Canadian websites:"],"codeBlocks":["recettes cuisine loc:ca lang:fr"]}
    - {"level":"H3","title":"Competitive Analysis","content":["Find information about AI startups while excluding major tech companies:"],"codeBlocks":["AI startup -google -microsoft -amazon -meta"]}
    - {"level":"H3","title":"Technical Documentation","content":["Search for Python documentation on specific topics with exact terms:"],"codeBlocks":["python \"asyncio\" intitle:documentation site:docs.python.org"]}
    - {"level":"H3","title":"News Research","content":["Find news articles about electric vehicles from multiple specific sources:"],"codeBlocks":["electric vehicles site:reuters.com OR site:bloomberg.com 2025"]}
    - {"level":"H2","title":"Operator Reference Table","content":["OperatorPurposeExampleext:File extension filtermanual ext:pdffiletype:File type filterreport filetype:pdfintitle:Search in page titleintitle:guideinbody:Search in page bodyinbody:\"exact phrase\"inpage:Search in title or bodyinpage:keywordlang:Language filter (ISO 639-1)lang:esloc:Location filter (ISO 3166-1)loc:casite:Domain filtersite:example.com+Force inclusion+required-Exclude term-unwanted\"\"Exact phrase match\"exact phrase\"ANDLogical ANDterm1 AND term2ORLogical ORterm1 OR term2NOTLogical NOTterm NOT excluded"],"codeBlocks":[]}
    - {"level":"H2","title":"Limitations and Notes","content":["Search operators are experimental and in the early stages of development.\nBehavior and availability may change as we continue to improve the feature.","Keep in mind:","• Not all queries may return results when operators are used, especially with very restrictive combinations\n• Operator behavior may vary depending on the complexity of the query\n• Some operators may have overlapping functionality (like ext and filetype)\n• Logical operators must be written in uppercase (AND, OR, NOT)"],"codeBlocks":[]}
    - {"level":"H2","title":"Related Resources","content":["Web Search API Learn about the Web Search API and how to integrate it    Goggles Create custom search experiences with Goggles    API Reference Complete API documentation and parameters    Quickstart Guide Get started with your first search query"],"codeBlocks":[]}
    - {"level":"H2","title":"Web Search API","content":["Learn about the Web Search API and how to integrate it"],"codeBlocks":[]}
    - {"level":"H2","title":"Goggles","content":["Create custom search experiences with Goggles"],"codeBlocks":[]}
    - {"level":"H2","title":"API Reference","content":["Complete API documentation and parameters"],"codeBlocks":[]}
    - {"level":"H2","title":"Quickstart Guide","content":["Get started with your first search query"],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Operator","Purpose","Example"],"rows":[["ext:","File extension filter","manual ext:pdf"],["filetype:","File type filter","report filetype:pdf"],["intitle:","Search in page title","intitle:guide"],["inbody:","Search in page body","inbody:\"exact phrase\""],["inpage:","Search in title or body","inpage:keyword"],["lang:","Language filter (ISO 639-1)","lang:es"],["loc:","Location filter (ISO 3166-1)","loc:ca"],["site:","Domain filter","site:example.com"],["+","Force inclusion","+required"],["-","Exclude term","-unwanted"],["\"\"","Exact phrase match","\"exact phrase\""],["AND","Logical AND","term1 AND term2"],["OR","Logical OR","term1 OR term2"],["NOT","Logical NOT","term NOT excluded"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf+lang:en\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf+lang:en\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nResources\n\nLearn what search operators are and how to use them to refine and control your search results\n\nOverview\n\nSearch operators are special commands that you can add to your search queries to filter and refine results. They help you find exactly what you’re looking for by limiting and focusing your search with precision. You can place them anywhere in your query string to gain better control over the returned results.\n\nWhether you’re building a specialized search application, filtering results by file type, or narrowing down results to specific websites, search operators give you the power to create more targeted searches.\n\nKey Features\n\nPrecise Filtering\n\nNarrow down results by file type, location, language, and more\n\nFlexible Placement\n\nAdd operators anywhere in your query for natural query construction\n\nContent Targeting\n\nSearch within specific parts of web pages (title, body, or both)\n\nLogical Combinations\n\nCombine multiple operators with AND, OR, NOT for complex queries\n\nUse Cases\n\nSearch operators are perfect for:\n\nResearch Applications: Filter academic papers, PDFs, and documents by file type\n\nCompetitive Analysis: Monitor specific domains while excluding others\n\nMultilingual Search: Target content in specific languages and regions\n\nContent Discovery: Find exact phrases and specific keyword placements\n\nAdvanced Filtering: Build complex search logic with operator combinations\n\nBasic Search Operators\n\nFile Extension and Type\n\nReturns web pages with a specific file extension.\n\nExample: To find the Honda GX120 Owner’s manual in PDF format:\n\nfiletype\n\nReturns web pages created in the specified file type.\n\nExample: To find documentation about cognitive changes in PDF format:\n\nContent Location\n\nintitle\n\nReturns web pages containing the specified term in the page title.\n\nExample: To find SEO conference pages with “2023” in the title:\n\ninbody\n\nReturns web pages containing the specified term in the body of the page.\n\nExample: To find information about the Nvidia GeForce GTX 1080 Ti with “founders edition” in the body:\n\ninpage\n\nReturns web pages containing the specified term either in the title or in the body.\n\nExample: To find pages about the 2024 Oscars with “best costume design” anywhere on the page:\n\nLanguage and Location\n\nlang or language\n\nReturns web pages written in the specified language. The language code must be in ISO 639-1 two-letter format.\n\nExample: To find information about visas only in Spanish:\n\nCommon language codes:\n\nen - English\n\nes - Spanish\n\nfr - French\n\nde - German\n\nja - Japanese\n\nzh - Chinese\n\nloc or location\n\nReturns web pages from a specific country or region. The country code must be in ISO 3166-1 alpha-2 format.\n\nExample: To find Canadian web pages about Niagara Falls:\n\nCommon country codes:\n\nus - United States\n\ngb - United Kingdom\n\nca - Canada\n\nau - Australia\n\nde - Germany\n\nfr - France\n\nDomain Filtering\n\nReturns web pages from only a specific website or domain.\n\nExample: To find information about Goggles only on Brave pages:\n\nYou can also use subdomains (e.g., site:blog.example.com) or partial domains\n(e.g., site:example.com will include all subdomains).\n\nAdvanced Search Operators\n\nInclusion and Exclusion\n\n+ (Plus)\n\nForces the inclusion of a term in the title or body of the page. Ensures that the specified keyword appears in results.\n\nExample: To find information about FreeSync GPU technology, ensuring “FreeSync” appears:\n\n- (Minus)\n\nExcludes web pages containing the specified term from results.\n\nExample: To search for office-related content while excluding Microsoft:\n\nThe minus operator is particularly useful for filtering out common but\nunwanted terms from your search results.\n\nExact Matching\n\n\"\" (Quotation Marks)\n\nReturns web pages containing exact matches to your query in the specified order.\n\nExample: To find pages about Harry Potter with the exact phrase “order of the phoenix”:\n\nLogical Operators\n\nLogical operators allow you to combine and refine search operators for complex queries. These operators enable advanced search logic and must be written in uppercase.\n\nReturns only web pages meeting all specified conditions. All criteria must be satisfied.\n\nExample: To search for visa information in English from UK websites:\n\nReturns web pages meeting any of the conditions. At least one criterion must be satisfied.\n\nExample: To search for travel requirements for either Australia or New Zealand:\n\nReturns web pages that do not meet the specified condition(s). Excludes results matching the criteria.\n\nExample: To search for information about Brave Search while excluding brave.com:\n\nLogical operators can be combined to create sophisticated search queries. For\nexample: coffee OR tea recipe NOT starbucks\n\nUsing Search Operators with the API\n\nSearch operators work seamlessly with the Brave Search API. Simply include them in your query parameter:\n\nPython\n\nNode.js\n\nPractical Examples\n\nHere are some real-world examples combining multiple operators:\n\nAcademic Research\n\nFind recent academic papers about climate change in PDF format from educational institutions:\n\nMultilingual Content Discovery\n\nSearch for cooking recipes in French from Canadian websites:\n\nCompetitive Analysis\n\nFind information about AI startups while excluding major tech companies:\n\nTechnical Documentation\n\nSearch for Python documentation on specific topics with exact terms:\n\nNews Research\n\nFind news articles about electric vehicles from multiple specific sources:\n\nBest Practices\n\nUse multiple operators together to create highly targeted searches. Start\nwith broader operators like site or lang, then narrow down with content\noperators like intitle or inbody.\n\nWhen searching for specific terminology, product names, or phrases, wrap them\nin quotation marks to ensure exact matching. This is particularly useful for\ntechnical terms and proper nouns.\n\nExperiment with different operator combinations to find the optimal query for\nyour use case. Some operators work better together than others depending on\nyour search goal.\n\nWhen using operators in API calls, ensure special characters are properly URL\nencoded. Most HTTP libraries handle this automatically.\n\nBegin with basic queries and gradually add operators to refine results.\nThis iterative approach helps you understand which operators provide the\nmost value for your specific use case.\n\nOperator Reference Table\n\nLimitations and Notes\n\nSearch operators are experimental and in the early stages of development.\nBehavior and availability may change as we continue to improve the feature.\n\nKeep in mind:\n\nNot all queries may return results when operators are used, especially with very restrictive combinations\n\nOperator behavior may vary depending on the complexity of the query\n\nSome operators may have overlapping functionality (like ext and filetype)\n\nLogical operators must be written in uppercase (AND, OR, NOT)\n\nRelated Resources\n\nWeb Search API\n\nLearn about the Web Search API and how to integrate it\n\nCreate custom search experiences with Goggles\n\nAPI Reference\n\nComplete API documentation and parameters\n\nQuickstart Guide\n\nGet started with your first search query\n\nOn this page\n\nPrecise Filtering Narrow down results by file type, location, language, and more\n\nFlexible Placement Add operators anywhere in your query for natural query construction\n\nContent Targeting Search within specific parts of web pages (title, body, or both)\n\nLogical Combinations Combine multiple operators with AND, OR, NOT for complex queries\n\nWeb Search API Learn about the Web Search API and how to integrate it\n\nGoggles Create custom search experiences with Goggles\n\nAPI Reference Complete API documentation and parameters\n\nQuickstart Guide Get started with your first search query"
  suggestedFilename: "resources-search-operators"
---

# Search operators

## 源URL

https://api-dashboard.search.brave.com/documentation/resources/search-operators

## 描述

Search operators are special commands that you can add to your search queries to filter and refine results. They help you find exactly what you’re looking for by limiting and focusing your search with precision. You can place them anywhere in your query string to gain better control over the returned results.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf+lang:en`

## 代码示例

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf+lang:en" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

## 文档正文

Search operators are special commands that you can add to your search queries to filter and refine results. They help you find exactly what you’re looking for by limiting and focusing your search with precision. You can place them anywhere in your query string to gain better control over the returned results.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf+lang:en`

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

Learn what search operators are and how to use them to refine and control your search results

Overview

Search operators are special commands that you can add to your search queries to filter and refine results. They help you find exactly what you’re looking for by limiting and focusing your search with precision. You can place them anywhere in your query string to gain better control over the returned results.

Whether you’re building a specialized search application, filtering results by file type, or narrowing down results to specific websites, search operators give you the power to create more targeted searches.

Key Features

Precise Filtering

Narrow down results by file type, location, language, and more

Flexible Placement

Add operators anywhere in your query for natural query construction

Content Targeting

Search within specific parts of web pages (title, body, or both)

Logical Combinations

Combine multiple operators with AND, OR, NOT for complex queries

Use Cases

Search operators are perfect for:

Research Applications: Filter academic papers, PDFs, and documents by file type

Competitive Analysis: Monitor specific domains while excluding others

Multilingual Search: Target content in specific languages and regions

Content Discovery: Find exact phrases and specific keyword placements

Advanced Filtering: Build complex search logic with operator combinations

Basic Search Operators

File Extension and Type

Returns web pages with a specific file extension.

Example: To find the Honda GX120 Owner’s manual in PDF format:

filetype

Returns web pages created in the specified file type.

Example: To find documentation about cognitive changes in PDF format:

Content Location

intitle

Returns web pages containing the specified term in the page title.

Example: To find SEO conference pages with “2023” in the title:

inbody

Returns web pages containing the specified term in the body of the page.

Example: To find information about the Nvidia GeForce GTX 1080 Ti with “founders edition” in the body:

inpage

Returns web pages containing the specified term either in the title or in the body.

Example: To find pages about the 2024 Oscars with “best costume design” anywhere on the page:

Language and Location

lang or language

Returns web pages written in the specified language. The language code must be in ISO 639-1 two-letter format.

Example: To find information about visas only in Spanish:

Common language codes:

en - English

es - Spanish

fr - French

de - German

ja - Japanese

zh - Chinese

loc or location

Returns web pages from a specific country or region. The country code must be in ISO 3166-1 alpha-2 format.

Example: To find Canadian web pages about Niagara Falls:

Common country codes:

us - United States

gb - United Kingdom

ca - Canada

au - Australia

de - Germany

fr - France

Domain Filtering

Returns web pages from only a specific website or domain.

Example: To find information about Goggles only on Brave pages:

You can also use subdomains (e.g., site:blog.example.com) or partial domains
(e.g., site:example.com will include all subdomains).

Advanced Search Operators

Inclusion and Exclusion

+ (Plus)

Forces the inclusion of a term in the title or body of the page. Ensures that the specified keyword appears in results.

Example: To find information about FreeSync GPU technology, ensuring “FreeSync” appears:

- (Minus)

Excludes web pages containing the specified term from results.

Example: To search for office-related content while excluding Microsoft:

The minus operator is particularly useful for filtering out common but
unwanted terms from your search results.

Exact Matching

"" (Quotation Marks)

Returns web pages containing exact matches to your query in the specified order.

Example: To find pages about Harry Potter with the exact phrase “order of the phoenix”:

Logical Operators

Logical operators allow you to combine and refine search operators for complex queries. These operators enable advanced search logic and must be written in uppercase.

Returns only web pages meeting all specified conditions. All criteria must be satisfied.

Example: To search for visa information in English from UK websites:

Returns web pages meeting any of the conditions. At least one criterion must be satisfied.

Example: To search for travel requirements for either Australia or New Zealand:

Returns web pages that do not meet the specified condition(s). Excludes results matching the criteria.

Example: To search for information about Brave Search while excluding brave.com:

Logical operators can be combined to create sophisticated search queries. For
example: coff
