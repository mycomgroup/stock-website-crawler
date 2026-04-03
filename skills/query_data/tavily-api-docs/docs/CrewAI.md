---
id: "url-1ff80f87"
type: "website"
title: "CrewAI"
url: "https://docs.tavily.com/documentation/integrations/crewai"
description: "Integrate Tavily with CrewAI to build powerful AI agents that can search the web."
source: ""
tags: []
crawl_time: "2026-03-18T02:59:35.180Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"CrewAI"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#introduction)Introduction"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#prerequisites)Prerequisites"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#installation)Installation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#setup)Setup"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#using-tavily-search-with-crewai)Using Tavily Search with CrewAI"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#customizing-search-tool-parameters)Customizing search tool parameters"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#using-tavily-extract-with-crewai)Using Tavily Extract with CrewAI"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/crewai#customizing-extract-tool-parameters)Customizing extract tool parameters"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#prerequisites)Prerequisites"}
    - {"type":"list","listType":"ul","items":["An OpenAI API key from [OpenAI Platform](https://platform.openai.com/)","A Tavily API key from [Tavily Dashboard](https://app.tavily.com/sign-in)"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#installation)Installation"}
    - {"type":"blockquote","content":"Note: The stable python versions to use with CrewAI are Python >=3.10 and Python <3.13 ."}
    - {"type":"codeblock","language":"","content":"pip install 'crewai[tools]'\npip install pydantic"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#setup)Setup"}
    - {"type":"codeblock","language":"","content":"import os\n\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#using-tavily-search-with-crewai)Using Tavily Search with CrewAI"}
    - {"type":"codeblock","language":"","content":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilySearchTool"}
    - {"type":"codeblock","language":"","content":"# Initialize the Tavily search tool\ntavily_tool = TavilySearchTool()"}
    - {"type":"codeblock","language":"","content":"# Create an agent that uses the tool\nresearcher = Agent(\n    role='News Researcher',\n    goal='Find trending information about AI agents',\n    backstory='An expert News researcher specializing in technology, focused on AI.',\n    tools=[tavily_tool],\n    verbose=True\n)"}
    - {"type":"codeblock","language":"","content":"# Create a task for the agent\nresearch_task = Task(\n    description='Search for the top 3 Agentic AI trends in 2025.',\n    expected_output='A JSON report summarizing the top 3 AI trends found.',\n    agent=researcher\n)"}
    - {"type":"codeblock","language":"","content":"# Form the crew and execute the task\ncrew = Crew(\n    agents=[researcher],\n    tasks=[research_task],\n    verbose=True\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#customizing-search-tool-parameters)Customizing search tool parameters"}
    - {"type":"codeblock","language":"","content":"from crewai_tools import TavilySearchTool\n\n# You can configure the tool with specific parameters\ntavily_search_tool = TavilySearchTool(\n    search_depth=\"advanced\",\n    max_results=10,\n    include_answer=True\n)"}
    - {"type":"list","listType":"ul","items":["`query` (str): Required. The search query string.","`search_depth` (Literal[“basic”, “advanced”], optional): The depth of the search. Defaults to “basic”.","`topic` (Literal[“general”, “news”, “finance”], optional): The topic to focus the search on. Defaults to “general”.","`time_range` (Literal[“day”, “week”, “month”, “year”], optional): The time range for the search. Defaults to None.","`max_results` (int, optional): The maximum number of search results to return. Defaults to 5.","`include_domains` (Sequence[str], optional): A list of domains to prioritize in the search. Defaults to None.","`exclude_domains` (Sequence[str], optional): A list of domains to exclude from the search. Defaults to None.","`include_answer` (Union[bool, Literal[“basic”, “advanced”]], optional): Whether to include a direct answer synthesized from the search results. Defaults to False.","`include_raw_content` (bool, optional): Whether to include the raw HTML content of the searched pages. Defaults to False.","`include_images` (bool, optional): Whether to include image results. Defaults to False.","`timeout` (int, optional): The request timeout in seconds. Defaults to 60."]}
    - {"type":"blockquote","content":"Explore More Parameters: For a complete list of available parameters and their descriptions, visit our API documentation to discover all the customization options available for search operations."}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#using-tavily-extract-with-crewai)Using Tavily Extract with CrewAI"}
    - {"type":"codeblock","language":"","content":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilyExtractorTool"}
    - {"type":"codeblock","language":"","content":"# Initialize the Tavily extractor tool\ntavily_tool = TavilyExtractorTool()"}
    - {"type":"codeblock","language":"","content":"# Create an agent that uses the tool\nextractor_agent = Agent(\n    role='Web Page Content Extractor',\n    goal='Extract key information from the given web pages',\n    backstory='You are an expert at extracting relevant content from websites using the Tavily Extract.',\n    tools=[tavily_tool],\n    verbose=True\n)"}
    - {"type":"codeblock","language":"","content":"# Define a task for the agent\nextract_task = Task(\n    description='Extract the main content from the URL https://en.wikipedia.org/wiki/Lionel_Messi .',\n    expected_output='A JSON string containing the extracted content from the URL.',\n    agent=extractor_agent\n)"}
    - {"type":"codeblock","language":"","content":"# Create and run the crew\ncrew = Crew(\n    agents=[extractor_agent],\n    tasks=[extract_task],\n    verbose=False\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/crewai#customizing-extract-tool-parameters)Customizing extract tool parameters"}
    - {"type":"codeblock","language":"","content":"from crewai_tools import TavilyExtractorTool\n\n# You can configure the tool with specific parameters\ntavily_extract_tool = TavilyExtractorTool(\n    extract_depth=\"advanced\",\n    include_images=True,\n    timeout=45\n)"}
    - {"type":"list","listType":"ul","items":["`urls` (Union[List[str], str]): Required. A single URL string or a list of URL strings to extract data from.","`include_images` (Optional[bool]): Whether to include images in the extraction results. Defaults to False.","`extract_depth` (Literal[“basic”, “advanced”]): The depth of extraction. Use “basic” for faster, surface-level extraction or “advanced” for more comprehensive extraction. Defaults to “basic”.","`timeout` (int): The maximum time in seconds to wait for the extraction request to complete. Defaults to 60."]}
    - {"type":"blockquote","content":"Explore More Parameters: For a complete list of available parameters and their descriptions, visit our API documentation to discover all the customization options available for extract operations."}
  paragraphs:
    - "Full Code Example - Search"
    - "Full Code Example - Extract"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/integrations/crewai#introduction)","[Prerequisites](https://docs.tavily.com/documentation/integrations/crewai#prerequisites)","[Installation](https://docs.tavily.com/documentation/integrations/crewai#installation)","[Setup](https://docs.tavily.com/documentation/integrations/crewai#setup)","[Using Tavily Search with CrewAI](https://docs.tavily.com/documentation/integrations/crewai#using-tavily-search-with-crewai)","[Customizing search tool parameters](https://docs.tavily.com/documentation/integrations/crewai#customizing-search-tool-parameters)","[Using Tavily Extract with CrewAI](https://docs.tavily.com/documentation/integrations/crewai#using-tavily-extract-with-crewai)","[Customizing extract tool parameters](https://docs.tavily.com/documentation/integrations/crewai#customizing-extract-tool-parameters)"]}
    - {"type":"ul","items":["An OpenAI API key from [OpenAI Platform](https://platform.openai.com/)","A Tavily API key from [Tavily Dashboard](https://app.tavily.com/sign-in)"]}
    - {"type":"ul","items":["query (str): Required. The search query string.","search_depth (Literal[“basic”, “advanced”], optional): The depth of the search. Defaults to “basic”.","topic (Literal[“general”, “news”, “finance”], optional): The topic to focus the search on. Defaults to “general”.","time_range (Literal[“day”, “week”, “month”, “year”], optional): The time range for the search. Defaults to None.","max_results (int, optional): The maximum number of search results to return. Defaults to 5.","include_domains (Sequence[str], optional): A list of domains to prioritize in the search. Defaults to None.","exclude_domains (Sequence[str], optional): A list of domains to exclude from the search. Defaults to None.","include_answer (Union[bool, Literal[“basic”, “advanced”]], optional): Whether to include a direct answer synthesized from the search results. Defaults to False.","include_raw_content (bool, optional): Whether to include the raw HTML content of the searched pages. Defaults to False.","include_images (bool, optional): Whether to include image results. Defaults to False.","timeout (int, optional): The request timeout in seconds. Defaults to 60."]}
    - {"type":"ul","items":["urls (Union[List[str], str]): Required. A single URL string or a list of URL strings to extract data from.","include_images (Optional[bool]): Whether to include images in the extraction results. Defaults to False.","extract_depth (Literal[“basic”, “advanced”]): The depth of extraction. Use “basic” for faster, surface-level extraction or “advanced” for more comprehensive extraction. Defaults to “basic”.","timeout (int): The maximum time in seconds to wait for the extraction request to complete. Defaults to 60."]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install 'crewai[tools]'\npip install pydantic"}
    - {"language":"text","code":"pip install 'crewai[tools]'\npip install pydantic"}
    - {"language":"text","code":"import os\n\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"language":"text","code":"import os\n\n# Set your API keys\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\""}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilySearchTool"}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilySearchTool"}
    - {"language":"text","code":"# Initialize the Tavily search tool\ntavily_tool = TavilySearchTool()"}
    - {"language":"text","code":"# Initialize the Tavily search tool\ntavily_tool = TavilySearchTool()"}
    - {"language":"text","code":"# Create an agent that uses the tool\nresearcher = Agent(\n    role='News Researcher',\n    goal='Find trending information about AI agents',\n    backstory='An expert News researcher specializing in technology, focused on AI.',\n    tools=[tavily_tool],\n    verbose=True\n)"}
    - {"language":"text","code":"# Create an agent that uses the tool\nresearcher = Agent(\n    role='News Researcher',\n    goal='Find trending information about AI agents',\n    backstory='An expert News researcher specializing in technology, focused on AI.',\n    tools=[tavily_tool],\n    verbose=True\n)"}
    - {"language":"text","code":"# Create a task for the agent\nresearch_task = Task(\n    description='Search for the top 3 Agentic AI trends in 2025.',\n    expected_output='A JSON report summarizing the top 3 AI trends found.',\n    agent=researcher\n)"}
    - {"language":"text","code":"# Create a task for the agent\nresearch_task = Task(\n    description='Search for the top 3 Agentic AI trends in 2025.',\n    expected_output='A JSON report summarizing the top 3 AI trends found.',\n    agent=researcher\n)"}
    - {"language":"text","code":"# Form the crew and execute the task\ncrew = Crew(\n    agents=[researcher],\n    tasks=[research_task],\n    verbose=True\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"language":"text","code":"# Form the crew and execute the task\ncrew = Crew(\n    agents=[researcher],\n    tasks=[research_task],\n    verbose=True\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"language":"text","code":"from crewai_tools import TavilySearchTool\n\n# You can configure the tool with specific parameters\ntavily_search_tool = TavilySearchTool(\n    search_depth=\"advanced\",\n    max_results=10,\n    include_answer=True\n)"}
    - {"language":"text","code":"from crewai_tools import TavilySearchTool\n\n# You can configure the tool with specific parameters\ntavily_search_tool = TavilySearchTool(\n    search_depth=\"advanced\",\n    max_results=10,\n    include_answer=True\n)"}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilySearchTool\n\n# Set up environment variables\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\"\n\n# Initialize the tool\ntavily_tool = TavilySearchTool()\n\n# Create an agent that uses the tool\nresearcher = Agent(\n    role='News Researcher',\n    goal='Find trending information about AI agents',\n    backstory='An expert News researcher specializing in technology, focused on AI.',\n    tools=[tavily_tool],\n    verbose=True\n)\n\n# Create a task for the agent\nresearch_task = Task(\n    description='Search for the top 3 Agentic AI trends in 2025.',\n    expected_output='A JSON report summarizing the top 3 AI trends found.',\n    agent=researcher\n)\n\n# Form the crew and kick it off\ncrew = Crew(\n    agents=[researcher],\n    tasks=[research_task],\n    verbose=True\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilySearchTool\n\n# Set up environment variables\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\"\n\n# Initialize the tool\ntavily_tool = TavilySearchTool()\n\n# Create an agent that uses the tool\nresearcher = Agent(\n    role='News Researcher',\n    goal='Find trending information about AI agents',\n    backstory='An expert News researcher specializing in technology, focused on AI.',\n    tools=[tavily_tool],\n    verbose=True\n)\n\n# Create a task for the agent\nresearch_task = Task(\n    description='Search for the top 3 Agentic AI trends in 2025.',\n    expected_output='A JSON report summarizing the top 3 AI trends found.',\n    agent=researcher\n)\n\n# Form the crew and kick it off\ncrew = Crew(\n    agents=[researcher],\n    tasks=[research_task],\n    verbose=True\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilyExtractorTool"}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilyExtractorTool"}
    - {"language":"text","code":"# Initialize the Tavily extractor tool\ntavily_tool = TavilyExtractorTool()"}
    - {"language":"text","code":"# Initialize the Tavily extractor tool\ntavily_tool = TavilyExtractorTool()"}
    - {"language":"text","code":"# Create an agent that uses the tool\nextractor_agent = Agent(\n    role='Web Page Content Extractor',\n    goal='Extract key information from the given web pages',\n    backstory='You are an expert at extracting relevant content from websites using the Tavily Extract.',\n    tools=[tavily_tool],\n    verbose=True\n)"}
    - {"language":"text","code":"# Create an agent that uses the tool\nextractor_agent = Agent(\n    role='Web Page Content Extractor',\n    goal='Extract key information from the given web pages',\n    backstory='You are an expert at extracting relevant content from websites using the Tavily Extract.',\n    tools=[tavily_tool],\n    verbose=True\n)"}
    - {"language":"text","code":"# Define a task for the agent\nextract_task = Task(\n    description='Extract the main content from the URL https://en.wikipedia.org/wiki/Lionel_Messi .',\n    expected_output='A JSON string containing the extracted content from the URL.',\n    agent=extractor_agent\n)"}
    - {"language":"text","code":"# Define a task for the agent\nextract_task = Task(\n    description='Extract the main content from the URL https://en.wikipedia.org/wiki/Lionel_Messi .',\n    expected_output='A JSON string containing the extracted content from the URL.',\n    agent=extractor_agent\n)"}
    - {"language":"text","code":"# Create and run the crew\ncrew = Crew(\n    agents=[extractor_agent],\n    tasks=[extract_task],\n    verbose=False\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"language":"text","code":"# Create and run the crew\ncrew = Crew(\n    agents=[extractor_agent],\n    tasks=[extract_task],\n    verbose=False\n)\n\nresult = crew.kickoff()\nprint(result)"}
    - {"language":"text","code":"from crewai_tools import TavilyExtractorTool\n\n# You can configure the tool with specific parameters\ntavily_extract_tool = TavilyExtractorTool(\n    extract_depth=\"advanced\",\n    include_images=True,\n    timeout=45\n)"}
    - {"language":"text","code":"from crewai_tools import TavilyExtractorTool\n\n# You can configure the tool with specific parameters\ntavily_extract_tool = TavilyExtractorTool(\n    extract_depth=\"advanced\",\n    include_images=True,\n    timeout=45\n)"}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilyExtractorTool\n\n# Set up environment variables\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\"\n\n# Initialize the Tavily extractor tool\ntavily_tool = TavilyExtractorTool()\n\n# Create an agent that uses the tool\nextractor_agent = Agent(\n    role='Web Page Content Extractor',\n    goal='Extract key information from the given web pages',\n    backstory='You are an expert at extracting relevant content from websites using the Tavily Extract.',\n    tools=[tavily_tool],\n    verbose=True\n)\n\n# Define a task for the agent\nextract_task = Task(\n    description='Extract the main content from the URL https://en.wikipedia.org/wiki/Lionel_Messi .',\n    expected_output='A JSON string containing the extracted content from the URL.',\n    agent=extractor_agent\n)\n\n# Create and execute the crew\ncrew = Crew(\n    agents=[extractor_agent],\n    tasks=[extract_task],\n    verbose=True\n)\n\n# Run the extraction\nresult = crew.kickoff()\nprint(\"Extraction Results:\")\nprint(result)"}
    - {"language":"text","code":"import os\nfrom crewai import Agent, Task, Crew\nfrom crewai_tools import TavilyExtractorTool\n\n# Set up environment variables\nos.environ[\"OPENAI_API_KEY\"] = \"your-openai-api-key\"\nos.environ[\"TAVILY_API_KEY\"] = \"your-tavily-api-key\"\n\n# Initialize the Tavily extractor tool\ntavily_tool = TavilyExtractorTool()\n\n# Create an agent that uses the tool\nextractor_agent = Agent(\n    role='Web Page Content Extractor',\n    goal='Extract key information from the given web pages',\n    backstory='You are an expert at extracting relevant content from websites using the Tavily Extract.',\n    tools=[tavily_tool],\n    verbose=True\n)\n\n# Define a task for the agent\nextract_task = Task(\n    description='Extract the main content from the URL https://en.wikipedia.org/wiki/Lionel_Messi .',\n    expected_output='A JSON string containing the extracted content from the URL.',\n    agent=extractor_agent\n)\n\n# Create and execute the crew\ncrew = Crew(\n    agents=[extractor_agent],\n    tasks=[extract_task],\n    verbose=True\n)\n\n# Run the extraction\nresult = crew.kickoff()\nprint(\"Extraction Results:\")\nprint(result)"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"CrewAI_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"CrewAI_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"CrewAI_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"CrewAI_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"CrewAI_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"CrewAI_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"CrewAI_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"CrewAI_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"CrewAI_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"CrewAI_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"CrewAI_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"CrewAI_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"CrewAI_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"CrewAI_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"CrewAI_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"CrewAI_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"CrewAI_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"CrewAI_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"CrewAI_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"CrewAI_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"CrewAI_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"CrewAI_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"CrewAI_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":28,"filename":"CrewAI_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"CrewAI_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"CrewAI_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"CrewAI_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"CrewAI_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"CrewAI_-_Tavily_Docs/svg_33.png","width":16,"height":16}
    - {"type":"svg","index":34,"filename":"CrewAI_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"CrewAI_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"CrewAI_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"CrewAI_-_Tavily_Docs/svg_37.png","width":16,"height":16}
    - {"type":"svg","index":38,"filename":"CrewAI_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"CrewAI_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"CrewAI_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"CrewAI_-_Tavily_Docs/svg_41.png","width":14,"height":12}
    - {"type":"svg","index":42,"filename":"CrewAI_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"CrewAI_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"CrewAI_-_Tavily_Docs/svg_44.png","width":12,"height":12}
    - {"type":"svg","index":45,"filename":"CrewAI_-_Tavily_Docs/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"CrewAI_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"CrewAI_-_Tavily_Docs/svg_47.png","width":14,"height":12}
    - {"type":"svg","index":48,"filename":"CrewAI_-_Tavily_Docs/svg_48.png","width":16,"height":16}
    - {"type":"svg","index":49,"filename":"CrewAI_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"CrewAI_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"CrewAI_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"CrewAI_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"CrewAI_-_Tavily_Docs/svg_53.png","width":16,"height":16}
    - {"type":"svg","index":54,"filename":"CrewAI_-_Tavily_Docs/svg_54.png","width":16,"height":16}
    - {"type":"svg","index":55,"filename":"CrewAI_-_Tavily_Docs/svg_55.png","width":16,"height":16}
    - {"type":"svg","index":56,"filename":"CrewAI_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"CrewAI_-_Tavily_Docs/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"CrewAI_-_Tavily_Docs/svg_58.png","width":14,"height":12}
    - {"type":"svg","index":59,"filename":"CrewAI_-_Tavily_Docs/svg_59.png","width":16,"height":16}
    - {"type":"svg","index":60,"filename":"CrewAI_-_Tavily_Docs/svg_60.png","width":16,"height":16}
    - {"type":"svg","index":61,"filename":"CrewAI_-_Tavily_Docs/svg_61.png","width":12,"height":12}
    - {"type":"svg","index":62,"filename":"CrewAI_-_Tavily_Docs/svg_62.png","width":16,"height":16}
    - {"type":"svg","index":63,"filename":"CrewAI_-_Tavily_Docs/svg_63.png","width":16,"height":16}
    - {"type":"svg","index":64,"filename":"CrewAI_-_Tavily_Docs/svg_64.png","width":14,"height":14}
    - {"type":"svg","index":65,"filename":"CrewAI_-_Tavily_Docs/svg_65.png","width":14,"height":14}
    - {"type":"svg","index":66,"filename":"CrewAI_-_Tavily_Docs/svg_66.png","width":14,"height":14}
    - {"type":"svg","index":71,"filename":"CrewAI_-_Tavily_Docs/svg_71.png","width":20,"height":20}
    - {"type":"svg","index":72,"filename":"CrewAI_-_Tavily_Docs/svg_72.png","width":20,"height":20}
    - {"type":"svg","index":73,"filename":"CrewAI_-_Tavily_Docs/svg_73.png","width":20,"height":20}
    - {"type":"svg","index":74,"filename":"CrewAI_-_Tavily_Docs/svg_74.png","width":20,"height":20}
    - {"type":"svg","index":75,"filename":"CrewAI_-_Tavily_Docs/svg_75.png","width":49,"height":14}
    - {"type":"svg","index":76,"filename":"CrewAI_-_Tavily_Docs/svg_76.png","width":16,"height":16}
    - {"type":"svg","index":77,"filename":"CrewAI_-_Tavily_Docs/svg_77.png","width":16,"height":16}
    - {"type":"svg","index":78,"filename":"CrewAI_-_Tavily_Docs/svg_78.png","width":16,"height":16}
    - {"type":"svg","index":88,"filename":"CrewAI_-_Tavily_Docs/svg_88.png","width":16,"height":16}
    - {"type":"svg","index":89,"filename":"CrewAI_-_Tavily_Docs/svg_89.png","width":14,"height":14}
    - {"type":"svg","index":90,"filename":"CrewAI_-_Tavily_Docs/svg_90.png","width":16,"height":16}
    - {"type":"svg","index":91,"filename":"CrewAI_-_Tavily_Docs/svg_91.png","width":12,"height":12}
    - {"type":"svg","index":92,"filename":"CrewAI_-_Tavily_Docs/svg_92.png","width":14,"height":14}
    - {"type":"svg","index":93,"filename":"CrewAI_-_Tavily_Docs/svg_93.png","width":16,"height":16}
    - {"type":"svg","index":94,"filename":"CrewAI_-_Tavily_Docs/svg_94.png","width":12,"height":12}
    - {"type":"svg","index":95,"filename":"CrewAI_-_Tavily_Docs/svg_95.png","width":14,"height":14}
    - {"type":"svg","index":96,"filename":"CrewAI_-_Tavily_Docs/svg_96.png","width":16,"height":16}
    - {"type":"svg","index":97,"filename":"CrewAI_-_Tavily_Docs/svg_97.png","width":12,"height":12}
    - {"type":"svg","index":98,"filename":"CrewAI_-_Tavily_Docs/svg_98.png","width":14,"height":14}
  chartData: []
  blockquotes:
    - "Note: The stable python versions to use with CrewAI are Python >=3.10 and Python <3.13 ."
    - "Explore More Parameters: For a complete list of available parameters and their descriptions, visit our API documentation to discover all the customization options available for search operations."
    - "Explore More Parameters: For a complete list of available parameters and their descriptions, visit our API documentation to discover all the customization options available for extract operations."
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

# CrewAI

## 源URL

https://docs.tavily.com/documentation/integrations/crewai

## 描述

Integrate Tavily with CrewAI to build powerful AI agents that can search the web.

## 内容

### Introduction

### Prerequisites

- An OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
- A Tavily API key from [Tavily Dashboard](https://app.tavily.com/sign-in)

### Installation

> Note: The stable python versions to use with CrewAI are Python >=3.10 and Python <3.13 .

```text
pip install 'crewai[tools]'
pip install pydantic
```

### Setup

```text
import os

# Set your API keys
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["TAVILY_API_KEY"] = "your-tavily-api-key"
```

### Using Tavily Search with CrewAI

```text
import os
from crewai import Agent, Task, Crew
from crewai_tools import TavilySearchTool
```

```text
# Initialize the Tavily search tool
tavily_tool = TavilySearchTool()
```

```text
# Create an agent that uses the tool
researcher = Agent(
    role='News Researcher',
    goal='Find trending information about AI agents',
    backstory='An expert News researcher specializing in technology, focused on AI.',
    tools=[tavily_tool],
    verbose=True
)
```

```text
# Create a task for the agent
research_task = Task(
    description='Search for the top 3 Agentic AI trends in 2025.',
    expected_output='A JSON report summarizing the top 3 AI trends found.',
    agent=researcher
)
```

```text
# Form the crew and execute the task
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

#### Customizing search tool parameters

```text
from crewai_tools import TavilySearchTool

# You can configure the tool with specific parameters
tavily_search_tool = TavilySearchTool(
    search_depth="advanced",
    max_results=10,
    include_answer=True
)
```

- `query` (str): Required. The search query string.
- `search_depth` (Literal[“basic”, “advanced”], optional): The depth of the search. Defaults to “basic”.
- `topic` (Literal[“general”, “news”, “finance”], optional): The topic to focus the search on. Defaults to “general”.
- `time_range` (Literal[“day”, “week”, “month”, “year”], optional): The time range for the search. Defaults to None.
- `max_results` (int, optional): The maximum number of search results to return. Defaults to 5.
- `include_domains` (Sequence[str], optional): A list of domains to prioritize in the search. Defaults to None.
- `exclude_domains` (Sequence[str], optional): A list of domains to exclude from the search. Defaults to None.
- `include_answer` (Union[bool, Literal[“basic”, “advanced”]], optional): Whether to include a direct answer synthesized from the search results. Defaults to False.
- `include_raw_content` (bool, optional): Whether to include the raw HTML content of the searched pages. Defaults to False.
- `include_images` (bool, optional): Whether to include image results. Defaults to False.
- `timeout` (int, optional): The request timeout in seconds. Defaults to 60.

> Explore More Parameters: For a complete list of available parameters and their descriptions, visit our API documentation to discover all the customization options available for search operations.

### Using Tavily Extract with CrewAI

```text
import os
from crewai import Agent, Task, Crew
from crewai_tools import TavilyExtractorTool
```

```text
# Initialize the Tavily extractor tool
tavily_tool = TavilyExtractorTool()
```

```text
# Create an agent that uses the tool
extractor_agent = Agent(
    role='Web Page Content Extractor',
    goal='Extract key information from the given web pages',
    backstory='You are an expert at extracting relevant content from websites using the Tavily Extract.',
    tools=[tavily_tool],
    verbose=True
)
```

```text
# Define a task for the agent
extract_task = Task(
    description='Extract the main content from the URL https://en.wikipedia.org/wiki/Lionel_Messi .',
    expected_output='A JSON string containing the extracted content from the URL.',
    agent=extractor_agent
)
```

```text
# Create and run the crew
crew = Crew(
    agents=[extractor_agent],
    tasks=[extract_task],
    verbose=False
)

result = crew.kickoff()
print(result)
```

#### Customizing extract tool parameters

```text
from crewai_tools import TavilyExtractorTool

# You can configure the tool with specific parameters
tavily_extract_tool = TavilyExtractorTool(
    extract_depth="advanced",
    include_images=True,
    timeout=45
)
```

- `urls` (Union[List[str], str]): Required. A single URL string or a list of URL strings to extract data from.
- `include_images` (Optional[bool]): Whether to include images in the extraction results. Defaults to False.
- `extract_depth` (Literal[“basic”, “advanced”]): The depth of extraction. Use “basic” for faster, surface-level extraction or “advanced” for more comprehensive extraction. Defaults to “basic”.
- `timeout` (int): The maximum time in seconds to wait for the extraction request to complete. Defaults to 60.

> Explore More Parameters: For a complete list of available parameters and their descriptions, visit our API documentation to discover all the customization options available for extract operations.

## 图片

![light logo](CrewAI_-_Tavily_Docs/image_1.svg)

![dark logo](CrewAI_-_Tavily_Docs/image_2.svg)

![light logo](CrewAI_-_Tavily_Docs/image_3.svg)

![dark logo](CrewAI_-_Tavily_Docs/image_4.svg)

![tavily-logo](CrewAI_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](CrewAI_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](CrewAI_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](CrewAI_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](CrewAI_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](CrewAI_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](CrewAI_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](CrewAI_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](CrewAI_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](CrewAI_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](CrewAI_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](CrewAI_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](CrewAI_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](CrewAI_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](CrewAI_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](CrewAI_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](CrewAI_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](CrewAI_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](CrewAI_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 28](CrewAI_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](CrewAI_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](CrewAI_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](CrewAI_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](CrewAI_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](CrewAI_-_Tavily_Docs/svg_33.png)
*尺寸: 16x16px*

![SVG图表 34](CrewAI_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](CrewAI_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](CrewAI_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](CrewAI_-_Tavily_Docs/svg_37.png)
*尺寸: 16x16px*

![SVG图表 38](CrewAI_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](CrewAI_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](CrewAI_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](CrewAI_-_Tavily_Docs/svg_41.png)
*尺寸: 14x12px*

![SVG图表 42](CrewAI_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](CrewAI_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](CrewAI_-_Tavily_Docs/svg_44.png)
*尺寸: 12x12px*

![SVG图表 45](CrewAI_-_Tavily_Docs/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](CrewAI_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](CrewAI_-_Tavily_Docs/svg_47.png)
*尺寸: 14x12px*

![SVG图表 48](CrewAI_-_Tavily_Docs/svg_48.png)
*尺寸: 16x16px*

![SVG图表 49](CrewAI_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](CrewAI_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](CrewAI_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 52](CrewAI_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](CrewAI_-_Tavily_Docs/svg_53.png)
*尺寸: 16x16px*

![SVG图表 54](CrewAI_-_Tavily_Docs/svg_54.png)
*尺寸: 16x16px*

![SVG图表 55](CrewAI_-_Tavily_Docs/svg_55.png)
*尺寸: 16x16px*

![SVG图表 56](CrewAI_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](CrewAI_-_Tavily_Docs/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](CrewAI_-_Tavily_Docs/svg_58.png)
*尺寸: 14x12px*

![SVG图表 59](CrewAI_-_Tavily_Docs/svg_59.png)
*尺寸: 16x16px*

![SVG图表 60](CrewAI_-_Tavily_Docs/svg_60.png)
*尺寸: 16x16px*

![SVG图表 61](CrewAI_-_Tavily_Docs/svg_61.png)
*尺寸: 12x12px*

![SVG图表 62](CrewAI_-_Tavily_Docs/svg_62.png)
*尺寸: 16x16px*

![SVG图表 63](CrewAI_-_Tavily_Docs/svg_63.png)
*尺寸: 16x16px*

![SVG图表 64](CrewAI_-_Tavily_Docs/svg_64.png)
*尺寸: 14x14px*

![SVG图表 65](CrewAI_-_Tavily_Docs/svg_65.png)
*尺寸: 14x14px*

![SVG图表 66](CrewAI_-_Tavily_Docs/svg_66.png)
*尺寸: 14x14px*

![SVG图表 71](CrewAI_-_Tavily_Docs/svg_71.png)
*尺寸: 20x20px*

![SVG图表 72](CrewAI_-_Tavily_Docs/svg_72.png)
*尺寸: 20x20px*

![SVG图表 73](CrewAI_-_Tavily_Docs/svg_73.png)
*尺寸: 20x20px*

![SVG图表 74](CrewAI_-_Tavily_Docs/svg_74.png)
*尺寸: 20x20px*

![SVG图表 75](CrewAI_-_Tavily_Docs/svg_75.png)
*尺寸: 49x14px*

![SVG图表 76](CrewAI_-_Tavily_Docs/svg_76.png)
*尺寸: 16x16px*

![SVG图表 77](CrewAI_-_Tavily_Docs/svg_77.png)
*尺寸: 16x16px*

![SVG图表 78](CrewAI_-_Tavily_Docs/svg_78.png)
*尺寸: 16x16px*

![SVG图表 88](CrewAI_-_Tavily_Docs/svg_88.png)
*尺寸: 16x16px*

![SVG图表 89](CrewAI_-_Tavily_Docs/svg_89.png)
*尺寸: 14x14px*

![SVG图表 90](CrewAI_-_Tavily_Docs/svg_90.png)
*尺寸: 16x16px*

![SVG图表 91](CrewAI_-_Tavily_Docs/svg_91.png)
*尺寸: 12x12px*

![SVG图表 92](CrewAI_-_Tavily_Docs/svg_92.png)
*尺寸: 14x14px*

![SVG图表 93](CrewAI_-_Tavily_Docs/svg_93.png)
*尺寸: 16x16px*

![SVG图表 94](CrewAI_-_Tavily_Docs/svg_94.png)
*尺寸: 12x12px*

![SVG图表 95](CrewAI_-_Tavily_Docs/svg_95.png)
*尺寸: 14x14px*

![SVG图表 96](CrewAI_-_Tavily_Docs/svg_96.png)
*尺寸: 16x16px*

![SVG图表 97](CrewAI_-_Tavily_Docs/svg_97.png)
*尺寸: 12x12px*

![SVG图表 98](CrewAI_-_Tavily_Docs/svg_98.png)
*尺寸: 14x14px*
