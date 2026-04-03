---
id: "url-1cd83aeb"
type: "api"
title: "Tavily Search"
url: "https://docs.tavily.com/documentation/api-reference/endpoint/search"
description: "Execute a search query using Tavily Search."
source: ""
tags: []
crawl_time: "2026-03-18T07:17:02.887Z"
metadata:
  method: "POST"
  endpoint: "/search"
  baseUrl: "https://api.tavily.com"
  parameters:
    - {"name":"Authorization","type":"string","required":true,"default":"","description":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).","location":"header"}
    - {"name":"query","type":"string","required":true,"default":"","description":"The search query to execute with Tavily.Example:\"who is Leo Messi?\""}
    - {"name":"search_depth","type":"enum<string>","required":false,"default":"basic","description":"Controls the latency vs. relevance tradeoff and how results[].content is generated:\n\nadvanced: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).\nbasic: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.\nfast: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant "}
    - {"name":"chunks_per_source","type":"integer","required":false,"default":"","description":"default:3Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length. Chunks will appear in the content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when search_depth is advanced.Required range: 1 <= x <= 3"}
    - {"name":"max_results","type":"integer","required":false,"default":"","description":"default:5The maximum number of search results to return.Required range: 0 <= x <= 20Example:1"}
    - {"name":"topic","type":"enum<string>","required":false,"default":"general","description":"The category of the search.news is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. general is for broader, more general-purpose searches that may include a wide range of sources.Available options: general, news, finance"}
    - {"name":"time_range","type":"enum<string>","required":false,"default":"","description":"The time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data.Available options: day, week, month, year, d, w, m, y"}
    - {"name":"start_date","type":"string","required":false,"default":"","description":"Will return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DDExample:\"2025-02-09\""}
    - {"name":"end_date","type":"string","required":false,"default":"","description":"Will return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DDExample:\"2025-12-29\""}
    - {"name":"include_answer","type":"","required":false,"default":"","description":""}
    - {"name":"include_raw_content","type":"","required":false,"default":"","description":""}
    - {"name":"include_images","type":"boolean","required":false,"default":"","description":"default:falseAlso perform an image search and include the results in the response."}
    - {"name":"include_image_descriptions","type":"boolean","required":false,"default":"","description":"default:falseWhen include_images is true, also add a descriptive text for each image."}
    - {"name":"include_favicon","type":"boolean","required":false,"default":"","description":"default:falseWhether to include the favicon URL for each result."}
    - {"name":"country","type":"enum<string>","required":false,"default":"","description":"Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general.Available options: afghanistan, albania, algeria, andorra, angola, argentina, armenia, australia, austria, azerbaijan, bahamas, bahrain, bangladesh, barbados, belarus, belgium, belize, benin, bhutan, bolivia, bosnia and herzegovina, botswana, brazil, brunei, bulgaria, burkina faso, burundi, cambodia, cameroon, canada, cape verde, central a"}
    - {"name":"auto_parameters","type":"boolean","required":false,"default":"","description":"default:falseWhen auto_parameters is enabled, Tavily automatically configures search parameters based on your query's content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones. The parameters include_answer, include_raw_content, and max_results must always be set manually, as they directly affect response size. Note: search_depth may be automatically set to advanced when it's likely to improve results. This uses 2 API credits per r"}
    - {"name":"exact_match","type":"boolean","required":false,"default":"","description":"default:falseEnsure that only search results containing the exact quoted phrase(s) in the query are returned, bypassing synonyms or semantic variations. Wrap target phrases in quotes within your query (e.g. \"John Smith\" CEO Acme Corp). Punctuation is typically ignored inside quotes."}
    - {"name":"include_usage","type":"boolean","required":false,"default":"","description":"default:falseWhether to include credit usage information in the response."}
    - {"name":"safe_search","type":"boolean","required":false,"default":"","description":"default:false🔒 Enterprise only.\nwhether to filter out adult or unsafe content from results. Not supported for fast or ultra-fast search depths."}
    - {"name":"answer","type":"string","required":true,"default":"","description":"A short answer to the user's query, generated by an LLM. Included in the response only if include_answer is requested (i.e., set to true, basic, or advanced)Example:\"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-sc"}
    - {"name":"results.title","type":"string","required":false,"default":"","description":"The title of the search result.Example:\"Lionel Messi Facts | Britannica\""}
    - {"name":"results.url","type":"string","required":false,"default":"","description":"The URL of the search result.Example:\"https://www.britannica.com/facts/Lionel-Messi\""}
    - {"name":"results.content","type":"string","required":false,"default":"","description":"A short description of the search result.Example:\"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\""}
    - {"name":"results.score","type":"number<float>","required":false,"default":"","description":"The relevance score of the search result.Example:0.81025416"}
    - {"name":"results.raw_content","type":"string","required":false,"default":"","description":"The cleaned and parsed HTML content of the search result. Only if include_raw_content is true.Example:null"}
    - {"name":"results.favicon","type":"string","required":false,"default":"","description":"The favicon URL for the result.Example:\"https://britannica.com/favicon.png\""}
    - {"name":"response_time","type":"number<float>","required":true,"default":"","description":"Time in seconds it took to complete the request.Example:\"1.67\""}
    - {"name":"request_id","type":"string","required":false,"default":"","description":"A unique request identifier you can share with customer support to help resolve issues with specific requests.Example:\"123e4567-e89b-12d3-a456-426614174111\""}
    - {"name":"Hide child attributes​images.url","type":"string","required":false,"default":"","description":"images.descriptionstring"}
    - {"name":"Hide child attributes​results.title","type":"string","required":false,"default":"","description":"The title of the search result.Example:\"Lionel Messi Facts | Britannica\"​results.urlstringThe URL of the search result.Example:\"https://www.britannica.com/facts/Lionel-Messi\"​results.contentstringA short description of the search result.Example:\"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champio"}
    - {"name":"usage","type":"object","required":false,"default":"","description":"Credit usage details for the request.Example:{ \"credits\": 1 }"}
    - {"name":"include_domains","type":"string[]","required":false,"default":"","description":"A list of domains to specifically include in the search results. Maximum 300 domains."}
    - {"name":"exclude_domains","type":"string[]","required":false,"default":"","description":"A list of domains to specifically exclude from the search results. Maximum 150 domains."}
    - {"name":"images","type":"object","required":false,"default":"","description":"[]requiredList of query-related images. If include_image_descriptions is true, each item will have url and description.Hide child attributes images.urlstring images.descriptionstringExample:[]"}
    - {"name":"results","type":"object","required":false,"default":"","description":"[]requiredA list of sorted search results, ranked by relevancy.Hide child attributes results.titlestringThe title of the search result.Example:\"Lionel Messi Facts | Britannica\" results.urlstringThe URL of the search result.Example:\"https://www.britannica.com/facts/Lionel-Messi\" results.contentstringA short description of the search result.Example:\"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the maj"}
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"query\": \"Who is Leo Messi?\",\n  \"answer\": \"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\",\n  \"images\": [],\n  \"results\": [\n    {\n      \"title\": \"Lionel Messi Facts | Britannica\",\n      \"url\": \"https://www.britannica.com/facts/Lionel-Messi\",\n      \"content\": \"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\",\n      \"score\": 0.81025416,\n      \"raw_content\": null,\n      \"favicon\": \"https://britannica.com/favicon.png\"\n    }\n  ],\n  \"response_time\": \"1.67\",\n  \"auto_parameters\": {\n    \"topic\": \"general\",\n    \"search_depth\": \"basic\"\n  },\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"json","code":"{  \"topic\": \"general\",  \"search_depth\": \"basic\"}"}
    - {"language":"json","code":"{ \"credits\": 1 }"}
  mainContent:
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Body"}
    - {"type":"paragraph","content":"Parameters for the Tavily Search request."}
    - {"type":"parameter","name":"\"who is Leo Messi?\"","paramType":"","description":"​querystringrequiredThe search query to execute with Tavily.Example:\"who is Leo Messi?\"​search_depthenum<string>default:basicControls the latency vs. relevance tradeoff and how results[].content is generated:\n\nadvanced: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).\nbasic: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.\nfast: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).\nultra-fast: Minimizes latency above all else. Best for time-critical use cases. Returns one NLP summary per URL.\n\nCost:\n\nbasic, fast, ultra-fast: 1 API Credit\nadvanced: 2 API Credits\n\nSee Search Best Practices for guidance on choosing the right search depth.Available options: advanced, basic, fast, ultra-fast ​chunks_per_sourceintegerdefault:3Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length. Chunks will appear in the content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when search_depth is advanced.Required range: 1 <= x <= 3​max_resultsintegerdefault:5The maximum number of search results to return.Required range: 0 <= x <= 20Example:1​topicenum<string>default:generalThe category of the search.news is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. general is for broader, more general-purpose searches that may include a wide range of sources.Available options: general, news, finance ​time_rangeenum<string>The time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data.Available options: day, week, month, year, d, w, m, y ​start_datestringWill return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DDExample:\"2025-02-09\"​end_datestringWill return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DDExample:\"2025-12-29\"​include_answer"}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Search results returned successfully"}
    - {"type":"parameter","name":"\"Who is Leo Messi?\"","paramType":"","description":"​querystringrequiredThe search query that was executed.Example:\"Who is Leo Messi?\"​answerstringrequiredA short answer to the user's query, generated by an LLM. Included in the response only if include_answer is requested (i.e., set to true, basic, or advanced)Example:\"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\"​imagesobject[]requiredList of query-related images. If include_image_descriptions is true, each item will have url and description.Hide child attributes​images.urlstring​images.descriptionstringExample:[]​resultsobject[]requiredA list of sorted search results, ranked by relevancy.Hide child attributes​results.titlestringThe title of the search result.Example:\"Lionel Messi Facts | Britannica\"​results.urlstringThe URL of the search result.Example:\"https://www.britannica.com/facts/Lionel-Messi\"​results.contentstringA short description of the search result.Example:\"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\"​results.scorenumber<float>The relevance score of the search result.Example:0.81025416​results.raw_contentstringThe cleaned and parsed HTML content of the search result. Only if include_raw_content is true.Example:null​results.faviconstringThe favicon URL for the result.Example:\"https://britannica.com/favicon.png\"​response_timenumber<float>requiredTime in seconds it took to complete the request.Example:\"1.67\"​auto_parametersobjectA dictionary of the selected auto_parameters, only shown when auto_parameters is true.Example:{  \"topic\": \"general\",  \"search_depth\": \"basic\"}​usageobjectCredit usage details for the request.Example:{ \"credits\": 1 }​request_idstringA unique request identifier you can share with customer support to help resolve issues with specific requests.Example:\"123e4567-e89b-12d3-a456-426614174111\""}
  rawContent: "Authorizations\n​\nAuthorization\nstringheaderrequired\n\nBearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).\n\nBody\napplication/json\n\nParameters for the Tavily Search request.\n\n​\nquery\nstringrequired\n\nThe search query to execute with Tavily.\n\nExample:\n\n\"who is Leo Messi?\"\n\n​\nsearch_depth\nenum<string>default:basic\n\nControls the latency vs. relevance tradeoff and how results[].content is generated:\n\nadvanced: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).\nbasic: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.\nfast: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).\nultra-fast: Minimizes latency above all else. Best for time-critical use cases. Returns one NLP summary per URL.\n\nCost:\n\nbasic, fast, ultra-fast: 1 API Credit\nadvanced: 2 API Credits\n\nSee Search Best Practices for guidance on choosing the right search depth.\n\nAvailable options: advanced, basic, fast, ultra-fast \n​\nchunks_per_source\nintegerdefault:3\n\nChunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length. Chunks will appear in the content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when search_depth is advanced.\n\nRequired range: 1 <= x <= 3\n​\nmax_results\nintegerdefault:5\n\nThe maximum number of search results to return.\n\nRequired range: 0 <= x <= 20\nExample:\n\n1\n\n​\ntopic\nenum<string>default:general\n\nThe category of the search.news is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. general is for broader, more general-purpose searches that may include a wide range of sources.\n\nAvailable options: general, news, finance \n​\ntime_range\nenum<string>\n\nThe time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data.\n\nAvailable options: day, week, month, year, d, w, m, y \n​\nstart_date\nstring\n\nWill return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD\n\nExample:\n\n\"2025-02-09\"\n\n​\nend_date\nstring\n\nWill return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD\n\nExample:\n\n\"2025-12-29\"\n\n​\ninclude_answer\nboolean\nenum<string>\nboolean\ndefault:false\n\nInclude an LLM-generated answer to the provided query. basic or true returns a quick answer. advanced returns a more detailed answer.\n\n​\ninclude_raw_content\nboolean\nenum<string>\nboolean\ndefault:false\n\nInclude the cleaned and parsed HTML content of each search result. markdown or true returns search result content in markdown format. text returns the plain text from the results and may increase latency.\n\n​\ninclude_images\nbooleandefault:false\n\nAlso perform an image search and include the results in the response.\n\n​\ninclude_image_descriptions\nbooleandefault:false\n\nWhen include_images is true, also add a descriptive text for each image.\n\n​\ninclude_favicon\nbooleandefault:false\n\nWhether to include the favicon URL for each result.\n\n​\ninclude_domains\nstring[]\n\nA list of domains to specifically include in the search results. Maximum 300 domains.\n\n​\nexclude_domains\nstring[]\n\nA list of domains to specifically exclude from the search results. Maximum 150 domains.\n\n​\ncountry\nenum<string>\n\nBoost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general.\n\nAvailable options: afghanistan, albania, algeria, andorra, angola, argentina, armenia, australia, austria, azerbaijan, bahamas, bahrain, bangladesh, barbados, belarus, belgium, belize, benin, bhutan, bolivia, bosnia and herzegovina, botswana, brazil, brunei, bulgaria, burkina faso, burundi, cambodia, cameroon, canada, cape verde, central african republic, chad, chile, china, colombia, comoros, congo, costa rica, croatia, cuba, cyprus, czech republic, denmark, djibouti, dominican republic, ecuador, egypt, el salvador, equatorial guinea, eritrea, estonia, ethiopia, fiji, finland, france, gabon, gambia, georgia, germany, ghana, greece, guatemala, guinea, haiti, honduras, hungary, iceland, india, indonesia, iran, iraq, ireland, israel, italy, jamaica, japan, jordan, kazakhstan, kenya, kuwait, kyrgyzstan, latvia, lebanon, lesotho, liberia, libya, liechtenstein, lithuania, luxembourg, madagascar, malawi, malaysia, maldives, mali, malta, mauritania, mauritius, mexico, moldova, monaco, mongolia, montenegro, morocco, mozambique, myanmar, namibia, nepal, netherlands, new zealand, nicaragua, niger, nigeria, north korea, north macedonia, norway, oman, pakistan, panama, papua new guinea, paraguay, peru, philippines, poland, portugal, qatar, romania, russia, rwanda, saudi arabia, senegal, serbia, singapore, slovakia, slovenia, somalia, south africa, south korea, south sudan, spain, sri lanka, sudan, sweden, switzerland, syria, taiwan, tajikistan, tanzania, thailand, togo, trinidad and tobago, tunisia, turkey, turkmenistan, uganda, ukraine, united arab emirates, united kingdom, united states, uruguay, uzbekistan, venezuela, vietnam, yemen, zambia, zimbabwe \n​\nauto_parameters\nbooleandefault:false\n\nWhen auto_parameters is enabled, Tavily automatically configures search parameters based on your query's content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones. The parameters include_answer, include_raw_content, and max_results must always be set manually, as they directly affect response size. Note: search_depth may be automatically set to advanced when it's likely to improve results. This uses 2 API credits per request. To avoid the extra cost, you can explicitly set search_depth to basic.\n\n​\nexact_match\nbooleandefault:false\n\nEnsure that only search results containing the exact quoted phrase(s) in the query are returned, bypassing synonyms or semantic variations. Wrap target phrases in quotes within your query (e.g. \"John Smith\" CEO Acme Corp). Punctuation is typically ignored inside quotes.\n\n​\ninclude_usage\nbooleandefault:false\n\nWhether to include credit usage information in the response.\n\n​\nsafe_search\nbooleandefault:false\n\n🔒 Enterprise only.\nwhether to filter out adult or unsafe content from results. Not supported for fast or ultra-fast search depths.\n\nResponse\n200\napplication/json\n\nSearch results returned successfully\n\n​\nquery\nstringrequired\n\nThe search query that was executed.\n\nExample:\n\n\"Who is Leo Messi?\"\n\n​\nanswer\nstringrequired\n\nA short answer to the user's query, generated by an LLM. Included in the response only if include_answer is requested (i.e., set to true, basic, or advanced)\n\nExample:\n\n\"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-scoring ability. He has won multiple FIFA Ballon d'Or awards, numerous La Liga titles with Barcelona, and holds the record for most goals scored in a calendar year. In 2014, he led Argentina to the World Cup final, and in 2015, he helped Barcelona capture another treble. Despite turning 36 in June, Messi remains highly influential in the sport.\"\n\n​\nimages\nobject[]required\n\nList of query-related images. If include_image_descriptions is true, each item will have url and description.\n\nHide child attributes\n\n​\nimages.url\nstring\n​\nimages.description\nstring\nExample:\n[]\n​\nresults\nobject[]required\n\nA list of sorted search results, ranked by relevancy.\n\nHide child attributes\n\n​\nresults.title\nstring\n\nThe title of the search result.\n\nExample:\n\n\"Lionel Messi Facts | Britannica\"\n\n​\nresults.url\nstring\n\nThe URL of the search result.\n\nExample:\n\n\"https://www.britannica.com/facts/Lionel-Messi\"\n\n​\nresults.content\nstring\n\nA short description of the search result.\n\nExample:\n\n\"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal\"\n\n​\nresults.score\nnumber<float>\n\nThe relevance score of the search result.\n\nExample:\n\n0.81025416\n\n​\nresults.raw_content\nstring\n\nThe cleaned and parsed HTML content of the search result. Only if include_raw_content is true.\n\nExample:\n\nnull\n\n​\nresults.favicon\nstring\n\nThe favicon URL for the result.\n\nExample:\n\n\"https://britannica.com/favicon.png\"\n\n​\nresponse_time\nnumber<float>required\n\nTime in seconds it took to complete the request.\n\nExample:\n\n\"1.67\"\n\n​\nauto_parameters\nobject\n\nA dictionary of the selected auto_parameters, only shown when auto_parameters is true.\n\nExample:\n{\n  \"topic\": \"general\",\n  \"search_depth\": \"basic\"\n}\n​\nusage\nobject\n\nCredit usage details for the request.\n\nExample:\n{ \"credits\": 1 }\n​\nrequest_id\nstring\n\nA unique request identifier you can share with customer support to help resolve issues with specific requests.\n\nExample:\n\n\"123e4567-e89b-12d3-a456-426614174111\""
  suggestedFilename: "endpoint_search"
