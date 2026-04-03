---
id: "url-3e14b9da"
type: "website"
title: "Tavily MCP Server"
url: "https://docs.tavily.com/documentation/mcp"
description: "Tavily MCP Server allows you to use the Tavily API in your MCP clients."
source: ""
tags: []
crawl_time: "2026-03-18T04:12:48.524Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Tavily MCP Server"}
    - {"level":2,"text":"GitHub"}
    - {"level":2,"text":"NPM"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/mcp#remote-mcp-server)Remote MCP Server"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#connect-to-cursor)Connect to Cursor"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#connect-to-claude-desktop)Connect to Claude Desktop"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#openai)OpenAI"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#connect-to-claude-code)Connect to Claude Code"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#clients-that-don%E2%80%99t-support-remote-mcps)Clients that don’t support remote MCPs"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#oauth-authentication)OAuth Authentication"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#default-parameters)Default Parameters"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/mcp#local-installation)Local Installation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#prerequisites)Prerequisites"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#configuring-mcp-clients)Configuring MCP Clients"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/mcp#default-parameters-2)Default Parameters"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/mcp#usage-examples)Usage Examples"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/mcp#troubleshooting)Troubleshooting"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/mcp#acknowledgments)Acknowledgments"}
    - {"level":2,"text":"Model Context Protocol"}
    - {"level":2,"text":"Anthropic"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"list","listType":"ul","items":["Overview","Features"]}
    - {"type":"list","listType":"ul","items":["Seamless interaction with the tavily-search and tavily-extract tools","Real-time web search capabilities through the tavily-search tool","Intelligent data extraction from web pages via the tavily-extract tool"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/mcp#remote-mcp-server)Remote MCP Server"}
    - {"type":"codeblock","language":"","content":"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#connect-to-cursor)Connect to Cursor"}
    - {"type":"codeblock","language":"","content":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"command\": \"npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\",\n      \"env\": {}\n    }\n  }\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#connect-to-claude-desktop)Connect to Claude Desktop"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#openai)OpenAI"}
    - {"type":"list","listType":"ul","items":["You first need to export your OPENAI_API_KEY","You must also add your Tavily API-key to `<your-api-key>`, you can get a Tavily API key [here](https://www.tavily.com/)"]}
    - {"type":"codeblock","language":"","content":"from openai import OpenAI\n\nclient = OpenAI()\n\nresp = client.responses.create(\n    model=\"gpt-4.1\",\n    tools=[\n        {\n            \"type\": \"mcp\",\n            \"server_label\": \"tavily\",\n            \"server_url\": \"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\",\n            \"require_approval\": \"never\",\n            ## Optional default parameters:\n            \"headers\": {\n                \"DEFAULT_PARAMETERS\": json.dumps({\n                    \"include_favicon\": True,\n                    \"include_images\": False,\n                    \"include_raw_content\": False,\n                }),\n            },\n        },\n    ],\n    input=\"Do you have access to the tavily mcp server?\",\n)\n\nprint(resp.output_text)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#connect-to-claude-code)Connect to Claude Code"}
    - {"type":"codeblock","language":"","content":"claude mcp add tavily-remote-mcp --transport http https://mcp.tavily.com/mcp/"}
    - {"type":"codeblock","language":"","content":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"type\": \"http\",\n      \"url\": \"https://mcp.tavily.com/mcp/\"\n    }\n  }\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#clients-that-don%E2%80%99t-support-remote-mcps)Clients that don’t support remote MCPs"}
    - {"type":"codeblock","language":"","content":"{\n    \"tavily-remote\": {\n      \"command\": \"npx\",\n      \"args\": [\n        \"-y\",\n        \"mcp-remote\",\n        \"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\"\n      ]\n    }\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#oauth-authentication)OAuth Authentication"}
    - {"type":"list","listType":"ul","items":["**Personal account**: If you have a key named `mcp_auth_default` in your personal account, it will be used for all OAuth-authenticated requests.","**Team account**: If your team has a key named `mcp_auth_default`, it will be used for all OAuth-authenticated requests.","**Both set**: If both your personal account and your team have a key named `mcp_auth_default`, the **personal key takes priority**.","**Neither set**: If no `mcp_auth_default` key exists, the `default` key in your personal account will be used. If no `default` key is set, the first available key will be used."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#default-parameters)Default Parameters"}
    - {"type":"codeblock","language":"","content":"{\"include_images\":true, \"search_depth\": \"advanced\", \"max_results\": 10}"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/mcp#local-installation)Local Installation"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#prerequisites)Prerequisites"}
    - {"type":"codeblock","language":"","content":"npx -y tavily-mcp@0.1.3"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#configuring-mcp-clients)Configuring MCP Clients"}
    - {"type":"list","listType":"ul","items":["Cursor","Claude Desktop"]}
    - {"type":"blockquote","content":"Note: Requires Cursor version 0.45.6 or higher"}
    - {"type":"list","listType":"ol","items":["Open Cursor Settings","Navigate to Features > MCP Servers","Click on the ”+ Add New MCP Server” button","Fill out the following information:\n\n**Name**: Enter a nickname for the server (e.g., “tavily-mcp”)\n**Type**: Select “command” as the type\n**Command**: Enter the command to run the server:\nCopyAsk AI`env TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3`\nReplace `tvly-YOUR_API_KEY` with your Tavily API key from [app.tavily.com/home](https://app.tavily.com/home)","**Name**: Enter a nickname for the server (e.g., “tavily-mcp”)","**Type**: Select “command” as the type","**Command**: Enter the command to run the server:\nCopyAsk AI`env TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3`\nReplace `tvly-YOUR_API_KEY` with your Tavily API key from [app.tavily.com/home](https://app.tavily.com/home)"]}
    - {"type":"codeblock","language":"","content":"# Create the config file if it doesn't exist\ntouch \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\"\n\n# Opens the config file in TextEdit\nopen -e \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\"\n\n# Alternative method using Visual Studio Code\ncode \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\""}
    - {"type":"codeblock","language":"","content":"{\n  \"mcpServers\": {\n    \"tavily-mcp\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"tavily-mcp@0.1.2\"],\n      \"env\": {\n        \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY-here\"\n      }\n    }\n  }\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/mcp#default-parameters-2)Default Parameters"}
    - {"type":"codeblock","language":"","content":"{\n  \"mcpServers\": {\n    \"tavily-mcp\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"tavily-mcp@latest\"],\n      \"env\": {\n        \"TAVILY_API_KEY\": \"your-api-key-here\",\n        \"DEFAULT_PARAMETERS\": \"{\\\"include_images\\\": true, \\\"max_results\\\": 15, \\\"search_depth\\\": \\\"advanced\\\"}\"\n      }\n    }\n  }\n}"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/mcp#usage-examples)Usage Examples"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/mcp#troubleshooting)Troubleshooting"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/mcp#acknowledgments)Acknowledgments"}
  paragraphs:
    - "Using MCP Inspector"
    - "Using Other MCP Clients"
    - "Required Tools"
    - "Git Installation (Optional)"
    - "Tavily Search Examples"
    - "Tavily Extract Examples"
    - "Combined Usage"
    - "Server Not Found"
    - "NPX Issues"
    - "API Key Issues"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Remote MCP Server](https://docs.tavily.com/documentation/mcp#remote-mcp-server)","[Connect to Cursor](https://docs.tavily.com/documentation/mcp#connect-to-cursor)","[Connect to Claude Desktop](https://docs.tavily.com/documentation/mcp#connect-to-claude-desktop)","[OpenAI](https://docs.tavily.com/documentation/mcp#openai)","[Connect to Claude Code](https://docs.tavily.com/documentation/mcp#connect-to-claude-code)","[Clients that don’t support remote MCPs](https://docs.tavily.com/documentation/mcp#clients-that-don%E2%80%99t-support-remote-mcps)","[OAuth Authentication](https://docs.tavily.com/documentation/mcp#oauth-authentication)","[Default Parameters](https://docs.tavily.com/documentation/mcp#default-parameters)","[Local Installation](https://docs.tavily.com/documentation/mcp#local-installation)","[Prerequisites](https://docs.tavily.com/documentation/mcp#prerequisites)","[Configuring MCP Clients](https://docs.tavily.com/documentation/mcp#configuring-mcp-clients)","[Default Parameters](https://docs.tavily.com/documentation/mcp#default-parameters-2)","[Usage Examples](https://docs.tavily.com/documentation/mcp#usage-examples)","[Troubleshooting](https://docs.tavily.com/documentation/mcp#troubleshooting)","[Acknowledgments](https://docs.tavily.com/documentation/mcp#acknowledgments)"]}
    - {"type":"ul","items":["Overview","Features"]}
    - {"type":"ul","items":["Seamless interaction with the tavily-search and tavily-extract tools","Real-time web search capabilities through the tavily-search tool","Intelligent data extraction from web pages via the tavily-extract tool"]}
    - {"type":"ul","items":["You first need to export your OPENAI_API_KEY","You must also add your Tavily API-key to <your-api-key>, you can get a Tavily API key [here](https://www.tavily.com/)"]}
    - {"type":"ol","items":["Metadata discovery","Client registration","Preparing authorization","Request authorization and obtain the authorization code","Token request","Authentication complete"]}
    - {"type":"ul","items":["Personal account: If you have a key named mcp_auth_default in your personal account, it will be used for all OAuth-authenticated requests.","Team account: If your team has a key named mcp_auth_default, it will be used for all OAuth-authenticated requests.","Both set: If both your personal account and your team have a key named mcp_auth_default, the personal key takes priority.","Neither set: If no mcp_auth_default key exists, the default key in your personal account will be used. If no default key is set, the first available key will be used."]}
    - {"type":"ul","items":["[Tavily API key](https://app.tavily.com/home)\n\nIf you don’t have a Tavily API key, you can sign up for a free account [here](https://app.tavily.com/home)","If you don’t have a Tavily API key, you can sign up for a free account [here](https://app.tavily.com/home)","[Claude Desktop](https://claude.ai/download) or [Cursor](https://cursor.sh/)","[Node.js](https://nodejs.org/) (v20 or higher)\n\nYou can verify your Node.js installation by running:\nCopyAsk AInode --version","You can verify your Node.js installation by running:\nCopyAsk AInode --version"]}
    - {"type":"ul","items":["If you don’t have a Tavily API key, you can sign up for a free account [here](https://app.tavily.com/home)"]}
    - {"type":"ul","items":["You can verify your Node.js installation by running:\nCopyAsk AInode --version"]}
    - {"type":"ul","items":["On macOS: brew install git","On Linux:\n\nDebian/Ubuntu: sudo apt install git\nRedHat/CentOS: sudo yum install git","Debian/Ubuntu: sudo apt install git","RedHat/CentOS: sudo yum install git","On Windows: Download [Git for Windows](https://git-scm.com/download/win)"]}
    - {"type":"ul","items":["Debian/Ubuntu: sudo apt install git","RedHat/CentOS: sudo yum install git"]}
    - {"type":"ul","items":["Cursor","Claude Desktop"]}
    - {"type":"ol","items":["Open Cursor Settings","Navigate to Features > MCP Servers","Click on the ”+ Add New MCP Server” button","Fill out the following information:\n\nName: Enter a nickname for the server (e.g., “tavily-mcp”)\nType: Select “command” as the type\nCommand: Enter the command to run the server:\nCopyAsk AIenv TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3\n\nReplace tvly-YOUR_API_KEY with your Tavily API key from [app.tavily.com/home](https://app.tavily.com/home)","Name: Enter a nickname for the server (e.g., “tavily-mcp”)","Type: Select “command” as the type","Command: Enter the command to run the server:\nCopyAsk AIenv TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3\n\nReplace tvly-YOUR_API_KEY with your Tavily API key from [app.tavily.com/home](https://app.tavily.com/home)"]}
    - {"type":"ul","items":["Name: Enter a nickname for the server (e.g., “tavily-mcp”)","Type: Select “command” as the type","Command: Enter the command to run the server:\nCopyAsk AIenv TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3\n\nReplace tvly-YOUR_API_KEY with your Tavily API key from [app.tavily.com/home](https://app.tavily.com/home)"]}
    - {"type":"ol","items":["General Web Search:"]}
    - {"type":"ol","items":["News Search:"]}
    - {"type":"ol","items":["Domain-Specific Search:"]}
    - {"type":"ul","items":["Properly formatted with the tvly- prefix","Valid and active in your Tavily dashboard","Correctly configured in your environment variables"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>"}
    - {"language":"text","code":"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"command\": \"npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\",\n      \"env\": {}\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"command\": \"npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\",\n      \"env\": {}\n    }\n  }\n}"}
    - {"language":"text","code":"from openai import OpenAI\n\nclient = OpenAI()\n\nresp = client.responses.create(\n    model=\"gpt-4.1\",\n    tools=[\n        {\n            \"type\": \"mcp\",\n            \"server_label\": \"tavily\",\n            \"server_url\": \"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\",\n            \"require_approval\": \"never\",\n            ## Optional default parameters:\n            \"headers\": {\n                \"DEFAULT_PARAMETERS\": json.dumps({\n                    \"include_favicon\": True,\n                    \"include_images\": False,\n                    \"include_raw_content\": False,\n                }),\n            },\n        },\n    ],\n    input=\"Do you have access to the tavily mcp server?\",\n)\n\nprint(resp.output_text)"}
    - {"language":"text","code":"from openai import OpenAI\n\nclient = OpenAI()\n\nresp = client.responses.create(\n    model=\"gpt-4.1\",\n    tools=[\n        {\n            \"type\": \"mcp\",\n            \"server_label\": \"tavily\",\n            \"server_url\": \"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\",\n            \"require_approval\": \"never\",\n            ## Optional default parameters:\n            \"headers\": {\n                \"DEFAULT_PARAMETERS\": json.dumps({\n                    \"include_favicon\": True,\n                    \"include_images\": False,\n                    \"include_raw_content\": False,\n                }),\n            },\n        },\n    ],\n    input=\"Do you have access to the tavily mcp server?\",\n)\n\nprint(resp.output_text)"}
    - {"language":"text","code":"claude mcp add tavily-remote-mcp --transport http https://mcp.tavily.com/mcp/"}
    - {"language":"text","code":"claude mcp add tavily-remote-mcp --transport http https://mcp.tavily.com/mcp/"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"type\": \"http\",\n      \"url\": \"https://mcp.tavily.com/mcp/\"\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"type\": \"http\",\n      \"url\": \"https://mcp.tavily.com/mcp/\"\n    }\n  }\n}"}
    - {"language":"json","code":"{\n    \"tavily-remote\": {\n      \"command\": \"npx\",\n      \"args\": [\n        \"-y\",\n        \"mcp-remote\",\n        \"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\"\n      ]\n    }\n}"}
    - {"language":"json","code":"{\n    \"tavily-remote\": {\n      \"command\": \"npx\",\n      \"args\": [\n        \"-y\",\n        \"mcp-remote\",\n        \"https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>\"\n      ]\n    }\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"command\": \"npx mcp-remote https://mcp.tavily.com/mcp\",\n      \"env\": {}\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-remote-mcp\": {\n      \"command\": \"npx mcp-remote https://mcp.tavily.com/mcp\",\n      \"env\": {}\n    }\n  }\n}"}
    - {"language":"text","code":"rm -rf ~/.mcp-auth"}
    - {"language":"text","code":"rm -rf ~/.mcp-auth"}
    - {"language":"json","code":"{\"include_images\":true, \"search_depth\": \"advanced\", \"max_results\": 10}"}
    - {"language":"json","code":"{\"include_images\":true, \"search_depth\": \"advanced\", \"max_results\": 10}"}
    - {"language":"text","code":"node --version"}
    - {"language":"text","code":"node --version"}
    - {"language":"text","code":"npx -y tavily-mcp@0.1.3"}
    - {"language":"text","code":"npx -y tavily-mcp@0.1.3"}
    - {"language":"text","code":"env TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3"}
    - {"language":"text","code":"env TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3"}
    - {"language":"text","code":"# Create the config file if it doesn't exist\ntouch \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\"\n\n# Opens the config file in TextEdit\nopen -e \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\"\n\n# Alternative method using Visual Studio Code\ncode \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\""}
    - {"language":"text","code":"# Create the config file if it doesn't exist\ntouch \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\"\n\n# Opens the config file in TextEdit\nopen -e \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\"\n\n# Alternative method using Visual Studio Code\ncode \"$HOME/Library/Application Support/Claude/claude_desktop_config.json\""}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-mcp\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"tavily-mcp@0.1.2\"],\n      \"env\": {\n        \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY-here\"\n      }\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-mcp\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"tavily-mcp@0.1.2\"],\n      \"env\": {\n        \"TAVILY_API_KEY\": \"tvly-YOUR_API_KEY-here\"\n      }\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-mcp\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"tavily-mcp@latest\"],\n      \"env\": {\n        \"TAVILY_API_KEY\": \"your-api-key-here\",\n        \"DEFAULT_PARAMETERS\": \"{\\\"include_images\\\": true, \\\"max_results\\\": 15, \\\"search_depth\\\": \\\"advanced\\\"}\"\n      }\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"tavily-mcp\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"tavily-mcp@latest\"],\n      \"env\": {\n        \"TAVILY_API_KEY\": \"your-api-key-here\",\n        \"DEFAULT_PARAMETERS\": \"{\\\"include_images\\\": true, \\\"max_results\\\": 15, \\\"search_depth\\\": \\\"advanced\\\"}\"\n      }\n    }\n  }\n}"}
    - {"language":"text","code":"Can you search for recent developments in quantum computing?"}
    - {"language":"text","code":"Can you search for recent developments in quantum computing?"}
    - {"language":"text","code":"Search for news articles about AI startups from the last 7 days."}
    - {"language":"text","code":"Search for news articles about AI startups from the last 7 days."}
    - {"language":"text","code":"Search for climate change research on nature.com and sciencedirect.com"}
    - {"language":"text","code":"Search for climate change research on nature.com and sciencedirect.com"}
    - {"language":"text","code":"Search for news articles about AI startups from the last 7 days and extract the main content from each article to generate a detailed report."}
    - {"language":"text","code":"Search for news articles about AI startups from the last 7 days and extract the main content from each article to generate a detailed report."}
    - {"language":"text","code":"npm --version\nnode --version"}
    - {"language":"text","code":"npm --version\nnode --version"}
    - {"language":"text","code":"which npx"}
    - {"language":"text","code":"which npx"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://img.shields.io/github/stars/tavily-ai/tavily-mcp?style=social","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_3.jpg","alt":"GitHub Repo stars","title":""}
    - {"src":"https://img.shields.io/npm/dt/tavily-mcp","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_4.jpg","alt":"npm","title":""}
    - {"src":"https://mintcdn.com/tavilyai/tgJqPSjqNVSkMFTO/images/mcp-demo.gif?s=387a3d560de94008f981b8896dcb25d2","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_5.gif","alt":"Tavily MCP Demo","title":""}
    - {"src":"https://cursor.com/deeplink/mcp-install-dark.svg","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_6.svg","alt":"Install MCP Server","title":""}
    - {"src":"https://mintcdn.com/tavilyai/tgJqPSjqNVSkMFTO/images/cursor-reference.png?fit=max&auto=format&n=tgJqPSjqNVSkMFTO&q=85&s=fb7da4e530057cf30d5e2fcf6de69f28","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_7.png","alt":"Cursor Interface Example","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_8.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_9.svg","alt":"dark logo","title":""}
    - {"src":"https://cursor.com/deeplink/mcp-install-dark.svg","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_10.svg","alt":"Install MCP Server","title":""}
    - {"src":"https://mintcdn.com/tavilyai/tgJqPSjqNVSkMFTO/images/mcp-demo.gif?s=387a3d560de94008f981b8896dcb25d2","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_11.gif","alt":"Tavily MCP Demo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/tgJqPSjqNVSkMFTO/images/cursor-reference.png?w=840&fit=max&auto=format&n=tgJqPSjqNVSkMFTO&q=85&s=db1b26d05d29b99cea759a0f067f9c34","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_12.png","alt":"Cursor Interface Example","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_13.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Tavily_MCP_Server_-_Tavily_Docs/image_14.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_23.png","width":24,"height":24}
    - {"type":"svg","index":24,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_25.png","width":24,"height":24}
    - {"type":"svg","index":26,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_26.png","width":14,"height":18}
    - {"type":"svg","index":27,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_27.png","width":20,"height":20}
    - {"type":"svg","index":29,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_29.png","width":14,"height":12}
    - {"type":"svg","index":30,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_32.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_36.png","width":14,"height":12}
    - {"type":"svg","index":37,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_37.png","width":14,"height":12}
    - {"type":"svg","index":38,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_40.png","width":14,"height":12}
    - {"type":"svg","index":41,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_41.png","width":16,"height":16}
    - {"type":"svg","index":42,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_44.png","width":16,"height":16}
    - {"type":"svg","index":45,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_45.png","width":14,"height":12}
    - {"type":"svg","index":46,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_47.png","width":16,"height":16}
    - {"type":"svg","index":48,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_48.png","width":14,"height":12}
    - {"type":"svg","index":49,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_49.png","width":12,"height":12}
    - {"type":"svg","index":50,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_51.png","width":12,"height":12}
    - {"type":"svg","index":52,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":54,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_55.png","width":16,"height":16}
    - {"type":"svg","index":56,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_58.png","width":14,"height":12}
    - {"type":"svg","index":59,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_59.png","width":16,"height":16}
    - {"type":"svg","index":60,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_60.png","width":16,"height":16}
    - {"type":"svg","index":61,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_61.png","width":14,"height":12}
    - {"type":"svg","index":62,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_62.png","width":14,"height":12}
    - {"type":"svg","index":63,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_63.png","width":12,"height":12}
    - {"type":"svg","index":64,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_64.png","width":16,"height":16}
    - {"type":"svg","index":65,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_65.png","width":16,"height":16}
    - {"type":"svg","index":66,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_66.png","width":16,"height":16}
    - {"type":"svg","index":67,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_67.png","width":12,"height":12}
    - {"type":"svg","index":68,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_68.png","width":16,"height":16}
    - {"type":"svg","index":69,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_69.png","width":16,"height":16}
    - {"type":"svg","index":70,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_70.png","width":16,"height":16}
    - {"type":"svg","index":71,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_71.png","width":16,"height":16}
    - {"type":"svg","index":72,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_72.png","width":14,"height":12}
    - {"type":"svg","index":73,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_73.png","width":16,"height":16}
    - {"type":"svg","index":74,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_74.png","width":16,"height":16}
    - {"type":"svg","index":75,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_75.png","width":20,"height":20}
    - {"type":"svg","index":81,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_81.png","width":14,"height":12}
    - {"type":"svg","index":82,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_82.png","width":16,"height":16}
    - {"type":"svg","index":83,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_83.png","width":16,"height":16}
    - {"type":"svg","index":84,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_84.png","width":14,"height":12}
    - {"type":"svg","index":85,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_85.png","width":12,"height":12}
    - {"type":"svg","index":86,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_86.png","width":16,"height":16}
    - {"type":"svg","index":87,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_87.png","width":16,"height":16}
    - {"type":"svg","index":88,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_88.png","width":16,"height":16}
    - {"type":"svg","index":89,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_89.png","width":16,"height":16}
    - {"type":"svg","index":90,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_90.png","width":16,"height":16}
    - {"type":"svg","index":91,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_91.png","width":16,"height":16}
    - {"type":"svg","index":92,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_92.png","width":16,"height":16}
    - {"type":"svg","index":93,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_93.png","width":12,"height":12}
    - {"type":"svg","index":94,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_94.png","width":16,"height":16}
    - {"type":"svg","index":95,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_95.png","width":12,"height":12}
    - {"type":"svg","index":96,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_96.png","width":16,"height":16}
    - {"type":"svg","index":97,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_97.png","width":16,"height":16}
    - {"type":"svg","index":98,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_98.png","width":16,"height":16}
    - {"type":"svg","index":99,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_99.png","width":14,"height":12}
    - {"type":"svg","index":100,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_100.png","width":12,"height":12}
    - {"type":"svg","index":101,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_101.png","width":16,"height":16}
    - {"type":"svg","index":102,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_102.png","width":16,"height":16}
    - {"type":"svg","index":103,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_103.png","width":16,"height":16}
    - {"type":"svg","index":104,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_104.png","width":12,"height":12}
    - {"type":"svg","index":105,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_105.png","width":16,"height":16}
    - {"type":"svg","index":106,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_106.png","width":16,"height":16}
    - {"type":"svg","index":107,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_107.png","width":16,"height":16}
    - {"type":"svg","index":108,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_108.png","width":14,"height":18}
    - {"type":"svg","index":109,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_109.png","width":12,"height":12}
    - {"type":"svg","index":110,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_110.png","width":16,"height":16}
    - {"type":"svg","index":111,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_111.png","width":14,"height":18}
    - {"type":"svg","index":112,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_112.png","width":14,"height":12}
    - {"type":"svg","index":113,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_113.png","width":16,"height":16}
    - {"type":"svg","index":114,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_114.png","width":24,"height":24}
    - {"type":"svg","index":115,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_115.png","width":16,"height":16}
    - {"type":"svg","index":116,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_116.png","width":24,"height":24}
    - {"type":"svg","index":117,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_117.png","width":14,"height":14}
    - {"type":"svg","index":118,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_118.png","width":14,"height":14}
    - {"type":"svg","index":123,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_123.png","width":20,"height":20}
    - {"type":"svg","index":124,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_124.png","width":20,"height":20}
    - {"type":"svg","index":125,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_125.png","width":20,"height":20}
    - {"type":"svg","index":126,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_126.png","width":20,"height":20}
    - {"type":"svg","index":127,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_127.png","width":49,"height":14}
    - {"type":"svg","index":128,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_128.png","width":16,"height":16}
    - {"type":"svg","index":129,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_129.png","width":16,"height":16}
    - {"type":"svg","index":130,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_130.png","width":16,"height":16}
    - {"type":"svg","index":143,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_143.png","width":16,"height":16}
    - {"type":"svg","index":144,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_144.png","width":14,"height":14}
    - {"type":"svg","index":145,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_145.png","width":16,"height":16}
    - {"type":"svg","index":146,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_146.png","width":12,"height":12}
    - {"type":"svg","index":147,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_147.png","width":14,"height":14}
    - {"type":"svg","index":148,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_148.png","width":16,"height":16}
    - {"type":"svg","index":149,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_149.png","width":12,"height":12}
    - {"type":"svg","index":150,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_150.png","width":14,"height":14}
    - {"type":"svg","index":151,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_151.png","width":16,"height":16}
    - {"type":"svg","index":152,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_152.png","width":12,"height":12}
    - {"type":"svg","index":153,"filename":"Tavily_MCP_Server_-_Tavily_Docs/svg_153.png","width":14,"height":14}
  chartData: []
  blockquotes:
    - "Note: Requires Cursor version 0.45.6 or higher"
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

# Tavily MCP Server

## 源URL

https://docs.tavily.com/documentation/mcp

## 描述

Tavily MCP Server allows you to use the Tavily API in your MCP clients.

## 内容

- Overview
- Features

- Seamless interaction with the tavily-search and tavily-extract tools
- Real-time web search capabilities through the tavily-search tool
- Intelligent data extraction from web pages via the tavily-extract tool

### Remote MCP Server

```text
https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>
```

#### Connect to Cursor

```text
{
  "mcpServers": {
    "tavily-remote-mcp": {
      "command": "npx -y mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>",
      "env": {}
    }
  }
}
```

#### Connect to Claude Desktop

#### OpenAI

- You first need to export your OPENAI_API_KEY
- You must also add your Tavily API-key to `<your-api-key>`, you can get a Tavily API key [here](https://www.tavily.com/)

```text
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "tavily",
            "server_url": "https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>",
            "require_approval": "never",
            ## Optional default parameters:
            "headers": {
                "DEFAULT_PARAMETERS": json.dumps({
                    "include_favicon": True,
                    "include_images": False,
                    "include_raw_content": False,
                }),
            },
        },
    ],
    input="Do you have access to the tavily mcp server?",
)

print(resp.output_text)
```

#### Connect to Claude Code

```text
claude mcp add tavily-remote-mcp --transport http https://mcp.tavily.com/mcp/
```

```text
{
  "mcpServers": {
    "tavily-remote-mcp": {
      "type": "http",
      "url": "https://mcp.tavily.com/mcp/"
    }
  }
}
```

#### Clients that don’t support remote MCPs

```text
{
    "tavily-remote": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.tavily.com/mcp/?tavilyApiKey=<your-api-key>"
      ]
    }
}
```

#### OAuth Authentication

- **Personal account**: If you have a key named `mcp_auth_default` in your personal account, it will be used for all OAuth-authenticated requests.
- **Team account**: If your team has a key named `mcp_auth_default`, it will be used for all OAuth-authenticated requests.
- **Both set**: If both your personal account and your team have a key named `mcp_auth_default`, the **personal key takes priority**.
- **Neither set**: If no `mcp_auth_default` key exists, the `default` key in your personal account will be used. If no `default` key is set, the first available key will be used.

#### Default Parameters

```text
{"include_images":true, "search_depth": "advanced", "max_results": 10}
```

### Local Installation

#### Prerequisites

```text
npx -y tavily-mcp@0.1.3
```

#### Configuring MCP Clients

- Cursor
- Claude Desktop

> Note: Requires Cursor version 0.45.6 or higher

1. Open Cursor Settings
2. Navigate to Features > MCP Servers
3. Click on the ”+ Add New MCP Server” button
4. Fill out the following information:

**Name**: Enter a nickname for the server (e.g., “tavily-mcp”)
**Type**: Select “command” as the type
**Command**: Enter the command to run the server:
CopyAsk AI`env TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3`
Replace `tvly-YOUR_API_KEY` with your Tavily API key from [app.tavily.com/home](https://app.tavily.com/home)
5. **Name**: Enter a nickname for the server (e.g., “tavily-mcp”)
6. **Type**: Select “command” as the type
7. **Command**: Enter the command to run the server:
CopyAsk AI`env TAVILY_API_KEY=tvly-YOUR_API_KEY npx -y tavily-mcp@0.1.3`
Replace `tvly-YOUR_API_KEY` with your Tavily API key from [app.tavily.com/home](https://app.tavily.com/home)

```text
# Create the config file if it doesn't exist
touch "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Opens the config file in TextEdit
open -e "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Alternative method using Visual Studio Code
code "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
```

```text
{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@0.1.2"],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR_API_KEY-here"
      }
    }
  }
}
```

#### Default Parameters

```text
{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "your-api-key-here",
        "DEFAULT_PARAMETERS": "{\"include_images\": true, \"max_results\": 15, \"search_depth\": \"advanced\"}"
      }
    }
  }
}
```

### Usage Examples

### Troubleshooting

### Acknowledgments

## 图片

![light logo](Tavily_MCP_Server_-_Tavily_Docs/image_1.svg)

![dark logo](Tavily_MCP_Server_-_Tavily_Docs/image_2.svg)

![GitHub Repo stars](Tavily_MCP_Server_-_Tavily_Docs/image_3.jpg)

![npm](Tavily_MCP_Server_-_Tavily_Docs/image_4.jpg)

![Tavily MCP Demo](Tavily_MCP_Server_-_Tavily_Docs/image_5.gif)

![Install MCP Server](Tavily_MCP_Server_-_Tavily_Docs/image_6.svg)

![Cursor Interface Example](Tavily_MCP_Server_-_Tavily_Docs/image_7.png)

![light logo](Tavily_MCP_Server_-_Tavily_Docs/image_8.svg)

![dark logo](Tavily_MCP_Server_-_Tavily_Docs/image_9.svg)

![Install MCP Server](Tavily_MCP_Server_-_Tavily_Docs/image_10.svg)

![Tavily MCP Demo](Tavily_MCP_Server_-_Tavily_Docs/image_11.gif)

![Cursor Interface Example](Tavily_MCP_Server_-_Tavily_Docs/image_12.png)

![tavily-logo](Tavily_MCP_Server_-_Tavily_Docs/image_13.png)

![Powered by Onetrust](Tavily_MCP_Server_-_Tavily_Docs/image_14.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Tavily_MCP_Server_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Tavily_MCP_Server_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Tavily_MCP_Server_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Tavily_MCP_Server_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Tavily_MCP_Server_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Tavily_MCP_Server_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Tavily_MCP_Server_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Tavily_MCP_Server_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Tavily_MCP_Server_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Tavily_MCP_Server_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Tavily_MCP_Server_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Tavily_MCP_Server_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](Tavily_MCP_Server_-_Tavily_Docs/svg_23.png)
*尺寸: 24x24px*

![SVG图表 24](Tavily_MCP_Server_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Tavily_MCP_Server_-_Tavily_Docs/svg_25.png)
*尺寸: 24x24px*

![SVG图表 26](Tavily_MCP_Server_-_Tavily_Docs/svg_26.png)
*尺寸: 14x18px*

![SVG图表 27](Tavily_MCP_Server_-_Tavily_Docs/svg_27.png)
*尺寸: 20x20px*

![SVG图表 29](Tavily_MCP_Server_-_Tavily_Docs/svg_29.png)
*尺寸: 14x12px*

![SVG图表 30](Tavily_MCP_Server_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 31](Tavily_MCP_Server_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](Tavily_MCP_Server_-_Tavily_Docs/svg_32.png)
*尺寸: 14x12px*

![SVG图表 34](Tavily_MCP_Server_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Tavily_MCP_Server_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](Tavily_MCP_Server_-_Tavily_Docs/svg_36.png)
*尺寸: 14x12px*

![SVG图表 37](Tavily_MCP_Server_-_Tavily_Docs/svg_37.png)
*尺寸: 14x12px*

![SVG图表 38](Tavily_MCP_Server_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](Tavily_MCP_Server_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](Tavily_MCP_Server_-_Tavily_Docs/svg_40.png)
*尺寸: 14x12px*

![SVG图表 41](Tavily_MCP_Server_-_Tavily_Docs/svg_41.png)
*尺寸: 16x16px*

![SVG图表 42](Tavily_MCP_Server_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](Tavily_MCP_Server_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](Tavily_MCP_Server_-_Tavily_Docs/svg_44.png)
*尺寸: 16x16px*

![SVG图表 45](Tavily_MCP_Server_-_Tavily_Docs/svg_45.png)
*尺寸: 14x12px*

![SVG图表 46](Tavily_MCP_Server_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](Tavily_MCP_Server_-_Tavily_Docs/svg_47.png)
*尺寸: 16x16px*

![SVG图表 48](Tavily_MCP_Server_-_Tavily_Docs/svg_48.png)
*尺寸: 14x12px*

![SVG图表 49](Tavily_MCP_Server_-_Tavily_Docs/svg_49.png)
*尺寸: 12x12px*

![SVG图表 50](Tavily_MCP_Server_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](Tavily_MCP_Server_-_Tavily_Docs/svg_51.png)
*尺寸: 12x12px*

![SVG图表 52](Tavily_MCP_Server_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](Tavily_MCP_Server_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 54](Tavily_MCP_Server_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](Tavily_MCP_Server_-_Tavily_Docs/svg_55.png)
*尺寸: 16x16px*

![SVG图表 56](Tavily_MCP_Server_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](Tavily_MCP_Server_-_Tavily_Docs/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](Tavily_MCP_Server_-_Tavily_Docs/svg_58.png)
*尺寸: 14x12px*

![SVG图表 59](Tavily_MCP_Server_-_Tavily_Docs/svg_59.png)
*尺寸: 16x16px*

![SVG图表 60](Tavily_MCP_Server_-_Tavily_Docs/svg_60.png)
*尺寸: 16x16px*

![SVG图表 61](Tavily_MCP_Server_-_Tavily_Docs/svg_61.png)
*尺寸: 14x12px*

![SVG图表 62](Tavily_MCP_Server_-_Tavily_Docs/svg_62.png)
*尺寸: 14x12px*

![SVG图表 63](Tavily_MCP_Server_-_Tavily_Docs/svg_63.png)
*尺寸: 12x12px*

![SVG图表 64](Tavily_MCP_Server_-_Tavily_Docs/svg_64.png)
*尺寸: 16x16px*

![SVG图表 65](Tavily_MCP_Server_-_Tavily_Docs/svg_65.png)
*尺寸: 16x16px*

![SVG图表 66](Tavily_MCP_Server_-_Tavily_Docs/svg_66.png)
*尺寸: 16x16px*

![SVG图表 67](Tavily_MCP_Server_-_Tavily_Docs/svg_67.png)
*尺寸: 12x12px*

![SVG图表 68](Tavily_MCP_Server_-_Tavily_Docs/svg_68.png)
*尺寸: 16x16px*

![SVG图表 69](Tavily_MCP_Server_-_Tavily_Docs/svg_69.png)
*尺寸: 16x16px*

![SVG图表 70](Tavily_MCP_Server_-_Tavily_Docs/svg_70.png)
*尺寸: 16x16px*

![SVG图表 71](Tavily_MCP_Server_-_Tavily_Docs/svg_71.png)
*尺寸: 16x16px*

![SVG图表 72](Tavily_MCP_Server_-_Tavily_Docs/svg_72.png)
*尺寸: 14x12px*

![SVG图表 73](Tavily_MCP_Server_-_Tavily_Docs/svg_73.png)
*尺寸: 16x16px*

![SVG图表 74](Tavily_MCP_Server_-_Tavily_Docs/svg_74.png)
*尺寸: 16x16px*

![SVG图表 75](Tavily_MCP_Server_-_Tavily_Docs/svg_75.png)
*尺寸: 20x20px*

![SVG图表 81](Tavily_MCP_Server_-_Tavily_Docs/svg_81.png)
*尺寸: 14x12px*

![SVG图表 82](Tavily_MCP_Server_-_Tavily_Docs/svg_82.png)
*尺寸: 16x16px*

![SVG图表 83](Tavily_MCP_Server_-_Tavily_Docs/svg_83.png)
*尺寸: 16x16px*

![SVG图表 84](Tavily_MCP_Server_-_Tavily_Docs/svg_84.png)
*尺寸: 14x12px*

![SVG图表 85](Tavily_MCP_Server_-_Tavily_Docs/svg_85.png)
*尺寸: 12x12px*

![SVG图表 86](Tavily_MCP_Server_-_Tavily_Docs/svg_86.png)
*尺寸: 16x16px*

![SVG图表 87](Tavily_MCP_Server_-_Tavily_Docs/svg_87.png)
*尺寸: 16x16px*

![SVG图表 88](Tavily_MCP_Server_-_Tavily_Docs/svg_88.png)
*尺寸: 16x16px*

![SVG图表 89](Tavily_MCP_Server_-_Tavily_Docs/svg_89.png)
*尺寸: 16x16px*

![SVG图表 90](Tavily_MCP_Server_-_Tavily_Docs/svg_90.png)
*尺寸: 16x16px*

![SVG图表 91](Tavily_MCP_Server_-_Tavily_Docs/svg_91.png)
*尺寸: 16x16px*

![SVG图表 92](Tavily_MCP_Server_-_Tavily_Docs/svg_92.png)
*尺寸: 16x16px*

![SVG图表 93](Tavily_MCP_Server_-_Tavily_Docs/svg_93.png)
*尺寸: 12x12px*

![SVG图表 94](Tavily_MCP_Server_-_Tavily_Docs/svg_94.png)
*尺寸: 16x16px*

![SVG图表 95](Tavily_MCP_Server_-_Tavily_Docs/svg_95.png)
*尺寸: 12x12px*

![SVG图表 96](Tavily_MCP_Server_-_Tavily_Docs/svg_96.png)
*尺寸: 16x16px*

![SVG图表 97](Tavily_MCP_Server_-_Tavily_Docs/svg_97.png)
*尺寸: 16x16px*

![SVG图表 98](Tavily_MCP_Server_-_Tavily_Docs/svg_98.png)
*尺寸: 16x16px*

![SVG图表 99](Tavily_MCP_Server_-_Tavily_Docs/svg_99.png)
*尺寸: 14x12px*

![SVG图表 100](Tavily_MCP_Server_-_Tavily_Docs/svg_100.png)
*尺寸: 12x12px*

![SVG图表 101](Tavily_MCP_Server_-_Tavily_Docs/svg_101.png)
*尺寸: 16x16px*

![SVG图表 102](Tavily_MCP_Server_-_Tavily_Docs/svg_102.png)
*尺寸: 16x16px*

![SVG图表 103](Tavily_MCP_Server_-_Tavily_Docs/svg_103.png)
*尺寸: 16x16px*

![SVG图表 104](Tavily_MCP_Server_-_Tavily_Docs/svg_104.png)
*尺寸: 12x12px*

![SVG图表 105](Tavily_MCP_Server_-_Tavily_Docs/svg_105.png)
*尺寸: 16x16px*

![SVG图表 106](Tavily_MCP_Server_-_Tavily_Docs/svg_106.png)
*尺寸: 16x16px*

![SVG图表 107](Tavily_MCP_Server_-_Tavily_Docs/svg_107.png)
*尺寸: 16x16px*

![SVG图表 108](Tavily_MCP_Server_-_Tavily_Docs/svg_108.png)
*尺寸: 14x18px*

![SVG图表 109](Tavily_MCP_Server_-_Tavily_Docs/svg_109.png)
*尺寸: 12x12px*

![SVG图表 110](Tavily_MCP_Server_-_Tavily_Docs/svg_110.png)
*尺寸: 16x16px*

![SVG图表 111](Tavily_MCP_Server_-_Tavily_Docs/svg_111.png)
*尺寸: 14x18px*

![SVG图表 112](Tavily_MCP_Server_-_Tavily_Docs/svg_112.png)
*尺寸: 14x12px*

![SVG图表 113](Tavily_MCP_Server_-_Tavily_Docs/svg_113.png)
*尺寸: 16x16px*

![SVG图表 114](Tavily_MCP_Server_-_Tavily_Docs/svg_114.png)
*尺寸: 24x24px*

![SVG图表 115](Tavily_MCP_Server_-_Tavily_Docs/svg_115.png)
*尺寸: 16x16px*

![SVG图表 116](Tavily_MCP_Server_-_Tavily_Docs/svg_116.png)
*尺寸: 24x24px*

![SVG图表 117](Tavily_MCP_Server_-_Tavily_Docs/svg_117.png)
*尺寸: 14x14px*

![SVG图表 118](Tavily_MCP_Server_-_Tavily_Docs/svg_118.png)
*尺寸: 14x14px*

![SVG图表 123](Tavily_MCP_Server_-_Tavily_Docs/svg_123.png)
*尺寸: 20x20px*

![SVG图表 124](Tavily_MCP_Server_-_Tavily_Docs/svg_124.png)
*尺寸: 20x20px*

![SVG图表 125](Tavily_MCP_Server_-_Tavily_Docs/svg_125.png)
*尺寸: 20x20px*

![SVG图表 126](Tavily_MCP_Server_-_Tavily_Docs/svg_126.png)
*尺寸: 20x20px*

![SVG图表 127](Tavily_MCP_Server_-_Tavily_Docs/svg_127.png)
*尺寸: 49x14px*

![SVG图表 128](Tavily_MCP_Server_-_Tavily_Docs/svg_128.png)
*尺寸: 16x16px*

![SVG图表 129](Tavily_MCP_Server_-_Tavily_Docs/svg_129.png)
*尺寸: 16x16px*

![SVG图表 130](Tavily_MCP_Server_-_Tavily_Docs/svg_130.png)
*尺寸: 16x16px*

![SVG图表 143](Tavily_MCP_Server_-_Tavily_Docs/svg_143.png)
*尺寸: 16x16px*

![SVG图表 144](Tavily_MCP_Server_-_Tavily_Docs/svg_144.png)
*尺寸: 14x14px*

![SVG图表 145](Tavily_MCP_Server_-_Tavily_Docs/svg_145.png)
*尺寸: 16x16px*

![SVG图表 146](Tavily_MCP_Server_-_Tavily_Docs/svg_146.png)
*尺寸: 12x12px*

![SVG图表 147](Tavily_MCP_Server_-_Tavily_Docs/svg_147.png)
*尺寸: 14x14px*

![SVG图表 148](Tavily_MCP_Server_-_Tavily_Docs/svg_148.png)
*尺寸: 16x16px*

![SVG图表 149](Tavily_MCP_Server_-_Tavily_Docs/svg_149.png)
*尺寸: 12x12px*

![SVG图表 150](Tavily_MCP_Server_-_Tavily_Docs/svg_150.png)
*尺寸: 14x14px*

![SVG图表 151](Tavily_MCP_Server_-_Tavily_Docs/svg_151.png)
*尺寸: 16x16px*

![SVG图表 152](Tavily_MCP_Server_-_Tavily_Docs/svg_152.png)
*尺寸: 12x12px*

![SVG图表 153](Tavily_MCP_Server_-_Tavily_Docs/svg_153.png)
*尺寸: 14x14px*
