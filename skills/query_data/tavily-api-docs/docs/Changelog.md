---
id: "url-2bf5a857"
type: "website"
title: "Changelog"
url: "https://docs.tavily.com/changelog"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:16:22.090Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":1,"text":"Changelog"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent: []
  paragraphs:
    - "Enterprise API key management endpoints"
    - "March 2026"
    - "Exact match parameter"
    - "February 2026"
    - "Project tracking with X-Project-ID header"
    - "January 2026"
    - "New search_depth options fast and ultra-fast (BETA)"
    - "December 2025"
    - "Intent Based Extraction"
    - "December 2025"
    - "Include usage parameter"
    - "December 2025"
    - "Vercel AI SDK v5 integration"
    - "November 2025"
    - "Crawl & Map timeout parameter"
    - "November 2025"
    - "New team roles & permissions"
    - "August 2025"
    - "Extract timeout parameter"
    - "August 2025"
    - "Start date & end date Parameters"
    - "July 2025"
    - "Usage dashboard"
    - "July 2025"
    - "Include favicon parameter"
    - "June 2025"
    - "Auto parameters"
    - "June 2025"
    - "Usage endpoint"
    - "May 2025"
    - "Country parameter"
    - "May 2025"
    - "Boost search results from a specific country."
    - "Make & n8n integrations"
    - "May 2025"
    - "Integrate Tavily with n8n to enhance your workflows with real-time web search and content extraction—without writing code. With Tavily’s powerful search and extraction capabilities, you can seamlessly integrate up-to-date online information into your n8n automations."
    - "With Tavily’s powerful search and content extraction capabilities, you can seamlessly integrate real-time online information into your Make workflows and automations."
    - "Markdown format"
    - "May 2025"
    - "Advanced search & chunks per source"
    - "April 2025"
    - "Tavily crawl (BETA)"
    - "April 2025"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Changelog](https://docs.tavily.com/changelog)"]}
    - {"type":"ul","items":["Enterprise users can programmatically manage API keys via dedicated endpoints.","[POST /generate-keys](https://docs.tavily.com/documentation/enterprise/generate-keys) — Generate new API keys for your organization.","[POST /deactivate-keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys) — Deactivate existing API keys.","[GET /key-info](https://docs.tavily.com/documentation/enterprise/key-info) — Retrieve information about an existing API key.","These endpoints are available on the Enterprise plan only. [Talk to an expert](https://enterprise.tavily.com/) to learn more."]}
    - {"type":"ul","items":["Use exact_match to ensure that only search results containing the exact quoted phrase(s) in your query are returned, bypassing synonyms or semantic variations.","Wrap target phrases in quotes within your query (e.g. “John Smith” CEO Acme Corp).","Type:boolean","Default:false","Because this narrows retrieval, it may return fewer results or empty result fields when no exact matches are found.","Best suited for due diligence, data enrichment, and legal/compliance use cases where verbatim matches are required."]}
    - {"type":"ul","items":["You can now attach a Project ID to your API requests to organize and track usage by project. This is useful when a single API key is used across multiple projects or applications.","HTTP Header: Add X-Project-ID: your-project-id to any API request","Python SDK: Pass project_id=“your-project-id” when instantiating the client, or set the TAVILY_PROJECT environment variable","JavaScript SDK: Pass projectId: “your-project-id” when instantiating the client, or set the TAVILY_PROJECT environment variable","An API key can be associated with multiple projects","Filter requests by project in the [/usage endpoint](https://docs.tavily.com/documentation/api-reference/endpoint/usage) and platform usage dashboard to keep track of where requests originate from"]}
    - {"type":"ul","items":["fast (BETA)Optimized for low latency while maintaining high relevance to the user queryCost: 1 API Credit","Optimized for low latency while maintaining high relevance to the user query","Cost: 1 API Credit","ultra-fast (BETA)Optimized strictly for latencyCost: 1 API Credit","Optimized strictly for latency","Cost: 1 API Credit"]}
    - {"type":"ul","items":["Optimized for low latency while maintaining high relevance to the user query","Cost: 1 API Credit"]}
    - {"type":"ul","items":["Optimized strictly for latency","Cost: 1 API Credit"]}
    - {"type":"ul","items":["query (Extract)Type: stringUser intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query.","Type: string","User intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query.","chunks_per_source (Extract & Crawl)Type: integerRange: 1 to 5Default: 3Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length.Chunks will appear in the raw_content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.Available only when query is provided (Extract) or instructions are provided (Crawl).","Type: integer","Range: 1 to 5","Default: 3","Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.","Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length.","Chunks will appear in the raw_content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.","Available only when query is provided (Extract) or instructions are provided (Crawl)."]}
    - {"type":"ul","items":["Type: string","User intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query."]}
    - {"type":"ul","items":["Type: integer","Range: 1 to 5","Default: 3","Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.","Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length.","Chunks will appear in the raw_content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.","Available only when query is provided (Extract) or instructions are provided (Crawl)."]}
    - {"type":"ul","items":["You can now include credit usage information in the API response for the [Search](https://docs.tavily.com/documentation/api-reference/endpoint/search#body-include-usage), [Extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract#body-include-usage), [Crawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl#body-include-usage), and [Map](https://docs.tavily.com/documentation/api-reference/endpoint/map#body-include-usage) endpoints.","Set the include_usage parameter to true to receive credit usage information in the API response.","Type:boolean","Default:false","When enabled, the response includes a usage object with credits information, making it easy to track API credit consumption for each request.","Note: The value may be 0 if the total successful calls have not yet reached the minimum threshold. See our [Credits & Pricing documentation](https://docs.tavily.com/documentation/api-credits) for details."]}
    - {"type":"ul","items":["We’ve released a new [@tavily/ai-sdk](https://www.npmjs.com/package/@tavily/ai-sdk) package that provides pre-built AI SDK tools for Vercel’s AI SDK v5.","Easily add real-time web search, content extraction, intelligent crawling, and site mapping to your AI SDK project with ready-to-use tools.","Available Tools: tavilySearch, tavilyExtract, tavilyCrawl, and tavilyMap","Full TypeScript support with proper type definitions and seamless integration with Vercel AI SDK v5.","Check out our [integration guide](https://docs.tavily.com/documentation/integrations/vercel) to get started."]}
    - {"type":"ul","items":["You can now specify a custom timeout for the [Crawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl) and [Map](https://docs.tavily.com/documentation/api-reference/endpoint/map) endpoints to control how long to wait for the operation before timing out.","Type:float","Range: Between 10 and 150 seconds","Default: 150 seconds","This gives you fine-grained control over crawl and map operation timeouts, allowing you to balance between reliability and speed based on your specific use case."]}
    - {"type":"ul","items":["OwnerFull access to all SettingsAccess and ownership of the Billing account","Full access to all Settings","Access and ownership of the Billing account","AdminFull access to Settings except ownership transferNo access to Billing","Full access to Settings except ownership transfer","No access to Billing","MemberLimited Settings access (view members only)No access to Billing","Limited Settings access (view members only)","No access to Billing"]}
    - {"type":"ul","items":["Full access to all Settings","Access and ownership of the Billing account"]}
    - {"type":"ul","items":["Full access to Settings except ownership transfer","No access to Billing"]}
    - {"type":"ul","items":["Limited Settings access (view members only)","No access to Billing"]}
    - {"type":"ul","items":["You can now specify a custom timeout for the [Extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract) endpoint to control how long to wait for URL extraction before timing out.","Type: number (float)","Range: Between 1.0 and 60.0 seconds","Default behavior: If not specified, automatic timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction.","This gives you fine-grained control over extraction timeouts, allowing you to balance between reliability and speed based on your specific use case."]}
    - {"type":"ul","items":["You can now use both the start_date and end_date parameters in the [Search](https://docs.tavily.com/documentation/api-reference/endpoint/search) endpoints.","start_date will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.","end_date will return all results before the specified end date. Required to be written in the format YYYY-MM-DD.","Set start_date to 2025-01-01 and end_date to 2025-04-01 to reiceive results strictly from this time range."]}
    - {"type":"ul","items":["The Usage Graph offers a breakdown of daily usage across all Tavily endpoints with historical data to enable month over month usage and spend comparison.","The Logs Table offers granular insight into each API request to ensure visibility and traceability with every Tavily interaction."]}
    - {"type":"ul","items":["You can now include the favicon URL for each result in the [Search](https://docs.tavily.com/documentation/api-reference/endpoint/search), [Extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract), and [Crawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl) endpoints.","Set the include_favicon parameter to true to receive the favicon URL (if available) for each result in the API response.","This makes it easy to display website icons alongside your search, extraction, or crawl results, improving the visual context and user experience in your application."]}
    - {"type":"ul","items":["Boolean default: false","When auto_parameters is enabled, Tavily automatically configures search parameters based on your query’s content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones.","The parameters include_answer, include_raw_content, and max_results must always be set manually, as they directly affect response size.","Note: search_depth may be automatically set to advanced when it’s likely to improve results. This uses 2 API credits per request. To avoid the extra cost, you can explicitly set search_depth to basic."]}
    - {"type":"ul","items":[]}
    - {"type":"ul","items":[]}
    - {"type":"ul","items":["[Tavily is now available for no-code integration through n8n.](https://docs.tavily.com/documentation/integrations/n8n)Integrate Tavily with n8n to enhance your workflows with real-time web search and content extraction—without writing code. With Tavily’s powerful search and extraction capabilities, you can seamlessly integrate up-to-date online information into your n8n automations.","[Integrate Tavily with Make without writing a single line of code.](https://docs.tavily.com/documentation/integrations/make)With Tavily’s powerful search and content extraction capabilities, you can seamlessly integrate real-time online information into your Make workflows and automations."]}
    - {"type":"ul","items":["Type: enum<string>","Default: markdown","The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.","Available options: markdown, text"]}
    - {"type":"ul","items":["search_depthType: enum<string>Default: basicThe depth of the search. advanced search is tailored to retrieve the most relevant sources and content snippets for your query, while basic search provides generic content snippets from each source.A basic search costs 1 API Credit, while an advanced search costs 2 API Credits.Available options: basic, advanced","Type: enum<string>","Default: basic","The depth of the search. advanced search is tailored to retrieve the most relevant sources and content snippets for your query, while basic search provides generic content snippets from each source.","A basic search costs 1 API Credit, while an advanced search costs 2 API Credits.","Available options: basic, advanced","chunks_per_sourceChunks are short content snippets (maximum 500 characters each) pulled directly from the source.Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length.Chunks will appear in the content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.Available only when search_depth is advanced.Required range: 1 < x < 3","Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.","Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length.","Chunks will appear in the content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.","Available only when search_depth is advanced.","Required range: 1 < x < 3"]}
    - {"type":"ul","items":["Type: enum<string>","Default: basic","The depth of the search. advanced search is tailored to retrieve the most relevant sources and content snippets for your query, while basic search provides generic content snippets from each source.","A basic search costs 1 API Credit, while an advanced search costs 2 API Credits.","Available options: basic, advanced"]}
    - {"type":"ul","items":["Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.","Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length.","Chunks will appear in the content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.","Available only when search_depth is advanced.","Required range: 1 < x < 3"]}
    - {"type":"ul","items":["Tavily Crawl enables you to traverse a website like a graph, starting from a base URL and automatically discovering and extracting content from multiple linked pages. With Tavily Crawl, you can:Specify the starting URL and let the crawler intelligently follow links to map out the site structure.Control the depth and breadth of the crawl, allowing you to focus on specific sections or perform comprehensive site-wide analysis.Apply filters and custom instructions to target only the most relevant pages or content types.Aggregate extracted content for further analysis, reporting, or integration into your workflows.Seamlessly integrate with your automation tools or use the API directly for flexible, programmatic access.Tavily Crawl is ideal for use cases such as large-scale content aggregation, competitive research, knowledge base creation, and more.\nFor full details and API usage examples, see the [Tavily Crawl API reference](https://docs.tavily.com/documentation/api-reference/endpoint/crawl).","Specify the starting URL and let the crawler intelligently follow links to map out the site structure.","Control the depth and breadth of the crawl, allowing you to focus on specific sections or perform comprehensive site-wide analysis.","Apply filters and custom instructions to target only the most relevant pages or content types.","Aggregate extracted content for further analysis, reporting, or integration into your workflows.","Seamlessly integrate with your automation tools or use the API directly for flexible, programmatic access."]}
    - {"type":"ul","items":["Specify the starting URL and let the crawler intelligently follow links to map out the site structure.","Control the depth and breadth of the crawl, allowing you to focus on specific sections or perform comprehensive site-wide analysis.","Apply filters and custom instructions to target only the most relevant pages or content types.","Aggregate extracted content for further analysis, reporting, or integration into your workflows.","Seamlessly integrate with your automation tools or use the API directly for flexible, programmatic access."]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks: []
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Changelog_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Changelog_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Changelog_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Changelog_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Changelog_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Changelog_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Changelog_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Changelog_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Changelog_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":10,"filename":"Changelog_-_Tavily_Docs/svg_10.png","width":16,"height":16}
    - {"type":"svg","index":11,"filename":"Changelog_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Changelog_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Changelog_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Changelog_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Changelog_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":19,"filename":"Changelog_-_Tavily_Docs/svg_19.png","width":12,"height":12}
    - {"type":"svg","index":20,"filename":"Changelog_-_Tavily_Docs/svg_20.png","width":16,"height":16}
    - {"type":"svg","index":21,"filename":"Changelog_-_Tavily_Docs/svg_21.png","width":12,"height":12}
    - {"type":"svg","index":22,"filename":"Changelog_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Changelog_-_Tavily_Docs/svg_23.png","width":12,"height":12}
    - {"type":"svg","index":24,"filename":"Changelog_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Changelog_-_Tavily_Docs/svg_25.png","width":12,"height":12}
    - {"type":"svg","index":26,"filename":"Changelog_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Changelog_-_Tavily_Docs/svg_27.png","width":12,"height":12}
    - {"type":"svg","index":28,"filename":"Changelog_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Changelog_-_Tavily_Docs/svg_29.png","width":12,"height":12}
    - {"type":"svg","index":30,"filename":"Changelog_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Changelog_-_Tavily_Docs/svg_31.png","width":12,"height":12}
    - {"type":"svg","index":32,"filename":"Changelog_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"Changelog_-_Tavily_Docs/svg_33.png","width":12,"height":12}
    - {"type":"svg","index":34,"filename":"Changelog_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Changelog_-_Tavily_Docs/svg_35.png","width":12,"height":12}
    - {"type":"svg","index":36,"filename":"Changelog_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Changelog_-_Tavily_Docs/svg_37.png","width":12,"height":12}
    - {"type":"svg","index":38,"filename":"Changelog_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"Changelog_-_Tavily_Docs/svg_39.png","width":12,"height":12}
    - {"type":"svg","index":40,"filename":"Changelog_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"Changelog_-_Tavily_Docs/svg_41.png","width":12,"height":12}
    - {"type":"svg","index":42,"filename":"Changelog_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Changelog_-_Tavily_Docs/svg_43.png","width":12,"height":12}
    - {"type":"svg","index":44,"filename":"Changelog_-_Tavily_Docs/svg_44.png","width":16,"height":16}
    - {"type":"svg","index":45,"filename":"Changelog_-_Tavily_Docs/svg_45.png","width":12,"height":12}
    - {"type":"svg","index":46,"filename":"Changelog_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"Changelog_-_Tavily_Docs/svg_47.png","width":12,"height":12}
    - {"type":"svg","index":48,"filename":"Changelog_-_Tavily_Docs/svg_48.png","width":16,"height":16}
    - {"type":"svg","index":49,"filename":"Changelog_-_Tavily_Docs/svg_49.png","width":12,"height":12}
    - {"type":"svg","index":50,"filename":"Changelog_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"Changelog_-_Tavily_Docs/svg_51.png","width":12,"height":12}
    - {"type":"svg","index":52,"filename":"Changelog_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"Changelog_-_Tavily_Docs/svg_53.png","width":12,"height":12}
    - {"type":"svg","index":54,"filename":"Changelog_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"Changelog_-_Tavily_Docs/svg_55.png","width":12,"height":12}
    - {"type":"svg","index":56,"filename":"Changelog_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"Changelog_-_Tavily_Docs/svg_57.png","width":14,"height":14}
    - {"type":"svg","index":62,"filename":"Changelog_-_Tavily_Docs/svg_62.png","width":20,"height":20}
    - {"type":"svg","index":63,"filename":"Changelog_-_Tavily_Docs/svg_63.png","width":20,"height":20}
    - {"type":"svg","index":64,"filename":"Changelog_-_Tavily_Docs/svg_64.png","width":20,"height":20}
    - {"type":"svg","index":65,"filename":"Changelog_-_Tavily_Docs/svg_65.png","width":20,"height":20}
    - {"type":"svg","index":66,"filename":"Changelog_-_Tavily_Docs/svg_66.png","width":49,"height":14}
    - {"type":"svg","index":67,"filename":"Changelog_-_Tavily_Docs/svg_67.png","width":16,"height":16}
    - {"type":"svg","index":68,"filename":"Changelog_-_Tavily_Docs/svg_68.png","width":16,"height":16}
    - {"type":"svg","index":69,"filename":"Changelog_-_Tavily_Docs/svg_69.png","width":16,"height":16}
    - {"type":"svg","index":79,"filename":"Changelog_-_Tavily_Docs/svg_79.png","width":16,"height":16}
    - {"type":"svg","index":80,"filename":"Changelog_-_Tavily_Docs/svg_80.png","width":14,"height":14}
    - {"type":"svg","index":81,"filename":"Changelog_-_Tavily_Docs/svg_81.png","width":16,"height":16}
    - {"type":"svg","index":82,"filename":"Changelog_-_Tavily_Docs/svg_82.png","width":12,"height":12}
    - {"type":"svg","index":83,"filename":"Changelog_-_Tavily_Docs/svg_83.png","width":14,"height":14}
    - {"type":"svg","index":84,"filename":"Changelog_-_Tavily_Docs/svg_84.png","width":16,"height":16}
    - {"type":"svg","index":85,"filename":"Changelog_-_Tavily_Docs/svg_85.png","width":12,"height":12}
    - {"type":"svg","index":86,"filename":"Changelog_-_Tavily_Docs/svg_86.png","width":14,"height":14}
    - {"type":"svg","index":87,"filename":"Changelog_-_Tavily_Docs/svg_87.png","width":16,"height":16}
    - {"type":"svg","index":88,"filename":"Changelog_-_Tavily_Docs/svg_88.png","width":12,"height":12}
    - {"type":"svg","index":89,"filename":"Changelog_-_Tavily_Docs/svg_89.png","width":14,"height":14}
  chartData: []
  blockquotes: []
  definitionLists: []
  horizontalRules: 0
  videos: []
  audios: []
  apiData: 0
  pageFeatures:
    suggestedType: "api-doc"
    confidence: 20
    signals:
      - "api-doc-like"
  tabsAndDropdowns: []
  dateFilters: []
---

# Changelog

## 源URL

https://docs.tavily.com/changelog

## 页面结构

- Changelog
  - Privacy Preference Center
    - Manage Consent Preferences
      - Strictly Necessary Cookies
      - Functional Cookies
      - Performance Cookies
      - Targeting Cookies
    - Cookie List

## 正文内容

Enterprise API key management endpoints

March 2026

Exact match parameter

February 2026

Project tracking with X-Project-ID header

January 2026

New search_depth options fast and ultra-fast (BETA)

December 2025

Intent Based Extraction

December 2025

Include usage parameter

December 2025

Vercel AI SDK v5 integration

November 2025

Crawl & Map timeout parameter

November 2025

New team roles & permissions

August 2025

Extract timeout parameter

August 2025

Start date & end date Parameters

July 2025

Usage dashboard

July 2025

Include favicon parameter

June 2025

Auto parameters

June 2025

Usage endpoint

May 2025

Country parameter

May 2025

Boost search results from a specific country.

Make & n8n integrations

May 2025

Integrate Tavily with n8n to enhance your workflows with real-time web search and content extraction—without writing code. With Tavily’s powerful search and extraction capabilities, you can seamlessly integrate up-to-date online information into your n8n automations.

With Tavily’s powerful search and content extraction capabilities, you can seamlessly integrate real-time online information into your Make workflows and automations.

Markdown format

May 2025

Advanced search & chunks per source

April 2025

Tavily crawl (BETA)

April 2025

## 列表

### 列表 1

- [Support](mailto:support@tavily.com)
- [Get an API key](https://app.tavily.com/)
- [Get an API key](https://app.tavily.com/)

### 列表 2

- [API Playground](https://app.tavily.com/playground)
- [Community](https://discord.gg/TPu2gkaWp2)
- [Blog](https://tavily.com/blog)

### 列表 3

- [Changelog](https://docs.tavily.com/changelog)

### 列表 4

- Enterprise users can programmatically manage API keys via dedicated endpoints.
- [POST /generate-keys](https://docs.tavily.com/documentation/enterprise/generate-keys) — Generate new API keys for your organization.
- [POST /deactivate-keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys) — Deactivate existing API keys.
- [GET /key-info](https://docs.tavily.com/documentation/enterprise/key-info) — Retrieve information about an existing API key.
- These endpoints are available on the Enterprise plan only. [Talk to an expert](https://enterprise.tavily.com/) to learn more.

### 列表 5

- Use exact_match to ensure that only search results containing the exact quoted phrase(s) in your query are returned, bypassing synonyms or semantic variations.
- Wrap target phrases in quotes within your query (e.g. “John Smith” CEO Acme Corp).
- Type:boolean
- Default:false
- Because this narrows retrieval, it may return fewer results or empty result fields when no exact matches are found.
- Best suited for due diligence, data enrichment, and legal/compliance use cases where verbatim matches are required.

### 列表 6

- You can now attach a Project ID to your API requests to organize and track usage by project. This is useful when a single API key is used across multiple projects or applications.
- HTTP Header: Add X-Project-ID: your-project-id to any API request
- Python SDK: Pass project_id=“your-project-id” when instantiating the client, or set the TAVILY_PROJECT environment variable
- JavaScript SDK: Pass projectId: “your-project-id” when instantiating the client, or set the TAVILY_PROJECT environment variable
- An API key can be associated with multiple projects
- Filter requests by project in the [/usage endpoint](https://docs.tavily.com/documentation/api-reference/endpoint/usage) and platform usage dashboard to keep track of where requests originate from

### 列表 7

- fast (BETA)Optimized for low latency while maintaining high relevance to the user queryCost: 1 API Credit
- Optimized for low latency while maintaining high relevance to the user query
- Cost: 1 API Credit
- ultra-fast (BETA)Optimized strictly for latencyCost: 1 API Credit
- Optimized strictly for latency
- Cost: 1 API Credit

### 列表 8

- Optimized for low latency while maintaining high relevance to the user query
- Cost: 1 API Credit

### 列表 9

- Optimized strictly for latency
- Cost: 1 API Credit

### 列表 10

- query (Extract)Type: stringUser intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query.
- Type: string
- User intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query.
- chunks_per_source (Extract & Crawl)Type: integerRange: 1 to 5Default: 3Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length.Chunks will appear in the raw_content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.Available only when query is provided (Extract) or instructions are provided (Crawl).
- Type: integer
- Range: 1 to 5
- Default: 3
- Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.
- Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length.
- Chunks will appear in the raw_content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.
- Available only when query is provided (Extract) or instructions are provided (Crawl).

### 列表 11

- Type: string
- User intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query.

### 列表 12

- Type: integer
- Range: 1 to 5
- Default: 3
- Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.
- Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length.
- Chunks will appear in the raw_content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.
- Available only when query is provided (Extract) or instructions are provided (Crawl).

### 列表 13

- You can now include credit usage information in the API response for the [Search](https://docs.tavily.com/documentation/api-reference/endpoint/search#body-include-usage), [Extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract#body-include-usage), [Crawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl#body-include-usage), and [Map](https://docs.tavily.com/documentation/api-reference/endpoint/map#body-include-usage) endpoints.
- Set the include_usage parameter to true to receive credit usage information in the API response.
- Type:boolean
- Default:false
- When enabled, the response includes a usage object with credits information, making it easy to track API credit consumption for each request.
- Note: The value may be 0 if the total successful calls have not yet reached the minimum threshold. See our [Credits & Pricing documentation](https://docs.tavily.com/documentation/api-credits) for details.

### 列表 14

- We’ve released a new [@tavily/ai-sdk](https://www.npmjs.com/package/@tavily/ai-sdk) package that provides pre-built AI SDK tools for Vercel’s AI SDK v5.
- Easily add real-time web search, content extraction, intelligent crawling, and site mapping to your AI SDK project with ready-to-use tools.
- Available Tools: tavilySearch, tavilyExtract, tavilyCrawl, and tavilyMap
- Full TypeScript support with proper type definitions and seamless integration with Vercel AI SDK v5.
- Check out our [integration guide](https://docs.tavily.com/documentation/integrations/vercel) to get started.

### 列表 15

- You can now specify a custom timeout for the [Crawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl) and [Map](https://docs.tavily.com/documentation/api-reference/endpoint/map) endpoints to control how long to wait for the operation before timing out.
- Type:float
- Range: Between 10 and 150 seconds
- Default: 150 seconds
- This gives you fine-grained control over crawl and map operation timeouts, allowing you to balance between reliability and speed based on your specific use case.

### 列表 16

- OwnerFull access to all SettingsAccess and ownership of the Billing account
- Full access to all Settings
- Access and ownership of the Billing account
- AdminFull access to Settings except ownership transferNo access to Billing
- Full access to Settings except ownership transfer
- No access to Billing
- MemberLimited Settings access (view members only)No access to Billing
- Limited Settings access (view members only)
- No access to Billing

### 列表 17

- Full access to all Settings
- Access and ownership of the Billing account

### 列表 18

- Full access to Settings except ownership transfer
- No access to Billing

### 列表 19

- Limited Settings access (view members only)
- No access to Billing

### 列表 20

- You can now specify a custom timeout for the [Extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract) endpoint to control how long to wait for URL extraction before timing out.
- Type: number (float)
- Range: Between 1.0 and 60.0 seconds
- Default behavior: If not specified, automatic timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction.
- This gives you fine-grained control over extraction timeouts, allowing you to balance between reliability and speed based on your specific use case.

### 列表 21

- You can now use both the start_date and end_date parameters in the [Search](https://docs.tavily.com/documentation/api-reference/endpoint/search) endpoints.
- start_date will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.
- end_date will return all results before the specified end date. Required to be written in the format YYYY-MM-DD.
- Set start_date to 2025-01-01 and end_date to 2025-04-01 to reiceive results strictly from this time range.

### 列表 22

- The Usage Graph offers a breakdown of daily usage across all Tavily endpoints with historical data to enable month over month usage and spend comparison.
- The Logs Table offers granular insight into each API request to ensure visibility and traceability with every Tavily interaction.

### 列表 23

- You can now include the favicon URL for each result in the [Search](https://docs.tavily.com/documentation/api-reference/endpoint/search), [Extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract), and [Crawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl) endpoints.
- Set the include_favicon parameter to true to receive the favicon URL (if available) for each result in the API response.
- This makes it easy to display website icons alongside your search, extraction, or crawl results, improving the visual context and user experience in your application.

### 列表 24

- Boolean default: false
- When auto_parameters is enabled, Tavily automatically configures search parameters based on your query’s content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones.
- The parameters include_answer, include_raw_content, and max_results must always be set manually, as they directly affect response size.
- Note: search_depth may be automatically set to advanced when it’s likely to improve results. This uses 2 API credits per request. To avoid the extra cost, you can explicitly set search_depth to basic.

### 列表 25

### 列表 26

### 列表 27

- [Tavily is now available for no-code integration through n8n.](https://docs.tavily.com/documentation/integrations/n8n)Integrate Tavily with n8n to enhance your workflows with real-time web search and content extraction—without writing code. With Tavily’s powerful search and extraction capabilities, you can seamlessly integrate up-to-date online information into your n8n automations.
- [Integrate Tavily with Make without writing a single line of code.](https://docs.tavily.com/documentation/integrations/make)With Tavily’s powerful search and content extraction capabilities, you can seamlessly integrate real-time online information into your Make workflows and automations.

### 列表 28

- Type: enum<string>
- Default: markdown
- The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.
- Available options: markdown, text

### 列表 29

- search_depthType: enum<string>Default: basicThe depth of the search. advanced search is tailored to retrieve the most relevant sources and content snippets for your query, while basic search provides generic content snippets from each source.A basic search costs 1 API Credit, while an advanced search costs 2 API Credits.Available options: basic, advanced
- Type: enum<string>
- Default: basic
- The depth of the search. advanced search is tailored to retrieve the most relevant sources and content snippets for your query, while basic search provides generic content snippets from each source.
- A basic search costs 1 API Credit, while an advanced search costs 2 API Credits.
- Available options: basic, advanced
- chunks_per_sourceChunks are short content snippets (maximum 500 characters each) pulled directly from the source.Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length.Chunks will appear in the content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.Available only when search_depth is advanced.Required range: 1 < x < 3
- Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.
- Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length.
- Chunks will appear in the content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.
- Available only when search_depth is advanced.
- Required range: 1 < x < 3

### 列表 30

- Type: enum<string>
- Default: basic
- The depth of the search. advanced search is tailored to retrieve the most relevant sources and content snippets for your query, while basic search provides generic content snippets from each source.
- A basic search costs 1 API Credit, while an advanced search costs 2 API Credits.
- Available options: basic, advanced

### 列表 31

- Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.
- Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length.
- Chunks will appear in the content field as: <chunk 1> […] <chunk 2> […] <chunk 3>.
- Available only when search_depth is advanced.
- Required range: 1 < x < 3

### 列表 32

- Tavily Crawl enables you to traverse a website like a graph, starting from a base URL and automatically discovering and extracting content from multiple linked pages. With Tavily Crawl, you can:Specify the starting URL and let the crawler intelligently follow links to map out the site structure.Control the depth and breadth of the crawl, allowing you to focus on specific sections or perform comprehensive site-wide analysis.Apply filters and custom instructions to target only the most relevant pages or content types.Aggregate extracted content for further analysis, reporting, or integration into your workflows.Seamlessly integrate with your automation tools or use the API directly for flexible, programmatic access.Tavily Crawl is ideal for use cases such as large-scale content aggregation, competitive research, knowledge base creation, and more.
For full details and API usage examples, see the [Tavily Crawl API reference](https://docs.tavily.com/documentation/api-reference/endpoint/crawl).
- Specify the starting URL and let the crawler intelligently follow links to map out the site structure.
- Control the depth and breadth of the crawl, allowing you to focus on specific sections or perform comprehensive site-wide analysis.
- Apply filters and custom instructions to target only the most relevant pages or content types.
- Aggregate extracted content for further analysis, reporting, or integration into your workflows.
- Seamlessly integrate with your automation tools or use the API directly for flexible, programmatic access.

### 列表 33

- Specify the starting URL and let the crawler intelligently follow links to map out the site structure.
- Control the depth and breadth of the crawl, allowing you to focus on specific sections or perform comprehensive site-wide analysis.
- Apply filters and custom instructions to target only the most relevant pages or content types.
- Aggregate extracted content for further analysis, reporting, or integration into your workflows.
- Seamlessly integrate with your automation tools or use the API directly for flexible, programmatic access.

### 列表 34

- checkbox label label

## 图片

![light logo](Changelog_-_Tavily_Docs/image_1.svg)

![dark logo](Changelog_-_Tavily_Docs/image_2.svg)

![light logo](Changelog_-_Tavily_Docs/image_3.svg)

![dark logo](Changelog_-_Tavily_Docs/image_4.svg)

![tavily-logo](Changelog_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Changelog_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Changelog_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Changelog_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Changelog_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 10](Changelog_-_Tavily_Docs/svg_10.png)
*尺寸: 16x16px*

![SVG图表 11](Changelog_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Changelog_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Changelog_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 17](Changelog_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Changelog_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 19](Changelog_-_Tavily_Docs/svg_19.png)
*尺寸: 12x12px*

![SVG图表 20](Changelog_-_Tavily_Docs/svg_20.png)
*尺寸: 16x16px*

![SVG图表 21](Changelog_-_Tavily_Docs/svg_21.png)
*尺寸: 12x12px*

![SVG图表 22](Changelog_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](Changelog_-_Tavily_Docs/svg_23.png)
*尺寸: 12x12px*

![SVG图表 24](Changelog_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Changelog_-_Tavily_Docs/svg_25.png)
*尺寸: 12x12px*

![SVG图表 26](Changelog_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Changelog_-_Tavily_Docs/svg_27.png)
*尺寸: 12x12px*

![SVG图表 28](Changelog_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Changelog_-_Tavily_Docs/svg_29.png)
*尺寸: 12x12px*

![SVG图表 30](Changelog_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 31](Changelog_-_Tavily_Docs/svg_31.png)
*尺寸: 12x12px*

![SVG图表 32](Changelog_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](Changelog_-_Tavily_Docs/svg_33.png)
*尺寸: 12x12px*

![SVG图表 34](Changelog_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Changelog_-_Tavily_Docs/svg_35.png)
*尺寸: 12x12px*

![SVG图表 36](Changelog_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](Changelog_-_Tavily_Docs/svg_37.png)
*尺寸: 12x12px*

![SVG图表 38](Changelog_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](Changelog_-_Tavily_Docs/svg_39.png)
*尺寸: 12x12px*

![SVG图表 40](Changelog_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](Changelog_-_Tavily_Docs/svg_41.png)
*尺寸: 12x12px*

![SVG图表 42](Changelog_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](Changelog_-_Tavily_Docs/svg_43.png)
*尺寸: 12x12px*

![SVG图表 44](Changelog_-_Tavily_Docs/svg_44.png)
*尺寸: 16x16px*

![SVG图表 45](Changelog_-_Tavily_Docs/svg_45.png)
*尺寸: 12x12px*

![SVG图表 46](Changelog_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](Changelog_-_Tavily_Docs/svg_47.png)
*尺寸: 12x12px*

![SVG图表 48](Changelog_-_Tavily_Docs/svg_48.png)
*尺寸: 16x16px*

![SVG图表 49](Changelog_-_Tavily_Docs/svg_49.png)
*尺寸: 12x12px*

![SVG图表 50](Changelog_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](Changelog_-_Tavily_Docs/svg_51.png)
*尺寸: 12x12px*

![SVG图表 52](Changelog_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](Changelog_-_Tavily_Docs/svg_53.png)
*尺寸: 12x12px*

![SVG图表 54](Changelog_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](Changelog_-_Tavily_Docs/svg_55.png)
*尺寸: 12x12px*

![SVG图表 56](Changelog_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](Changelog_-_Tavily_Docs/svg_57.png)
*尺寸: 14x14px*

![SVG图表 62](Changelog_-_Tavily_Docs/svg_62.png)
*尺寸: 20x20px*

![SVG图表 63](Changelog_-_Tavily_Docs/svg_63.png)
*尺寸: 20x20px*

![SVG图表 64](Changelog_-_Tavily_Docs/svg_64.png)
*尺寸: 20x20px*

![SVG图表 65](Changelog_-_Tavily_Docs/svg_65.png)
*尺寸: 20x20px*

![SVG图表 66](Changelog_-_Tavily_Docs/svg_66.png)
*尺寸: 49x14px*

![SVG图表 67](Changelog_-_Tavily_Docs/svg_67.png)
*尺寸: 16x16px*

![SVG图表 68](Changelog_-_Tavily_Docs/svg_68.png)
*尺寸: 16x16px*

![SVG图表 69](Changelog_-_Tavily_Docs/svg_69.png)
*尺寸: 16x16px*

![SVG图表 79](Changelog_-_Tavily_Docs/svg_79.png)
*尺寸: 16x16px*

![SVG图表 80](Changelog_-_Tavily_Docs/svg_80.png)
*尺寸: 14x14px*

![SVG图表 81](Changelog_-_Tavily_Docs/svg_81.png)
*尺寸: 16x16px*

![SVG图表 82](Changelog_-_Tavily_Docs/svg_82.png)
*尺寸: 12x12px*

![SVG图表 83](Changelog_-_Tavily_Docs/svg_83.png)
*尺寸: 14x14px*

![SVG图表 84](Changelog_-_Tavily_Docs/svg_84.png)
*尺寸: 16x16px*

![SVG图表 85](Changelog_-_Tavily_Docs/svg_85.png)
*尺寸: 12x12px*

![SVG图表 86](Changelog_-_Tavily_Docs/svg_86.png)
*尺寸: 14x14px*

![SVG图表 87](Changelog_-_Tavily_Docs/svg_87.png)
*尺寸: 16x16px*

![SVG图表 88](Changelog_-_Tavily_Docs/svg_88.png)
*尺寸: 12x12px*

![SVG图表 89](Changelog_-_Tavily_Docs/svg_89.png)
*尺寸: 14x14px*
