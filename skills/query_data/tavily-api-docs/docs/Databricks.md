---
id: "url-6b8ce4dc"
type: "website"
title: "Databricks"
url: "https://docs.tavily.com/documentation/partnerships/databricks"
description: "Integrate Tavily MCP Server with Databricks for real-time web search and RAG capabilities."
source: ""
tags: []
crawl_time: "2026-03-18T07:09:52.799Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Databricks"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#overview)Overview"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#prerequisites)Prerequisites"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#setup)Setup"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#install-from-databricks-marketplace)Install from Databricks Marketplace"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#share-the-mcp-server-connection)Share the MCP server connection"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#test-tavily-mcp-server-within-databricks)Test Tavily MCP Server within Databricks"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#add-tavily-mcp-server-to-databricks-assistant)Add Tavily MCP Server to Databricks Assistant"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#use-tavily-mcp-in-your-agent-code)Use Tavily MCP in Your Agent Code"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/databricks#resources)Resources"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#overview)Overview"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#prerequisites)Prerequisites"}
    - {"type":"list","listType":"ul","items":["[Databricks workspace](https://www.databricks.com/) with the **Managed MCP Servers** preview enabled. See [Manage Databricks previews](https://docs.databricks.com/aws/en/admin/workspace-settings/manage-previews).","`CREATE CONNECTION` privilege on the Unity Catalog metastore","[Tavily API Key](https://app.tavily.com/home) for authenticating the Tavily MCP connection (via bearer token)"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#setup)Setup"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#install-from-databricks-marketplace)Install from Databricks Marketplace"}
    - {"type":"paragraph","content":"Navigate to Marketplace and find Tavily MCP Server"}
    - {"type":"paragraph","content":"Install and configure the connection"}
    - {"type":"list","listType":"ul","items":["**Connection name**: Enter a name for the Unity Catalog connection (for example, `tavily_mcp_connection`).","**Host**: Pre-populated for Tavily.","**Base path**: Pre-populated for Tavily.","**Bearer token**: Enter your Tavily API Key as the bearer token."]}
    - {"type":"paragraph","content":"Verify Unity Catalog Connection"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#share-the-mcp-server-connection)Share the MCP server connection"}
    - {"type":"paragraph","content":"Open the Unity Catalog connection"}
    - {"type":"paragraph","content":"Grant access to the connection"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#test-tavily-mcp-server-within-databricks)Test Tavily MCP Server within Databricks"}
    - {"type":"paragraph","content":"Open AI Playground"}
    - {"type":"paragraph","content":"Add Tavily MCP Server as a tool"}
    - {"type":"paragraph","content":"Chat and test Tavily MCP Server"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#add-tavily-mcp-server-to-databricks-assistant)Add Tavily MCP Server to Databricks Assistant"}
    - {"type":"paragraph","content":"Open Databricks Assistant"}
    - {"type":"paragraph","content":"Add MCP Server from Settings"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#use-tavily-mcp-in-your-agent-code)Use Tavily MCP in Your Agent Code"}
    - {"type":"paragraph","content":"Configure the proxy endpoint"}
    - {"type":"codeblock","language":"","content":"from databricks.sdk import WorkspaceClient\nfrom databricks_mcp import DatabricksMCPClient\n\n# Initialize workspace client\nworkspace_client = WorkspaceClient()\nhost = workspace_client.config.host\n\n# External MCP servers are proxied as managed servers, allowing you\n# to use the same API for both managed and external servers\nMANAGED_MCP_SERVER_URLS = [\n    f\"{host}/api/2.0/mcp/functions/system/ai\",  # Default managed MCP\n    f\"{host}/api/2.0/mcp/external/tavily_mcp_connection\"  # Tavily MCP proxy\n]"}
    - {"type":"paragraph","content":"Use with agents"}
    - {"type":"codeblock","language":"","content":"# Use with agents — external servers work just like managed ones\nimport asyncio\nfrom your_agent_code import create_mcp_tools  # Your agent's tool creation function\n\n# Create tools from both managed and external (proxied) servers\nmcp_tools = asyncio.run(\n    create_mcp_tools(\n        ws=workspace_client,\n        managed_server_urls=MANAGED_MCP_SERVER_URLS\n    )\n)"}
    - {"type":"paragraph","content":"Call tools directly (optional)"}
    - {"type":"codeblock","language":"","content":"# Direct tool call using DatabricksMCPClient\nmcp_client = DatabricksMCPClient(\n    server_url=f\"{host}/api/2.0/mcp/external/tavily_mcp_connection\",\n    workspace_client=workspace_client\n)\n\n# List available tools\ntools = mcp_client.list_tools()\nprint(f\"Available tools: {[tool.name for tool in tools]}\")\n\n# Call a tool\nresponse = mcp_client.call_tool(\n    \"tavily_search\",\n    {\"query\": \"latest AI research breakthroughs\"}\n)\nprint(response.content[0].text)"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/databricks#resources)Resources"}
    - {"type":"list","listType":"ul","items":["[Tavily MCP Server on Databricks Marketplace](https://marketplace.databricks.com/details/3709f418-1ed3-42a8-a753-38d06ce281c7/Tavily_Tavily-MCP-Server)","[Tavily MCP Documentation](https://docs.tavily.com/documentation/mcp)"]}
  paragraphs:
    - "Navigate to Marketplace and find Tavily MCP Server"
    - "Install and configure the connection"
    - "Verify Unity Catalog Connection"
    - "Open the Unity Catalog connection"
    - "Grant access to the connection"
    - "Open AI Playground"
    - "Add Tavily MCP Server as a tool"
    - "Chat and test Tavily MCP Server"
    - "Open Databricks Assistant"
    - "Add MCP Server from Settings"
    - "Configure the proxy endpoint"
    - "Use with agents"
    - "Call tools directly (optional)"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Overview](https://docs.tavily.com/documentation/partnerships/databricks#overview)","[Prerequisites](https://docs.tavily.com/documentation/partnerships/databricks#prerequisites)","[Setup](https://docs.tavily.com/documentation/partnerships/databricks#setup)","[Install from Databricks Marketplace](https://docs.tavily.com/documentation/partnerships/databricks#install-from-databricks-marketplace)","[Share the MCP server connection](https://docs.tavily.com/documentation/partnerships/databricks#share-the-mcp-server-connection)","[Test Tavily MCP Server within Databricks](https://docs.tavily.com/documentation/partnerships/databricks#test-tavily-mcp-server-within-databricks)","[Add Tavily MCP Server to Databricks Assistant](https://docs.tavily.com/documentation/partnerships/databricks#add-tavily-mcp-server-to-databricks-assistant)","[Use Tavily MCP in Your Agent Code](https://docs.tavily.com/documentation/partnerships/databricks#use-tavily-mcp-in-your-agent-code)","[Resources](https://docs.tavily.com/documentation/partnerships/databricks#resources)"]}
    - {"type":"ul","items":["[Databricks workspace](https://www.databricks.com/) with the Managed MCP Servers preview enabled. See [Manage Databricks previews](https://docs.databricks.com/aws/en/admin/workspace-settings/manage-previews).","CREATE CONNECTION privilege on the Unity Catalog metastore","[Tavily API Key](https://app.tavily.com/home) for authenticating the Tavily MCP connection (via bearer token)"]}
    - {"type":"ul","items":["Connection name: Enter a name for the Unity Catalog connection (for example, tavily_mcp_connection).","Host: Pre-populated for Tavily.","Base path: Pre-populated for Tavily.","Bearer token: Enter your Tavily API Key as the bearer token."]}
    - {"type":"ul","items":["[Tavily MCP Server on Databricks Marketplace](https://marketplace.databricks.com/details/3709f418-1ed3-42a8-a753-38d06ce281c7/Tavily_Tavily-MCP-Server)","[Tavily MCP Documentation](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"from databricks.sdk import WorkspaceClient\nfrom databricks_mcp import DatabricksMCPClient\n\n# Initialize workspace client\nworkspace_client = WorkspaceClient()\nhost = workspace_client.config.host\n\n# External MCP servers are proxied as managed servers, allowing you\n# to use the same API for both managed and external servers\nMANAGED_MCP_SERVER_URLS = [\n    f\"{host}/api/2.0/mcp/functions/system/ai\",  # Default managed MCP\n    f\"{host}/api/2.0/mcp/external/tavily_mcp_connection\"  # Tavily MCP proxy\n]"}
    - {"language":"text","code":"from databricks.sdk import WorkspaceClient\nfrom databricks_mcp import DatabricksMCPClient\n\n# Initialize workspace client\nworkspace_client = WorkspaceClient()\nhost = workspace_client.config.host\n\n# External MCP servers are proxied as managed servers, allowing you\n# to use the same API for both managed and external servers\nMANAGED_MCP_SERVER_URLS = [\n    f\"{host}/api/2.0/mcp/functions/system/ai\",  # Default managed MCP\n    f\"{host}/api/2.0/mcp/external/tavily_mcp_connection\"  # Tavily MCP proxy\n]"}
    - {"language":"text","code":"# Use with agents — external servers work just like managed ones\nimport asyncio\nfrom your_agent_code import create_mcp_tools  # Your agent's tool creation function\n\n# Create tools from both managed and external (proxied) servers\nmcp_tools = asyncio.run(\n    create_mcp_tools(\n        ws=workspace_client,\n        managed_server_urls=MANAGED_MCP_SERVER_URLS\n    )\n)"}
    - {"language":"text","code":"# Use with agents — external servers work just like managed ones\nimport asyncio\nfrom your_agent_code import create_mcp_tools  # Your agent's tool creation function\n\n# Create tools from both managed and external (proxied) servers\nmcp_tools = asyncio.run(\n    create_mcp_tools(\n        ws=workspace_client,\n        managed_server_urls=MANAGED_MCP_SERVER_URLS\n    )\n)"}
    - {"language":"text","code":"# Direct tool call using DatabricksMCPClient\nmcp_client = DatabricksMCPClient(\n    server_url=f\"{host}/api/2.0/mcp/external/tavily_mcp_connection\",\n    workspace_client=workspace_client\n)\n\n# List available tools\ntools = mcp_client.list_tools()\nprint(f\"Available tools: {[tool.name for tool in tools]}\")\n\n# Call a tool\nresponse = mcp_client.call_tool(\n    \"tavily_search\",\n    {\"query\": \"latest AI research breakthroughs\"}\n)\nprint(response.content[0].text)"}
    - {"language":"text","code":"# Direct tool call using DatabricksMCPClient\nmcp_client = DatabricksMCPClient(\n    server_url=f\"{host}/api/2.0/mcp/external/tavily_mcp_connection\",\n    workspace_client=workspace_client\n)\n\n# List available tools\ntools = mcp_client.list_tools()\nprint(f\"Available tools: {[tool.name for tool in tools]}\")\n\n# Call a tool\nresponse = mcp_client.call_tool(\n    \"tavily_search\",\n    {\"query\": \"latest AI research breakthroughs\"}\n)\nprint(response.content[0].text)"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Databricks_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Databricks_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/tavilymcp.gif?s=35a5154bf150c14c2da906302c4c0e1c","localPath":"Databricks_-_Tavily_Docs/image_3.gif","alt":"Search for Tavily MCP Server in Databricks Marketplace","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/configmcp.gif?s=4bb7cd389d3a4946a9de6fc1727573e8","localPath":"Databricks_-_Tavily_Docs/image_4.gif","alt":"Configure the connection for Tavily MCP Server","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/verifyconnection.gif?s=961b443e643b84028dbe7c38a26cdb7c","localPath":"Databricks_-_Tavily_Docs/image_5.gif","alt":"Verify the connection from Unity Catalog","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/connections.gif?s=f1dcff39a064a8772349f517fcbded02","localPath":"Databricks_-_Tavily_Docs/image_6.gif","alt":"Open the Unity Catalog Connections","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/useconnection.gif?s=2b82c6f3769d1a1f312a6971756284c4","localPath":"Databricks_-_Tavily_Docs/image_7.gif","alt":"Grant USE CONNECTION privileges to identity principals","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/model.gif?s=329fd57e0ceb6472077f49298542b911","localPath":"Databricks_-_Tavily_Docs/image_8.gif","alt":"Select a model in AI Playground","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/tool.gif?s=da6126bde43802d05ce1b4206ef016bb","localPath":"Databricks_-_Tavily_Docs/image_9.gif","alt":"Add Tavily MCP Server as a tool","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/tavilyresults.gif?s=2dcc0826ff4f6f2638692319c6c82518","localPath":"Databricks_-_Tavily_Docs/image_10.gif","alt":"Test Tavily MCP Server results","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/assistant.gif?s=8f5f6075d8fe3d0992ede976bc97fa5b","localPath":"Databricks_-_Tavily_Docs/image_11.gif","alt":"Add MCP Server from Settings","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Databricks_-_Tavily_Docs/image_12.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Databricks_-_Tavily_Docs/image_13.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/tavilymcp.gif?s=35a5154bf150c14c2da906302c4c0e1c","localPath":"Databricks_-_Tavily_Docs/image_14.gif","alt":"Search for Tavily MCP Server in Databricks Marketplace","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/configmcp.gif?s=4bb7cd389d3a4946a9de6fc1727573e8","localPath":"Databricks_-_Tavily_Docs/image_15.gif","alt":"Configure the connection for Tavily MCP Server","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/verifyconnection.gif?s=961b443e643b84028dbe7c38a26cdb7c","localPath":"Databricks_-_Tavily_Docs/image_16.gif","alt":"Verify the connection from Unity Catalog","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/connections.gif?s=f1dcff39a064a8772349f517fcbded02","localPath":"Databricks_-_Tavily_Docs/image_17.gif","alt":"Open the Unity Catalog Connections","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/useconnection.gif?s=2b82c6f3769d1a1f312a6971756284c4","localPath":"Databricks_-_Tavily_Docs/image_18.gif","alt":"Grant USE CONNECTION privileges to identity principals","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/model.gif?s=329fd57e0ceb6472077f49298542b911","localPath":"Databricks_-_Tavily_Docs/image_19.gif","alt":"Select a model in AI Playground","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/tool.gif?s=da6126bde43802d05ce1b4206ef016bb","localPath":"Databricks_-_Tavily_Docs/image_20.gif","alt":"Add Tavily MCP Server as a tool","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/tavilyresults.gif?s=2dcc0826ff4f6f2638692319c6c82518","localPath":"Databricks_-_Tavily_Docs/image_21.gif","alt":"Test Tavily MCP Server results","title":""}
    - {"src":"https://mintcdn.com/tavilyai/3qtRHnSgAhfp9BRT/images/partnerships/databricks/assistant.gif?s=8f5f6075d8fe3d0992ede976bc97fa5b","localPath":"Databricks_-_Tavily_Docs/image_22.gif","alt":"Add MCP Server from Settings","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Databricks_-_Tavily_Docs/image_23.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Databricks_-_Tavily_Docs/image_24.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Databricks_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Databricks_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Databricks_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Databricks_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Databricks_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Databricks_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Databricks_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Databricks_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Databricks_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Databricks_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Databricks_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Databricks_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Databricks_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Databricks_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Databricks_-_Tavily_Docs/svg_25.png","width":14,"height":12}
    - {"type":"svg","index":26,"filename":"Databricks_-_Tavily_Docs/svg_26.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"Databricks_-_Tavily_Docs/svg_28.png","width":14,"height":12}
    - {"type":"svg","index":30,"filename":"Databricks_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":32,"filename":"Databricks_-_Tavily_Docs/svg_32.png","width":14,"height":12}
    - {"type":"svg","index":33,"filename":"Databricks_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":35,"filename":"Databricks_-_Tavily_Docs/svg_35.png","width":14,"height":12}
    - {"type":"svg","index":37,"filename":"Databricks_-_Tavily_Docs/svg_37.png","width":14,"height":12}
    - {"type":"svg","index":38,"filename":"Databricks_-_Tavily_Docs/svg_38.png","width":14,"height":12}
    - {"type":"svg","index":40,"filename":"Databricks_-_Tavily_Docs/svg_40.png","width":14,"height":12}
    - {"type":"svg","index":42,"filename":"Databricks_-_Tavily_Docs/svg_42.png","width":14,"height":12}
    - {"type":"svg","index":44,"filename":"Databricks_-_Tavily_Docs/svg_44.png","width":14,"height":12}
    - {"type":"svg","index":45,"filename":"Databricks_-_Tavily_Docs/svg_45.png","width":14,"height":12}
    - {"type":"svg","index":46,"filename":"Databricks_-_Tavily_Docs/svg_46.png","width":14,"height":12}
    - {"type":"svg","index":48,"filename":"Databricks_-_Tavily_Docs/svg_48.png","width":14,"height":12}
    - {"type":"svg","index":49,"filename":"Databricks_-_Tavily_Docs/svg_49.png","width":14,"height":12}
    - {"type":"svg","index":50,"filename":"Databricks_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"Databricks_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"Databricks_-_Tavily_Docs/svg_52.png","width":14,"height":12}
    - {"type":"svg","index":53,"filename":"Databricks_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":54,"filename":"Databricks_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"Databricks_-_Tavily_Docs/svg_55.png","width":14,"height":12}
    - {"type":"svg","index":56,"filename":"Databricks_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"Databricks_-_Tavily_Docs/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"Databricks_-_Tavily_Docs/svg_58.png","width":14,"height":12}
    - {"type":"svg","index":59,"filename":"Databricks_-_Tavily_Docs/svg_59.png","width":14,"height":14}
    - {"type":"svg","index":60,"filename":"Databricks_-_Tavily_Docs/svg_60.png","width":14,"height":14}
    - {"type":"svg","index":61,"filename":"Databricks_-_Tavily_Docs/svg_61.png","width":14,"height":14}
    - {"type":"svg","index":66,"filename":"Databricks_-_Tavily_Docs/svg_66.png","width":20,"height":20}
    - {"type":"svg","index":67,"filename":"Databricks_-_Tavily_Docs/svg_67.png","width":20,"height":20}
    - {"type":"svg","index":68,"filename":"Databricks_-_Tavily_Docs/svg_68.png","width":20,"height":20}
    - {"type":"svg","index":69,"filename":"Databricks_-_Tavily_Docs/svg_69.png","width":20,"height":20}
    - {"type":"svg","index":70,"filename":"Databricks_-_Tavily_Docs/svg_70.png","width":49,"height":14}
    - {"type":"svg","index":71,"filename":"Databricks_-_Tavily_Docs/svg_71.png","width":16,"height":16}
    - {"type":"svg","index":72,"filename":"Databricks_-_Tavily_Docs/svg_72.png","width":16,"height":16}
    - {"type":"svg","index":73,"filename":"Databricks_-_Tavily_Docs/svg_73.png","width":16,"height":16}
    - {"type":"svg","index":92,"filename":"Databricks_-_Tavily_Docs/svg_92.png","width":16,"height":16}
    - {"type":"svg","index":93,"filename":"Databricks_-_Tavily_Docs/svg_93.png","width":14,"height":14}
    - {"type":"svg","index":94,"filename":"Databricks_-_Tavily_Docs/svg_94.png","width":16,"height":16}
    - {"type":"svg","index":95,"filename":"Databricks_-_Tavily_Docs/svg_95.png","width":12,"height":12}
    - {"type":"svg","index":96,"filename":"Databricks_-_Tavily_Docs/svg_96.png","width":14,"height":14}
    - {"type":"svg","index":97,"filename":"Databricks_-_Tavily_Docs/svg_97.png","width":16,"height":16}
    - {"type":"svg","index":98,"filename":"Databricks_-_Tavily_Docs/svg_98.png","width":12,"height":12}
    - {"type":"svg","index":99,"filename":"Databricks_-_Tavily_Docs/svg_99.png","width":14,"height":14}
    - {"type":"svg","index":100,"filename":"Databricks_-_Tavily_Docs/svg_100.png","width":16,"height":16}
    - {"type":"svg","index":101,"filename":"Databricks_-_Tavily_Docs/svg_101.png","width":12,"height":12}
    - {"type":"svg","index":102,"filename":"Databricks_-_Tavily_Docs/svg_102.png","width":14,"height":14}
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

# Databricks

## 源URL

https://docs.tavily.com/documentation/partnerships/databricks

## 描述

Integrate Tavily MCP Server with Databricks for real-time web search and RAG capabilities.

## 内容

### Overview

### Prerequisites

- [Databricks workspace](https://www.databricks.com/) with the **Managed MCP Servers** preview enabled. See [Manage Databricks previews](https://docs.databricks.com/aws/en/admin/workspace-settings/manage-previews).
- `CREATE CONNECTION` privilege on the Unity Catalog metastore
- [Tavily API Key](https://app.tavily.com/home) for authenticating the Tavily MCP connection (via bearer token)

### Setup

#### Install from Databricks Marketplace

Navigate to Marketplace and find Tavily MCP Server

Install and configure the connection

- **Connection name**: Enter a name for the Unity Catalog connection (for example, `tavily_mcp_connection`).
- **Host**: Pre-populated for Tavily.
- **Base path**: Pre-populated for Tavily.
- **Bearer token**: Enter your Tavily API Key as the bearer token.

Verify Unity Catalog Connection

#### Share the MCP server connection

Open the Unity Catalog connection

Grant access to the connection

#### Test Tavily MCP Server within Databricks

Open AI Playground

Add Tavily MCP Server as a tool

Chat and test Tavily MCP Server

#### Add Tavily MCP Server to Databricks Assistant

Open Databricks Assistant

Add MCP Server from Settings

#### Use Tavily MCP in Your Agent Code

Configure the proxy endpoint

```text
from databricks.sdk import WorkspaceClient
from databricks_mcp import DatabricksMCPClient

# Initialize workspace client
workspace_client = WorkspaceClient()
host = workspace_client.config.host

# External MCP servers are proxied as managed servers, allowing you
# to use the same API for both managed and external servers
MANAGED_MCP_SERVER_URLS = [
    f"{host}/api/2.0/mcp/functions/system/ai",  # Default managed MCP
    f"{host}/api/2.0/mcp/external/tavily_mcp_connection"  # Tavily MCP proxy
]
```

Use with agents

```text
# Use with agents — external servers work just like managed ones
import asyncio
from your_agent_code import create_mcp_tools  # Your agent's tool creation function

# Create tools from both managed and external (proxied) servers
mcp_tools = asyncio.run(
    create_mcp_tools(
        ws=workspace_client,
        managed_server_urls=MANAGED_MCP_SERVER_URLS
    )
)
```

Call tools directly (optional)

```text
# Direct tool call using DatabricksMCPClient
mcp_client = DatabricksMCPClient(
    server_url=f"{host}/api/2.0/mcp/external/tavily_mcp_connection",
    workspace_client=workspace_client
)

# List available tools
tools = mcp_client.list_tools()
print(f"Available tools: {[tool.name for tool in tools]}")

# Call a tool
response = mcp_client.call_tool(
    "tavily_search",
    {"query": "latest AI research breakthroughs"}
)
print(response.content[0].text)
```

### Resources

- [Tavily MCP Server on Databricks Marketplace](https://marketplace.databricks.com/details/3709f418-1ed3-42a8-a753-38d06ce281c7/Tavily_Tavily-MCP-Server)
- [Tavily MCP Documentation](https://docs.tavily.com/documentation/mcp)

## 图片

![light logo](Databricks_-_Tavily_Docs/image_1.svg)

![dark logo](Databricks_-_Tavily_Docs/image_2.svg)

![Search for Tavily MCP Server in Databricks Marketplace](Databricks_-_Tavily_Docs/image_3.gif)

![Configure the connection for Tavily MCP Server](Databricks_-_Tavily_Docs/image_4.gif)

![Verify the connection from Unity Catalog](Databricks_-_Tavily_Docs/image_5.gif)

![Open the Unity Catalog Connections](Databricks_-_Tavily_Docs/image_6.gif)

![Grant USE CONNECTION privileges to identity principals](Databricks_-_Tavily_Docs/image_7.gif)

![Select a model in AI Playground](Databricks_-_Tavily_Docs/image_8.gif)

![Add Tavily MCP Server as a tool](Databricks_-_Tavily_Docs/image_9.gif)

![Test Tavily MCP Server results](Databricks_-_Tavily_Docs/image_10.gif)

![Add MCP Server from Settings](Databricks_-_Tavily_Docs/image_11.gif)

![light logo](Databricks_-_Tavily_Docs/image_12.svg)

![dark logo](Databricks_-_Tavily_Docs/image_13.svg)

![Search for Tavily MCP Server in Databricks Marketplace](Databricks_-_Tavily_Docs/image_14.gif)

![Configure the connection for Tavily MCP Server](Databricks_-_Tavily_Docs/image_15.gif)

![Verify the connection from Unity Catalog](Databricks_-_Tavily_Docs/image_16.gif)

![Open the Unity Catalog Connections](Databricks_-_Tavily_Docs/image_17.gif)

![Grant USE CONNECTION privileges to identity principals](Databricks_-_Tavily_Docs/image_18.gif)

![Select a model in AI Playground](Databricks_-_Tavily_Docs/image_19.gif)

![Add Tavily MCP Server as a tool](Databricks_-_Tavily_Docs/image_20.gif)

![Test Tavily MCP Server results](Databricks_-_Tavily_Docs/image_21.gif)

![Add MCP Server from Settings](Databricks_-_Tavily_Docs/image_22.gif)

![tavily-logo](Databricks_-_Tavily_Docs/image_23.png)

![Powered by Onetrust](Databricks_-_Tavily_Docs/image_24.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Databricks_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Databricks_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Databricks_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Databricks_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Databricks_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Databricks_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Databricks_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Databricks_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Databricks_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Databricks_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Databricks_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Databricks_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Databricks_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Databricks_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Databricks_-_Tavily_Docs/svg_25.png)
*尺寸: 14x12px*

![SVG图表 26](Databricks_-_Tavily_Docs/svg_26.png)
*尺寸: 14x12px*

![SVG图表 28](Databricks_-_Tavily_Docs/svg_28.png)
*尺寸: 14x12px*

![SVG图表 30](Databricks_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 32](Databricks_-_Tavily_Docs/svg_32.png)
*尺寸: 14x12px*

![SVG图表 33](Databricks_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 35](Databricks_-_Tavily_Docs/svg_35.png)
*尺寸: 14x12px*

![SVG图表 37](Databricks_-_Tavily_Docs/svg_37.png)
*尺寸: 14x12px*

![SVG图表 38](Databricks_-_Tavily_Docs/svg_38.png)
*尺寸: 14x12px*

![SVG图表 40](Databricks_-_Tavily_Docs/svg_40.png)
*尺寸: 14x12px*

![SVG图表 42](Databricks_-_Tavily_Docs/svg_42.png)
*尺寸: 14x12px*

![SVG图表 44](Databricks_-_Tavily_Docs/svg_44.png)
*尺寸: 14x12px*

![SVG图表 45](Databricks_-_Tavily_Docs/svg_45.png)
*尺寸: 14x12px*

![SVG图表 46](Databricks_-_Tavily_Docs/svg_46.png)
*尺寸: 14x12px*

![SVG图表 48](Databricks_-_Tavily_Docs/svg_48.png)
*尺寸: 14x12px*

![SVG图表 49](Databricks_-_Tavily_Docs/svg_49.png)
*尺寸: 14x12px*

![SVG图表 50](Databricks_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](Databricks_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 52](Databricks_-_Tavily_Docs/svg_52.png)
*尺寸: 14x12px*

![SVG图表 53](Databricks_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 54](Databricks_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](Databricks_-_Tavily_Docs/svg_55.png)
*尺寸: 14x12px*

![SVG图表 56](Databricks_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](Databricks_-_Tavily_Docs/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](Databricks_-_Tavily_Docs/svg_58.png)
*尺寸: 14x12px*

![SVG图表 59](Databricks_-_Tavily_Docs/svg_59.png)
*尺寸: 14x14px*

![SVG图表 60](Databricks_-_Tavily_Docs/svg_60.png)
*尺寸: 14x14px*

![SVG图表 61](Databricks_-_Tavily_Docs/svg_61.png)
*尺寸: 14x14px*

![SVG图表 66](Databricks_-_Tavily_Docs/svg_66.png)
*尺寸: 20x20px*

![SVG图表 67](Databricks_-_Tavily_Docs/svg_67.png)
*尺寸: 20x20px*

![SVG图表 68](Databricks_-_Tavily_Docs/svg_68.png)
*尺寸: 20x20px*

![SVG图表 69](Databricks_-_Tavily_Docs/svg_69.png)
*尺寸: 20x20px*

![SVG图表 70](Databricks_-_Tavily_Docs/svg_70.png)
*尺寸: 49x14px*

![SVG图表 71](Databricks_-_Tavily_Docs/svg_71.png)
*尺寸: 16x16px*

![SVG图表 72](Databricks_-_Tavily_Docs/svg_72.png)
*尺寸: 16x16px*

![SVG图表 73](Databricks_-_Tavily_Docs/svg_73.png)
*尺寸: 16x16px*

![SVG图表 92](Databricks_-_Tavily_Docs/svg_92.png)
*尺寸: 16x16px*

![SVG图表 93](Databricks_-_Tavily_Docs/svg_93.png)
*尺寸: 14x14px*

![SVG图表 94](Databricks_-_Tavily_Docs/svg_94.png)
*尺寸: 16x16px*

![SVG图表 95](Databricks_-_Tavily_Docs/svg_95.png)
*尺寸: 12x12px*

![SVG图表 96](Databricks_-_Tavily_Docs/svg_96.png)
*尺寸: 14x14px*

![SVG图表 97](Databricks_-_Tavily_Docs/svg_97.png)
*尺寸: 16x16px*

![SVG图表 98](Databricks_-_Tavily_Docs/svg_98.png)
*尺寸: 12x12px*

![SVG图表 99](Databricks_-_Tavily_Docs/svg_99.png)
*尺寸: 14x14px*

![SVG图表 100](Databricks_-_Tavily_Docs/svg_100.png)
*尺寸: 16x16px*

![SVG图表 101](Databricks_-_Tavily_Docs/svg_101.png)
*尺寸: 12x12px*

![SVG图表 102](Databricks_-_Tavily_Docs/svg_102.png)
*尺寸: 14x14px*
