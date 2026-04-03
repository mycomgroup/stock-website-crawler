---
id: "url-44f05062"
type: "api"
title: "Tavily Extract"
url: "https://docs.tavily.com/documentation/api-reference/endpoint/extract"
description: "Extract web page content from one or more specified URLs using Tavily Extract."
source: ""
tags: []
crawl_time: "2026-03-18T07:48:22.748Z"
metadata:
  method: "POST"
  endpoint: "/extract"
  baseUrl: "https://api.tavily.com"
  parameters:
    - {"name":"Authorization","type":"string","required":true,"default":"","description":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).","location":"header"}
    - {"name":"urls","type":"","required":false,"default":"","description":""}
    - {"name":"query","type":"string","required":false,"default":"","description":"User intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query."}
    - {"name":"chunks_per_source","type":"integer","required":false,"default":"","description":"default:3Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length. Chunks will appear in the raw_content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when query is provided. Must be between 1 and 5.Required range: 1 <= x <= 5"}
    - {"name":"extract_depth","type":"enum<string>","required":false,"default":"basic","description":"The depth of the extraction process. advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency.basic extraction costs 1 credit per 5 successful URL extractions, while advanced extraction costs 2 credits per 5 successful URL extractions.Available options: basic, advanced"}
    - {"name":"include_images","type":"boolean","required":false,"default":"","description":"default:falseInclude a list of images extracted from the URLs in the response. Default is false."}
    - {"name":"include_favicon","type":"boolean","required":false,"default":"","description":"default:falseWhether to include the favicon URL for each result."}
    - {"name":"format","type":"enum<string>","required":false,"default":"markdownThe","description":"format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.Available options: markdown, text"}
    - {"name":"timeout","type":"number<float>","required":false,"default":"NoneMaximum","description":"time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction.Required range: 1 <= x <= 60"}
    - {"name":"include_usage","type":"boolean","required":false,"default":"","description":"default:falseWhether to include credit usage information in the response. NOTE:The value may be 0 if the total successful URL extractions has not yet reached 5 calls. See our Credits & Pricing documentation for details."}
    - {"name":"results.url","type":"string","required":false,"default":"","description":"The URL from which the content was extracted.Example:\"https://en.wikipedia.org/wiki/Artificial_intelligence\""}
    - {"name":"results.raw_content","type":"string","required":false,"default":"","description":"The full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.Example:\"\\\"Jump to content\\\\nMain menu\\\\nSearch\\\\nAppearance\\\\nDonate\\\\nCreate account\\\\nLog in\\\\nPersonal tools\\\\n        Photograph your local culture, help Wikipedia and win!\\\\nToggle the table of contents\\\\nArtificial intelligence\\\\n161 languages\\\\nArticle\\\\nTalk\\\\nRead\\\\nView source\\\\nView history\\\\nTools\\\\nFrom Wikipedia, the free encyclopedia\\\\n\\\\\\\"AI\\\\\\\" redirects he"}
    - {"name":"results.favicon","type":"string","required":false,"default":"","description":"The favicon URL for the result.Example:\"https://en.wikipedia.org/static/favicon/wikipedia.ico\""}
    - {"name":"failed_results.url","type":"string","required":false,"default":"","description":"The URL that failed to be processed."}
    - {"name":"failed_results.error","type":"string","required":false,"default":"","description":"An error message describing why the URL couldn't be processed."}
    - {"name":"response_time","type":"number<float>","required":false,"default":"","description":"Time in seconds it took to complete the request.Example:0.02"}
    - {"name":"request_id","type":"string","required":false,"default":"","description":"A unique request identifier you can share with customer support to help resolve issues with specific requests.Example:\"123e4567-e89b-12d3-a456-426614174111\""}
    - {"name":"results","type":"object","required":false,"default":"","description":"[]A list of extracted content from the provided URLs.Hide child attributes results.urlstringThe URL from which the content was extracted.Example:\"https://en.wikipedia.org/wiki/Artificial_intelligence\" results.raw_contentstringThe full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.Example:\"\\\"Jump to content\\\\nMain menu\\\\nSearch\\\\nAppearance\\\\nDonate\\\\nCreate account\\\\nLog in\\\\nPersonal tools\\\\n        Photograph your local cultur"}
    - {"name":"Hide child attributes​results.url","type":"string","required":false,"default":"","description":"The URL from which the content was extracted.Example:\"https://en.wikipedia.org/wiki/Artificial_intelligence\"​results.raw_contentstringThe full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.Example:\"\\\"Jump to content\\\\nMain menu\\\\nSearch\\\\nAppearance\\\\nDonate\\\\nCreate account\\\\nLog in\\\\nPersonal tools\\\\n        Photograph your local culture, help Wikipedia and win!\\\\nToggle the table of contents\\\\nArtificial intelligence\\\\n161 la"}
    - {"name":"Hide child attributes​failed_results.url","type":"string","required":false,"default":"","description":"The URL that failed to be processed.​failed_results.errorstringAn error message describing why the URL couldn't be processed."}
    - {"name":"usage","type":"object","required":false,"default":"","description":"Credit usage details for the request.Example:{ \"credits\": 1 }"}
    - {"name":"results.images","type":"string[]","required":false,"default":"","description":"This is only available if include_images is set to true. A list of image URLs extracted from the page.Example:[]"}
    - {"name":"failed_results","type":"object","required":false,"default":"","description":"[]A list of URLs that could not be processed.Hide child attributes failed_results.urlstringThe URL that failed to be processed. failed_results.errorstringAn error message describing why the URL couldn't be processed.Example:[]"}
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.extract(\"https://en.wikipedia.org/wiki/Artificial_intelligence\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"results\": [\n    {\n      \"url\": \"https://en.wikipedia.org/wiki/Artificial_intelligence\",\n      \"raw_content\": \"\\\"Jump to content\\\\nMain menu\\\\nSearch\\\\nAppearance\\\\nDonate\\\\nCreate account\\\\nLog in\\\\nPersonal tools\\\\n        Photograph your local culture, help Wikipedia and win!\\\\nToggle the table of contents\\\\nArtificial intelligence\\\\n161 languages\\\\nArticle\\\\nTalk\\\\nRead\\\\nView source\\\\nView history\\\\nTools\\\\nFrom Wikipedia, the free encyclopedia\\\\n\\\\\\\"AI\\\\\\\" redirects here. For other uses, see AI (disambiguation) and Artificial intelligence (disambiguation).\\\\nPart of a series on\\\\nArtificial intelligence (AI)\\\\nshow\\\\nMajor goals\\\\nshow\\\\nApproaches\\\\nshow\\\\nApplications\\\\nshow\\\\nPhilosophy\\\\nshow\\\\nHistory\\\\nshow\\\\nGlossary\\\\nvte\\\\nArtificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.\\\\nHigh-profile applications of AI include advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); virtual assistants (e.g., Google Assistant, Siri, and Alexa); autonomous vehicles (e.g., Waymo); generative and creative tools (e.g., ChatGPT and AI art); and superhuman play and analysis in strategy games (e.g., chess and Go)...................\",\n      \"images\": [],\n      \"favicon\": \"https://en.wikipedia.org/static/favicon/wikipedia.ico\"\n    }\n  ],\n  \"failed_results\": [],\n  \"response_time\": 0.02,\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.extract(\"https://en.wikipedia.org/wiki/Artificial_intelligence\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"results\": [\n    {\n      \"url\": \"https://en.wikipedia.org/wiki/Artificial_intelligence\",\n      \"raw_content\": \"\\\"Jump to content\\\\nMain menu\\\\nSearch\\\\nAppearance\\\\nDonate\\\\nCreate account\\\\nLog in\\\\nPersonal tools\\\\n        Photograph your local culture, help Wikipedia and win!\\\\nToggle the table of contents\\\\nArtificial intelligence\\\\n161 languages\\\\nArticle\\\\nTalk\\\\nRead\\\\nView source\\\\nView history\\\\nTools\\\\nFrom Wikipedia, the free encyclopedia\\\\n\\\\\\\"AI\\\\\\\" redirects here. For other uses, see AI (disambiguation) and Artificial intelligence (disambiguation).\\\\nPart of a series on\\\\nArtificial intelligence (AI)\\\\nshow\\\\nMajor goals\\\\nshow\\\\nApproaches\\\\nshow\\\\nApplications\\\\nshow\\\\nPhilosophy\\\\nshow\\\\nHistory\\\\nshow\\\\nGlossary\\\\nvte\\\\nArtificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.\\\\nHigh-profile applications of AI include advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); virtual assistants (e.g., Google Assistant, Siri, and Alexa); autonomous vehicles (e.g., Waymo); generative and creative tools (e.g., ChatGPT and AI art); and superhuman play and analysis in strategy games (e.g., chess and Go)...................\",\n      \"images\": [],\n      \"favicon\": \"https://en.wikipedia.org/static/favicon/wikipedia.ico\"\n    }\n  ],\n  \"failed_results\": [],\n  \"response_time\": 0.02,\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"json","code":"{ \"credits\": 1 }"}
  mainContent:
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Body"}
    - {"type":"paragraph","content":"Parameters for the Tavily Extract request."}
    - {"type":"parameter","name":"\"https://en.wikipedia.org/wiki/Artificial_intelligence\"","paramType":"","description":"​urls"}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Extraction results returned successfully"}
    - {"type":"parameter","name":"\"https://en.wikipedia.org/wiki/Artificial_intelligence\"","paramType":"","description":"​resultsobject[]A list of extracted content from the provided URLs.Hide child attributes​results.urlstringThe URL from which the content was extracted.Example:\"https://en.wikipedia.org/wiki/Artificial_intelligence\"​results.raw_contentstringThe full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.Example:\"\\\"Jump to content\\\\nMain menu\\\\nSearch\\\\nAppearance\\\\nDonate\\\\nCreate account\\\\nLog in\\\\nPersonal tools\\\\n        Photograph your local culture, help Wikipedia and win!\\\\nToggle the table of contents\\\\nArtificial intelligence\\\\n161 languages\\\\nArticle\\\\nTalk\\\\nRead\\\\nView source\\\\nView history\\\\nTools\\\\nFrom Wikipedia, the free encyclopedia\\\\n\\\\\\\"AI\\\\\\\" redirects here. For other uses, see AI (disambiguation) and Artificial intelligence (disambiguation).\\\\nPart of a series on\\\\nArtificial intelligence (AI)\\\\nshow\\\\nMajor goals\\\\nshow\\\\nApproaches\\\\nshow\\\\nApplications\\\\nshow\\\\nPhilosophy\\\\nshow\\\\nHistory\\\\nshow\\\\nGlossary\\\\nvte\\\\nArtificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.\\\\nHigh-profile applications of AI include advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); virtual assistants (e.g., Google Assistant, Siri, and Alexa); autonomous vehicles (e.g., Waymo); generative and creative tools (e.g., ChatGPT and AI art); and superhuman play and analysis in strategy games (e.g., chess and Go)...................\"​results.imagesstring[]This is only available if include_images is set to true. A list of image URLs extracted from the page.Example:[]​results.faviconstringThe favicon URL for the result.Example:\"https://en.wikipedia.org/static/favicon/wikipedia.ico\"​failed_resultsobject[]A list of URLs that could not be processed.Hide child attributes​failed_results.urlstringThe URL that failed to be processed.​failed_results.errorstringAn error message describing why the URL couldn't be processed.Example:[]​response_timenumber<float>Time in seconds it took to complete the request.Example:0.02​usageobjectCredit usage details for the request.Example:{ \"credits\": 1 }​request_idstringA unique request identifier you can share with customer support to help resolve issues with specific requests.Example:\"123e4567-e89b-12d3-a456-426614174111\""}
  rawContent: "Authorizations\n​\nAuthorization\nstringheaderrequired\n\nBearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).\n\nBody\napplication/json\n\nParameters for the Tavily Extract request.\n\n​\nurls\nstring\nstring[]\nstring\nrequired\n\nThe URL to extract content from.\n\nExample:\n\n\"https://en.wikipedia.org/wiki/Artificial_intelligence\"\n\n​\nquery\nstring\n\nUser intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query.\n\n​\nchunks_per_source\nintegerdefault:3\n\nChunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length. Chunks will appear in the raw_content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when query is provided. Must be between 1 and 5.\n\nRequired range: 1 <= x <= 5\n​\nextract_depth\nenum<string>default:basic\n\nThe depth of the extraction process. advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency.basic extraction costs 1 credit per 5 successful URL extractions, while advanced extraction costs 2 credits per 5 successful URL extractions.\n\nAvailable options: basic, advanced \n​\ninclude_images\nbooleandefault:false\n\nInclude a list of images extracted from the URLs in the response. Default is false.\n\n​\ninclude_favicon\nbooleandefault:false\n\nWhether to include the favicon URL for each result.\n\n​\nformat\nenum<string>default:markdown\n\nThe format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.\n\nAvailable options: markdown, text \n​\ntimeout\nnumber<float>default:None\n\nMaximum time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction.\n\nRequired range: 1 <= x <= 60\n​\ninclude_usage\nbooleandefault:false\n\nWhether to include credit usage information in the response. NOTE:The value may be 0 if the total successful URL extractions has not yet reached 5 calls. See our Credits & Pricing documentation for details.\n\nResponse\n200\napplication/json\n\nExtraction results returned successfully\n\n​\nresults\nobject[]\n\nA list of extracted content from the provided URLs.\n\nHide child attributes\n\n​\nresults.url\nstring\n\nThe URL from which the content was extracted.\n\nExample:\n\n\"https://en.wikipedia.org/wiki/Artificial_intelligence\"\n\n​\nresults.raw_content\nstring\n\nThe full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.\n\nExample:\n\n\"\\\"Jump to content\\\\nMain menu\\\\nSearch\\\\nAppearance\\\\nDonate\\\\nCreate account\\\\nLog in\\\\nPersonal tools\\\\n Photograph your local culture, help Wikipedia and win!\\\\nToggle the table of contents\\\\nArtificial intelligence\\\\n161 languages\\\\nArticle\\\\nTalk\\\\nRead\\\\nView source\\\\nView history\\\\nTools\\\\nFrom Wikipedia, the free encyclopedia\\\\n\\\\\\\"AI\\\\\\\" redirects here. For other uses, see AI (disambiguation) and Artificial intelligence (disambiguation).\\\\nPart of a series on\\\\nArtificial intelligence (AI)\\\\nshow\\\\nMajor goals\\\\nshow\\\\nApproaches\\\\nshow\\\\nApplications\\\\nshow\\\\nPhilosophy\\\\nshow\\\\nHistory\\\\nshow\\\\nGlossary\\\\nvte\\\\nArtificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.\\\\nHigh-profile applications of AI include advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); virtual assistants (e.g., Google Assistant, Siri, and Alexa); autonomous vehicles (e.g., Waymo); generative and creative tools (e.g., ChatGPT and AI art); and superhuman play and analysis in strategy games (e.g., chess and Go)...................\"\n\n​\nresults.images\nstring[]\n\nThis is only available if include_images is set to true. A list of image URLs extracted from the page.\n\nExample:\n[]\n​\nresults.favicon\nstring\n\nThe favicon URL for the result.\n\nExample:\n\n\"https://en.wikipedia.org/static/favicon/wikipedia.ico\"\n\n​\nfailed_results\nobject[]\n\nA list of URLs that could not be processed.\n\nHide child attributes\n\n​\nfailed_results.url\nstring\n\nThe URL that failed to be processed.\n\n​\nfailed_results.error\nstring\n\nAn error message describing why the URL couldn't be processed.\n\nExample:\n[]\n​\nresponse_time\nnumber<float>\n\nTime in seconds it took to complete the request.\n\nExample:\n\n0.02\n\n​\nusage\nobject\n\nCredit usage details for the request.\n\nExample:\n{ \"credits\": 1 }\n​\nrequest_id\nstring\n\nA unique request identifier you can share with customer support to help resolve issues with specific requests.\n\nExample:\n\n\"123e4567-e89b-12d3-a456-426614174111\""
  suggestedFilename: "endpoint_extract"
---

# Tavily Extract

## 源URL

https://docs.tavily.com/documentation/api-reference/endpoint/extract

## 描述

Extract web page content from one or more specified URLs using Tavily Extract.

## API 端点

**Method**: `POST`
**Endpoint**: `/extract`
**Base URL**: `https://api.tavily.com`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Authorization` | string | 是 | - | Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY). |
| `urls` | - | 否 | - | - |
| `query` | string | 否 | - | User intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query. |
| `chunks_per_source` | integer | 否 | - | default:3Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length. Chunks will appear in the raw_content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when query is provided. Must be between 1 and 5.Required range: 1 <= x <= 5 |
| `extract_depth` | enum<string> | 否 | basic | The depth of the extraction process. advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency.basic extraction costs 1 credit per 5 successful URL extractions, while advanced extraction costs 2 credits per 5 successful URL extractions.Available options: basic, advanced |
| `include_images` | boolean | 否 | - | default:falseInclude a list of images extracted from the URLs in the response. Default is false. |
| `include_favicon` | boolean | 否 | - | default:falseWhether to include the favicon URL for each result. |
| `format` | enum<string> | 否 | markdownThe | format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.Available options: markdown, text |
| `timeout` | number<float> | 否 | NoneMaximum | time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction.Required range: 1 <= x <= 60 |
| `include_usage` | boolean | 否 | - | default:falseWhether to include credit usage information in the response. NOTE:The value may be 0 if the total successful URL extractions has not yet reached 5 calls. See our Credits & Pricing documentation for details. |
| `results.url` | string | 否 | - | The URL from which the content was extracted.Example:"https://en.wikipedia.org/wiki/Artificial_intelligence" |
| `results.raw_content` | string | 否 | - | The full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.Example:"\"Jump to content\\nMain menu\\nSearch\\nAppearance\\nDonate\\nCreate account\\nLog in\\nPersonal tools\\n        Photograph your local culture, help Wikipedia and win!\\nToggle the table of contents\\nArtificial intelligence\\n161 languages\\nArticle\\nTalk\\nRead\\nView source\\nView history\\nTools\\nFrom Wikipedia, the free encyclopedia\\n\\\"AI\\\" redirects he |
| `results.favicon` | string | 否 | - | The favicon URL for the result.Example:"https://en.wikipedia.org/static/favicon/wikipedia.ico" |
| `failed_results.url` | string | 否 | - | The URL that failed to be processed. |
| `failed_results.error` | string | 否 | - | An error message describing why the URL couldn't be processed. |
| `response_time` | number<float> | 否 | - | Time in seconds it took to complete the request.Example:0.02 |
| `request_id` | string | 否 | - | A unique request identifier you can share with customer support to help resolve issues with specific requests.Example:"123e4567-e89b-12d3-a456-426614174111" |
| `results` | object | 否 | - | []A list of extracted content from the provided URLs.Hide child attributes results.urlstringThe URL from which the content was extracted.Example:"https://en.wikipedia.org/wiki/Artificial_intelligence" results.raw_contentstringThe full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.Example:"\"Jump to content\\nMain menu\\nSearch\\nAppearance\\nDonate\\nCreate account\\nLog in\\nPersonal tools\\n        Photograph your local cultur |
| `Hide child attributesresults.url` | string | 否 | - | The URL from which the content was extracted.Example:"https://en.wikipedia.org/wiki/Artificial_intelligence"results.raw_contentstringThe full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.Example:"\"Jump to content\\nMain menu\\nSearch\\nAppearance\\nDonate\\nCreate account\\nLog in\\nPersonal tools\\n        Photograph your local culture, help Wikipedia and win!\\nToggle the table of contents\\nArtificial intelligence\\n161 la |
| `Hide child attributesfailed_results.url` | string | 否 | - | The URL that failed to be processed.failed_results.errorstringAn error message describing why the URL couldn't be processed. |
| `usage` | object | 否 | - | Credit usage details for the request.Example:{ "credits": 1 } |
| `results.images` | string[] | 否 | - | This is only available if include_images is set to true. A list of image URLs extracted from the page.Example:[] |
| `failed_results` | object | 否 | - | []A list of URLs that could not be processed.Hide child attributes failed_results.urlstringThe URL that failed to be processed. failed_results.errorstringAn error message describing why the URL couldn't be processed.Example:[] |

## 代码示例

### 示例 1 (text)

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.extract("https://en.wikipedia.org/wiki/Artificial_intelligence")

print(response)
```

### 示例 2 (json)

```json
{
  "results": [
    {
      "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
      "raw_content": "\"Jump to content\\nMain menu\\nSearch\\nAppearance\\nDonate\\nCreate account\\nLog in\\nPersonal tools\\n        Photograph your local culture, help Wikipedia and win!\\nToggle the table of contents\\nArtificial intelligence\\n161 languages\\nArticle\\nTalk\\nRead\\nView source\\nView history\\nTools\\nFrom Wikipedia, the free encyclopedia\\n\\\"AI\\\" redirects here. For other uses, see AI (disambiguation) and Artificial intelligence (disambiguation).\\nPart of a series on\\nArtificial intelligence (AI)\\nshow\\nMajor goals\\nshow\\nApproaches\\nshow\\nApplications\\nshow\\nPhilosophy\\nshow\\nHistory\\nshow\\nGlossary\\nvte\\nArtificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.\\nHigh-profile applications of AI include advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); virtual assistants (e.g., Google Assistant, Siri, and Alexa); autonomous vehicles (e.g., Waymo); generative and creative tools (e.g., ChatGPT and AI art); and superhuman play and analysis in strategy games (e.g., chess and Go)...................",
      "images": [],
      "favicon": "https://en.wikipedia.org/static/favicon/wikipedia.ico"
    }
  ],
  "failed_results": [],
  "response_time": 0.02,
  "usage": {
    "credits": 1
  },
  "request_id": "123e4567-e89b-12d3-a456-426614174111"
}
```

### 示例 3 (json)

```json
{ "credits": 1 }
```

## 文档正文

Extract web page content from one or more specified URLs using Tavily Extract.

## API 端点

**Method:** `POST`
**Endpoint:** `/extract`

Authorizations

Authorization
stringheaderrequired

Bearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

Body
application/json

Parameters for the Tavily Extract request.

urls
string
string[]
string
required

The URL to extract content from.

Example:

"https://en.wikipedia.org/wiki/Artificial_intelligence"

query
string

User intent for reranking extracted content chunks. When provided, chunks are reranked based on relevance to this query.

chunks_per_source
integerdefault:3

Chunks are short content snippets (maximum 500 characters each) pulled directly from the source. Use chunks_per_source to define the maximum number of relevant chunks returned per source and to control the raw_content length. Chunks will appear in the raw_content field as: <chunk 1> [...] <chunk 2> [...] <chunk 3>. Available only when query is provided. Must be between 1 and 5.

Required range: 1 <= x <= 5

extract_depth
enum<string>default:basic

The depth of the extraction process. advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency.basic extraction costs 1 credit per 5 successful URL extractions, while advanced extraction costs 2 credits per 5 successful URL extractions.

Available options: basic, advanced 

include_images
booleandefault:false

Include a list of images extracted from the URLs in the response. Default is false.

include_favicon
booleandefault:false

Whether to include the favicon URL for each result.

format
enum<string>default:markdown

The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.

Available options: markdown, text 

timeout
number<float>default:None

Maximum time in seconds to wait for the URL extraction before timing out. Must be between 1.0 and 60.0 seconds. If not specified, default timeouts are applied based on extract_depth: 10 seconds for basic extraction and 30 seconds for advanced extraction.

Required range: 1 <= x <= 60

include_usage
booleandefault:false

Whether to include credit usage information in the response. NOTE:The value may be 0 if the total successful URL extractions has not yet reached 5 calls. See our Credits & Pricing documentation for details.

Response
200
application/json

Extraction results returned successfully

results
object[]

A list of extracted content from the provided URLs.

Hide child attributes

results.url
string

The URL from which the content was extracted.

Example:

"https://en.wikipedia.org/wiki/Artificial_intelligence"

results.raw_content
string

The full content extracted from the page. When query is provided, contains the top-ranked chunks joined by [...] separator.

Example:

"\"Jump to content\\nMain menu\\nSearch\\nAppearance\\nDonate\\nCreate account\\nLog in\\nPersonal tools\\n Photograph your local culture, help Wikipedia and win!\\nToggle the table of contents\\nArtificial intelligence\\n161 languages\\nArticle\\nTalk\\nRead\\nView source\\nView history\\nTools\\nFrom Wikipedia, the free encyclopedia\\n\\\"AI\\\" redirects here. For other uses, see AI (disambiguation) and Artificial intelligence (disambiguation).\\nPart of a series on\\nArtificial intelligence (AI)\\nshow\\nMajor goals\\nshow\\nApproaches\\nshow\\nApplications\\nshow\\nPhilosophy\\nshow\\nHistory\\nshow\\nGlossary\\nvte\\nArtificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines, particularly computer systems. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals.[1] Such machines may be called AIs.\\nHigh-profile applications of AI include advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); virtual assistants (e.g., Google Assistant, Siri, and Alexa); autonomous vehicles (e.g., Waymo); generative and creative tools (e.g., ChatGPT and AI art); and superhuman play and analysis in strategy games (e.g., chess and Go)..................."

results.images
string[]

This is only available if include_images is set to true. A list of image URLs extracted from the page.

Example:
[]

results.favicon
string

The favicon URL for the result.

Example:

"https://en.wikipedia.org/static/favicon/wikipedia.ico"

failed_results
object[]

A list of URLs that could not be processed.

Hide child attributes

failed_results.url
string

The URL that failed to be processed.

failed_results.error
string

An error message describing why the URL couldn't be processed.

Example:
[]

response_time
number<float>

Time in seconds it took to complete the request.

Example:

0.02

usage
object

Credit usage details for the request.

Example:
{ "credits": 1 }

request_id
string

A u
