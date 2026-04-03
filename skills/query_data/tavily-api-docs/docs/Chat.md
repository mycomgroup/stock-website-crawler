---
id: "url-3defb17b"
type: "website"
title: "Chat"
url: "https://docs.tavily.com/examples/use-cases/chat"
description: "Build a conversational chat agent with real-time web search, crawl, and extract capabilities using Tavily's API"
source: ""
tags: []
crawl_time: "2026-03-18T04:11:51.327Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Use Cases"}
    - {"level":5,"text":"Quick Tutorials"}
    - {"level":5,"text":"Open Source"}
    - {"level":1,"text":"Chat"}
    - {"level":2,"text":"[​](https://docs.tavily.com/examples/use-cases/chat#try-our-chatbot)Try Our Chatbot"}
    - {"level":3,"text":"[​](https://docs.tavily.com/examples/use-cases/chat#step-1-get-your-api-key)Step 1: Get Your API Key"}
    - {"level":2,"text":"Get your Tavily API key"}
    - {"level":3,"text":"[​](https://docs.tavily.com/examples/use-cases/chat#step-2-chat-with-tavily)Step 2: Chat with Tavily"}
    - {"level":2,"text":"Launch the application"}
    - {"level":3,"text":"[​](https://docs.tavily.com/examples/use-cases/chat#step-3-read-the-open-source-code)Step 3: Read The Open Source Code"}
    - {"level":2,"text":"View Github Repository"}
    - {"level":2,"text":"[​](https://docs.tavily.com/examples/use-cases/chat#features)Features"}
    - {"level":2,"text":"[​](https://docs.tavily.com/examples/use-cases/chat#how-does-it-work)How Does It Work?"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/examples/use-cases/chat#try-our-chatbot)Try Our Chatbot"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/examples/use-cases/chat#step-1-get-your-api-key)Step 1: Get Your API Key"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/examples/use-cases/chat#step-2-chat-with-tavily)Step 2: Chat with Tavily"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/examples/use-cases/chat#step-3-read-the-open-source-code)Step 3: Read The Open Source Code"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/examples/use-cases/chat#features)Features"}
    - {"type":"list","listType":"ol","items":["**Fast Results**: Tavily’s API delivers quick responses essential for real-time chat experiences.","**Intelligent Parameter Selection**: Dynamically select API parameters based on conversation context using LangChain integration. Specifically designed for agentic systems. All you need is a natural language input, no need to configure structured JSON for our API.","**Content Snippets**: Tavily provides compact summaries of search results in the `content` field, best for maintaining small context sizes in low latency, multi-turn applications.","**Source Attribution**: All search, extract, and crawl results include URLs, enabling easy implementation of citations for transparency and credibility in responses."]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/examples/use-cases/chat#how-does-it-work)How Does It Work?"}
  paragraphs:
    - "1. Code Snippet: Graph Structure"
    - "2. Routing Logic"
    - "3. Memory Management"
    - "4. Real-time Search Integration"
    - "5. Streaming Updates"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Chat](https://docs.tavily.com/examples/use-cases/chat)","[Data Enrichment](https://docs.tavily.com/examples/use-cases/data-enrichment)","[Company Research](https://docs.tavily.com/examples/use-cases/company-research)","[Crawl to RAG](https://docs.tavily.com/examples/use-cases/crawl-to-rag)","[Meeting Prep](https://docs.tavily.com/examples/use-cases/meeting-prep)","[RAG evaluation](https://docs.tavily.com/examples/use-cases/web-eval)","[Market Researcher](https://docs.tavily.com/examples/use-cases/market-researcher)"]}
    - {"type":"ul","items":["[Cookbook](https://docs.tavily.com/examples/quick-tutorials/cookbook)"]}
    - {"type":"ul","items":["[Projects](https://docs.tavily.com/examples/open-sources/projects)"]}
    - {"type":"ul","items":["[Try Our Chatbot](https://docs.tavily.com/examples/use-cases/chat#try-our-chatbot)","[Step 1: Get Your API Key](https://docs.tavily.com/examples/use-cases/chat#step-1-get-your-api-key)","[Step 2: Chat with Tavily](https://docs.tavily.com/examples/use-cases/chat#step-2-chat-with-tavily)","[Step 3: Read The Open Source Code](https://docs.tavily.com/examples/use-cases/chat#step-3-read-the-open-source-code)","[Features](https://docs.tavily.com/examples/use-cases/chat#features)","[How Does It Work?](https://docs.tavily.com/examples/use-cases/chat#how-does-it-work)"]}
    - {"type":"ol","items":["Fast Results: Tavily’s API delivers quick responses essential for real-time chat experiences.","Intelligent Parameter Selection: Dynamically select API parameters based on conversation context using LangChain integration. Specifically designed for agentic systems. All you need is a natural language input, no need to configure structured JSON for our API.","Content Snippets: Tavily provides compact summaries of search results in the content field, best for maintaining small context sizes in low latency, multi-turn applications.","Source Attribution: All search, extract, and crawl results include URLs, enabling easy implementation of citations for transparency and credibility in responses."]}
    - {"type":"ul","items":["Question complexity","Need for current information","Available conversation context"]}
    - {"type":"ul","items":["Preserves context across multiple exchanges","Stores relevant search results for future reference","Manages system prompts and initialization"]}
    - {"type":"ul","items":["Performs targeted web search, extract, or crawl using the LangChain integration","Includes source citations"]}
    - {"type":"ul","items":["Search progress","Response generation","Source processing"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"class WebAgent:\n    def __init__(\n        self,\n    ):\n        self.llm = ChatOpenAI(\n            model=\"gpt-4.1-nano\", api_key=os.getenv(\"OPENAI_API_KEY\")\n        ).with_config({\"tags\": [\"streaming\"]})\n\n        # Define the LangChain search tool\n        self.search = TavilySearch(\n            max_results=10, topic=\"general\", api_key=os.getenv(\"TAVILY_API_KEY\")\n        )\n\n        # Define the LangChain extract tool\n        self.extract = TavilyExtract(\n            extract_depth=\"advanced\", api_key=os.getenv(\"TAVILY_API_KEY\")\n        )\n        # Define the LangChain crawl tool\n        self.crawl = TavilyCrawl(api_key=os.getenv(\"TAVILY_API_KEY\"))\n        self.prompt = PROMPT\n        self.checkpointer = MemorySaver()\n\n    def build_graph(self):\n        \"\"\"\n        Build and compile the LangGraph workflow.\n        \"\"\"\n        return create_react_agent(\n            prompt=self.prompt,\n            model=self.llm,\n            tools=[self.search, self.extract, self.crawl],\n            checkpointer=self.checkpointer,\n        )"}
    - {"language":"text","code":"class WebAgent:\n    def __init__(\n        self,\n    ):\n        self.llm = ChatOpenAI(\n            model=\"gpt-4.1-nano\", api_key=os.getenv(\"OPENAI_API_KEY\")\n        ).with_config({\"tags\": [\"streaming\"]})\n\n        # Define the LangChain search tool\n        self.search = TavilySearch(\n            max_results=10, topic=\"general\", api_key=os.getenv(\"TAVILY_API_KEY\")\n        )\n\n        # Define the LangChain extract tool\n        self.extract = TavilyExtract(\n            extract_depth=\"advanced\", api_key=os.getenv(\"TAVILY_API_KEY\")\n        )\n        # Define the LangChain crawl tool\n        self.crawl = TavilyCrawl(api_key=os.getenv(\"TAVILY_API_KEY\"))\n        self.prompt = PROMPT\n        self.checkpointer = MemorySaver()\n\n    def build_graph(self):\n        \"\"\"\n        Build and compile the LangGraph workflow.\n        \"\"\"\n        return create_react_agent(\n            prompt=self.prompt,\n            model=self.llm,\n            tools=[self.search, self.extract, self.crawl],\n            checkpointer=self.checkpointer,\n        )"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Chat_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Chat_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/tgJqPSjqNVSkMFTO/images/chatbotgif.gif?s=34574620e82d48fe93965035840fca9f","localPath":"Chat_-_Tavily_Docs/image_3.gif","alt":"Tavily Chatbot Demo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/Kondu-1Gs9IHpAYd/images/web-agent.png?fit=max&auto=format&n=Kondu-1Gs9IHpAYd&q=85&s=ab86ef264a4cc606f955be338c03429f","localPath":"Chat_-_Tavily_Docs/image_4.png","alt":"","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Chat_-_Tavily_Docs/image_5.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Chat_-_Tavily_Docs/image_6.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/Kondu-1Gs9IHpAYd/images/web-agent.png?w=840&fit=max&auto=format&n=Kondu-1Gs9IHpAYd&q=85&s=a75700b229e95844d71df3aa4f5ddec7","localPath":"Chat_-_Tavily_Docs/image_7.png","alt":"","title":""}
    - {"src":"https://mintcdn.com/tavilyai/tgJqPSjqNVSkMFTO/images/chatbotgif.gif?s=34574620e82d48fe93965035840fca9f","localPath":"Chat_-_Tavily_Docs/image_8.gif","alt":"Tavily Chatbot Demo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Chat_-_Tavily_Docs/image_9.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Chat_-_Tavily_Docs/image_10.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Chat_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Chat_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Chat_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Chat_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Chat_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Chat_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Chat_-_Tavily_Docs/svg_14.png","width":12,"height":12}
    - {"type":"svg","index":15,"filename":"Chat_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":20,"filename":"Chat_-_Tavily_Docs/svg_20.png","width":14,"height":12}
    - {"type":"svg","index":21,"filename":"Chat_-_Tavily_Docs/svg_21.png","width":14,"height":12}
    - {"type":"svg","index":22,"filename":"Chat_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Chat_-_Tavily_Docs/svg_23.png","width":24,"height":24}
    - {"type":"svg","index":24,"filename":"Chat_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Chat_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Chat_-_Tavily_Docs/svg_26.png","width":24,"height":24}
    - {"type":"svg","index":27,"filename":"Chat_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Chat_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Chat_-_Tavily_Docs/svg_29.png","width":24,"height":24}
    - {"type":"svg","index":30,"filename":"Chat_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"Chat_-_Tavily_Docs/svg_31.png","width":14,"height":12}
    - {"type":"svg","index":33,"filename":"Chat_-_Tavily_Docs/svg_33.png","width":12,"height":12}
    - {"type":"svg","index":34,"filename":"Chat_-_Tavily_Docs/svg_34.png","width":14,"height":18}
    - {"type":"svg","index":35,"filename":"Chat_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"Chat_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Chat_-_Tavily_Docs/svg_37.png","width":12,"height":12}
    - {"type":"svg","index":38,"filename":"Chat_-_Tavily_Docs/svg_38.png","width":12,"height":12}
    - {"type":"svg","index":39,"filename":"Chat_-_Tavily_Docs/svg_39.png","width":12,"height":12}
    - {"type":"svg","index":40,"filename":"Chat_-_Tavily_Docs/svg_40.png","width":12,"height":12}
    - {"type":"svg","index":41,"filename":"Chat_-_Tavily_Docs/svg_41.png","width":14,"height":14}
    - {"type":"svg","index":42,"filename":"Chat_-_Tavily_Docs/svg_42.png","width":14,"height":14}
    - {"type":"svg","index":47,"filename":"Chat_-_Tavily_Docs/svg_47.png","width":20,"height":20}
    - {"type":"svg","index":48,"filename":"Chat_-_Tavily_Docs/svg_48.png","width":20,"height":20}
    - {"type":"svg","index":49,"filename":"Chat_-_Tavily_Docs/svg_49.png","width":20,"height":20}
    - {"type":"svg","index":50,"filename":"Chat_-_Tavily_Docs/svg_50.png","width":20,"height":20}
    - {"type":"svg","index":51,"filename":"Chat_-_Tavily_Docs/svg_51.png","width":49,"height":14}
    - {"type":"svg","index":52,"filename":"Chat_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"Chat_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":54,"filename":"Chat_-_Tavily_Docs/svg_54.png","width":16,"height":16}
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

# Chat

## 源URL

https://docs.tavily.com/examples/use-cases/chat

## 描述

Build a conversational chat agent with real-time web search, crawl, and extract capabilities using Tavily's API

## 内容

### Try Our Chatbot

#### Step 1: Get Your API Key

#### Step 2: Chat with Tavily

#### Step 3: Read The Open Source Code

### Features

1. **Fast Results**: Tavily’s API delivers quick responses essential for real-time chat experiences.
2. **Intelligent Parameter Selection**: Dynamically select API parameters based on conversation context using LangChain integration. Specifically designed for agentic systems. All you need is a natural language input, no need to configure structured JSON for our API.
3. **Content Snippets**: Tavily provides compact summaries of search results in the `content` field, best for maintaining small context sizes in low latency, multi-turn applications.
4. **Source Attribution**: All search, extract, and crawl results include URLs, enabling easy implementation of citations for transparency and credibility in responses.

### How Does It Work?

## 图片

![light logo](Chat_-_Tavily_Docs/image_1.svg)

![dark logo](Chat_-_Tavily_Docs/image_2.svg)

![Tavily Chatbot Demo](Chat_-_Tavily_Docs/image_3.gif)

![图片](Chat_-_Tavily_Docs/image_4.png)

![light logo](Chat_-_Tavily_Docs/image_5.svg)

![dark logo](Chat_-_Tavily_Docs/image_6.svg)

![图片](Chat_-_Tavily_Docs/image_7.png)

![Tavily Chatbot Demo](Chat_-_Tavily_Docs/image_8.gif)

![tavily-logo](Chat_-_Tavily_Docs/image_9.png)

![Powered by Onetrust](Chat_-_Tavily_Docs/image_10.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Chat_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Chat_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Chat_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Chat_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Chat_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Chat_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Chat_-_Tavily_Docs/svg_14.png)
*尺寸: 12x12px*

![SVG图表 15](Chat_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 20](Chat_-_Tavily_Docs/svg_20.png)
*尺寸: 14x12px*

![SVG图表 21](Chat_-_Tavily_Docs/svg_21.png)
*尺寸: 14x12px*

![SVG图表 22](Chat_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](Chat_-_Tavily_Docs/svg_23.png)
*尺寸: 24x24px*

![SVG图表 24](Chat_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Chat_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Chat_-_Tavily_Docs/svg_26.png)
*尺寸: 24x24px*

![SVG图表 27](Chat_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](Chat_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Chat_-_Tavily_Docs/svg_29.png)
*尺寸: 24x24px*

![SVG图表 30](Chat_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](Chat_-_Tavily_Docs/svg_31.png)
*尺寸: 14x12px*

![SVG图表 33](Chat_-_Tavily_Docs/svg_33.png)
*尺寸: 12x12px*

![SVG图表 34](Chat_-_Tavily_Docs/svg_34.png)
*尺寸: 14x18px*

![SVG图表 35](Chat_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](Chat_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](Chat_-_Tavily_Docs/svg_37.png)
*尺寸: 12x12px*

![SVG图表 38](Chat_-_Tavily_Docs/svg_38.png)
*尺寸: 12x12px*

![SVG图表 39](Chat_-_Tavily_Docs/svg_39.png)
*尺寸: 12x12px*

![SVG图表 40](Chat_-_Tavily_Docs/svg_40.png)
*尺寸: 12x12px*

![SVG图表 41](Chat_-_Tavily_Docs/svg_41.png)
*尺寸: 14x14px*

![SVG图表 42](Chat_-_Tavily_Docs/svg_42.png)
*尺寸: 14x14px*

![SVG图表 47](Chat_-_Tavily_Docs/svg_47.png)
*尺寸: 20x20px*

![SVG图表 48](Chat_-_Tavily_Docs/svg_48.png)
*尺寸: 20x20px*

![SVG图表 49](Chat_-_Tavily_Docs/svg_49.png)
*尺寸: 20x20px*

![SVG图表 50](Chat_-_Tavily_Docs/svg_50.png)
*尺寸: 20x20px*

![SVG图表 51](Chat_-_Tavily_Docs/svg_51.png)
*尺寸: 49x14px*

![SVG图表 52](Chat_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](Chat_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 54](Chat_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*
