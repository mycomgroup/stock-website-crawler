---
id: "url-2b255cae"
type: "website"
title: "LangChain"
url: "https://docs.tavily.com/integrations/langchain"
description: "We're excited to partner with Langchain as their recommended search tool!"
source: ""
tags: []
crawl_time: "2026-03-18T04:23:58.929Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"LangChain"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#installation)Installation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#credentials)Credentials"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-search)Tavily Search"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters)Available Parameters"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation)Instantiation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args)Invoke directly with args"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation)Direct Tool Invocation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#use-with-agent)Use with Agent"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-extract)Tavily Extract"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-2)Available Parameters"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-2)Instantiation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args-2)Invoke directly with args"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-2)Direct Tool Invocation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-map/crawl)Tavily Map/Crawl"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-map)Tavily Map"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-3)Available Parameters"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-3)Instantiation"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-3)Direct Tool Invocation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-crawl)Tavily Crawl"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-4)Available Parameters"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-4)Instantiation"}
    - {"level":4,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-4)Direct Tool Invocation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-research)Tavily Research"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-5)Available Parameters"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-5)Instantiation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args-3)Invoke directly with args"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-5)Direct Tool Invocation"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-get-research)Tavily Get Research"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-6)Available Parameters"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-6)Instantiation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-6)Direct Tool Invocation"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"blockquote","content":"Warning: The langchain_community.tools.tavily_search.tool is deprecated. While it remains functional for now, we strongly recommend migrating to the new langchain-tavily Python package which supports Search, Extract, Map, and Crawl functionality and receives continuous updates with the latest features."}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#installation)Installation"}
    - {"type":"codeblock","language":"","content":"pip install -U langchain-tavily"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#credentials)Credentials"}
    - {"type":"codeblock","language":"","content":"import getpass\nimport os\n\nif not os.environ.get(\"TAVILY_API_KEY\"):\n    os.environ[\"TAVILY_API_KEY\"] = getpass.getpass(\"Tavily API key:\\n\")"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-search)Tavily Search"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters)Available Parameters"}
    - {"type":"list","listType":"ul","items":["`max_results` (optional, int): Maximum number of search results to return. Default is 5.","`topic` (optional, str): Category of the search. Can be “general”, “news”, or “finance”. Default is “general”.","`include_answer` (optional, bool): Include an answer to original query in results. Default is False.","`include_raw_content` (optional, bool): Include cleaned and parsed HTML of each search result. Default is False.","`include_images` (optional, bool): Include a list of query related images in the response. Default is False.","`include_image_descriptions` (optional, bool): Include descriptive text for each image. Default is False.","`search_depth` (optional, str): Depth of the search, either “basic” or “advanced”. Default is “basic”.","`time_range` (optional, str): The time range back from the current date ( publish date ) to filter results - “day”, “week”, “month”, or “year”. Default is None.","`start_date` (optional, str): Will return all results after the specified start date ( publish date ). Required to be written in the format YYYY-MM-DD. Default is None.","`end_date` (optional, str): Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD. Default is None.","`include_domains` (optional, List[str]): List of domains to specifically include. Maximum 300 domains. Default is None.","`exclude_domains` (optional, List[str]): List of domains to specifically exclude. Maximum 150 domains. Default is None.","`include_usage` (optional, bool): Whether to include credit usage information in the response. Default is False."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation)Instantiation"}
    - {"type":"codeblock","language":"","content":"from langchain_tavily import TavilySearch\n\ntool = TavilySearch(\n    max_results=5,\n    topic=\"general\",\n    # include_answer=False,\n    # include_raw_content=False,\n    # include_images=False,\n    # include_image_descriptions=False,\n    # search_depth=\"basic\",\n    # time_range=\"day\",\n    # start_date=None,\n    # end_date=None,\n    # include_domains=None,\n    # exclude_domains=None,\n    # include_usage= False\n)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args)Invoke directly with args"}
    - {"type":"list","listType":"ul","items":["`query` (required): A natural language search query","The following arguments can also be set during invocation: `include_images`, `search_depth`, `time_range`, `include_domains`, `exclude_domains`, `start_date`, `end_date`","For reliability and performance reasons, certain parameters that affect response size cannot be modified during invocation: `include_answer` and `include_raw_content`. These limitations prevent unexpected context window issues and ensure consistent results."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation)Direct Tool Invocation"}
    - {"type":"codeblock","language":"","content":"# Basic usage\nresult = tavily_search.invoke({\"query\": \"What happened at the last wimbledon\"})"}
    - {"type":"codeblock","language":"","content":"{\n 'query': 'What happened at the last wimbledon',\n 'follow_up_questions': None,\n 'answer': None,\n 'images': [],\n 'results': [\n   {'url': 'https://en.wikipedia.org/wiki/Wimbledon_Championships',\n    'title': 'Wimbledon Championships - Wikipedia',\n    'content': 'Due to the COVID-19 pandemic, Wimbledon 2020 was cancelled ...',\n    'score': 0.62365627198,\n    'raw_content': None},\n   {'url': 'https://www.cbsnews.com/news/wimbledon-men-final-carlos-alcaraz-novak-djokovic/',\n    'title': \"Carlos Alcaraz beats Novak Djokovic at Wimbledon men's final to ...\",\n    'content': 'In attendance on Sunday was Catherine, the Princess of Wales ...',\n    'score': 0.5154731446,\n    'raw_content': None}\n ],\n 'response_time': 2.3\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#use-with-agent)Use with Agent"}
    - {"type":"codeblock","language":"","content":"# !pip install -qU langchain langchain-openai langchain-tavily\nfrom langchain.agents import create_agent\nfrom langchain_openai import ChatOpenAI\nfrom langchain_tavily import TavilySearch\n\n# Initialize the Tavily Search tool\ntavily_search = TavilySearch(max_results=5, topic=\"general\")\n\n# Initialize the agent with the search tool\nagent = create_agent(\n    model=ChatOpenAI(model=\"gpt-5\"),\n    tools=[tavily_search],\n    system_prompt=\"You are a helpful research assistant. Use web search to find accurate, up-to-date information.\"\n)\n\n# Use the agent\nresponse = agent.invoke({\n    \"messages\": [{\"role\": \"user\", \"content\": \"What is the most popular sport in the world? Include only Wikipedia sources.\"}]\n})"}
    - {"type":"blockquote","content":"Tip: For more relevant and time-aware results, inject today’s date into your system prompt. This helps the agent understand the current context when searching for recent information. For example: f\"You are a helpful research assistant. Today's date is {datetime.today().strftime('%B %d, %Y')}. Use web search to find accurate, up-to-date information.\""}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-extract)Tavily Extract"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-2)Available Parameters"}
    - {"type":"list","listType":"ul","items":["`extract_depth` (optional, str): The depth of the extraction, either “basic” or “advanced”. Default is “basic”.","`include_images` (optional, bool): Whether to include images in the extraction. Default is False."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-2)Instantiation"}
    - {"type":"codeblock","language":"","content":"from langchain_tavily import TavilyExtract\n\ntool = TavilyExtract(\n    extract_depth=\"basic\",\n    # include_images=False\n)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args-2)Invoke directly with args"}
    - {"type":"list","listType":"ul","items":["`urls` (required): A list of URLs to extract content from.","Both `extract_depth` and `include_images` can also be set during invocation"]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-2)Direct Tool Invocation"}
    - {"type":"codeblock","language":"","content":"# Extract content from a URL\nresult = tavily_extract.invoke({\n    \"urls\": [\"https://en.wikipedia.org/wiki/Lionel_Messi\"]\n})"}
    - {"type":"codeblock","language":"","content":"{\n    'results': [{\n        'url': 'https://en.wikipedia.org/wiki/Lionel_Messi',\n        'raw_content': 'Lionel Messi\\nLionel Andrés \"Leo\" Messi...',\n        'images': []\n    }],\n    'failed_results': [],\n    'response_time': 0.79\n}"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-map/crawl)Tavily Map/Crawl"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-map)Tavily Map"}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-3)Available Parameters"}
    - {"type":"list","listType":"ul","items":["`url` (required, str): The root URL to begin mapping.","`instructions` (optional, str): Natural language instructions guiding the mapping process."]}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-3)Instantiation"}
    - {"type":"codeblock","language":"","content":"from langchain_tavily import TavilyMap\n\ntool = TavilyMap()"}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-3)Direct Tool Invocation"}
    - {"type":"codeblock","language":"","content":"# Map a website structure\nresult = tavily_map.invoke({\n    \"url\": \"https://docs.example.com\",\n    \"instructions\": \"Find all documentation and tutorial pages\"\n})"}
    - {"type":"codeblock","language":"","content":"{\n    'base_url': 'https://docs.example.com',\n    'results': [\n        'https://docs.example.com',\n        'https://docs.example.com/api',\n        'https://docs.example.com/tutorials',\n        'https://docs.example.com/api/endpoints',\n        'https://docs.example.com/tutorials/getting-started'\n    ],\n    'request_id': 'req_abc123',\n    'response_time': 2.1\n}"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-crawl)Tavily Crawl"}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-4)Available Parameters"}
    - {"type":"list","listType":"ul","items":["`url` (required, str): The root URL to begin the crawl.","`instructions` (optional, str): Natural language instructions guiding content extraction."]}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-4)Instantiation"}
    - {"type":"codeblock","language":"","content":"from langchain_tavily import TavilyCrawl\n\ntool = TavilyCrawl()"}
    - {"type":"heading","level":4,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-4)Direct Tool Invocation"}
    - {"type":"codeblock","language":"","content":"# Crawl and extract content\nresult = tavily_crawl.invoke({\n    \"url\": \"https://docs.example.com\",\n    \"instructions\": \"Extract API documentation and code examples\"\n})"}
    - {"type":"codeblock","language":"","content":"{\n    'base_url': 'https://docs.example.com',\n    'results': [\n        {\n            'url': 'https://docs.example.com',\n            'raw_content': '# Documentation\\nWelcome to our API documentation...'\n        },\n        {\n            'url': 'https://docs.example.com/api',\n            'raw_content': '# API Reference\\nComplete API reference guide...'\n        }\n    ],\n    'response_time': 4.5,\n    'request_id': 'req_abc123'\n}"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-research)Tavily Research"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-5)Available Parameters"}
    - {"type":"list","listType":"ul","items":["`input` (required, str): The research task or question to investigate.","`model` (optional, str): The research model to use, one of `\"mini\"`, `\"pro\"`, or `\"auto\"`. Default is `\"auto\"`.","`output_schema` (optional, dict): A JSON Schema object that defines the structure of the research output. Must include a `properties` field and may optionally include a `required` field.","`stream` (optional, bool): Whether to stream the research results as they are generated. When `True`, returns a streaming response. Default is `False`.","`citation_format` (optional, str): The format for citations in the research report, one of `\"numbered\"`, `\"mla\"`, `\"apa\"`, or `\"chicago\"`. Default is `\"numbered\"`."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-5)Instantiation"}
    - {"type":"codeblock","language":"","content":"from langchain_tavily import TavilyResearch\n\ntavily_research = TavilyResearch(\n    # model=\"auto\",\n    # citation_format=\"numbered\",\n    # stream=False,\n)"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args-3)Invoke directly with args"}
    - {"type":"list","listType":"ul","items":["`input` (required): A natural language research task or question.","The following arguments can also be set during invocation: `model`, `output_schema`, `stream`, and `citation_format`."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-5)Direct Tool Invocation"}
    - {"type":"codeblock","language":"","content":"# Create a research task with a structured output schema\nresult = tavily_research.invoke({\n    \"input\": \"Research the latest developments in AI and summarize key trends.\",\n    \"model\": \"mini\",\n    \"citation_format\": \"apa\",\n})"}
    - {"type":"codeblock","language":"","content":"{\n    \"request_id\": \"test-request-123\",\n    \"created_at\": \"2024-01-01T00:00:00Z\",\n    \"status\": \"pending\",\n    \"input\": \"Research the latest developments in AI and summarize key trends.\",\n    \"model\": \"mini\"\n}"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#tavily-get-research)Tavily Get Research"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-6)Available Parameters"}
    - {"type":"list","listType":"ul","items":["`request_id` (required, str): The unique identifier of the research task to retrieve."]}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#instantiation-6)Instantiation"}
    - {"type":"codeblock","language":"","content":"from langchain_tavily import TavilyGetResearch\n\ntavily_get_research = TavilyGetResearch()"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-6)Direct Tool Invocation"}
    - {"type":"codeblock","language":"","content":"# Retrieve results for a completed research task\nresult = tavily_get_research.invoke({\n    \"request_id\": \"test-request-123\"\n})"}
    - {"type":"codeblock","language":"","content":"{\n    \"request_id\": \"test-request-123\",\n    \"created_at\": \"2024-01-01T00:00:00Z\",\n    \"completed_at\": \"2024-01-01T00:05:00Z\",\n    \"status\": \"completed\",\n    \"content\": \"This is a comprehensive research report on AI developments...\",\n    \"sources\": [\n        {\n            \"title\": \"AI Research Paper\",\n            \"url\": \"https://example.com/ai-paper\",\n        }\n    ]\n}"}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Installation](https://docs.tavily.com/documentation/integrations/langchain#installation)","[Credentials](https://docs.tavily.com/documentation/integrations/langchain#credentials)","[Tavily Search](https://docs.tavily.com/documentation/integrations/langchain#tavily-search)","[Available Parameters](https://docs.tavily.com/documentation/integrations/langchain#available-parameters)","[Instantiation](https://docs.tavily.com/documentation/integrations/langchain#instantiation)","[Invoke directly with args](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args)","[Direct Tool Invocation](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation)","[Use with Agent](https://docs.tavily.com/documentation/integrations/langchain#use-with-agent)","[Tavily Extract](https://docs.tavily.com/documentation/integrations/langchain#tavily-extract)","[Available Parameters](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-2)","[Instantiation](https://docs.tavily.com/documentation/integrations/langchain#instantiation-2)","[Invoke directly with args](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args-2)","[Direct Tool Invocation](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-2)","[Tavily Map/Crawl](https://docs.tavily.com/documentation/integrations/langchain#tavily-map%2Fcrawl)","[Tavily Map](https://docs.tavily.com/documentation/integrations/langchain#tavily-map)","[Available Parameters](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-3)","[Instantiation](https://docs.tavily.com/documentation/integrations/langchain#instantiation-3)","[Direct Tool Invocation](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-3)","[Tavily Crawl](https://docs.tavily.com/documentation/integrations/langchain#tavily-crawl)","[Available Parameters](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-4)","[Instantiation](https://docs.tavily.com/documentation/integrations/langchain#instantiation-4)","[Direct Tool Invocation](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-4)","[Tavily Research](https://docs.tavily.com/documentation/integrations/langchain#tavily-research)","[Available Parameters](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-5)","[Instantiation](https://docs.tavily.com/documentation/integrations/langchain#instantiation-5)","[Invoke directly with args](https://docs.tavily.com/documentation/integrations/langchain#invoke-directly-with-args-3)","[Direct Tool Invocation](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-5)","[Tavily Get Research](https://docs.tavily.com/documentation/integrations/langchain#tavily-get-research)","[Available Parameters](https://docs.tavily.com/documentation/integrations/langchain#available-parameters-6)","[Instantiation](https://docs.tavily.com/documentation/integrations/langchain#instantiation-6)","[Direct Tool Invocation](https://docs.tavily.com/documentation/integrations/langchain#direct-tool-invocation-6)"]}
    - {"type":"ul","items":["max_results (optional, int): Maximum number of search results to return. Default is 5.","topic (optional, str): Category of the search. Can be “general”, “news”, or “finance”. Default is “general”.","include_answer (optional, bool): Include an answer to original query in results. Default is False.","include_raw_content (optional, bool): Include cleaned and parsed HTML of each search result. Default is False.","include_images (optional, bool): Include a list of query related images in the response. Default is False.","include_image_descriptions (optional, bool): Include descriptive text for each image. Default is False.","search_depth (optional, str): Depth of the search, either “basic” or “advanced”. Default is “basic”.","time_range (optional, str): The time range back from the current date ( publish date ) to filter results - “day”, “week”, “month”, or “year”. Default is None.","start_date (optional, str): Will return all results after the specified start date ( publish date ). Required to be written in the format YYYY-MM-DD. Default is None.","end_date (optional, str): Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD. Default is None.","include_domains (optional, List[str]): List of domains to specifically include. Maximum 300 domains. Default is None.","exclude_domains (optional, List[str]): List of domains to specifically exclude. Maximum 150 domains. Default is None.","include_usage (optional, bool): Whether to include credit usage information in the response. Default is False."]}
    - {"type":"ul","items":["query (required): A natural language search query","The following arguments can also be set during invocation: include_images, search_depth, time_range, include_domains, exclude_domains, start_date, end_date","For reliability and performance reasons, certain parameters that affect response size cannot be modified during invocation: include_answer and include_raw_content. These limitations prevent unexpected context window issues and ensure consistent results."]}
    - {"type":"ul","items":["extract_depth (optional, str): The depth of the extraction, either “basic” or “advanced”. Default is “basic”.","include_images (optional, bool): Whether to include images in the extraction. Default is False."]}
    - {"type":"ul","items":["urls (required): A list of URLs to extract content from.","Both extract_depth and include_images can also be set during invocation"]}
    - {"type":"ul","items":["url (required, str): The root URL to begin mapping.","instructions (optional, str): Natural language instructions guiding the mapping process."]}
    - {"type":"ul","items":["url (required, str): The root URL to begin the crawl.","instructions (optional, str): Natural language instructions guiding content extraction."]}
    - {"type":"ul","items":["input (required, str): The research task or question to investigate.","model (optional, str): The research model to use, one of \"mini\", \"pro\", or \"auto\". Default is \"auto\".","output_schema (optional, dict): A JSON Schema object that defines the structure of the research output. Must include a properties field and may optionally include a required field.","stream (optional, bool): Whether to stream the research results as they are generated. When True, returns a streaming response. Default is False.","citation_format (optional, str): The format for citations in the research report, one of \"numbered\", \"mla\", \"apa\", or \"chicago\". Default is \"numbered\"."]}
    - {"type":"ul","items":["input (required): A natural language research task or question.","The following arguments can also be set during invocation: model, output_schema, stream, and citation_format."]}
    - {"type":"ul","items":["request_id (required, str): The unique identifier of the research task to retrieve."]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install -U langchain-tavily"}
    - {"language":"text","code":"pip install -U langchain-tavily"}
    - {"language":"text","code":"import getpass\nimport os\n\nif not os.environ.get(\"TAVILY_API_KEY\"):\n    os.environ[\"TAVILY_API_KEY\"] = getpass.getpass(\"Tavily API key:\\n\")"}
    - {"language":"text","code":"import getpass\nimport os\n\nif not os.environ.get(\"TAVILY_API_KEY\"):\n    os.environ[\"TAVILY_API_KEY\"] = getpass.getpass(\"Tavily API key:\\n\")"}
    - {"language":"text","code":"from langchain_tavily import TavilySearch\n\ntool = TavilySearch(\n    max_results=5,\n    topic=\"general\",\n    # include_answer=False,\n    # include_raw_content=False,\n    # include_images=False,\n    # include_image_descriptions=False,\n    # search_depth=\"basic\",\n    # time_range=\"day\",\n    # start_date=None,\n    # end_date=None,\n    # include_domains=None,\n    # exclude_domains=None,\n    # include_usage= False\n)"}
    - {"language":"text","code":"from langchain_tavily import TavilySearch\n\ntool = TavilySearch(\n    max_results=5,\n    topic=\"general\",\n    # include_answer=False,\n    # include_raw_content=False,\n    # include_images=False,\n    # include_image_descriptions=False,\n    # search_depth=\"basic\",\n    # time_range=\"day\",\n    # start_date=None,\n    # end_date=None,\n    # include_domains=None,\n    # exclude_domains=None,\n    # include_usage= False\n)"}
    - {"language":"text","code":"# Basic usage\nresult = tavily_search.invoke({\"query\": \"What happened at the last wimbledon\"})"}
    - {"language":"text","code":"# Basic usage\nresult = tavily_search.invoke({\"query\": \"What happened at the last wimbledon\"})"}
    - {"language":"json","code":"{\n 'query': 'What happened at the last wimbledon',\n 'follow_up_questions': None,\n 'answer': None,\n 'images': [],\n 'results': [\n   {'url': 'https://en.wikipedia.org/wiki/Wimbledon_Championships',\n    'title': 'Wimbledon Championships - Wikipedia',\n    'content': 'Due to the COVID-19 pandemic, Wimbledon 2020 was cancelled ...',\n    'score': 0.62365627198,\n    'raw_content': None},\n   {'url': 'https://www.cbsnews.com/news/wimbledon-men-final-carlos-alcaraz-novak-djokovic/',\n    'title': \"Carlos Alcaraz beats Novak Djokovic at Wimbledon men's final to ...\",\n    'content': 'In attendance on Sunday was Catherine, the Princess of Wales ...',\n    'score': 0.5154731446,\n    'raw_content': None}\n ],\n 'response_time': 2.3\n}"}
    - {"language":"json","code":"{\n 'query': 'What happened at the last wimbledon',\n 'follow_up_questions': None,\n 'answer': None,\n 'images': [],\n 'results': [\n   {'url': 'https://en.wikipedia.org/wiki/Wimbledon_Championships',\n    'title': 'Wimbledon Championships - Wikipedia',\n    'content': 'Due to the COVID-19 pandemic, Wimbledon 2020 was cancelled ...',\n    'score': 0.62365627198,\n    'raw_content': None},\n   {'url': 'https://www.cbsnews.com/news/wimbledon-men-final-carlos-alcaraz-novak-djokovic/',\n    'title': \"Carlos Alcaraz beats Novak Djokovic at Wimbledon men's final to ...\",\n    'content': 'In attendance on Sunday was Catherine, the Princess of Wales ...',\n    'score': 0.5154731446,\n    'raw_content': None}\n ],\n 'response_time': 2.3\n}"}
    - {"language":"text","code":"# !pip install -qU langchain langchain-openai langchain-tavily\nfrom langchain.agents import create_agent\nfrom langchain_openai import ChatOpenAI\nfrom langchain_tavily import TavilySearch\n\n# Initialize the Tavily Search tool\ntavily_search = TavilySearch(max_results=5, topic=\"general\")\n\n# Initialize the agent with the search tool\nagent = create_agent(\n    model=ChatOpenAI(model=\"gpt-5\"),\n    tools=[tavily_search],\n    system_prompt=\"You are a helpful research assistant. Use web search to find accurate, up-to-date information.\"\n)\n\n# Use the agent\nresponse = agent.invoke({\n    \"messages\": [{\"role\": \"user\", \"content\": \"What is the most popular sport in the world? Include only Wikipedia sources.\"}]\n})"}
    - {"language":"text","code":"# !pip install -qU langchain langchain-openai langchain-tavily\nfrom langchain.agents import create_agent\nfrom langchain_openai import ChatOpenAI\nfrom langchain_tavily import TavilySearch\n\n# Initialize the Tavily Search tool\ntavily_search = TavilySearch(max_results=5, topic=\"general\")\n\n# Initialize the agent with the search tool\nagent = create_agent(\n    model=ChatOpenAI(model=\"gpt-5\"),\n    tools=[tavily_search],\n    system_prompt=\"You are a helpful research assistant. Use web search to find accurate, up-to-date information.\"\n)\n\n# Use the agent\nresponse = agent.invoke({\n    \"messages\": [{\"role\": \"user\", \"content\": \"What is the most popular sport in the world? Include only Wikipedia sources.\"}]\n})"}
    - {"language":"text","code":"from langchain_tavily import TavilyExtract\n\ntool = TavilyExtract(\n    extract_depth=\"basic\",\n    # include_images=False\n)"}
    - {"language":"text","code":"from langchain_tavily import TavilyExtract\n\ntool = TavilyExtract(\n    extract_depth=\"basic\",\n    # include_images=False\n)"}
    - {"language":"text","code":"# Extract content from a URL\nresult = tavily_extract.invoke({\n    \"urls\": [\"https://en.wikipedia.org/wiki/Lionel_Messi\"]\n})"}
    - {"language":"text","code":"# Extract content from a URL\nresult = tavily_extract.invoke({\n    \"urls\": [\"https://en.wikipedia.org/wiki/Lionel_Messi\"]\n})"}
    - {"language":"json","code":"{\n    'results': [{\n        'url': 'https://en.wikipedia.org/wiki/Lionel_Messi',\n        'raw_content': 'Lionel Messi\\nLionel Andrés \"Leo\" Messi...',\n        'images': []\n    }],\n    'failed_results': [],\n    'response_time': 0.79\n}"}
    - {"language":"json","code":"{\n    'results': [{\n        'url': 'https://en.wikipedia.org/wiki/Lionel_Messi',\n        'raw_content': 'Lionel Messi\\nLionel Andrés \"Leo\" Messi...',\n        'images': []\n    }],\n    'failed_results': [],\n    'response_time': 0.79\n}"}
    - {"language":"text","code":"from langchain_tavily import TavilyMap\n\ntool = TavilyMap()"}
    - {"language":"text","code":"from langchain_tavily import TavilyMap\n\ntool = TavilyMap()"}
    - {"language":"text","code":"# Map a website structure\nresult = tavily_map.invoke({\n    \"url\": \"https://docs.example.com\",\n    \"instructions\": \"Find all documentation and tutorial pages\"\n})"}
    - {"language":"text","code":"# Map a website structure\nresult = tavily_map.invoke({\n    \"url\": \"https://docs.example.com\",\n    \"instructions\": \"Find all documentation and tutorial pages\"\n})"}
    - {"language":"json","code":"{\n    'base_url': 'https://docs.example.com',\n    'results': [\n        'https://docs.example.com',\n        'https://docs.example.com/api',\n        'https://docs.example.com/tutorials',\n        'https://docs.example.com/api/endpoints',\n        'https://docs.example.com/tutorials/getting-started'\n    ],\n    'request_id': 'req_abc123',\n    'response_time': 2.1\n}"}
    - {"language":"json","code":"{\n    'base_url': 'https://docs.example.com',\n    'results': [\n        'https://docs.example.com',\n        'https://docs.example.com/api',\n        'https://docs.example.com/tutorials',\n        'https://docs.example.com/api/endpoints',\n        'https://docs.example.com/tutorials/getting-started'\n    ],\n    'request_id': 'req_abc123',\n    'response_time': 2.1\n}"}
    - {"language":"text","code":"from langchain_tavily import TavilyCrawl\n\ntool = TavilyCrawl()"}
    - {"language":"text","code":"from langchain_tavily import TavilyCrawl\n\ntool = TavilyCrawl()"}
    - {"language":"text","code":"# Crawl and extract content\nresult = tavily_crawl.invoke({\n    \"url\": \"https://docs.example.com\",\n    \"instructions\": \"Extract API documentation and code examples\"\n})"}
    - {"language":"text","code":"# Crawl and extract content\nresult = tavily_crawl.invoke({\n    \"url\": \"https://docs.example.com\",\n    \"instructions\": \"Extract API documentation and code examples\"\n})"}
    - {"language":"json","code":"{\n    'base_url': 'https://docs.example.com',\n    'results': [\n        {\n            'url': 'https://docs.example.com',\n            'raw_content': '# Documentation\\nWelcome to our API documentation...'\n        },\n        {\n            'url': 'https://docs.example.com/api',\n            'raw_content': '# API Reference\\nComplete API reference guide...'\n        }\n    ],\n    'response_time': 4.5,\n    'request_id': 'req_abc123'\n}"}
    - {"language":"json","code":"{\n    'base_url': 'https://docs.example.com',\n    'results': [\n        {\n            'url': 'https://docs.example.com',\n            'raw_content': '# Documentation\\nWelcome to our API documentation...'\n        },\n        {\n            'url': 'https://docs.example.com/api',\n            'raw_content': '# API Reference\\nComplete API reference guide...'\n        }\n    ],\n    'response_time': 4.5,\n    'request_id': 'req_abc123'\n}"}
    - {"language":"text","code":"from langchain_tavily import TavilyResearch\n\ntavily_research = TavilyResearch(\n    # model=\"auto\",\n    # citation_format=\"numbered\",\n    # stream=False,\n)"}
    - {"language":"text","code":"from langchain_tavily import TavilyResearch\n\ntavily_research = TavilyResearch(\n    # model=\"auto\",\n    # citation_format=\"numbered\",\n    # stream=False,\n)"}
    - {"language":"text","code":"# Create a research task with a structured output schema\nresult = tavily_research.invoke({\n    \"input\": \"Research the latest developments in AI and summarize key trends.\",\n    \"model\": \"mini\",\n    \"citation_format\": \"apa\",\n})"}
    - {"language":"text","code":"# Create a research task with a structured output schema\nresult = tavily_research.invoke({\n    \"input\": \"Research the latest developments in AI and summarize key trends.\",\n    \"model\": \"mini\",\n    \"citation_format\": \"apa\",\n})"}
    - {"language":"json","code":"{\n    \"request_id\": \"test-request-123\",\n    \"created_at\": \"2024-01-01T00:00:00Z\",\n    \"status\": \"pending\",\n    \"input\": \"Research the latest developments in AI and summarize key trends.\",\n    \"model\": \"mini\"\n}"}
    - {"language":"json","code":"{\n    \"request_id\": \"test-request-123\",\n    \"created_at\": \"2024-01-01T00:00:00Z\",\n    \"status\": \"pending\",\n    \"input\": \"Research the latest developments in AI and summarize key trends.\",\n    \"model\": \"mini\"\n}"}
    - {"language":"text","code":"from langchain_tavily import TavilyGetResearch\n\ntavily_get_research = TavilyGetResearch()"}
    - {"language":"text","code":"from langchain_tavily import TavilyGetResearch\n\ntavily_get_research = TavilyGetResearch()"}
    - {"language":"text","code":"# Retrieve results for a completed research task\nresult = tavily_get_research.invoke({\n    \"request_id\": \"test-request-123\"\n})"}
    - {"language":"text","code":"# Retrieve results for a completed research task\nresult = tavily_get_research.invoke({\n    \"request_id\": \"test-request-123\"\n})"}
    - {"language":"json","code":"{\n    \"request_id\": \"test-request-123\",\n    \"created_at\": \"2024-01-01T00:00:00Z\",\n    \"completed_at\": \"2024-01-01T00:05:00Z\",\n    \"status\": \"completed\",\n    \"content\": \"This is a comprehensive research report on AI developments...\",\n    \"sources\": [\n        {\n            \"title\": \"AI Research Paper\",\n            \"url\": \"https://example.com/ai-paper\",\n        }\n    ]\n}"}
    - {"language":"json","code":"{\n    \"request_id\": \"test-request-123\",\n    \"created_at\": \"2024-01-01T00:00:00Z\",\n    \"completed_at\": \"2024-01-01T00:05:00Z\",\n    \"status\": \"completed\",\n    \"content\": \"This is a comprehensive research report on AI developments...\",\n    \"sources\": [\n        {\n            \"title\": \"AI Research Paper\",\n            \"url\": \"https://example.com/ai-paper\",\n        }\n    ]\n}"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"LangChain_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"LangChain_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"LangChain_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"LangChain_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"LangChain_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"LangChain_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"LangChain_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"LangChain_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"LangChain_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"LangChain_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"LangChain_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"LangChain_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"LangChain_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"LangChain_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"LangChain_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"LangChain_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"LangChain_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"LangChain_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"LangChain_-_Tavily_Docs/svg_23.png","width":16,"height":16}
    - {"type":"svg","index":24,"filename":"LangChain_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"LangChain_-_Tavily_Docs/svg_25.png","width":14,"height":12}
    - {"type":"svg","index":26,"filename":"LangChain_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"LangChain_-_Tavily_Docs/svg_27.png","width":16,"height":16}
    - {"type":"svg","index":28,"filename":"LangChain_-_Tavily_Docs/svg_28.png","width":14,"height":12}
    - {"type":"svg","index":29,"filename":"LangChain_-_Tavily_Docs/svg_29.png","width":14,"height":12}
    - {"type":"svg","index":30,"filename":"LangChain_-_Tavily_Docs/svg_30.png","width":14,"height":12}
    - {"type":"svg","index":31,"filename":"LangChain_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"LangChain_-_Tavily_Docs/svg_32.png","width":16,"height":16}
    - {"type":"svg","index":33,"filename":"LangChain_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"LangChain_-_Tavily_Docs/svg_34.png","width":14,"height":12}
    - {"type":"svg","index":35,"filename":"LangChain_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"LangChain_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"LangChain_-_Tavily_Docs/svg_37.png","width":16,"height":16}
    - {"type":"svg","index":38,"filename":"LangChain_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"LangChain_-_Tavily_Docs/svg_39.png","width":14,"height":12}
    - {"type":"svg","index":40,"filename":"LangChain_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"LangChain_-_Tavily_Docs/svg_41.png","width":16,"height":16}
    - {"type":"svg","index":42,"filename":"LangChain_-_Tavily_Docs/svg_42.png","width":14,"height":12}
    - {"type":"svg","index":43,"filename":"LangChain_-_Tavily_Docs/svg_43.png","width":14,"height":12}
    - {"type":"svg","index":44,"filename":"LangChain_-_Tavily_Docs/svg_44.png","width":14,"height":12}
    - {"type":"svg","index":45,"filename":"LangChain_-_Tavily_Docs/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"LangChain_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"LangChain_-_Tavily_Docs/svg_47.png","width":14,"height":12}
    - {"type":"svg","index":48,"filename":"LangChain_-_Tavily_Docs/svg_48.png","width":14,"height":12}
    - {"type":"svg","index":49,"filename":"LangChain_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"LangChain_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"LangChain_-_Tavily_Docs/svg_51.png","width":16,"height":16}
    - {"type":"svg","index":52,"filename":"LangChain_-_Tavily_Docs/svg_52.png","width":16,"height":16}
    - {"type":"svg","index":53,"filename":"LangChain_-_Tavily_Docs/svg_53.png","width":14,"height":12}
    - {"type":"svg","index":54,"filename":"LangChain_-_Tavily_Docs/svg_54.png","width":14,"height":12}
    - {"type":"svg","index":55,"filename":"LangChain_-_Tavily_Docs/svg_55.png","width":14,"height":12}
    - {"type":"svg","index":56,"filename":"LangChain_-_Tavily_Docs/svg_56.png","width":14,"height":12}
    - {"type":"svg","index":57,"filename":"LangChain_-_Tavily_Docs/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"LangChain_-_Tavily_Docs/svg_58.png","width":16,"height":16}
    - {"type":"svg","index":59,"filename":"LangChain_-_Tavily_Docs/svg_59.png","width":14,"height":12}
    - {"type":"svg","index":60,"filename":"LangChain_-_Tavily_Docs/svg_60.png","width":16,"height":16}
    - {"type":"svg","index":61,"filename":"LangChain_-_Tavily_Docs/svg_61.png","width":16,"height":16}
    - {"type":"svg","index":62,"filename":"LangChain_-_Tavily_Docs/svg_62.png","width":16,"height":16}
    - {"type":"svg","index":63,"filename":"LangChain_-_Tavily_Docs/svg_63.png","width":16,"height":16}
    - {"type":"svg","index":64,"filename":"LangChain_-_Tavily_Docs/svg_64.png","width":14,"height":12}
    - {"type":"svg","index":65,"filename":"LangChain_-_Tavily_Docs/svg_65.png","width":14,"height":12}
    - {"type":"svg","index":66,"filename":"LangChain_-_Tavily_Docs/svg_66.png","width":14,"height":12}
    - {"type":"svg","index":67,"filename":"LangChain_-_Tavily_Docs/svg_67.png","width":16,"height":16}
    - {"type":"svg","index":68,"filename":"LangChain_-_Tavily_Docs/svg_68.png","width":16,"height":16}
    - {"type":"svg","index":69,"filename":"LangChain_-_Tavily_Docs/svg_69.png","width":14,"height":12}
    - {"type":"svg","index":70,"filename":"LangChain_-_Tavily_Docs/svg_70.png","width":16,"height":16}
    - {"type":"svg","index":71,"filename":"LangChain_-_Tavily_Docs/svg_71.png","width":16,"height":16}
    - {"type":"svg","index":72,"filename":"LangChain_-_Tavily_Docs/svg_72.png","width":16,"height":16}
    - {"type":"svg","index":73,"filename":"LangChain_-_Tavily_Docs/svg_73.png","width":16,"height":16}
    - {"type":"svg","index":74,"filename":"LangChain_-_Tavily_Docs/svg_74.png","width":14,"height":12}
    - {"type":"svg","index":75,"filename":"LangChain_-_Tavily_Docs/svg_75.png","width":14,"height":12}
    - {"type":"svg","index":76,"filename":"LangChain_-_Tavily_Docs/svg_76.png","width":14,"height":12}
    - {"type":"svg","index":77,"filename":"LangChain_-_Tavily_Docs/svg_77.png","width":16,"height":16}
    - {"type":"svg","index":78,"filename":"LangChain_-_Tavily_Docs/svg_78.png","width":16,"height":16}
    - {"type":"svg","index":79,"filename":"LangChain_-_Tavily_Docs/svg_79.png","width":14,"height":12}
    - {"type":"svg","index":80,"filename":"LangChain_-_Tavily_Docs/svg_80.png","width":14,"height":12}
    - {"type":"svg","index":81,"filename":"LangChain_-_Tavily_Docs/svg_81.png","width":16,"height":16}
    - {"type":"svg","index":82,"filename":"LangChain_-_Tavily_Docs/svg_82.png","width":16,"height":16}
    - {"type":"svg","index":83,"filename":"LangChain_-_Tavily_Docs/svg_83.png","width":16,"height":16}
    - {"type":"svg","index":84,"filename":"LangChain_-_Tavily_Docs/svg_84.png","width":16,"height":16}
    - {"type":"svg","index":85,"filename":"LangChain_-_Tavily_Docs/svg_85.png","width":14,"height":12}
    - {"type":"svg","index":86,"filename":"LangChain_-_Tavily_Docs/svg_86.png","width":14,"height":12}
    - {"type":"svg","index":87,"filename":"LangChain_-_Tavily_Docs/svg_87.png","width":14,"height":12}
    - {"type":"svg","index":88,"filename":"LangChain_-_Tavily_Docs/svg_88.png","width":16,"height":16}
    - {"type":"svg","index":89,"filename":"LangChain_-_Tavily_Docs/svg_89.png","width":16,"height":16}
    - {"type":"svg","index":90,"filename":"LangChain_-_Tavily_Docs/svg_90.png","width":14,"height":12}
    - {"type":"svg","index":91,"filename":"LangChain_-_Tavily_Docs/svg_91.png","width":16,"height":16}
    - {"type":"svg","index":92,"filename":"LangChain_-_Tavily_Docs/svg_92.png","width":16,"height":16}
    - {"type":"svg","index":93,"filename":"LangChain_-_Tavily_Docs/svg_93.png","width":16,"height":16}
    - {"type":"svg","index":94,"filename":"LangChain_-_Tavily_Docs/svg_94.png","width":16,"height":16}
    - {"type":"svg","index":95,"filename":"LangChain_-_Tavily_Docs/svg_95.png","width":14,"height":14}
    - {"type":"svg","index":96,"filename":"LangChain_-_Tavily_Docs/svg_96.png","width":14,"height":14}
    - {"type":"svg","index":97,"filename":"LangChain_-_Tavily_Docs/svg_97.png","width":14,"height":14}
    - {"type":"svg","index":102,"filename":"LangChain_-_Tavily_Docs/svg_102.png","width":20,"height":20}
    - {"type":"svg","index":103,"filename":"LangChain_-_Tavily_Docs/svg_103.png","width":20,"height":20}
    - {"type":"svg","index":104,"filename":"LangChain_-_Tavily_Docs/svg_104.png","width":20,"height":20}
    - {"type":"svg","index":105,"filename":"LangChain_-_Tavily_Docs/svg_105.png","width":20,"height":20}
    - {"type":"svg","index":106,"filename":"LangChain_-_Tavily_Docs/svg_106.png","width":49,"height":14}
    - {"type":"svg","index":107,"filename":"LangChain_-_Tavily_Docs/svg_107.png","width":16,"height":16}
    - {"type":"svg","index":108,"filename":"LangChain_-_Tavily_Docs/svg_108.png","width":16,"height":16}
    - {"type":"svg","index":109,"filename":"LangChain_-_Tavily_Docs/svg_109.png","width":16,"height":16}
    - {"type":"svg","index":119,"filename":"LangChain_-_Tavily_Docs/svg_119.png","width":16,"height":16}
    - {"type":"svg","index":120,"filename":"LangChain_-_Tavily_Docs/svg_120.png","width":14,"height":14}
    - {"type":"svg","index":121,"filename":"LangChain_-_Tavily_Docs/svg_121.png","width":16,"height":16}
    - {"type":"svg","index":122,"filename":"LangChain_-_Tavily_Docs/svg_122.png","width":12,"height":12}
    - {"type":"svg","index":123,"filename":"LangChain_-_Tavily_Docs/svg_123.png","width":14,"height":14}
    - {"type":"svg","index":124,"filename":"LangChain_-_Tavily_Docs/svg_124.png","width":16,"height":16}
    - {"type":"svg","index":125,"filename":"LangChain_-_Tavily_Docs/svg_125.png","width":12,"height":12}
    - {"type":"svg","index":126,"filename":"LangChain_-_Tavily_Docs/svg_126.png","width":14,"height":14}
    - {"type":"svg","index":127,"filename":"LangChain_-_Tavily_Docs/svg_127.png","width":16,"height":16}
    - {"type":"svg","index":128,"filename":"LangChain_-_Tavily_Docs/svg_128.png","width":12,"height":12}
    - {"type":"svg","index":129,"filename":"LangChain_-_Tavily_Docs/svg_129.png","width":14,"height":14}
  chartData: []
  blockquotes:
    - "Warning: The langchain_community.tools.tavily_search.tool is deprecated. While it remains functional for now, we strongly recommend migrating to the new langchain-tavily Python package which supports Search, Extract, Map, and Crawl functionality and receives continuous updates with the latest features."
    - "Tip: For more relevant and time-aware results, inject today’s date into your system prompt. This helps the agent understand the current context when searching for recent information. For example: f\"You are a helpful research assistant. Today's date is {datetime.today().strftime('%B %d, %Y')}. Use web search to find accurate, up-to-date information.\""
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

# LangChain

## 源URL

https://docs.tavily.com/integrations/langchain

## 描述

We're excited to partner with Langchain as their recommended search tool!

## 内容

> Warning: The langchain_community.tools.tavily_search.tool is deprecated. While it remains functional for now, we strongly recommend migrating to the new langchain-tavily Python package which supports Search, Extract, Map, and Crawl functionality and receives continuous updates with the latest features.

### Installation

```text
pip install -U langchain-tavily
```

#### Credentials

```text
import getpass
import os

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")
```

### Tavily Search

#### Available Parameters

- `max_results` (optional, int): Maximum number of search results to return. Default is 5.
- `topic` (optional, str): Category of the search. Can be “general”, “news”, or “finance”. Default is “general”.
- `include_answer` (optional, bool): Include an answer to original query in results. Default is False.
- `include_raw_content` (optional, bool): Include cleaned and parsed HTML of each search result. Default is False.
- `include_images` (optional, bool): Include a list of query related images in the response. Default is False.
- `include_image_descriptions` (optional, bool): Include descriptive text for each image. Default is False.
- `search_depth` (optional, str): Depth of the search, either “basic” or “advanced”. Default is “basic”.
- `time_range` (optional, str): The time range back from the current date ( publish date ) to filter results - “day”, “week”, “month”, or “year”. Default is None.
- `start_date` (optional, str): Will return all results after the specified start date ( publish date ). Required to be written in the format YYYY-MM-DD. Default is None.
- `end_date` (optional, str): Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD. Default is None.
- `include_domains` (optional, List[str]): List of domains to specifically include. Maximum 300 domains. Default is None.
- `exclude_domains` (optional, List[str]): List of domains to specifically exclude. Maximum 150 domains. Default is None.
- `include_usage` (optional, bool): Whether to include credit usage information in the response. Default is False.

#### Instantiation

```text
from langchain_tavily import TavilySearch

tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # start_date=None,
    # end_date=None,
    # include_domains=None,
    # exclude_domains=None,
    # include_usage= False
)
```

#### Invoke directly with args

- `query` (required): A natural language search query
- The following arguments can also be set during invocation: `include_images`, `search_depth`, `time_range`, `include_domains`, `exclude_domains`, `start_date`, `end_date`
- For reliability and performance reasons, certain parameters that affect response size cannot be modified during invocation: `include_answer` and `include_raw_content`. These limitations prevent unexpected context window issues and ensure consistent results.

#### Direct Tool Invocation

```text
# Basic usage
result = tavily_search.invoke({"query": "What happened at the last wimbledon"})
```

```text
{
 'query': 'What happened at the last wimbledon',
 'follow_up_questions': None,
 'answer': None,
 'images': [],
 'results': [
   {'url': 'https://en.wikipedia.org/wiki/Wimbledon_Championships',
    'title': 'Wimbledon Championships - Wikipedia',
    'content': 'Due to the COVID-19 pandemic, Wimbledon 2020 was cancelled ...',
    'score': 0.62365627198,
    'raw_content': None},
   {'url': 'https://www.cbsnews.com/news/wimbledon-men-final-carlos-alcaraz-novak-djokovic/',
    'title': "Carlos Alcaraz beats Novak Djokovic at Wimbledon men's final to ...",
    'content': 'In attendance on Sunday was Catherine, the Princess of Wales ...',
    'score': 0.5154731446,
    'raw_content': None}
 ],
 'response_time': 2.3
}
```

#### Use with Agent

```text
# !pip install -qU langchain langchain-openai langchain-tavily
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# Initialize the Tavily Search tool
tavily_search = TavilySearch(max_results=5, topic="general")

# Initialize the agent with the search tool
agent = create_agent(
    model=ChatOpenAI(model="gpt-5"),
    tools=[tavily_search],
    system_prompt="You are a helpful research assistant. Use web search to find accurate, up-to-date information."
)

# Use the agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "What is the most popular sport in the world? Include only Wikipedia sources."}]
})
```

> Tip: For more relevant and time-aware results, inject today’s date into your system prompt. This helps the agent understand the current context when searching for recent information. For example: f"You are a helpful research assistant. Today's date is {datetime.today().strftime('%B %d, %Y')}. Use web search to find accurate, up-to-date information."

### Tavily Extract

#### Available Parameters

- `extract_depth` (optional, str): The depth of the extraction, either “basic” or “advanced”. Default is “basic”.
- `include_images` (optional, bool): Whether to include images in the extraction. Default is False.

#### Instantiation

```text
from langchain_tavily import TavilyExtract

tool = TavilyExtract(
    extract_depth="basic",
    # include_images=False
)
```

#### Invoke directly with args

- `urls` (required): A list of URLs to extract content from.
- Both `extract_depth` and `include_images` can also be set during invocation

#### Direct Tool Invocation

```text
# Extract content from a URL
result = tavily_extract.invoke({
    "urls": ["https://en.wikipedia.org/wiki/Lionel_Messi"]
})
```

```text
{
    'results': [{
        'url': 'https://en.wikipedia.org/wiki/Lionel_Messi',
        'raw_content': 'Lionel Messi\nLionel Andrés "Leo" Messi...',
        'images': []
    }],
    'failed_results': [],
    'response_time': 0.79
}
```

### Tavily Map/Crawl

#### Tavily Map

##### Available Parameters

- `url` (required, str): The root URL to begin mapping.
- `instructions` (optional, str): Natural language instructions guiding the mapping process.

##### Instantiation

```text
from langchain_tavily import TavilyMap

tool = TavilyMap()
```

##### Direct Tool Invocation

```text
# Map a website structure
result = tavily_map.invoke({
    "url": "https://docs.example.com",
    "instructions": "Find all documentation and tutorial pages"
})
```

```text
{
    'base_url': 'https://docs.example.com',
    'results': [
        'https://docs.example.com',
        'https://docs.example.com/api',
        'https://docs.example.com/tutorials',
        'https://docs.example.com/api/endpoints',
        'https://docs.example.com/tutorials/getting-started'
    ],
    'request_id': 'req_abc123',
    'response_time': 2.1
}
```

#### Tavily Crawl

##### Available Parameters

- `url` (required, str): The root URL to begin the crawl.
- `instructions` (optional, str): Natural language instructions guiding content extraction.

##### Instantiation

```text
from langchain_tavily import TavilyCrawl

tool = TavilyCrawl()
```

##### Direct Tool Invocation

```text
# Crawl and extract content
result = tavily_crawl.invoke({
    "url": "https://docs.example.com",
    "instructions": "Extract API documentation and code examples"
})
```

```text
{
    'base_url': 'https://docs.example.com',
    'results': [
        {
            'url': 'https://docs.example.com',
            'raw_content': '# Documentation\nWelcome to our API documentation...'
        },
        {
            'url': 'https://docs.example.com/api',
            'raw_content': '# API Reference\nComplete API reference guide...'
        }
    ],
    'response_time': 4.5,
    'request_id': 'req_abc123'
}
```

### Tavily Research

#### Available Parameters

- `input` (required, str): The research task or question to investigate.
- `model` (optional, str): The research model to use, one of `"mini"`, `"pro"`, or `"auto"`. Default is `"auto"`.
- `output_schema` (optional, dict): A JSON Schema object that defines the structure of the research output. Must include a `properties` field and may optionally include a `required` field.
- `stream` (optional, bool): Whether to stream the research results as they are generated. When `True`, returns a streaming response. Default is `False`.
- `citation_format` (optional, str): The format for citations in the research report, one of `"numbered"`, `"mla"`, `"apa"`, or `"chicago"`. Default is `"numbered"`.

#### Instantiation

```text
from langchain_tavily import TavilyResearch

tavily_research = TavilyResearch(
    # model="auto",
    # citation_format="numbered",
    # stream=False,
)
```

#### Invoke directly with args

- `input` (required): A natural language research task or question.
- The following arguments can also be set during invocation: `model`, `output_schema`, `stream`, and `citation_format`.

#### Direct Tool Invocation

```text
# Create a research task with a structured output schema
result = tavily_research.invoke({
    "input": "Research the latest developments in AI and summarize key trends.",
    "model": "mini",
    "citation_format": "apa",
})
```

```text
{
    "request_id": "test-request-123",
    "created_at": "2024-01-01T00:00:00Z",
    "status": "pending",
    "input": "Research the latest developments in AI and summarize key trends.",
    "model": "mini"
}
```

### Tavily Get Research

#### Available Parameters

- `request_id` (required, str): The unique identifier of the research task to retrieve.

#### Instantiation

```text
from langchain_tavily import TavilyGetResearch

tavily_get_research = TavilyGetResearch()
```

#### Direct Tool Invocation

```text
# Retrieve results for a completed research task
result = tavily_get_research.invoke({
    "request_id": "test-request-123"
})
```

```text
{
    "request_id": "test-request-123",
    "created_at": "2024-01-01T00:00:00Z",
    "completed_at": "2024-01-01T00:05:00Z",
    "status": "completed",
    "content": "This is a comprehensive research report on AI developments...",
    "sources": [
        {
            "title": "AI Research Paper",
            "url": "https://example.com/ai-paper",
        }
    ]
}
```

## 图片

![light logo](LangChain_-_Tavily_Docs/image_1.svg)

![dark logo](LangChain_-_Tavily_Docs/image_2.svg)

![light logo](LangChain_-_Tavily_Docs/image_3.svg)

![dark logo](LangChain_-_Tavily_Docs/image_4.svg)

![tavily-logo](LangChain_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](LangChain_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](LangChain_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](LangChain_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](LangChain_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](LangChain_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](LangChain_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](LangChain_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](LangChain_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](LangChain_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](LangChain_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](LangChain_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](LangChain_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](LangChain_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](LangChain_-_Tavily_Docs/svg_23.png)
*尺寸: 16x16px*

![SVG图表 24](LangChain_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](LangChain_-_Tavily_Docs/svg_25.png)
*尺寸: 14x12px*

![SVG图表 26](LangChain_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](LangChain_-_Tavily_Docs/svg_27.png)
*尺寸: 16x16px*

![SVG图表 28](LangChain_-_Tavily_Docs/svg_28.png)
*尺寸: 14x12px*

![SVG图表 29](LangChain_-_Tavily_Docs/svg_29.png)
*尺寸: 14x12px*

![SVG图表 30](LangChain_-_Tavily_Docs/svg_30.png)
*尺寸: 14x12px*

![SVG图表 31](LangChain_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](LangChain_-_Tavily_Docs/svg_32.png)
*尺寸: 16x16px*

![SVG图表 33](LangChain_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 34](LangChain_-_Tavily_Docs/svg_34.png)
*尺寸: 14x12px*

![SVG图表 35](LangChain_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](LangChain_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](LangChain_-_Tavily_Docs/svg_37.png)
*尺寸: 16x16px*

![SVG图表 38](LangChain_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](LangChain_-_Tavily_Docs/svg_39.png)
*尺寸: 14x12px*

![SVG图表 40](LangChain_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](LangChain_-_Tavily_Docs/svg_41.png)
*尺寸: 16x16px*

![SVG图表 42](LangChain_-_Tavily_Docs/svg_42.png)
*尺寸: 14x12px*

![SVG图表 43](LangChain_-_Tavily_Docs/svg_43.png)
*尺寸: 14x12px*

![SVG图表 44](LangChain_-_Tavily_Docs/svg_44.png)
*尺寸: 14x12px*

![SVG图表 45](LangChain_-_Tavily_Docs/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](LangChain_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](LangChain_-_Tavily_Docs/svg_47.png)
*尺寸: 14x12px*

![SVG图表 48](LangChain_-_Tavily_Docs/svg_48.png)
*尺寸: 14x12px*

![SVG图表 49](LangChain_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](LangChain_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](LangChain_-_Tavily_Docs/svg_51.png)
*尺寸: 16x16px*

![SVG图表 52](LangChain_-_Tavily_Docs/svg_52.png)
*尺寸: 16x16px*

![SVG图表 53](LangChain_-_Tavily_Docs/svg_53.png)
*尺寸: 14x12px*

![SVG图表 54](LangChain_-_Tavily_Docs/svg_54.png)
*尺寸: 14x12px*

![SVG图表 55](LangChain_-_Tavily_Docs/svg_55.png)
*尺寸: 14x12px*

![SVG图表 56](LangChain_-_Tavily_Docs/svg_56.png)
*尺寸: 14x12px*

![SVG图表 57](LangChain_-_Tavily_Docs/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](LangChain_-_Tavily_Docs/svg_58.png)
*尺寸: 16x16px*

![SVG图表 59](LangChain_-_Tavily_Docs/svg_59.png)
*尺寸: 14x12px*

![SVG图表 60](LangChain_-_Tavily_Docs/svg_60.png)
*尺寸: 16x16px*

![SVG图表 61](LangChain_-_Tavily_Docs/svg_61.png)
*尺寸: 16x16px*

![SVG图表 62](LangChain_-_Tavily_Docs/svg_62.png)
*尺寸: 16x16px*

![SVG图表 63](LangChain_-_Tavily_Docs/svg_63.png)
*尺寸: 16x16px*

![SVG图表 64](LangChain_-_Tavily_Docs/svg_64.png)
*尺寸: 14x12px*

![SVG图表 65](LangChain_-_Tavily_Docs/svg_65.png)
*尺寸: 14x12px*

![SVG图表 66](LangChain_-_Tavily_Docs/svg_66.png)
*尺寸: 14x12px*

![SVG图表 67](LangChain_-_Tavily_Docs/svg_67.png)
*尺寸: 16x16px*

![SVG图表 68](LangChain_-_Tavily_Docs/svg_68.png)
*尺寸: 16x16px*

![SVG图表 69](LangChain_-_Tavily_Docs/svg_69.png)
*尺寸: 14x12px*

![SVG图表 70](LangChain_-_Tavily_Docs/svg_70.png)
*尺寸: 16x16px*

![SVG图表 71](LangChain_-_Tavily_Docs/svg_71.png)
*尺寸: 16x16px*

![SVG图表 72](LangChain_-_Tavily_Docs/svg_72.png)
*尺寸: 16x16px*

![SVG图表 73](LangChain_-_Tavily_Docs/svg_73.png)
*尺寸: 16x16px*

![SVG图表 74](LangChain_-_Tavily_Docs/svg_74.png)
*尺寸: 14x12px*

![SVG图表 75](LangChain_-_Tavily_Docs/svg_75.png)
*尺寸: 14x12px*

![SVG图表 76](LangChain_-_Tavily_Docs/svg_76.png)
*尺寸: 14x12px*

![SVG图表 77](LangChain_-_Tavily_Docs/svg_77.png)
*尺寸: 16x16px*

![SVG图表 78](LangChain_-_Tavily_Docs/svg_78.png)
*尺寸: 16x16px*

![SVG图表 79](LangChain_-_Tavily_Docs/svg_79.png)
*尺寸: 14x12px*

![SVG图表 80](LangChain_-_Tavily_Docs/svg_80.png)
*尺寸: 14x12px*

![SVG图表 81](LangChain_-_Tavily_Docs/svg_81.png)
*尺寸: 16x16px*

![SVG图表 82](LangChain_-_Tavily_Docs/svg_82.png)
*尺寸: 16x16px*

![SVG图表 83](LangChain_-_Tavily_Docs/svg_83.png)
*尺寸: 16x16px*

![SVG图表 84](LangChain_-_Tavily_Docs/svg_84.png)
*尺寸: 16x16px*

![SVG图表 85](LangChain_-_Tavily_Docs/svg_85.png)
*尺寸: 14x12px*

![SVG图表 86](LangChain_-_Tavily_Docs/svg_86.png)
*尺寸: 14x12px*

![SVG图表 87](LangChain_-_Tavily_Docs/svg_87.png)
*尺寸: 14x12px*

![SVG图表 88](LangChain_-_Tavily_Docs/svg_88.png)
*尺寸: 16x16px*

![SVG图表 89](LangChain_-_Tavily_Docs/svg_89.png)
*尺寸: 16x16px*

![SVG图表 90](LangChain_-_Tavily_Docs/svg_90.png)
*尺寸: 14x12px*

![SVG图表 91](LangChain_-_Tavily_Docs/svg_91.png)
*尺寸: 16x16px*

![SVG图表 92](LangChain_-_Tavily_Docs/svg_92.png)
*尺寸: 16x16px*

![SVG图表 93](LangChain_-_Tavily_Docs/svg_93.png)
*尺寸: 16x16px*

![SVG图表 94](LangChain_-_Tavily_Docs/svg_94.png)
*尺寸: 16x16px*

![SVG图表 95](LangChain_-_Tavily_Docs/svg_95.png)
*尺寸: 14x14px*

![SVG图表 96](LangChain_-_Tavily_Docs/svg_96.png)
*尺寸: 14x14px*

![SVG图表 97](LangChain_-_Tavily_Docs/svg_97.png)
*尺寸: 14x14px*

![SVG图表 102](LangChain_-_Tavily_Docs/svg_102.png)
*尺寸: 20x20px*

![SVG图表 103](LangChain_-_Tavily_Docs/svg_103.png)
*尺寸: 20x20px*

![SVG图表 104](LangChain_-_Tavily_Docs/svg_104.png)
*尺寸: 20x20px*

![SVG图表 105](LangChain_-_Tavily_Docs/svg_105.png)
*尺寸: 20x20px*

![SVG图表 106](LangChain_-_Tavily_Docs/svg_106.png)
*尺寸: 49x14px*

![SVG图表 107](LangChain_-_Tavily_Docs/svg_107.png)
*尺寸: 16x16px*

![SVG图表 108](LangChain_-_Tavily_Docs/svg_108.png)
*尺寸: 16x16px*

![SVG图表 109](LangChain_-_Tavily_Docs/svg_109.png)
*尺寸: 16x16px*

![SVG图表 119](LangChain_-_Tavily_Docs/svg_119.png)
*尺寸: 16x16px*

![SVG图表 120](LangChain_-_Tavily_Docs/svg_120.png)
*尺寸: 14x14px*

![SVG图表 121](LangChain_-_Tavily_Docs/svg_121.png)
*尺寸: 16x16px*

![SVG图表 122](LangChain_-_Tavily_Docs/svg_122.png)
*尺寸: 12x12px*

![SVG图表 123](LangChain_-_Tavily_Docs/svg_123.png)
*尺寸: 14x14px*

![SVG图表 124](LangChain_-_Tavily_Docs/svg_124.png)
*尺寸: 16x16px*

![SVG图表 125](LangChain_-_Tavily_Docs/svg_125.png)
*尺寸: 12x12px*

![SVG图表 126](LangChain_-_Tavily_Docs/svg_126.png)
*尺寸: 14x14px*

![SVG图表 127](LangChain_-_Tavily_Docs/svg_127.png)
*尺寸: 16x16px*

![SVG图表 128](LangChain_-_Tavily_Docs/svg_128.png)
*尺寸: 12x12px*

![SVG图表 129](LangChain_-_Tavily_Docs/svg_129.png)
*尺寸: 14x14px*
