---
id: "url-6e67619"
type: "api"
title: "LLM Context"
url: "https://api-dashboard.search.brave.com/documentation/services/llm-context"
description: "Brave LLM Context API delivers pre-extracted, relevance-scored web content\noptimized for grounding LLM responses in real-time search results. Unlike\ntraditional web search APIs that return links and snippets, LLM Context\nextracts the actual page content—text chunks, tables, code blocks, and\nstructured data so your LLM or AI agent can reason over it directly."
source: ""
tags: []
crawl_time: "2026-03-18T02:33:20.346Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/llm/context?q=tallest+mountains+in+the+world"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Brave LLM Context API delivers pre-extracted, relevance-scored web content\noptimized for grounding LLM responses in real-time search results. Unlike\ntraditional web search APIs that return links and snippets, LLM Context\nextracts the actual page content—text chunks, tables, code blocks, and\nstructured data so your LLM or AI agent can reason over it directly.","This makes it ideal for AI agents that need web access as a tool,\nRAG (Retrieval-Augmented Generation) pipelines, and any application that\nneeds to ground LLM output in fresh, verifiable web content with a single\nAPI call."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Pre-Extracted Content Get actual page content (text, tables, code) ready for LLM consumption—no\nscraping needed   Token Budget Control Fine-tune the amount of context with configurable token and URL limits   Relevance Filtering Adjustable threshold modes ensure only relevant content reaches your LLM   Goggles Support Control which sources ground your LLM using Brave’s unique Goggles\nre-ranking system   Local & POI Results Location-aware queries with point-of-interest and map data   Fast Single-Search Optimized for speed with a single search per request"],"codeBlocks":[]}
    - {"level":"H2","title":"Pre-Extracted Content","content":["Get actual page content (text, tables, code) ready for LLM consumption—no\nscraping needed"],"codeBlocks":[]}
    - {"level":"H2","title":"Token Budget Control","content":["Fine-tune the amount of context with configurable token and URL limits"],"codeBlocks":[]}
    - {"level":"H2","title":"Relevance Filtering","content":["Adjustable threshold modes ensure only relevant content reaches your LLM"],"codeBlocks":[]}
    - {"level":"H2","title":"Goggles Support","content":["Control which sources ground your LLM using Brave’s unique Goggles\nre-ranking system"],"codeBlocks":[]}
    - {"level":"H2","title":"Local & POI Results","content":["Location-aware queries with point-of-interest and map data"],"codeBlocks":[]}
    - {"level":"H2","title":"Fast Single-Search","content":["Optimized for speed with a single search per request"],"codeBlocks":[]}
    - {"level":"H2","title":"LLM Context API Documentation","content":["View the complete API reference, including parameters and response schemas"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["LLM Context is perfect for:","• AI Agents: Give your agent a web search tool that returns ready-to-use content in a single call\n• RAG Pipelines: Ground LLM responses in fresh, relevant web content\n• AI Assistants & Chatbots: Provide factual answers backed by real sources\n• Question Answering: Retrieve focused context for specific queries\n• Fact Checking: Verify claims against current web content\n• Content Research: Gather source material on any topic with one API call"],"codeBlocks":[]}
    - {"level":"H2","title":"Endpoint","content":["Authentication: Include your API key in the X-Subscription-Token header."],"codeBlocks":["GET https://api.search.brave.com/res/v1/llm/context\nPOST https://api.search.brave.com/res/v1/llm/context"]}
    - {"level":"H2","title":"Quick Start","content":["POST accepts the same query parameters as a JSON request body with Content-Type: application/json. This is useful for complex queries\nor when parameters exceed URL length limits."],"codeBlocks":[]}
    - {"level":"H3","title":"POST Request","content":["POST accepts the same query parameters as a JSON request body with Content-Type: application/json. This is useful for complex queries\nor when parameters exceed URL length limits."],"codeBlocks":[]}
    - {"level":"H2","title":"Parameters","content":["ParameterTypeDefaultRangeDescriptionqstringrequired1-400 chars, max 50 wordsThe search querycountrystringus2-char codeCountry for search resultssearch_langstringen2+ char codeLanguage preference for resultscountint201-50Maximum number of search results to considerfreshnessstring\"\"—Filter results by their freshness (see Freshness below)","ParameterTypeDefaultRangeDescriptionmaximum_number_of_urlsint201-50Maximum URLs in the responsemaximum_number_of_tokensint81921024-32768Approximate maximum tokens in contextmaximum_number_of_snippetsint501-100Maximum snippets across all URLsmaximum_number_of_tokens_per_urlint4096512-8192Maximum tokens per individual URLmaximum_number_of_snippets_per_urlint501-100Maximum snippets per individual URL","ParameterTypeDefaultOptionsDescriptioncontext_threshold_modestringbalancedstrict, balanced, lenient, disabledRelevance threshold for including contentenable_localboolnulltrue, false, nullEnable local recall for location-aware queries. When not set (null), auto-detects based on whether location headers are providedgogglesstring/listnull—Goggle URL or inline definition for custom re-ranking"],"codeBlocks":[]}
    - {"level":"H3","title":"Query Parameters","content":["ParameterTypeDefaultRangeDescriptionqstringrequired1-400 chars, max 50 wordsThe search querycountrystringus2-char codeCountry for search resultssearch_langstringen2+ char codeLanguage preference for resultscountint201-50Maximum number of search results to considerfreshnessstring\"\"—Filter results by their freshness (see Freshness below)"],"codeBlocks":[]}
    - {"level":"H3","title":"Context Size Parameters","content":["ParameterTypeDefaultRangeDescriptionmaximum_number_of_urlsint201-50Maximum URLs in the responsemaximum_number_of_tokensint81921024-32768Approximate maximum tokens in contextmaximum_number_of_snippetsint501-100Maximum snippets across all URLsmaximum_number_of_tokens_per_urlint4096512-8192Maximum tokens per individual URLmaximum_number_of_snippets_per_urlint501-100Maximum snippets per individual URL"],"codeBlocks":[]}
    - {"level":"H3","title":"Filtering & Local Parameters","content":["ParameterTypeDefaultOptionsDescriptioncontext_threshold_modestringbalancedstrict, balanced, lenient, disabledRelevance threshold for including contentenable_localboolnulltrue, false, nullEnable local recall for location-aware queries. When not set (null), auto-detects based on whether location headers are providedgogglesstring/listnull—Goggle URL or inline definition for custom re-ranking"],"codeBlocks":[]}
    - {"level":"H2","title":"Context Size Guidelines","content":["Adjust context parameters based on your task complexity. For agent tool\ncalls, smaller budgets keep responses fast; for deep research, increase them:","Task Typecountmax_tokensExampleSimple factual52048“What year was Python created?”Standard queries208192“Best practices for React hooks”Complex research5016384“Compare AI frameworks for production”","Larger context windows provide more information but increase latency and\ncost (of your inference). Start with the defaults and adjust based on your use case."],"codeBlocks":[]}
    - {"level":"H2","title":"Threshold Modes","content":["The context_threshold_mode parameter controls how aggressively the API filters content for relevance:","ModeBehaviorstrictHigher threshold — fewer but more relevant resultsbalancedDefault — good balance between coverage and relevancelenientLower threshold — more results, may include less relevant contentdisabledNo threshold filtering — return all extracted content"],"codeBlocks":[]}
    - {"level":"H2","title":"Freshness","content":["The freshness parameter filters results used for context by their freshness. The freshness of a page is determined by the most relevant date reported by the content, such as its published or last modified date.","ValueDescriptionpdPages aged 24 hours or lesspwPages aged 7 days or lesspmPages aged 31 days or lesspyPages aged 365 days or lessYYYY-MM-DDtoYYYY-MM-DDCustom date range, e.g. 2022-04-01to2022-07-30"],"codeBlocks":[]}
    - {"level":"H2","title":"Local Recall","content":["The enable_local parameter controls whether location-aware recall is used:","ValueBehaviornull (not set)Auto-detect — default, local recall is enabled automatically when any location header is providedtrueForce local — always use local recall, even without location headersfalseForce standard — always use standard web ranking, even when location headers are present","For most use cases, you can omit enable_local entirely and let the API\nauto-detect based on whether you provide location headers. Set it explicitly\nonly when you need to override the default behavior."],"codeBlocks":[]}
    - {"level":"H2","title":"Location-Aware Queries","content":["For local queries (restaurants, businesses, directions), provide location context via headers. Local recall will be enabled automatically when location headers are present, or you can set enable_local=true explicitly.","HeaderTypeDescriptionX-Loc-LatfloatLatitude (-90.0 to 90.0)X-Loc-LongfloatLongitude (-180.0 to 180.0)X-Loc-CitystringCity nameX-Loc-StatestringState/region code (ISO 3166-2)X-Loc-State-NamestringState/region nameX-Loc-Countrystring2-letter country codeX-Loc-Postal-CodestringPostal code","Not all headers are required. If you have coordinates (X-Loc-Lat and X-Loc-Long),\nthose alone are usually sufficient. Otherwise, provide whichever place-name headers\nyou have available (city, state, country, etc.).","Example using coordinates:","Example using place name:","Example with explicit enable_local=true (no location headers needed):","When local recall is active, the response may include poi (point of interest) and map fields in addition to the standard generic array."],"codeBlocks":[]}
    - {"level":"H2","title":"Goggles (Custom Source Ranking)","content":["Goggles let you tailor which sources ground your LLM to better match your use case. You can restrict results to trusted domains, exclude user-generated content, or boost authoritative sources.","Goggles can be provided as a URL pointing to a hosted goggle file, or as an inline definition passed directly in the goggles parameter. For example, to restrict results to specific documentation sites, use an inline goggle with site rules.","For detailed syntax and examples, see the Goggles documentation."],"codeBlocks":[]}
    - {"level":"H2","title":"Response Format","content":["The response contains extracted web content organized into grounding data (by content type) and sources metadata.","When local recall is active, the response may include POI and map data:","Snippets may contain plain text or JSON-serialized structured data\n(tables, schemas, code blocks). LLMs handle this mixed format well, but\nyou should be prepared for both when post-processing."],"codeBlocks":["{\n  \"grounding\": {\n    \"generic\": [\n      {\n        \"url\": \"https://example.com/page\",\n        \"title\": \"Page Title\",\n        \"snippets\": [\n          \"Relevant text chunk extracted from the page...\",\n          \"Another relevant passage from the same page...\"\n        ]\n      }\n    ],\n    \"map\": []\n  },\n  \"sources\": {\n    \"https://example.com/page\": {\n      \"title\": \"Page Title\",\n      \"hostname\": \"example.com\",\n      \"age\": [\"Monday, January 15, 2024\", \"2024-01-15\", \"380 days ago\"]\n    }\n  }\n}","{\n  \"grounding\": {\n    \"generic\": [...],\n    \"poi\": {\n      \"name\": \"Business Name\",\n      \"url\": \"https://business.com\",\n      \"title\": \"Title of business.com website\",\n      \"snippets\": [\"Business details and information...\"]\n    },\n    \"map\": [\n      {\n        \"name\": \"Place Name\",\n        \"url\": \"https://place.com\",\n        \"title\": \"Title of place.com website\",\n        \"snippets\": [\"Place information and details...\"]\n      }\n    ]\n  },\n  \"sources\": {\n    \"https://business.com\": {\n      \"title\": \"Business Name\",\n      \"hostname\": \"business.com\",\n      \"age\": null\n    }\n  }\n}"]}
    - {"level":"H3","title":"Standard Response","content":[],"codeBlocks":["{\n  \"grounding\": {\n    \"generic\": [\n      {\n        \"url\": \"https://example.com/page\",\n        \"title\": \"Page Title\",\n        \"snippets\": [\n          \"Relevant text chunk extracted from the page...\",\n          \"Another relevant passage from the same page...\"\n        ]\n      }\n    ],\n    \"map\": []\n  },\n  \"sources\": {\n    \"https://example.com/page\": {\n      \"title\": \"Page Title\",\n      \"hostname\": \"example.com\",\n      \"age\": [\"Monday, January 15, 2024\", \"2024-01-15\", \"380 days ago\"]\n    }\n  }\n}"]}
    - {"level":"H3","title":"Local Response (with enable_local)","content":["When local recall is active, the response may include POI and map data:"],"codeBlocks":["{\n  \"grounding\": {\n    \"generic\": [...],\n    \"poi\": {\n      \"name\": \"Business Name\",\n      \"url\": \"https://business.com\",\n      \"title\": \"Title of business.com website\",\n      \"snippets\": [\"Business details and information...\"]\n    },\n    \"map\": [\n      {\n        \"name\": \"Place Name\",\n        \"url\": \"https://place.com\",\n        \"title\": \"Title of place.com website\",\n        \"snippets\": [\"Place information and details...\"]\n      }\n    ]\n  },\n  \"sources\": {\n    \"https://business.com\": {\n      \"title\": \"Business Name\",\n      \"hostname\": \"business.com\",\n      \"age\": null\n    }\n  }\n}"]}
    - {"level":"H3","title":"Response Fields","content":["Snippets may contain plain text or JSON-serialized structured data\n(tables, schemas, code blocks). LLMs handle this mixed format well, but\nyou should be prepared for both when post-processing."],"codeBlocks":[]}
    - {"level":"H2","title":"LLM Context vs Answers","content":["Brave offers several complementary approaches for AI-powered search:","LLM Context Raw extracted content for your own LLM pipeline. Best for AI agents,\nRAG, and applications where you control the model.    Answers Direct AI answers using OpenAI-compatible endpoint. Best for chat\ninterfaces that need instant, grounded AI responses.","When to use LLM Context:","• Giving your AI agent a web search tool it can call autonomously\n• Building RAG pipelines with your own LLM\n• Need full control over how context is processed and presented\n• Want raw extracted content without AI-generated summaries\n• Optimizing for speed with single-search retrieval\n• Need fine-grained control over token budgets and source filtering","When to use Answers:","• Want end-to-end AI answers with citations\n• Need OpenAI SDK compatibility\n• Building conversational AI agents or chatbots with built-in search\n• Require research mode for thorough, multi-search answers","Learn more about Answers."],"codeBlocks":[]}
    - {"level":"H2","title":"LLM Context","content":["Raw extracted content for your own LLM pipeline. Best for AI agents,\nRAG, and applications where you control the model."],"codeBlocks":[]}
    - {"level":"H2","title":"Answers","content":["Direct AI answers using OpenAI-compatible endpoint. Best for chat\ninterfaces that need instant, grounded AI responses."],"codeBlocks":[]}
    - {"level":"H2","title":"Best Practices","content":["• Start with defaults (maximum_number_of_tokens=8192, count=20) for most queries\n• Reduce for simple factual lookups to save latency and cost (of your inference)\n• Increase for complex research tasks that benefit from more context","• Use Goggles to restrict context to trusted, authoritative sources\n• Set context_threshold_mode=strict when precision matters more than recall","• Set a 30-second timeout for requests\n• Handle empty grounding.generic arrays gracefully—this means no relevant content was found\n• Implement retry logic with exponential backoff for transient failures\n• Check rate limit headers and respect the 1-second sliding window","• Use the smallest count and maximum_number_of_tokens values that meet your needs\n• For local queries, provide as many location headers as possible for better results"],"codeBlocks":[]}
    - {"level":"H3","title":"Token Budget Tuning","content":["• Start with defaults (maximum_number_of_tokens=8192, count=20) for most queries\n• Reduce for simple factual lookups to save latency and cost (of your inference)\n• Increase for complex research tasks that benefit from more context"],"codeBlocks":[]}
    - {"level":"H3","title":"Source Quality","content":["• Use Goggles to restrict context to trusted, authoritative sources\n• Set context_threshold_mode=strict when precision matters more than recall"],"codeBlocks":[]}
    - {"level":"H3","title":"Error Handling","content":["• Set a 30-second timeout for requests\n• Handle empty grounding.generic arrays gracefully—this means no relevant content was found\n• Implement retry logic with exponential backoff for transient failures\n• Check rate limit headers and respect the 1-second sliding window"],"codeBlocks":[]}
    - {"level":"H3","title":"Performance","content":["• Use the smallest count and maximum_number_of_tokens values that meet your needs\n• For local queries, provide as many location headers as possible for better results"],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the Brave LLM Context API in chronological order.","• Launch Brave LLM Context API at /v1/llm/context\n• Support for both GET and POST methods\n• Single-search context retrieval with configurable token budgets\n• Support for Goggles, local/POI queries, and relevance threshold modes"],"codeBlocks":[]}
    - {"level":"H3","title":"2026-02-06","content":["• Launch Brave LLM Context API at /v1/llm/context\n• Support for both GET and POST methods\n• Single-search context retrieval with configurable token budgets\n• Support for Goggles, local/POI queries, and relevance threshold modes"],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Parameter","Type","Default","Range","Description"],"rows":[["q","string","required","1-400 chars, max 50 words","The search query"],["country","string","us","2-char code","Country for search results"],["search_lang","string","en","2+ char code","Language preference for results"],["count","int","20","1-50","Maximum number of search results to consider"],["freshness","string","\"\"","—","Filter results by their freshness (see Freshness below)"]]}
    - {"index":1,"headers":["Parameter","Type","Default","Range","Description"],"rows":[["maximum_number_of_urls","int","20","1-50","Maximum URLs in the response"],["maximum_number_of_tokens","int","8192","1024-32768","Approximate maximum tokens in context"],["maximum_number_of_snippets","int","50","1-100","Maximum snippets across all URLs"],["maximum_number_of_tokens_per_url","int","4096","512-8192","Maximum tokens per individual URL"],["maximum_number_of_snippets_per_url","int","50","1-100","Maximum snippets per individual URL"]]}
    - {"index":2,"headers":["Parameter","Type","Default","Options","Description"],"rows":[["context_threshold_mode","string","balanced","strict, balanced, lenient, disabled","Relevance threshold for including content"],["enable_local","bool","null","true, false, null","Enable local recall for location-aware queries. When not set (null), auto-detects based on whether location headers are provided"],["goggles","string/list","null","—","Goggle URL or inline definition for custom re-ranking"]]}
    - {"index":3,"headers":["Task Type","count","max_tokens","Example"],"rows":[["Simple factual","5","2048","“What year was Python created?”"],["Standard queries","20","8192","“Best practices for React hooks”"],["Complex research","50","16384","“Compare AI frameworks for production”"]]}
    - {"index":4,"headers":["Mode","Behavior"],"rows":[["strict","Higher threshold — fewer but more relevant results"],["balanced","Default — good balance between coverage and relevance"],["lenient","Lower threshold — more results, may include less relevant content"],["disabled","No threshold filtering — return all extracted content"]]}
    - {"index":5,"headers":["Value","Description"],"rows":[["pd","Pages aged 24 hours or less"],["pw","Pages aged 7 days or less"],["pm","Pages aged 31 days or less"],["py","Pages aged 365 days or less"],["YYYY-MM-DDtoYYYY-MM-DD","Custom date range, e.g. 2022-04-01to2022-07-30"]]}
    - {"index":6,"headers":["Value","Behavior"],"rows":[["null (not set)","Auto-detect — default, local recall is enabled automatically when any location header is provided"],["true","Force local — always use local recall, even without location headers"],["false","Force standard — always use standard web ranking, even when location headers are present"]]}
    - {"index":7,"headers":["Header","Type","Description"],"rows":[["X-Loc-Lat","float","Latitude (-90.0 to 90.0)"],["X-Loc-Long","float","Longitude (-180.0 to 180.0)"],["X-Loc-City","string","City name"],["X-Loc-State","string","State/region code (ISO 3166-2)"],["X-Loc-State-Name","string","State/region name"],["X-Loc-Country","string","2-letter country code"],["X-Loc-Postal-Code","string","Postal code"]]}
    - {"index":8,"headers":["Field","Type","Description"],"rows":[["grounding","object","Container for all grounding content by type"],["grounding.generic","array","Array of URL objects with extracted content (main grounding data)"],["grounding.generic[].url","string","Source URL"],["grounding.generic[].title","string","Page title"],["grounding.generic[].snippets","array","Extracted text chunks from the page relevant to the query"],["grounding.poi","object/null","Point of interest data (only with local recall enabled)"],["grounding.map","array","Map/place results (only with local recall enabled)"],["sources","object","Metadata for all referenced URLs, keyed by URL"],["sources[url].title","string","Page title"],["sources[url].hostname","string","Source hostname"],["sources[url].age","array/null","Page modification dates (when available)"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context?q=tallest+mountains+in+the+world\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context?q=tallest+mountains+in+the+world\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl -s --compressed -X POST \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"accept: application/json\" \\\n  -H \"Accept-Encoding: gzip\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"q\": \"tallest mountains in the world\"}'"}
    - {"type":"request","language":"bash","code":"curl -s --compressed -X POST \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"accept: application/json\" \\\n  -H \"Accept-Encoding: gzip\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"q\": \"tallest mountains in the world\"}'"}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -H \"X-Loc-Lat: 37.7749\" \\\n  -H \"X-Loc-Long: -122.4194\" \\\n  -G \\\n  --data-urlencode \"q=best coffee shops near me\""}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -H \"X-Loc-Lat: 37.7749\" \\\n  -H \"X-Loc-Long: -122.4194\" \\\n  -G \\\n  --data-urlencode \"q=best coffee shops near me\""}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -H \"X-Loc-City: San Francisco\" \\\n  -H \"X-Loc-State: CA\" \\\n  -H \"X-Loc-Country: US\" \\\n  -G \\\n  --data-urlencode \"q=best coffee shops near me\""}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -H \"X-Loc-City: San Francisco\" \\\n  -H \"X-Loc-State: CA\" \\\n  -H \"X-Loc-Country: US\" \\\n  -G \\\n  --data-urlencode \"q=best coffee shops near me\""}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -G \\\n  --data-urlencode \"q=best coffee shops in san francisco\" \\\n  --data-urlencode \"enable_local=true\""}
    - {"type":"request","language":"bash","code":"curl -X GET \"https://api.search.brave.com/res/v1/llm/context\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\" \\\n  -G \\\n  --data-urlencode \"q=best coffee shops in san francisco\" \\\n  --data-urlencode \"enable_local=true\""}
    - {"type":"response","language":"json","code":"{\n  \"grounding\": {\n    \"generic\": [\n      {\n        \"url\": \"https://example.com/page\",\n        \"title\": \"Page Title\",\n        \"snippets\": [\n          \"Relevant text chunk extracted from the page...\",\n          \"Another relevant passage from the same page...\"\n        ]\n      }\n    ],\n    \"map\": []\n  },\n  \"sources\": {\n    \"https://example.com/page\": {\n      \"title\": \"Page Title\",\n      \"hostname\": \"example.com\",\n      \"age\": [\"Monday, January 15, 2024\", \"2024-01-15\", \"380 days ago\"]\n    }\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"grounding\": {\n    \"generic\": [\n      {\n        \"url\": \"https://example.com/page\",\n        \"title\": \"Page Title\",\n        \"snippets\": [\n          \"Relevant text chunk extracted from the page...\",\n          \"Another relevant passage from the same page...\"\n        ]\n      }\n    ],\n    \"map\": []\n  },\n  \"sources\": {\n    \"https://example.com/page\": {\n      \"title\": \"Page Title\",\n      \"hostname\": \"example.com\",\n      \"age\": [\"Monday, January 15, 2024\", \"2024-01-15\", \"380 days ago\"]\n    }\n  }\n}"}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nPre-extracted web content optimized for AI agents, LLM grounding, and RAG pipelines\n\nOverview\n\nBrave LLM Context API delivers pre-extracted, relevance-scored web content\noptimized for grounding LLM responses in real-time search results. Unlike\ntraditional web search APIs that return links and snippets, LLM Context\nextracts the actual page content—text chunks, tables, code blocks, and\nstructured data so your LLM or AI agent can reason over it directly.\n\nThis makes it ideal for AI agents that need web access as a tool,\nRAG (Retrieval-Augmented Generation) pipelines, and any application that\nneeds to ground LLM output in fresh, verifiable web content with a single\nAPI call.\n\nKey Features\n\nPre-Extracted Content\n\nGet actual page content (text, tables, code) ready for LLM consumption—no\nscraping needed\n\nToken Budget Control\n\nFine-tune the amount of context with configurable token and URL limits\n\nRelevance Filtering\n\nAdjustable threshold modes ensure only relevant content reaches your LLM\n\nGoggles Support\n\nControl which sources ground your LLM using Brave’s unique Goggles\nre-ranking system\n\nLocal & POI Results\n\nLocation-aware queries with point-of-interest and map data\n\nFast Single-Search\n\nOptimized for speed with a single search per request\n\nAPI Reference\n\nLLM Context API Documentation\n\nView the complete API reference, including parameters and response schemas\n\nUse Cases\n\nLLM Context is perfect for:\n\nAI Agents: Give your agent a web search tool that returns ready-to-use content in a single call\n\nRAG Pipelines: Ground LLM responses in fresh, relevant web content\n\nAI Assistants & Chatbots: Provide factual answers backed by real sources\n\nQuestion Answering: Retrieve focused context for specific queries\n\nFact Checking: Verify claims against current web content\n\nContent Research: Gather source material on any topic with one API call\n\nEndpoint\n\nAuthentication: Include your API key in the X-Subscription-Token header.\n\nQuick Start\n\nGET Request\n\nPOST Request\n\nPOST accepts the same query parameters as a JSON request body with Content-Type: application/json. This is useful for complex queries\nor when parameters exceed URL length limits.\n\nParameters\n\nQuery Parameters\n\nContext Size Parameters\n\nFiltering & Local Parameters\n\nContext Size Guidelines\n\nAdjust context parameters based on your task complexity. For agent tool\ncalls, smaller budgets keep responses fast; for deep research, increase them:\n\nLarger context windows provide more information but increase latency and\ncost (of your inference). Start with the defaults and adjust based on your use case.\n\nThreshold Modes\n\nThe context_threshold_mode parameter controls how aggressively the API filters content for relevance:\n\nFreshness\n\nThe freshness parameter filters results used for context by their freshness. The freshness of a page is determined by the most relevant date reported by the content, such as its published or last modified date.\n\nLocal Recall\n\nThe enable_local parameter controls whether location-aware recall is used:\n\nFor most use cases, you can omit enable_local entirely and let the API\nauto-detect based on whether you provide location headers. Set it explicitly\nonly when you need to override the default behavior.\n\nLocation-Aware Queries\n\nFor local queries (restaurants, businesses, directions), provide location context via headers. Local recall will be enabled automatically when location headers are present, or you can set enable_local=true explicitly.\n\nNot all headers are required. If you have coordinates (X-Loc-Lat and X-Loc-Long),\nthose alone are usually sufficient. Otherwise, provide whichever place-name headers\nyou have available (city, state, country, etc.).\n\nExample using coordinates:\n\nExample using place name:\n\nExample with explicit enable_local=true (no location headers needed):\n\nWhen local recall is active, the response may include poi (point of interest) and map fields in addition to the standard generic array.\n\nGoggles (Custom Source Ranking)\n\nGoggles let you tailor which sources ground your LLM to better match your use case. You can restrict results to trusted domains, exclude user-generated content, or boost authoritative sources.\n\nGoggles can be provided as a URL pointing to a hosted goggle file, or as an inline definition passed directly in the goggles parameter. For example, to restrict results to specific documentation sites, use an inline goggle with site rules.\n\nFor detailed syntax and examples, see the Goggles documentation.\n\nResponse Format\n\nThe response contains extracted web content organized into grounding data (by content type) and sources metadata.\n\nStandard Response\n\nLocal Response (with enable_local)\n\nWhen local recall is active, the response may include POI and map data:\n\nResponse Fields\n\nSnippets may contain plain text or JSON-serialized structured data\n(tables, schemas, code blocks). LLMs handle this mixed format well, but\nyou should be prepared for both when post-processing.\n\nLLM Context vs Answers\n\nBrave offers several complementary approaches for AI-powered search:\n\nLLM Context\n\nRaw extracted content for your own LLM pipeline. Best for AI agents,\nRAG, and applications where you control the model.\n\nDirect AI answers using OpenAI-compatible endpoint. Best for chat\ninterfaces that need instant, grounded AI responses.\n\nWhen to use LLM Context:\n\nGiving your AI agent a web search tool it can call autonomously\n\nBuilding RAG pipelines with your own LLM\n\nNeed full control over how context is processed and presented\n\nWant raw extracted content without AI-generated summaries\n\nOptimizing for speed with single-search retrieval\n\nNeed fine-grained control over token budgets and source filtering\n\nWhen to use Answers:\n\nWant end-to-end AI answers with citations\n\nNeed OpenAI SDK compatibility\n\nBuilding conversational AI agents or chatbots with built-in search\n\nRequire research mode for thorough, multi-search answers\n\nLearn more about Answers.\n\nBest Practices\n\nToken Budget Tuning\n\nStart with defaults (maximum_number_of_tokens=8192, count=20) for most queries\n\nReduce for simple factual lookups to save latency and cost (of your inference)\n\nIncrease for complex research tasks that benefit from more context\n\nSource Quality\n\nUse Goggles to restrict context to trusted, authoritative sources\n\nSet context_threshold_mode=strict when precision matters more than recall\n\nError Handling\n\nSet a 30-second timeout for requests\n\nHandle empty grounding.generic arrays gracefully—this means no relevant content was found\n\nImplement retry logic with exponential backoff for transient failures\n\nCheck rate limit headers and respect the 1-second sliding window\n\nPerformance\n\nUse the smallest count and maximum_number_of_tokens values that meet your needs\n\nFor local queries, provide as many location headers as possible for better results\n\nChangelog\n\nThis changelog outlines all significant changes to the Brave LLM Context API in chronological order.\n\n2026-02-06\n\nLaunch Brave LLM Context API at /v1/llm/context\n\nSupport for both GET and POST methods\n\nSingle-search context retrieval with configurable token budgets\n\nSupport for Goggles, local/POI queries, and relevance threshold modes\n\nOn this page\n\nLocal Response (with `enable_local`)\n\nPre-Extracted Content Get actual page content (text, tables, code) ready for LLM consumption—no\nscraping needed\n\nToken Budget Control Fine-tune the amount of context with configurable token and URL limits\n\nRelevance Filtering Adjustable threshold modes ensure only relevant content reaches your LLM\n\nGoggles Support Control which sources ground your LLM using Brave’s unique Goggles\nre-ranking system\n\nLocal & POI Results Location-aware queries with point-of-interest and map data\n\nFast Single-Search Optimized for speed with a single search per request\n\nLLM Context API Documentation View the complete API reference, including parameters and response schemas\n\nLLM Context Raw extracted content for your own LLM pipeline. Best for AI agents,\nRAG, and applications where you control the model.\n\nAnswers Direct AI answers using OpenAI-compatible endpoint. Best for chat\ninterfaces that need instant, grounded AI responses."
  suggestedFilename: "services-llm-context"
