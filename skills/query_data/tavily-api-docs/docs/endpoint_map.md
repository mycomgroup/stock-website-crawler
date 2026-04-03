---
id: "url-49297107"
type: "api"
title: "Tavily Map"
url: "https://docs.tavily.com/documentation/api-reference/endpoint/map"
description: "Tavily Map traverses websites like a graph and can explore hundreds of paths in parallel with intelligent discovery to generate comprehensive site maps."
source: ""
tags: []
crawl_time: "2026-03-18T07:13:54.877Z"
metadata:
  method: "POST"
  endpoint: "/map"
  baseUrl: "https://api.tavily.com"
  parameters:
    - {"name":"Authorization","type":"string","required":true,"default":"","description":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).","location":"header"}
    - {"name":"url","type":"string","required":true,"default":"","description":"The root URL to begin the mapping.Example:\"docs.tavily.com\""}
    - {"name":"instructions","type":"string","required":false,"default":"","description":"Natural language instructions for the crawler. When specified, the cost increases to 2 API credits per 10 successful pages instead of 1 API credit per 10 pages.Example:\"Find all pages about the Python SDK\""}
    - {"name":"max_depth","type":"integer","required":false,"default":"","description":"default:1Max depth of the mapping. Defines how far from the base URL the crawler can explore.Required range: 1 <= x <= 5"}
    - {"name":"max_breadth","type":"integer","required":false,"default":"","description":"default:20Max number of links to follow per level of the tree (i.e., per page).Required range: 1 <= x <= 500"}
    - {"name":"limit","type":"integer","required":false,"default":"","description":"default:50Total number of links the crawler will process before stopping.Required range: x >= 1"}
    - {"name":"allow_external","type":"boolean","required":false,"default":"","description":"default:trueWhether to include external domain links in the final results list."}
    - {"name":"timeout","type":"number<float>","required":false,"default":"150","description":"Maximum time in seconds to wait for the map operation before timing out. Must be between 10 and 150 seconds.Required range: 10 <= x <= 150"}
    - {"name":"include_usage","type":"boolean","required":false,"default":"","description":"default:falseWhether to include credit usage information in the response.NOTE:The value may be 0 if the total successful pages mapped has not yet reached 10 calls. See our Credits & Pricing documentation for details."}
    - {"name":"base_url","type":"string","required":false,"default":"","description":"The base URL that was mapped.Example:\"docs.tavily.com\""}
    - {"name":"response_time","type":"number<float>","required":false,"default":"","description":"Time in seconds it took to complete the request.Example:1.23"}
    - {"name":"request_id","type":"string","required":false,"default":"","description":"A unique request identifier you can share with customer support to help resolve issues with specific requests.Example:\"123e4567-e89b-12d3-a456-426614174111\""}
    - {"name":"usage","type":"object","required":false,"default":"","description":"Credit usage details for the request.Example:{ \"credits\": 1 }"}
    - {"name":"select_paths","type":"string[]","required":false,"default":"","description":"Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)."}
    - {"name":"select_domains","type":"string[]","required":false,"default":"","description":"Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\.example\\.com$)."}
    - {"name":"exclude_paths","type":"string[]","required":false,"default":"","description":"Regex patterns to exclude URLs with specific path patterns (e.g., /private/.*, /admin/.*)."}
    - {"name":"exclude_domains","type":"string[]","required":false,"default":"","description":"Regex patterns to exclude specific domains or subdomains from crawling (e.g., ^private\\.example\\.com$)."}
    - {"name":"results","type":"string[]","required":false,"default":"","description":"A list of URLs that were discovered during the mapping.Example:[  \"https://docs.tavily.com/welcome\",  \"https://docs.tavily.com/documentation/api-credits\",  \"https://docs.tavily.com/documentation/about\"]"}
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.map(\"https://docs.tavily.com\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"base_url\": \"docs.tavily.com\",\n  \"results\": [\n    \"https://docs.tavily.com/welcome\",\n    \"https://docs.tavily.com/documentation/api-credits\",\n    \"https://docs.tavily.com/documentation/about\"\n  ],\n  \"response_time\": 1.23,\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.map(\"https://docs.tavily.com\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"base_url\": \"docs.tavily.com\",\n  \"results\": [\n    \"https://docs.tavily.com/welcome\",\n    \"https://docs.tavily.com/documentation/api-credits\",\n    \"https://docs.tavily.com/documentation/about\"\n  ],\n  \"response_time\": 1.23,\n  \"usage\": {\n    \"credits\": 1\n  },\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\"\n}"}
    - {"language":"text","code":"[  \"https://docs.tavily.com/welcome\",  \"https://docs.tavily.com/documentation/api-credits\",  \"https://docs.tavily.com/documentation/about\"]"}
    - {"language":"json","code":"{ \"credits\": 1 }"}
  mainContent:
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Body"}
    - {"type":"paragraph","content":"Parameters for the Tavily Map request."}
    - {"type":"parameter","name":"\"docs.tavily.com\"","paramType":"","description":"​urlstringrequiredThe root URL to begin the mapping.Example:\"docs.tavily.com\"​instructionsstringNatural language instructions for the crawler. When specified, the cost increases to 2 API credits per 10 successful pages instead of 1 API credit per 10 pages.Example:\"Find all pages about the Python SDK\"​max_depthintegerdefault:1Max depth of the mapping. Defines how far from the base URL the crawler can explore.Required range: 1 <= x <= 5​max_breadthintegerdefault:20Max number of links to follow per level of the tree (i.e., per page).Required range: 1 <= x <= 500​limitintegerdefault:50Total number of links the crawler will process before stopping.Required range: x >= 1​select_pathsstring[]Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*).​select_domainsstring[]Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\.example\\.com$).​exclude_pathsstring[]Regex patterns to exclude URLs with specific path patterns (e.g., /private/.*, /admin/.*).​exclude_domainsstring[]Regex patterns to exclude specific domains or subdomains from crawling (e.g., ^private\\.example\\.com$).​allow_externalbooleandefault:trueWhether to include external domain links in the final results list.​timeoutnumber<float>default:150Maximum time in seconds to wait for the map operation before timing out. Must be between 10 and 150 seconds.Required range: 10 <= x <= 150​include_usagebooleandefault:falseWhether to include credit usage information in the response.NOTE:The value may be 0 if the total successful pages mapped has not yet reached 10 calls. See our Credits & Pricing documentation for details."}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Map results returned successfully"}
    - {"type":"parameter","name":"\"docs.tavily.com\"","paramType":"","description":"​base_urlstringThe base URL that was mapped.Example:\"docs.tavily.com\"​resultsstring[]A list of URLs that were discovered during the mapping.Example:[  \"https://docs.tavily.com/welcome\",  \"https://docs.tavily.com/documentation/api-credits\",  \"https://docs.tavily.com/documentation/about\"]​response_timenumber<float>Time in seconds it took to complete the request.Example:1.23​usageobjectCredit usage details for the request.Example:{ \"credits\": 1 }​request_idstringA unique request identifier you can share with customer support to help resolve issues with specific requests.Example:\"123e4567-e89b-12d3-a456-426614174111\""}
  rawContent: "Authorizations\n​\nAuthorization\nstringheaderrequired\n\nBearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).\n\nBody\napplication/json\n\nParameters for the Tavily Map request.\n\n​\nurl\nstringrequired\n\nThe root URL to begin the mapping.\n\nExample:\n\n\"docs.tavily.com\"\n\n​\ninstructions\nstring\n\nNatural language instructions for the crawler. When specified, the cost increases to 2 API credits per 10 successful pages instead of 1 API credit per 10 pages.\n\nExample:\n\n\"Find all pages about the Python SDK\"\n\n​\nmax_depth\nintegerdefault:1\n\nMax depth of the mapping. Defines how far from the base URL the crawler can explore.\n\nRequired range: 1 <= x <= 5\n​\nmax_breadth\nintegerdefault:20\n\nMax number of links to follow per level of the tree (i.e., per page).\n\nRequired range: 1 <= x <= 500\n​\nlimit\nintegerdefault:50\n\nTotal number of links the crawler will process before stopping.\n\nRequired range: x >= 1\n​\nselect_paths\nstring[]\n\nRegex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*).\n\n​\nselect_domains\nstring[]\n\nRegex patterns to select crawling to specific domains or subdomains (e.g., ^docs\\.example\\.com$).\n\n​\nexclude_paths\nstring[]\n\nRegex patterns to exclude URLs with specific path patterns (e.g., /private/.*, /admin/.*).\n\n​\nexclude_domains\nstring[]\n\nRegex patterns to exclude specific domains or subdomains from crawling (e.g., ^private\\.example\\.com$).\n\n​\nallow_external\nbooleandefault:true\n\nWhether to include external domain links in the final results list.\n\n​\ntimeout\nnumber<float>default:150\n\nMaximum time in seconds to wait for the map operation before timing out. Must be between 10 and 150 seconds.\n\nRequired range: 10 <= x <= 150\n​\ninclude_usage\nbooleandefault:false\n\nWhether to include credit usage information in the response.NOTE:The value may be 0 if the total successful pages mapped has not yet reached 10 calls. See our Credits & Pricing documentation for details.\n\nResponse\n200\napplication/json\n\nMap results returned successfully\n\n​\nbase_url\nstring\n\nThe base URL that was mapped.\n\nExample:\n\n\"docs.tavily.com\"\n\n​\nresults\nstring[]\n\nA list of URLs that were discovered during the mapping.\n\nExample:\n[\n  \"https://docs.tavily.com/welcome\",\n  \"https://docs.tavily.com/documentation/api-credits\",\n  \"https://docs.tavily.com/documentation/about\"\n]\n​\nresponse_time\nnumber<float>\n\nTime in seconds it took to complete the request.\n\nExample:\n\n1.23\n\n​\nusage\nobject\n\nCredit usage details for the request.\n\nExample:\n{ \"credits\": 1 }\n​\nrequest_id\nstring\n\nA unique request identifier you can share with customer support to help resolve issues with specific requests.\n\nExample:\n\n\"123e4567-e89b-12d3-a456-426614174111\""
  suggestedFilename: "endpoint_map"
