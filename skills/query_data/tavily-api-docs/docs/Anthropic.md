---
id: "url-b4bbdc4"
type: "website"
title: "Anthropic"
url: "https://docs.tavily.com/documentation/integrations/anthropic"
description: "Integrate Tavily with Anthropic Claude to enhance your AI applications with real-time web search capabilities."
source: ""
tags: []
crawl_time: "2026-03-18T02:59:10.328Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Anthropic"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#installation)Installation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#setup)Setup"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#using-tavily-with-anthropic-tool-calling)Using Tavily with Anthropic tool calling"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#implementation)Implementation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#system-prompt)System prompt"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#tool-schema)Tool schema"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#tool-execution)Tool execution"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#main-chat-function)Main chat function"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#usage-example)Usage example"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/anthropic#tavily-endpoints-schema-for-anthropic-tool-definition)Tavily endpoints schema for Anthropic tool definition"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#installation)Installation"}
    - {"type":"codeblock","language":"","content":"pip install anthropic tavily-python"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#setup)Setup"}
    - {"type":"codeblock","language":"","content":"import os\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#using-tavily-with-anthropic-tool-calling)Using Tavily with Anthropic tool calling"}
    - {"type":"codeblock","language":"","content":"import json\nfrom anthropic import Anthropic\nfrom tavily import TavilyClient\n\n# Initialize clients\nclient = Anthropic(api_key=os.environ[\"ANTHROPIC_API_KEY\"])\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nMODEL_NAME = \"claude-sonnet-4-20250514\""}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#implementation)Implementation"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#system-prompt)System prompt"}
    - {"type":"codeblock","language":"","content":"SYSTEM_PROMPT = (\n    \"You are a research assistant. Use the tavily_search tool when needed. \"\n    \"After tools run and tool results are provided back to you, produce a concise, well-structured summary \"\n    \"with a short bullet list of key points and a 'Sources' section listing the URLs. \"\n)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#tool-schema)Tool schema"}
    - {"type":"codeblock","language":"","content":"tools = [\n    {\n        \"name\": \"tavily_search\",\n        \"description\": \"Search the web using Tavily. Return relevant links & summaries.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"query\": {\"type\": \"string\", \"description\": \"Search query string.\"},\n                \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                \"search_depth\": {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]},\n            },\n            \"required\": [\"query\"]\n        }\n    }\n]"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#tool-execution)Tool execution"}
    - {"type":"codeblock","language":"","content":"def tavily_search(**kwargs):\n    return tavily_client.search(**kwargs)\n\ndef process_tool_call(name, args):\n    if name == \"tavily_search\":\n        return tavily_search(**args)\n    raise ValueError(f\"Unknown tool: {name}\")"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#main-chat-function)Main chat function"}
    - {"type":"codeblock","language":"","content":"def chat_with_claude(user_message: str):\n    print(f\"\\n{'='*50}\\nUser Message: {user_message}\\n{'='*50}\")\n\n    # ---- Call 1: allow tools so Claude can ask for searches ----\n    initial_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[{\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]}],\n        tools=tools,\n    )\n\n    print(\"\\nInitial Response stop_reason:\", initial_response.stop_reason)\n    print(\"Initial content:\", initial_response.content)\n\n    # If Claude already answered in text, return it\n    if initial_response.stop_reason != \"tool_use\":\n        final_text = next((b.text for b in initial_response.content if getattr(b, \"type\", None) == \"text\"), None)\n        print(\"\\nFinal Response:\", final_text)\n        return final_text\n\n    # ---- Execute ALL tool_use blocks from Call 1 ----\n    tool_result_blocks = []\n    for block in initial_response.content:\n        if getattr(block, \"type\", None) == \"tool_use\":\n            result = process_tool_call(block.name, block.input)\n            tool_result_blocks.append({\n                \"type\": \"tool_result\",\n                \"tool_use_id\": block.id,\n                \"content\": [{\"type\": \"text\", \"text\": json.dumps(result)}],\n            })\n\n    # ---- Call 2: NO tools; ask for the final summary from tool results ----\n    final_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]},\n            {\"role\": \"assistant\", \"content\": initial_response.content},    # Claude's tool requests\n            {\"role\": \"user\", \"content\": tool_result_blocks},    # Your tool results\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\":\n                \"Please synthesize the final answer now based on the tool results above. \"\n                \"Include 3–7 bullets and a 'Sources' section with URLs.\"}]},\n        ],\n    )\n\n    final_text = next((b.text for b in final_response.content if getattr(b, \"type\", None) == \"text\"), None)\n    print(\"\\nFinal Response:\", final_text)\n    return final_text"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#usage-example)Usage example"}
    - {"type":"codeblock","language":"","content":"# Example usage\nchat_with_claude(\"What is trending now in the agents space in 2025?\")"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/anthropic#tavily-endpoints-schema-for-anthropic-tool-definition)Tavily endpoints schema for Anthropic tool definition"}
    - {"type":"blockquote","content":"Note: When using these schemas, you can customize which parameters are exposed to the model based on your specific use case. For example, if you are building a finance application, you might set topic: \"finance\" for all queries without exposing the topic parameter. This way, the LLM can focus on deciding other parameters, such as time_range, country, and so on, based on the user’s request. Feel free to modify these schemas as needed and only pass the parameters that are relevant to your application."}
    - {"type":"blockquote","content":"API Format: The schemas below are for Anthropic’s tool format. Each tool uses the input_schema structure with type, properties, and required fields."}
  paragraphs:
    - "Full Code Example"
    - "search schema"
    - "extract schema"
    - "map schema"
    - "crawl schema"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Installation](https://docs.tavily.com/documentation/integrations/anthropic#installation)","[Setup](https://docs.tavily.com/documentation/integrations/anthropic#setup)","[Using Tavily with Anthropic tool calling](https://docs.tavily.com/documentation/integrations/anthropic#using-tavily-with-anthropic-tool-calling)","[Implementation](https://docs.tavily.com/documentation/integrations/anthropic#implementation)","[System prompt](https://docs.tavily.com/documentation/integrations/anthropic#system-prompt)","[Tool schema](https://docs.tavily.com/documentation/integrations/anthropic#tool-schema)","[Tool execution](https://docs.tavily.com/documentation/integrations/anthropic#tool-execution)","[Main chat function](https://docs.tavily.com/documentation/integrations/anthropic#main-chat-function)","[Usage example](https://docs.tavily.com/documentation/integrations/anthropic#usage-example)","[Tavily endpoints schema for Anthropic tool definition](https://docs.tavily.com/documentation/integrations/anthropic#tavily-endpoints-schema-for-anthropic-tool-definition)"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install anthropic tavily-python"}
    - {"language":"text","code":"pip install anthropic tavily-python"}
    - {"language":"text","code":"import os\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"language":"text","code":"import os\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"language":"text","code":"import json\nfrom anthropic import Anthropic\nfrom tavily import TavilyClient\n\n# Initialize clients\nclient = Anthropic(api_key=os.environ[\"ANTHROPIC_API_KEY\"])\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nMODEL_NAME = \"claude-sonnet-4-20250514\""}
    - {"language":"text","code":"import json\nfrom anthropic import Anthropic\nfrom tavily import TavilyClient\n\n# Initialize clients\nclient = Anthropic(api_key=os.environ[\"ANTHROPIC_API_KEY\"])\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nMODEL_NAME = \"claude-sonnet-4-20250514\""}
    - {"language":"text","code":"SYSTEM_PROMPT = (\n    \"You are a research assistant. Use the tavily_search tool when needed. \"\n    \"After tools run and tool results are provided back to you, produce a concise, well-structured summary \"\n    \"with a short bullet list of key points and a 'Sources' section listing the URLs. \"\n)"}
    - {"language":"text","code":"SYSTEM_PROMPT = (\n    \"You are a research assistant. Use the tavily_search tool when needed. \"\n    \"After tools run and tool results are provided back to you, produce a concise, well-structured summary \"\n    \"with a short bullet list of key points and a 'Sources' section listing the URLs. \"\n)"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_search\",\n        \"description\": \"Search the web using Tavily. Return relevant links & summaries.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"query\": {\"type\": \"string\", \"description\": \"Search query string.\"},\n                \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                \"search_depth\": {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]},\n            },\n            \"required\": [\"query\"]\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_search\",\n        \"description\": \"Search the web using Tavily. Return relevant links & summaries.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"query\": {\"type\": \"string\", \"description\": \"Search query string.\"},\n                \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                \"search_depth\": {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]},\n            },\n            \"required\": [\"query\"]\n        }\n    }\n]"}
    - {"language":"text","code":"def tavily_search(**kwargs):\n    return tavily_client.search(**kwargs)\n\ndef process_tool_call(name, args):\n    if name == \"tavily_search\":\n        return tavily_search(**args)\n    raise ValueError(f\"Unknown tool: {name}\")"}
    - {"language":"text","code":"def tavily_search(**kwargs):\n    return tavily_client.search(**kwargs)\n\ndef process_tool_call(name, args):\n    if name == \"tavily_search\":\n        return tavily_search(**args)\n    raise ValueError(f\"Unknown tool: {name}\")"}
    - {"language":"text","code":"def chat_with_claude(user_message: str):\n    print(f\"\\n{'='*50}\\nUser Message: {user_message}\\n{'='*50}\")\n\n    # ---- Call 1: allow tools so Claude can ask for searches ----\n    initial_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[{\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]}],\n        tools=tools,\n    )\n\n    print(\"\\nInitial Response stop_reason:\", initial_response.stop_reason)\n    print(\"Initial content:\", initial_response.content)\n\n    # If Claude already answered in text, return it\n    if initial_response.stop_reason != \"tool_use\":\n        final_text = next((b.text for b in initial_response.content if getattr(b, \"type\", None) == \"text\"), None)\n        print(\"\\nFinal Response:\", final_text)\n        return final_text\n\n    # ---- Execute ALL tool_use blocks from Call 1 ----\n    tool_result_blocks = []\n    for block in initial_response.content:\n        if getattr(block, \"type\", None) == \"tool_use\":\n            result = process_tool_call(block.name, block.input)\n            tool_result_blocks.append({\n                \"type\": \"tool_result\",\n                \"tool_use_id\": block.id,\n                \"content\": [{\"type\": \"text\", \"text\": json.dumps(result)}],\n            })\n\n    # ---- Call 2: NO tools; ask for the final summary from tool results ----\n    final_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]},\n            {\"role\": \"assistant\", \"content\": initial_response.content},    # Claude's tool requests\n            {\"role\": \"user\", \"content\": tool_result_blocks},    # Your tool results\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\":\n                \"Please synthesize the final answer now based on the tool results above. \"\n                \"Include 3–7 bullets and a 'Sources' section with URLs.\"}]},\n        ],\n    )\n\n    final_text = next((b.text for b in final_response.content if getattr(b, \"type\", None) == \"text\"), None)\n    print(\"\\nFinal Response:\", final_text)\n    return final_text"}
    - {"language":"text","code":"def chat_with_claude(user_message: str):\n    print(f\"\\n{'='*50}\\nUser Message: {user_message}\\n{'='*50}\")\n\n    # ---- Call 1: allow tools so Claude can ask for searches ----\n    initial_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[{\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]}],\n        tools=tools,\n    )\n\n    print(\"\\nInitial Response stop_reason:\", initial_response.stop_reason)\n    print(\"Initial content:\", initial_response.content)\n\n    # If Claude already answered in text, return it\n    if initial_response.stop_reason != \"tool_use\":\n        final_text = next((b.text for b in initial_response.content if getattr(b, \"type\", None) == \"text\"), None)\n        print(\"\\nFinal Response:\", final_text)\n        return final_text\n\n    # ---- Execute ALL tool_use blocks from Call 1 ----\n    tool_result_blocks = []\n    for block in initial_response.content:\n        if getattr(block, \"type\", None) == \"tool_use\":\n            result = process_tool_call(block.name, block.input)\n            tool_result_blocks.append({\n                \"type\": \"tool_result\",\n                \"tool_use_id\": block.id,\n                \"content\": [{\"type\": \"text\", \"text\": json.dumps(result)}],\n            })\n\n    # ---- Call 2: NO tools; ask for the final summary from tool results ----\n    final_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]},\n            {\"role\": \"assistant\", \"content\": initial_response.content},    # Claude's tool requests\n            {\"role\": \"user\", \"content\": tool_result_blocks},    # Your tool results\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\":\n                \"Please synthesize the final answer now based on the tool results above. \"\n                \"Include 3–7 bullets and a 'Sources' section with URLs.\"}]},\n        ],\n    )\n\n    final_text = next((b.text for b in final_response.content if getattr(b, \"type\", None) == \"text\"), None)\n    print(\"\\nFinal Response:\", final_text)\n    return final_text"}
    - {"language":"text","code":"# Example usage\nchat_with_claude(\"What is trending now in the agents space in 2025?\")"}
    - {"language":"text","code":"# Example usage\nchat_with_claude(\"What is trending now in the agents space in 2025?\")"}
    - {"language":"text","code":"import os\nimport json\nfrom anthropic import Anthropic\nfrom tavily import TavilyClient\n\nclient = Anthropic(api_key=os.environ[\"ANTHROPIC_API_KEY\"])\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nMODEL_NAME = \"claude-sonnet-4-20250514\"\n\nSYSTEM_PROMPT = (\n    \"You are a research assistant. Use the tavily_search tool when needed. \"\n    \"After tools run and tool results are provided back to you, produce a concise, well-structured summary \"\n    \"with a short bullet list of key points and a 'Sources' section listing the URLs. \"\n)\n\n# ---- Define your client-side tool schema for Anthropic ----\ntools = [\n    {\n        \"name\": \"tavily_search\",\n        \"description\": \"Search the web using Tavily. Return relevant links & summaries.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"query\": {\"type\": \"string\", \"description\": \"Search query string.\"},\n                \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                \"search_depth\": {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]},\n            },\n            \"required\": [\"query\"]\n        }\n    }\n]\n\n# ---- Your local tool executor ----\ndef tavily_search(**kwargs):\n    return tavily_client.search(**kwargs)\n\ndef process_tool_call(name, args):\n    if name == \"tavily_search\":\n        return tavily_search(**args)\n    raise ValueError(f\"Unknown tool: {name}\")\n\ndef chat_with_claude(user_message: str):\n    print(f\"\\n{'='*50}\\nUser Message: {user_message}\\n{'='*50}\")\n\n    # ---- Call 1: allow tools so Claude can ask for searches ----\n    initial_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT, \n        messages=[{\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]}],\n        tools=tools,\n    )\n\n    print(\"\\nInitial Response stop_reason:\", initial_response.stop_reason)\n    print(\"Initial content:\", initial_response.content)\n\n    # If Claude already answered in text, return it\n    if initial_response.stop_reason != \"tool_use\":\n        final_text = next((b.text for b in initial_response.content if getattr(b, \"type\", None) == \"text\"), None)\n        print(\"\\nFinal Response:\", final_text)\n        return final_text\n\n    # ---- Execute ALL tool_use blocks from Call 1 ----\n    tool_result_blocks = []\n    for block in initial_response.content:\n        if getattr(block, \"type\", None) == \"tool_use\":\n            result = process_tool_call(block.name, block.input)\n            tool_result_blocks.append({\n                \"type\": \"tool_result\",\n                \"tool_use_id\": block.id,\n                \"content\": [{\"type\": \"text\", \"text\": json.dumps(result)}],\n            })\n\n    # ---- Call 2: NO tools; ask for the final summary from tool results ----\n    final_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]},\n            {\"role\": \"assistant\", \"content\": initial_response.content},    # Claude's tool requests\n            {\"role\": \"user\", \"content\": tool_result_blocks},    # Your tool results\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\":\n                \"Please synthesize the final answer now based on the tool results above. \"\n                \"Include 3–7 bullets and a 'Sources' section with URLs.\"}]},\n        ],\n    )\n\n    final_text = next((b.text for b in final_response.content if getattr(b, \"type\", None) == \"text\"), None)\n    print(\"\\nFinal Response:\", final_text)\n    return final_text\n\n# Example usage\nchat_with_claude(\"What is trending now in the agents space in 2025?\")"}
    - {"language":"text","code":"import os\nimport json\nfrom anthropic import Anthropic\nfrom tavily import TavilyClient\n\nclient = Anthropic(api_key=os.environ[\"ANTHROPIC_API_KEY\"])\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nMODEL_NAME = \"claude-sonnet-4-20250514\"\n\nSYSTEM_PROMPT = (\n    \"You are a research assistant. Use the tavily_search tool when needed. \"\n    \"After tools run and tool results are provided back to you, produce a concise, well-structured summary \"\n    \"with a short bullet list of key points and a 'Sources' section listing the URLs. \"\n)\n\n# ---- Define your client-side tool schema for Anthropic ----\ntools = [\n    {\n        \"name\": \"tavily_search\",\n        \"description\": \"Search the web using Tavily. Return relevant links & summaries.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"query\": {\"type\": \"string\", \"description\": \"Search query string.\"},\n                \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                \"search_depth\": {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]},\n            },\n            \"required\": [\"query\"]\n        }\n    }\n]\n\n# ---- Your local tool executor ----\ndef tavily_search(**kwargs):\n    return tavily_client.search(**kwargs)\n\ndef process_tool_call(name, args):\n    if name == \"tavily_search\":\n        return tavily_search(**args)\n    raise ValueError(f\"Unknown tool: {name}\")\n\ndef chat_with_claude(user_message: str):\n    print(f\"\\n{'='*50}\\nUser Message: {user_message}\\n{'='*50}\")\n\n    # ---- Call 1: allow tools so Claude can ask for searches ----\n    initial_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT, \n        messages=[{\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]}],\n        tools=tools,\n    )\n\n    print(\"\\nInitial Response stop_reason:\", initial_response.stop_reason)\n    print(\"Initial content:\", initial_response.content)\n\n    # If Claude already answered in text, return it\n    if initial_response.stop_reason != \"tool_use\":\n        final_text = next((b.text for b in initial_response.content if getattr(b, \"type\", None) == \"text\"), None)\n        print(\"\\nFinal Response:\", final_text)\n        return final_text\n\n    # ---- Execute ALL tool_use blocks from Call 1 ----\n    tool_result_blocks = []\n    for block in initial_response.content:\n        if getattr(block, \"type\", None) == \"tool_use\":\n            result = process_tool_call(block.name, block.input)\n            tool_result_blocks.append({\n                \"type\": \"tool_result\",\n                \"tool_use_id\": block.id,\n                \"content\": [{\"type\": \"text\", \"text\": json.dumps(result)}],\n            })\n\n    # ---- Call 2: NO tools; ask for the final summary from tool results ----\n    final_response = client.messages.create(\n        model=MODEL_NAME,\n        max_tokens=4096,\n        system=SYSTEM_PROMPT,\n        messages=[\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\": user_message}]},\n            {\"role\": \"assistant\", \"content\": initial_response.content},    # Claude's tool requests\n            {\"role\": \"user\", \"content\": tool_result_blocks},    # Your tool results\n            {\"role\": \"user\", \"content\": [{\"type\": \"text\", \"text\":\n                \"Please synthesize the final answer now based on the tool results above. \"\n                \"Include 3–7 bullets and a 'Sources' section with URLs.\"}]},\n        ],\n    )\n\n    final_text = next((b.text for b in final_response.content if getattr(b, \"type\", None) == \"text\"), None)\n    print(\"\\nFinal Response:\", final_text)\n    return final_text\n\n# Example usage\nchat_with_claude(\"What is trending now in the agents space in 2025?\")"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_search\",\n        \"description\": \"A powerful web search tool that provides comprehensive, real-time results using Tavily's AI search engine. Returns relevant web content with customizable parameters for result count, content type, and domain filtering. Ideal for gathering current information, news, and detailed web content analysis.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"query\"],\n            \"properties\": {\n                \"query\": {\n                    \"type\": \"string\",\n                    \"description\": \"Search query\"\n                },\n                \"auto_parameters\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Auto-tune parameters based on the query. Explicit values you pass still win.\"\n                },\n                \"topic\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"general\", \"news\",\"finance\"],\n                    \"default\": \"general\",\n                    \"description\": \"The category of the search. This will determine which of our agents will be used for the search\"\n                },\n                \"search_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"The depth of the search. It can be 'basic' or 'advanced'\"\n                },\n                \"chunks_per_source\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 3,\n                    \"default\": 3,\n                    \"description\": \"Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.\"\n                },\n                \"max_results\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 0,\n                    \"maximum\": 20,\n                    \"default\": 5,\n                    \"description\": \"The maximum number of search results to return\"\n                },\n                \"time_range\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"day\", \"week\", \"month\", \"year\"],\n                    \"description\": \"The time range back from the current date to include in the search results. This feature is available for both 'general' and 'news' search topics\"\n                },\n                \"start_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.\"\n                },\n                \"end_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD\"\n                },\n                \"include_answer\": {\n                    \"description\": \"Include an LLM-generated answer. 'basic' is brief; 'advanced' is more detailed.\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_raw_content\": {\n                    \"description\": \"Include the cleaned and parsed HTML content of each search result\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"markdown\", \"text\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images in the response\"\n                },\n                \"include_image_descriptions\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images and their descriptions in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"include_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 300,\n                    \"description\": \"A list of domains to specifically include in the search results, if the user asks to search on specific sites set this to the domain of the site\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 150,\n                    \"description\": \"List of domains to specifically exclude, if the user asks to exclude a domain set this to the domain of the site\"\n                },\n                \"country\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"afghanistan\", \"albania\", \"algeria\", \"andorra\", \"angola\", \"argentina\", \"armenia\", \"australia\", \"austria\", \"azerbaijan\", \"bahamas\", \"bahrain\", \"bangladesh\", \"barbados\", \"belarus\", \"belgium\", \"belize\", \"benin\", \"bhutan\", \"bolivia\", \"bosnia and herzegovina\", \"botswana\", \"brazil\", \"brunei\", \"bulgaria\", \"burkina faso\", \"burundi\", \"cambodia\", \"cameroon\", \"canada\", \"cape verde\", \"central african republic\", \"chad\", \"chile\", \"china\", \"colombia\", \"comoros\", \"congo\", \"costa rica\", \"croatia\", \"cuba\", \"cyprus\", \"czech republic\", \"denmark\", \"djibouti\", \"dominican republic\", \"ecuador\", \"egypt\", \"el salvador\", \"equatorial guinea\", \"eritrea\", \"estonia\", \"ethiopia\", \"fiji\", \"finland\", \"france\", \"gabon\", \"gambia\", \"georgia\", \"germany\", \"ghana\", \"greece\", \"guatemala\", \"guinea\", \"haiti\", \"honduras\", \"hungary\", \"iceland\", \"india\", \"indonesia\", \"iran\", \"iraq\", \"ireland\", \"israel\", \"italy\", \"jamaica\", \"japan\", \"jordan\", \"kazakhstan\", \"kenya\", \"kuwait\", \"kyrgyzstan\", \"latvia\", \"lebanon\", \"lesotho\", \"liberia\", \"libya\", \"liechtenstein\", \"lithuania\", \"luxembourg\", \"madagascar\", \"malawi\", \"malaysia\", \"maldives\", \"mali\", \"malta\", \"mauritania\", \"mauritius\", \"mexico\", \"moldova\", \"monaco\", \"mongolia\", \"montenegro\", \"morocco\", \"mozambique\", \"myanmar\", \"namibia\", \"nepal\", \"netherlands\", \"new zealand\", \"nicaragua\", \"niger\", \"nigeria\", \"north korea\", \"north macedonia\", \"norway\", \"oman\", \"pakistan\", \"panama\", \"papua new guinea\", \"paraguay\", \"peru\", \"philippines\", \"poland\", \"portugal\", \"qatar\", \"romania\", \"russia\", \"rwanda\", \"saudi arabia\", \"senegal\", \"serbia\", \"singapore\", \"slovakia\", \"slovenia\", \"somalia\", \"south africa\", \"south korea\", \"south sudan\", \"spain\", \"sri lanka\", \"sudan\", \"sweden\", \"switzerland\", \"syria\", \"taiwan\", \"tajikistan\", \"tanzania\", \"thailand\", \"togo\", \"trinidad and tobago\", \"tunisia\", \"turkey\", \"turkmenistan\", \"uganda\", \"ukraine\", \"united arab emirates\", \"united kingdom\", \"united states\", \"uruguay\", \"uzbekistan\", \"venezuela\", \"vietnam\", \"yemen\", \"zambia\", \"zimbabwe\"],\n                    \"description\": \"Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general. Country names MUST be written in lowercase, plain English, with spaces and no underscores.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_search\",\n        \"description\": \"A powerful web search tool that provides comprehensive, real-time results using Tavily's AI search engine. Returns relevant web content with customizable parameters for result count, content type, and domain filtering. Ideal for gathering current information, news, and detailed web content analysis.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"query\"],\n            \"properties\": {\n                \"query\": {\n                    \"type\": \"string\",\n                    \"description\": \"Search query\"\n                },\n                \"auto_parameters\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Auto-tune parameters based on the query. Explicit values you pass still win.\"\n                },\n                \"topic\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"general\", \"news\",\"finance\"],\n                    \"default\": \"general\",\n                    \"description\": \"The category of the search. This will determine which of our agents will be used for the search\"\n                },\n                \"search_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"The depth of the search. It can be 'basic' or 'advanced'\"\n                },\n                \"chunks_per_source\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 3,\n                    \"default\": 3,\n                    \"description\": \"Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.\"\n                },\n                \"max_results\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 0,\n                    \"maximum\": 20,\n                    \"default\": 5,\n                    \"description\": \"The maximum number of search results to return\"\n                },\n                \"time_range\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"day\", \"week\", \"month\", \"year\"],\n                    \"description\": \"The time range back from the current date to include in the search results. This feature is available for both 'general' and 'news' search topics\"\n                },\n                \"start_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.\"\n                },\n                \"end_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD\"\n                },\n                \"include_answer\": {\n                    \"description\": \"Include an LLM-generated answer. 'basic' is brief; 'advanced' is more detailed.\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_raw_content\": {\n                    \"description\": \"Include the cleaned and parsed HTML content of each search result\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"markdown\", \"text\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images in the response\"\n                },\n                \"include_image_descriptions\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images and their descriptions in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"include_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 300,\n                    \"description\": \"A list of domains to specifically include in the search results, if the user asks to search on specific sites set this to the domain of the site\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 150,\n                    \"description\": \"List of domains to specifically exclude, if the user asks to exclude a domain set this to the domain of the site\"\n                },\n                \"country\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"afghanistan\", \"albania\", \"algeria\", \"andorra\", \"angola\", \"argentina\", \"armenia\", \"australia\", \"austria\", \"azerbaijan\", \"bahamas\", \"bahrain\", \"bangladesh\", \"barbados\", \"belarus\", \"belgium\", \"belize\", \"benin\", \"bhutan\", \"bolivia\", \"bosnia and herzegovina\", \"botswana\", \"brazil\", \"brunei\", \"bulgaria\", \"burkina faso\", \"burundi\", \"cambodia\", \"cameroon\", \"canada\", \"cape verde\", \"central african republic\", \"chad\", \"chile\", \"china\", \"colombia\", \"comoros\", \"congo\", \"costa rica\", \"croatia\", \"cuba\", \"cyprus\", \"czech republic\", \"denmark\", \"djibouti\", \"dominican republic\", \"ecuador\", \"egypt\", \"el salvador\", \"equatorial guinea\", \"eritrea\", \"estonia\", \"ethiopia\", \"fiji\", \"finland\", \"france\", \"gabon\", \"gambia\", \"georgia\", \"germany\", \"ghana\", \"greece\", \"guatemala\", \"guinea\", \"haiti\", \"honduras\", \"hungary\", \"iceland\", \"india\", \"indonesia\", \"iran\", \"iraq\", \"ireland\", \"israel\", \"italy\", \"jamaica\", \"japan\", \"jordan\", \"kazakhstan\", \"kenya\", \"kuwait\", \"kyrgyzstan\", \"latvia\", \"lebanon\", \"lesotho\", \"liberia\", \"libya\", \"liechtenstein\", \"lithuania\", \"luxembourg\", \"madagascar\", \"malawi\", \"malaysia\", \"maldives\", \"mali\", \"malta\", \"mauritania\", \"mauritius\", \"mexico\", \"moldova\", \"monaco\", \"mongolia\", \"montenegro\", \"morocco\", \"mozambique\", \"myanmar\", \"namibia\", \"nepal\", \"netherlands\", \"new zealand\", \"nicaragua\", \"niger\", \"nigeria\", \"north korea\", \"north macedonia\", \"norway\", \"oman\", \"pakistan\", \"panama\", \"papua new guinea\", \"paraguay\", \"peru\", \"philippines\", \"poland\", \"portugal\", \"qatar\", \"romania\", \"russia\", \"rwanda\", \"saudi arabia\", \"senegal\", \"serbia\", \"singapore\", \"slovakia\", \"slovenia\", \"somalia\", \"south africa\", \"south korea\", \"south sudan\", \"spain\", \"sri lanka\", \"sudan\", \"sweden\", \"switzerland\", \"syria\", \"taiwan\", \"tajikistan\", \"tanzania\", \"thailand\", \"togo\", \"trinidad and tobago\", \"tunisia\", \"turkey\", \"turkmenistan\", \"uganda\", \"ukraine\", \"united arab emirates\", \"united kingdom\", \"united states\", \"uruguay\", \"uzbekistan\", \"venezuela\", \"vietnam\", \"yemen\", \"zambia\", \"zimbabwe\"],\n                    \"description\": \"Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general. Country names MUST be written in lowercase, plain English, with spaces and no underscores.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_extract\",\n        \"description\": \"A powerful web content extraction tool that retrieves and processes raw content from specified URLs, ideal for data collection, content analysis, and research tasks.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"urls\"],\n            \"properties\": {\n                \"urls\": {\n                    \"type\": \"string\",\n                    \"description\": \"List of URLs to extract content from\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of images extracted from the urls in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Depth of extraction - 'basic' or 'advanced', if urls are linkedin use 'advanced' or if explicitly told to use advanced\"\n                },\n                \"timeout\": {\n                    \"type\": \"number\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"minimum\": 0,\n                    \"maximum\": 60,\n                    \"default\": None,\n                    \"description\": \"Maximum time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_extract\",\n        \"description\": \"A powerful web content extraction tool that retrieves and processes raw content from specified URLs, ideal for data collection, content analysis, and research tasks.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"urls\"],\n            \"properties\": {\n                \"urls\": {\n                    \"type\": \"string\",\n                    \"description\": \"List of URLs to extract content from\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of images extracted from the urls in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Depth of extraction - 'basic' or 'advanced', if urls are linkedin use 'advanced' or if explicitly told to use advanced\"\n                },\n                \"timeout\": {\n                    \"type\": \"number\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"minimum\": 0,\n                    \"maximum\": 60,\n                    \"default\": None,\n                    \"description\": \"Maximum time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_map\",\n        \"description\": \"A powerful web mapping tool that creates a structured map of website URLs, allowing you to discover and analyze site structure, content organization, and navigation paths. Perfect for site audits, content discovery, and understanding website architecture.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the mapping\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the mapping. Defines how far from the base URL the crawler can explore\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude URLs with specific path patterns (e.g., /admin/.*).\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude specific domains or subdomains\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"categories\": {\n                    \"type\": \"array\",\n                    \"items\": {\n                        \"type\": \"string\",\n                        \"enum\": [\"Documentation\", \"Blog\", \"Careers\",\"About\",\"Pricing\",\"Community\",\"Developers\",\"Contact\",\"Media\"]\n                    },\n                    \"description\": \"Filter URLs using predefined categories like documentation, blog, api, etc\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_map\",\n        \"description\": \"A powerful web mapping tool that creates a structured map of website URLs, allowing you to discover and analyze site structure, content organization, and navigation paths. Perfect for site audits, content discovery, and understanding website architecture.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the mapping\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the mapping. Defines how far from the base URL the crawler can explore\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude URLs with specific path patterns (e.g., /admin/.*).\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude specific domains or subdomains\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"categories\": {\n                    \"type\": \"array\",\n                    \"items\": {\n                        \"type\": \"string\",\n                        \"enum\": [\"Documentation\", \"Blog\", \"Careers\",\"About\",\"Pricing\",\"Community\",\"Developers\",\"Contact\",\"Media\"]\n                    },\n                    \"description\": \"Filter URLs using predefined categories like documentation, blog, api, etc\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_crawl\",\n        \"description\": \"A powerful web crawler that initiates a structured web crawl starting from a specified base URL. The crawler expands from that point like a tree, following internal links across pages. You can control how deep and wide it goes, and guide it to focus on specific sections of the site.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the crawl\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum: 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the crawl. Defines how far from the base URL the crawler can explore.\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude paths (e.g., /private/.*, /admin/.*)\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude domains/subdomains (e.g., ^private\\\\.example\\\\.com$)\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include images discovered during the crawl\"\n                },\n                \"categories\": {\n                    \"type\": \"array\",\n                    \"items\": {\n                        \"type\": \"string\",\n                        \"enum\": [\"Careers\", \"Blog\", \"Documentation\", \"About\", \"Pricing\", \"Community\", \"Developers\", \"Contact\", \"Media\"]\n                    },\n                    \"description\": \"Filter URLs using predefined categories like documentation, blog, api, etc\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"name\": \"tavily_crawl\",\n        \"description\": \"A powerful web crawler that initiates a structured web crawl starting from a specified base URL. The crawler expands from that point like a tree, following internal links across pages. You can control how deep and wide it goes, and guide it to focus on specific sections of the site.\",\n        \"input_schema\": {\n            \"type\": \"object\",\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the crawl\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum: 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the crawl. Defines how far from the base URL the crawler can explore.\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude paths (e.g., /private/.*, /admin/.*)\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude domains/subdomains (e.g., ^private\\\\.example\\\\.com$)\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include images discovered during the crawl\"\n                },\n                \"categories\": {\n                    \"type\": \"array\",\n                    \"items\": {\n                        \"type\": \"string\",\n                        \"enum\": [\"Careers\", \"Blog\", \"Documentation\", \"About\", \"Pricing\", \"Community\", \"Developers\", \"Contact\", \"Media\"]\n                    },\n                    \"description\": \"Filter URLs using predefined categories like documentation, blog, api, etc\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Anthropic_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Anthropic_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Anthropic_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Anthropic_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Anthropic_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Anthropic_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Anthropic_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Anthropic_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Anthropic_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Anthropic_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Anthropic_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Anthropic_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Anthropic_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Anthropic_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Anthropic_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Anthropic_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Anthropic_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Anthropic_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Anthropic_-_Tavily_Docs/svg_23.png","width":16,"height":16}
    - {"type":"svg","index":24,"filename":"Anthropic_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Anthropic_-_Tavily_Docs/svg_25.png","width":14,"height":12}
    - {"type":"svg","index":26,"filename":"Anthropic_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Anthropic_-_Tavily_Docs/svg_27.png","width":16,"height":16}
    - {"type":"svg","index":28,"filename":"Anthropic_-_Tavily_Docs/svg_28.png","width":14,"height":12}
    - {"type":"svg","index":29,"filename":"Anthropic_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Anthropic_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Anthropic_-_Tavily_Docs/svg_31.png","width":14,"height":12}
    - {"type":"svg","index":32,"filename":"Anthropic_-_Tavily_Docs/svg_32.png","width":14,"height":12}
    - {"type":"svg","index":33,"filename":"Anthropic_-_Tavily_Docs/svg_33.png","width":16,"height":16}
    - {"type":"svg","index":34,"filename":"Anthropic_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Anthropic_-_Tavily_Docs/svg_35.png","width":14,"height":12}
    - {"type":"svg","index":36,"filename":"Anthropic_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Anthropic_-_Tavily_Docs/svg_37.png","width":16,"height":16}
    - {"type":"svg","index":38,"filename":"Anthropic_-_Tavily_Docs/svg_38.png","width":14,"height":12}
    - {"type":"svg","index":39,"filename":"Anthropic_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Anthropic_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"Anthropic_-_Tavily_Docs/svg_41.png","width":14,"height":12}
    - {"type":"svg","index":42,"filename":"Anthropic_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Anthropic_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"Anthropic_-_Tavily_Docs/svg_44.png","width":14,"height":12}
    - {"type":"svg","index":45,"filename":"Anthropic_-_Tavily_Docs/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"Anthropic_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"Anthropic_-_Tavily_Docs/svg_47.png","width":12,"height":12}
    - {"type":"svg","index":48,"filename":"Anthropic_-_Tavily_Docs/svg_48.png","width":16,"height":16}
    - {"type":"svg","index":49,"filename":"Anthropic_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"Anthropic_-_Tavily_Docs/svg_50.png","width":14,"height":12}
    - {"type":"svg","index":51,"filename":"Anthropic_-_Tavily_Docs/svg_51.png","width":12,"height":12}
    - {"type":"svg","index":52,"filename":"Anthropic_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"Anthropic_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":54,"filename":"Anthropic_-_Tavily_Docs/svg_54.png","width":12,"height":12}
    - {"type":"svg","index":55,"filename":"Anthropic_-_Tavily_Docs/svg_55.png","width":16,"height":16}
    - {"type":"svg","index":56,"filename":"Anthropic_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"Anthropic_-_Tavily_Docs/svg_57.png","width":12,"height":12}
    - {"type":"svg","index":58,"filename":"Anthropic_-_Tavily_Docs/svg_58.png","width":16,"height":16}
    - {"type":"svg","index":59,"filename":"Anthropic_-_Tavily_Docs/svg_59.png","width":16,"height":16}
    - {"type":"svg","index":60,"filename":"Anthropic_-_Tavily_Docs/svg_60.png","width":12,"height":12}
    - {"type":"svg","index":61,"filename":"Anthropic_-_Tavily_Docs/svg_61.png","width":16,"height":16}
    - {"type":"svg","index":62,"filename":"Anthropic_-_Tavily_Docs/svg_62.png","width":16,"height":16}
    - {"type":"svg","index":63,"filename":"Anthropic_-_Tavily_Docs/svg_63.png","width":14,"height":14}
    - {"type":"svg","index":64,"filename":"Anthropic_-_Tavily_Docs/svg_64.png","width":14,"height":14}
    - {"type":"svg","index":65,"filename":"Anthropic_-_Tavily_Docs/svg_65.png","width":14,"height":14}
    - {"type":"svg","index":70,"filename":"Anthropic_-_Tavily_Docs/svg_70.png","width":20,"height":20}
    - {"type":"svg","index":71,"filename":"Anthropic_-_Tavily_Docs/svg_71.png","width":20,"height":20}
    - {"type":"svg","index":72,"filename":"Anthropic_-_Tavily_Docs/svg_72.png","width":20,"height":20}
    - {"type":"svg","index":73,"filename":"Anthropic_-_Tavily_Docs/svg_73.png","width":20,"height":20}
    - {"type":"svg","index":74,"filename":"Anthropic_-_Tavily_Docs/svg_74.png","width":49,"height":14}
    - {"type":"svg","index":75,"filename":"Anthropic_-_Tavily_Docs/svg_75.png","width":16,"height":16}
    - {"type":"svg","index":76,"filename":"Anthropic_-_Tavily_Docs/svg_76.png","width":16,"height":16}
    - {"type":"svg","index":77,"filename":"Anthropic_-_Tavily_Docs/svg_77.png","width":16,"height":16}
    - {"type":"svg","index":87,"filename":"Anthropic_-_Tavily_Docs/svg_87.png","width":16,"height":16}
    - {"type":"svg","index":88,"filename":"Anthropic_-_Tavily_Docs/svg_88.png","width":14,"height":14}
    - {"type":"svg","index":89,"filename":"Anthropic_-_Tavily_Docs/svg_89.png","width":16,"height":16}
    - {"type":"svg","index":90,"filename":"Anthropic_-_Tavily_Docs/svg_90.png","width":12,"height":12}
    - {"type":"svg","index":91,"filename":"Anthropic_-_Tavily_Docs/svg_91.png","width":14,"height":14}
    - {"type":"svg","index":92,"filename":"Anthropic_-_Tavily_Docs/svg_92.png","width":16,"height":16}
    - {"type":"svg","index":93,"filename":"Anthropic_-_Tavily_Docs/svg_93.png","width":12,"height":12}
    - {"type":"svg","index":94,"filename":"Anthropic_-_Tavily_Docs/svg_94.png","width":14,"height":14}
    - {"type":"svg","index":95,"filename":"Anthropic_-_Tavily_Docs/svg_95.png","width":16,"height":16}
    - {"type":"svg","index":96,"filename":"Anthropic_-_Tavily_Docs/svg_96.png","width":12,"height":12}
    - {"type":"svg","index":97,"filename":"Anthropic_-_Tavily_Docs/svg_97.png","width":14,"height":14}
  chartData: []
  blockquotes:
    - "Note: When using these schemas, you can customize which parameters are exposed to the model based on your specific use case. For example, if you are building a finance application, you might set topic: \"finance\" for all queries without exposing the topic parameter. This way, the LLM can focus on deciding other parameters, such as time_range, country, and so on, based on the user’s request. Feel free to modify these schemas as needed and only pass the parameters that are relevant to your application."
    - "API Format: The schemas below are for Anthropic’s tool format. Each tool uses the input_schema structure with type, properties, and required fields."
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

# Anthropic

## 源URL

https://docs.tavily.com/documentation/integrations/anthropic

## 描述

Integrate Tavily with Anthropic Claude to enhance your AI applications with real-time web search capabilities.

## 内容

### Installation

```text
pip install anthropic tavily-python
```

### Setup

```text
import os
# Set your API keys
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["TAVILY_API_KEY"] = "your-tavily-api-key"
```

### Using Tavily with Anthropic tool calling

```text
import json
from anthropic import Anthropic
from tavily import TavilyClient

# Initialize clients
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
MODEL_NAME = "claude-sonnet-4-20250514"
```

### Implementation

#### System prompt

```text
SYSTEM_PROMPT = (
    "You are a research assistant. Use the tavily_search tool when needed. "
    "After tools run and tool results are provided back to you, produce a concise, well-structured summary "
    "with a short bullet list of key points and a 'Sources' section listing the URLs. "
)
```

#### Tool schema

```text
tools = [
    {
        "name": "tavily_search",
        "description": "Search the web using Tavily. Return relevant links & summaries.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string."},
                "max_results": {"type": "integer", "default": 5},
                "search_depth": {"type": "string", "enum": ["basic", "advanced"]},
            },
            "required": ["query"]
        }
    }
]
```

#### Tool execution

```text
def tavily_search(**kwargs):
    return tavily_client.search(**kwargs)

def process_tool_call(name, args):
    if name == "tavily_search":
        return tavily_search(**args)
    raise ValueError(f"Unknown tool: {name}")
```

#### Main chat function

```text
def chat_with_claude(user_message: str):
    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    # ---- Call 1: allow tools so Claude can ask for searches ----
    initial_response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": [{"type": "text", "text": user_message}]}],
        tools=tools,
    )

    print("\nInitial Response stop_reason:", initial_response.stop_reason)
    print("Initial content:", initial_response.content)

    # If Claude already answered in text, return it
    if initial_response.stop_reason != "tool_use":
        final_text = next((b.text for b in initial_response.content if getattr(b, "type", None) == "text"), None)
        print("\nFinal Response:", final_text)
        return final_text

    # ---- Execute ALL tool_use blocks from Call 1 ----
    tool_result_blocks = []
    for block in initial_response.content:
        if getattr(block, "type", None) == "tool_use":
            result = process_tool_call(block.name, block.input)
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": [{"type": "text", "text": json.dumps(result)}],
            })

    # ---- Call 2: NO tools; ask for the final summary from tool results ----
    final_response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": [{"type": "text", "text": user_message}]},
            {"role": "assistant", "content": initial_response.content},    # Claude's tool requests
            {"role": "user", "content": tool_result_blocks},    # Your tool results
            {"role": "user", "content": [{"type": "text", "text":
                "Please synthesize the final answer now based on the tool results above. "
                "Include 3–7 bullets and a 'Sources' section with URLs."}]},
        ],
    )

    final_text = next((b.text for b in final_response.content if getattr(b, "type", None) == "text"), None)
    print("\nFinal Response:", final_text)
    return final_text
```

#### Usage example

```text
# Example usage
chat_with_claude("What is trending now in the agents space in 2025?")
```

### Tavily endpoints schema for Anthropic tool definition

> Note: When using these schemas, you can customize which parameters are exposed to the model based on your specific use case. For example, if you are building a finance application, you might set topic: "finance" for all queries without exposing the topic parameter. This way, the LLM can focus on deciding other parameters, such as time_range, country, and so on, based on the user’s request. Feel free to modify these schemas as needed and only pass the parameters that are relevant to your application.

> API Format: The schemas below are for Anthropic’s tool format. Each tool uses the input_schema structure with type, properties, and required fields.

## 图片

![light logo](Anthropic_-_Tavily_Docs/image_1.svg)

![dark logo](Anthropic_-_Tavily_Docs/image_2.svg)

![light logo](Anthropic_-_Tavily_Docs/image_3.svg)

![dark logo](Anthropic_-_Tavily_Docs/image_4.svg)

![tavily-logo](Anthropic_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Anthropic_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Anthropic_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Anthropic_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Anthropic_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Anthropic_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Anthropic_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Anthropic_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Anthropic_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Anthropic_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Anthropic_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Anthropic_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Anthropic_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Anthropic_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Anthropic_-_Tavily_Docs/svg_23.png)
*尺寸: 16x16px*

![SVG图表 24](Anthropic_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Anthropic_-_Tavily_Docs/svg_25.png)
*尺寸: 14x12px*

![SVG图表 26](Anthropic_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Anthropic_-_Tavily_Docs/svg_27.png)
*尺寸: 16x16px*

![SVG图表 28](Anthropic_-_Tavily_Docs/svg_28.png)
*尺寸: 14x12px*

![SVG图表 29](Anthropic_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Anthropic_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 31](Anthropic_-_Tavily_Docs/svg_31.png)
*尺寸: 14x12px*

![SVG图表 32](Anthropic_-_Tavily_Docs/svg_32.png)
*尺寸: 14x12px*

![SVG图表 33](Anthropic_-_Tavily_Docs/svg_33.png)
*尺寸: 16x16px*

![SVG图表 34](Anthropic_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Anthropic_-_Tavily_Docs/svg_35.png)
*尺寸: 14x12px*

![SVG图表 36](Anthropic_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](Anthropic_-_Tavily_Docs/svg_37.png)
*尺寸: 16x16px*

![SVG图表 38](Anthropic_-_Tavily_Docs/svg_38.png)
*尺寸: 14x12px*

![SVG图表 39](Anthropic_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](Anthropic_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](Anthropic_-_Tavily_Docs/svg_41.png)
*尺寸: 14x12px*

![SVG图表 42](Anthropic_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](Anthropic_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](Anthropic_-_Tavily_Docs/svg_44.png)
*尺寸: 14x12px*

![SVG图表 45](Anthropic_-_Tavily_Docs/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](Anthropic_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](Anthropic_-_Tavily_Docs/svg_47.png)
*尺寸: 12x12px*

![SVG图表 48](Anthropic_-_Tavily_Docs/svg_48.png)
*尺寸: 16x16px*

![SVG图表 49](Anthropic_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](Anthropic_-_Tavily_Docs/svg_50.png)
*尺寸: 14x12px*

![SVG图表 51](Anthropic_-_Tavily_Docs/svg_51.png)
*尺寸: 12x12px*

![SVG图表 52](Anthropic_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](Anthropic_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 54](Anthropic_-_Tavily_Docs/svg_54.png)
*尺寸: 12x12px*

![SVG图表 55](Anthropic_-_Tavily_Docs/svg_55.png)
*尺寸: 16x16px*

![SVG图表 56](Anthropic_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](Anthropic_-_Tavily_Docs/svg_57.png)
*尺寸: 12x12px*

![SVG图表 58](Anthropic_-_Tavily_Docs/svg_58.png)
*尺寸: 16x16px*

![SVG图表 59](Anthropic_-_Tavily_Docs/svg_59.png)
*尺寸: 16x16px*

![SVG图表 60](Anthropic_-_Tavily_Docs/svg_60.png)
*尺寸: 12x12px*

![SVG图表 61](Anthropic_-_Tavily_Docs/svg_61.png)
*尺寸: 16x16px*

![SVG图表 62](Anthropic_-_Tavily_Docs/svg_62.png)
*尺寸: 16x16px*

![SVG图表 63](Anthropic_-_Tavily_Docs/svg_63.png)
*尺寸: 14x14px*

![SVG图表 64](Anthropic_-_Tavily_Docs/svg_64.png)
*尺寸: 14x14px*

![SVG图表 65](Anthropic_-_Tavily_Docs/svg_65.png)
*尺寸: 14x14px*

![SVG图表 70](Anthropic_-_Tavily_Docs/svg_70.png)
*尺寸: 20x20px*

![SVG图表 71](Anthropic_-_Tavily_Docs/svg_71.png)
*尺寸: 20x20px*

![SVG图表 72](Anthropic_-_Tavily_Docs/svg_72.png)
*尺寸: 20x20px*

![SVG图表 73](Anthropic_-_Tavily_Docs/svg_73.png)
*尺寸: 20x20px*

![SVG图表 74](Anthropic_-_Tavily_Docs/svg_74.png)
*尺寸: 49x14px*

![SVG图表 75](Anthropic_-_Tavily_Docs/svg_75.png)
*尺寸: 16x16px*

![SVG图表 76](Anthropic_-_Tavily_Docs/svg_76.png)
*尺寸: 16x16px*

![SVG图表 77](Anthropic_-_Tavily_Docs/svg_77.png)
*尺寸: 16x16px*

![SVG图表 87](Anthropic_-_Tavily_Docs/svg_87.png)
*尺寸: 16x16px*

![SVG图表 88](Anthropic_-_Tavily_Docs/svg_88.png)
*尺寸: 14x14px*

![SVG图表 89](Anthropic_-_Tavily_Docs/svg_89.png)
*尺寸: 16x16px*

![SVG图表 90](Anthropic_-_Tavily_Docs/svg_90.png)
*尺寸: 12x12px*

![SVG图表 91](Anthropic_-_Tavily_Docs/svg_91.png)
*尺寸: 14x14px*

![SVG图表 92](Anthropic_-_Tavily_Docs/svg_92.png)
*尺寸: 16x16px*

![SVG图表 93](Anthropic_-_Tavily_Docs/svg_93.png)
*尺寸: 12x12px*

![SVG图表 94](Anthropic_-_Tavily_Docs/svg_94.png)
*尺寸: 14x14px*

![SVG图表 95](Anthropic_-_Tavily_Docs/svg_95.png)
*尺寸: 16x16px*

![SVG图表 96](Anthropic_-_Tavily_Docs/svg_96.png)
*尺寸: 12x12px*

![SVG图表 97](Anthropic_-_Tavily_Docs/svg_97.png)
*尺寸: 14x14px*