---

# LLM Context

## 源URL

https://api-dashboard.search.brave.com/documentation/services/llm-context

## 描述

Brave LLM Context API delivers pre-extracted, relevance-scored web content
optimized for grounding LLM responses in real-time search results. Unlike
traditional web search APIs that return links and snippets, LLM Context
extracts the actual page content—text chunks, tables, code blocks, and
structured data so your LLM or AI agent can reason over it directly.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/llm/context?q=tallest+mountains+in+the+world`

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET "https://api.search.brave.com/res/v1/llm/context?q=tallest+mountains+in+the+world" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (bash)

```bash
curl -s --compressed -X POST "https://api.search.brave.com/res/v1/llm/context" \
  -H "accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"q": "tallest mountains in the world"}'
```

### 示例 3 (json)

```json
{
  "grounding": {
    "generic": [
      {
        "url": "https://example.com/page",
        "title": "Page Title",
        "snippets": [
          "Relevant text chunk extracted from the page...",
          "Another relevant passage from the same page..."
        ]
      }
    ],
    "map": []
  },
  "sources": {
    "https://example.com/page": {
      "title": "Page Title",
      "hostname": "example.com",
      "age": ["Monday, January 15, 2024", "2024-01-15", "380 days ago"]
    }
  }
}
```

## 文档正文

Brave LLM Context API delivers pre-extracted, relevance-scored web content
optimized for grounding LLM responses in real-time search results. Unlike
traditional web search APIs that return links and snippets, LLM Context
extracts the actual page content—text chunks, tables, code blocks, and
structured data so your LLM or AI agent can reason over it directly.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/llm/context?q=tallest+mountains+in+the+world`

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

