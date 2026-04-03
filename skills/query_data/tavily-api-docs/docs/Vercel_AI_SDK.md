---
id: "url-3d8f09"
type: "website"
title: "Vercel AI SDK"
url: "https://docs.tavily.com/documentation/integrations/vercel"
description: "Integrate Tavily with Vercel AI SDK to enhance your AI agents with powerful web search, content extraction, crawling, and site mapping capabilities."
source: ""
tags: []
crawl_time: "2026-03-18T06:36:01.796Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Vercel AI SDK"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-by-step-integration-guide)Step-by-Step Integration Guide"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-1-install-required-packages)Step 1: Install Required Packages"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-2-set-up-api-keys)Step 2: Set Up API Keys"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-3-basic-usage)Step 3: Basic Usage"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#available-tools)Available Tools"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-search)Tavily Search"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-extract)Tavily Extract"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-crawl)Tavily Crawl"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-map)Tavily Map"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#using-multiple-tools-together)Using Multiple Tools Together"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#advanced-examples)Advanced Examples"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#news-research-with-time-range)News Research with Time Range"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#market-analysis-with-advanced-search)Market Analysis with Advanced Search"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/vercel#benefits-of-tavily-+-vercel-ai-sdk)Benefits of Tavily + Vercel AI SDK"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-by-step-integration-guide)Step-by-Step Integration Guide"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-1-install-required-packages)Step 1: Install Required Packages"}
    - {"type":"codeblock","language":"","content":"npm install ai @ai-sdk/openai @tavily/ai-sdk"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-2-set-up-api-keys)Step 2: Set Up API Keys"}
    - {"type":"list","listType":"ul","items":["**Tavily API Key:** [Get your Tavily API key here](https://app.tavily.com/home)","**OpenAI API Key:** [Get your OpenAI API key here](https://platform.openai.com/account/api-keys)"]}
    - {"type":"codeblock","language":"","content":"export TAVILY_API_KEY=tvly-your-api-key\nexport OPENAI_API_KEY=your-openai-api-key"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#step-3-basic-usage)Step 3: Basic Usage"}
    - {"type":"codeblock","language":"","content":"import { tavilySearch } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"What are the latest developments in quantum computing?\",\n  tools: {\n    tavilySearch: tavilySearch(),\n  },\n  stopWhen: stepCountIs(3),\n});\n\nconsole.log(result.text);"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#available-tools)Available Tools"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-search)Tavily Search"}
    - {"type":"codeblock","language":"","content":"import { tavilySearch } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Research the latest trends in renewable energy technology\",\n  tools: {\n    tavilySearch: tavilySearch({\n      searchDepth: \"advanced\",\n      includeAnswer: true,\n      maxResults: 5,\n      topic: \"general\",\n    }),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"type":"list","listType":"ul","items":["`searchDepth?: \"basic\" | \"advanced\"` - Search depth (default: “basic”)","`topic?: \"general\" | \"news\" | \"finance\"` - Search category","`includeAnswer?: boolean` - Include AI-generated answer","`maxResults?: number` - Maximum results to return (default: 5)","`includeImages?: boolean` - Include images in results","`timeRange?: \"year\" | \"month\" | \"week\" | \"day\"` - Time range for results","`includeDomains?: string[]` - Domains to include","`excludeDomains?: string[]` - Domains to exclude"]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-extract)Tavily Extract"}
    - {"type":"codeblock","language":"","content":"import { tavilyExtract } from \"@tavily/ai-sdk\";\nimport { generateText } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Extract and summarize the content from https://tavily.com\",\n  tools: {\n    tavilyExtract: tavilyExtract(),\n  },\n});"}
    - {"type":"list","listType":"ul","items":["`extractDepth?: \"basic\" | \"advanced\"` - Extraction depth","`format?: \"markdown\" | \"text\"` - Output format (default: “markdown”)","`includeImages?: boolean` - Include images in extracted content"]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-crawl)Tavily Crawl"}
    - {"type":"codeblock","language":"","content":"import { tavilyCrawl } from \"@tavily/ai-sdk\";\nimport { generateText } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Crawl tavily.com and tell me about their integrations\",\n  tools: {\n    tavilyCrawl: tavilyCrawl({\n      maxDepth: 2,\n      limit: 50,\n    }),\n  },\n});"}
    - {"type":"list","listType":"ul","items":["`maxDepth?: number` - Maximum crawl depth (1-5, default: 1)","`maxBreadth?: number` - Maximum pages per depth level (1-100, default: 20)","`limit?: number` - Maximum total pages to crawl (default: 50)","`extractDepth?: \"basic\" | \"advanced\"` - Content extraction depth","`instructions?: string` - Natural language crawling instructions","`selectPaths?: string[]` - Path patterns to include","`excludePaths?: string[]` - Path patterns to exclude","`allowExternal?: boolean` - Allow crawling external domains"]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#tavily-map)Tavily Map"}
    - {"type":"codeblock","language":"","content":"import { tavilyMap } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Map the structure of tavily.com\",\n  tools: {\n    tavilyMap: tavilyMap(),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"type":"list","listType":"ul","items":["`maxDepth?: number` - Maximum mapping depth (1-5, default: 1)","`maxBreadth?: number` - Maximum pages per depth level (1-100, default: 20)","`limit?: number` - Maximum total pages to map (default: 50)","`instructions?: string` - Natural language mapping instructions","`selectPaths?: string[]` - Path patterns to include","`excludePaths?: string[]` - Path patterns to exclude","`allowExternal?: boolean` - Allow mapping external domains"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#using-multiple-tools-together)Using Multiple Tools Together"}
    - {"type":"codeblock","language":"","content":"import { \n  tavilySearch, \n  tavilyExtract, \n  tavilyCrawl, \n  tavilyMap \n} from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Research the company at tavily.com - search for news, map their site, and extract key pages\",\n  tools: {\n    tavilySearch: tavilySearch({ searchDepth: \"advanced\" }),\n    tavilyExtract: tavilyExtract(),\n    tavilyCrawl: tavilyCrawl(),\n    tavilyMap: tavilyMap(),\n  },\n  stopWhen: stepCountIs(5),\n});"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#advanced-examples)Advanced Examples"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#news-research-with-time-range)News Research with Time Range"}
    - {"type":"codeblock","language":"","content":"const newsResult = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"What are the top technology news stories from this week?\",\n  tools: {\n    tavilySearch: tavilySearch({\n      topic: \"news\",\n      timeRange: \"week\",\n      maxResults: 10,\n    }),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#market-analysis-with-advanced-search)Market Analysis with Advanced Search"}
    - {"type":"codeblock","language":"","content":"const marketResult = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Analyze the current state of the electric vehicle market\",\n  tools: {\n    tavilySearch: tavilySearch({\n      searchDepth: \"advanced\",\n      topic: \"finance\",\n      includeAnswer: true,\n      maxResults: 10,\n    }),\n  },\n  stopWhen: stepCountIs(5),\n});"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/vercel#benefits-of-tavily-+-vercel-ai-sdk)Benefits of Tavily + Vercel AI SDK"}
    - {"type":"list","listType":"ul","items":["**Pre-built Tools:** No need to manually create tool definitions - just import and use","**Type-Safe:** Full TypeScript support with proper type definitions","**Real-time Information:** Access up-to-date web content for your AI agents","**Optimized for LLMs:** Search results are specifically formatted for language models","**Multiple Capabilities:** Search, extract, crawl, and map websites - all in one package","**Easy Integration:** Works seamlessly with Vercel AI SDK v5","**Flexible Configuration:** Extensive configuration options for all tools","**Production-Ready:** Built on the reliable Tavily API infrastructure"]}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/integrations/vercel#introduction)","[Step-by-Step Integration Guide](https://docs.tavily.com/documentation/integrations/vercel#step-by-step-integration-guide)","[Step 1: Install Required Packages](https://docs.tavily.com/documentation/integrations/vercel#step-1-install-required-packages)","[Step 2: Set Up API Keys](https://docs.tavily.com/documentation/integrations/vercel#step-2-set-up-api-keys)","[Step 3: Basic Usage](https://docs.tavily.com/documentation/integrations/vercel#step-3-basic-usage)","[Available Tools](https://docs.tavily.com/documentation/integrations/vercel#available-tools)","[Tavily Search](https://docs.tavily.com/documentation/integrations/vercel#tavily-search)","[Tavily Extract](https://docs.tavily.com/documentation/integrations/vercel#tavily-extract)","[Tavily Crawl](https://docs.tavily.com/documentation/integrations/vercel#tavily-crawl)","[Tavily Map](https://docs.tavily.com/documentation/integrations/vercel#tavily-map)","[Using Multiple Tools Together](https://docs.tavily.com/documentation/integrations/vercel#using-multiple-tools-together)","[Advanced Examples](https://docs.tavily.com/documentation/integrations/vercel#advanced-examples)","[News Research with Time Range](https://docs.tavily.com/documentation/integrations/vercel#news-research-with-time-range)","[Market Analysis with Advanced Search](https://docs.tavily.com/documentation/integrations/vercel#market-analysis-with-advanced-search)","[Benefits of Tavily + Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel#benefits-of-tavily-%2B-vercel-ai-sdk)"]}
    - {"type":"ul","items":["Tavily API Key: [Get your Tavily API key here](https://app.tavily.com/home)","OpenAI API Key: [Get your OpenAI API key here](https://platform.openai.com/account/api-keys)"]}
    - {"type":"ul","items":["searchDepth?: \"basic\" | \"advanced\" - Search depth (default: “basic”)","topic?: \"general\" | \"news\" | \"finance\" - Search category","includeAnswer?: boolean - Include AI-generated answer","maxResults?: number - Maximum results to return (default: 5)","includeImages?: boolean - Include images in results","timeRange?: \"year\" | \"month\" | \"week\" | \"day\" - Time range for results","includeDomains?: string[] - Domains to include","excludeDomains?: string[] - Domains to exclude"]}
    - {"type":"ul","items":["extractDepth?: \"basic\" | \"advanced\" - Extraction depth","format?: \"markdown\" | \"text\" - Output format (default: “markdown”)","includeImages?: boolean - Include images in extracted content"]}
    - {"type":"ul","items":["maxDepth?: number - Maximum crawl depth (1-5, default: 1)","maxBreadth?: number - Maximum pages per depth level (1-100, default: 20)","limit?: number - Maximum total pages to crawl (default: 50)","extractDepth?: \"basic\" | \"advanced\" - Content extraction depth","instructions?: string - Natural language crawling instructions","selectPaths?: string[] - Path patterns to include","excludePaths?: string[] - Path patterns to exclude","allowExternal?: boolean - Allow crawling external domains"]}
    - {"type":"ul","items":["maxDepth?: number - Maximum mapping depth (1-5, default: 1)","maxBreadth?: number - Maximum pages per depth level (1-100, default: 20)","limit?: number - Maximum total pages to map (default: 50)","instructions?: string - Natural language mapping instructions","selectPaths?: string[] - Path patterns to include","excludePaths?: string[] - Path patterns to exclude","allowExternal?: boolean - Allow mapping external domains"]}
    - {"type":"ul","items":["Pre-built Tools: No need to manually create tool definitions - just import and use","Type-Safe: Full TypeScript support with proper type definitions","Real-time Information: Access up-to-date web content for your AI agents","Optimized for LLMs: Search results are specifically formatted for language models","Multiple Capabilities: Search, extract, crawl, and map websites - all in one package","Easy Integration: Works seamlessly with Vercel AI SDK v5","Flexible Configuration: Extensive configuration options for all tools","Production-Ready: Built on the reliable Tavily API infrastructure"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"npm install ai @ai-sdk/openai @tavily/ai-sdk"}
    - {"language":"text","code":"npm install ai @ai-sdk/openai @tavily/ai-sdk"}
    - {"language":"text","code":"export TAVILY_API_KEY=tvly-your-api-key\nexport OPENAI_API_KEY=your-openai-api-key"}
    - {"language":"text","code":"export TAVILY_API_KEY=tvly-your-api-key\nexport OPENAI_API_KEY=your-openai-api-key"}
    - {"language":"text","code":"import { tavilySearch } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"What are the latest developments in quantum computing?\",\n  tools: {\n    tavilySearch: tavilySearch(),\n  },\n  stopWhen: stepCountIs(3),\n});\n\nconsole.log(result.text);"}
    - {"language":"text","code":"import { tavilySearch } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"What are the latest developments in quantum computing?\",\n  tools: {\n    tavilySearch: tavilySearch(),\n  },\n  stopWhen: stepCountIs(3),\n});\n\nconsole.log(result.text);"}
    - {"language":"text","code":"import { tavilySearch } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Research the latest trends in renewable energy technology\",\n  tools: {\n    tavilySearch: tavilySearch({\n      searchDepth: \"advanced\",\n      includeAnswer: true,\n      maxResults: 5,\n      topic: \"general\",\n    }),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"language":"text","code":"import { tavilySearch } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Research the latest trends in renewable energy technology\",\n  tools: {\n    tavilySearch: tavilySearch({\n      searchDepth: \"advanced\",\n      includeAnswer: true,\n      maxResults: 5,\n      topic: \"general\",\n    }),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"language":"text","code":"import { tavilyExtract } from \"@tavily/ai-sdk\";\nimport { generateText } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Extract and summarize the content from https://tavily.com\",\n  tools: {\n    tavilyExtract: tavilyExtract(),\n  },\n});"}
    - {"language":"text","code":"import { tavilyExtract } from \"@tavily/ai-sdk\";\nimport { generateText } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Extract and summarize the content from https://tavily.com\",\n  tools: {\n    tavilyExtract: tavilyExtract(),\n  },\n});"}
    - {"language":"text","code":"import { tavilyCrawl } from \"@tavily/ai-sdk\";\nimport { generateText } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Crawl tavily.com and tell me about their integrations\",\n  tools: {\n    tavilyCrawl: tavilyCrawl({\n      maxDepth: 2,\n      limit: 50,\n    }),\n  },\n});"}
    - {"language":"text","code":"import { tavilyCrawl } from \"@tavily/ai-sdk\";\nimport { generateText } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Crawl tavily.com and tell me about their integrations\",\n  tools: {\n    tavilyCrawl: tavilyCrawl({\n      maxDepth: 2,\n      limit: 50,\n    }),\n  },\n});"}
    - {"language":"text","code":"import { tavilyMap } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Map the structure of tavily.com\",\n  tools: {\n    tavilyMap: tavilyMap(),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"language":"text","code":"import { tavilyMap } from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Map the structure of tavily.com\",\n  tools: {\n    tavilyMap: tavilyMap(),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"language":"text","code":"import { \n  tavilySearch, \n  tavilyExtract, \n  tavilyCrawl, \n  tavilyMap \n} from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Research the company at tavily.com - search for news, map their site, and extract key pages\",\n  tools: {\n    tavilySearch: tavilySearch({ searchDepth: \"advanced\" }),\n    tavilyExtract: tavilyExtract(),\n    tavilyCrawl: tavilyCrawl(),\n    tavilyMap: tavilyMap(),\n  },\n  stopWhen: stepCountIs(5),\n});"}
    - {"language":"text","code":"import { \n  tavilySearch, \n  tavilyExtract, \n  tavilyCrawl, \n  tavilyMap \n} from \"@tavily/ai-sdk\";\nimport { generateText, stepCountIs } from \"ai\";\nimport { openai } from \"@ai-sdk/openai\";\n\nconst result = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Research the company at tavily.com - search for news, map their site, and extract key pages\",\n  tools: {\n    tavilySearch: tavilySearch({ searchDepth: \"advanced\" }),\n    tavilyExtract: tavilyExtract(),\n    tavilyCrawl: tavilyCrawl(),\n    tavilyMap: tavilyMap(),\n  },\n  stopWhen: stepCountIs(5),\n});"}
    - {"language":"text","code":"const newsResult = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"What are the top technology news stories from this week?\",\n  tools: {\n    tavilySearch: tavilySearch({\n      topic: \"news\",\n      timeRange: \"week\",\n      maxResults: 10,\n    }),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"language":"text","code":"const newsResult = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"What are the top technology news stories from this week?\",\n  tools: {\n    tavilySearch: tavilySearch({\n      topic: \"news\",\n      timeRange: \"week\",\n      maxResults: 10,\n    }),\n  },\n  stopWhen: stepCountIs(3),\n});"}
    - {"language":"text","code":"const marketResult = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Analyze the current state of the electric vehicle market\",\n  tools: {\n    tavilySearch: tavilySearch({\n      searchDepth: \"advanced\",\n      topic: \"finance\",\n      includeAnswer: true,\n      maxResults: 10,\n    }),\n  },\n  stopWhen: stepCountIs(5),\n});"}
    - {"language":"text","code":"const marketResult = await generateText({\n  model: openai(\"gpt-5-mini\"),\n  prompt: \"Analyze the current state of the electric vehicle market\",\n  tools: {\n    tavilySearch: tavilySearch({\n      searchDepth: \"advanced\",\n      topic: \"finance\",\n      includeAnswer: true,\n      maxResults: 10,\n    }),\n  },\n  stopWhen: stepCountIs(5),\n});"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Vercel_AI_SDK_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Vercel_AI_SDK_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Vercel_AI_SDK_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Vercel_AI_SDK_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Vercel_AI_SDK_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Vercel_AI_SDK_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_34.png","width":14,"height":12}
    - {"type":"svg","index":35,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_37.png","width":14,"height":12}
    - {"type":"svg","index":38,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_40.png","width":14,"height":12}
    - {"type":"svg","index":41,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_41.png","width":16,"height":16}
    - {"type":"svg","index":42,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_43.png","width":14,"height":12}
    - {"type":"svg","index":44,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_44.png","width":16,"height":16}
    - {"type":"svg","index":45,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_46.png","width":14,"height":12}
    - {"type":"svg","index":47,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_47.png","width":16,"height":16}
    - {"type":"svg","index":48,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_48.png","width":16,"height":16}
    - {"type":"svg","index":49,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_49.png","width":14,"height":12}
    - {"type":"svg","index":50,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_50.png","width":14,"height":12}
    - {"type":"svg","index":51,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_53.png","width":14,"height":12}
    - {"type":"svg","index":54,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_55.png","width":16,"height":16}
    - {"type":"svg","index":56,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_56.png","width":14,"height":12}
    - {"type":"svg","index":57,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_57.png","width":14,"height":14}
    - {"type":"svg","index":58,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_58.png","width":14,"height":14}
    - {"type":"svg","index":59,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_59.png","width":14,"height":14}
    - {"type":"svg","index":64,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_64.png","width":20,"height":20}
    - {"type":"svg","index":65,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_65.png","width":20,"height":20}
    - {"type":"svg","index":66,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_66.png","width":20,"height":20}
    - {"type":"svg","index":67,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_67.png","width":20,"height":20}
    - {"type":"svg","index":68,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_68.png","width":49,"height":14}
    - {"type":"svg","index":69,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_69.png","width":16,"height":16}
    - {"type":"svg","index":70,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_70.png","width":16,"height":16}
    - {"type":"svg","index":71,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_71.png","width":16,"height":16}
    - {"type":"svg","index":81,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_81.png","width":16,"height":16}
    - {"type":"svg","index":82,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_82.png","width":14,"height":14}
    - {"type":"svg","index":83,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_83.png","width":16,"height":16}
    - {"type":"svg","index":84,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_84.png","width":12,"height":12}
    - {"type":"svg","index":85,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_85.png","width":14,"height":14}
    - {"type":"svg","index":86,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_86.png","width":16,"height":16}
    - {"type":"svg","index":87,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_87.png","width":12,"height":12}
    - {"type":"svg","index":88,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_88.png","width":14,"height":14}
    - {"type":"svg","index":89,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_89.png","width":16,"height":16}
    - {"type":"svg","index":90,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_90.png","width":12,"height":12}
    - {"type":"svg","index":91,"filename":"Vercel_AI_SDK_-_Tavily_Docs/svg_91.png","width":14,"height":14}
  chartData: []
  blockquotes: []
  definitionLists: []
  horizontalRules: 0
  videos: []
  audios: []
  apiData: 0
  pageFeatures:
    suggestedType: "article"
    confidence: 45
    signals:
      - "article-like"
      - "api-doc-like"
  tabsAndDropdowns: []
  dateFilters: []
---

# Vercel AI SDK

## 源URL

https://docs.tavily.com/documentation/integrations/vercel

## 描述

Integrate Tavily with Vercel AI SDK to enhance your AI agents with powerful web search, content extraction, crawling, and site mapping capabilities.

## 内容

### Introduction

### Step-by-Step Integration Guide

#### Step 1: Install Required Packages

```text
npm install ai @ai-sdk/openai @tavily/ai-sdk
```

#### Step 2: Set Up API Keys

- **Tavily API Key:** [Get your Tavily API key here](https://app.tavily.com/home)
- **OpenAI API Key:** [Get your OpenAI API key here](https://platform.openai.com/account/api-keys)

```text
export TAVILY_API_KEY=tvly-your-api-key
export OPENAI_API_KEY=your-openai-api-key
```

#### Step 3: Basic Usage

```text
import { tavilySearch } from "@tavily/ai-sdk";
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";

const result = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "What are the latest developments in quantum computing?",
  tools: {
    tavilySearch: tavilySearch(),
  },
  stopWhen: stepCountIs(3),
});

console.log(result.text);
```

### Available Tools

#### Tavily Search

```text
import { tavilySearch } from "@tavily/ai-sdk";
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";

const result = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "Research the latest trends in renewable energy technology",
  tools: {
    tavilySearch: tavilySearch({
      searchDepth: "advanced",
      includeAnswer: true,
      maxResults: 5,
      topic: "general",
    }),
  },
  stopWhen: stepCountIs(3),
});
```

- `searchDepth?: "basic" | "advanced"` - Search depth (default: “basic”)
- `topic?: "general" | "news" | "finance"` - Search category
- `includeAnswer?: boolean` - Include AI-generated answer
- `maxResults?: number` - Maximum results to return (default: 5)
- `includeImages?: boolean` - Include images in results
- `timeRange?: "year" | "month" | "week" | "day"` - Time range for results
- `includeDomains?: string[]` - Domains to include
- `excludeDomains?: string[]` - Domains to exclude

#### Tavily Extract

```text
import { tavilyExtract } from "@tavily/ai-sdk";
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

const result = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "Extract and summarize the content from https://tavily.com",
  tools: {
    tavilyExtract: tavilyExtract(),
  },
});
```

- `extractDepth?: "basic" | "advanced"` - Extraction depth
- `format?: "markdown" | "text"` - Output format (default: “markdown”)
- `includeImages?: boolean` - Include images in extracted content

#### Tavily Crawl

```text
import { tavilyCrawl } from "@tavily/ai-sdk";
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

const result = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "Crawl tavily.com and tell me about their integrations",
  tools: {
    tavilyCrawl: tavilyCrawl({
      maxDepth: 2,
      limit: 50,
    }),
  },
});
```

- `maxDepth?: number` - Maximum crawl depth (1-5, default: 1)
- `maxBreadth?: number` - Maximum pages per depth level (1-100, default: 20)
- `limit?: number` - Maximum total pages to crawl (default: 50)
- `extractDepth?: "basic" | "advanced"` - Content extraction depth
- `instructions?: string` - Natural language crawling instructions
- `selectPaths?: string[]` - Path patterns to include
- `excludePaths?: string[]` - Path patterns to exclude
- `allowExternal?: boolean` - Allow crawling external domains

#### Tavily Map

```text
import { tavilyMap } from "@tavily/ai-sdk";
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";

const result = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "Map the structure of tavily.com",
  tools: {
    tavilyMap: tavilyMap(),
  },
  stopWhen: stepCountIs(3),
});
```

- `maxDepth?: number` - Maximum mapping depth (1-5, default: 1)
- `maxBreadth?: number` - Maximum pages per depth level (1-100, default: 20)
- `limit?: number` - Maximum total pages to map (default: 50)
- `instructions?: string` - Natural language mapping instructions
- `selectPaths?: string[]` - Path patterns to include
- `excludePaths?: string[]` - Path patterns to exclude
- `allowExternal?: boolean` - Allow mapping external domains

### Using Multiple Tools Together

```text
import { 
  tavilySearch, 
  tavilyExtract, 
  tavilyCrawl, 
  tavilyMap 
} from "@tavily/ai-sdk";
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";

const result = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "Research the company at tavily.com - search for news, map their site, and extract key pages",
  tools: {
    tavilySearch: tavilySearch({ searchDepth: "advanced" }),
    tavilyExtract: tavilyExtract(),
    tavilyCrawl: tavilyCrawl(),
    tavilyMap: tavilyMap(),
  },
  stopWhen: stepCountIs(5),
});
```

### Advanced Examples

#### News Research with Time Range

```text
const newsResult = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "What are the top technology news stories from this week?",
  tools: {
    tavilySearch: tavilySearch({
      topic: "news",
      timeRange: "week",
      maxResults: 10,
    }),
  },
  stopWhen: stepCountIs(3),
});
```

#### Market Analysis with Advanced Search

```text
const marketResult = await generateText({
  model: openai("gpt-5-mini"),
  prompt: "Analyze the current state of the electric vehicle market",
  tools: {
    tavilySearch: tavilySearch({
      searchDepth: "advanced",
      topic: "finance",
      includeAnswer: true,
      maxResults: 10,
    }),
  },
  stopWhen: stepCountIs(5),
});
```

### Benefits of Tavily + Vercel AI SDK

- **Pre-built Tools:** No need to manually create tool definitions - just import and use
- **Type-Safe:** Full TypeScript support with proper type definitions
- **Real-time Information:** Access up-to-date web content for your AI agents
- **Optimized for LLMs:** Search results are specifically formatted for language models
- **Multiple Capabilities:** Search, extract, crawl, and map websites - all in one package
- **Easy Integration:** Works seamlessly with Vercel AI SDK v5
- **Flexible Configuration:** Extensive configuration options for all tools
- **Production-Ready:** Built on the reliable Tavily API infrastructure

## 图片

![light logo](Vercel_AI_SDK_-_Tavily_Docs/image_1.svg)

![dark logo](Vercel_AI_SDK_-_Tavily_Docs/image_2.svg)

![light logo](Vercel_AI_SDK_-_Tavily_Docs/image_3.svg)

![dark logo](Vercel_AI_SDK_-_Tavily_Docs/image_4.svg)

![tavily-logo](Vercel_AI_SDK_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Vercel_AI_SDK_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Vercel_AI_SDK_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Vercel_AI_SDK_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Vercel_AI_SDK_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Vercel_AI_SDK_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Vercel_AI_SDK_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Vercel_AI_SDK_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Vercel_AI_SDK_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Vercel_AI_SDK_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Vercel_AI_SDK_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Vercel_AI_SDK_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Vercel_AI_SDK_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Vercel_AI_SDK_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Vercel_AI_SDK_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Vercel_AI_SDK_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Vercel_AI_SDK_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Vercel_AI_SDK_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Vercel_AI_SDK_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](Vercel_AI_SDK_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Vercel_AI_SDK_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Vercel_AI_SDK_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](Vercel_AI_SDK_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](Vercel_AI_SDK_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](Vercel_AI_SDK_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 34](Vercel_AI_SDK_-_Tavily_Docs/svg_34.png)
*尺寸: 14x12px*

![SVG图表 35](Vercel_AI_SDK_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](Vercel_AI_SDK_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](Vercel_AI_SDK_-_Tavily_Docs/svg_37.png)
*尺寸: 14x12px*

![SVG图表 38](Vercel_AI_SDK_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](Vercel_AI_SDK_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](Vercel_AI_SDK_-_Tavily_Docs/svg_40.png)
*尺寸: 14x12px*

![SVG图表 41](Vercel_AI_SDK_-_Tavily_Docs/svg_41.png)
*尺寸: 16x16px*

![SVG图表 42](Vercel_AI_SDK_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](Vercel_AI_SDK_-_Tavily_Docs/svg_43.png)
*尺寸: 14x12px*

![SVG图表 44](Vercel_AI_SDK_-_Tavily_Docs/svg_44.png)
*尺寸: 16x16px*

![SVG图表 45](Vercel_AI_SDK_-_Tavily_Docs/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](Vercel_AI_SDK_-_Tavily_Docs/svg_46.png)
*尺寸: 14x12px*

![SVG图表 47](Vercel_AI_SDK_-_Tavily_Docs/svg_47.png)
*尺寸: 16x16px*

![SVG图表 48](Vercel_AI_SDK_-_Tavily_Docs/svg_48.png)
*尺寸: 16x16px*

![SVG图表 49](Vercel_AI_SDK_-_Tavily_Docs/svg_49.png)
*尺寸: 14x12px*

![SVG图表 50](Vercel_AI_SDK_-_Tavily_Docs/svg_50.png)
*尺寸: 14x12px*

![SVG图表 51](Vercel_AI_SDK_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 52](Vercel_AI_SDK_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](Vercel_AI_SDK_-_Tavily_Docs/svg_53.png)
*尺寸: 14x12px*

![SVG图表 54](Vercel_AI_SDK_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](Vercel_AI_SDK_-_Tavily_Docs/svg_55.png)
*尺寸: 16x16px*

![SVG图表 56](Vercel_AI_SDK_-_Tavily_Docs/svg_56.png)
*尺寸: 14x12px*

![SVG图表 57](Vercel_AI_SDK_-_Tavily_Docs/svg_57.png)
*尺寸: 14x14px*

![SVG图表 58](Vercel_AI_SDK_-_Tavily_Docs/svg_58.png)
*尺寸: 14x14px*

![SVG图表 59](Vercel_AI_SDK_-_Tavily_Docs/svg_59.png)
*尺寸: 14x14px*

![SVG图表 64](Vercel_AI_SDK_-_Tavily_Docs/svg_64.png)
*尺寸: 20x20px*

![SVG图表 65](Vercel_AI_SDK_-_Tavily_Docs/svg_65.png)
*尺寸: 20x20px*

![SVG图表 66](Vercel_AI_SDK_-_Tavily_Docs/svg_66.png)
*尺寸: 20x20px*

![SVG图表 67](Vercel_AI_SDK_-_Tavily_Docs/svg_67.png)
*尺寸: 20x20px*

![SVG图表 68](Vercel_AI_SDK_-_Tavily_Docs/svg_68.png)
*尺寸: 49x14px*

![SVG图表 69](Vercel_AI_SDK_-_Tavily_Docs/svg_69.png)
*尺寸: 16x16px*

![SVG图表 70](Vercel_AI_SDK_-_Tavily_Docs/svg_70.png)
*尺寸: 16x16px*

![SVG图表 71](Vercel_AI_SDK_-_Tavily_Docs/svg_71.png)
*尺寸: 16x16px*

![SVG图表 81](Vercel_AI_SDK_-_Tavily_Docs/svg_81.png)
*尺寸: 16x16px*

![SVG图表 82](Vercel_AI_SDK_-_Tavily_Docs/svg_82.png)
*尺寸: 14x14px*

![SVG图表 83](Vercel_AI_SDK_-_Tavily_Docs/svg_83.png)
*尺寸: 16x16px*

![SVG图表 84](Vercel_AI_SDK_-_Tavily_Docs/svg_84.png)
*尺寸: 12x12px*

![SVG图表 85](Vercel_AI_SDK_-_Tavily_Docs/svg_85.png)
*尺寸: 14x14px*

![SVG图表 86](Vercel_AI_SDK_-_Tavily_Docs/svg_86.png)
*尺寸: 16x16px*

![SVG图表 87](Vercel_AI_SDK_-_Tavily_Docs/svg_87.png)
*尺寸: 12x12px*

![SVG图表 88](Vercel_AI_SDK_-_Tavily_Docs/svg_88.png)
*尺寸: 14x14px*

![SVG图表 89](Vercel_AI_SDK_-_Tavily_Docs/svg_89.png)
*尺寸: 16x16px*

![SVG图表 90](Vercel_AI_SDK_-_Tavily_Docs/svg_90.png)
*尺寸: 12x12px*

![SVG图表 91](Vercel_AI_SDK_-_Tavily_Docs/svg_91.png)
*尺寸: 14x14px*
