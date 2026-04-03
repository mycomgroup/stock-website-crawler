---
id: "url-38332ef2"
type: "website"
title: "Snowflake"
url: "https://docs.tavily.com/documentation/partnerships/snowflake"
description: "Tavily is now available as a native app on the Snowflake Marketplace."
source: ""
tags: []
crawl_time: "2026-03-18T06:45:26.659Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Snowflake"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#tutorial)Tutorial"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#installation-and-setup)Installation and Setup"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#use-cases)Use cases"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#using-tavily_web_search-in-snowsight)Using TAVILY_WEB_SEARCH in Snowsight"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#using-tavily_web_search-in-snowflake-intelligence)Using TAVILY_WEB_SEARCH in Snowflake Intelligence"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#tutorial)Tutorial"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#installation-and-setup)Installation and Setup"}
    - {"type":"list","listType":"ol","items":["After logging into your Snowflake account, click on *Marketplace* from the sidebar.","In the search bar, search for *Tavily* and find the *Tavily Search API* app.","Click on *GET* in the right top side to download the app into your Snowflake account.","Read through the permissions and click on *Agree and Continue* and click on *GET*.","After the app finished downloading, hover over *Catalog* in the left sidebar and click on *Apps*.","Locate the Tavily app named *Tavily Search API* in the installed apps section.","Now you have to configure the application.","Visit [https://tavily.com](https://tavily.com/) to get your API key if you don’t already have one.","After you have your API key, click on the *Configure* button and pass the API key in the secret value box to configure the API key for your native app.","Now, in the *Review integration requests* section, click on *Review* and toggle the button to the right to enable your app *Access the Tavily external API for web search*.","Click on *Save*. Now you have successfully configured your application for use in the Snowflake environment.","Click on *Next* to visit the app page."]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#use-cases)Use cases"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#using-tavily_web_search-in-snowsight)Using TAVILY_WEB_SEARCH in Snowsight"}
    - {"type":"list","listType":"ol","items":["After installation in the app page, you can click on *Open Worksheet* to pop up a Snowflake worksheet with a pre-loaded SQL query to use Tavily web search.","Make sure to select the appropriate database for your worksheet. In the top right, ensure the database is `TAVILY_SEARCH_API` and the schema is `TAVILY_SCHEMA`.","Now you can click the *Run* button on the top left of your worksheet to run the query."]}
    - {"type":"list","listType":"ul","items":["`QUERY` (VARCHAR): The search query in natural language","`SEARCH_DEPTH` (VARCHAR, optional): `'basic'` (default) or `'advanced'`","`MAX_RESULTS` (INTEGER, optional): Maximum number of results (default: 5)"]}
    - {"type":"codeblock","language":"","content":"CALL TAVILY_SCHEMA.TAVILY_WEB_SEARCH('latest Quantum computing trends', 'advanced', 10);"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/partnerships/snowflake#using-tavily_web_search-in-snowflake-intelligence)Using TAVILY_WEB_SEARCH in Snowflake Intelligence"}
    - {"type":"list","listType":"ol","items":["**Set up Snowflake Intelligence**: Follow the [Snowflake documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence) to set up Snowflake Intelligence. Make sure you have the snowflake_intelligence database, required schema and GRANTs before proceeding to the next steps.","**Create an Agent**: In the Snowsight UI sidebar, navigate to the *Agents* admin page under *AI & ML*, click on *create agent* and provide agent object name, display name and create the agent.","**Add the TAVILY_WEB_SEARCH Custom Tool**: Within the current agent’s menu bar, navigate to the *Tools* section and click on *+Add* in Custom tools.\n\n\nSelect the Resource type as *Procedure*\n\n\nSelect the database and schema: `TAVILY_SEARCH_API.TAVILY_SCHEMA`\n\n\nSelect the custom tool identifier: `TAVILY_SEARCH_API.TAVILY_SCHEMA.TAVILY_WEB_SEARCH`\n\n\nGive your tool a descriptive name\n\n\nConfigure the following parameters with their descriptions:\n\n\n`query`: “Search query”\n\n\n`search_depth`: “The depth of the search. It can be ‘basic’ or ‘advanced’”\n\n\n`max_results`: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”\n\n\n\n\nClick on *Add* to attach the tool to your agent\n\n\nMake sure to click on *Save* in the top right corner to update the agent","Select the Resource type as *Procedure*","Select the database and schema: `TAVILY_SEARCH_API.TAVILY_SCHEMA`","Select the custom tool identifier: `TAVILY_SEARCH_API.TAVILY_SCHEMA.TAVILY_WEB_SEARCH`","Give your tool a descriptive name","Configure the following parameters with their descriptions:\n\n\n`query`: “Search query”\n\n\n`search_depth`: “The depth of the search. It can be ‘basic’ or ‘advanced’”\n\n\n`max_results`: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”","`query`: “Search query”","`search_depth`: “The depth of the search. It can be ‘basic’ or ‘advanced’”","`max_results`: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”","Click on *Add* to attach the tool to your agent","Make sure to click on *Save* in the top right corner to update the agent","**Use the Agent**: In the Snowsight UI sidebar, navigate to the *Snowflake Intelligence* landing page under *AI & ML*, select the agent you created, and use the tool."]}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/partnerships/snowflake#introduction)","[Tutorial](https://docs.tavily.com/documentation/partnerships/snowflake#tutorial)","[Installation and Setup](https://docs.tavily.com/documentation/partnerships/snowflake#installation-and-setup)","[Use cases](https://docs.tavily.com/documentation/partnerships/snowflake#use-cases)","[Using TAVILY_WEB_SEARCH in Snowsight](https://docs.tavily.com/documentation/partnerships/snowflake#using-tavily_web_search-in-snowsight)","[Using TAVILY_WEB_SEARCH in Snowflake Intelligence](https://docs.tavily.com/documentation/partnerships/snowflake#using-tavily_web_search-in-snowflake-intelligence)"]}
    - {"type":"ol","items":["After logging into your Snowflake account, click on Marketplace from the sidebar.","In the search bar, search for Tavily and find the Tavily Search API app.","Click on GET in the right top side to download the app into your Snowflake account.","Read through the permissions and click on Agree and Continue and click on GET.","After the app finished downloading, hover over Catalog in the left sidebar and click on Apps.","Locate the Tavily app named Tavily Search API in the installed apps section.","Now you have to configure the application.","Visit [https://tavily.com](https://tavily.com/) to get your API key if you don’t already have one.","After you have your API key, click on the Configure button and pass the API key in the secret value box to configure the API key for your native app.","Now, in the Review integration requests section, click on Review and toggle the button to the right to enable your app Access the Tavily external API for web search.","Click on Save. Now you have successfully configured your application for use in the Snowflake environment.","Click on Next to visit the app page."]}
    - {"type":"ol","items":["After installation in the app page, you can click on Open Worksheet to pop up a Snowflake worksheet with a pre-loaded SQL query to use Tavily web search.","Make sure to select the appropriate database for your worksheet. In the top right, ensure the database is TAVILY_SEARCH_API and the schema is TAVILY_SCHEMA.","Now you can click the Run button on the top left of your worksheet to run the query."]}
    - {"type":"ul","items":["QUERY (VARCHAR): The search query in natural language","SEARCH_DEPTH (VARCHAR, optional): 'basic' (default) or 'advanced'","MAX_RESULTS (INTEGER, optional): Maximum number of results (default: 5)"]}
    - {"type":"ol","items":["Set up Snowflake Intelligence: Follow the [Snowflake documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence) to set up Snowflake Intelligence. Make sure you have the snowflake_intelligence database, required schema and GRANTs before proceeding to the next steps.","Create an Agent: In the Snowsight UI sidebar, navigate to the Agents admin page under AI & ML, click on create agent and provide agent object name, display name and create the agent.","Add the TAVILY_WEB_SEARCH Custom Tool: Within the current agent’s menu bar, navigate to the Tools section and click on +Add in Custom tools.\n\n\nSelect the Resource type as Procedure\n\n\nSelect the database and schema: TAVILY_SEARCH_API.TAVILY_SCHEMA\n\n\nSelect the custom tool identifier: TAVILY_SEARCH_API.TAVILY_SCHEMA.TAVILY_WEB_SEARCH\n\n\nGive your tool a descriptive name\n\n\nConfigure the following parameters with their descriptions:\n\n\nquery: “Search query”\n\n\nsearch_depth: “The depth of the search. It can be ‘basic’ or ‘advanced’”\n\n\nmax_results: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”\n\n\n\n\nClick on Add to attach the tool to your agent\n\n\nMake sure to click on Save in the top right corner to update the agent","Select the Resource type as Procedure","Select the database and schema: TAVILY_SEARCH_API.TAVILY_SCHEMA","Select the custom tool identifier: TAVILY_SEARCH_API.TAVILY_SCHEMA.TAVILY_WEB_SEARCH","Give your tool a descriptive name","Configure the following parameters with their descriptions:\n\n\nquery: “Search query”\n\n\nsearch_depth: “The depth of the search. It can be ‘basic’ or ‘advanced’”\n\n\nmax_results: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”","query: “Search query”","search_depth: “The depth of the search. It can be ‘basic’ or ‘advanced’”","max_results: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”","Click on Add to attach the tool to your agent","Make sure to click on Save in the top right corner to update the agent","Use the Agent: In the Snowsight UI sidebar, navigate to the Snowflake Intelligence landing page under AI & ML, select the agent you created, and use the tool."]}
    - {"type":"ul","items":["Select the Resource type as Procedure","Select the database and schema: TAVILY_SEARCH_API.TAVILY_SCHEMA","Select the custom tool identifier: TAVILY_SEARCH_API.TAVILY_SCHEMA.TAVILY_WEB_SEARCH","Give your tool a descriptive name","Configure the following parameters with their descriptions:\n\n\nquery: “Search query”\n\n\nsearch_depth: “The depth of the search. It can be ‘basic’ or ‘advanced’”\n\n\nmax_results: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”","query: “Search query”","search_depth: “The depth of the search. It can be ‘basic’ or ‘advanced’”","max_results: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”","Click on Add to attach the tool to your agent","Make sure to click on Save in the top right corner to update the agent"]}
    - {"type":"ul","items":["query: “Search query”","search_depth: “The depth of the search. It can be ‘basic’ or ‘advanced’”","max_results: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"CALL TAVILY_SCHEMA.TAVILY_WEB_SEARCH('latest Quantum computing trends', 'advanced', 10);"}
    - {"language":"text","code":"CALL TAVILY_SCHEMA.TAVILY_WEB_SEARCH('latest Quantum computing trends', 'advanced', 10);"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Snowflake_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Snowflake_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Snowflake_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Snowflake_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
  charts:
    - {"type":"svg","index":1,"filename":"Snowflake_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Snowflake_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":5,"filename":"Snowflake_-_Tavily_Docs/svg_5.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Snowflake_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Snowflake_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Snowflake_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Snowflake_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Snowflake_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Snowflake_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Snowflake_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Snowflake_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Snowflake_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Snowflake_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Snowflake_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Snowflake_-_Tavily_Docs/svg_25.png","width":14,"height":12}
    - {"type":"svg","index":26,"filename":"Snowflake_-_Tavily_Docs/svg_26.png","width":14,"height":12}
    - {"type":"svg","index":27,"filename":"Snowflake_-_Tavily_Docs/svg_27.png","width":16,"height":16}
    - {"type":"svg","index":28,"filename":"Snowflake_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Snowflake_-_Tavily_Docs/svg_29.png","width":14,"height":12}
    - {"type":"svg","index":30,"filename":"Snowflake_-_Tavily_Docs/svg_30.png","width":14,"height":14}
    - {"type":"svg","index":31,"filename":"Snowflake_-_Tavily_Docs/svg_31.png","width":14,"height":14}
    - {"type":"svg","index":32,"filename":"Snowflake_-_Tavily_Docs/svg_32.png","width":14,"height":14}
    - {"type":"svg","index":37,"filename":"Snowflake_-_Tavily_Docs/svg_37.png","width":20,"height":20}
    - {"type":"svg","index":38,"filename":"Snowflake_-_Tavily_Docs/svg_38.png","width":20,"height":20}
    - {"type":"svg","index":39,"filename":"Snowflake_-_Tavily_Docs/svg_39.png","width":20,"height":20}
    - {"type":"svg","index":40,"filename":"Snowflake_-_Tavily_Docs/svg_40.png","width":20,"height":20}
    - {"type":"svg","index":41,"filename":"Snowflake_-_Tavily_Docs/svg_41.png","width":49,"height":14}
    - {"type":"svg","index":42,"filename":"Snowflake_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Snowflake_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"Snowflake_-_Tavily_Docs/svg_44.png","width":16,"height":16}
    - {"type":"svg","index":45,"filename":"Snowflake_-_Tavily_Docs/svg_45.png","width":20,"height":20}
    - {"type":"svg","index":46,"filename":"Snowflake_-_Tavily_Docs/svg_46.png","width":14,"height":14}
    - {"type":"svg","index":47,"filename":"Snowflake_-_Tavily_Docs/svg_47.png","width":16,"height":16}
    - {"type":"svg","index":48,"filename":"Snowflake_-_Tavily_Docs/svg_48.png","width":14,"height":14}
    - {"type":"svg","index":49,"filename":"Snowflake_-_Tavily_Docs/svg_49.png","width":14,"height":14}
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

# Snowflake

## 源URL

https://docs.tavily.com/documentation/partnerships/snowflake

## 描述

Tavily is now available as a native app on the Snowflake Marketplace.

## 内容

### Introduction

### Tutorial

### Installation and Setup

1. After logging into your Snowflake account, click on *Marketplace* from the sidebar.
2. In the search bar, search for *Tavily* and find the *Tavily Search API* app.
3. Click on *GET* in the right top side to download the app into your Snowflake account.
4. Read through the permissions and click on *Agree and Continue* and click on *GET*.
5. After the app finished downloading, hover over *Catalog* in the left sidebar and click on *Apps*.
6. Locate the Tavily app named *Tavily Search API* in the installed apps section.
7. Now you have to configure the application.
8. Visit [https://tavily.com](https://tavily.com/) to get your API key if you don’t already have one.
9. After you have your API key, click on the *Configure* button and pass the API key in the secret value box to configure the API key for your native app.
10. Now, in the *Review integration requests* section, click on *Review* and toggle the button to the right to enable your app *Access the Tavily external API for web search*.
11. Click on *Save*. Now you have successfully configured your application for use in the Snowflake environment.
12. Click on *Next* to visit the app page.

### Use cases

#### Using TAVILY_WEB_SEARCH in Snowsight

1. After installation in the app page, you can click on *Open Worksheet* to pop up a Snowflake worksheet with a pre-loaded SQL query to use Tavily web search.
2. Make sure to select the appropriate database for your worksheet. In the top right, ensure the database is `TAVILY_SEARCH_API` and the schema is `TAVILY_SCHEMA`.
3. Now you can click the *Run* button on the top left of your worksheet to run the query.

- `QUERY` (VARCHAR): The search query in natural language
- `SEARCH_DEPTH` (VARCHAR, optional): `'basic'` (default) or `'advanced'`
- `MAX_RESULTS` (INTEGER, optional): Maximum number of results (default: 5)

```text
CALL TAVILY_SCHEMA.TAVILY_WEB_SEARCH('latest Quantum computing trends', 'advanced', 10);
```

#### Using TAVILY_WEB_SEARCH in Snowflake Intelligence

1. **Set up Snowflake Intelligence**: Follow the [Snowflake documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence) to set up Snowflake Intelligence. Make sure you have the snowflake_intelligence database, required schema and GRANTs before proceeding to the next steps.
2. **Create an Agent**: In the Snowsight UI sidebar, navigate to the *Agents* admin page under *AI & ML*, click on *create agent* and provide agent object name, display name and create the agent.
3. **Add the TAVILY_WEB_SEARCH Custom Tool**: Within the current agent’s menu bar, navigate to the *Tools* section and click on *+Add* in Custom tools.

Select the Resource type as *Procedure*

Select the database and schema: `TAVILY_SEARCH_API.TAVILY_SCHEMA`

Select the custom tool identifier: `TAVILY_SEARCH_API.TAVILY_SCHEMA.TAVILY_WEB_SEARCH`

Give your tool a descriptive name

Configure the following parameters with their descriptions:

`query`: “Search query”

`search_depth`: “The depth of the search. It can be ‘basic’ or ‘advanced’”

`max_results`: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”

Click on *Add* to attach the tool to your agent

Make sure to click on *Save* in the top right corner to update the agent
4. Select the Resource type as *Procedure*
5. Select the database and schema: `TAVILY_SEARCH_API.TAVILY_SCHEMA`
6. Select the custom tool identifier: `TAVILY_SEARCH_API.TAVILY_SCHEMA.TAVILY_WEB_SEARCH`
7. Give your tool a descriptive name
8. Configure the following parameters with their descriptions:

`query`: “Search query”

`search_depth`: “The depth of the search. It can be ‘basic’ or ‘advanced’”

`max_results`: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”
9. `query`: “Search query”
10. `search_depth`: “The depth of the search. It can be ‘basic’ or ‘advanced’”
11. `max_results`: “The maximum number of search results to return. Minimum is 1 and Maximum is 20”
12. Click on *Add* to attach the tool to your agent
13. Make sure to click on *Save* in the top right corner to update the agent
14. **Use the Agent**: In the Snowsight UI sidebar, navigate to the *Snowflake Intelligence* landing page under *AI & ML*, select the agent you created, and use the tool.

## 图片

![light logo](Snowflake_-_Tavily_Docs/image_1.svg)

![dark logo](Snowflake_-_Tavily_Docs/image_2.svg)

![light logo](Snowflake_-_Tavily_Docs/image_3.svg)

![dark logo](Snowflake_-_Tavily_Docs/image_4.svg)

## 图表

![SVG图表 1](Snowflake_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Snowflake_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 5](Snowflake_-_Tavily_Docs/svg_5.png)
*尺寸: 14x16px*

![SVG图表 11](Snowflake_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Snowflake_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Snowflake_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Snowflake_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Snowflake_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Snowflake_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Snowflake_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Snowflake_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Snowflake_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Snowflake_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Snowflake_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Snowflake_-_Tavily_Docs/svg_25.png)
*尺寸: 14x12px*

![SVG图表 26](Snowflake_-_Tavily_Docs/svg_26.png)
*尺寸: 14x12px*

![SVG图表 27](Snowflake_-_Tavily_Docs/svg_27.png)
*尺寸: 16x16px*

![SVG图表 28](Snowflake_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Snowflake_-_Tavily_Docs/svg_29.png)
*尺寸: 14x12px*

![SVG图表 30](Snowflake_-_Tavily_Docs/svg_30.png)
*尺寸: 14x14px*

![SVG图表 31](Snowflake_-_Tavily_Docs/svg_31.png)
*尺寸: 14x14px*

![SVG图表 32](Snowflake_-_Tavily_Docs/svg_32.png)
*尺寸: 14x14px*

![SVG图表 37](Snowflake_-_Tavily_Docs/svg_37.png)
*尺寸: 20x20px*

![SVG图表 38](Snowflake_-_Tavily_Docs/svg_38.png)
*尺寸: 20x20px*

![SVG图表 39](Snowflake_-_Tavily_Docs/svg_39.png)
*尺寸: 20x20px*

![SVG图表 40](Snowflake_-_Tavily_Docs/svg_40.png)
*尺寸: 20x20px*

![SVG图表 41](Snowflake_-_Tavily_Docs/svg_41.png)
*尺寸: 49x14px*

![SVG图表 42](Snowflake_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](Snowflake_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](Snowflake_-_Tavily_Docs/svg_44.png)
*尺寸: 16x16px*

![SVG图表 45](Snowflake_-_Tavily_Docs/svg_45.png)
*尺寸: 20x20px*

![SVG图表 46](Snowflake_-_Tavily_Docs/svg_46.png)
*尺寸: 14x14px*

![SVG图表 47](Snowflake_-_Tavily_Docs/svg_47.png)
*尺寸: 16x16px*

![SVG图表 48](Snowflake_-_Tavily_Docs/svg_48.png)
*尺寸: 14x14px*

![SVG图表 49](Snowflake_-_Tavily_Docs/svg_49.png)
*尺寸: 14x14px*
