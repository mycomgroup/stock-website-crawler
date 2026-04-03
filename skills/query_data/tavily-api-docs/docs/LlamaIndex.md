---
id: "url-73e8a9fe"
type: "website"
title: "LlamaIndex"
url: "https://docs.tavily.com/integrations/llamaindex"
description: "Search the web from LlamaIndex with Tavily."
source: ""
tags: []
crawl_time: "2026-03-18T04:24:44.007Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"LlamaIndex"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/llamaindex#install-tavily-and-llamaindex)Install Tavily and LlamaIndex"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/llamaindex#usage)Usage"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/llamaindex#install-tavily-and-llamaindex)Install Tavily and LlamaIndex"}
    - {"type":"codeblock","language":"","content":"pip install llama-index-tools-tavily-research llama-index llama-hub tavily-python"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/llamaindex#usage)Usage"}
    - {"type":"codeblock","language":"","content":"from llama_index.tools.tavily_research.base import TavilyToolSpec\nfrom llama_index.agent.openai import OpenAIAgent\n\ntavily_tool = TavilyToolSpec(\n    api_key='tvly-YOUR_API_KEY',\n)\nagent = OpenAIAgent.from_tools(tavily_tool.to_tool_list())\n\nagent.chat('What happened in the latest Burning Man festival?')"}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Install Tavily and LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex#install-tavily-and-llamaindex)","[Usage](https://docs.tavily.com/documentation/integrations/llamaindex#usage)"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install llama-index-tools-tavily-research llama-index llama-hub tavily-python"}
    - {"language":"text","code":"pip install llama-index-tools-tavily-research llama-index llama-hub tavily-python"}
    - {"language":"text","code":"from llama_index.tools.tavily_research.base import TavilyToolSpec\nfrom llama_index.agent.openai import OpenAIAgent\n\ntavily_tool = TavilyToolSpec(\n    api_key='tvly-YOUR_API_KEY',\n)\nagent = OpenAIAgent.from_tools(tavily_tool.to_tool_list())\n\nagent.chat('What happened in the latest Burning Man festival?')"}
    - {"language":"text","code":"from llama_index.tools.tavily_research.base import TavilyToolSpec\nfrom llama_index.agent.openai import OpenAIAgent\n\ntavily_tool = TavilyToolSpec(\n    api_key='tvly-YOUR_API_KEY',\n)\nagent = OpenAIAgent.from_tools(tavily_tool.to_tool_list())\n\nagent.chat('What happened in the latest Burning Man festival?')"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"LlamaIndex_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"LlamaIndex_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"LlamaIndex_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"LlamaIndex_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"LlamaIndex_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"LlamaIndex_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"LlamaIndex_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"LlamaIndex_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"LlamaIndex_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"LlamaIndex_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"LlamaIndex_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"LlamaIndex_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"LlamaIndex_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"LlamaIndex_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"LlamaIndex_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"LlamaIndex_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"LlamaIndex_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"LlamaIndex_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"LlamaIndex_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"LlamaIndex_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"LlamaIndex_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"LlamaIndex_-_Tavily_Docs/svg_26.png","width":14,"height":12}
    - {"type":"svg","index":27,"filename":"LlamaIndex_-_Tavily_Docs/svg_27.png","width":16,"height":16}
    - {"type":"svg","index":28,"filename":"LlamaIndex_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"LlamaIndex_-_Tavily_Docs/svg_29.png","width":14,"height":14}
    - {"type":"svg","index":30,"filename":"LlamaIndex_-_Tavily_Docs/svg_30.png","width":14,"height":14}
    - {"type":"svg","index":31,"filename":"LlamaIndex_-_Tavily_Docs/svg_31.png","width":14,"height":14}
    - {"type":"svg","index":36,"filename":"LlamaIndex_-_Tavily_Docs/svg_36.png","width":20,"height":20}
    - {"type":"svg","index":37,"filename":"LlamaIndex_-_Tavily_Docs/svg_37.png","width":20,"height":20}
    - {"type":"svg","index":38,"filename":"LlamaIndex_-_Tavily_Docs/svg_38.png","width":20,"height":20}
    - {"type":"svg","index":39,"filename":"LlamaIndex_-_Tavily_Docs/svg_39.png","width":20,"height":20}
    - {"type":"svg","index":40,"filename":"LlamaIndex_-_Tavily_Docs/svg_40.png","width":49,"height":14}
    - {"type":"svg","index":41,"filename":"LlamaIndex_-_Tavily_Docs/svg_41.png","width":16,"height":16}
    - {"type":"svg","index":42,"filename":"LlamaIndex_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"LlamaIndex_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"LlamaIndex_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":54,"filename":"LlamaIndex_-_Tavily_Docs/svg_54.png","width":14,"height":14}
    - {"type":"svg","index":55,"filename":"LlamaIndex_-_Tavily_Docs/svg_55.png","width":16,"height":16}
    - {"type":"svg","index":56,"filename":"LlamaIndex_-_Tavily_Docs/svg_56.png","width":12,"height":12}
    - {"type":"svg","index":57,"filename":"LlamaIndex_-_Tavily_Docs/svg_57.png","width":14,"height":14}
    - {"type":"svg","index":58,"filename":"LlamaIndex_-_Tavily_Docs/svg_58.png","width":16,"height":16}
    - {"type":"svg","index":59,"filename":"LlamaIndex_-_Tavily_Docs/svg_59.png","width":12,"height":12}
    - {"type":"svg","index":60,"filename":"LlamaIndex_-_Tavily_Docs/svg_60.png","width":14,"height":14}
    - {"type":"svg","index":61,"filename":"LlamaIndex_-_Tavily_Docs/svg_61.png","width":16,"height":16}
    - {"type":"svg","index":62,"filename":"LlamaIndex_-_Tavily_Docs/svg_62.png","width":12,"height":12}
    - {"type":"svg","index":63,"filename":"LlamaIndex_-_Tavily_Docs/svg_63.png","width":14,"height":14}
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

# LlamaIndex

## 源URL

https://docs.tavily.com/integrations/llamaindex

## 描述

Search the web from LlamaIndex with Tavily.

## 内容

### Install Tavily and LlamaIndex

```text
pip install llama-index-tools-tavily-research llama-index llama-hub tavily-python
```

### Usage

```text
from llama_index.tools.tavily_research.base import TavilyToolSpec
from llama_index.agent.openai import OpenAIAgent

tavily_tool = TavilyToolSpec(
    api_key='tvly-YOUR_API_KEY',
)
agent = OpenAIAgent.from_tools(tavily_tool.to_tool_list())

agent.chat('What happened in the latest Burning Man festival?')
```

## 图片

![light logo](LlamaIndex_-_Tavily_Docs/image_1.svg)

![dark logo](LlamaIndex_-_Tavily_Docs/image_2.svg)

![light logo](LlamaIndex_-_Tavily_Docs/image_3.svg)

![dark logo](LlamaIndex_-_Tavily_Docs/image_4.svg)

![tavily-logo](LlamaIndex_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](LlamaIndex_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](LlamaIndex_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](LlamaIndex_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](LlamaIndex_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](LlamaIndex_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](LlamaIndex_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](LlamaIndex_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](LlamaIndex_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](LlamaIndex_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](LlamaIndex_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](LlamaIndex_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](LlamaIndex_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](LlamaIndex_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](LlamaIndex_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](LlamaIndex_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](LlamaIndex_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](LlamaIndex_-_Tavily_Docs/svg_26.png)
*尺寸: 14x12px*

![SVG图表 27](LlamaIndex_-_Tavily_Docs/svg_27.png)
*尺寸: 16x16px*

![SVG图表 28](LlamaIndex_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](LlamaIndex_-_Tavily_Docs/svg_29.png)
*尺寸: 14x14px*

![SVG图表 30](LlamaIndex_-_Tavily_Docs/svg_30.png)
*尺寸: 14x14px*

![SVG图表 31](LlamaIndex_-_Tavily_Docs/svg_31.png)
*尺寸: 14x14px*

![SVG图表 36](LlamaIndex_-_Tavily_Docs/svg_36.png)
*尺寸: 20x20px*

![SVG图表 37](LlamaIndex_-_Tavily_Docs/svg_37.png)
*尺寸: 20x20px*

![SVG图表 38](LlamaIndex_-_Tavily_Docs/svg_38.png)
*尺寸: 20x20px*

![SVG图表 39](LlamaIndex_-_Tavily_Docs/svg_39.png)
*尺寸: 20x20px*

![SVG图表 40](LlamaIndex_-_Tavily_Docs/svg_40.png)
*尺寸: 49x14px*

![SVG图表 41](LlamaIndex_-_Tavily_Docs/svg_41.png)
*尺寸: 16x16px*

![SVG图表 42](LlamaIndex_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](LlamaIndex_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 53](LlamaIndex_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 54](LlamaIndex_-_Tavily_Docs/svg_54.png)
*尺寸: 14x14px*

![SVG图表 55](LlamaIndex_-_Tavily_Docs/svg_55.png)
*尺寸: 16x16px*

![SVG图表 56](LlamaIndex_-_Tavily_Docs/svg_56.png)
*尺寸: 12x12px*

![SVG图表 57](LlamaIndex_-_Tavily_Docs/svg_57.png)
*尺寸: 14x14px*

![SVG图表 58](LlamaIndex_-_Tavily_Docs/svg_58.png)
*尺寸: 16x16px*

![SVG图表 59](LlamaIndex_-_Tavily_Docs/svg_59.png)
*尺寸: 12x12px*

![SVG图表 60](LlamaIndex_-_Tavily_Docs/svg_60.png)
*尺寸: 14x14px*

![SVG图表 61](LlamaIndex_-_Tavily_Docs/svg_61.png)
*尺寸: 16x16px*

![SVG图表 62](LlamaIndex_-_Tavily_Docs/svg_62.png)
*尺寸: 12x12px*

![SVG图表 63](LlamaIndex_-_Tavily_Docs/svg_63.png)
*尺寸: 14x14px*