---

# Tavily Search

## 源URL

https://docs.tavily.com/documentation/api-reference/endpoint/search

## 描述

Execute a search query using Tavily Search.

## API 端点

**Method**: `POST`
**Endpoint**: `/search`
**Base URL**: `https://api.tavily.com`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Authorization` | string | 是 | - | Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY). |
| `query` | string | 是 | - | The search query to execute with Tavily.Example:"who is Leo Messi?" |
| `search_depth` | enum<string> | 否 | basic | Controls the latency vs. relevance tradeoff and how results[].content is generated:<br><br>advanced: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).<br>basic: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.<br>fast: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant  |
| `chunks_per_source` | integer | 否 | - | default:3Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length. Chunks will appear in the content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when search_depth is advanced.Required range: 1 <= x <= 3 |
| `max_results` | integer | 否 | - | default:5The maximum number of search results to return.Required range: 0 <= x <= 20Example:1 |
| `topic` | enum<string> | 否 | general | The category of the search.news is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. general is for broader, more general-purpose searches that may include a wide range of sources.Available options: general, news, finance |
| `time_range` | enum<string> | 否 | - | The time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data.Available options: day, week, month, year, d, w, m, y |
| `start_date` | string | 否 | - | Will return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DDExample:"2025-02-09" |
| `end_date` | string | 否 | - | Will return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DDExample:"2025-12-29" |
| `include_answer` | - | 否 | - | - |
| `include_raw_content` | - | 否 | - | - |
| `include_images` | boolean | 否 | - | default:falseAlso perform an image search and include the results in the response. |
| `include_image_descriptions` | boolean | 否 | - | default:falseWhen include_images is true, also add a descriptive text for each image. |
| `include_favicon` | boolean | 否 | - | default:falseWhether to include the favicon URL for each result. |
| `country` | enum<string> | 否 | - | Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general.Available options: afghanistan, albania, algeria, andorra, angola, argentina, armenia, australia, austria, azerbaijan, bahamas, bahrain, bangladesh, barbados, belarus, belgium, belize, benin, bhutan, bolivia, bosnia and herzegovina, botswana, brazil, brunei, bulgaria, burkina faso, burundi, cambodia, cameroon, canada, cape verde, central a |
| `auto_parameters` | boolean | 否 | - | default:falseWhen auto_parameters is enabled, Tavily automatically configures search parameters based on your query's content and intent. You can still set other parameters manually, and your explicit values will override the automatic ones. The parameters include_answer, include_raw_content, and max_results must always be set manually, as they directly affect response size. Note: search_depth may be automatically set to advanced when it's likely to improve results. This uses 2 API credits per r |
| `exact_match` | boolean | 否 | - | default:falseEnsure that only search results containing the exact quoted phrase(s) in the query are returned, bypassing synonyms or semantic variations. Wrap target phrases in quotes within your query (e.g. "John Smith" CEO Acme Corp). Punctuation is typically ignored inside quotes. |
| `include_usage` | boolean | 否 | - | default:falseWhether to include credit usage information in the response. |
| `safe_search` | boolean | 否 | - | default:false🔒 Enterprise only.<br>whether to filter out adult or unsafe content from results. Not supported for fast or ultra-fast search depths. |
| `answer` | string | 是 | - | A short answer to the user's query, generated by an LLM. Included in the response only if include_answer is requested (i.e., set to true, basic, or advanced)Example:"Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation. He spent the majority of his career playing for FC Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal-sc |
| `results.title` | string | 否 | - | The title of the search result.Example:"Lionel Messi Facts \| Britannica" |
| `results.url` | string | 否 | - | The URL of the search result.Example:"https://www.britannica.com/facts/Lionel-Messi" |
| `results.content` | string | 否 | - | A short description of the search result.Example:"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champions League titles. Messi is known for his exceptional dribbling skills, vision, and goal" |
| `results.score` | number<float> | 否 | - | The relevance score of the search result.Example:0.81025416 |
| `results.raw_content` | string | 否 | - | The cleaned and parsed HTML content of the search result. Only if include_raw_content is true.Example:null |
| `results.favicon` | string | 否 | - | The favicon URL for the result.Example:"https://britannica.com/favicon.png" |
| `response_time` | number<float> | 是 | - | Time in seconds it took to complete the request.Example:"1.67" |
| `request_id` | string | 否 | - | A unique request identifier you can share with customer support to help resolve issues with specific requests.Example:"123e4567-e89b-12d3-a456-426614174111" |
| `Hide child attributesimages.url` | string | 否 | - | images.descriptionstring |
| `Hide child attributesresults.title` | string | 否 | - | The title of the search result.Example:"Lionel Messi Facts \| Britannica"results.urlstringThe URL of the search result.Example:"https://www.britannica.com/facts/Lionel-Messi"results.contentstringA short description of the search result.Example:"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the majority of his career playing for Barcelona, where he won numerous domestic league titles and UEFA Champio |
| `usage` | object | 否 | - | Credit usage details for the request.Example:{ "credits": 1 } |
| `include_domains` | string[] | 否 | - | A list of domains to specifically include in the search results. Maximum 300 domains. |
| `exclude_domains` | string[] | 否 | - | A list of domains to specifically exclude from the search results. Maximum 150 domains. |
| `images` | object | 否 | - | []requiredList of query-related images. If include_image_descriptions is true, each item will have url and description.Hide child attributes images.urlstring images.descriptionstringExample:[] |
| `results` | object | 否 | - | []requiredA list of sorted search results, ranked by relevancy.Hide child attributes results.titlestringThe title of the search result.Example:"Lionel Messi Facts \| Britannica" results.urlstringThe URL of the search result.Example:"https://www.britannica.com/facts/Lionel-Messi" results.contentstringA short description of the search result.Example:"Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest football players of his generation. Born in 1987, Messi spent the maj |

## 代码示例

### 示例 1 (text)

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.search("Who is Leo Messi?")

print(response)
```

