---
id: "url-123d3e4b"
type: "website"
title: "Tavily Search"
url: "https://docs.tavily.com/"
description: "Execute a search query using Tavily Search."
source: ""
tags: []
crawl_time: "2026-03-18T04:13:38.812Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"API Reference"}
    - {"level":5,"text":"Enterprise API Reference"}
    - {"level":5,"text":"Python SDK"}
    - {"level":5,"text":"JavaScript SDK"}
    - {"level":5,"text":"Best Practices"}
    - {"level":1,"text":"Tavily Search"}
    - {"level":4,"text":"Authorizations"}
    - {"level":4,"text":"Body"}
    - {"level":4,"text":"Response"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"list","listType":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"heading","level":5,"content":"API Reference"}
    - {"type":"list","listType":"ul","items":["[Introduction](https://docs.tavily.com/documentation/api-reference/introduction)","[POSTSearch](https://docs.tavily.com/documentation/api-reference/endpoint/search)","[POSTExtract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)","[POSTCrawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)","[POSTMap](https://docs.tavily.com/documentation/api-reference/endpoint/map)","Research","[GETUsage](https://docs.tavily.com/documentation/api-reference/endpoint/usage)"]}
    - {"type":"heading","level":5,"content":"Enterprise API Reference"}
    - {"type":"list","listType":"ul","items":["API Key Generator"]}
    - {"type":"heading","level":5,"content":"Python SDK"}
    - {"type":"list","listType":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/python/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/python/reference)"]}
    - {"type":"heading","level":5,"content":"JavaScript SDK"}
    - {"type":"list","listType":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/javascript/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/javascript/reference)"]}
    - {"type":"heading","level":5,"content":"Best Practices"}
    - {"type":"list","listType":"ul","items":["[Search](https://docs.tavily.com/documentation/best-practices/best-practices-search)","[Extract](https://docs.tavily.com/documentation/best-practices/best-practices-extract)","[Crawl](https://docs.tavily.com/documentation/best-practices/best-practices-crawl)","[Research](https://docs.tavily.com/documentation/best-practices/best-practices-research)","[API Key Management](https://docs.tavily.com/documentation/best-practices/api-key-management)"]}
    - {"type":"codeblock","language":"","content":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"type":"codeblock","language":"","content":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"type":"codeblock","language":"","content":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"type":"codeblock","language":"","content":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Body"}
    - {"type":"paragraph","content":"Parameters for the Tavily Search request."}
    - {"type":"paragraph","content":"The search query to execute with Tavily."}
    - {"type":"paragraph","content":"`\"who is Leo Messi?\"`"}
    - {"type":"paragraph","content":"Controls the latency vs. relevance tradeoff and how `results[].content` is generated:"}
    - {"type":"list","listType":"ul","items":["`advanced`: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via `chunks_per_source`).","`basic`: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.","`fast`: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant snippets per URL (configurable via `chunks_per_source`).","`ultra-fast`: Minimizes latency above all else. Best for time-critical use cases. Returns one NLP summary per URL."]}
    - {"type":"paragraph","content":"Cost:"}
    - {"type":"list","listType":"ul","items":["`basic`, `fast`, `ultra-fast`: 1 API Credit","`advanced`: 2 API Credits"]}
    - {"type":"paragraph","content":"See [Search Best Practices](https://docs.tavily.com/documentation/best-practices/best-practices-search#search-depth) for guidance on choosing the right search depth."}
    - {"type":"paragraph","content":"Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use `chunks_per_source` to define the maximum number of relevant chunks returned per source and to control the `content` length. Chunks will appear in the `content` field as: `<chunk 1> [...] <chunk 2> [...] <chunk 3>`. Available only when `search_depth` is `advanced`."}
    - {"type":"paragraph","content":"The maximum number of search results to return."}
    - {"type":"paragraph","content":"`1`"}
    - {"type":"paragraph","content":"The category of the search.`news` is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. `general` is for broader, more general-purpose searches that may include a wide range of sources."}
    - {"type":"paragraph","content":"The time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data."}
    - {"type":"paragraph","content":"Will return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD"}
    - {"type":"paragraph","content":"`\"2025-02-09\"`"}
    - {"type":"paragraph","content":"Will return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD"}
    - {"type":"paragraph","content":"`\"2025-12-29\"`"}
    - {"type":"paragraph","content":"Include an LLM-generated answer to the provided query. `basic` or `true` returns a quick answer. `advanced` returns a more detailed answer."}
    - {"type":"paragraph","content":"Include the cleaned and parsed HTML content of each search result. `markdown` or `true` returns search result content in markdown format. `text` returns the plain text from the results and may increase latency."}
    - {"type":"paragraph","content":"Also perform an image search and include the results in the response."}
    - {"type":"paragraph","content":"When `include_images` is `true`, also add a descriptive text for each image."}
    - {"type":"paragraph","content":"Whether to include the favicon URL for each result."}
    - {"type":"paragraph","content":"A list of domains to specifically include in the search results. Maximum 300 domains."}
    - {"type":"paragraph","content":"A list of domains to specifically exclude from the search results. Maximum 150 domains."}
    - {"type":"paragraph","content":"Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is `general`."}
    - {"type":"paragraph","content":"When `auto_parameters` is enabled, Tavily automatically configures search parameters based on your query's content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones. The parameters `include_answer`, `include_raw_content`, and `max_results` must always be set manually, as they directly affect response size. Note: `search_depth` may be automatically set to advanced when it's likely to improve results. This uses 2 API credits per request. To avoid the extra cost, you can explicitly set `search_depth` to `basic`."}
    - {"type":"paragraph","content":"Ensure that only search results containing the exact quoted phrase(s) in the query are returned, bypassing synonyms or semantic variations. Wrap target phrases in quotes within your query (e.g. `\"John Smith\" CEO Acme Corp`). Punctuation is typically ignored inside quotes."}
    - {"type":"paragraph","content":"Whether to include credit usage information in the response."}
    - {"type":"paragraph","content":"🔒 Enterprise only.\nwhether to filter out adult or unsafe content from results. Not supported for `fast` or `ultra-fast` search depths."}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Search results returned successfully"}
    - {"type":"paragraph","content":"The search query that was executed."}
    - {"type":"paragraph","content":"`\"Who is Leo Messi?\"`"}
    - {"type":"paragraph","content":"A short answer to the user's query, generated by an LLM. Included in the response only if `include_answer` is requested (i.e., set to `true`, `basic`, or `advanced`)"}
    - {"type":"paragraph","content":"`\"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\"`"}
    - {"type":"paragraph","content":"List of query-related images. If `include_image_descriptions` is true, each item will have `url` and `description`."}
    - {"type":"codeblock","language":"","content":"[]"}
    - {"type":"paragraph","content":"A list of sorted search results, ranked by relevancy."}
    - {"type":"paragraph","content":"Time in seconds it took to complete the request."}
    - {"type":"paragraph","content":"`\"1.67\"`"}
    - {"type":"paragraph","content":"A dictionary of the selected auto_parameters, only shown when `auto_parameters` is true."}
    - {"type":"codeblock","language":"","content":"{  \"topic\": \"general\",  \"search_depth\": \"basic\"}"}
    - {"type":"paragraph","content":"Credit usage details for the request."}
    - {"type":"codeblock","language":"","content":"{ \"credits\": 1 }"}
    - {"type":"paragraph","content":"A unique request identifier you can share with customer support to help resolve issues with specific requests."}
    - {"type":"paragraph","content":"`\"123e4567-e89b-12d3-a456-426614174111\"`"}
    - {"type":"image","src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","alt":"tavily-logo","title":"","index":1,"localPath":"Welcome_-_Tavily_Docs/image_1.png"}
    - {"type":"heading","level":2,"content":"Privacy Preference Center"}
    - {"type":"heading","level":3,"content":"Manage Consent Preferences"}
    - {"type":"heading","level":4,"content":"Strictly Necessary Cookies"}
    - {"type":"paragraph","content":"These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information."}
    - {"type":"heading","level":4,"content":"Functional Cookies"}
    - {"type":"paragraph","content":"These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly."}
    - {"type":"heading","level":4,"content":"Performance Cookies"}
    - {"type":"paragraph","content":"These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance."}
    - {"type":"heading","level":4,"content":"Targeting Cookies"}
    - {"type":"paragraph","content":"These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising."}
    - {"type":"heading","level":3,"content":"Cookie List"}
    - {"type":"list","listType":"ul","items":["checkbox label label"]}
  paragraphs:
    - "Python"
    - "Execute a search query using Tavily Search."
    - "Python"
    - "Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."
    - "Parameters for the Tavily Search request."
    - "The search query to execute with Tavily."
    - "`\"who is Leo Messi?\"`"
    - "Controls the latency vs. relevance tradeoff and how `results[].content` is generated:"
    - "Cost:"
    - "See [Search Best Practices](https://docs.tavily.com/documentation/best-practices/best-practices-search#search-depth) for guidance on choosing the right search depth."
    - "Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use `chunks_per_source` to define the maximum number of relevant chunks returned per source and to control the `content` length. Chunks will appear in the `content` field as: `<chunk 1> [...] <chunk 2> [...] <chunk 3>`. Available only when `search_depth` is `advanced`."
    - "The maximum number of search results to return."
    - "`1`"
    - "The category of the search.`news` is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. `general` is for broader, more general-purpose searches that may include a wide range of sources."
    - "The time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data."
    - "Will return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD"
    - "`\"2025-02-09\"`"
    - "Will return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD"
    - "`\"2025-12-29\"`"
    - "Include an LLM-generated answer to the provided query. `basic` or `true` returns a quick answer. `advanced` returns a more detailed answer."
    - "Include the cleaned and parsed HTML content of each search result. `markdown` or `true` returns search result content in markdown format. `text` returns the plain text from the results and may increase latency."
    - "Also perform an image search and include the results in the response."
    - "When `include_images` is `true`, also add a descriptive text for each image."
    - "Whether to include the favicon URL for each result."
    - "A list of domains to specifically include in the search results. Maximum 300 domains."
    - "A list of domains to specifically exclude from the search results. Maximum 150 domains."
    - "Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is `general`."
    - "When `auto_parameters` is enabled, Tavily automatically configures search parameters based on your query's content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones. The parameters `include_answer`, `include_raw_content`, and `max_results` must always be set manually, as they directly affect response size. Note: `search_depth` may be automatically set to advanced when it's likely to improve results. This uses 2 API credits per request. To avoid the extra cost, you can explicitly set `search_depth` to `basic`."
    - "Ensure that only search results containing the exact quoted phrase(s) in the query are returned, bypassing synonyms or semantic variations. Wrap target phrases in quotes within your query (e.g. `\"John Smith\" CEO Acme Corp`). Punctuation is typically ignored inside quotes."
    - "Whether to include credit usage information in the response."
    - "🔒 Enterprise only.\nwhether to filter out adult or unsafe content from results. Not supported for `fast` or `ultra-fast` search depths."
    - "Search results returned successfully"
    - "The search query that was executed."
    - "`\"Who is Leo Messi?\"`"
    - "A short answer to the user's query, generated by an LLM. Included in the response only if `include_answer` is requested (i.e., set to `true`, `basic`, or `advanced`)"
    - "`\"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\"`"
    - "List of query-related images. If `include_image_descriptions` is true, each item will have `url` and `description`."
    - "Show child attributes"
    - "A list of sorted search results, ranked by relevancy."
    - "Show child attributes"
    - "Time in seconds it took to complete the request."
    - "`\"1.67\"`"
    - "A dictionary of the selected auto_parameters, only shown when `auto_parameters` is true."
    - "Credit usage details for the request."
    - "A unique request identifier you can share with customer support to help resolve issues with specific requests."
    - "`\"123e4567-e89b-12d3-a456-426614174111\"`"
    - "Resources"
    - "Legal"
    - "These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information."
    - "These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly."
    - "These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance."
    - "These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising."
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/api-reference/introduction)","[POSTSearch](https://docs.tavily.com/documentation/api-reference/endpoint/search)","[POSTExtract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)","[POSTCrawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)","[POSTMap](https://docs.tavily.com/documentation/api-reference/endpoint/map)","Research","[GETUsage](https://docs.tavily.com/documentation/api-reference/endpoint/usage)"]}
    - {"type":"ul","items":["API Key Generator"]}
    - {"type":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/python/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/python/reference)"]}
    - {"type":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/javascript/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/javascript/reference)"]}
    - {"type":"ul","items":["[Search](https://docs.tavily.com/documentation/best-practices/best-practices-search)","[Extract](https://docs.tavily.com/documentation/best-practices/best-practices-extract)","[Crawl](https://docs.tavily.com/documentation/best-practices/best-practices-crawl)","[Research](https://docs.tavily.com/documentation/best-practices/best-practices-research)","[API Key Management](https://docs.tavily.com/documentation/best-practices/api-key-management)"]}
    - {"type":"ul","items":["advanced: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).","basic: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.","fast: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).","ultra-fast: Minimizes latency above all else. Best for time-critical use cases. Returns one NLP summary per URL."]}
    - {"type":"ul","items":["basic, fast, ultra-fast: 1 API Credit","advanced: 2 API Credits"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"json","code":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"json","code":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"json","code":"[]"}
    - {"language":"json","code":"[]"}
    - {"language":"json","code":"{  \"topic\": \"general\",  \"search_depth\": \"basic\"}"}
    - {"language":"json","code":"{  \"topic\": \"general\",  \"search_depth\": \"basic\"}"}
    - {"language":"json","code":"{ \"credits\": 1 }"}
    - {"language":"json","code":"{ \"credits\": 1 }"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Welcome_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Welcome_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Welcome_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Welcome_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Welcome_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Welcome_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Welcome_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Welcome_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Welcome_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Welcome_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Welcome_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Welcome_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Welcome_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Welcome_-_Tavily_Docs/svg_17.png","width":16,"height":16}
    - {"type":"svg","index":18,"filename":"Welcome_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":19,"filename":"Welcome_-_Tavily_Docs/svg_19.png","width":16,"height":16}
    - {"type":"svg","index":20,"filename":"Welcome_-_Tavily_Docs/svg_20.png","width":16,"height":16}
    - {"type":"svg","index":21,"filename":"Welcome_-_Tavily_Docs/svg_21.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Welcome_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Welcome_-_Tavily_Docs/svg_23.png","width":16,"height":16}
    - {"type":"svg","index":24,"filename":"Welcome_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Welcome_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Welcome_-_Tavily_Docs/svg_26.png","width":14,"height":14}
    - {"type":"svg","index":27,"filename":"Welcome_-_Tavily_Docs/svg_27.png","width":14,"height":14}
    - {"type":"svg","index":28,"filename":"Welcome_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":29,"filename":"Welcome_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Welcome_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"Welcome_-_Tavily_Docs/svg_39.png","width":18,"height":18}
    - {"type":"svg","index":40,"filename":"Welcome_-_Tavily_Docs/svg_40.png","width":18,"height":18}
    - {"type":"svg","index":41,"filename":"Welcome_-_Tavily_Docs/svg_41.png","width":18,"height":18}
    - {"type":"svg","index":42,"filename":"Welcome_-_Tavily_Docs/svg_42.png","width":18,"height":18}
    - {"type":"svg","index":43,"filename":"Welcome_-_Tavily_Docs/svg_43.png","width":18,"height":18}
    - {"type":"svg","index":44,"filename":"Welcome_-_Tavily_Docs/svg_44.png","width":18,"height":18}
    - {"type":"svg","index":45,"filename":"Welcome_-_Tavily_Docs/svg_45.png","width":18,"height":18}
    - {"type":"svg","index":46,"filename":"Welcome_-_Tavily_Docs/svg_46.png","width":18,"height":18}
    - {"type":"svg","index":47,"filename":"Welcome_-_Tavily_Docs/svg_47.png","width":18,"height":18}
    - {"type":"svg","index":48,"filename":"Welcome_-_Tavily_Docs/svg_48.png","width":18,"height":18}
    - {"type":"svg","index":49,"filename":"Welcome_-_Tavily_Docs/svg_49.png","width":10,"height":10}
    - {"type":"svg","index":50,"filename":"Welcome_-_Tavily_Docs/svg_50.png","width":18,"height":18}
    - {"type":"svg","index":51,"filename":"Welcome_-_Tavily_Docs/svg_51.png","width":10,"height":10}
    - {"type":"svg","index":52,"filename":"Welcome_-_Tavily_Docs/svg_52.png","width":18,"height":18}
    - {"type":"svg","index":53,"filename":"Welcome_-_Tavily_Docs/svg_53.png","width":18,"height":18}
    - {"type":"svg","index":54,"filename":"Welcome_-_Tavily_Docs/svg_54.png","width":18,"height":18}
    - {"type":"svg","index":55,"filename":"Welcome_-_Tavily_Docs/svg_55.png","width":18,"height":18}
    - {"type":"svg","index":56,"filename":"Welcome_-_Tavily_Docs/svg_56.png","width":18,"height":18}
    - {"type":"svg","index":57,"filename":"Welcome_-_Tavily_Docs/svg_57.png","width":18,"height":18}
    - {"type":"svg","index":58,"filename":"Welcome_-_Tavily_Docs/svg_58.png","width":18,"height":18}
    - {"type":"svg","index":59,"filename":"Welcome_-_Tavily_Docs/svg_59.png","width":18,"height":18}
    - {"type":"svg","index":60,"filename":"Welcome_-_Tavily_Docs/svg_60.png","width":18,"height":18}
    - {"type":"svg","index":61,"filename":"Welcome_-_Tavily_Docs/svg_61.png","width":18,"height":18}
    - {"type":"svg","index":62,"filename":"Welcome_-_Tavily_Docs/svg_62.png","width":10,"height":10}
    - {"type":"svg","index":63,"filename":"Welcome_-_Tavily_Docs/svg_63.png","width":18,"height":18}
    - {"type":"svg","index":64,"filename":"Welcome_-_Tavily_Docs/svg_64.png","width":18,"height":18}
    - {"type":"svg","index":65,"filename":"Welcome_-_Tavily_Docs/svg_65.png","width":18,"height":18}
    - {"type":"svg","index":66,"filename":"Welcome_-_Tavily_Docs/svg_66.png","width":10,"height":10}
    - {"type":"svg","index":67,"filename":"Welcome_-_Tavily_Docs/svg_67.png","width":18,"height":18}
    - {"type":"svg","index":68,"filename":"Welcome_-_Tavily_Docs/svg_68.png","width":10,"height":10}
    - {"type":"svg","index":69,"filename":"Welcome_-_Tavily_Docs/svg_69.png","width":18,"height":18}
    - {"type":"svg","index":70,"filename":"Welcome_-_Tavily_Docs/svg_70.png","width":18,"height":18}
    - {"type":"svg","index":71,"filename":"Welcome_-_Tavily_Docs/svg_71.png","width":18,"height":18}
    - {"type":"svg","index":72,"filename":"Welcome_-_Tavily_Docs/svg_72.png","width":18,"height":18}
    - {"type":"svg","index":73,"filename":"Welcome_-_Tavily_Docs/svg_73.png","width":14,"height":14}
    - {"type":"svg","index":74,"filename":"Welcome_-_Tavily_Docs/svg_74.png","width":14,"height":14}
    - {"type":"svg","index":75,"filename":"Welcome_-_Tavily_Docs/svg_75.png","width":14,"height":14}
    - {"type":"svg","index":80,"filename":"Welcome_-_Tavily_Docs/svg_80.png","width":20,"height":20}
    - {"type":"svg","index":81,"filename":"Welcome_-_Tavily_Docs/svg_81.png","width":20,"height":20}
    - {"type":"svg","index":82,"filename":"Welcome_-_Tavily_Docs/svg_82.png","width":20,"height":20}
    - {"type":"svg","index":83,"filename":"Welcome_-_Tavily_Docs/svg_83.png","width":20,"height":20}
    - {"type":"svg","index":84,"filename":"Welcome_-_Tavily_Docs/svg_84.png","width":49,"height":14}
    - {"type":"svg","index":85,"filename":"Welcome_-_Tavily_Docs/svg_85.png","width":16,"height":16}
    - {"type":"svg","index":86,"filename":"Welcome_-_Tavily_Docs/svg_86.png","width":16,"height":16}
    - {"type":"svg","index":87,"filename":"Welcome_-_Tavily_Docs/svg_87.png","width":16,"height":16}
  chartData: []
  blockquotes: []
  definitionLists: []
  horizontalRules: 0
  videos: []
  audios: []
  apiData: 0
  pageFeatures:
    suggestedType: "api-doc"
    confidence: 75
    signals:
      - "article-like"
      - "api-doc-like"
      - "api-endpoints"
  tabsAndDropdowns: []
  dateFilters: []
---

# Tavily Search

## 源URL

https://docs.tavily.com/

## 描述

Execute a search query using Tavily Search.

## 内容

- [API Playground](https://app.tavily.com/playground)
- [Community](https://discord.gg/TPu2gkaWp2)
- [Blog](https://tavily.com/blog)

###### API Reference

- [Introduction](https://docs.tavily.com/documentation/api-reference/introduction)
- [POSTSearch](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [POSTExtract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)
- [POSTCrawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)
- [POSTMap](https://docs.tavily.com/documentation/api-reference/endpoint/map)
- Research
- [GETUsage](https://docs.tavily.com/documentation/api-reference/endpoint/usage)

###### Enterprise API Reference

- API Key Generator

###### Python SDK

- [Quickstart](https://docs.tavily.com/sdk/python/quick-start)
- [SDK Reference](https://docs.tavily.com/sdk/python/reference)

###### JavaScript SDK

- [Quickstart](https://docs.tavily.com/sdk/javascript/quick-start)
- [SDK Reference](https://docs.tavily.com/sdk/javascript/reference)

###### Best Practices

- [Search](https://docs.tavily.com/documentation/best-practices/best-practices-search)
- [Extract](https://docs.tavily.com/documentation/best-practices/best-practices-extract)
- [Crawl](https://docs.tavily.com/documentation/best-practices/best-practices-crawl)
- [Research](https://docs.tavily.com/documentation/best-practices/best-practices-research)
- [API Key Management](https://docs.tavily.com/documentation/best-practices/api-key-management)

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.search("Who is Leo Messi?")

print(response)
```

```text
{
  "query": "Who is Leo Messi?",
  "answer": "Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.",
  "images": [],
  "results": [
    {
      "title": "Lionel Messi Facts | Britannica",
      "url": "https://www.britannica.com/facts/Lionel-Messi",
      "content": "Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal",
      "score": 0.81025416,
      "raw_content": null,
      "favicon": "https://britannica.com/favicon.png"
    }
  ],
  "response_time": "1.67",
  "auto_parameters": {
    "topic": "general",
    "search_depth": "basic"
  },
  "usage": {
    "credits": 1
  },
  "request_id": "123e4567-e89b-12d3-a456-426614174111"
}
```

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.search("Who is Leo Messi?")

print(response)
```

```text
{
  "query": "Who is Leo Messi?",
  "answer": "Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.",
  "images": [],
  "results": [
    {
      "title": "Lionel Messi Facts | Britannica",
      "url": "https://www.britannica.com/facts/Lionel-Messi",
      "content": "Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal",
      "score": 0.81025416,
      "raw_content": null,
      "favicon": "https://britannica.com/favicon.png"
    }
  ],
  "response_time": "1.67",
  "auto_parameters": {
    "topic": "general",
    "search_depth": "basic"
  },
  "usage": {
    "credits": 1
  },
  "request_id": "123e4567-e89b-12d3-a456-426614174111"
}
```

##### Authorizations

Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

##### Body

Parameters for the Tavily Search request.

The search query to execute with Tavily.

`"who is Leo Messi?"`

Controls the latency vs. relevance tradeoff and how `results[].content` is generated:

- `advanced`: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via `chunks_per_source`).
- `basic`: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.
- `fast`: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant snippets per URL (configurable via `chunks_per_source`).
- `ultra-fast`: Minimizes latency above all else. Best for time-critical use cases. Returns one NLP summary per URL.

Cost:

- `basic`, `fast`, `ultra-fast`: 1 API Credit
- `advanced`: 2 API Credits

See [Search Best Practices](https://docs.tavily.com/documentation/best-practices/best-practices-search#search-depth) for guidance on choosing the right search depth.

Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use `chunks_per_source` to define the maximum number of relevant chunks returned per source and to control the `content` length. Chunks will appear in the `content` field as: `<chunk 1> [...] <chunk 2> [...] <chunk 3>`. Available only when `search_depth` is `advanced`.

The maximum number of search results to return.

`1`

The category of the search.`news` is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. `general` is for broader, more general-purpose searches that may include a wide range of sources.

The time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data.

Will return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD

`"2025-02-09"`

Will return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD

`"2025-12-29"`

Include an LLM-generated answer to the provided query. `basic` or `true` returns a quick answer. `advanced` returns a more detailed answer.

Include the cleaned and parsed HTML content of each search result. `markdown` or `true` returns search result content in markdown format. `text` returns the plain text from the results and may increase latency.

Also perform an image search and include the results in the response.

When `include_images` is `true`, also add a descriptive text for each image.

Whether to include the favicon URL for each result.

A list of domains to specifically include in the search results. Maximum 300 domains.

A list of domains to specifically exclude from the search results. Maximum 150 domains.

Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is `general`.

When `auto_parameters` is enabled, Tavily automatically configures search parameters based on your query's content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones. The parameters `include_answer`, `include_raw_content`, and `max_results` must always be set manually, as they directly affect response size. Note: `search_depth` may be automatically set to advanced when it's likely to improve results. This uses 2 API credits per request. To avoid the extra cost, you can explicitly set `search_depth` to `basic`.

Ensure that only search results containing the exact quoted phrase(s) in the query are returned, bypassing synonyms or semantic variations. Wrap target phrases in quotes within your query (e.g. `"John Smith" CEO Acme Corp`). Punctuation is typically ignored inside quotes.

Whether to include credit usage information in the response.

🔒 Enterprise only.
whether to filter out adult or unsafe content from results. Not supported for `fast` or `ultra-fast` search depths.

##### Response

Search results returned successfully

The search query that was executed.

`"Who is Leo Messi?"`

A short answer to the user's query, generated by an LLM. Included in the response only if `include_answer` is requested (i.e., set to `true`, `basic`, or `advanced`)

`"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport."`

List of query-related images. If `include_image_descriptions` is true, each item will have `url` and `description`.

```text
[]
```

A list of sorted search results, ranked by relevancy.

Time in seconds it took to complete the request.

`"1.67"`

A dictionary of the selected auto_parameters, only shown when `auto_parameters` is true.

```text
{  "topic": "general",  "search_depth": "basic"}
```

Credit usage details for the request.

```text
{ "credits": 1 }
```

A unique request identifier you can share with customer support to help resolve issues with specific requests.

`"123e4567-e89b-12d3-a456-426614174111"`

![tavily-logo](Welcome_-_Tavily_Docs/image_1.png)

### Privacy Preference Center

#### Manage Consent Preferences

##### Strictly Necessary Cookies

These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information.

##### Functional Cookies

These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly.

##### Performance Cookies

These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance.

##### Targeting Cookies

These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising.

#### Cookie List

- checkbox label label

## 图片

![light logo](Welcome_-_Tavily_Docs/image_1.svg)

![dark logo](Welcome_-_Tavily_Docs/image_2.svg)

![light logo](Welcome_-_Tavily_Docs/image_3.svg)

![dark logo](Welcome_-_Tavily_Docs/image_4.svg)

![tavily-logo](Welcome_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Welcome_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Welcome_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Welcome_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Welcome_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Welcome_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Welcome_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Welcome_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Welcome_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 17](Welcome_-_Tavily_Docs/svg_17.png)
*尺寸: 16x16px*

![SVG图表 18](Welcome_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 19](Welcome_-_Tavily_Docs/svg_19.png)
*尺寸: 16x16px*

![SVG图表 20](Welcome_-_Tavily_Docs/svg_20.png)
*尺寸: 16x16px*

![SVG图表 21](Welcome_-_Tavily_Docs/svg_21.png)
*尺寸: 16x16px*

![SVG图表 22](Welcome_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](Welcome_-_Tavily_Docs/svg_23.png)
*尺寸: 16x16px*

![SVG图表 24](Welcome_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Welcome_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Welcome_-_Tavily_Docs/svg_26.png)
*尺寸: 14x14px*

![SVG图表 27](Welcome_-_Tavily_Docs/svg_27.png)
*尺寸: 14x14px*

![SVG图表 28](Welcome_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 29](Welcome_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Welcome_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 39](Welcome_-_Tavily_Docs/svg_39.png)
*尺寸: 18x18px*

![SVG图表 40](Welcome_-_Tavily_Docs/svg_40.png)
*尺寸: 18x18px*

![SVG图表 41](Welcome_-_Tavily_Docs/svg_41.png)
*尺寸: 18x18px*

![SVG图表 42](Welcome_-_Tavily_Docs/svg_42.png)
*尺寸: 18x18px*

![SVG图表 43](Welcome_-_Tavily_Docs/svg_43.png)
*尺寸: 18x18px*

![SVG图表 44](Welcome_-_Tavily_Docs/svg_44.png)
*尺寸: 18x18px*

![SVG图表 45](Welcome_-_Tavily_Docs/svg_45.png)
*尺寸: 18x18px*

![SVG图表 46](Welcome_-_Tavily_Docs/svg_46.png)
*尺寸: 18x18px*

![SVG图表 47](Welcome_-_Tavily_Docs/svg_47.png)
*尺寸: 18x18px*

![SVG图表 48](Welcome_-_Tavily_Docs/svg_48.png)
*尺寸: 18x18px*

![SVG图表 49](Welcome_-_Tavily_Docs/svg_49.png)
*尺寸: 10x10px*

![SVG图表 50](Welcome_-_Tavily_Docs/svg_50.png)
*尺寸: 18x18px*

![SVG图表 51](Welcome_-_Tavily_Docs/svg_51.png)
*尺寸: 10x10px*

![SVG图表 52](Welcome_-_Tavily_Docs/svg_52.png)
*尺寸: 18x18px*

![SVG图表 53](Welcome_-_Tavily_Docs/svg_53.png)
*尺寸: 18x18px*

![SVG图表 54](Welcome_-_Tavily_Docs/svg_54.png)
*尺寸: 18x18px*

![SVG图表 55](Welcome_-_Tavily_Docs/svg_55.png)
*尺寸: 18x18px*

![SVG图表 56](Welcome_-_Tavily_Docs/svg_56.png)
*尺寸: 18x18px*

![SVG图表 57](Welcome_-_Tavily_Docs/svg_57.png)
*尺寸: 18x18px*

![SVG图表 58](Welcome_-_Tavily_Docs/svg_58.png)
*尺寸: 18x18px*

![SVG图表 59](Welcome_-_Tavily_Docs/svg_59.png)
*尺寸: 18x18px*

![SVG图表 60](Welcome_-_Tavily_Docs/svg_60.png)
*尺寸: 18x18px*

![SVG图表 61](Welcome_-_Tavily_Docs/svg_61.png)
*尺寸: 18x18px*

![SVG图表 62](Welcome_-_Tavily_Docs/svg_62.png)
*尺寸: 10x10px*

![SVG图表 63](Welcome_-_Tavily_Docs/svg_63.png)
*尺寸: 18x18px*

![SVG图表 64](Welcome_-_Tavily_Docs/svg_64.png)
*尺寸: 18x18px*

![SVG图表 65](Welcome_-_Tavily_Docs/svg_65.png)
*尺寸: 18x18px*

![SVG图表 66](Welcome_-_Tavily_Docs/svg_66.png)
*尺寸: 10x10px*

![SVG图表 67](Welcome_-_Tavily_Docs/svg_67.png)
*尺寸: 18x18px*

![SVG图表 68](Welcome_-_Tavily_Docs/svg_68.png)
*尺寸: 10x10px*

![SVG图表 69](Welcome_-_Tavily_Docs/svg_69.png)
*尺寸: 18x18px*

![SVG图表 70](Welcome_-_Tavily_Docs/svg_70.png)
*尺寸: 18x18px*

![SVG图表 71](Welcome_-_Tavily_Docs/svg_71.png)
*尺寸: 18x18px*

![SVG图表 72](Welcome_-_Tavily_Docs/svg_72.png)
*尺寸: 18x18px*

![SVG图表 73](Welcome_-_Tavily_Docs/svg_73.png)
*尺寸: 14x14px*

![SVG图表 74](Welcome_-_Tavily_Docs/svg_74.png)
*尺寸: 14x14px*

![SVG图表 75](Welcome_-_Tavily_Docs/svg_75.png)
*尺寸: 14x14px*

![SVG图表 80](Welcome_-_Tavily_Docs/svg_80.png)
*尺寸: 20x20px*

![SVG图表 81](Welcome_-_Tavily_Docs/svg_81.png)
*尺寸: 20x20px*

![SVG图表 82](Welcome_-_Tavily_Docs/svg_82.png)
*尺寸: 20x20px*

![SVG图表 83](Welcome_-_Tavily_Docs/svg_83.png)
*尺寸: 20x20px*

![SVG图表 84](Welcome_-_Tavily_Docs/svg_84.png)
*尺寸: 49x14px*

![SVG图表 85](Welcome_-_Tavily_Docs/svg_85.png)
*尺寸: 16x16px*

![SVG图表 86](Welcome_-_Tavily_Docs/svg_86.png)
*尺寸: 16x16px*

![SVG图表 87](Welcome_-_Tavily_Docs/svg_87.png)
*尺寸: 16x16px*