Pre-extracted web content optimized for AI agents, LLM grounding, and RAG pipelines

Overview

Brave LLM Context API delivers pre-extracted, relevance-scored web content
optimized for grounding LLM responses in real-time search results. Unlike
traditional web search APIs that return links and snippets, LLM Context
extracts the actual page content—text chunks, tables, code blocks, and
structured data so your LLM or AI agent can reason over it directly.

This makes it ideal for AI agents that need web access as a tool,
RAG (Retrieval-Augmented Generation) pipelines, and any application that
needs to ground LLM output in fresh, verifiable web content with a single
API call.

Key Features

Pre-Extracted Content

Get actual page content (text, tables, code) ready for LLM consumption—no
scraping needed

Token Budget Control

Fine-tune the amount of context with configurable token and URL limits

Relevance Filtering

Adjustable threshold modes ensure only relevant content reaches your LLM

Goggles Support

Control which sources ground your LLM using Brave’s unique Goggles
re-ranking system

Local & POI Results

Location-aware queries with point-of-interest and map data

Fast Single-Search

Optimized for speed with a single search per request

API Reference

LLM Context API Documentation

View the complete API reference, including parameters and response schemas

Use Cases

LLM Context is perfect for:

AI Agents: Give your agent a web search tool that returns ready-to-use content in a single call