---

# Tavily Map

## 源URL

https://docs.tavily.com/documentation/api-reference/endpoint/map

## 描述

Tavily Map traverses websites like a graph and can explore hundreds of paths in parallel with intelligent discovery to generate comprehensive site maps.

## API 端点

**Method**: `POST`
**Endpoint**: `/map`
**Base URL**: `https://api.tavily.com`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Authorization` | string | 是 | - | Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY). |
| `url` | string | 是 | - | The root URL to begin the mapping.Example:"docs.tavily.com" |
| `instructions` | string | 否 | - | Natural language instructions for the crawler. When specified, the cost increases to 2 API credits per 10 successful pages instead of 1 API credit per 10 pages.Example:"Find all pages about the Python SDK" |
| `max_depth` | integer | 否 | - | default:1Max depth of the mapping. Defines how far from the base URL the crawler can explore.Required range: 1 <= x <= 5 |
| `max_breadth` | integer | 否 | - | default:20Max number of links to follow per level of the tree (i.e., per page).Required range: 1 <= x <= 500 |
| `limit` | integer | 否 | - | default:50Total number of links the crawler will process before stopping.Required range: x >= 1 |
| `allow_external` | boolean | 否 | - | default:trueWhether to include external domain links in the final results list. |
| `timeout` | number<float> | 否 | 150 | Maximum time in seconds to wait for the map operation before timing out. Must be between 10 and 150 seconds.Required range: 10 <= x <= 150 |
| `include_usage` | boolean | 否 | - | default:falseWhether to include credit usage information in the response.NOTE:The value may be 0 if the total successful pages mapped has not yet reached 10 calls. See our Credits & Pricing documentation for details. |
| `base_url` | string | 否 | - | The base URL that was mapped.Example:"docs.tavily.com" |
| `response_time` | number<float> | 否 | - | Time in seconds it took to complete the request.Example:1.23 |
| `request_id` | string | 否 | - | A unique request identifier you can share with customer support to help resolve issues with specific requests.Example:"123e4567-e89b-12d3-a456-426614174111" |
| `usage` | object | 否 | - | Credit usage details for the request.Example:{ "credits": 1 } |
| `select_paths` | string[] | 否 | - | Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*). |
| `select_domains` | string[] | 否 | - | Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\.example\.com$). |
| `exclude_paths` | string[] | 否 | - | Regex patterns to exclude URLs with specific path patterns (e.g., /private/.*, /admin/.*). |
| `exclude_domains` | string[] | 否 | - | Regex patterns to exclude specific domains or subdomains from crawling (e.g., ^private\.example\.com$). |
| `results` | string[] | 否 | - | A list of URLs that were discovered during the mapping.Example:[  "https://docs.tavily.com/welcome",  "https://docs.tavily.com/documentation/api-credits",  "https://docs.tavily.com/documentation/about"] |

## 代码示例

### 示例 1 (text)

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.map("https://docs.tavily.com")

print(response)
```