### 示例 2 (json)

```json
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

### 示例 3 (json)

```json
{  "topic": "general",  "search_depth": "basic"}
```

### 示例 4 (json)

```json
{ "credits": 1 }
```

## 文档正文

Execute a search query using Tavily Search.

## API 端点

**Method:** `POST`
**Endpoint:** `/search`

Authorizations

Authorization
stringheaderrequired

Bearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

Body
application/json

Parameters for the Tavily Search request.

query
stringrequired

The search query to execute with Tavily.

Example:

"who is Leo Messi?"

search_depth
enum<string>default:basic

Controls the latency vs. relevance tradeoff and how results[].content is generated:

advanced: Highest relevance with increased latency. Best for detailed, high-precision queries. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).
basic: A balanced option for relevance and latency. Ideal for general-purpose searches. Returns one NLP summary per URL.
fast: Prioritizes lower latency while maintaining good relevance. Returns multiple semantically relevant snippets per URL (configurable via chunks_per_source).
ultra-fast: Minimizes latency above all else. Best for time-critical use cases. Returns one NLP summary per URL.

Cost:

basic, fast, ultra-fast: 1 API Credit
advanced: 2 API Credits

See Search Best Practices for guidance on choosing the right search depth.

Available options: advanced, basic, fast, ultra-fast 

chunks_per_source
integerdefault:3

Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the content length. Chunks will appear in the content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when search_depth is advanced.

Required range: 1 <= x <= 3

max_results
integerdefault:5

The maximum number of search results to return.

Required range: 0 <= x <= 20
Example:

1

topic
enum<string>default:general

The category of the search.news is useful for retrieving real-time updates, particularly about politics, sports, and major current events covered by mainstream media sources. general is for broader, more general-purpose searches that may include a wide range of sources.

Available options: general, news, finance 

time_range
enum<string>

The time range back from the current date to filter results based on publish date or last updated date. Useful when looking for sources that have published or updated data.

Available options: day, week, month, year, d, w, m, y 

start_date
string

Will return all results after the specified start date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD

Example:

"2025-02-09"

end_date
string

Will return all results before the specified end date based on publish date or last updated date. Required to be written in the format YYYY-MM-DD

Example:

"2025-12-29"

include_answer
boolean
enum<string>
boolean
default:false

Include an LLM-generated answer to the provided query. basic or true returns a quick answer. advanced returns a more detailed answer.

include_raw_content
boolean
enum<string>
boolean
default:false

Include the cleaned and parsed HTML content of each search result. markdown or true returns search result content in markdown format. text returns the plain text from the results and may increase latency.

include_images
booleandefault:false

Also perform an image search and include the results in the response.

include_image_descriptions
booleandefault:false

When include_images is true, also add a descriptive text for each image.

include_favicon
booleandefault:false

Whether to include the favicon URL for each result.

include_domains
string[]

A list of domains to specifically include in the search results. Maximum 300 domains.

exclude_domains
string[]

A list of domains to specifically exclude from the search results. Maximum 150 domains.

country
enum<string>

Boost search results from a specific country. This will prioritize content from the selected country in the search results. Available only if topic is general.

Available options: afghanistan, albania, algeria, andorra, angola, argentina, armenia, australia, austria, azerbaijan, bahamas, bahrain, bangladesh, barbados, belarus, belgium, belize, benin, bhutan, bolivia, bosnia and herzegovina, botswana, brazil, brunei, bulgaria, burkina faso, burundi, cambodia, cameroon, canada, cape verde, central african republic, chad, chile, china, colombia, comoros, congo, costa rica, croatia, cuba, cyprus, czech republic, denmark, djibouti, dominican republic, ecuador, egypt, el salvador, equatorial guinea, eritrea, estonia, ethiopia, fiji, finland, france, gabon, gambia, georgia, germany, ghana, greece, guatemala, guinea, haiti, honduras, hungary, iceland, india, indonesia, iran, iraq, ireland, israel, italy, jamaica, japan, jordan, kazakhstan, kenya, kuwait, kyrgyzstan, latvia, lebanon, lesotho, liberia, libya, liechtenstein, lithuania, luxembourg, madagascar, malawi, malaysia, maldives, mali, malta, mauritania, mauritius, mexico, moldova, monaco, mongolia, montene
