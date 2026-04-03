---
id: "url-78a855b7"
type: "api"
title: "Web search"
url: "https://api-dashboard.search.brave.com/documentation/services/web-search"
description: "Web Search provides access to our comprehensive index of web pages, enabling you to retrieve relevant results from across the internet. Our service crawls and indexes billions of web pages, ensuring fresh and accurate search results for your applications."
source: ""
tags: []
crawl_time: "2026-03-18T02:32:53.047Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search?q=machine+learning+tutorials&freshness=pw"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Web Search provides access to our comprehensive index of web pages, enabling you to retrieve relevant results from across the internet. Our service crawls and indexes billions of web pages, ensuring fresh and accurate search results for your applications."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["Comprehensive Index Search across billions of indexed web pages with fast, reliable results   Fresh Results Regularly updated index ensures you get the most current information   Local Enrichments Enhanced results with local business data and geographic context   Rich Data Enrichments 3rd party data integration for rich real-time results","Local enrichments and rich 3rd party data enrichments require the Search\nplan. View pricing to learn more."],"codeBlocks":[]}
    - {"level":"H2","title":"Comprehensive Index","content":["Search across billions of indexed web pages with fast, reliable results"],"codeBlocks":[]}
    - {"level":"H2","title":"Fresh Results","content":["Regularly updated index ensures you get the most current information"],"codeBlocks":[]}
    - {"level":"H2","title":"Local Enrichments","content":["Enhanced results with local business data and geographic context"],"codeBlocks":[]}
    - {"level":"H2","title":"Rich Data Enrichments","content":["3rd party data integration for rich real-time results"],"codeBlocks":[]}
    - {"level":"H2","title":"Web Search API Documentation","content":["View the complete API reference, including endpoints, parameters, and example\nrequests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Web Search is perfect for:","• Search Applications: Build custom search experiences for your users\n• Content Aggregation: Gather information from multiple web sources\n• Market Research: Track mentions, trends, and competitor activity\n• Data Enrichment: Supplement your data with web-sourced information"],"codeBlocks":[]}
    - {"level":"H2","title":"Freshness Filtering","content":["Web Search offers powerful date-based filtering to help you find the most relevant content:","• Last 24 Hours (pd): Get the latest updates and recent content\n• Last 7 Days (pw): Track weekly trends and recent discussions\n• Last 31 Days (pm): Monitor monthly developments\n• Last Year (py): Search content from the past year\n• Custom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)","Example request filtering for web pages from the past week:"],"codeBlocks":[]}
    - {"level":"H2","title":"Country and Language Targeting","content":["Customize your web search results by specifying:","• Country: Target results from specific countries using 2-character country codes\n• Search Language: Filter results by content language\n• UI Language: Set the preferred language for response metadata","Example request for German content from Germany:"],"codeBlocks":[]}
    - {"level":"H2","title":"Extra Snippets","content":["The extra snippets feature provides up to 5 additional excerpts per search result, giving you more context from each web page. This is particularly useful for:","• Comprehensive content preview before clicking through\n• Better relevance assessment for search applications\n• Enhanced user experience with richer result cards","To enable extra snippets, add the extra_snippets query parameter set to true:","When enabled, each result in the web.results array will include an additional extra_snippets property containing an array of alternative excerpts:"],"codeBlocks":["{\n  \"web\": {\n    \"results\": [\n      {\n        \"title\": \"Python Web Frameworks\",\n        \"url\": \"https://example.com/python-frameworks\",\n        \"description\": \"Main snippet text...\",\n        \"extra_snippets\": [\n          \"First additional excerpt from the page...\",\n          \"Second additional excerpt from the page...\",\n          \"Third additional excerpt from the page...\"\n        ]\n      }\n    ]\n  }\n}"]}
    - {"level":"H2","title":"Goggles Support","content":["Web Search supports Goggles, which allow you to apply custom re-ranking on top of search results. You can:","• Boost or demote specific websites and domains\n• Filter by custom criteria\n• Create personalized ranking algorithms","Goggles can be provided as a URL or inline definition, and multiple goggles can be combined."],"codeBlocks":[]}
    - {"level":"H2","title":"Search Operators","content":["Web Search supports search operators to refine your queries. These operators are included directly within the q query parameter itself, not as separate API parameters:","• Use quotes for exact phrase matching: \"climate change solutions\"\n• Exclude terms with minus: javascript -jquery\n• Site-specific searches: site:github.com rust tutorials\n• File type searches: filetype:pdf machine learning","For example, to search for PDF files about machine learning:"],"codeBlocks":[]}
    - {"level":"H2","title":"Pagination","content":["Efficiently paginate through web search results:","• count: Maximum number of results per page (max 20, default 20). The actual number of results returned may be less than count.\n• offset: Starting position for results (0-based, max 9)","Example request for page 2 with up to 20 results per page:","Rather than blindly iterating with increasing offset values, check the more_results_available field in the response to determine if additional pages exist. This field is located in the query object of the response:","Only request the next page if more_results_available is true. This prevents unnecessary API calls when no more results are available."],"codeBlocks":["{\n  \"query\": {\n    \"original\": \"open source projects\",\n    \"more_results_available\": true\n  }\n}"]}
    - {"level":"H3","title":"Best Practice: Check more_results_available","content":["Rather than blindly iterating with increasing offset values, check the more_results_available field in the response to determine if additional pages exist. This field is located in the query object of the response:","Only request the next page if more_results_available is true. This prevents unnecessary API calls when no more results are available."],"codeBlocks":["{\n  \"query\": {\n    \"original\": \"open source projects\",\n    \"more_results_available\": true\n  }\n}"]}
    - {"level":"H2","title":"Safe Search","content":["Control adult content filtering with the safesearch parameter:","• off: No filtering\n• moderate: Filter explicit content (default)\n• strict: Filter explicit and suggestive content"],"codeBlocks":[]}
    - {"level":"H2","title":"Local enrichments","content":["Local enrichments provide extra information about places of interest (POI), such as images and the websites where the POI is mentioned. The Local Search API is a separate endpoint from Web Search, requiring a two-step process (similar to the Summarizer API).","First, make a request to the web search endpoint with a location-based query:","If the query returns a list of locations, each location result includes an id field — a temporary identifier that can be used to retrieve extra information:","Use the id values to fetch detailed POI information from the Local Search API endpoints. The ids query parameter accepts up to 20 location IDs:","To fetch AI-generated descriptions for locations:","The Local POIs endpoint (/local/pois) supports the following parameters:","ParameterTypeDescriptionids (required)arrayLocation IDs from the web search response (max 20)search_langstringSearch language preference (ISO 639-1, default: en)ui_langstringUI language for response (e.g., en-US)unitsstringMeasurement units: metric or imperial","The Local Descriptions endpoint (/local/descriptions) accepts only the ids parameter (same format as above, max 20).","For complete API documentation, see the Local POIs API Reference and Local Descriptions API Reference.","Note that the id fields of POIs are ephemeral and will expire after approximately 8 hours. Do not store them for later use."],"codeBlocks":["{\n  \"locations\": {\n    \"results\": [\n      {\n        \"id\": \"1520066f3f39496780c5931d9f7b26a6\",\n        \"title\": \"Pangea Banquet Mediterranean Food\",\n        ...\n      },\n      {\n        \"id\": \"d00b153c719a427ea515f9eacf4853a2\",\n        \"title\": \"Park Mediterranean Grill\",\n        ...\n      },\n      {\n        \"id\": \"4b943b378725432aa29f019def0f0154\",\n        \"title\": \"The Halal Mediterranean Co.\",\n        ...\n      }\n    ]\n  }\n}"]}
    - {"level":"H3","title":"Step 1: Query Web Search for Locations","content":["First, make a request to the web search endpoint with a location-based query:","If the query returns a list of locations, each location result includes an id field — a temporary identifier that can be used to retrieve extra information:"],"codeBlocks":["{\n  \"locations\": {\n    \"results\": [\n      {\n        \"id\": \"1520066f3f39496780c5931d9f7b26a6\",\n        \"title\": \"Pangea Banquet Mediterranean Food\",\n        ...\n      },\n      {\n        \"id\": \"d00b153c719a427ea515f9eacf4853a2\",\n        \"title\": \"Park Mediterranean Grill\",\n        ...\n      },\n      {\n        \"id\": \"4b943b378725432aa29f019def0f0154\",\n        \"title\": \"The Halal Mediterranean Co.\",\n        ...\n      }\n    ]\n  }\n}"]}
    - {"level":"H3","title":"Step 2: Fetch Local POI Details","content":["Use the id values to fetch detailed POI information from the Local Search API endpoints. The ids query parameter accepts up to 20 location IDs:","To fetch AI-generated descriptions for locations:"],"codeBlocks":[]}
    - {"level":"H3","title":"Local POIs Parameters","content":["The Local POIs endpoint (/local/pois) supports the following parameters:","ParameterTypeDescriptionids (required)arrayLocation IDs from the web search response (max 20)search_langstringSearch language preference (ISO 639-1, default: en)ui_langstringUI language for response (e.g., en-US)unitsstringMeasurement units: metric or imperial"],"codeBlocks":[]}
    - {"level":"H3","title":"Local Descriptions Parameters","content":["The Local Descriptions endpoint (/local/descriptions) accepts only the ids parameter (same format as above, max 20).","For complete API documentation, see the Local POIs API Reference and Local Descriptions API Reference.","Note that the id fields of POIs are ephemeral and will expire after approximately 8 hours. Do not store them for later use."],"codeBlocks":[]}
    - {"level":"H2","title":"Rich Data Enrichments","content":["Rich Search API responses provide accurate, real-time information\nabout the intent of the query. This data is sourced from 3rd-party\nAPI providers and includes verticals such as sports, stocks, and\nweather.","A request must be made to the web search endpoint with the query parameter enable_rich_callback=1.\nAn example cURL request for the query weather in munich is given below.","The Web Search API response contains a rich field if the query is expected to return rich results. An example of the rich field is given below.","The rich field of Web Search API response contains a callback_key field which can be used to fetch the rich results. An example cURL request to fetch the rich results is given below.","The Rich Search API provides detailed information across multiple verticals, matching the query intent. Each result includes a type field (always set to rich) and a subtype field indicating the specific vertical.","Some of these providers will require attribution for showing this data.","Calculator results for mathematical expressions. Use this for queries involving arithmetic operations, complex calculations, and mathematical expressions.","Word definitions and meanings.","Data provided by Wordnik.","Unit conversion calculations and results. Convert between different measurement units (length, weight, volume, temperature, etc.).","Unix timestamp conversion results. Convert between Unix timestamps and human-readable date/time formats.","Package tracking information. Track shipments and delivery status from various carriers.","Stock market information and price data. Access real-time stock quotes and intraday changes.","Data provided by FMP.","Currency conversion results. Provides exchange rates and conversion between different currencies.","Data provided by Fixer.","Cryptocurrency information and pricing data. Get real-time prices, market data, and trends for digital currencies.","Data provided by CoinGecko.","Weather forecast and current conditions. Get detailed weather information including temperature, precipitation, wind, and extended forecasts.","Data provided by OpenWeatherMap.","American football scores, schedules, and statistics.","Supported Leagues:","• NFL (USA)\n• CFB (USA)","Data provided by Stats Perform.","Baseball scores, schedules, and statistics.","Supported Leagues:","• MLB (USA)","Data provided by API Sports.","Basketball scores, schedules, and statistics.","Supported Leagues:","• ABA League (Europe)\n• BBL: Basket Bundesliga (Germany)\n• NBA: National Basketball Association (US & Canada)\n• Liga ACB (Spain)\n• Eurobasket (Europe)\n• Euroleague (Europe)\n• NBL (Australia)\n• LNB (France)\n• WNBA (USA)\n• NBA-G (USA)\n• Korisliiga (Finland)\n• Basket League (Greece)\n• Lega A (Italy)\n• LKL (Lithuania)\n• LNBP (Mexico)\n• LEB Oro (Spain)\n• LEB Plata (Spain)\n• Super Ligi (Turkey)\n• BBL (United Kingdom)","Data provided by API Sports.","Cricket scores, schedules, and statistics.","Supported Leagues:","• IPL (India)\n• PSL (Pakistan)","Data provided by Stats Perform.","Football scores, schedules, and statistics.","Supported Leagues:","• Major League Soccer (USA)\n• English Premier League (UK)\n• Bundesliga (Germany)\n• La Liga (Spain)\n• Serie A (Italy)\n• UEFA Champions League (International)\n• UEFA Europa League (International)\n• UEFA European Championship (International)\n• FIFA World Cup (International)\n• FIFA Women’s World Cup (International)\n• CONMEBOL Copa America (International)\n• CONMEBOL Libertadores (International)\n• Ligue 1 (France)\n• Serie A (Brazil)\n• Serie B (Brazil)\n• Copa do Brasil (Brazil)\n• Primeira Liga (Portugal)\n• Primera Division (Argentina)\n• Tipp3 Bundesliga (Austria)\n• Primera A (Colombia)\n• NWSL (USA)\n• Liga MX (Mexico)\n• Primera Division (Chile)\n• Primera Division (Peru)\n• Saudi Arabia Pro League (Saudi Arabia)\n• Indian Super League (India)\n• Premier Division (Ireland)\n• Premier League (Malta)\n• Campeonato Paulista (Brazil)\n• Campeonato Paranaense (Brazil)\n• Campeonato Carioca (Brazil)\n• Campeonato Mineiro (Brazil)\n• Eredivisie (Netherlands)","Data provided by API Sports.","Ice hockey scores, schedules, and statistics.","Supported Leagues:","• NHL: National Hockey League (US & Canada)\n• Liiga (Finland)","Data provided by API Sports."],"codeBlocks":["{\n  \"rich\": {\n    \"type\": \"rich\",\n    \"hint\": {\n      \"vertical\": \"weather\",\n      \"callback_key\": \"86d06abffc884e9ea281a40f62e0a5a6\"\n    }\n  }\n}"]}
    - {"level":"H3","title":"Supported Rich Result Types","content":["The Rich Search API provides detailed information across multiple verticals, matching the query intent. Each result includes a type field (always set to rich) and a subtype field indicating the specific vertical.","Some of these providers will require attribution for showing this data.","Calculator results for mathematical expressions. Use this for queries involving arithmetic operations, complex calculations, and mathematical expressions.","Word definitions and meanings.","Data provided by Wordnik.","Unit conversion calculations and results. Convert between different measurement units (length, weight, volume, temperature, etc.).","Unix timestamp conversion results. Convert between Unix timestamps and human-readable date/time formats.","Package tracking information. Track shipments and delivery status from various carriers.","Stock market information and price data. Access real-time stock quotes and intraday changes.","Data provided by FMP.","Currency conversion results. Provides exchange rates and conversion between different currencies.","Data provided by Fixer.","Cryptocurrency information and pricing data. Get real-time prices, market data, and trends for digital currencies.","Data provided by CoinGecko.","Weather forecast and current conditions. Get detailed weather information including temperature, precipitation, wind, and extended forecasts.","Data provided by OpenWeatherMap.","American football scores, schedules, and statistics.","Supported Leagues:","• NFL (USA)\n• CFB (USA)","Data provided by Stats Perform.","Baseball scores, schedules, and statistics.","Supported Leagues:","• MLB (USA)","Data provided by API Sports.","Basketball scores, schedules, and statistics.","Supported Leagues:","• ABA League (Europe)\n• BBL: Basket Bundesliga (Germany)\n• NBA: National Basketball Association (US & Canada)\n• Liga ACB (Spain)\n• Eurobasket (Europe)\n• Euroleague (Europe)\n• NBL (Australia)\n• LNB (France)\n• WNBA (USA)\n• NBA-G (USA)\n• Korisliiga (Finland)\n• Basket League (Greece)\n• Lega A (Italy)\n• LKL (Lithuania)\n• LNBP (Mexico)\n• LEB Oro (Spain)\n• LEB Plata (Spain)\n• Super Ligi (Turkey)\n• BBL (United Kingdom)","Data provided by API Sports.","Cricket scores, schedules, and statistics.","Supported Leagues:","• IPL (India)\n• PSL (Pakistan)","Data provided by Stats Perform.","Football scores, schedules, and statistics.","Supported Leagues:","• Major League Soccer (USA)\n• English Premier League (UK)\n• Bundesliga (Germany)\n• La Liga (Spain)\n• Serie A (Italy)\n• UEFA Champions League (International)\n• UEFA Europa League (International)\n• UEFA European Championship (International)\n• FIFA World Cup (International)\n• FIFA Women’s World Cup (International)\n• CONMEBOL Copa America (International)\n• CONMEBOL Libertadores (International)\n• Ligue 1 (France)\n• Serie A (Brazil)\n• Serie B (Brazil)\n• Copa do Brasil (Brazil)\n• Primeira Liga (Portugal)\n• Primera Division (Argentina)\n• Tipp3 Bundesliga (Austria)\n• Primera A (Colombia)\n• NWSL (USA)\n• Liga MX (Mexico)\n• Primera Division (Chile)\n• Primera Division (Peru)\n• Saudi Arabia Pro League (Saudi Arabia)\n• Indian Super League (India)\n• Premier Division (Ireland)\n• Premier League (Malta)\n• Campeonato Paulista (Brazil)\n• Campeonato Paranaense (Brazil)\n• Campeonato Carioca (Brazil)\n• Campeonato Mineiro (Brazil)\n• Eredivisie (Netherlands)","Data provided by API Sports.","Ice hockey scores, schedules, and statistics.","Supported Leagues:","• NHL: National Hockey League (US & Canada)\n• Liiga (Finland)","Data provided by API Sports."],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["This changelog outlines all significant changes to the\nBrave Web Search API in chronological order.","• 2023-01-01 Add Brave Web Search API resource.\n• 2023-04-14 Change SearchResult restaurant property to location.\n• 2023-10-11 Add spellcheck flag.\n• 2024-06-11 Add Brave Local Search API resource.\n• 2025-02-20 Add Brave Rich Search API resource."],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Parameter","Type","Description"],"rows":[["ids (required)","array","Location IDs from the web search response (max 20)"],["search_lang","string","Search language preference (ISO 639-1, default: en)"],["ui_lang","string","UI language for response (e.g., en-US)"],["units","string","Measurement units: metric or imperial"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=machine+learning+tutorials&freshness=pw\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=machine+learning+tutorials&freshness=pw\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=nachhaltige+energie&country=DE&search_lang=de\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=nachhaltige+energie&country=DE&search_lang=de\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=python+web+frameworks&extra_snippets=true\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=python+web+frameworks&extra_snippets=true\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"web\": {\n    \"results\": [\n      {\n        \"title\": \"Python Web Frameworks\",\n        \"url\": \"https://example.com/python-frameworks\",\n        \"description\": \"Main snippet text...\",\n        \"extra_snippets\": [\n          \"First additional excerpt from the page...\",\n          \"Second additional excerpt from the page...\",\n          \"Third additional excerpt from the page...\"\n        ]\n      }\n    ]\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"web\": {\n    \"results\": [\n      {\n        \"title\": \"Python Web Frameworks\",\n        \"url\": \"https://example.com/python-frameworks\",\n        \"description\": \"Main snippet text...\",\n        \"extra_snippets\": [\n          \"First additional excerpt from the page...\",\n          \"Second additional excerpt from the page...\",\n          \"Third additional excerpt from the page...\"\n        ]\n      }\n    ]\n  }\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=machine+learning+filetype:pdf\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=open+source+projects&count=20&offset=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=open+source+projects&count=20&offset=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"query\": {\n    \"original\": \"open source projects\",\n    \"more_results_available\": true\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"query\": {\n    \"original\": \"open source projects\",\n    \"more_results_available\": true\n  }\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=greek+restaurants+in+san+francisco\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=greek+restaurants+in+san+francisco\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/pois?ids=1520066f3f39496780c5931d9f7b26a6&ids=d00b153c719a427ea515f9eacf4853a2\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/pois?ids=1520066f3f39496780c5931d9f7b26a6&ids=d00b153c719a427ea515f9eacf4853a2\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/descriptions?ids=1520066f3f39496780c5931d9f7b26a6&ids=d00b153c719a427ea515f9eacf4853a2\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/descriptions?ids=1520066f3f39496780c5931d9f7b26a6&ids=d00b153c719a427ea515f9eacf4853a2\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=weather+in+munich&enable_rich_callback=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=weather+in+munich&enable_rich_callback=1\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"rich\": {\n    \"type\": \"rich\",\n    \"hint\": {\n      \"vertical\": \"weather\",\n      \"callback_key\": \"86d06abffc884e9ea281a40f62e0a5a6\"\n    }\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"rich\": {\n    \"type\": \"rich\",\n    \"hint\": {\n      \"vertical\": \"weather\",\n      \"callback_key\": \"86d06abffc884e9ea281a40f62e0a5a6\"\n    }\n  }\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/rich?callback_key=86d06abffc884e9ea281a40f62e0a5a6\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/rich?callback_key=86d06abffc884e9ea281a40f62e0a5a6\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nSearch from a large index of web pages with optional local and rich data enrichments\n\nOverview\n\nWeb Search provides access to our comprehensive index of web pages, enabling you to retrieve relevant results from across the internet. Our service crawls and indexes billions of web pages, ensuring fresh and accurate search results for your applications.\n\nKey Features\n\nComprehensive Index\n\nSearch across billions of indexed web pages with fast, reliable results\n\nFresh Results\n\nRegularly updated index ensures you get the most current information\n\nLocal Enrichments\n\nEnhanced results with local business data and geographic context\n\nRich Data Enrichments\n\n3rd party data integration for rich real-time results\n\nLocal enrichments and rich 3rd party data enrichments require the Search\nplan. View pricing to learn more.\n\nAPI Reference\n\nWeb Search API Documentation\n\nView the complete API reference, including endpoints, parameters, and example\nrequests\n\nUse Cases\n\nWeb Search is perfect for:\n\nSearch Applications: Build custom search experiences for your users\n\nContent Aggregation: Gather information from multiple web sources\n\nMarket Research: Track mentions, trends, and competitor activity\n\nData Enrichment: Supplement your data with web-sourced information\n\nFreshness Filtering\n\nWeb Search offers powerful date-based filtering to help you find the most relevant content:\n\nLast 24 Hours (pd): Get the latest updates and recent content\n\nLast 7 Days (pw): Track weekly trends and recent discussions\n\nLast 31 Days (pm): Monitor monthly developments\n\nLast Year (py): Search content from the past year\n\nCustom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)\n\nExample request filtering for web pages from the past week:\n\nCountry and Language Targeting\n\nCustomize your web search results by specifying:\n\nCountry: Target results from specific countries using 2-character country codes\n\nSearch Language: Filter results by content language\n\nUI Language: Set the preferred language for response metadata\n\nExample request for German content from Germany:\n\nExtra Snippets\n\nThe extra snippets feature provides up to 5 additional excerpts per search result, giving you more context from each web page. This is particularly useful for:\n\nComprehensive content preview before clicking through\n\nBetter relevance assessment for search applications\n\nEnhanced user experience with richer result cards\n\nTo enable extra snippets, add the extra_snippets query parameter set to true:\n\nWhen enabled, each result in the web.results array will include an additional extra_snippets property containing an array of alternative excerpts:\n\nGoggles Support\n\nWeb Search supports Goggles, which allow you to apply custom re-ranking on top of search results. You can:\n\nBoost or demote specific websites and domains\n\nFilter by custom criteria\n\nCreate personalized ranking algorithms\n\nGoggles can be provided as a URL or inline definition, and multiple goggles can be combined.\n\nSearch Operators\n\nWeb Search supports search operators to refine your queries. These operators are included directly within the q query parameter itself, not as separate API parameters:\n\nUse quotes for exact phrase matching: \"climate change solutions\"\n\nExclude terms with minus: javascript -jquery\n\nSite-specific searches: site:github.com rust tutorials\n\nFile type searches: filetype:pdf machine learning\n\nFor example, to search for PDF files about machine learning:\n\nPagination\n\nEfficiently paginate through web search results:\n\ncount: Maximum number of results per page (max 20, default 20). The actual number of results returned may be less than count.\n\noffset: Starting position for results (0-based, max 9)\n\nExample request for page 2 with up to 20 results per page:\n\nBest Practice: Check more_results_available\n\nRather than blindly iterating with increasing offset values, check the more_results_available field in the response to determine if additional pages exist. This field is located in the query object of the response:\n\nOnly request the next page if more_results_available is true. This prevents unnecessary API calls when no more results are available.\n\nSafe Search\n\nControl adult content filtering with the safesearch parameter:\n\noff: No filtering\n\nmoderate: Filter explicit content (default)\n\nstrict: Filter explicit and suggestive content\n\nLocal enrichments\n\nLocal enrichments provide extra information about places of interest (POI), such as images and the websites where the POI is mentioned. The Local Search API is a separate endpoint from Web Search, requiring a two-step process (similar to the Summarizer API).\n\nStep 1: Query Web Search for Locations\n\nFirst, make a request to the web search endpoint with a location-based query:\n\nIf the query returns a list of locations, each location result includes an id field — a temporary identifier that can be used to retrieve extra information:\n\nStep 2: Fetch Local POI Details\n\nUse the id values to fetch detailed POI information from the Local Search API endpoints. The ids query parameter accepts up to 20 location IDs:\n\nTo fetch AI-generated descriptions for locations:\n\nLocal POIs Parameters\n\nThe Local POIs endpoint (/local/pois) supports the following parameters:\n\nLocal Descriptions Parameters\n\nThe Local Descriptions endpoint (/local/descriptions) accepts only the ids parameter (same format as above, max 20).\n\nFor complete API documentation, see the Local POIs API Reference and Local Descriptions API Reference.\n\nNote that the id fields of POIs are ephemeral and will expire after approximately 8 hours. Do not store them for later use.\n\nRich Search API responses provide accurate, real-time information\nabout the intent of the query. This data is sourced from 3rd-party\nAPI providers and includes verticals such as sports, stocks, and\nweather.\n\nA request must be made to the web search endpoint with the query parameter enable_rich_callback=1.\nAn example cURL request for the query weather in munich is given below.\n\nThe Web Search API response contains a rich field if the query is expected to return rich results. An example of the rich field is given below.\n\nThe rich field of Web Search API response contains a callback_key field which can be used to fetch the rich results. An example cURL request to fetch the rich results is given below.\n\nSupported Rich Result Types\n\nThe Rich Search API provides detailed information across multiple verticals, matching the query intent. Each result includes a type field (always set to rich) and a subtype field indicating the specific vertical.\n\nSome of these providers will require attribution for showing this data.\n\nCalculator\n\nCalculator results for mathematical expressions. Use this for queries involving arithmetic operations, complex calculations, and mathematical expressions.\n\nDefinitions\n\nWord definitions and meanings.\n\nData provided by Wordnik.\n\nUnit Conversion\n\nUnit conversion calculations and results. Convert between different measurement units (length, weight, volume, temperature, etc.).\n\nUnix Timestamp\n\nUnix timestamp conversion results. Convert between Unix timestamps and human-readable date/time formats.\n\nPackage Tracker\n\nPackage tracking information. Track shipments and delivery status from various carriers.\n\nStock market information and price data. Access real-time stock quotes and intraday changes.\n\nData provided by FMP.\n\nCurrency\n\nCurrency conversion results. Provides exchange rates and conversion between different currencies.\n\nData provided by Fixer.\n\nCryptocurrency\n\nCryptocurrency information and pricing data. Get real-time prices, market data, and trends for digital currencies.\n\nData provided by CoinGecko.\n\nWeather\n\nWeather forecast and current conditions. Get detailed weather information including temperature, precipitation, wind, and extended forecasts.\n\nData provided by OpenWeatherMap.\n\nAmerican Football\n\nAmerican football scores, schedules, and statistics.\n\nSupported Leagues:\n\nNFL (USA)\n\nCFB (USA)\n\nData provided by Stats Perform.\n\nBaseball\n\nBaseball scores, schedules, and statistics.\n\nMLB (USA)\n\nData provided by API Sports.\n\nBasketball\n\nBasketball scores, schedules, and statistics.\n\nABA League (Europe)\n\nBBL: Basket Bundesliga (Germany)\n\nNBA: National Basketball Association (US & Canada)\n\nLiga ACB (Spain)\n\nEurobasket (Europe)\n\nEuroleague (Europe)\n\nNBL (Australia)\n\nLNB (France)\n\nWNBA (USA)\n\nNBA-G (USA)\n\nKorisliiga (Finland)\n\nBasket League (Greece)\n\nLega A (Italy)\n\nLKL (Lithuania)\n\nLNBP (Mexico)\n\nLEB Oro (Spain)\n\nLEB Plata (Spain)\n\nSuper Ligi (Turkey)\n\nBBL (United Kingdom)\n\nCricket\n\nCricket scores, schedules, and statistics.\n\nIPL (India)\n\nPSL (Pakistan)\n\nFootball (Soccer)\n\nFootball scores, schedules, and statistics.\n\nMajor League Soccer (USA)\n\nEnglish Premier League (UK)\n\nBundesliga (Germany)\n\nLa Liga (Spain)\n\nSerie A (Italy)\n\nUEFA Champions League (International)\n\nUEFA Europa League (International)\n\nUEFA European Championship (International)\n\nFIFA World Cup (International)\n\nFIFA Women’s World Cup (International)\n\nCONMEBOL Copa America (International)\n\nCONMEBOL Libertadores (International)\n\nLigue 1 (France)\n\nSerie A (Brazil)\n\nSerie B (Brazil)\n\nCopa do Brasil (Brazil)\n\nPrimeira Liga (Portugal)\n\nPrimera Division (Argentina)\n\nTipp3 Bundesliga (Austria)\n\nPrimera A (Colombia)\n\nNWSL (USA)\n\nLiga MX (Mexico)\n\nPrimera Division (Chile)\n\nPrimera Division (Peru)\n\nSaudi Arabia Pro League (Saudi Arabia)\n\nIndian Super League (India)\n\nPremier Division (Ireland)\n\nPremier League (Malta)\n\nCampeonato Paulista (Brazil)\n\nCampeonato Paranaense (Brazil)\n\nCampeonato Carioca (Brazil)\n\nCampeonato Mineiro (Brazil)\n\nEredivisie (Netherlands)\n\nIce Hockey\n\nIce hockey scores, schedules, and statistics.\n\nNHL: National Hockey League (US & Canada)\n\nLiiga (Finland)\n\nChangelog\n\nThis changelog outlines all significant changes to the\nBrave Web Search API in chronological order.\n\n2023-01-01 Add Brave Web Search API resource.\n\n2023-04-14 Change SearchResult restaurant property to location.\n\n2023-10-11 Add spellcheck flag.\n\n2024-06-11 Add Brave Local Search API resource.\n\n2025-02-20 Add Brave Rich Search API resource.\n\nOn this page\n\nBest Practice: Check `more_results_available`\n\nComprehensive Index Search across billions of indexed web pages with fast, reliable results\n\nFresh Results Regularly updated index ensures you get the most current information\n\nLocal Enrichments Enhanced results with local business data and geographic context\n\nRich Data Enrichments 3rd party data integration for rich real-time results\n\nWeb Search API Documentation View the complete API reference, including endpoints, parameters, and example\nrequests"
  suggestedFilename: "services-web-search"
---

# Web search

## 源URL

https://api-dashboard.search.brave.com/documentation/services/web-search

## 描述

Web Search provides access to our comprehensive index of web pages, enabling you to retrieve relevant results from across the internet. Our service crawls and indexes billions of web pages, ensuring fresh and accurate search results for your applications.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search?q=machine+learning+tutorials&freshness=pw`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=machine+learning+tutorials&freshness=pw" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "web": {
    "results": [
      {
        "title": "Python Web Frameworks",
        "url": "https://example.com/python-frameworks",
        "description": "Main snippet text...",
        "extra_snippets": [
          "First additional excerpt from the page...",
          "Second additional excerpt from the page...",
          "Third additional excerpt from the page..."
        ]
      }
    ]
  }
}
```

### 示例 3 (json)

```json
{
  "query": {
    "original": "open source projects",
    "more_results_available": true
  }
}
```

### 示例 4 (bash)

```bash
curl "https://api.search.brave.com/res/v1/local/pois?ids=1520066f3f39496780c5931d9f7b26a6&ids=d00b153c719a427ea515f9eacf4853a2" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 5 (bash)

```bash
curl "https://api.search.brave.com/res/v1/local/descriptions?ids=1520066f3f39496780c5931d9f7b26a6&ids=d00b153c719a427ea515f9eacf4853a2" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 6 (json)

```json
{
  "rich": {
    "type": "rich",
    "hint": {
      "vertical": "weather",
      "callback_key": "86d06abffc884e9ea281a40f62e0a5a6"
    }
  }
}
```

### 示例 7 (bash)

```bash
curl "https://api.search.brave.com/res/v1/web/rich?callback_key=86d06abffc884e9ea281a40f62e0a5a6" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

## 文档正文

Web Search provides access to our comprehensive index of web pages, enabling you to retrieve relevant results from across the internet. Our service crawls and indexes billions of web pages, ensuring fresh and accurate search results for your applications.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search?q=machine+learning+tutorials&freshness=pw`

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

Search from a large index of web pages with optional local and rich data enrichments

Overview

Web Search provides access to our comprehensive index of web pages, enabling you to retrieve relevant results from across the internet. Our service crawls and indexes billions of web pages, ensuring fresh and accurate search results for your applications.

Key Features

Comprehensive Index

Search across billions of indexed web pages with fast, reliable results

Fresh Results

Regularly updated index ensures you get the most current information

Local Enrichments

Enhanced results with local business data and geographic context

Rich Data Enrichments

3rd party data integration for rich real-time results

Local enrichments and rich 3rd party data enrichments require the Search
plan. View pricing to learn more.

API Reference

Web Search API Documentation

View the complete API reference, including endpoints, parameters, and example
requests

Use Cases

Web Search is perfect for:

Search Applications: Build custom search experiences for your users

Content Aggregation: Gather information from multiple web sources

Market Research: Track mentions, trends, and competitor activity

Data Enrichment: Supplement your data with web-sourced information

Freshness Filtering

Web Search offers powerful date-based filtering to help you find the most relevant content:

Last 24 Hours (pd): Get the latest updates and recent content

Last 7 Days (pw): Track weekly trends and recent discussions

Last 31 Days (pm): Monitor monthly developments

Last Year (py): Search content from the past year

Custom Date Range: Specify exact timeframes (e.g., 2022-04-01to2022-07-30)

Example request filtering for web pages from the past week:

Country and Language Targeting

Customize your web search results by specifying:

Country: Target results from specific countries using 2-character country codes

Search Language: Filter results by content language

UI Language: Set the preferred language for response metadata

Example request for German content from Germany:

Extra Snippets

The extra snippets feature provides up to 5 additional excerpts per search result, giving you more context from each web page. This is particularly useful for:

Comprehensive content preview before clicking through

Better relevance assessment for search applications

Enhanced user experience with richer result cards

To enable extra snippets, add the extra_snippets query parameter set to true:

When enabled, each result in the web.results array will include an additional extra_snippets property containing an array of alternative excerpts:

Goggles Support

Web Search supports Goggles, which allow you to apply custom re-ranking on top of search results. You can:

Boost or demote specific websites and domains

Filter by custom criteria

Create personalized ranking algorithms

Goggles can be provided as a URL or inline definition, and multiple goggles can be combined.

Search Operators

Web Search supports search operators to refine your queries. These operators are included directly within the q query parameter itself, not as separate API parameters:

Use quotes for exact phrase matching: "climate change solutions"

Exclude terms with minus: javascript -jquery

Site-specific searches: site:github.com rust tutorials

File type searches: filetype:pdf machine learning

For example, to search for PDF files about machine learning:

Pagination

Efficiently paginate through web search results:

count: Maximum number of results per page (max 20, default 20). The actual number of results returned may be less than count.

offset: Starting position for results (0-based, max 9)

Example request for page 2 with up to 20 results per page:

Best Practice: Check more_results_available

Rather than blindly iterating with increasing offset values, check the more_results_available field in the response to determine if additional pages exist. This field is located in the query object of the response:

Only request the next page if more_results_available is true. This prevents unnecessary API calls when no more results are available.

Safe Search

Control adult content filtering with the safesearch parameter:

off: No filtering

moderate: Filter explicit content (default)

strict: Filter explicit and suggestive content

Local enrichments

Local enrichments provide extra information about places of interest (POI), such as images and the websites where the POI is mentioned. The Local Search API is a separate endpoint from Web Search, requiring a two-step process (similar to the Summarizer API).

Step 1: Query Web Search for Locations

First, make a request to the web