### 示例 2 (json)

```json
{
  "base_url": "docs.tavily.com",
  "results": [
    "https://docs.tavily.com/welcome",
    "https://docs.tavily.com/documentation/api-credits",
    "https://docs.tavily.com/documentation/about"
  ],
  "response_time": 1.23,
  "usage": {
    "credits": 1
  },
  "request_id": "123e4567-e89b-12d3-a456-426614174111"
}
```

### 示例 3 (text)

```text
[  "https://docs.tavily.com/welcome",  "https://docs.tavily.com/documentation/api-credits",  "https://docs.tavily.com/documentation/about"]
```

### 示例 4 (json)

```json
{ "credits": 1 }
```

## 文档正文

Tavily Map traverses websites like a graph and can explore hundreds of paths in parallel with intelligent discovery to generate comprehensive site maps.

## API 端点

**Method:** `POST`
**Endpoint:** `/map`

Authorizations

Authorization
stringheaderrequired

Bearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

Body
application/json

Parameters for the Tavily Map request.

url
stringrequired

The root URL to begin the mapping.

Example:

"docs.tavily.com"

instructions
string

Natural language instructions for the crawler. When specified, the cost increases to 2 API credits per 10 successful pages instead of 1 API credit per 10 pages.

Example:

"Find all pages about the Python SDK"

