---
id: "url-6c65b4c9"
type: "website"
title: "Composio"
url: "https://docs.tavily.com/documentation/integrations/composio"
description: "Tavily is now available for integration through Composio."
source: ""
tags: []
crawl_time: "2026-03-18T06:44:44.578Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Composio"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/composio#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/composio#step-by-step-integration-guide)Step-by-Step Integration Guide"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/composio#step-1-install-required-packages)Step 1: Install Required Packages"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/composio#step-2-set-up-api-keys)Step 2: Set Up API Keys"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/composio#step-3-connect-tavily-to-composio)Step 3: Connect Tavily to Composio"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/composio#step-4-example-use-case)Step 4: Example Use Case"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/composio#additional-use-cases)Additional Use Cases"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/composio#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/composio#step-by-step-integration-guide)Step-by-Step Integration Guide"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/composio#step-1-install-required-packages)Step 1: Install Required Packages"}
    - {"type":"codeblock","language":"","content":"pip install composio composio-openai openai python-dotenv"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/composio#step-2-set-up-api-keys)Step 2: Set Up API Keys"}
    - {"type":"list","listType":"ul","items":["**OpenAI API Key:** [Get your OpenAI API key here](https://platform.openai.com/account/api-keys)","**Composio API Key:** [Get your Composio API key here](https://app.composio.dev/dashboard)"]}
    - {"type":"codeblock","language":"","content":"export OPENAI_API_KEY=your_openai_api_key\nexport COMPOSIO_API_KEY=your_composio_api_key"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/composio#step-3-connect-tavily-to-composio)Step 3: Connect Tavily to Composio"}
    - {"type":"codeblock","language":"","content":"from composio import Composio\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\ncomposio = Composio()\n\n# Use composio managed auth\nauth_config = composio.auth_configs.create(\n    toolkit=\"tavily\",\n    options={\n        \"type\": \"use_custom_auth\",\n        \"auth_scheme\": \"API_KEY\",\n        \"credentials\": {}\n    }\n)\nprint(auth_config)\nauth_config_id = auth_config.id\n\nuser_id = \"your-user-id\"\nconnection_request = composio.connected_accounts.link(user_id, auth_config_id)\nprint(connection_request.redirect_url)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/composio#step-4-example-use-case)Step 4: Example Use Case"}
    - {"type":"codeblock","language":"","content":"from composio import Composio\nfrom composio_openai import OpenAIProvider\nfrom openai import OpenAI\nimport os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n# Initialize OpenAI client with API key\nclient = OpenAI()\n\n# Initialize Composio toolset\ncomposio = Composio(\n    api_key=os.getenv(\"COMPOSIO_API_KEY\"),\n    provider=OpenAIProvider()\n)\n\nuser_id = \"your-user-id\"\n\n# Get the Tavily tool with all available parameters\ntools = composio.tools.get(user_id,\n    toolkits=['TAVILY']\n)\n\n# Define the market research task with specific parameters\ntask = {\n    \"query\": \"Analyze the competitive landscape of AI-powered customer service solutions in 2024\",\n    \"search_depth\": \"advanced\",  \n    \"include_answer\": True,      \n    \"max_results\": 10,  \n    # Focus on relevant industry sources         \n    \"include_domains\": [        \n        \"techcrunch.com\",\n        \"venturebeat.com\",\n        \"forbes.com\",\n        \"gartner.com\",\n        \"marketsandmarkets.com\"\n    ],\n}\n\n# Send request to LLM\nmessages = [{\"role\": \"user\", \"content\": str(task)}]\n\nresponse = client.chat.completions.create(\n    model=\"gpt-4.1\",\n    messages=messages,\n    tools=tools,\n    tool_choice=\"auto\"\n)\n\n# Handle tool call via Composio\nexecution_result = None\nresponse_message = response.choices[0].message\n\nif response_message.tool_calls:\n    execution_result = composio.provider.handle_tool_calls(user_id,response)\n    print(\"Execution Result:\", execution_result)\n    messages.append(response_message)\n    \n    # Add tool response messages\n    for tool_call, result in zip(response_message.tool_calls, execution_result):\n        messages.append({\n            \"role\": \"tool\",\n            \"content\": str(result[\"data\"]),\n            \"tool_call_id\": tool_call.id\n        })\n    \n    # Get final response from LLM\n    final_response = client.chat.completions.create(\n        model=\"gpt-4.1\",\n        messages=messages\n    )\n    print(\"\\nMarket Research Summary:\")\n    print(final_response.choices[0].message.content)\nelse:\n    print(\"LLM responded directly (no tool used):\", response_message.content)"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/composio#additional-use-cases)Additional Use Cases"}
    - {"type":"list","listType":"ol","items":["**Research Automation**: Automate the collection and summarization of research data","**Content Curation**: Gather and organize information from multiple sources","**Real-time Data Integration**: Keeping your AI models up-to-date with the latest information."]}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/integrations/composio#introduction)","[Step-by-Step Integration Guide](https://docs.tavily.com/documentation/integrations/composio#step-by-step-integration-guide)","[Step 1: Install Required Packages](https://docs.tavily.com/documentation/integrations/composio#step-1-install-required-packages)","[Step 2: Set Up API Keys](https://docs.tavily.com/documentation/integrations/composio#step-2-set-up-api-keys)","[Step 3: Connect Tavily to Composio](https://docs.tavily.com/documentation/integrations/composio#step-3-connect-tavily-to-composio)","[Step 4: Example Use Case](https://docs.tavily.com/documentation/integrations/composio#step-4-example-use-case)","[Additional Use Cases](https://docs.tavily.com/documentation/integrations/composio#additional-use-cases)"]}
    - {"type":"ul","items":["OpenAI API Key: [Get your OpenAI API key here](https://platform.openai.com/account/api-keys)","Composio API Key: [Get your Composio API key here](https://app.composio.dev/dashboard)"]}
    - {"type":"ol","items":["Research Automation: Automate the collection and summarization of research data","Content Curation: Gather and organize information from multiple sources","Real-time Data Integration: Keeping your AI models up-to-date with the latest information."]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install composio composio-openai openai python-dotenv"}
    - {"language":"text","code":"pip install composio composio-openai openai python-dotenv"}
    - {"language":"text","code":"export OPENAI_API_KEY=your_openai_api_key\nexport COMPOSIO_API_KEY=your_composio_api_key"}
    - {"language":"text","code":"export OPENAI_API_KEY=your_openai_api_key\nexport COMPOSIO_API_KEY=your_composio_api_key"}
    - {"language":"text","code":"from composio import Composio\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\ncomposio = Composio()\n\n# Use composio managed auth\nauth_config = composio.auth_configs.create(\n    toolkit=\"tavily\",\n    options={\n        \"type\": \"use_custom_auth\",\n        \"auth_scheme\": \"API_KEY\",\n        \"credentials\": {}\n    }\n)\nprint(auth_config)\nauth_config_id = auth_config.id\n\nuser_id = \"your-user-id\"\nconnection_request = composio.connected_accounts.link(user_id, auth_config_id)\nprint(connection_request.redirect_url)"}
    - {"language":"text","code":"from composio import Composio\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\ncomposio = Composio()\n\n# Use composio managed auth\nauth_config = composio.auth_configs.create(\n    toolkit=\"tavily\",\n    options={\n        \"type\": \"use_custom_auth\",\n        \"auth_scheme\": \"API_KEY\",\n        \"credentials\": {}\n    }\n)\nprint(auth_config)\nauth_config_id = auth_config.id\n\nuser_id = \"your-user-id\"\nconnection_request = composio.connected_accounts.link(user_id, auth_config_id)\nprint(connection_request.redirect_url)"}
    - {"language":"text","code":"from composio import Composio\nfrom composio_openai import OpenAIProvider\nfrom openai import OpenAI\nimport os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n# Initialize OpenAI client with API key\nclient = OpenAI()\n\n# Initialize Composio toolset\ncomposio = Composio(\n    api_key=os.getenv(\"COMPOSIO_API_KEY\"),\n    provider=OpenAIProvider()\n)\n\nuser_id = \"your-user-id\"\n\n# Get the Tavily tool with all available parameters\ntools = composio.tools.get(user_id,\n    toolkits=['TAVILY']\n)\n\n# Define the market research task with specific parameters\ntask = {\n    \"query\": \"Analyze the competitive landscape of AI-powered customer service solutions in 2024\",\n    \"search_depth\": \"advanced\",  \n    \"include_answer\": True,      \n    \"max_results\": 10,  \n    # Focus on relevant industry sources         \n    \"include_domains\": [        \n        \"techcrunch.com\",\n        \"venturebeat.com\",\n        \"forbes.com\",\n        \"gartner.com\",\n        \"marketsandmarkets.com\"\n    ],\n}\n\n# Send request to LLM\nmessages = [{\"role\": \"user\", \"content\": str(task)}]\n\nresponse = client.chat.completions.create(\n    model=\"gpt-4.1\",\n    messages=messages,\n    tools=tools,\n    tool_choice=\"auto\"\n)\n\n# Handle tool call via Composio\nexecution_result = None\nresponse_message = response.choices[0].message\n\nif response_message.tool_calls:\n    execution_result = composio.provider.handle_tool_calls(user_id,response)\n    print(\"Execution Result:\", execution_result)\n    messages.append(response_message)\n    \n    # Add tool response messages\n    for tool_call, result in zip(response_message.tool_calls, execution_result):\n        messages.append({\n            \"role\": \"tool\",\n            \"content\": str(result[\"data\"]),\n            \"tool_call_id\": tool_call.id\n        })\n    \n    # Get final response from LLM\n    final_response = client.chat.completions.create(\n        model=\"gpt-4.1\",\n        messages=messages\n    )\n    print(\"\\nMarket Research Summary:\")\n    print(final_response.choices[0].message.content)\nelse:\n    print(\"LLM responded directly (no tool used):\", response_message.content)"}
    - {"language":"text","code":"from composio import Composio\nfrom composio_openai import OpenAIProvider\nfrom openai import OpenAI\nimport os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n# Initialize OpenAI client with API key\nclient = OpenAI()\n\n# Initialize Composio toolset\ncomposio = Composio(\n    api_key=os.getenv(\"COMPOSIO_API_KEY\"),\n    provider=OpenAIProvider()\n)\n\nuser_id = \"your-user-id\"\n\n# Get the Tavily tool with all available parameters\ntools = composio.tools.get(user_id,\n    toolkits=['TAVILY']\n)\n\n# Define the market research task with specific parameters\ntask = {\n    \"query\": \"Analyze the competitive landscape of AI-powered customer service solutions in 2024\",\n    \"search_depth\": \"advanced\",  \n    \"include_answer\": True,      \n    \"max_results\": 10,  \n    # Focus on relevant industry sources         \n    \"include_domains\": [        \n        \"techcrunch.com\",\n        \"venturebeat.com\",\n        \"forbes.com\",\n        \"gartner.com\",\n        \"marketsandmarkets.com\"\n    ],\n}\n\n# Send request to LLM\nmessages = [{\"role\": \"user\", \"content\": str(task)}]\n\nresponse = client.chat.completions.create(\n    model=\"gpt-4.1\",\n    messages=messages,\n    tools=tools,\n    tool_choice=\"auto\"\n)\n\n# Handle tool call via Composio\nexecution_result = None\nresponse_message = response.choices[0].message\n\nif response_message.tool_calls:\n    execution_result = composio.provider.handle_tool_calls(user_id,response)\n    print(\"Execution Result:\", execution_result)\n    messages.append(response_message)\n    \n    # Add tool response messages\n    for tool_call, result in zip(response_message.tool_calls, execution_result):\n        messages.append({\n            \"role\": \"tool\",\n            \"content\": str(result[\"data\"]),\n            \"tool_call_id\": tool_call.id\n        })\n    \n    # Get final response from LLM\n    final_response = client.chat.completions.create(\n        model=\"gpt-4.1\",\n        messages=messages\n    )\n    print(\"\\nMarket Research Summary:\")\n    print(final_response.choices[0].message.content)\nelse:\n    print(\"LLM responded directly (no tool used):\", response_message.content)"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Composio_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Composio_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Composio_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Composio_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
  charts:
    - {"type":"svg","index":1,"filename":"Composio_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Composio_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":5,"filename":"Composio_-_Tavily_Docs/svg_5.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Composio_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Composio_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Composio_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Composio_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Composio_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Composio_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Composio_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Composio_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Composio_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Composio_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Composio_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Composio_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Composio_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Composio_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Composio_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Composio_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Composio_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"Composio_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"Composio_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"Composio_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"Composio_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Composio_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"Composio_-_Tavily_Docs/svg_36.png","width":14,"height":12}
    - {"type":"svg","index":37,"filename":"Composio_-_Tavily_Docs/svg_37.png","width":14,"height":14}
    - {"type":"svg","index":38,"filename":"Composio_-_Tavily_Docs/svg_38.png","width":14,"height":14}
    - {"type":"svg","index":39,"filename":"Composio_-_Tavily_Docs/svg_39.png","width":14,"height":14}
    - {"type":"svg","index":44,"filename":"Composio_-_Tavily_Docs/svg_44.png","width":20,"height":20}
    - {"type":"svg","index":45,"filename":"Composio_-_Tavily_Docs/svg_45.png","width":20,"height":20}
    - {"type":"svg","index":46,"filename":"Composio_-_Tavily_Docs/svg_46.png","width":20,"height":20}
    - {"type":"svg","index":47,"filename":"Composio_-_Tavily_Docs/svg_47.png","width":20,"height":20}
    - {"type":"svg","index":48,"filename":"Composio_-_Tavily_Docs/svg_48.png","width":49,"height":14}
    - {"type":"svg","index":49,"filename":"Composio_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"Composio_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"Composio_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"Composio_-_Tavily_Docs/svg_52.png","width":20,"height":20}
    - {"type":"svg","index":53,"filename":"Composio_-_Tavily_Docs/svg_53.png","width":14,"height":14}
    - {"type":"svg","index":54,"filename":"Composio_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"Composio_-_Tavily_Docs/svg_55.png","width":14,"height":14}
    - {"type":"svg","index":56,"filename":"Composio_-_Tavily_Docs/svg_56.png","width":14,"height":14}
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

# Composio

## 源URL

https://docs.tavily.com/documentation/integrations/composio

## 描述

Tavily is now available for integration through Composio.

## 内容

### Introduction

### Step-by-Step Integration Guide

#### Step 1: Install Required Packages

```text
pip install composio composio-openai openai python-dotenv
```

#### Step 2: Set Up API Keys

- **OpenAI API Key:** [Get your OpenAI API key here](https://platform.openai.com/account/api-keys)
- **Composio API Key:** [Get your Composio API key here](https://app.composio.dev/dashboard)

```text
export OPENAI_API_KEY=your_openai_api_key
export COMPOSIO_API_KEY=your_composio_api_key
```

#### Step 3: Connect Tavily to Composio

```text
from composio import Composio
from dotenv import load_dotenv

load_dotenv()

composio = Composio()

# Use composio managed auth
auth_config = composio.auth_configs.create(
    toolkit="tavily",
    options={
        "type": "use_custom_auth",
        "auth_scheme": "API_KEY",
        "credentials": {}
    }
)
print(auth_config)
auth_config_id = auth_config.id

user_id = "your-user-id"
connection_request = composio.connected_accounts.link(user_id, auth_config_id)
print(connection_request.redirect_url)
```

#### Step 4: Example Use Case

```text
from composio import Composio
from composio_openai import OpenAIProvider
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize OpenAI client with API key
client = OpenAI()

# Initialize Composio toolset
composio = Composio(
    api_key=os.getenv("COMPOSIO_API_KEY"),
    provider=OpenAIProvider()
)

user_id = "your-user-id"

# Get the Tavily tool with all available parameters
tools = composio.tools.get(user_id,
    toolkits=['TAVILY']
)

# Define the market research task with specific parameters
task = {
    "query": "Analyze the competitive landscape of AI-powered customer service solutions in 2024",
    "search_depth": "advanced",  
    "include_answer": True,      
    "max_results": 10,  
    # Focus on relevant industry sources         
    "include_domains": [        
        "techcrunch.com",
        "venturebeat.com",
        "forbes.com",
        "gartner.com",
        "marketsandmarkets.com"
    ],
}

# Send request to LLM
messages = [{"role": "user", "content": str(task)}]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Handle tool call via Composio
execution_result = None
response_message = response.choices[0].message

if response_message.tool_calls:
    execution_result = composio.provider.handle_tool_calls(user_id,response)
    print("Execution Result:", execution_result)
    messages.append(response_message)
    
    # Add tool response messages
    for tool_call, result in zip(response_message.tool_calls, execution_result):
        messages.append({
            "role": "tool",
            "content": str(result["data"]),
            "tool_call_id": tool_call.id
        })
    
    # Get final response from LLM
    final_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )
    print("\nMarket Research Summary:")
    print(final_response.choices[0].message.content)
else:
    print("LLM responded directly (no tool used):", response_message.content)
```

### Additional Use Cases

1. **Research Automation**: Automate the collection and summarization of research data
2. **Content Curation**: Gather and organize information from multiple sources
3. **Real-time Data Integration**: Keeping your AI models up-to-date with the latest information.

## 图片

![light logo](Composio_-_Tavily_Docs/image_1.svg)

![dark logo](Composio_-_Tavily_Docs/image_2.svg)

![light logo](Composio_-_Tavily_Docs/image_3.svg)

![dark logo](Composio_-_Tavily_Docs/image_4.svg)

## 图表

![SVG图表 1](Composio_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Composio_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 5](Composio_-_Tavily_Docs/svg_5.png)
*尺寸: 14x16px*

![SVG图表 11](Composio_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Composio_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Composio_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Composio_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Composio_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Composio_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Composio_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Composio_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Composio_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Composio_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Composio_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Composio_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Composio_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Composio_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](Composio_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Composio_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Composio_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](Composio_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](Composio_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](Composio_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 34](Composio_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Composio_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](Composio_-_Tavily_Docs/svg_36.png)
*尺寸: 14x12px*

![SVG图表 37](Composio_-_Tavily_Docs/svg_37.png)
*尺寸: 14x14px*

![SVG图表 38](Composio_-_Tavily_Docs/svg_38.png)
*尺寸: 14x14px*

![SVG图表 39](Composio_-_Tavily_Docs/svg_39.png)
*尺寸: 14x14px*

![SVG图表 44](Composio_-_Tavily_Docs/svg_44.png)
*尺寸: 20x20px*

![SVG图表 45](Composio_-_Tavily_Docs/svg_45.png)
*尺寸: 20x20px*

![SVG图表 46](Composio_-_Tavily_Docs/svg_46.png)
*尺寸: 20x20px*

![SVG图表 47](Composio_-_Tavily_Docs/svg_47.png)
*尺寸: 20x20px*

![SVG图表 48](Composio_-_Tavily_Docs/svg_48.png)
*尺寸: 49x14px*

![SVG图表 49](Composio_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](Composio_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](Composio_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 52](Composio_-_Tavily_Docs/svg_52.png)
*尺寸: 20x20px*

![SVG图表 53](Composio_-_Tavily_Docs/svg_53.png)
*尺寸: 14x14px*

![SVG图表 54](Composio_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](Composio_-_Tavily_Docs/svg_55.png)
*尺寸: 14x14px*

![SVG图表 56](Composio_-_Tavily_Docs/svg_56.png)
*尺寸: 14x14px*