RAG Pipelines: Ground LLM responses in fresh, relevant web content

AI Assistants & Chatbots: Provide factual answers backed by real sources

Question Answering: Retrieve focused context for specific queries

Fact Checking: Verify claims against current web content

Content Research: Gather source material on any topic with one API call

Endpoint

Authentication: Include your API key in the X-Subscription-Token header.

Quick Start

GET Request

POST Request

POST accepts the same query parameters as a JSON request body with Content-Type: application/json. This is useful for complex queries
or when parameters exceed URL length limits.

Parameters

Query Parameters

Context Size Parameters

Filtering & Local Parameters

Context Size Guidelines

Adjust context parameters based on your task complexity. For agent tool
calls, smaller budgets keep responses fast; for deep research, increase them:

Larger context windows provide more information but increase latency and
cost (of your inference). Start with the defaults and adjust based on your use case.

Threshold Modes

The context_threshold_mode parameter controls how aggressively the API filters content for relevance:

Freshness

The freshness parameter filters results used for context by their freshness. The freshness of a page is determined by the most relevant date reported by the content, such as its published or last modified date.

Local Recall

The enable_local parameter controls whether location-aware recall is used:

For most use cases, you can omit enable_local entirely and let the API
auto-detect based on whether you provide location headers. Set it explicitly
only when you need to override the default behavior.

Location-Aware Queries

For local queries (restaurants, businesses, directions), provide location context via headers. Local recall will be enabled automatically when location headers are present, or you can set enable_local=true explicitly.

Not all headers are required. If you have coordinates (X-Loc-Lat and X-Loc-Long),
those alone are usually sufficient. Otherwise, provide whichever place-name headers
you have available (city, state, country, etc.).

Example using coordinates:

Example using place name:

Example with explicit enable_local=true (no location headers needed):

When local recall is active, the response may include poi (point of interest) and map fields in addition to the standard generic array.

Goggles (Custom Source Ranking)

Goggles let you tailor which sources ground your LLM to better match your use case. You can restrict results to trusted domains, exclude user-generated content, or boost authoritative sources.

Goggles can be provided as a URL pointing to a hosted goggle file, or as an inline definition passed directly in the goggles parameter. For example, to restrict results to specific documentation sites, use an inline goggle with site rules.

For detailed syntax and examples, see the Goggles documentation.

Response Format

The response contains extracted web content organized into grounding data (by content type) and sources metadata.

Standard Response

Local Response (with enable_local)

When local r
