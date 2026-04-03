---
id: "url-576391bc"
type: "website"
title: "Google ADK"
url: "https://docs.tavily.com/documentation/integrations/google-adk"
description: "Connect your Google ADK agent to Tavily's AI-focused search, extraction, and crawling platform for real-time web intelligence."
source: ""
tags: []
crawl_time: "2026-03-18T07:10:32.612Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Google ADK"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#prerequisites)Prerequisites"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#installation)Installation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#building-your-agent)Building Your Agent"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-1-create-an-agent-project)Step 1: Create an Agent Project"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-2-update-your-agent-code)Step 2: Update Your Agent Code"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-3-set-your-api-keys)Step 3: Set Your API Keys"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-4-run-your-agent)Step 4: Run Your Agent"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#run-with-command-line-interface)Run with Command-Line Interface"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#run-with-web-interface)Run with Web Interface"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#example-usage)Example Usage"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#available-tools)Available Tools"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-search)tavily-search"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-extract)tavily-extract"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-map)tavily-map"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-crawl)tavily-crawl"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#prerequisites)Prerequisites"}
    - {"type":"list","listType":"ul","items":["Python 3.9 or later","pip for installing packages","A [Tavily API key](https://app.tavily.com/home) (sign up for free if you don’t have one)","A [Gemini API key](https://aistudio.google.com/app/apikey) for Google AI Studio"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#installation)Installation"}
    - {"type":"codeblock","language":"","content":"pip install google-adk mcp"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#building-your-agent)Building Your Agent"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-1-create-an-agent-project)Step 1: Create an Agent Project"}
    - {"type":"codeblock","language":"","content":"adk create my_agent"}
    - {"type":"codeblock","language":"","content":"my_agent/\n    agent.py      # main agent code\n    .env          # API keys or project IDs\n    __init__.py"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-2-update-your-agent-code)Step 2: Update Your Agent Code"}
    - {"type":"codeblock","language":"","content":"from google.adk.agents import Agent\nfrom google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams\nfrom google.adk.tools.mcp_tool.mcp_toolset import MCPToolset\nimport os\n\n# Get API key from environment\nTAVILY_API_KEY = os.getenv(\"TAVILY_API_KEY\")\n\nroot_agent = Agent(\n    model=\"gemini-2.5-pro\",\n    name=\"tavily_agent\",\n    instruction=\"You are a helpful assistant that uses Tavily to search the web, extract content, and explore websites. Use Tavily's tools to provide up-to-date information to users.\",\n    tools=[\n        MCPToolset(\n            connection_params=StreamableHTTPServerParams(\n                url=\"https://mcp.tavily.com/mcp/\",\n                headers={\n                    \"Authorization\": f\"Bearer {TAVILY_API_KEY}\",\n                },\n            ),\n        )\n    ],\n)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-3-set-your-api-keys)Step 3: Set Your API Keys"}
    - {"type":"codeblock","language":"","content":"echo 'GOOGLE_API_KEY=\"YOUR_GEMINI_API_KEY\"' >> my_agent/.env\necho 'TAVILY_API_KEY=\"YOUR_TAVILY_API_KEY\"' >> my_agent/.env"}
    - {"type":"codeblock","language":"","content":"GOOGLE_API_KEY=\"your_gemini_api_key_here\"\nTAVILY_API_KEY=\"your_tavily_api_key_here\""}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#step-4-run-your-agent)Step 4: Run Your Agent"}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#run-with-command-line-interface)Run with Command-Line Interface"}
    - {"type":"codeblock","language":"","content":"adk run my_agent"}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#run-with-web-interface)Run with Web Interface"}
    - {"type":"codeblock","language":"","content":"adk web --port 8000"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#example-usage)Example Usage"}
    - {"type":"codeblock","language":"","content":"Find all documentation pages on tavily.com and provide instructions on how to get started with Tavily"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#available-tools)Available Tools"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-search)tavily-search"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-extract)tavily-extract"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-map)tavily-map"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/google-adk#tavily-crawl)tavily-crawl"}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/integrations/google-adk#introduction)","[Prerequisites](https://docs.tavily.com/documentation/integrations/google-adk#prerequisites)","[Installation](https://docs.tavily.com/documentation/integrations/google-adk#installation)","[Building Your Agent](https://docs.tavily.com/documentation/integrations/google-adk#building-your-agent)","[Step 1: Create an Agent Project](https://docs.tavily.com/documentation/integrations/google-adk#step-1-create-an-agent-project)","[Step 2: Update Your Agent Code](https://docs.tavily.com/documentation/integrations/google-adk#step-2-update-your-agent-code)","[Step 3: Set Your API Keys](https://docs.tavily.com/documentation/integrations/google-adk#step-3-set-your-api-keys)","[Step 4: Run Your Agent](https://docs.tavily.com/documentation/integrations/google-adk#step-4-run-your-agent)","[Run with Command-Line Interface](https://docs.tavily.com/documentation/integrations/google-adk#run-with-command-line-interface)","[Run with Web Interface](https://docs.tavily.com/documentation/integrations/google-adk#run-with-web-interface)","[Example Usage](https://docs.tavily.com/documentation/integrations/google-adk#example-usage)","[Available Tools](https://docs.tavily.com/documentation/integrations/google-adk#available-tools)","[tavily-search](https://docs.tavily.com/documentation/integrations/google-adk#tavily-search)","[tavily-extract](https://docs.tavily.com/documentation/integrations/google-adk#tavily-extract)","[tavily-map](https://docs.tavily.com/documentation/integrations/google-adk#tavily-map)","[tavily-crawl](https://docs.tavily.com/documentation/integrations/google-adk#tavily-crawl)"]}
    - {"type":"ul","items":["Python 3.9 or later","pip for installing packages","A [Tavily API key](https://app.tavily.com/home) (sign up for free if you don’t have one)","A [Gemini API key](https://aistudio.google.com/app/apikey) for Google AI Studio"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install google-adk mcp"}
    - {"language":"text","code":"pip install google-adk mcp"}
    - {"language":"text","code":"adk create my_agent"}
    - {"language":"text","code":"adk create my_agent"}
    - {"language":"text","code":"my_agent/\n    agent.py      # main agent code\n    .env          # API keys or project IDs\n    __init__.py"}
    - {"language":"text","code":"my_agent/\n    agent.py      # main agent code\n    .env          # API keys or project IDs\n    __init__.py"}
    - {"language":"text","code":"from google.adk.agents import Agent\nfrom google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams\nfrom google.adk.tools.mcp_tool.mcp_toolset import MCPToolset\nimport os\n\n# Get API key from environment\nTAVILY_API_KEY = os.getenv(\"TAVILY_API_KEY\")\n\nroot_agent = Agent(\n    model=\"gemini-2.5-pro\",\n    name=\"tavily_agent\",\n    instruction=\"You are a helpful assistant that uses Tavily to search the web, extract content, and explore websites. Use Tavily's tools to provide up-to-date information to users.\",\n    tools=[\n        MCPToolset(\n            connection_params=StreamableHTTPServerParams(\n                url=\"https://mcp.tavily.com/mcp/\",\n                headers={\n                    \"Authorization\": f\"Bearer {TAVILY_API_KEY}\",\n                },\n            ),\n        )\n    ],\n)"}
    - {"language":"text","code":"from google.adk.agents import Agent\nfrom google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams\nfrom google.adk.tools.mcp_tool.mcp_toolset import MCPToolset\nimport os\n\n# Get API key from environment\nTAVILY_API_KEY = os.getenv(\"TAVILY_API_KEY\")\n\nroot_agent = Agent(\n    model=\"gemini-2.5-pro\",\n    name=\"tavily_agent\",\n    instruction=\"You are a helpful assistant that uses Tavily to search the web, extract content, and explore websites. Use Tavily's tools to provide up-to-date information to users.\",\n    tools=[\n        MCPToolset(\n            connection_params=StreamableHTTPServerParams(\n                url=\"https://mcp.tavily.com/mcp/\",\n                headers={\n                    \"Authorization\": f\"Bearer {TAVILY_API_KEY}\",\n                },\n            ),\n        )\n    ],\n)"}
    - {"language":"text","code":"echo 'GOOGLE_API_KEY=\"YOUR_GEMINI_API_KEY\"' >> my_agent/.env\necho 'TAVILY_API_KEY=\"YOUR_TAVILY_API_KEY\"' >> my_agent/.env"}
    - {"language":"text","code":"echo 'GOOGLE_API_KEY=\"YOUR_GEMINI_API_KEY\"' >> my_agent/.env\necho 'TAVILY_API_KEY=\"YOUR_TAVILY_API_KEY\"' >> my_agent/.env"}
    - {"language":"text","code":"GOOGLE_API_KEY=\"your_gemini_api_key_here\"\nTAVILY_API_KEY=\"your_tavily_api_key_here\""}
    - {"language":"text","code":"GOOGLE_API_KEY=\"your_gemini_api_key_here\"\nTAVILY_API_KEY=\"your_tavily_api_key_here\""}
    - {"language":"text","code":"adk run my_agent"}
    - {"language":"text","code":"adk run my_agent"}
    - {"language":"text","code":"adk web --port 8000"}
    - {"language":"text","code":"adk web --port 8000"}
    - {"language":"text","code":"Find all documentation pages on tavily.com and provide instructions on how to get started with Tavily"}
    - {"language":"text","code":"Find all documentation pages on tavily.com and provide instructions on how to get started with Tavily"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Google_ADK_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Google_ADK_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/6_GM_pQOTDBhyG2t/images/google-adk.png?fit=max&auto=format&n=6_GM_pQOTDBhyG2t&q=85&s=32daff4af3598c46f1bedae141666bc9","localPath":"Google_ADK_-_Tavily_Docs/image_3.png","alt":"Tavily-ADK","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Google_ADK_-_Tavily_Docs/image_4.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Google_ADK_-_Tavily_Docs/image_5.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/6_GM_pQOTDBhyG2t/images/google-adk.png?w=840&fit=max&auto=format&n=6_GM_pQOTDBhyG2t&q=85&s=2ac15ad4b9b3a9708f51a3fafb1cfc60","localPath":"Google_ADK_-_Tavily_Docs/image_6.png","alt":"Tavily-ADK","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Google_ADK_-_Tavily_Docs/image_7.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Google_ADK_-_Tavily_Docs/image_8.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Google_ADK_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Google_ADK_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Google_ADK_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Google_ADK_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Google_ADK_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Google_ADK_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Google_ADK_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Google_ADK_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Google_ADK_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Google_ADK_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Google_ADK_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Google_ADK_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Google_ADK_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Google_ADK_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Google_ADK_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Google_ADK_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Google_ADK_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Google_ADK_-_Tavily_Docs/svg_28.png","width":14,"height":12}
    - {"type":"svg","index":29,"filename":"Google_ADK_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Google_ADK_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Google_ADK_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"Google_ADK_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"Google_ADK_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"Google_ADK_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Google_ADK_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"Google_ADK_-_Tavily_Docs/svg_36.png","width":14,"height":12}
    - {"type":"svg","index":37,"filename":"Google_ADK_-_Tavily_Docs/svg_37.png","width":16,"height":16}
    - {"type":"svg","index":38,"filename":"Google_ADK_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"Google_ADK_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Google_ADK_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"Google_ADK_-_Tavily_Docs/svg_41.png","width":14,"height":12}
    - {"type":"svg","index":42,"filename":"Google_ADK_-_Tavily_Docs/svg_42.png","width":14,"height":12}
    - {"type":"svg","index":43,"filename":"Google_ADK_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"Google_ADK_-_Tavily_Docs/svg_44.png","width":16,"height":16}
    - {"type":"svg","index":45,"filename":"Google_ADK_-_Tavily_Docs/svg_45.png","width":14,"height":12}
    - {"type":"svg","index":46,"filename":"Google_ADK_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"Google_ADK_-_Tavily_Docs/svg_47.png","width":16,"height":16}
    - {"type":"svg","index":48,"filename":"Google_ADK_-_Tavily_Docs/svg_48.png","width":14,"height":12}
    - {"type":"svg","index":49,"filename":"Google_ADK_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"Google_ADK_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"Google_ADK_-_Tavily_Docs/svg_52.png","width":14,"height":12}
    - {"type":"svg","index":53,"filename":"Google_ADK_-_Tavily_Docs/svg_53.png","width":14,"height":12}
    - {"type":"svg","index":54,"filename":"Google_ADK_-_Tavily_Docs/svg_54.png","width":14,"height":12}
    - {"type":"svg","index":55,"filename":"Google_ADK_-_Tavily_Docs/svg_55.png","width":14,"height":12}
    - {"type":"svg","index":56,"filename":"Google_ADK_-_Tavily_Docs/svg_56.png","width":14,"height":12}
    - {"type":"svg","index":57,"filename":"Google_ADK_-_Tavily_Docs/svg_57.png","width":14,"height":14}
    - {"type":"svg","index":58,"filename":"Google_ADK_-_Tavily_Docs/svg_58.png","width":14,"height":14}
    - {"type":"svg","index":59,"filename":"Google_ADK_-_Tavily_Docs/svg_59.png","width":14,"height":14}
    - {"type":"svg","index":64,"filename":"Google_ADK_-_Tavily_Docs/svg_64.png","width":20,"height":20}
    - {"type":"svg","index":65,"filename":"Google_ADK_-_Tavily_Docs/svg_65.png","width":20,"height":20}
    - {"type":"svg","index":66,"filename":"Google_ADK_-_Tavily_Docs/svg_66.png","width":20,"height":20}
    - {"type":"svg","index":67,"filename":"Google_ADK_-_Tavily_Docs/svg_67.png","width":20,"height":20}
    - {"type":"svg","index":68,"filename":"Google_ADK_-_Tavily_Docs/svg_68.png","width":49,"height":14}
    - {"type":"svg","index":69,"filename":"Google_ADK_-_Tavily_Docs/svg_69.png","width":16,"height":16}
    - {"type":"svg","index":70,"filename":"Google_ADK_-_Tavily_Docs/svg_70.png","width":16,"height":16}
    - {"type":"svg","index":71,"filename":"Google_ADK_-_Tavily_Docs/svg_71.png","width":16,"height":16}
    - {"type":"svg","index":82,"filename":"Google_ADK_-_Tavily_Docs/svg_82.png","width":16,"height":16}
    - {"type":"svg","index":83,"filename":"Google_ADK_-_Tavily_Docs/svg_83.png","width":14,"height":14}
    - {"type":"svg","index":84,"filename":"Google_ADK_-_Tavily_Docs/svg_84.png","width":16,"height":16}
    - {"type":"svg","index":85,"filename":"Google_ADK_-_Tavily_Docs/svg_85.png","width":12,"height":12}
    - {"type":"svg","index":86,"filename":"Google_ADK_-_Tavily_Docs/svg_86.png","width":14,"height":14}
    - {"type":"svg","index":87,"filename":"Google_ADK_-_Tavily_Docs/svg_87.png","width":16,"height":16}
    - {"type":"svg","index":88,"filename":"Google_ADK_-_Tavily_Docs/svg_88.png","width":12,"height":12}
    - {"type":"svg","index":89,"filename":"Google_ADK_-_Tavily_Docs/svg_89.png","width":14,"height":14}
    - {"type":"svg","index":90,"filename":"Google_ADK_-_Tavily_Docs/svg_90.png","width":16,"height":16}
    - {"type":"svg","index":91,"filename":"Google_ADK_-_Tavily_Docs/svg_91.png","width":12,"height":12}
    - {"type":"svg","index":92,"filename":"Google_ADK_-_Tavily_Docs/svg_92.png","width":14,"height":14}
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

# Google ADK

## 源URL

https://docs.tavily.com/documentation/integrations/google-adk

## 描述

Connect your Google ADK agent to Tavily's AI-focused search, extraction, and crawling platform for real-time web intelligence.

## 内容

### Introduction

### Prerequisites

- Python 3.9 or later
- pip for installing packages
- A [Tavily API key](https://app.tavily.com/home) (sign up for free if you don’t have one)
- A [Gemini API key](https://aistudio.google.com/app/apikey) for Google AI Studio

### Installation

```text
pip install google-adk mcp
```

### Building Your Agent

#### Step 1: Create an Agent Project

```text
adk create my_agent
```

```text
my_agent/
    agent.py      # main agent code
    .env          # API keys or project IDs
    __init__.py
```

#### Step 2: Update Your Agent Code

```text
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
import os

# Get API key from environment
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

root_agent = Agent(
    model="gemini-2.5-pro",
    name="tavily_agent",
    instruction="You are a helpful assistant that uses Tavily to search the web, extract content, and explore websites. Use Tavily's tools to provide up-to-date information to users.",
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://mcp.tavily.com/mcp/",
                headers={
                    "Authorization": f"Bearer {TAVILY_API_KEY}",
                },
            ),
        )
    ],
)
```

#### Step 3: Set Your API Keys

```text
echo 'GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"' >> my_agent/.env
echo 'TAVILY_API_KEY="YOUR_TAVILY_API_KEY"' >> my_agent/.env
```

```text
GOOGLE_API_KEY="your_gemini_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
```

#### Step 4: Run Your Agent

##### Run with Command-Line Interface

```text
adk run my_agent
```

##### Run with Web Interface

```text
adk web --port 8000
```

### Example Usage

```text
Find all documentation pages on tavily.com and provide instructions on how to get started with Tavily
```

### Available Tools

#### tavily-search

#### tavily-extract

#### tavily-map

#### tavily-crawl

## 图片

![light logo](Google_ADK_-_Tavily_Docs/image_1.svg)

![dark logo](Google_ADK_-_Tavily_Docs/image_2.svg)

![Tavily-ADK](Google_ADK_-_Tavily_Docs/image_3.png)

![light logo](Google_ADK_-_Tavily_Docs/image_4.svg)

![dark logo](Google_ADK_-_Tavily_Docs/image_5.svg)

![Tavily-ADK](Google_ADK_-_Tavily_Docs/image_6.png)

![tavily-logo](Google_ADK_-_Tavily_Docs/image_7.png)

![Powered by Onetrust](Google_ADK_-_Tavily_Docs/image_8.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Google_ADK_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Google_ADK_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Google_ADK_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Google_ADK_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Google_ADK_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Google_ADK_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Google_ADK_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Google_ADK_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Google_ADK_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Google_ADK_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Google_ADK_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Google_ADK_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Google_ADK_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Google_ADK_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Google_ADK_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Google_ADK_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Google_ADK_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](Google_ADK_-_Tavily_Docs/svg_28.png)
*尺寸: 14x12px*

![SVG图表 29](Google_ADK_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Google_ADK_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 31](Google_ADK_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](Google_ADK_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](Google_ADK_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 34](Google_ADK_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Google_ADK_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](Google_ADK_-_Tavily_Docs/svg_36.png)
*尺寸: 14x12px*

![SVG图表 37](Google_ADK_-_Tavily_Docs/svg_37.png)
*尺寸: 16x16px*

![SVG图表 38](Google_ADK_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](Google_ADK_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](Google_ADK_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](Google_ADK_-_Tavily_Docs/svg_41.png)
*尺寸: 14x12px*

![SVG图表 42](Google_ADK_-_Tavily_Docs/svg_42.png)
*尺寸: 14x12px*

![SVG图表 43](Google_ADK_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](Google_ADK_-_Tavily_Docs/svg_44.png)
*尺寸: 16x16px*

![SVG图表 45](Google_ADK_-_Tavily_Docs/svg_45.png)
*尺寸: 14x12px*

![SVG图表 46](Google_ADK_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](Google_ADK_-_Tavily_Docs/svg_47.png)
*尺寸: 16x16px*

![SVG图表 48](Google_ADK_-_Tavily_Docs/svg_48.png)
*尺寸: 14x12px*

![SVG图表 49](Google_ADK_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](Google_ADK_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 52](Google_ADK_-_Tavily_Docs/svg_52.png)
*尺寸: 14x12px*

![SVG图表 53](Google_ADK_-_Tavily_Docs/svg_53.png)
*尺寸: 14x12px*

![SVG图表 54](Google_ADK_-_Tavily_Docs/svg_54.png)
*尺寸: 14x12px*

![SVG图表 55](Google_ADK_-_Tavily_Docs/svg_55.png)
*尺寸: 14x12px*

![SVG图表 56](Google_ADK_-_Tavily_Docs/svg_56.png)
*尺寸: 14x12px*

![SVG图表 57](Google_ADK_-_Tavily_Docs/svg_57.png)
*尺寸: 14x14px*

![SVG图表 58](Google_ADK_-_Tavily_Docs/svg_58.png)
*尺寸: 14x14px*

![SVG图表 59](Google_ADK_-_Tavily_Docs/svg_59.png)
*尺寸: 14x14px*

![SVG图表 64](Google_ADK_-_Tavily_Docs/svg_64.png)
*尺寸: 20x20px*

![SVG图表 65](Google_ADK_-_Tavily_Docs/svg_65.png)
*尺寸: 20x20px*

![SVG图表 66](Google_ADK_-_Tavily_Docs/svg_66.png)
*尺寸: 20x20px*

![SVG图表 67](Google_ADK_-_Tavily_Docs/svg_67.png)
*尺寸: 20x20px*

![SVG图表 68](Google_ADK_-_Tavily_Docs/svg_68.png)
*尺寸: 49x14px*

![SVG图表 69](Google_ADK_-_Tavily_Docs/svg_69.png)
*尺寸: 16x16px*

![SVG图表 70](Google_ADK_-_Tavily_Docs/svg_70.png)
*尺寸: 16x16px*

![SVG图表 71](Google_ADK_-_Tavily_Docs/svg_71.png)
*尺寸: 16x16px*

![SVG图表 82](Google_ADK_-_Tavily_Docs/svg_82.png)
*尺寸: 16x16px*

![SVG图表 83](Google_ADK_-_Tavily_Docs/svg_83.png)
*尺寸: 14x14px*

![SVG图表 84](Google_ADK_-_Tavily_Docs/svg_84.png)
*尺寸: 16x16px*

![SVG图表 85](Google_ADK_-_Tavily_Docs/svg_85.png)
*尺寸: 12x12px*

![SVG图表 86](Google_ADK_-_Tavily_Docs/svg_86.png)
*尺寸: 14x14px*

![SVG图表 87](Google_ADK_-_Tavily_Docs/svg_87.png)
*尺寸: 16x16px*

![SVG图表 88](Google_ADK_-_Tavily_Docs/svg_88.png)
*尺寸: 12x12px*

![SVG图表 89](Google_ADK_-_Tavily_Docs/svg_89.png)
*尺寸: 14x14px*

![SVG图表 90](Google_ADK_-_Tavily_Docs/svg_90.png)
*尺寸: 16x16px*

![SVG图表 91](Google_ADK_-_Tavily_Docs/svg_91.png)
*尺寸: 12x12px*

![SVG图表 92](Google_ADK_-_Tavily_Docs/svg_92.png)
*尺寸: 14x14px*
