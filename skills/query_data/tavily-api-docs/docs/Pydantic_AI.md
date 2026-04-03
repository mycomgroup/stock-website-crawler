---
id: "url-15ab0081"
type: "website"
title: "Pydantic AI"
url: "https://docs.tavily.com/documentation/integrations/pydantic-ai"
description: "Tavily is now available for integration through Pydantic AI."
source: ""
tags: []
crawl_time: "2026-03-18T07:11:09.278Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Pydantic AI"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-by-step-integration-guide)Step-by-Step Integration Guide"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-1-install-required-packages)Step 1: Install Required Packages"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-2-set-up-api-keys)Step 2: Set Up API Keys"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-3-initialize-pydantic-ai-agent-with-tavily-tools)Step 3: Initialize Pydantic AI Agent with Tavily Tools"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-4-example-use-cases)Step 4: Example Use Cases"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#additional-use-cases)Additional Use Cases"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-by-step-integration-guide)Step-by-Step Integration Guide"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-1-install-required-packages)Step 1: Install Required Packages"}
    - {"type":"codeblock","language":"","content":"pip install \"pydantic-ai-slim[tavily]\""}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-2-set-up-api-keys)Step 2: Set Up API Keys"}
    - {"type":"list","listType":"ul","items":["**Tavily API Key:** [Get your Tavily API key here](https://app.tavily.com/home)"]}
    - {"type":"codeblock","language":"","content":"export TAVILY_API_KEY=your_tavily_api_key"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-3-initialize-pydantic-ai-agent-with-tavily-tools)Step 3: Initialize Pydantic AI Agent with Tavily Tools"}
    - {"type":"codeblock","language":"","content":"import os\nfrom pydantic_ai.agent import Agent\nfrom pydantic_ai.common_tools.tavily import tavily_search_tool\n\n# Get API key from environment\napi_key = os.getenv('TAVILY_API_KEY')\nassert api_key is not None\n\n# Initialize the agent with Tavily tools\nagent = Agent(\n    'openai:o3-mini',\n    tools=[tavily_search_tool(api_key)],\n    system_prompt='Search Tavily for the given query and return the results.'\n)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-4-example-use-cases)Step 4: Example Use Cases"}
    - {"type":"codeblock","language":"","content":"# Example 1: Basic search for news\nresult = agent.run_sync('Tell me the top news in the GenAI world, give me links.')\nprint(result.output)"}
    - {"type":"codeblock","language":"","content":"Here are some of the top recent news articles related to GenAI:\n\n1. How CLEAR users can improve risk analysis with GenAI – Thomson Reuters\n   Read more: https://legal.thomsonreuters.com/blog/how-clear-users-can-improve-risk-analysis-with-genai/\n   (This article discusses how CLEAR's new GenAI-powered tool streamlines risk analysis by quickly summarizing key information from various public data sources.)\n\n2. TELUS Digital Survey Reveals Enterprise Employees Are Entering Sensitive Data Into AI Assistants More Than You Think – FT.com\n   Read more: https://markets.ft.com/data/announce/detail?dockey=600-202502260645BIZWIRE_USPRX____20250226_BW490609-1\n   (This news piece highlights findings from a TELUS Digital survey showing that many enterprise employees use public GenAI tools and sometimes even enter sensitive data.)\n\n3. The Essential Guide to Generative AI – Virtualization Review\n   Read more: https://virtualizationreview.com/Whitepapers/2025/02/SNOWFLAKE-The-Essential-Guide-to-Generative-AI.aspx\n   (This guide provides insights into how GenAI is revolutionizing enterprise strategies and productivity, with input from industry leaders.)"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/pydantic-ai#additional-use-cases)Additional Use Cases"}
    - {"type":"list","listType":"ol","items":["**Content Curation**: Gather and organize information from multiple sources","**Real-time Data Integration**: Keep your AI agents up-to-date with the latest information","**Technical Documentation**: Search and analyze technical documentation","**Market Analysis**: Conduct comprehensive market research and analysis"]}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/integrations/pydantic-ai#introduction)","[Step-by-Step Integration Guide](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-by-step-integration-guide)","[Step 1: Install Required Packages](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-1-install-required-packages)","[Step 2: Set Up API Keys](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-2-set-up-api-keys)","[Step 3: Initialize Pydantic AI Agent with Tavily Tools](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-3-initialize-pydantic-ai-agent-with-tavily-tools)","[Step 4: Example Use Cases](https://docs.tavily.com/documentation/integrations/pydantic-ai#step-4-example-use-cases)","[Additional Use Cases](https://docs.tavily.com/documentation/integrations/pydantic-ai#additional-use-cases)"]}
    - {"type":"ul","items":["Tavily API Key: [Get your Tavily API key here](https://app.tavily.com/home)"]}
    - {"type":"ol","items":["Content Curation: Gather and organize information from multiple sources","Real-time Data Integration: Keep your AI agents up-to-date with the latest information","Technical Documentation: Search and analyze technical documentation","Market Analysis: Conduct comprehensive market research and analysis"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install \"pydantic-ai-slim[tavily]\""}
    - {"language":"text","code":"pip install \"pydantic-ai-slim[tavily]\""}
    - {"language":"text","code":"export TAVILY_API_KEY=your_tavily_api_key"}
    - {"language":"text","code":"export TAVILY_API_KEY=your_tavily_api_key"}
    - {"language":"text","code":"import os\nfrom pydantic_ai.agent import Agent\nfrom pydantic_ai.common_tools.tavily import tavily_search_tool\n\n# Get API key from environment\napi_key = os.getenv('TAVILY_API_KEY')\nassert api_key is not None\n\n# Initialize the agent with Tavily tools\nagent = Agent(\n    'openai:o3-mini',\n    tools=[tavily_search_tool(api_key)],\n    system_prompt='Search Tavily for the given query and return the results.'\n)"}
    - {"language":"text","code":"import os\nfrom pydantic_ai.agent import Agent\nfrom pydantic_ai.common_tools.tavily import tavily_search_tool\n\n# Get API key from environment\napi_key = os.getenv('TAVILY_API_KEY')\nassert api_key is not None\n\n# Initialize the agent with Tavily tools\nagent = Agent(\n    'openai:o3-mini',\n    tools=[tavily_search_tool(api_key)],\n    system_prompt='Search Tavily for the given query and return the results.'\n)"}
    - {"language":"text","code":"# Example 1: Basic search for news\nresult = agent.run_sync('Tell me the top news in the GenAI world, give me links.')\nprint(result.output)"}
    - {"language":"text","code":"# Example 1: Basic search for news\nresult = agent.run_sync('Tell me the top news in the GenAI world, give me links.')\nprint(result.output)"}
    - {"language":"text","code":"Here are some of the top recent news articles related to GenAI:\n\n1. How CLEAR users can improve risk analysis with GenAI – Thomson Reuters\n   Read more: https://legal.thomsonreuters.com/blog/how-clear-users-can-improve-risk-analysis-with-genai/\n   (This article discusses how CLEAR's new GenAI-powered tool streamlines risk analysis by quickly summarizing key information from various public data sources.)\n\n2. TELUS Digital Survey Reveals Enterprise Employees Are Entering Sensitive Data Into AI Assistants More Than You Think – FT.com\n   Read more: https://markets.ft.com/data/announce/detail?dockey=600-202502260645BIZWIRE_USPRX____20250226_BW490609-1\n   (This news piece highlights findings from a TELUS Digital survey showing that many enterprise employees use public GenAI tools and sometimes even enter sensitive data.)\n\n3. The Essential Guide to Generative AI – Virtualization Review\n   Read more: https://virtualizationreview.com/Whitepapers/2025/02/SNOWFLAKE-The-Essential-Guide-to-Generative-AI.aspx\n   (This guide provides insights into how GenAI is revolutionizing enterprise strategies and productivity, with input from industry leaders.)"}
    - {"language":"text","code":"Here are some of the top recent news articles related to GenAI:\n\n1. How CLEAR users can improve risk analysis with GenAI – Thomson Reuters\n   Read more: https://legal.thomsonreuters.com/blog/how-clear-users-can-improve-risk-analysis-with-genai/\n   (This article discusses how CLEAR's new GenAI-powered tool streamlines risk analysis by quickly summarizing key information from various public data sources.)\n\n2. TELUS Digital Survey Reveals Enterprise Employees Are Entering Sensitive Data Into AI Assistants More Than You Think – FT.com\n   Read more: https://markets.ft.com/data/announce/detail?dockey=600-202502260645BIZWIRE_USPRX____20250226_BW490609-1\n   (This news piece highlights findings from a TELUS Digital survey showing that many enterprise employees use public GenAI tools and sometimes even enter sensitive data.)\n\n3. The Essential Guide to Generative AI – Virtualization Review\n   Read more: https://virtualizationreview.com/Whitepapers/2025/02/SNOWFLAKE-The-Essential-Guide-to-Generative-AI.aspx\n   (This guide provides insights into how GenAI is revolutionizing enterprise strategies and productivity, with input from industry leaders.)"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Pydantic_AI_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Pydantic_AI_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Pydantic_AI_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Pydantic_AI_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Pydantic_AI_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Pydantic_AI_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Pydantic_AI_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Pydantic_AI_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Pydantic_AI_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Pydantic_AI_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Pydantic_AI_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Pydantic_AI_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Pydantic_AI_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Pydantic_AI_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Pydantic_AI_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Pydantic_AI_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Pydantic_AI_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Pydantic_AI_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Pydantic_AI_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Pydantic_AI_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Pydantic_AI_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Pydantic_AI_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Pydantic_AI_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Pydantic_AI_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Pydantic_AI_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Pydantic_AI_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"Pydantic_AI_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"Pydantic_AI_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"Pydantic_AI_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"Pydantic_AI_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Pydantic_AI_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"Pydantic_AI_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Pydantic_AI_-_Tavily_Docs/svg_37.png","width":16,"height":16}
    - {"type":"svg","index":38,"filename":"Pydantic_AI_-_Tavily_Docs/svg_38.png","width":14,"height":12}
    - {"type":"svg","index":39,"filename":"Pydantic_AI_-_Tavily_Docs/svg_39.png","width":14,"height":14}
    - {"type":"svg","index":40,"filename":"Pydantic_AI_-_Tavily_Docs/svg_40.png","width":14,"height":14}
    - {"type":"svg","index":41,"filename":"Pydantic_AI_-_Tavily_Docs/svg_41.png","width":14,"height":14}
    - {"type":"svg","index":46,"filename":"Pydantic_AI_-_Tavily_Docs/svg_46.png","width":20,"height":20}
    - {"type":"svg","index":47,"filename":"Pydantic_AI_-_Tavily_Docs/svg_47.png","width":20,"height":20}
    - {"type":"svg","index":48,"filename":"Pydantic_AI_-_Tavily_Docs/svg_48.png","width":20,"height":20}
    - {"type":"svg","index":49,"filename":"Pydantic_AI_-_Tavily_Docs/svg_49.png","width":20,"height":20}
    - {"type":"svg","index":50,"filename":"Pydantic_AI_-_Tavily_Docs/svg_50.png","width":49,"height":14}
    - {"type":"svg","index":51,"filename":"Pydantic_AI_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"Pydantic_AI_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"Pydantic_AI_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":63,"filename":"Pydantic_AI_-_Tavily_Docs/svg_63.png","width":16,"height":16}
    - {"type":"svg","index":64,"filename":"Pydantic_AI_-_Tavily_Docs/svg_64.png","width":14,"height":14}
    - {"type":"svg","index":65,"filename":"Pydantic_AI_-_Tavily_Docs/svg_65.png","width":16,"height":16}
    - {"type":"svg","index":66,"filename":"Pydantic_AI_-_Tavily_Docs/svg_66.png","width":12,"height":12}
    - {"type":"svg","index":67,"filename":"Pydantic_AI_-_Tavily_Docs/svg_67.png","width":14,"height":14}
    - {"type":"svg","index":68,"filename":"Pydantic_AI_-_Tavily_Docs/svg_68.png","width":16,"height":16}
    - {"type":"svg","index":69,"filename":"Pydantic_AI_-_Tavily_Docs/svg_69.png","width":12,"height":12}
    - {"type":"svg","index":70,"filename":"Pydantic_AI_-_Tavily_Docs/svg_70.png","width":14,"height":14}
    - {"type":"svg","index":71,"filename":"Pydantic_AI_-_Tavily_Docs/svg_71.png","width":16,"height":16}
    - {"type":"svg","index":72,"filename":"Pydantic_AI_-_Tavily_Docs/svg_72.png","width":12,"height":12}
    - {"type":"svg","index":73,"filename":"Pydantic_AI_-_Tavily_Docs/svg_73.png","width":14,"height":14}
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

# Pydantic AI

## 源URL

https://docs.tavily.com/documentation/integrations/pydantic-ai

## 描述

Tavily is now available for integration through Pydantic AI.

## 内容

### Introduction

### Step-by-Step Integration Guide

#### Step 1: Install Required Packages

```text
pip install "pydantic-ai-slim[tavily]"
```

#### Step 2: Set Up API Keys

- **Tavily API Key:** [Get your Tavily API key here](https://app.tavily.com/home)

```text
export TAVILY_API_KEY=your_tavily_api_key
```

#### Step 3: Initialize Pydantic AI Agent with Tavily Tools

```text
import os
from pydantic_ai.agent import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

# Get API key from environment
api_key = os.getenv('TAVILY_API_KEY')
assert api_key is not None

# Initialize the agent with Tavily tools
agent = Agent(
    'openai:o3-mini',
    tools=[tavily_search_tool(api_key)],
    system_prompt='Search Tavily for the given query and return the results.'
)
```

#### Step 4: Example Use Cases

```text
# Example 1: Basic search for news
result = agent.run_sync('Tell me the top news in the GenAI world, give me links.')
print(result.output)
```

```text
Here are some of the top recent news articles related to GenAI:

1. How CLEAR users can improve risk analysis with GenAI – Thomson Reuters
   Read more: https://legal.thomsonreuters.com/blog/how-clear-users-can-improve-risk-analysis-with-genai/
   (This article discusses how CLEAR's new GenAI-powered tool streamlines risk analysis by quickly summarizing key information from various public data sources.)

2. TELUS Digital Survey Reveals Enterprise Employees Are Entering Sensitive Data Into AI Assistants More Than You Think – FT.com
   Read more: https://markets.ft.com/data/announce/detail?dockey=600-202502260645BIZWIRE_USPRX____20250226_BW490609-1
   (This news piece highlights findings from a TELUS Digital survey showing that many enterprise employees use public GenAI tools and sometimes even enter sensitive data.)

3. The Essential Guide to Generative AI – Virtualization Review
   Read more: https://virtualizationreview.com/Whitepapers/2025/02/SNOWFLAKE-The-Essential-Guide-to-Generative-AI.aspx
   (This guide provides insights into how GenAI is revolutionizing enterprise strategies and productivity, with input from industry leaders.)
```

### Additional Use Cases

1. **Content Curation**: Gather and organize information from multiple sources
2. **Real-time Data Integration**: Keep your AI agents up-to-date with the latest information
3. **Technical Documentation**: Search and analyze technical documentation
4. **Market Analysis**: Conduct comprehensive market research and analysis

## 图片

![light logo](Pydantic_AI_-_Tavily_Docs/image_1.svg)

![dark logo](Pydantic_AI_-_Tavily_Docs/image_2.svg)

![light logo](Pydantic_AI_-_Tavily_Docs/image_3.svg)

![dark logo](Pydantic_AI_-_Tavily_Docs/image_4.svg)

![tavily-logo](Pydantic_AI_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Pydantic_AI_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Pydantic_AI_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Pydantic_AI_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Pydantic_AI_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Pydantic_AI_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Pydantic_AI_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Pydantic_AI_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Pydantic_AI_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Pydantic_AI_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Pydantic_AI_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Pydantic_AI_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Pydantic_AI_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Pydantic_AI_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Pydantic_AI_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Pydantic_AI_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Pydantic_AI_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Pydantic_AI_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Pydantic_AI_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](Pydantic_AI_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Pydantic_AI_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Pydantic_AI_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](Pydantic_AI_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](Pydantic_AI_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](Pydantic_AI_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 34](Pydantic_AI_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Pydantic_AI_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](Pydantic_AI_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](Pydantic_AI_-_Tavily_Docs/svg_37.png)
*尺寸: 16x16px*

![SVG图表 38](Pydantic_AI_-_Tavily_Docs/svg_38.png)
*尺寸: 14x12px*

![SVG图表 39](Pydantic_AI_-_Tavily_Docs/svg_39.png)
*尺寸: 14x14px*

![SVG图表 40](Pydantic_AI_-_Tavily_Docs/svg_40.png)
*尺寸: 14x14px*

![SVG图表 41](Pydantic_AI_-_Tavily_Docs/svg_41.png)
*尺寸: 14x14px*

![SVG图表 46](Pydantic_AI_-_Tavily_Docs/svg_46.png)
*尺寸: 20x20px*

![SVG图表 47](Pydantic_AI_-_Tavily_Docs/svg_47.png)
*尺寸: 20x20px*

![SVG图表 48](Pydantic_AI_-_Tavily_Docs/svg_48.png)
*尺寸: 20x20px*

![SVG图表 49](Pydantic_AI_-_Tavily_Docs/svg_49.png)
*尺寸: 20x20px*

![SVG图表 50](Pydantic_AI_-_Tavily_Docs/svg_50.png)
*尺寸: 49x14px*

![SVG图表 51](Pydantic_AI_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 52](Pydantic_AI_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](Pydantic_AI_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 63](Pydantic_AI_-_Tavily_Docs/svg_63.png)
*尺寸: 16x16px*

![SVG图表 64](Pydantic_AI_-_Tavily_Docs/svg_64.png)
*尺寸: 14x14px*

![SVG图表 65](Pydantic_AI_-_Tavily_Docs/svg_65.png)
*尺寸: 16x16px*

![SVG图表 66](Pydantic_AI_-_Tavily_Docs/svg_66.png)
*尺寸: 12x12px*

![SVG图表 67](Pydantic_AI_-_Tavily_Docs/svg_67.png)
*尺寸: 14x14px*

![SVG图表 68](Pydantic_AI_-_Tavily_Docs/svg_68.png)
*尺寸: 16x16px*

![SVG图表 69](Pydantic_AI_-_Tavily_Docs/svg_69.png)
*尺寸: 12x12px*

![SVG图表 70](Pydantic_AI_-_Tavily_Docs/svg_70.png)
*尺寸: 14x14px*

![SVG图表 71](Pydantic_AI_-_Tavily_Docs/svg_71.png)
*尺寸: 16x16px*

![SVG图表 72](Pydantic_AI_-_Tavily_Docs/svg_72.png)
*尺寸: 12x12px*

![SVG图表 73](Pydantic_AI_-_Tavily_Docs/svg_73.png)
*尺寸: 14x14px*
