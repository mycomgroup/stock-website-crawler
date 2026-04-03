---
id: "url-2feadf4c"
type: "website"
title: "Langflow"
url: "https://docs.tavily.com/documentation/integrations/langflow"
description: "Integrate Tavily with Langflow, an open-source visual framework for building multi-agent and RAG applications."
source: ""
tags: []
crawl_time: "2026-03-18T06:43:53.391Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Langflow"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#installation)Installation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#setting-up-tavily-components-in-langflow)Setting Up Tavily Components in Langflow"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#step-1-launch-langflow)Step 1: Launch Langflow"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#step-2-using-tavily-components)Step 2: Using Tavily Components"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#step-3-configure-your-tavily-api-key)Step 3: Configure Your Tavily API Key"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#example-workflows)Example Workflows"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#basic-search-workflow)Basic Search Workflow"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#content-extraction-workflow)Content Extraction Workflow"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#example-use-cases)Example Use Cases"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langflow#additional-resources)Additional Resources"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#installation)Installation"}
    - {"type":"codeblock","language":"","content":"# Using UV (recommended)\nuv pip install langflow\n\n# Using pip\npip install langflow"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#setting-up-tavily-components-in-langflow)Setting Up Tavily Components in Langflow"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#step-1-launch-langflow)Step 1: Launch Langflow"}
    - {"type":"codeblock","language":"","content":"langflow run"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#step-2-using-tavily-components)Step 2: Using Tavily Components"}
    - {"type":"list","listType":"ol","items":["**Tavily Search API**: Perform web searches and retrieve relevant information\n\nLocated under Tools > Tavily Search API\n**Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nMax Results: Number of results to return\nSearch Depth: “basic” or “advanced”\n*Note: Additional parameters are available in the Controls panel*","Located under Tools > Tavily Search API","**Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nMax Results: Number of results to return\nSearch Depth: “basic” or “advanced”\n*Note: Additional parameters are available in the Controls panel*","Max Results: Number of results to return","Search Depth: “basic” or “advanced”","*Note: Additional parameters are available in the Controls panel*","**Tavily Extract API**: Extract content from web pages\n\nLocated under Tools > Tavily Extract API\n**Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nExtract Depth: “basic” or “advanced”\n*Note: Additional parameters are available in the Controls panel*","Located under Tools > Tavily Extract API","**Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nExtract Depth: “basic” or “advanced”\n*Note: Additional parameters are available in the Controls panel*","Extract Depth: “basic” or “advanced”","*Note: Additional parameters are available in the Controls panel*"]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#step-3-configure-your-tavily-api-key)Step 3: Configure Your Tavily API Key"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#example-workflows)Example Workflows"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#basic-search-workflow)Basic Search Workflow"}
    - {"type":"list","listType":"ol","items":["Add a Tavily Search component to your flow","Connect it to a prompt template","Configure the search parameters","Add an LLM component to process the results","Connect to an output component"]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#content-extraction-workflow)Content Extraction Workflow"}
    - {"type":"list","listType":"ol","items":["Add a Tavily Extract component","Connect it to a URL input","Configure extraction parameters","Add processing components as needed","Connect to your desired output"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#example-use-cases)Example Use Cases"}
    - {"type":"list","listType":"ol","items":["**Research Assistant**\n\nCombine Tavily Search with LLMs for comprehensive research\nExtract and summarize information from multiple sources","Combine Tavily Search with LLMs for comprehensive research","Extract and summarize information from multiple sources","**Content Aggregation**\n\nUse Tavily Extract to gather content from specific websites\nProcess and format the extracted content","Use Tavily Extract to gather content from specific websites","Process and format the extracted content","**Market Intelligence**\n\nCreate workflows for competitive analysis\nMonitor industry trends and news","Create workflows for competitive analysis","Monitor industry trends and news","**Documentation Search**\n\nBuild custom documentation search interfaces\nExtract and format technical documentation","Build custom documentation search interfaces","Extract and format technical documentation"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langflow#additional-resources)Additional Resources"}
    - {"type":"list","listType":"ul","items":["[Langflow GitHub Repository](https://github.com/langflow-ai/langflow)","[Langflow Documentation](https://docs.langflow.org/)"]}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/integrations/langflow#introduction)","[Installation](https://docs.tavily.com/documentation/integrations/langflow#installation)","[Setting Up Tavily Components in Langflow](https://docs.tavily.com/documentation/integrations/langflow#setting-up-tavily-components-in-langflow)","[Step 1: Launch Langflow](https://docs.tavily.com/documentation/integrations/langflow#step-1-launch-langflow)","[Step 2: Using Tavily Components](https://docs.tavily.com/documentation/integrations/langflow#step-2-using-tavily-components)","[Step 3: Configure Your Tavily API Key](https://docs.tavily.com/documentation/integrations/langflow#step-3-configure-your-tavily-api-key)","[Example Workflows](https://docs.tavily.com/documentation/integrations/langflow#example-workflows)","[Basic Search Workflow](https://docs.tavily.com/documentation/integrations/langflow#basic-search-workflow)","[Content Extraction Workflow](https://docs.tavily.com/documentation/integrations/langflow#content-extraction-workflow)","[Example Use Cases](https://docs.tavily.com/documentation/integrations/langflow#example-use-cases)","[Additional Resources](https://docs.tavily.com/documentation/integrations/langflow#additional-resources)"]}
    - {"type":"ol","items":["Tavily Search API: Perform web searches and retrieve relevant information\n\nLocated under Tools > Tavily Search API\nConfiguration Options: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nMax Results: Number of results to return\nSearch Depth: “basic” or “advanced”\nNote: Additional parameters are available in the Controls panel","Located under Tools > Tavily Search API","Configuration Options: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nMax Results: Number of results to return\nSearch Depth: “basic” or “advanced”\nNote: Additional parameters are available in the Controls panel","Max Results: Number of results to return","Search Depth: “basic” or “advanced”","Note: Additional parameters are available in the Controls panel","Tavily Extract API: Extract content from web pages\n\nLocated under Tools > Tavily Extract API\nConfiguration Options: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nExtract Depth: “basic” or “advanced”\nNote: Additional parameters are available in the Controls panel","Located under Tools > Tavily Extract API","Configuration Options: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nExtract Depth: “basic” or “advanced”\nNote: Additional parameters are available in the Controls panel","Extract Depth: “basic” or “advanced”","Note: Additional parameters are available in the Controls panel"]}
    - {"type":"ul","items":["Located under Tools > Tavily Search API","Configuration Options: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nMax Results: Number of results to return\nSearch Depth: “basic” or “advanced”\nNote: Additional parameters are available in the Controls panel","Max Results: Number of results to return","Search Depth: “basic” or “advanced”","Note: Additional parameters are available in the Controls panel"]}
    - {"type":"ul","items":["Max Results: Number of results to return","Search Depth: “basic” or “advanced”","Note: Additional parameters are available in the Controls panel"]}
    - {"type":"ul","items":["Located under Tools > Tavily Extract API","Configuration Options: Select the component and go to “Controls” to access all available settings. Here are some key examples:\n\nExtract Depth: “basic” or “advanced”\nNote: Additional parameters are available in the Controls panel","Extract Depth: “basic” or “advanced”","Note: Additional parameters are available in the Controls panel"]}
    - {"type":"ul","items":["Extract Depth: “basic” or “advanced”","Note: Additional parameters are available in the Controls panel"]}
    - {"type":"ol","items":["Add a Tavily Search component to your flow","Connect it to a prompt template","Configure the search parameters","Add an LLM component to process the results","Connect to an output component"]}
    - {"type":"ol","items":["Add a Tavily Extract component","Connect it to a URL input","Configure extraction parameters","Add processing components as needed","Connect to your desired output"]}
    - {"type":"ol","items":["Research Assistant\n\nCombine Tavily Search with LLMs for comprehensive research\nExtract and summarize information from multiple sources","Combine Tavily Search with LLMs for comprehensive research","Extract and summarize information from multiple sources","Content Aggregation\n\nUse Tavily Extract to gather content from specific websites\nProcess and format the extracted content","Use Tavily Extract to gather content from specific websites","Process and format the extracted content","Market Intelligence\n\nCreate workflows for competitive analysis\nMonitor industry trends and news","Create workflows for competitive analysis","Monitor industry trends and news","Documentation Search\n\nBuild custom documentation search interfaces\nExtract and format technical documentation","Build custom documentation search interfaces","Extract and format technical documentation"]}
    - {"type":"ul","items":["Combine Tavily Search with LLMs for comprehensive research","Extract and summarize information from multiple sources"]}
    - {"type":"ul","items":["Use Tavily Extract to gather content from specific websites","Process and format the extracted content"]}
    - {"type":"ul","items":["Create workflows for competitive analysis","Monitor industry trends and news"]}
    - {"type":"ul","items":["Build custom documentation search interfaces","Extract and format technical documentation"]}
    - {"type":"ul","items":["[Langflow GitHub Repository](https://github.com/langflow-ai/langflow)","[Langflow Documentation](https://docs.langflow.org/)"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"# Using UV (recommended)\nuv pip install langflow\n\n# Using pip\npip install langflow"}
    - {"language":"text","code":"# Using UV (recommended)\nuv pip install langflow\n\n# Using pip\npip install langflow"}
    - {"language":"text","code":"langflow run"}
    - {"language":"text","code":"langflow run"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Langflow_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Langflow_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Langflow_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Langflow_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Langflow_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Langflow_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Langflow_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Langflow_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Langflow_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Langflow_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Langflow_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Langflow_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Langflow_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Langflow_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Langflow_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Langflow_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Langflow_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Langflow_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Langflow_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Langflow_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Langflow_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Langflow_-_Tavily_Docs/svg_26.png","width":14,"height":12}
    - {"type":"svg","index":27,"filename":"Langflow_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Langflow_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Langflow_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Langflow_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"Langflow_-_Tavily_Docs/svg_31.png","width":14,"height":12}
    - {"type":"svg","index":32,"filename":"Langflow_-_Tavily_Docs/svg_32.png","width":14,"height":12}
    - {"type":"svg","index":33,"filename":"Langflow_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"Langflow_-_Tavily_Docs/svg_34.png","width":14,"height":12}
    - {"type":"svg","index":35,"filename":"Langflow_-_Tavily_Docs/svg_35.png","width":14,"height":12}
    - {"type":"svg","index":36,"filename":"Langflow_-_Tavily_Docs/svg_36.png","width":14,"height":12}
    - {"type":"svg","index":37,"filename":"Langflow_-_Tavily_Docs/svg_37.png","width":14,"height":14}
    - {"type":"svg","index":38,"filename":"Langflow_-_Tavily_Docs/svg_38.png","width":14,"height":14}
    - {"type":"svg","index":39,"filename":"Langflow_-_Tavily_Docs/svg_39.png","width":14,"height":14}
    - {"type":"svg","index":44,"filename":"Langflow_-_Tavily_Docs/svg_44.png","width":20,"height":20}
    - {"type":"svg","index":45,"filename":"Langflow_-_Tavily_Docs/svg_45.png","width":20,"height":20}
    - {"type":"svg","index":46,"filename":"Langflow_-_Tavily_Docs/svg_46.png","width":20,"height":20}
    - {"type":"svg","index":47,"filename":"Langflow_-_Tavily_Docs/svg_47.png","width":20,"height":20}
    - {"type":"svg","index":48,"filename":"Langflow_-_Tavily_Docs/svg_48.png","width":49,"height":14}
    - {"type":"svg","index":49,"filename":"Langflow_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"Langflow_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"Langflow_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":61,"filename":"Langflow_-_Tavily_Docs/svg_61.png","width":16,"height":16}
    - {"type":"svg","index":62,"filename":"Langflow_-_Tavily_Docs/svg_62.png","width":14,"height":14}
    - {"type":"svg","index":63,"filename":"Langflow_-_Tavily_Docs/svg_63.png","width":16,"height":16}
    - {"type":"svg","index":64,"filename":"Langflow_-_Tavily_Docs/svg_64.png","width":12,"height":12}
    - {"type":"svg","index":65,"filename":"Langflow_-_Tavily_Docs/svg_65.png","width":14,"height":14}
    - {"type":"svg","index":66,"filename":"Langflow_-_Tavily_Docs/svg_66.png","width":16,"height":16}
    - {"type":"svg","index":67,"filename":"Langflow_-_Tavily_Docs/svg_67.png","width":12,"height":12}
    - {"type":"svg","index":68,"filename":"Langflow_-_Tavily_Docs/svg_68.png","width":14,"height":14}
    - {"type":"svg","index":69,"filename":"Langflow_-_Tavily_Docs/svg_69.png","width":16,"height":16}
    - {"type":"svg","index":70,"filename":"Langflow_-_Tavily_Docs/svg_70.png","width":12,"height":12}
    - {"type":"svg","index":71,"filename":"Langflow_-_Tavily_Docs/svg_71.png","width":14,"height":14}
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

# Langflow

## 源URL

https://docs.tavily.com/documentation/integrations/langflow

## 描述

Integrate Tavily with Langflow, an open-source visual framework for building multi-agent and RAG applications.

## 内容

### Introduction

### Installation

```text
# Using UV (recommended)
uv pip install langflow

# Using pip
pip install langflow
```

### Setting Up Tavily Components in Langflow

#### Step 1: Launch Langflow

```text
langflow run
```

#### Step 2: Using Tavily Components

1. **Tavily Search API**: Perform web searches and retrieve relevant information

Located under Tools > Tavily Search API
**Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:

Max Results: Number of results to return
Search Depth: “basic” or “advanced”
*Note: Additional parameters are available in the Controls panel*
2. Located under Tools > Tavily Search API
3. **Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:

Max Results: Number of results to return
Search Depth: “basic” or “advanced”
*Note: Additional parameters are available in the Controls panel*
4. Max Results: Number of results to return
5. Search Depth: “basic” or “advanced”
6. *Note: Additional parameters are available in the Controls panel*
7. **Tavily Extract API**: Extract content from web pages

Located under Tools > Tavily Extract API
**Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:

Extract Depth: “basic” or “advanced”
*Note: Additional parameters are available in the Controls panel*
8. Located under Tools > Tavily Extract API
9. **Configuration Options**: Select the component and go to “Controls” to access all available settings. Here are some key examples:

Extract Depth: “basic” or “advanced”
*Note: Additional parameters are available in the Controls panel*
10. Extract Depth: “basic” or “advanced”
11. *Note: Additional parameters are available in the Controls panel*

#### Step 3: Configure Your Tavily API Key

### Example Workflows

#### Basic Search Workflow

1. Add a Tavily Search component to your flow
2. Connect it to a prompt template
3. Configure the search parameters
4. Add an LLM component to process the results
5. Connect to an output component

#### Content Extraction Workflow

1. Add a Tavily Extract component
2. Connect it to a URL input
3. Configure extraction parameters
4. Add processing components as needed
5. Connect to your desired output

### Example Use Cases

1. **Research Assistant**

Combine Tavily Search with LLMs for comprehensive research
Extract and summarize information from multiple sources
2. Combine Tavily Search with LLMs for comprehensive research
3. Extract and summarize information from multiple sources
4. **Content Aggregation**

Use Tavily Extract to gather content from specific websites
Process and format the extracted content
5. Use Tavily Extract to gather content from specific websites
6. Process and format the extracted content
7. **Market Intelligence**

Create workflows for competitive analysis
Monitor industry trends and news
8. Create workflows for competitive analysis
9. Monitor industry trends and news
10. **Documentation Search**

Build custom documentation search interfaces
Extract and format technical documentation
11. Build custom documentation search interfaces
12. Extract and format technical documentation

### Additional Resources

- [Langflow GitHub Repository](https://github.com/langflow-ai/langflow)
- [Langflow Documentation](https://docs.langflow.org/)

## 图片

![light logo](Langflow_-_Tavily_Docs/image_1.svg)

![dark logo](Langflow_-_Tavily_Docs/image_2.svg)

![light logo](Langflow_-_Tavily_Docs/image_3.svg)

![dark logo](Langflow_-_Tavily_Docs/image_4.svg)

![tavily-logo](Langflow_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Langflow_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Langflow_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Langflow_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Langflow_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Langflow_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Langflow_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Langflow_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Langflow_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Langflow_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Langflow_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Langflow_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Langflow_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Langflow_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Langflow_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Langflow_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Langflow_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Langflow_-_Tavily_Docs/svg_26.png)
*尺寸: 14x12px*

![SVG图表 27](Langflow_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](Langflow_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Langflow_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Langflow_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](Langflow_-_Tavily_Docs/svg_31.png)
*尺寸: 14x12px*

![SVG图表 32](Langflow_-_Tavily_Docs/svg_32.png)
*尺寸: 14x12px*

![SVG图表 33](Langflow_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 34](Langflow_-_Tavily_Docs/svg_34.png)
*尺寸: 14x12px*

![SVG图表 35](Langflow_-_Tavily_Docs/svg_35.png)
*尺寸: 14x12px*

![SVG图表 36](Langflow_-_Tavily_Docs/svg_36.png)
*尺寸: 14x12px*

![SVG图表 37](Langflow_-_Tavily_Docs/svg_37.png)
*尺寸: 14x14px*

![SVG图表 38](Langflow_-_Tavily_Docs/svg_38.png)
*尺寸: 14x14px*

![SVG图表 39](Langflow_-_Tavily_Docs/svg_39.png)
*尺寸: 14x14px*

![SVG图表 44](Langflow_-_Tavily_Docs/svg_44.png)
*尺寸: 20x20px*

![SVG图表 45](Langflow_-_Tavily_Docs/svg_45.png)
*尺寸: 20x20px*

![SVG图表 46](Langflow_-_Tavily_Docs/svg_46.png)
*尺寸: 20x20px*

![SVG图表 47](Langflow_-_Tavily_Docs/svg_47.png)
*尺寸: 20x20px*

![SVG图表 48](Langflow_-_Tavily_Docs/svg_48.png)
*尺寸: 49x14px*

![SVG图表 49](Langflow_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](Langflow_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](Langflow_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 61](Langflow_-_Tavily_Docs/svg_61.png)
*尺寸: 16x16px*

![SVG图表 62](Langflow_-_Tavily_Docs/svg_62.png)
*尺寸: 14x14px*

![SVG图表 63](Langflow_-_Tavily_Docs/svg_63.png)
*尺寸: 16x16px*

![SVG图表 64](Langflow_-_Tavily_Docs/svg_64.png)
*尺寸: 12x12px*

![SVG图表 65](Langflow_-_Tavily_Docs/svg_65.png)
*尺寸: 14x14px*

![SVG图表 66](Langflow_-_Tavily_Docs/svg_66.png)
*尺寸: 16x16px*

![SVG图表 67](Langflow_-_Tavily_Docs/svg_67.png)
*尺寸: 12x12px*

![SVG图表 68](Langflow_-_Tavily_Docs/svg_68.png)
*尺寸: 14x14px*

![SVG图表 69](Langflow_-_Tavily_Docs/svg_69.png)
*尺寸: 16x16px*

![SVG图表 70](Langflow_-_Tavily_Docs/svg_70.png)
*尺寸: 12x12px*

![SVG图表 71](Langflow_-_Tavily_Docs/svg_71.png)
*尺寸: 14x14px*