max_depth
integerdefault:1

Max depth of the mapping. Defines how far from the base URL the crawler can explore.

Required range: 1 <= x <= 5

max_breadth
integerdefault:20

Max number of links to follow per level of the tree (i.e., per page).

Required range: 1 <= x <= 500

limit
integerdefault:50

Total number of links the crawler will process before stopping.

Required range: x >= 1

select_paths
string[]

Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*).

select_domains
string[]

Regex patterns to select crawling to specific domains or subdomains (e.g., ^docs\.example\.com$).

exclude_paths
string[]

Regex patterns to exclude URLs with specific path patterns (e.g., /private/.*, /admin/.*).

exclude_domains
string[]

Regex patterns to exclude specific domains or subdomains from crawling (e.g., ^private\.example\.com$).

allow_external
booleandefault:true

Whether to include external domain links in the final results list.

timeout
number<float>default:150

Maximum time in seconds to wait for the map operation before timing out. Must be between 10 and 150 seconds.

Required range: 10 <= x <= 150

include_usage
booleandefault:false

Whether to include credit usage information in the response.NOTE:The value may be 0 if the total successful pages mapped has not yet reached 10 calls. See our Credits & Pricing documentation for details.

Response
200
application/json

Map results returned successfully

base_url
string

The base URL that was mapped.

Example:

"docs.tavily.com"

results
string[]

A list of URLs that were discovered during the mapping.

Example:
[
  "https://docs.tavily.com/welcome",
  "https://docs.tavily.com/documentation/api-credits",
  "https://docs.tavily.com/documentation/about"
]

response_time
number<float>

Time in seconds it took to complete the request.

Example:

1.23

usage
object

Credit usage details for the request.

Example:
{ "credits": 1 }

request_id
string

A unique request identifier you can share with customer support to help resolve issues with specific requests.

Example:

"123e4567-e89b-12d3-a456-426614174111"
