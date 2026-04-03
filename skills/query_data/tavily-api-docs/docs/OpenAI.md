---
id: "url-b9a38de"
type: "website"
title: "OpenAI"
url: "https://docs.tavily.com/documentation/integrations/openai"
description: "Integrate Tavily with OpenAI to enhance your AI applications with real-time web search capabilities."
source: ""
tags: []
crawl_time: "2026-03-18T02:58:45.264Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"OpenAI"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#prerequisites)Prerequisites"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#installation)Installation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#setup)Setup"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-agents-sdk)Using Tavily with OpenAI agents SDK"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-chat-completions-api-function-calling)Using Tavily with OpenAI Chat Completions API function calling"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#function-definition)Function definition"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-responses-api-function-calling)Using Tavily with OpenAI Responses API function calling"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#function-definition-2)Function definition"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/openai#tavily-endpoints-schema-for-openai-responses-api-tool-definition)Tavily endpoints schema for OpenAI Responses API tool definition"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#prerequisites)Prerequisites"}
    - {"type":"list","listType":"ul","items":["An OpenAI API key from [OpenAI Platform](https://platform.openai.com/)","A Tavily API key from [Tavily Dashboard](https://app.tavily.com/sign-in)"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#installation)Installation"}
    - {"type":"codeblock","language":"","content":"pip install openai tavily-python"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#setup)Setup"}
    - {"type":"codeblock","language":"","content":"import os\n\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-agents-sdk)Using Tavily with OpenAI agents SDK"}
    - {"type":"codeblock","language":"","content":"pip install -U openai-agents"}
    - {"type":"codeblock","language":"","content":"import os\nimport asyncio\nfrom agents import Agent, Runner, function_tool\nfrom tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])"}
    - {"type":"codeblock","language":"","content":"@function_tool\ndef tavily_search(query: str) -> str:\n    \"\"\"\n    Perform a web search using Tavily and return a summarized result.\n    \"\"\"\n    response = tavily_client.search(query,search_depth='advanced',max_results='5')\n    results = response.get(\"results\", [])\n    return results or \"No results found.\""}
    - {"type":"blockquote","content":"Note: You can enhance the function by adding more parameters like topic=\"news\", include_domains=[\"example.com\"], time_range=\"week\", etc. to customize your search results."}
    - {"type":"blockquote","content":"You can set auto_parameters=True to have Tavily automatically configure search parameters based on the content and intent of your query. You can still set other parameters manually, and any explicit values you provide will override the automatic ones."}
    - {"type":"codeblock","language":"","content":"async def main():\n    agent = Agent(\n        name=\"Web Research Agent\",\n        instructions=\"Use tavily_search when you need up-to-date info.\",\n        tools=[tavily_search],\n    )\n    out = await Runner.run(agent, \"Latest developments about quantum computing from 2025\")\n    print(out.final_output)"}
    - {"type":"codeblock","language":"","content":"asyncio.run(main())"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-chat-completions-api-function-calling)Using Tavily with OpenAI Chat Completions API function calling"}
    - {"type":"codeblock","language":"","content":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# Load your API keys from environment variables\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#function-definition)Function definition"}
    - {"type":"codeblock","language":"","content":"def tavily_search(**kwargs):\n    # Pass ALL supported kwargs straight to Tavily\n    results = tavily_client.search(**kwargs)\n    return results"}
    - {"type":"codeblock","language":"","content":"# --- define tools ---\ntools = [\n    {\n        \"type\": \"function\",\n        \"function\": {\n            \"name\": \"tavily_search\",\n            \"description\": \"Search the web with Tavily for up-to-date information\",\n            \"parameters\": {\n                \"type\": \"object\",\n                \"properties\": {\n                    \"query\": {\"type\": \"string\", \"description\": \"The search query\"},\n                    \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                },\n                \"required\": [\"query\"],\n            },\n        },\n    }\n]"}
    - {"type":"codeblock","language":"","content":"# --- conversation ---\nmessages = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]"}
    - {"type":"codeblock","language":"","content":"#Ask the model; let it decide whether to call the tool\nresponse = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n    tools=tools,\n)"}
    - {"type":"codeblock","language":"","content":"assistant_msg = response.choices[0].message\n # keep the assistant msg that requested tool(s)\nmessages.append(assistant_msg)"}
    - {"type":"codeblock","language":"","content":"if getattr(assistant_msg, \"tool_calls\", None):\n    for tc in assistant_msg.tool_calls:\n        args = tc.function.arguments\n        if isinstance(args, str):\n            args = json.loads(args)\n        elif not isinstance(args, dict):\n            args = json.loads(str(args))\n\n        if tc.function.name == \"tavily_search\":\n            # forward ALL args\n            results = tavily_search(**args)\n\n            messages.append({\n                \"role\": \"tool\",\n                \"tool_call_id\": tc.id,\n                \"name\": \"tavily_search\",\n                \"content\": json.dumps(results),\n            })\nelse:\n    print(\"\\nNo tool call requested by the model.\")"}
    - {"type":"codeblock","language":"","content":"# Ask the model again for the final grounded answer\nfinal = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n)\n\nfinal_msg = final.choices[0].message\nprint(\"\\nFINAL ANSWER:\\n\", final_msg.content or \"(no content)\")"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-responses-api-function-calling)Using Tavily with OpenAI Responses API function calling"}
    - {"type":"codeblock","language":"","content":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# --- setup ---\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#function-definition-2)Function definition"}
    - {"type":"codeblock","language":"","content":"# --- Function that will be called when AI requests a search ---\ndef tavily_search(**kwargs):\n    \"\"\"\n    Execute a Tavily web search with the given parameters.\n    This function is called by the AI when it needs to search the web.\n    \"\"\"\n    results = tavily_client.search(**kwargs)\n    return results"}
    - {"type":"codeblock","language":"","content":"# Define the tool for Tavily web search\n# This tells the AI what function it can call and what parameters it needs\ntools = [{\n    \"type\": \"function\",\n    \"name\": \"tavily_search\",\n    \"description\": \"Search the web using Tavily. Provide relevant links in your answer.\",\n    \"parameters\": {\n        \"type\": \"object\",\n        \"properties\": {\n            \"query\": {\n                \"type\": \"string\",\n                \"description\": \"Search query for Tavily.\"\n            },\n            \"max_results\": {\n                \"type\": \"integer\",\n                \"description\": \"Max number of results to return\",\n                \"default\": 5\n            }\n        },\n        \"required\": [\"query\", \"max_results\"], \n        \"additionalProperties\": False\n    },\n    \"strict\": True\n}]"}
    - {"type":"codeblock","language":"","content":"# --- Step 1: Create initial conversation ---\n# This sets up the conversation context for the AI\ninput_list = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]\n\n# --- Step 2: First API call - AI decides to search ---\n# The AI will analyze the user's question and decide if it needs to search the web\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    tools=tools,\n    input=input_list,\n)\n\n# --- Step 3: Process the AI's response ---\n# Add the AI's response (including any function calls) to our conversation\ninput_list += response.output"}
    - {"type":"codeblock","language":"","content":"# --- Step 4: Execute any function calls the AI made ---\nfor item in response.output:\n    if item.type == \"function_call\":\n        if item.name == \"tavily_search\":\n            # Parse the arguments the AI provided for the search\n            parsed_args = json.loads(item.arguments)\n            \n            # Execute the actual Tavily search\n            results = tavily_search(**parsed_args)\n            \n            # Add the search results back to the conversation\n            # This tells the AI what it found when it searched\n            function_output = {\n                \"type\": \"function_call_output\",\n                \"call_id\": item.call_id,\n                \"output\": json.dumps({\n                  \"results\": results\n                })\n            }\n            input_list.append(function_output)"}
    - {"type":"codeblock","language":"","content":"# --- Step 5: Second API call - AI provides final answer ---\n# Now the AI has the search results and can provide an informed response\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    instructions=\"Based on the Tavily search results provided, give me a comprehensive summary with citations.\",\n    input=input_list,\n)\n\n# --- Display the final result ---\nprint(\"AI Response:\")\nprint(response.output_text)"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/openai#tavily-endpoints-schema-for-openai-responses-api-tool-definition)Tavily endpoints schema for OpenAI Responses API tool definition"}
    - {"type":"blockquote","content":"Note: When using these schemas, you can customize which parameters are exposed to the model based on your specific use case. For example, if you are building a finance application, you might set topic: \"finance\" for all queries without exposing the topic parameter. This way, the LLM can focus on deciding other parameters, such as time_range, country, and so on, based on the user’s request. Feel free to modify these schemas as needed and only pass the parameters that are relevant to your application."}
    - {"type":"blockquote","content":"API Format: The schemas below are for OpenAI Responses API. For Chat Completions API, wrap the parameters in a \"function\" object: {\"type\": \"function\", \"function\": {\"name\": \"...\", \"parameters\": {...}}}."}
  paragraphs:
    - "Full Code Example"
    - "Full Code Example"
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
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/integrations/openai#introduction)","[Prerequisites](https://docs.tavily.com/documentation/integrations/openai#prerequisites)","[Installation](https://docs.tavily.com/documentation/integrations/openai#installation)","[Setup](https://docs.tavily.com/documentation/integrations/openai#setup)","[Using Tavily with OpenAI agents SDK](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-agents-sdk)","[Using Tavily with OpenAI Chat Completions API function calling](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-chat-completions-api-function-calling)","[Function definition](https://docs.tavily.com/documentation/integrations/openai#function-definition)","[Using Tavily with OpenAI Responses API function calling](https://docs.tavily.com/documentation/integrations/openai#using-tavily-with-openai-responses-api-function-calling)","[Function definition](https://docs.tavily.com/documentation/integrations/openai#function-definition-2)","[Tavily endpoints schema for OpenAI Responses API tool definition](https://docs.tavily.com/documentation/integrations/openai#tavily-endpoints-schema-for-openai-responses-api-tool-definition)"]}
    - {"type":"ul","items":["An OpenAI API key from [OpenAI Platform](https://platform.openai.com/)","A Tavily API key from [Tavily Dashboard](https://app.tavily.com/sign-in)"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install openai tavily-python"}
    - {"language":"text","code":"pip install openai tavily-python"}
    - {"language":"text","code":"import os\n\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"language":"text","code":"import os\n\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"language":"text","code":"pip install -U openai-agents"}
    - {"language":"text","code":"pip install -U openai-agents"}
    - {"language":"text","code":"import os\nimport asyncio\nfrom agents import Agent, Runner, function_tool\nfrom tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])"}
    - {"language":"text","code":"import os\nimport asyncio\nfrom agents import Agent, Runner, function_tool\nfrom tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])"}
    - {"language":"text","code":"@function_tool\ndef tavily_search(query: str) -> str:\n    \"\"\"\n    Perform a web search using Tavily and return a summarized result.\n    \"\"\"\n    response = tavily_client.search(query,search_depth='advanced',max_results='5')\n    results = response.get(\"results\", [])\n    return results or \"No results found.\""}
    - {"language":"text","code":"@function_tool\ndef tavily_search(query: str) -> str:\n    \"\"\"\n    Perform a web search using Tavily and return a summarized result.\n    \"\"\"\n    response = tavily_client.search(query,search_depth='advanced',max_results='5')\n    results = response.get(\"results\", [])\n    return results or \"No results found.\""}
    - {"language":"text","code":"async def main():\n    agent = Agent(\n        name=\"Web Research Agent\",\n        instructions=\"Use tavily_search when you need up-to-date info.\",\n        tools=[tavily_search],\n    )\n    out = await Runner.run(agent, \"Latest developments about quantum computing from 2025\")\n    print(out.final_output)"}
    - {"language":"text","code":"async def main():\n    agent = Agent(\n        name=\"Web Research Agent\",\n        instructions=\"Use tavily_search when you need up-to-date info.\",\n        tools=[tavily_search],\n    )\n    out = await Runner.run(agent, \"Latest developments about quantum computing from 2025\")\n    print(out.final_output)"}
    - {"language":"text","code":"asyncio.run(main())"}
    - {"language":"text","code":"asyncio.run(main())"}
    - {"language":"text","code":"import os\nimport asyncio\nfrom agents import Agent, Runner, function_tool\nfrom tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\n\n@function_tool\ndef tavily_search(query: str) -> str:\n    \"\"\"\n    Perform a web search using Tavily and return a summarized result.\n    \"\"\"\n    response = tavily_client.search(query,search_depth='advanced',max_results='5')\n    results = response.get(\"results\", [])\n    return results or \"No results found.\"\n\nasync def main():\n    agent = Agent(\n        name=\"Web Research Agent\",\n        instructions=\"Use tavily_search when you need up-to-date info.\",\n        tools=[tavily_search],\n    )\n    out = await Runner.run(agent, \"Latest developments about quantum computing from 2025\")\n    print(out.final_output)\n\n\nasyncio.run(main())"}
    - {"language":"text","code":"import os\nimport asyncio\nfrom agents import Agent, Runner, function_tool\nfrom tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\n\n@function_tool\ndef tavily_search(query: str) -> str:\n    \"\"\"\n    Perform a web search using Tavily and return a summarized result.\n    \"\"\"\n    response = tavily_client.search(query,search_depth='advanced',max_results='5')\n    results = response.get(\"results\", [])\n    return results or \"No results found.\"\n\nasync def main():\n    agent = Agent(\n        name=\"Web Research Agent\",\n        instructions=\"Use tavily_search when you need up-to-date info.\",\n        tools=[tavily_search],\n    )\n    out = await Runner.run(agent, \"Latest developments about quantum computing from 2025\")\n    print(out.final_output)\n\n\nasyncio.run(main())"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# Load your API keys from environment variables\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# Load your API keys from environment variables\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])"}
    - {"language":"text","code":"def tavily_search(**kwargs):\n    # Pass ALL supported kwargs straight to Tavily\n    results = tavily_client.search(**kwargs)\n    return results"}
    - {"language":"text","code":"def tavily_search(**kwargs):\n    # Pass ALL supported kwargs straight to Tavily\n    results = tavily_client.search(**kwargs)\n    return results"}
    - {"language":"text","code":"# --- define tools ---\ntools = [\n    {\n        \"type\": \"function\",\n        \"function\": {\n            \"name\": \"tavily_search\",\n            \"description\": \"Search the web with Tavily for up-to-date information\",\n            \"parameters\": {\n                \"type\": \"object\",\n                \"properties\": {\n                    \"query\": {\"type\": \"string\", \"description\": \"The search query\"},\n                    \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                },\n                \"required\": [\"query\"],\n            },\n        },\n    }\n]"}
    - {"language":"text","code":"# --- define tools ---\ntools = [\n    {\n        \"type\": \"function\",\n        \"function\": {\n            \"name\": \"tavily_search\",\n            \"description\": \"Search the web with Tavily for up-to-date information\",\n            \"parameters\": {\n                \"type\": \"object\",\n                \"properties\": {\n                    \"query\": {\"type\": \"string\", \"description\": \"The search query\"},\n                    \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                },\n                \"required\": [\"query\"],\n            },\n        },\n    }\n]"}
    - {"language":"text","code":"# --- conversation ---\nmessages = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]"}
    - {"language":"text","code":"# --- conversation ---\nmessages = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]"}
    - {"language":"text","code":"#Ask the model; let it decide whether to call the tool\nresponse = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n    tools=tools,\n)"}
    - {"language":"text","code":"#Ask the model; let it decide whether to call the tool\nresponse = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n    tools=tools,\n)"}
    - {"language":"text","code":"assistant_msg = response.choices[0].message\n # keep the assistant msg that requested tool(s)\nmessages.append(assistant_msg)"}
    - {"language":"text","code":"assistant_msg = response.choices[0].message\n # keep the assistant msg that requested tool(s)\nmessages.append(assistant_msg)"}
    - {"language":"text","code":"if getattr(assistant_msg, \"tool_calls\", None):\n    for tc in assistant_msg.tool_calls:\n        args = tc.function.arguments\n        if isinstance(args, str):\n            args = json.loads(args)\n        elif not isinstance(args, dict):\n            args = json.loads(str(args))\n\n        if tc.function.name == \"tavily_search\":\n            # forward ALL args\n            results = tavily_search(**args)\n\n            messages.append({\n                \"role\": \"tool\",\n                \"tool_call_id\": tc.id,\n                \"name\": \"tavily_search\",\n                \"content\": json.dumps(results),\n            })\nelse:\n    print(\"\\nNo tool call requested by the model.\")"}
    - {"language":"text","code":"if getattr(assistant_msg, \"tool_calls\", None):\n    for tc in assistant_msg.tool_calls:\n        args = tc.function.arguments\n        if isinstance(args, str):\n            args = json.loads(args)\n        elif not isinstance(args, dict):\n            args = json.loads(str(args))\n\n        if tc.function.name == \"tavily_search\":\n            # forward ALL args\n            results = tavily_search(**args)\n\n            messages.append({\n                \"role\": \"tool\",\n                \"tool_call_id\": tc.id,\n                \"name\": \"tavily_search\",\n                \"content\": json.dumps(results),\n            })\nelse:\n    print(\"\\nNo tool call requested by the model.\")"}
    - {"language":"text","code":"# Ask the model again for the final grounded answer\nfinal = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n)\n\nfinal_msg = final.choices[0].message\nprint(\"\\nFINAL ANSWER:\\n\", final_msg.content or \"(no content)\")"}
    - {"language":"text","code":"# Ask the model again for the final grounded answer\nfinal = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n)\n\nfinal_msg = final.choices[0].message\nprint(\"\\nFINAL ANSWER:\\n\", final_msg.content or \"(no content)\")"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# --- setup ---\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])\n\ndef tavily_search(**kwargs):\n    # Pass ALL supported kwargs straight to Tavily\n    results = tavily_client.search(**kwargs)\n    return results\n\n# --- define tools ---\ntools = [\n    {\n        \"type\": \"function\",\n        \"function\": {\n            \"name\": \"tavily_search\",\n            \"description\": \"Search the web with Tavily for up-to-date information\",\n            \"parameters\": {\n                \"type\": \"object\",\n                \"properties\": {\n                    \"query\": {\"type\": \"string\", \"description\": \"The search query\"},\n                    \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                },\n                \"required\": [\"query\"],\n            },\n        },\n    }\n]\n\n\n# --- conversation ---\nmessages = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]\n\n\n#Ask the model; let it decide whether to call the tool\nresponse = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n    tools=tools,\n)\n\nassistant_msg = response.choices[0].message\nmessages.append(assistant_msg)  # keep the assistant msg that requested tool(s)\n\nif getattr(assistant_msg, \"tool_calls\", None):\n    for tc in assistant_msg.tool_calls:\n        args = tc.function.arguments\n        if isinstance(args, str):\n            args = json.loads(args)\n        elif not isinstance(args, dict):\n            args = json.loads(str(args))\n\n        if tc.function.name == \"tavily_search\":\n            # forward ALL args\n            results = tavily_search(**args)\n\n            messages.append({\n                \"role\": \"tool\",\n                \"tool_call_id\": tc.id,\n                \"name\": \"tavily_search\",\n                \"content\": json.dumps(results),\n            })\nelse:\n    print(\"\\nNo tool call requested by the model.\")\n\n# Ask the model again for the final grounded answer\nfinal = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n)\n\nfinal_msg = final.choices[0].message\nprint(\"\\nFINAL ANSWER:\\n\", final_msg.content or \"(no content)\")"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# --- setup ---\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])\n\ndef tavily_search(**kwargs):\n    # Pass ALL supported kwargs straight to Tavily\n    results = tavily_client.search(**kwargs)\n    return results\n\n# --- define tools ---\ntools = [\n    {\n        \"type\": \"function\",\n        \"function\": {\n            \"name\": \"tavily_search\",\n            \"description\": \"Search the web with Tavily for up-to-date information\",\n            \"parameters\": {\n                \"type\": \"object\",\n                \"properties\": {\n                    \"query\": {\"type\": \"string\", \"description\": \"The search query\"},\n                    \"max_results\": {\"type\": \"integer\", \"default\": 5},\n                },\n                \"required\": [\"query\"],\n            },\n        },\n    }\n]\n\n\n# --- conversation ---\nmessages = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]\n\n\n#Ask the model; let it decide whether to call the tool\nresponse = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n    tools=tools,\n)\n\nassistant_msg = response.choices[0].message\nmessages.append(assistant_msg)  # keep the assistant msg that requested tool(s)\n\nif getattr(assistant_msg, \"tool_calls\", None):\n    for tc in assistant_msg.tool_calls:\n        args = tc.function.arguments\n        if isinstance(args, str):\n            args = json.loads(args)\n        elif not isinstance(args, dict):\n            args = json.loads(str(args))\n\n        if tc.function.name == \"tavily_search\":\n            # forward ALL args\n            results = tavily_search(**args)\n\n            messages.append({\n                \"role\": \"tool\",\n                \"tool_call_id\": tc.id,\n                \"name\": \"tavily_search\",\n                \"content\": json.dumps(results),\n            })\nelse:\n    print(\"\\nNo tool call requested by the model.\")\n\n# Ask the model again for the final grounded answer\nfinal = openai_client.chat.completions.create(\n    model=\"gpt-4o-mini\",\n    messages=messages,\n)\n\nfinal_msg = final.choices[0].message\nprint(\"\\nFINAL ANSWER:\\n\", final_msg.content or \"(no content)\")"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# --- setup ---\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# --- setup ---\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])"}
    - {"language":"text","code":"# --- Function that will be called when AI requests a search ---\ndef tavily_search(**kwargs):\n    \"\"\"\n    Execute a Tavily web search with the given parameters.\n    This function is called by the AI when it needs to search the web.\n    \"\"\"\n    results = tavily_client.search(**kwargs)\n    return results"}
    - {"language":"text","code":"# --- Function that will be called when AI requests a search ---\ndef tavily_search(**kwargs):\n    \"\"\"\n    Execute a Tavily web search with the given parameters.\n    This function is called by the AI when it needs to search the web.\n    \"\"\"\n    results = tavily_client.search(**kwargs)\n    return results"}
    - {"language":"text","code":"# Define the tool for Tavily web search\n# This tells the AI what function it can call and what parameters it needs\ntools = [{\n    \"type\": \"function\",\n    \"name\": \"tavily_search\",\n    \"description\": \"Search the web using Tavily. Provide relevant links in your answer.\",\n    \"parameters\": {\n        \"type\": \"object\",\n        \"properties\": {\n            \"query\": {\n                \"type\": \"string\",\n                \"description\": \"Search query for Tavily.\"\n            },\n            \"max_results\": {\n                \"type\": \"integer\",\n                \"description\": \"Max number of results to return\",\n                \"default\": 5\n            }\n        },\n        \"required\": [\"query\", \"max_results\"], \n        \"additionalProperties\": False\n    },\n    \"strict\": True\n}]"}
    - {"language":"text","code":"# Define the tool for Tavily web search\n# This tells the AI what function it can call and what parameters it needs\ntools = [{\n    \"type\": \"function\",\n    \"name\": \"tavily_search\",\n    \"description\": \"Search the web using Tavily. Provide relevant links in your answer.\",\n    \"parameters\": {\n        \"type\": \"object\",\n        \"properties\": {\n            \"query\": {\n                \"type\": \"string\",\n                \"description\": \"Search query for Tavily.\"\n            },\n            \"max_results\": {\n                \"type\": \"integer\",\n                \"description\": \"Max number of results to return\",\n                \"default\": 5\n            }\n        },\n        \"required\": [\"query\", \"max_results\"], \n        \"additionalProperties\": False\n    },\n    \"strict\": True\n}]"}
    - {"language":"text","code":"# --- Step 1: Create initial conversation ---\n# This sets up the conversation context for the AI\ninput_list = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]\n\n# --- Step 2: First API call - AI decides to search ---\n# The AI will analyze the user's question and decide if it needs to search the web\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    tools=tools,\n    input=input_list,\n)\n\n# --- Step 3: Process the AI's response ---\n# Add the AI's response (including any function calls) to our conversation\ninput_list += response.output"}
    - {"language":"text","code":"# --- Step 1: Create initial conversation ---\n# This sets up the conversation context for the AI\ninput_list = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]\n\n# --- Step 2: First API call - AI decides to search ---\n# The AI will analyze the user's question and decide if it needs to search the web\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    tools=tools,\n    input=input_list,\n)\n\n# --- Step 3: Process the AI's response ---\n# Add the AI's response (including any function calls) to our conversation\ninput_list += response.output"}
    - {"language":"text","code":"# --- Step 4: Execute any function calls the AI made ---\nfor item in response.output:\n    if item.type == \"function_call\":\n        if item.name == \"tavily_search\":\n            # Parse the arguments the AI provided for the search\n            parsed_args = json.loads(item.arguments)\n            \n            # Execute the actual Tavily search\n            results = tavily_search(**parsed_args)\n            \n            # Add the search results back to the conversation\n            # This tells the AI what it found when it searched\n            function_output = {\n                \"type\": \"function_call_output\",\n                \"call_id\": item.call_id,\n                \"output\": json.dumps({\n                  \"results\": results\n                })\n            }\n            input_list.append(function_output)"}
    - {"language":"text","code":"# --- Step 4: Execute any function calls the AI made ---\nfor item in response.output:\n    if item.type == \"function_call\":\n        if item.name == \"tavily_search\":\n            # Parse the arguments the AI provided for the search\n            parsed_args = json.loads(item.arguments)\n            \n            # Execute the actual Tavily search\n            results = tavily_search(**parsed_args)\n            \n            # Add the search results back to the conversation\n            # This tells the AI what it found when it searched\n            function_output = {\n                \"type\": \"function_call_output\",\n                \"call_id\": item.call_id,\n                \"output\": json.dumps({\n                  \"results\": results\n                })\n            }\n            input_list.append(function_output)"}
    - {"language":"text","code":"# --- Step 5: Second API call - AI provides final answer ---\n# Now the AI has the search results and can provide an informed response\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    instructions=\"Based on the Tavily search results provided, give me a comprehensive summary with citations.\",\n    input=input_list,\n)\n\n# --- Display the final result ---\nprint(\"AI Response:\")\nprint(response.output_text)"}
    - {"language":"text","code":"# --- Step 5: Second API call - AI provides final answer ---\n# Now the AI has the search results and can provide an informed response\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    instructions=\"Based on the Tavily search results provided, give me a comprehensive summary with citations.\",\n    input=input_list,\n)\n\n# --- Display the final result ---\nprint(\"AI Response:\")\nprint(response.output_text)"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# --- Setup: Initialize API clients ---\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])\n\n# --- Function that will be called when AI requests a search ---\ndef tavily_search(**kwargs):\n    \"\"\"\n    Execute a Tavily web search with the given parameters.\n    This function is called by the AI when it needs to search the web.\n    \"\"\"\n    results = tavily_client.search(**kwargs)\n    return results\n\n# --- Define the search tool for OpenAI to use ---\n# This tells the AI what function it can call and what parameters it needs\ntools = [{\n    \"type\": \"function\",\n    \"name\": \"tavily_search\",\n    \"description\": \"Search the web using Tavily. Provide relevant links in your answer.\",\n    \"parameters\": {\n        \"type\": \"object\",\n        \"properties\": {\n            \"query\": {\n                \"type\": \"string\",\n                \"description\": \"Search query for Tavily.\"\n            },\n            \"max_results\": {\n                \"type\": \"integer\",\n                \"description\": \"Max number of results to return\",\n                \"default\": 5\n            }\n        },\n        \"required\": [\"query\", \"max_results\"], \n        \"additionalProperties\": False\n    },\n    \"strict\": True\n}]\n\n\n# --- Step 1: Create initial conversation ---\n# This sets up the conversation context for the AI\ninput_list = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]\n\n# --- Step 2: First API call - AI decides to search ---\n# The AI will analyze the user's question and decide if it needs to search the web\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    tools=tools,\n    input=input_list,\n)\n\n# --- Step 3: Process the AI's response ---\n# Add the AI's response (including any function calls) to our conversation\ninput_list += response.output\n\n# --- Step 4: Execute any function calls the AI made ---\nfor item in response.output:\n    if item.type == \"function_call\":\n        if item.name == \"tavily_search\":\n            # Parse the arguments the AI provided for the search\n            parsed_args = json.loads(item.arguments)\n            \n            # Execute the actual Tavily search\n            results = tavily_search(**parsed_args)\n            \n            # Add the search results back to the conversation\n            # This tells the AI what it found when it searched\n            function_output = {\n                \"type\": \"function_call_output\",\n                \"call_id\": item.call_id,\n                \"output\": json.dumps({\n                  \"results\": results\n                })\n            }\n            input_list.append(function_output)\n\n# --- Step 5: Second API call - AI provides final answer ---\n# Now the AI has the search results and can provide an informed response\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    instructions=\"Based on the Tavily search results provided, give me a comprehensive summary with citations.\",\n    input=input_list,\n)\n\n# --- Display the final result ---\nprint(\"AI Response:\")\nprint(response.output_text)"}
    - {"language":"text","code":"import os\nimport json\nfrom tavily import TavilyClient\nfrom openai import OpenAI\n\n# --- Setup: Initialize API clients ---\ntavily_client = TavilyClient(api_key=os.environ[\"TAVILY_API_KEY\"])\nopenai_client = OpenAI(api_key=os.environ[\"OPENAI_API_KEY\"])\n\n# --- Function that will be called when AI requests a search ---\ndef tavily_search(**kwargs):\n    \"\"\"\n    Execute a Tavily web search with the given parameters.\n    This function is called by the AI when it needs to search the web.\n    \"\"\"\n    results = tavily_client.search(**kwargs)\n    return results\n\n# --- Define the search tool for OpenAI to use ---\n# This tells the AI what function it can call and what parameters it needs\ntools = [{\n    \"type\": \"function\",\n    \"name\": \"tavily_search\",\n    \"description\": \"Search the web using Tavily. Provide relevant links in your answer.\",\n    \"parameters\": {\n        \"type\": \"object\",\n        \"properties\": {\n            \"query\": {\n                \"type\": \"string\",\n                \"description\": \"Search query for Tavily.\"\n            },\n            \"max_results\": {\n                \"type\": \"integer\",\n                \"description\": \"Max number of results to return\",\n                \"default\": 5\n            }\n        },\n        \"required\": [\"query\", \"max_results\"], \n        \"additionalProperties\": False\n    },\n    \"strict\": True\n}]\n\n\n# --- Step 1: Create initial conversation ---\n# This sets up the conversation context for the AI\ninput_list = [\n    {\"role\": \"system\", \"content\": \"You are a helpful assistant that uses Tavily search when needed.\"},\n    {\"role\": \"user\", \"content\": \"What are the top trends in 2025 about AI agents?\"}\n]\n\n# --- Step 2: First API call - AI decides to search ---\n# The AI will analyze the user's question and decide if it needs to search the web\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    tools=tools,\n    input=input_list,\n)\n\n# --- Step 3: Process the AI's response ---\n# Add the AI's response (including any function calls) to our conversation\ninput_list += response.output\n\n# --- Step 4: Execute any function calls the AI made ---\nfor item in response.output:\n    if item.type == \"function_call\":\n        if item.name == \"tavily_search\":\n            # Parse the arguments the AI provided for the search\n            parsed_args = json.loads(item.arguments)\n            \n            # Execute the actual Tavily search\n            results = tavily_search(**parsed_args)\n            \n            # Add the search results back to the conversation\n            # This tells the AI what it found when it searched\n            function_output = {\n                \"type\": \"function_call_output\",\n                \"call_id\": item.call_id,\n                \"output\": json.dumps({\n                  \"results\": results\n                })\n            }\n            input_list.append(function_output)\n\n# --- Step 5: Second API call - AI provides final answer ---\n# Now the AI has the search results and can provide an informed response\nresponse = openai_client.responses.create(\n    model=\"gpt-4o-mini\",\n    instructions=\"Based on the Tavily search results provided, give me a comprehensive summary with citations.\",\n    input=input_list,\n)\n\n# --- Display the final result ---\nprint(\"AI Response:\")\nprint(response.output_text)"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_search\",\n        \"description\": \"A powerful web search tool that provides comprehensive, real-time results using Tavily's AI search engine. Returns relevant web content with customizable parameters for result count, content type, and domain filtering. Ideal for gathering current information, news, and detailed web content analysis.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"query\"],\n            \"properties\": {\n                \"query\": {\n                    \"type\": \"string\",\n                    \"description\": \"Search query\"\n                },\n                \"auto_parameters\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Auto-tune parameters based on the query. Explicit values you pass still win.\"\n                },\n                \"topic\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"general\", \"news\",\"finance\"],\n                    \"default\": \"general\",\n                    \"description\": \"The category of the search. This will determine which of our agents will be used for the search\"\n                },\n                \"search_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"The depth of the search. It can be 'basic' or 'advanced'\"\n                },\n                \"chunks_per_source\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 3,\n                    \"default\": 3,\n                    \"description\": \"Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.\"\n                },\n                \"max_results\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 0,\n                    \"maximum\": 20,\n                    \"default\": 5,\n                    \"description\": \"The maximum number of search results to return\"\n                },\n                \"time_range\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"day\", \"week\", \"month\", \"year\"],\n                    \"description\": \"The time range back from the current date to include in the search results. This feature is available for both 'general' and 'news' search topics\"\n                },\n                \"start_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.\"\n                },\n                \"end_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD\"\n                },\n                \"include_answer\": {\n                    \"description\": \"Include an LLM-generated answer. 'basic' is brief; 'advanced' is more detailed.\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_raw_content\": {\n                    \"description\": \"Include the cleaned and parsed HTML content of each search result\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"markdown\", \"text\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images in the response\"\n                },\n                \"include_image_descriptions\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images and their descriptions in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"include_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 300,\n                    \"description\": \"A list of domains to specifically include in the search results, if the user asks to search on specific sites set this to the domain of the site\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 150,\n                    \"description\": \"List of domains to specifically exclude, if the user asks to exclude a domain set this to the domain of the site\"\n                },\n                \"country\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"afghanistan\", \"albania\", \"algeria\", \"andorra\", \"angola\", \"argentina\", \"armenia\", \"australia\", \"austria\", \"azerbaijan\", \"bahamas\", \"bahrain\", \"bangladesh\", \"barbados\", \"belarus\", \"belgium\", \"belize\", \"benin\", \"bhutan\", \"bolivia\", \"bosnia and herzegovina\", \"botswana\", \"brazil\", \"brunei\", \"bulgaria\", \"burkina faso\", \"burundi\", \"cambodia\", \"cameroon\", \"canada\", \"cape verde\", \"central african republic\", \"chad\", \"chile\", \"china\", \"colombia\", \"comoros\", \"congo\", \"costa rica\", \"croatia\", \"cuba\", \"cyprus\", \"czech republic\", \"denmark\", \"djibouti\", \"dominican republic\", \"ecuador\", \"egypt\", \"el salvador\", \"equatorial guinea\", \"eritrea\", \"estonia\", \"ethiopia\", \"fiji\", \"finland\", \"france\", \"gabon\", \"gambia\", \"georgia\", \"germany\", \"ghana\", \"greece\", \"guatemala\", \"guinea\", \"haiti\", \"honduras\", \"hungary\", \"iceland\", \"india\", \"indonesia\", \"iran\", \"iraq\", \"ireland\", \"israel\", \"italy\", \"jamaica\", \"japan\", \"jordan\", \"kazakhstan\", \"kenya\", \"kuwait\", \"kyrgyzstan\", \"latvia\", \"lebanon\", \"lesotho\", \"liberia\", \"libya\", \"liechtenstein\", \"lithuania\", \"luxembourg\", \"madagascar\", \"malawi\", \"malaysia\", \"maldives\", \"mali\", \"malta\", \"mauritania\", \"mauritius\", \"mexico\", \"moldova\", \"monaco\", \"mongolia\", \"montenegro\", \"morocco\", \"mozambique\", \"myanmar\", \"namibia\", \"nepal\", \"netherlands\", \"new zealand\", \"nicaragua\", \"niger\", \"nigeria\", \"north korea\", \"north macedonia\", \"norway\", \"oman\", \"pakistan\", \"panama\", \"papua new guinea\", \"paraguay\", \"peru\", \"philippines\", \"poland\", \"portugal\", \"qatar\", \"romania\", \"russia\", \"rwanda\", \"saudi arabia\", \"senegal\", \"serbia\", \"singapore\", \"slovakia\", \"slovenia\", \"somalia\", \"south africa\", \"south korea\", \"south sudan\", \"spain\", \"sri lanka\", \"sudan\", \"sweden\", \"switzerland\", \"syria\", \"taiwan\", \"tajikistan\", \"tanzania\", \"thailand\", \"togo\", \"trinidad and tobago\", \"tunisia\", \"turkey\", \"turkmenistan\", \"uganda\", \"ukraine\", \"united arab emirates\", \"united kingdom\", \"united states\", \"uruguay\", \"uzbekistan\", \"venezuela\", \"vietnam\", \"yemen\", \"zambia\", \"zimbabwe\"],\n                    \"description\": \"Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general. Country names MUST be written in lowercase, plain English, with spaces and no underscores.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_search\",\n        \"description\": \"A powerful web search tool that provides comprehensive, real-time results using Tavily's AI search engine. Returns relevant web content with customizable parameters for result count, content type, and domain filtering. Ideal for gathering current information, news, and detailed web content analysis.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"query\"],\n            \"properties\": {\n                \"query\": {\n                    \"type\": \"string\",\n                    \"description\": \"Search query\"\n                },\n                \"auto_parameters\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Auto-tune parameters based on the query. Explicit values you pass still win.\"\n                },\n                \"topic\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"general\", \"news\",\"finance\"],\n                    \"default\": \"general\",\n                    \"description\": \"The category of the search. This will determine which of our agents will be used for the search\"\n                },\n                \"search_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"The depth of the search. It can be 'basic' or 'advanced'\"\n                },\n                \"chunks_per_source\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 3,\n                    \"default\": 3,\n                    \"description\": \"Chunks are short content snippets (maximum 500 characters each) pulled directly from the source.\"\n                },\n                \"max_results\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 0,\n                    \"maximum\": 20,\n                    \"default\": 5,\n                    \"description\": \"The maximum number of search results to return\"\n                },\n                \"time_range\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"day\", \"week\", \"month\", \"year\"],\n                    \"description\": \"The time range back from the current date to include in the search results. This feature is available for both 'general' and 'news' search topics\"\n                },\n                \"start_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.\"\n                },\n                \"end_date\": {\n                    \"type\": \"string\",\n                    \"format\": \"date\",\n                    \"description\": \"Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD\"\n                },\n                \"include_answer\": {\n                    \"description\": \"Include an LLM-generated answer. 'basic' is brief; 'advanced' is more detailed.\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"basic\", \"advanced\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_raw_content\": {\n                    \"description\": \"Include the cleaned and parsed HTML content of each search result\",\n                    \"oneOf\": [\n                        {\"type\": \"boolean\"},\n                        {\"type\": \"string\", \"enum\": [\"markdown\", \"text\"]}\n                    ],\n                    \"default\": False\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images in the response\"\n                },\n                \"include_image_descriptions\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of query-related images and their descriptions in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"include_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 300,\n                    \"description\": \"A list of domains to specifically include in the search results, if the user asks to search on specific sites set this to the domain of the site\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"maxItems\": 150,\n                    \"description\": \"List of domains to specifically exclude, if the user asks to exclude a domain set this to the domain of the site\"\n                },\n                \"country\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"afghanistan\", \"albania\", \"algeria\", \"andorra\", \"angola\", \"argentina\", \"armenia\", \"australia\", \"austria\", \"azerbaijan\", \"bahamas\", \"bahrain\", \"bangladesh\", \"barbados\", \"belarus\", \"belgium\", \"belize\", \"benin\", \"bhutan\", \"bolivia\", \"bosnia and herzegovina\", \"botswana\", \"brazil\", \"brunei\", \"bulgaria\", \"burkina faso\", \"burundi\", \"cambodia\", \"cameroon\", \"canada\", \"cape verde\", \"central african republic\", \"chad\", \"chile\", \"china\", \"colombia\", \"comoros\", \"congo\", \"costa rica\", \"croatia\", \"cuba\", \"cyprus\", \"czech republic\", \"denmark\", \"djibouti\", \"dominican republic\", \"ecuador\", \"egypt\", \"el salvador\", \"equatorial guinea\", \"eritrea\", \"estonia\", \"ethiopia\", \"fiji\", \"finland\", \"france\", \"gabon\", \"gambia\", \"georgia\", \"germany\", \"ghana\", \"greece\", \"guatemala\", \"guinea\", \"haiti\", \"honduras\", \"hungary\", \"iceland\", \"india\", \"indonesia\", \"iran\", \"iraq\", \"ireland\", \"israel\", \"italy\", \"jamaica\", \"japan\", \"jordan\", \"kazakhstan\", \"kenya\", \"kuwait\", \"kyrgyzstan\", \"latvia\", \"lebanon\", \"lesotho\", \"liberia\", \"libya\", \"liechtenstein\", \"lithuania\", \"luxembourg\", \"madagascar\", \"malawi\", \"malaysia\", \"maldives\", \"mali\", \"malta\", \"mauritania\", \"mauritius\", \"mexico\", \"moldova\", \"monaco\", \"mongolia\", \"montenegro\", \"morocco\", \"mozambique\", \"myanmar\", \"namibia\", \"nepal\", \"netherlands\", \"new zealand\", \"nicaragua\", \"niger\", \"nigeria\", \"north korea\", \"north macedonia\", \"norway\", \"oman\", \"pakistan\", \"panama\", \"papua new guinea\", \"paraguay\", \"peru\", \"philippines\", \"poland\", \"portugal\", \"qatar\", \"romania\", \"russia\", \"rwanda\", \"saudi arabia\", \"senegal\", \"serbia\", \"singapore\", \"slovakia\", \"slovenia\", \"somalia\", \"south africa\", \"south korea\", \"south sudan\", \"spain\", \"sri lanka\", \"sudan\", \"sweden\", \"switzerland\", \"syria\", \"taiwan\", \"tajikistan\", \"tanzania\", \"thailand\", \"togo\", \"trinidad and tobago\", \"tunisia\", \"turkey\", \"turkmenistan\", \"uganda\", \"ukraine\", \"united arab emirates\", \"united kingdom\", \"united states\", \"uruguay\", \"uzbekistan\", \"venezuela\", \"vietnam\", \"yemen\", \"zambia\", \"zimbabwe\"],\n                    \"description\": \"Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general. Country names MUST be written in lowercase, plain English, with spaces and no underscores.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_extract\",\n        \"description\": \"A powerful web content extraction tool that retrieves and processes raw content from specified URLs, ideal for data collection, content analysis, and research tasks.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"urls\"],\n            \"properties\": {\n                \"urls\": {\n                    \"type\": \"string\",\n                    \"description\": \"List of URLs to extract content from\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of images extracted from the urls in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Depth of extraction - 'basic' or 'advanced', if urls are linkedin use 'advanced' or if explicitly told to use advanced\"\n                },\n                \"timeout\": {\n                    \"type\": \"number\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"minimum\": 0,\n                    \"maximum\": 60,\n                    \"default\": None,\n                    \"description\": \"Maximum time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_extract\",\n        \"description\": \"A powerful web content extraction tool that retrieves and processes raw content from specified URLs, ideal for data collection, content analysis, and research tasks.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"urls\"],\n            \"properties\": {\n                \"urls\": {\n                    \"type\": \"string\",\n                    \"description\": \"List of URLs to extract content from\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include a list of images extracted from the urls in the response\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Depth of extraction - 'basic' or 'advanced', if urls are linkedin use 'advanced' or if explicitly told to use advanced\"\n                },\n                \"timeout\": {\n                    \"type\": \"number\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"minimum\": 0,\n                    \"maximum\": 60,\n                    \"default\": None,\n                    \"description\": \"Maximum time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_map\",\n        \"description\": \"A powerful web mapping tool that creates a structured map of website URLs, allowing you to discover and analyze site structure, content organization, and navigation paths. Perfect for site audits, content discovery, and understanding website architecture.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the mapping\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the mapping. Defines how far from the base URL the crawler can explore\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude URLs with specific path patterns (e.g., /admin/.*).\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude specific domains or subdomains\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_map\",\n        \"description\": \"A powerful web mapping tool that creates a structured map of website URLs, allowing you to discover and analyze site structure, content organization, and navigation paths. Perfect for site audits, content discovery, and understanding website architecture.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the mapping\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the mapping. Defines how far from the base URL the crawler can explore\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude URLs with specific path patterns (e.g., /admin/.*).\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude specific domains or subdomains\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_crawl\",\n        \"description\": \"A powerful web crawler that initiates a structured web crawl starting from a specified base URL. The crawler expands from that point like a tree, following internal links across pages. You can control how deep and wide it goes, and guide it to focus on specific sections of the site.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the crawl\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the crawl. Defines how far from the base URL the crawler can explore.\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude paths (e.g., /private/.*, /admin/.*)\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude domains/subdomains (e.g., ^private\\\\.example\\\\.com$)\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include images discovered during the crawl\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
    - {"language":"text","code":"tools = [\n    {\n        \"type\": \"function\",\n        \"name\": \"tavily_crawl\",\n        \"description\": \"A powerful web crawler that initiates a structured web crawl starting from a specified base URL. The crawler expands from that point like a tree, following internal links across pages. You can control how deep and wide it goes, and guide it to focus on specific sections of the site.\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"additionalProperties\": False,\n            \"required\": [\"url\"],\n            \"properties\": {\n                \"url\": {\n                    \"type\": \"string\",\n                    \"description\": \"The root URL to begin the crawl\"\n                },\n                \"instructions\": {\n                    \"type\": \"string\",\n                    \"description\": \"Natural language instructions for the crawler\"\n                },\n                \"max_depth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"maximum\": 5,\n                    \"default\": 1,\n                    \"description\": \"Max depth of the crawl. Defines how far from the base URL the crawler can explore.\"\n                },\n                \"max_breadth\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 20,\n                    \"description\": \"Max number of links to follow per level of the tree (i.e., per page)\"\n                },\n                \"limit\": {\n                    \"type\": \"integer\",\n                    \"minimum\": 1,\n                    \"default\": 50,\n                    \"description\": \"Total number of links the crawler will process before stopping\"\n                },\n                \"select_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)\"\n                },\n                \"select_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\\\.example\\\\.com$)\"\n                },\n                \"exclude_paths\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude paths (e.g., /private/.*, /admin/.*)\"\n                },\n                \"exclude_domains\": {\n                    \"type\": \"array\",\n                    \"items\": {\"type\": \"string\"},\n                    \"description\": \"Regex patterns to exclude domains/subdomains (e.g., ^private\\\\.example\\\\.com$)\"\n                },\n                \"allow_external\": {\n                    \"type\": \"boolean\",\n                    \"default\": True,\n                    \"description\": \"Whether to allow following links that go to external domains\"\n                },\n                \"include_images\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Include images discovered during the crawl\"\n                },\n                \"extract_depth\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"basic\", \"advanced\"],\n                    \"default\": \"basic\",\n                    \"description\": \"Advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency\"\n                },\n                \"format\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"markdown\", \"text\"],\n                    \"default\": \"markdown\",\n                    \"description\": \"The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\"\n                },\n                \"include_favicon\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include the favicon URL for each result\"\n                },\n                \"include_usage\": {\n                    \"type\": \"boolean\",\n                    \"default\": False,\n                    \"description\": \"Whether to include credit usage information in the response\"\n                }\n            }\n        }\n    }\n]"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"OpenAI_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"OpenAI_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"OpenAI_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"OpenAI_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/8eed9f5a-5e6b-45e6-9868-0af340d198d0/Dark_Tavily_Symbol.png","localPath":"OpenAI_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":"tavily-logo"}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"OpenAI_-_Tavily_Docs/image_6.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"OpenAI_-_Tavily_Docs/image_7.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"OpenAI_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"OpenAI_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"OpenAI_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"OpenAI_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"OpenAI_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"OpenAI_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"OpenAI_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"OpenAI_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"OpenAI_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"OpenAI_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"OpenAI_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"OpenAI_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"OpenAI_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"OpenAI_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"OpenAI_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"OpenAI_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"OpenAI_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"OpenAI_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"OpenAI_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"OpenAI_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"OpenAI_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"OpenAI_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"OpenAI_-_Tavily_Docs/svg_33.png","width":16,"height":16}
    - {"type":"svg","index":34,"filename":"OpenAI_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"OpenAI_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"OpenAI_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"OpenAI_-_Tavily_Docs/svg_37.png","width":16,"height":16}
    - {"type":"svg","index":38,"filename":"OpenAI_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"OpenAI_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"OpenAI_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"OpenAI_-_Tavily_Docs/svg_41.png","width":12,"height":12}
    - {"type":"svg","index":42,"filename":"OpenAI_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"OpenAI_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"OpenAI_-_Tavily_Docs/svg_44.png","width":14,"height":12}
    - {"type":"svg","index":45,"filename":"OpenAI_-_Tavily_Docs/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"OpenAI_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"OpenAI_-_Tavily_Docs/svg_47.png","width":14,"height":12}
    - {"type":"svg","index":48,"filename":"OpenAI_-_Tavily_Docs/svg_48.png","width":16,"height":16}
    - {"type":"svg","index":49,"filename":"OpenAI_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"OpenAI_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"OpenAI_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"OpenAI_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"OpenAI_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":54,"filename":"OpenAI_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"OpenAI_-_Tavily_Docs/svg_55.png","width":16,"height":16}
    - {"type":"svg","index":56,"filename":"OpenAI_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"OpenAI_-_Tavily_Docs/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"OpenAI_-_Tavily_Docs/svg_58.png","width":16,"height":16}
    - {"type":"svg","index":59,"filename":"OpenAI_-_Tavily_Docs/svg_59.png","width":16,"height":16}
    - {"type":"svg","index":60,"filename":"OpenAI_-_Tavily_Docs/svg_60.png","width":16,"height":16}
    - {"type":"svg","index":61,"filename":"OpenAI_-_Tavily_Docs/svg_61.png","width":16,"height":16}
    - {"type":"svg","index":62,"filename":"OpenAI_-_Tavily_Docs/svg_62.png","width":12,"height":12}
    - {"type":"svg","index":63,"filename":"OpenAI_-_Tavily_Docs/svg_63.png","width":16,"height":16}
    - {"type":"svg","index":64,"filename":"OpenAI_-_Tavily_Docs/svg_64.png","width":16,"height":16}
    - {"type":"svg","index":65,"filename":"OpenAI_-_Tavily_Docs/svg_65.png","width":14,"height":12}
    - {"type":"svg","index":66,"filename":"OpenAI_-_Tavily_Docs/svg_66.png","width":16,"height":16}
    - {"type":"svg","index":67,"filename":"OpenAI_-_Tavily_Docs/svg_67.png","width":16,"height":16}
    - {"type":"svg","index":68,"filename":"OpenAI_-_Tavily_Docs/svg_68.png","width":14,"height":12}
    - {"type":"svg","index":69,"filename":"OpenAI_-_Tavily_Docs/svg_69.png","width":16,"height":16}
    - {"type":"svg","index":70,"filename":"OpenAI_-_Tavily_Docs/svg_70.png","width":16,"height":16}
    - {"type":"svg","index":71,"filename":"OpenAI_-_Tavily_Docs/svg_71.png","width":16,"height":16}
    - {"type":"svg","index":72,"filename":"OpenAI_-_Tavily_Docs/svg_72.png","width":16,"height":16}
    - {"type":"svg","index":73,"filename":"OpenAI_-_Tavily_Docs/svg_73.png","width":16,"height":16}
    - {"type":"svg","index":74,"filename":"OpenAI_-_Tavily_Docs/svg_74.png","width":16,"height":16}
    - {"type":"svg","index":75,"filename":"OpenAI_-_Tavily_Docs/svg_75.png","width":16,"height":16}
    - {"type":"svg","index":76,"filename":"OpenAI_-_Tavily_Docs/svg_76.png","width":16,"height":16}
    - {"type":"svg","index":77,"filename":"OpenAI_-_Tavily_Docs/svg_77.png","width":16,"height":16}
    - {"type":"svg","index":78,"filename":"OpenAI_-_Tavily_Docs/svg_78.png","width":16,"height":16}
    - {"type":"svg","index":79,"filename":"OpenAI_-_Tavily_Docs/svg_79.png","width":12,"height":12}
    - {"type":"svg","index":80,"filename":"OpenAI_-_Tavily_Docs/svg_80.png","width":16,"height":16}
    - {"type":"svg","index":81,"filename":"OpenAI_-_Tavily_Docs/svg_81.png","width":16,"height":16}
    - {"type":"svg","index":82,"filename":"OpenAI_-_Tavily_Docs/svg_82.png","width":14,"height":12}
    - {"type":"svg","index":83,"filename":"OpenAI_-_Tavily_Docs/svg_83.png","width":12,"height":12}
    - {"type":"svg","index":84,"filename":"OpenAI_-_Tavily_Docs/svg_84.png","width":16,"height":16}
    - {"type":"svg","index":85,"filename":"OpenAI_-_Tavily_Docs/svg_85.png","width":16,"height":16}
    - {"type":"svg","index":86,"filename":"OpenAI_-_Tavily_Docs/svg_86.png","width":12,"height":12}
    - {"type":"svg","index":87,"filename":"OpenAI_-_Tavily_Docs/svg_87.png","width":16,"height":16}
    - {"type":"svg","index":88,"filename":"OpenAI_-_Tavily_Docs/svg_88.png","width":16,"height":16}
    - {"type":"svg","index":89,"filename":"OpenAI_-_Tavily_Docs/svg_89.png","width":12,"height":12}
    - {"type":"svg","index":90,"filename":"OpenAI_-_Tavily_Docs/svg_90.png","width":16,"height":16}
    - {"type":"svg","index":91,"filename":"OpenAI_-_Tavily_Docs/svg_91.png","width":16,"height":16}
    - {"type":"svg","index":92,"filename":"OpenAI_-_Tavily_Docs/svg_92.png","width":12,"height":12}
    - {"type":"svg","index":93,"filename":"OpenAI_-_Tavily_Docs/svg_93.png","width":16,"height":16}
    - {"type":"svg","index":94,"filename":"OpenAI_-_Tavily_Docs/svg_94.png","width":16,"height":16}
    - {"type":"svg","index":95,"filename":"OpenAI_-_Tavily_Docs/svg_95.png","width":14,"height":14}
    - {"type":"svg","index":96,"filename":"OpenAI_-_Tavily_Docs/svg_96.png","width":14,"height":14}
    - {"type":"svg","index":97,"filename":"OpenAI_-_Tavily_Docs/svg_97.png","width":14,"height":14}
    - {"type":"svg","index":102,"filename":"OpenAI_-_Tavily_Docs/svg_102.png","width":20,"height":20}
    - {"type":"svg","index":103,"filename":"OpenAI_-_Tavily_Docs/svg_103.png","width":20,"height":20}
    - {"type":"svg","index":104,"filename":"OpenAI_-_Tavily_Docs/svg_104.png","width":20,"height":20}
    - {"type":"svg","index":105,"filename":"OpenAI_-_Tavily_Docs/svg_105.png","width":20,"height":20}
    - {"type":"svg","index":106,"filename":"OpenAI_-_Tavily_Docs/svg_106.png","width":49,"height":14}
    - {"type":"svg","index":107,"filename":"OpenAI_-_Tavily_Docs/svg_107.png","width":16,"height":16}
    - {"type":"svg","index":108,"filename":"OpenAI_-_Tavily_Docs/svg_108.png","width":16,"height":16}
    - {"type":"svg","index":109,"filename":"OpenAI_-_Tavily_Docs/svg_109.png","width":16,"height":16}
    - {"type":"svg","index":119,"filename":"OpenAI_-_Tavily_Docs/svg_119.png","width":16,"height":16}
    - {"type":"svg","index":120,"filename":"OpenAI_-_Tavily_Docs/svg_120.png","width":14,"height":14}
    - {"type":"svg","index":121,"filename":"OpenAI_-_Tavily_Docs/svg_121.png","width":16,"height":16}
    - {"type":"svg","index":122,"filename":"OpenAI_-_Tavily_Docs/svg_122.png","width":12,"height":12}
    - {"type":"svg","index":123,"filename":"OpenAI_-_Tavily_Docs/svg_123.png","width":14,"height":14}
    - {"type":"svg","index":124,"filename":"OpenAI_-_Tavily_Docs/svg_124.png","width":16,"height":16}
    - {"type":"svg","index":125,"filename":"OpenAI_-_Tavily_Docs/svg_125.png","width":12,"height":12}
    - {"type":"svg","index":126,"filename":"OpenAI_-_Tavily_Docs/svg_126.png","width":14,"height":14}
    - {"type":"svg","index":127,"filename":"OpenAI_-_Tavily_Docs/svg_127.png","width":16,"height":16}
    - {"type":"svg","index":128,"filename":"OpenAI_-_Tavily_Docs/svg_128.png","width":12,"height":12}
    - {"type":"svg","index":129,"filename":"OpenAI_-_Tavily_Docs/svg_129.png","width":14,"height":14}
  chartData: []
  blockquotes:
    - "Note: You can enhance the function by adding more parameters like topic=\"news\", include_domains=[\"example.com\"], time_range=\"week\", etc. to customize your search results."
    - "You can set auto_parameters=True to have Tavily automatically configure search parameters based on the content and intent of your query. You can still set other parameters manually, and any explicit values you provide will override the automatic ones."
    - "Note: When using these schemas, you can customize which parameters are exposed to the model based on your specific use case. For example, if you are building a finance application, you might set topic: \"finance\" for all queries without exposing the topic parameter. This way, the LLM can focus on deciding other parameters, such as time_range, country, and so on, based on the user’s request. Feel free to modify these schemas as needed and only pass the parameters that are relevant to your application."
    - "API Format: The schemas below are for OpenAI Responses API. For Chat Completions API, wrap the parameters in a \"function\" object: {\"type\": \"function\", \"function\": {\"name\": \"...\", \"parameters\": {...}}}."
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

# OpenAI

## 源URL

https://docs.tavily.com/documentation/integrations/openai

## 描述

Integrate Tavily with OpenAI to enhance your AI applications with real-time web search capabilities.

## 内容

### Introduction

### Prerequisites

- An OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
- A Tavily API key from [Tavily Dashboard](https://app.tavily.com/sign-in)

### Installation

```text
pip install openai tavily-python
```

### Setup

```text
import os

# Set your API keys
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["TAVILY_API_KEY"] = "your-tavily-api-key"
```

### Using Tavily with OpenAI agents SDK

```text
pip install -U openai-agents
```

```text
import os
import asyncio
from agents import Agent, Runner, function_tool
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
```

```text
@function_tool
def tavily_search(query: str) -> str:
    """
    Perform a web search using Tavily and return a summarized result.
    """
    response = tavily_client.search(query,search_depth='advanced',max_results='5')
    results = response.get("results", [])
    return results or "No results found."
```

> Note: You can enhance the function by adding more parameters like topic="news", include_domains=["example.com"], time_range="week", etc. to customize your search results.

> You can set auto_parameters=True to have Tavily automatically configure search parameters based on the content and intent of your query. You can still set other parameters manually, and any explicit values you provide will override the automatic ones.

```text
async def main():
    agent = Agent(
        name="Web Research Agent",
        instructions="Use tavily_search when you need up-to-date info.",
        tools=[tavily_search],
    )
    out = await Runner.run(agent, "Latest developments about quantum computing from 2025")
    print(out.final_output)
```

```text
asyncio.run(main())
```

### Using Tavily with OpenAI Chat Completions API function calling

```text
import os
import json
from tavily import TavilyClient
from openai import OpenAI

# Load your API keys from environment variables
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

#### Function definition

```text
def tavily_search(**kwargs):
    # Pass ALL supported kwargs straight to Tavily
    results = tavily_client.search(**kwargs)
    return results
```

```text
# --- define tools ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": "Search the web with Tavily for up-to-date information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"},
                    "max_results": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
    }
]
```

```text
# --- conversation ---
messages = [
    {"role": "system", "content": "You are a helpful assistant that uses Tavily search when needed."},
    {"role": "user", "content": "What are the top trends in 2025 about AI agents?"}
]
```

```text
#Ask the model; let it decide whether to call the tool
response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
)
```

```text
assistant_msg = response.choices[0].message
 # keep the assistant msg that requested tool(s)
messages.append(assistant_msg)
```

```text
if getattr(assistant_msg, "tool_calls", None):
    for tc in assistant_msg.tool_calls:
        args = tc.function.arguments
        if isinstance(args, str):
            args = json.loads(args)
        elif not isinstance(args, dict):
            args = json.loads(str(args))

        if tc.function.name == "tavily_search":
            # forward ALL args
            results = tavily_search(**args)

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "name": "tavily_search",
                "content": json.dumps(results),
            })
else:
    print("\nNo tool call requested by the model.")
```

```text
# Ask the model again for the final grounded answer
final = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

final_msg = final.choices[0].message
print("\nFINAL ANSWER:\n", final_msg.content or "(no content)")
```

### Using Tavily with OpenAI Responses API function calling

```text
import os
import json
from tavily import TavilyClient
from openai import OpenAI

# --- setup ---
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

#### Function definition

```text
# --- Function that will be called when AI requests a search ---
def tavily_search(**kwargs):
    """
    Execute a Tavily web search with the given parameters.
    This function is called by the AI when it needs to search the web.
    """
    results = tavily_client.search(**kwargs)
    return results
```

```text
# Define the tool for Tavily web search
# This tells the AI what function it can call and what parameters it needs
tools = [{
    "type": "function",
    "name": "tavily_search",
    "description": "Search the web using Tavily. Provide relevant links in your answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for Tavily."
            },
            "max_results": {
                "type": "integer",
                "description": "Max number of results to return",
                "default": 5
            }
        },
        "required": ["query", "max_results"], 
        "additionalProperties": False
    },
    "strict": True
}]
```

```text
# --- Step 1: Create initial conversation ---
# This sets up the conversation context for the AI
input_list = [
    {"role": "system", "content": "You are a helpful assistant that uses Tavily search when needed."},
    {"role": "user", "content": "What are the top trends in 2025 about AI agents?"}
]

# --- Step 2: First API call - AI decides to search ---
# The AI will analyze the user's question and decide if it needs to search the web
response = openai_client.responses.create(
    model="gpt-4o-mini",
    tools=tools,
    input=input_list,
)

# --- Step 3: Process the AI's response ---
# Add the AI's response (including any function calls) to our conversation
input_list += response.output
```

```text
# --- Step 4: Execute any function calls the AI made ---
for item in response.output:
    if item.type == "function_call":
        if item.name == "tavily_search":
            # Parse the arguments the AI provided for the search
            parsed_args = json.loads(item.arguments)
            
            # Execute the actual Tavily search
            results = tavily_search(**parsed_args)
            
            # Add the search results back to the conversation
            # This tells the AI what it found when it searched
            function_output = {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "results": results
                })
            }
            input_list.append(function_output)
```

```text
# --- Step 5: Second API call - AI provides final answer ---
# Now the AI has the search results and can provide an informed response
response = openai_client.responses.create(
    model="gpt-4o-mini",
    instructions="Based on the Tavily search results provided, give me a comprehensive summary with citations.",
    input=input_list,
)

# --- Display the final result ---
print("AI Response:")
print(response.output_text)
```

### Tavily endpoints schema for OpenAI Responses API tool definition

> Note: When using these schemas, you can customize which parameters are exposed to the model based on your specific use case. For example, if you are building a finance application, you might set topic: "finance" for all queries without exposing the topic parameter. This way, the LLM can focus on deciding other parameters, such as time_range, country, and so on, based on the user’s request. Feel free to modify these schemas as needed and only pass the parameters that are relevant to your application.

> API Format: The schemas below are for OpenAI Responses API. For Chat Completions API, wrap the parameters in a "function" object: {"type": "function", "function": {"name": "...", "parameters": {...}}}.

## 图片

![light logo](OpenAI_-_Tavily_Docs/image_1.svg)

![dark logo](OpenAI_-_Tavily_Docs/image_2.svg)

![light logo](OpenAI_-_Tavily_Docs/image_3.svg)

![dark logo](OpenAI_-_Tavily_Docs/image_4.svg)

![tavily-logo](OpenAI_-_Tavily_Docs/image_5.png)

![tavily-logo](OpenAI_-_Tavily_Docs/image_6.png)

![Powered by Onetrust](OpenAI_-_Tavily_Docs/image_7.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](OpenAI_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](OpenAI_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](OpenAI_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](OpenAI_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](OpenAI_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](OpenAI_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](OpenAI_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](OpenAI_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](OpenAI_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](OpenAI_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](OpenAI_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](OpenAI_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](OpenAI_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](OpenAI_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](OpenAI_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](OpenAI_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](OpenAI_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](OpenAI_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](OpenAI_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](OpenAI_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](OpenAI_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](OpenAI_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](OpenAI_-_Tavily_Docs/svg_33.png)
*尺寸: 16x16px*

![SVG图表 34](OpenAI_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](OpenAI_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](OpenAI_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](OpenAI_-_Tavily_Docs/svg_37.png)
*尺寸: 16x16px*

![SVG图表 38](OpenAI_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](OpenAI_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](OpenAI_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](OpenAI_-_Tavily_Docs/svg_41.png)
*尺寸: 12x12px*

![SVG图表 42](OpenAI_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](OpenAI_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](OpenAI_-_Tavily_Docs/svg_44.png)
*尺寸: 14x12px*

![SVG图表 45](OpenAI_-_Tavily_Docs/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](OpenAI_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](OpenAI_-_Tavily_Docs/svg_47.png)
*尺寸: 14x12px*

![SVG图表 48](OpenAI_-_Tavily_Docs/svg_48.png)
*尺寸: 16x16px*

![SVG图表 49](OpenAI_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](OpenAI_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](OpenAI_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 52](OpenAI_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](OpenAI_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 54](OpenAI_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](OpenAI_-_Tavily_Docs/svg_55.png)
*尺寸: 16x16px*

![SVG图表 56](OpenAI_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](OpenAI_-_Tavily_Docs/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](OpenAI_-_Tavily_Docs/svg_58.png)
*尺寸: 16x16px*

![SVG图表 59](OpenAI_-_Tavily_Docs/svg_59.png)
*尺寸: 16x16px*

![SVG图表 60](OpenAI_-_Tavily_Docs/svg_60.png)
*尺寸: 16x16px*

![SVG图表 61](OpenAI_-_Tavily_Docs/svg_61.png)
*尺寸: 16x16px*

![SVG图表 62](OpenAI_-_Tavily_Docs/svg_62.png)
*尺寸: 12x12px*

![SVG图表 63](OpenAI_-_Tavily_Docs/svg_63.png)
*尺寸: 16x16px*

![SVG图表 64](OpenAI_-_Tavily_Docs/svg_64.png)
*尺寸: 16x16px*

![SVG图表 65](OpenAI_-_Tavily_Docs/svg_65.png)
*尺寸: 14x12px*

![SVG图表 66](OpenAI_-_Tavily_Docs/svg_66.png)
*尺寸: 16x16px*

![SVG图表 67](OpenAI_-_Tavily_Docs/svg_67.png)
*尺寸: 16x16px*

![SVG图表 68](OpenAI_-_Tavily_Docs/svg_68.png)
*尺寸: 14x12px*

![SVG图表 69](OpenAI_-_Tavily_Docs/svg_69.png)
*尺寸: 16x16px*

![SVG图表 70](OpenAI_-_Tavily_Docs/svg_70.png)
*尺寸: 16x16px*

![SVG图表 71](OpenAI_-_Tavily_Docs/svg_71.png)
*尺寸: 16x16px*

![SVG图表 72](OpenAI_-_Tavily_Docs/svg_72.png)
*尺寸: 16x16px*

![SVG图表 73](OpenAI_-_Tavily_Docs/svg_73.png)
*尺寸: 16x16px*

![SVG图表 74](OpenAI_-_Tavily_Docs/svg_74.png)
*尺寸: 16x16px*

![SVG图表 75](OpenAI_-_Tavily_Docs/svg_75.png)
*尺寸: 16x16px*

![SVG图表 76](OpenAI_-_Tavily_Docs/svg_76.png)
*尺寸: 16x16px*

![SVG图表 77](OpenAI_-_Tavily_Docs/svg_77.png)
*尺寸: 16x16px*

![SVG图表 78](OpenAI_-_Tavily_Docs/svg_78.png)
*尺寸: 16x16px*

![SVG图表 79](OpenAI_-_Tavily_Docs/svg_79.png)
*尺寸: 12x12px*

![SVG图表 80](OpenAI_-_Tavily_Docs/svg_80.png)
*尺寸: 16x16px*

![SVG图表 81](OpenAI_-_Tavily_Docs/svg_81.png)
*尺寸: 16x16px*

![SVG图表 82](OpenAI_-_Tavily_Docs/svg_82.png)
*尺寸: 14x12px*

![SVG图表 83](OpenAI_-_Tavily_Docs/svg_83.png)
*尺寸: 12x12px*

![SVG图表 84](OpenAI_-_Tavily_Docs/svg_84.png)
*尺寸: 16x16px*

![SVG图表 85](OpenAI_-_Tavily_Docs/svg_85.png)
*尺寸: 16x16px*

![SVG图表 86](OpenAI_-_Tavily_Docs/svg_86.png)
*尺寸: 12x12px*

![SVG图表 87](OpenAI_-_Tavily_Docs/svg_87.png)
*尺寸: 16x16px*

![SVG图表 88](OpenAI_-_Tavily_Docs/svg_88.png)
*尺寸: 16x16px*

![SVG图表 89](OpenAI_-_Tavily_Docs/svg_89.png)
*尺寸: 12x12px*

![SVG图表 90](OpenAI_-_Tavily_Docs/svg_90.png)
*尺寸: 16x16px*

![SVG图表 91](OpenAI_-_Tavily_Docs/svg_91.png)
*尺寸: 16x16px*

![SVG图表 92](OpenAI_-_Tavily_Docs/svg_92.png)
*尺寸: 12x12px*

![SVG图表 93](OpenAI_-_Tavily_Docs/svg_93.png)
*尺寸: 16x16px*

![SVG图表 94](OpenAI_-_Tavily_Docs/svg_94.png)
*尺寸: 16x16px*

![SVG图表 95](OpenAI_-_Tavily_Docs/svg_95.png)
*尺寸: 14x14px*

![SVG图表 96](OpenAI_-_Tavily_Docs/svg_96.png)
*尺寸: 14x14px*

![SVG图表 97](OpenAI_-_Tavily_Docs/svg_97.png)
*尺寸: 14x14px*

![SVG图表 102](OpenAI_-_Tavily_Docs/svg_102.png)
*尺寸: 20x20px*

![SVG图表 103](OpenAI_-_Tavily_Docs/svg_103.png)
*尺寸: 20x20px*

![SVG图表 104](OpenAI_-_Tavily_Docs/svg_104.png)
*尺寸: 20x20px*

![SVG图表 105](OpenAI_-_Tavily_Docs/svg_105.png)
*尺寸: 20x20px*

![SVG图表 106](OpenAI_-_Tavily_Docs/svg_106.png)
*尺寸: 49x14px*

![SVG图表 107](OpenAI_-_Tavily_Docs/svg_107.png)
*尺寸: 16x16px*

![SVG图表 108](OpenAI_-_Tavily_Docs/svg_108.png)
*尺寸: 16x16px*

![SVG图表 109](OpenAI_-_Tavily_Docs/svg_109.png)
*尺寸: 16x16px*

![SVG图表 119](OpenAI_-_Tavily_Docs/svg_119.png)
*尺寸: 16x16px*

![SVG图表 120](OpenAI_-_Tavily_Docs/svg_120.png)
*尺寸: 14x14px*

![SVG图表 121](OpenAI_-_Tavily_Docs/svg_121.png)
*尺寸: 16x16px*

![SVG图表 122](OpenAI_-_Tavily_Docs/svg_122.png)
*尺寸: 12x12px*

![SVG图表 123](OpenAI_-_Tavily_Docs/svg_123.png)
*尺寸: 14x14px*

![SVG图表 124](OpenAI_-_Tavily_Docs/svg_124.png)
*尺寸: 16x16px*

![SVG图表 125](OpenAI_-_Tavily_Docs/svg_125.png)
*尺寸: 12x12px*

![SVG图表 126](OpenAI_-_Tavily_Docs/svg_126.png)
*尺寸: 14x14px*

![SVG图表 127](OpenAI_-_Tavily_Docs/svg_127.png)
*尺寸: 16x16px*

![SVG图表 128](OpenAI_-_Tavily_Docs/svg_128.png)
*尺寸: 12x12px*

![SVG图表 129](OpenAI_-_Tavily_Docs/svg_129.png)
*尺寸: 14x14px*
