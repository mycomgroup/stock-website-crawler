---
id: "url-37f82436"
type: "website"
title: "Tavily Agent Skills"
url: "https://docs.tavily.com/documentation/agent-skills"
description: "Official skills that define best practices for working with the Tavily API. Useful for AI agents like Claude Code, Codex, or Cursor."
source: ""
tags: []
crawl_time: "2026-03-18T04:28:45.961Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Tavily Agent Skills"}
    - {"level":2,"text":"GitHub"}
    - {"level":2,"text":"Get API Key"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/agent-skills#why-use-these-skills)Why Use These Skills?"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/agent-skills#what-you-can-build)What You Can Build"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/agent-skills#installation)Installation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#prerequisites)Prerequisites"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#step-1-configure-your-api-key)Step 1: Configure Your API Key"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#step-2-install-the-skills)Step 2: Install the Skills"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#step-3-restart-your-agent)Step 3: Restart Your Agent"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/agent-skills#available-skills)Available Skills"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/agent-skills#usage-examples)Usage Examples"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#automatic-skill-invocation)Automatic Skill Invocation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#explicit-skill-invocation)Explicit Skill Invocation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/agent-skills#claude-code-plugin)Claude Code Plugin"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#step-1-configure-your-api-key-2)Step 1: Configure Your API Key"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#step-2-install-the-skills-2)Step 2: Install the Skills"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/agent-skills#step-3-restart-claude-code)Step 3: Restart Claude Code"}
  mainContent:
    - {"type":"heading","level":2,"content":"GitHub"}
    - {"type":"heading","level":2,"content":"Get API Key"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/agent-skills#why-use-these-skills)Why Use These Skills?"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/agent-skills#what-you-can-build)What You Can Build"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/agent-skills#installation)Installation"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#prerequisites)Prerequisites"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#step-1-configure-your-api-key)Step 1: Configure Your API Key"}
    - {"type":"codeblock","language":"","content":"# Open your Claude settings file\nopen -e \"$HOME/.claude/settings.json\"\n\n# Or with VS Code\ncode \"$HOME/.claude/settings.json\""}
    - {"type":"codeblock","language":"","content":"{\n  \"env\": {\n    \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY\"\n  }\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#step-2-install-the-skills)Step 2: Install the Skills"}
    - {"type":"codeblock","language":"","content":"npx skills add tavily-ai/skills"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#step-3-restart-your-agent)Step 3: Restart Your Agent"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/agent-skills#available-skills)Available Skills"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/agent-skills#usage-examples)Usage Examples"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#automatic-skill-invocation)Automatic Skill Invocation"}
    - {"type":"codeblock","language":"","content":"Research the latest developments in AI agents and summarize the key trends"}
    - {"type":"codeblock","language":"","content":"Search for the latest news on AI regulations"}
    - {"type":"codeblock","language":"","content":"Crawl the Stripe API docs and save them locally"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#explicit-skill-invocation)Explicit Skill Invocation"}
    - {"type":"codeblock","language":"","content":"/research AI agent frameworks and save to report.json"}
    - {"type":"codeblock","language":"","content":"/search current React best practices"}
    - {"type":"codeblock","language":"","content":"/crawl https://docs.example.com"}
    - {"type":"codeblock","language":"","content":"/extract https://example.com/blog/post"}
    - {"type":"codeblock","language":"","content":"/tavily-best-practices"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/agent-skills#claude-code-plugin)Claude Code Plugin"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#step-1-configure-your-api-key-2)Step 1: Configure Your API Key"}
    - {"type":"codeblock","language":"","content":"code ~/.claude/settings.json"}
    - {"type":"codeblock","language":"","content":"{\n  \"env\": {\n    \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY\"\n  }\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#step-2-install-the-skills-2)Step 2: Install the Skills"}
    - {"type":"codeblock","language":"","content":"/plugin marketplace add tavily-ai/skills"}
    - {"type":"codeblock","language":"","content":"/plugin install tavily@skills"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/agent-skills#step-3-restart-claude-code)Step 3: Restart Claude Code"}
    - {"type":"codeblock","language":"","content":"/clear"}
  paragraphs:
    - "AI Chatbot with Real-Time Search"
    - "News Dashboard with Sentiment Analysis"
    - "Lead Enrichment Tool"
    - "Competitive Intelligence Agent"
    - "Required"
    - "Tavily Best Practices"
    - "Search"
    - "Research"
    - "Crawl"
    - "Extract"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Why Use These Skills?](https://docs.tavily.com/documentation/agent-skills#why-use-these-skills)","[What You Can Build](https://docs.tavily.com/documentation/agent-skills#what-you-can-build)","[Installation](https://docs.tavily.com/documentation/agent-skills#installation)","[Prerequisites](https://docs.tavily.com/documentation/agent-skills#prerequisites)","[Step 1: Configure Your API Key](https://docs.tavily.com/documentation/agent-skills#step-1-configure-your-api-key)","[Step 2: Install the Skills](https://docs.tavily.com/documentation/agent-skills#step-2-install-the-skills)","[Step 3: Restart Your Agent](https://docs.tavily.com/documentation/agent-skills#step-3-restart-your-agent)","[Available Skills](https://docs.tavily.com/documentation/agent-skills#available-skills)","[Usage Examples](https://docs.tavily.com/documentation/agent-skills#usage-examples)","[Automatic Skill Invocation](https://docs.tavily.com/documentation/agent-skills#automatic-skill-invocation)","[Explicit Skill Invocation](https://docs.tavily.com/documentation/agent-skills#explicit-skill-invocation)","[Claude Code Plugin](https://docs.tavily.com/documentation/agent-skills#claude-code-plugin)","[Step 1: Configure Your API Key](https://docs.tavily.com/documentation/agent-skills#step-1-configure-your-api-key-2)","[Step 2: Install the Skills](https://docs.tavily.com/documentation/agent-skills#step-2-install-the-skills-2)","[Step 3: Restart Claude Code](https://docs.tavily.com/documentation/agent-skills#step-3-restart-claude-code)"]}
    - {"type":"ul","items":["[Tavily API key](https://app.tavily.com/home) - Sign up for free","An AI agent that supports skills (Claude Code, Codex, Cursor, etc.)"]}
    - {"type":"ul","items":["“Add Tavily search to my internal company chatbot so it can answer questions about our competitors”","“Build a lead enrichment tool that uses Tavily to find company information from their website”","“Create a news monitoring agent that tracks mentions of our brand using Tavily search”","“Implement a RAG pipeline that uses Tavily extract to pull content from industry reports”"]}
    - {"type":"ul","items":["“Search for the latest news on AI regulations”","“/search current React best practices”","“Search for Python async patterns”"]}
    - {"type":"ul","items":["“Research the latest developments in quantum computing”","“/research AI agent frameworks and save to report.json”","“Research the competitive landscape for AI coding assistants”"]}
    - {"type":"ul","items":["“Crawl the Stripe API docs and save them locally”","“/crawl [https://docs.example.com](https://docs.example.com/)”","“Download the Next.js documentation for offline reference”"]}
    - {"type":"ul","items":["“Extract the content from this article URL”","“/extract [https://example.com/blog/post](https://example.com/blog/post)”","“Extract content from these three documentation pages”"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"/tavily-best-practices Build a chatbot that integrates Tavily search to answer questions with up-to-date web information"}
    - {"language":"text","code":"/tavily-best-practices Build a chatbot that integrates Tavily search to answer questions with up-to-date web information"}
    - {"language":"text","code":"/tavily-best-practices Add Tavily search to my internal company chatbot so it can answer questions about our competitors"}
    - {"language":"text","code":"/tavily-best-practices Add Tavily search to my internal company chatbot so it can answer questions about our competitors"}
    - {"language":"text","code":"/tavily-best-practices Build a website that refreshes daily with Tesla news and gives a sentiment score on each article"}
    - {"language":"text","code":"/tavily-best-practices Build a website that refreshes daily with Tesla news and gives a sentiment score on each article"}
    - {"language":"text","code":"/tavily-best-practices Create a news monitoring dashboard that tracks AI industry news and sends daily Slack summaries"}
    - {"language":"text","code":"/tavily-best-practices Create a news monitoring dashboard that tracks AI industry news and sends daily Slack summaries"}
    - {"language":"text","code":"/tavily-best-practices Build a lead enrichment tool that uses Tavily to find company information from their website"}
    - {"language":"text","code":"/tavily-best-practices Build a lead enrichment tool that uses Tavily to find company information from their website"}
    - {"language":"text","code":"/tavily-best-practices Create a script that takes a list of company URLs and extracts key business information"}
    - {"language":"text","code":"/tavily-best-practices Create a script that takes a list of company URLs and extracts key business information"}
    - {"language":"text","code":"/tavily-best-practices Build a market research tool that crawls competitor documentation and pricing pages"}
    - {"language":"text","code":"/tavily-best-practices Build a market research tool that crawls competitor documentation and pricing pages"}
    - {"language":"text","code":"/tavily-best-practices Create an agent that monitors competitor product launches and generates weekly reports"}
    - {"language":"text","code":"/tavily-best-practices Create an agent that monitors competitor product launches and generates weekly reports"}
    - {"language":"text","code":"# Open your Claude settings file\nopen -e \"$HOME/.claude/settings.json\"\n\n# Or with VS Code\ncode \"$HOME/.claude/settings.json\""}
    - {"language":"text","code":"# Open your Claude settings file\nopen -e \"$HOME/.claude/settings.json\"\n\n# Or with VS Code\ncode \"$HOME/.claude/settings.json\""}
    - {"language":"json","code":"{\n  \"env\": {\n    \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY\"\n  }\n}"}
    - {"language":"json","code":"{\n  \"env\": {\n    \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY\"\n  }\n}"}
    - {"language":"text","code":"npx skills add tavily-ai/skills"}
    - {"language":"text","code":"npx skills add tavily-ai/skills"}
    - {"language":"text","code":"/tavily-best-practices"}
    - {"language":"text","code":"/tavily-best-practices"}
    - {"language":"text","code":"/search"}
    - {"language":"text","code":"/search"}
    - {"language":"text","code":"/research"}
    - {"language":"text","code":"/research"}
    - {"language":"text","code":"/crawl"}
    - {"language":"text","code":"/crawl"}
    - {"language":"text","code":"/extract"}
    - {"language":"text","code":"/extract"}
    - {"language":"text","code":"Research the latest developments in AI agents and summarize the key trends"}
    - {"language":"text","code":"Research the latest developments in AI agents and summarize the key trends"}
    - {"language":"text","code":"Search for the latest news on AI regulations"}
    - {"language":"text","code":"Search for the latest news on AI regulations"}
    - {"language":"text","code":"Crawl the Stripe API docs and save them locally"}
    - {"language":"text","code":"Crawl the Stripe API docs and save them locally"}
    - {"language":"text","code":"/research AI agent frameworks and save to report.json"}
    - {"language":"text","code":"/research AI agent frameworks and save to report.json"}
    - {"language":"text","code":"/search current React best practices"}
    - {"language":"text","code":"/search current React best practices"}
    - {"language":"text","code":"/crawl https://docs.example.com"}
    - {"language":"text","code":"/crawl https://docs.example.com"}
    - {"language":"text","code":"/extract https://example.com/blog/post"}
    - {"language":"text","code":"/extract https://example.com/blog/post"}
    - {"language":"text","code":"/tavily-best-practices"}
    - {"language":"text","code":"/tavily-best-practices"}
    - {"language":"text","code":"code ~/.claude/settings.json"}
    - {"language":"text","code":"code ~/.claude/settings.json"}
    - {"language":"json","code":"{\n  \"env\": {\n    \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY\"\n  }\n}"}
    - {"language":"json","code":"{\n  \"env\": {\n    \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY\"\n  }\n}"}
    - {"language":"text","code":"/plugin marketplace add tavily-ai/skills"}
    - {"language":"text","code":"/plugin marketplace add tavily-ai/skills"}
    - {"language":"text","code":"/plugin install tavily@skills"}
    - {"language":"text","code":"/plugin install tavily@skills"}
    - {"language":"text","code":"/clear"}
    - {"language":"text","code":"/clear"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Tavily_Agent_Skills_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Tavily_Agent_Skills_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Tavily_Agent_Skills_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Tavily_Agent_Skills_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
  charts:
    - {"type":"svg","index":1,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":5,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_5.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_23.png","width":24,"height":24}
    - {"type":"svg","index":25,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_25.png","width":24,"height":24}
    - {"type":"svg","index":26,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_26.png","width":14,"height":12}
    - {"type":"svg","index":27,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_28.png","width":12,"height":12}
    - {"type":"svg","index":33,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_33.png","width":12,"height":12}
    - {"type":"svg","index":38,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_38.png","width":12,"height":12}
    - {"type":"svg","index":43,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_43.png","width":12,"height":12}
    - {"type":"svg","index":48,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_48.png","width":14,"height":18}
    - {"type":"svg","index":49,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_49.png","width":14,"height":12}
    - {"type":"svg","index":50,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_50.png","width":14,"height":12}
    - {"type":"svg","index":51,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_51.png","width":12,"height":12}
    - {"type":"svg","index":52,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_53.png","width":14,"height":12}
    - {"type":"svg","index":54,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_55.png","width":16,"height":16}
    - {"type":"svg","index":56,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_58.png","width":20,"height":20}
    - {"type":"svg","index":59,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_59.png","width":14,"height":12}
    - {"type":"svg","index":60,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_60.png","width":16,"height":16}
    - {"type":"svg","index":61,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_61.png","width":16,"height":16}
    - {"type":"svg","index":62,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_62.png","width":14,"height":12}
    - {"type":"svg","index":63,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_63.png","width":14,"height":12}
    - {"type":"svg","index":64,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_64.png","width":12,"height":12}
    - {"type":"svg","index":65,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_65.png","width":16,"height":16}
    - {"type":"svg","index":66,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_66.png","width":16,"height":16}
    - {"type":"svg","index":67,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_67.png","width":16,"height":16}
    - {"type":"svg","index":68,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_68.png","width":12,"height":12}
    - {"type":"svg","index":69,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_69.png","width":16,"height":16}
    - {"type":"svg","index":72,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_72.png","width":12,"height":12}
    - {"type":"svg","index":73,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_73.png","width":16,"height":16}
    - {"type":"svg","index":76,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_76.png","width":12,"height":12}
    - {"type":"svg","index":77,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_77.png","width":16,"height":16}
    - {"type":"svg","index":80,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_80.png","width":12,"height":12}
    - {"type":"svg","index":81,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_81.png","width":16,"height":16}
    - {"type":"svg","index":84,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_84.png","width":14,"height":12}
    - {"type":"svg","index":85,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_85.png","width":14,"height":12}
    - {"type":"svg","index":86,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_86.png","width":16,"height":16}
    - {"type":"svg","index":87,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_87.png","width":16,"height":16}
    - {"type":"svg","index":88,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_88.png","width":16,"height":16}
    - {"type":"svg","index":89,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_89.png","width":16,"height":16}
    - {"type":"svg","index":90,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_90.png","width":16,"height":16}
    - {"type":"svg","index":91,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_91.png","width":16,"height":16}
    - {"type":"svg","index":92,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_92.png","width":14,"height":12}
    - {"type":"svg","index":93,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_93.png","width":16,"height":16}
    - {"type":"svg","index":94,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_94.png","width":16,"height":16}
    - {"type":"svg","index":95,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_95.png","width":16,"height":16}
    - {"type":"svg","index":96,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_96.png","width":16,"height":16}
    - {"type":"svg","index":97,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_97.png","width":16,"height":16}
    - {"type":"svg","index":98,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_98.png","width":16,"height":16}
    - {"type":"svg","index":99,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_99.png","width":16,"height":16}
    - {"type":"svg","index":100,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_100.png","width":16,"height":16}
    - {"type":"svg","index":101,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_101.png","width":16,"height":16}
    - {"type":"svg","index":102,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_102.png","width":16,"height":16}
    - {"type":"svg","index":103,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_103.png","width":14,"height":12}
    - {"type":"svg","index":104,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_104.png","width":14,"height":12}
    - {"type":"svg","index":105,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_105.png","width":16,"height":16}
    - {"type":"svg","index":106,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_106.png","width":16,"height":16}
    - {"type":"svg","index":107,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_107.png","width":16,"height":16}
    - {"type":"svg","index":108,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_108.png","width":16,"height":16}
    - {"type":"svg","index":109,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_109.png","width":14,"height":12}
    - {"type":"svg","index":110,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_110.png","width":16,"height":16}
    - {"type":"svg","index":111,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_111.png","width":16,"height":16}
    - {"type":"svg","index":112,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_112.png","width":16,"height":16}
    - {"type":"svg","index":113,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_113.png","width":16,"height":16}
    - {"type":"svg","index":114,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_114.png","width":14,"height":12}
    - {"type":"svg","index":115,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_115.png","width":16,"height":16}
    - {"type":"svg","index":116,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_116.png","width":16,"height":16}
    - {"type":"svg","index":117,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_117.png","width":14,"height":14}
    - {"type":"svg","index":118,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_118.png","width":14,"height":14}
    - {"type":"svg","index":119,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_119.png","width":14,"height":14}
    - {"type":"svg","index":124,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_124.png","width":20,"height":20}
    - {"type":"svg","index":125,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_125.png","width":20,"height":20}
    - {"type":"svg","index":126,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_126.png","width":20,"height":20}
    - {"type":"svg","index":127,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_127.png","width":20,"height":20}
    - {"type":"svg","index":128,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_128.png","width":49,"height":14}
    - {"type":"svg","index":129,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_129.png","width":16,"height":16}
    - {"type":"svg","index":130,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_130.png","width":16,"height":16}
    - {"type":"svg","index":131,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_131.png","width":16,"height":16}
    - {"type":"svg","index":132,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_132.png","width":20,"height":20}
    - {"type":"svg","index":133,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_133.png","width":14,"height":14}
    - {"type":"svg","index":134,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_134.png","width":16,"height":16}
    - {"type":"svg","index":135,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_135.png","width":14,"height":14}
    - {"type":"svg","index":136,"filename":"Tavily_Agent_Skills_-_Tavily_Docs/svg_136.png","width":14,"height":14}
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

# Tavily Agent Skills

## 源URL

https://docs.tavily.com/documentation/agent-skills

## 描述

Official skills that define best practices for working with the Tavily API. Useful for AI agents like Claude Code, Codex, or Cursor.

## 内容

### GitHub

### Get API Key

### Why Use These Skills?

### What You Can Build

### Installation

#### Prerequisites

#### Step 1: Configure Your API Key

```text
# Open your Claude settings file
open -e "$HOME/.claude/settings.json"

# Or with VS Code
code "$HOME/.claude/settings.json"
```

```text
{
  "env": {
    "TAVILY_API_KEY": "tvly-YOUR_API_KEY"
  }
}
```

#### Step 2: Install the Skills

```text
npx skills add tavily-ai/skills
```

#### Step 3: Restart Your Agent

### Available Skills

### Usage Examples

#### Automatic Skill Invocation

```text
Research the latest developments in AI agents and summarize the key trends
```

```text
Search for the latest news on AI regulations
```

```text
Crawl the Stripe API docs and save them locally
```

#### Explicit Skill Invocation

```text
/research AI agent frameworks and save to report.json
```

```text
/search current React best practices
```

```text
/crawl https://docs.example.com
```

```text
/extract https://example.com/blog/post
```

```text
/tavily-best-practices
```

### Claude Code Plugin

#### Step 1: Configure Your API Key

```text
code ~/.claude/settings.json
```

```text
{
  "env": {
    "TAVILY_API_KEY": "tvly-YOUR_API_KEY"
  }
}
```

#### Step 2: Install the Skills

```text
/plugin marketplace add tavily-ai/skills
```

```text
/plugin install tavily@skills
```

#### Step 3: Restart Claude Code

```text
/clear
```

## 图片

![light logo](Tavily_Agent_Skills_-_Tavily_Docs/image_1.svg)

![dark logo](Tavily_Agent_Skills_-_Tavily_Docs/image_2.svg)

![light logo](Tavily_Agent_Skills_-_Tavily_Docs/image_3.svg)

![dark logo](Tavily_Agent_Skills_-_Tavily_Docs/image_4.svg)

## 图表

![SVG图表 1](Tavily_Agent_Skills_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Tavily_Agent_Skills_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 5](Tavily_Agent_Skills_-_Tavily_Docs/svg_5.png)
*尺寸: 14x16px*

![SVG图表 11](Tavily_Agent_Skills_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Tavily_Agent_Skills_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Tavily_Agent_Skills_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Tavily_Agent_Skills_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Tavily_Agent_Skills_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Tavily_Agent_Skills_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Tavily_Agent_Skills_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Tavily_Agent_Skills_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 23](Tavily_Agent_Skills_-_Tavily_Docs/svg_23.png)
*尺寸: 24x24px*

![SVG图表 25](Tavily_Agent_Skills_-_Tavily_Docs/svg_25.png)
*尺寸: 24x24px*

![SVG图表 26](Tavily_Agent_Skills_-_Tavily_Docs/svg_26.png)
*尺寸: 14x12px*

![SVG图表 27](Tavily_Agent_Skills_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](Tavily_Agent_Skills_-_Tavily_Docs/svg_28.png)
*尺寸: 12x12px*

![SVG图表 33](Tavily_Agent_Skills_-_Tavily_Docs/svg_33.png)
*尺寸: 12x12px*

![SVG图表 38](Tavily_Agent_Skills_-_Tavily_Docs/svg_38.png)
*尺寸: 12x12px*

![SVG图表 43](Tavily_Agent_Skills_-_Tavily_Docs/svg_43.png)
*尺寸: 12x12px*

![SVG图表 48](Tavily_Agent_Skills_-_Tavily_Docs/svg_48.png)
*尺寸: 14x18px*

![SVG图表 49](Tavily_Agent_Skills_-_Tavily_Docs/svg_49.png)
*尺寸: 14x12px*

![SVG图表 50](Tavily_Agent_Skills_-_Tavily_Docs/svg_50.png)
*尺寸: 14x12px*

![SVG图表 51](Tavily_Agent_Skills_-_Tavily_Docs/svg_51.png)
*尺寸: 12x12px*

![SVG图表 52](Tavily_Agent_Skills_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](Tavily_Agent_Skills_-_Tavily_Docs/svg_53.png)
*尺寸: 14x12px*

![SVG图表 54](Tavily_Agent_Skills_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](Tavily_Agent_Skills_-_Tavily_Docs/svg_55.png)
*尺寸: 16x16px*

![SVG图表 56](Tavily_Agent_Skills_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](Tavily_Agent_Skills_-_Tavily_Docs/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](Tavily_Agent_Skills_-_Tavily_Docs/svg_58.png)
*尺寸: 20x20px*

![SVG图表 59](Tavily_Agent_Skills_-_Tavily_Docs/svg_59.png)
*尺寸: 14x12px*

![SVG图表 60](Tavily_Agent_Skills_-_Tavily_Docs/svg_60.png)
*尺寸: 16x16px*

![SVG图表 61](Tavily_Agent_Skills_-_Tavily_Docs/svg_61.png)
*尺寸: 16x16px*

![SVG图表 62](Tavily_Agent_Skills_-_Tavily_Docs/svg_62.png)
*尺寸: 14x12px*

![SVG图表 63](Tavily_Agent_Skills_-_Tavily_Docs/svg_63.png)
*尺寸: 14x12px*

![SVG图表 64](Tavily_Agent_Skills_-_Tavily_Docs/svg_64.png)
*尺寸: 12x12px*

![SVG图表 65](Tavily_Agent_Skills_-_Tavily_Docs/svg_65.png)
*尺寸: 16x16px*

![SVG图表 66](Tavily_Agent_Skills_-_Tavily_Docs/svg_66.png)
*尺寸: 16x16px*

![SVG图表 67](Tavily_Agent_Skills_-_Tavily_Docs/svg_67.png)
*尺寸: 16x16px*

![SVG图表 68](Tavily_Agent_Skills_-_Tavily_Docs/svg_68.png)
*尺寸: 12x12px*

![SVG图表 69](Tavily_Agent_Skills_-_Tavily_Docs/svg_69.png)
*尺寸: 16x16px*

![SVG图表 72](Tavily_Agent_Skills_-_Tavily_Docs/svg_72.png)
*尺寸: 12x12px*

![SVG图表 73](Tavily_Agent_Skills_-_Tavily_Docs/svg_73.png)
*尺寸: 16x16px*

![SVG图表 76](Tavily_Agent_Skills_-_Tavily_Docs/svg_76.png)
*尺寸: 12x12px*

![SVG图表 77](Tavily_Agent_Skills_-_Tavily_Docs/svg_77.png)
*尺寸: 16x16px*

![SVG图表 80](Tavily_Agent_Skills_-_Tavily_Docs/svg_80.png)
*尺寸: 12x12px*

![SVG图表 81](Tavily_Agent_Skills_-_Tavily_Docs/svg_81.png)
*尺寸: 16x16px*

![SVG图表 84](Tavily_Agent_Skills_-_Tavily_Docs/svg_84.png)
*尺寸: 14x12px*

![SVG图表 85](Tavily_Agent_Skills_-_Tavily_Docs/svg_85.png)
*尺寸: 14x12px*

![SVG图表 86](Tavily_Agent_Skills_-_Tavily_Docs/svg_86.png)
*尺寸: 16x16px*

![SVG图表 87](Tavily_Agent_Skills_-_Tavily_Docs/svg_87.png)
*尺寸: 16x16px*

![SVG图表 88](Tavily_Agent_Skills_-_Tavily_Docs/svg_88.png)
*尺寸: 16x16px*

![SVG图表 89](Tavily_Agent_Skills_-_Tavily_Docs/svg_89.png)
*尺寸: 16x16px*

![SVG图表 90](Tavily_Agent_Skills_-_Tavily_Docs/svg_90.png)
*尺寸: 16x16px*

![SVG图表 91](Tavily_Agent_Skills_-_Tavily_Docs/svg_91.png)
*尺寸: 16x16px*

![SVG图表 92](Tavily_Agent_Skills_-_Tavily_Docs/svg_92.png)
*尺寸: 14x12px*

![SVG图表 93](Tavily_Agent_Skills_-_Tavily_Docs/svg_93.png)
*尺寸: 16x16px*

![SVG图表 94](Tavily_Agent_Skills_-_Tavily_Docs/svg_94.png)
*尺寸: 16x16px*

![SVG图表 95](Tavily_Agent_Skills_-_Tavily_Docs/svg_95.png)
*尺寸: 16x16px*

![SVG图表 96](Tavily_Agent_Skills_-_Tavily_Docs/svg_96.png)
*尺寸: 16x16px*

![SVG图表 97](Tavily_Agent_Skills_-_Tavily_Docs/svg_97.png)
*尺寸: 16x16px*

![SVG图表 98](Tavily_Agent_Skills_-_Tavily_Docs/svg_98.png)
*尺寸: 16x16px*

![SVG图表 99](Tavily_Agent_Skills_-_Tavily_Docs/svg_99.png)
*尺寸: 16x16px*

![SVG图表 100](Tavily_Agent_Skills_-_Tavily_Docs/svg_100.png)
*尺寸: 16x16px*

![SVG图表 101](Tavily_Agent_Skills_-_Tavily_Docs/svg_101.png)
*尺寸: 16x16px*

![SVG图表 102](Tavily_Agent_Skills_-_Tavily_Docs/svg_102.png)
*尺寸: 16x16px*

![SVG图表 103](Tavily_Agent_Skills_-_Tavily_Docs/svg_103.png)
*尺寸: 14x12px*

![SVG图表 104](Tavily_Agent_Skills_-_Tavily_Docs/svg_104.png)
*尺寸: 14x12px*

![SVG图表 105](Tavily_Agent_Skills_-_Tavily_Docs/svg_105.png)
*尺寸: 16x16px*

![SVG图表 106](Tavily_Agent_Skills_-_Tavily_Docs/svg_106.png)
*尺寸: 16x16px*

![SVG图表 107](Tavily_Agent_Skills_-_Tavily_Docs/svg_107.png)
*尺寸: 16x16px*

![SVG图表 108](Tavily_Agent_Skills_-_Tavily_Docs/svg_108.png)
*尺寸: 16x16px*

![SVG图表 109](Tavily_Agent_Skills_-_Tavily_Docs/svg_109.png)
*尺寸: 14x12px*

![SVG图表 110](Tavily_Agent_Skills_-_Tavily_Docs/svg_110.png)
*尺寸: 16x16px*

![SVG图表 111](Tavily_Agent_Skills_-_Tavily_Docs/svg_111.png)
*尺寸: 16x16px*

![SVG图表 112](Tavily_Agent_Skills_-_Tavily_Docs/svg_112.png)
*尺寸: 16x16px*

![SVG图表 113](Tavily_Agent_Skills_-_Tavily_Docs/svg_113.png)
*尺寸: 16x16px*

![SVG图表 114](Tavily_Agent_Skills_-_Tavily_Docs/svg_114.png)
*尺寸: 14x12px*

![SVG图表 115](Tavily_Agent_Skills_-_Tavily_Docs/svg_115.png)
*尺寸: 16x16px*

![SVG图表 116](Tavily_Agent_Skills_-_Tavily_Docs/svg_116.png)
*尺寸: 16x16px*

![SVG图表 117](Tavily_Agent_Skills_-_Tavily_Docs/svg_117.png)
*尺寸: 14x14px*

![SVG图表 118](Tavily_Agent_Skills_-_Tavily_Docs/svg_118.png)
*尺寸: 14x14px*

![SVG图表 119](Tavily_Agent_Skills_-_Tavily_Docs/svg_119.png)
*尺寸: 14x14px*

![SVG图表 124](Tavily_Agent_Skills_-_Tavily_Docs/svg_124.png)
*尺寸: 20x20px*

![SVG图表 125](Tavily_Agent_Skills_-_Tavily_Docs/svg_125.png)
*尺寸: 20x20px*

![SVG图表 126](Tavily_Agent_Skills_-_Tavily_Docs/svg_126.png)
*尺寸: 20x20px*

![SVG图表 127](Tavily_Agent_Skills_-_Tavily_Docs/svg_127.png)
*尺寸: 20x20px*

![SVG图表 128](Tavily_Agent_Skills_-_Tavily_Docs/svg_128.png)
*尺寸: 49x14px*

![SVG图表 129](Tavily_Agent_Skills_-_Tavily_Docs/svg_129.png)
*尺寸: 16x16px*

![SVG图表 130](Tavily_Agent_Skills_-_Tavily_Docs/svg_130.png)
*尺寸: 16x16px*

![SVG图表 131](Tavily_Agent_Skills_-_Tavily_Docs/svg_131.png)
*尺寸: 16x16px*

![SVG图表 132](Tavily_Agent_Skills_-_Tavily_Docs/svg_132.png)
*尺寸: 20x20px*

![SVG图表 133](Tavily_Agent_Skills_-_Tavily_Docs/svg_133.png)
*尺寸: 14x14px*

![SVG图表 134](Tavily_Agent_Skills_-_Tavily_Docs/svg_134.png)
*尺寸: 16x16px*

![SVG图表 135](Tavily_Agent_Skills_-_Tavily_Docs/svg_135.png)
*尺寸: 14x14px*

![SVG图表 136](Tavily_Agent_Skills_-_Tavily_Docs/svg_136.png)
*尺寸: 14x14px*
