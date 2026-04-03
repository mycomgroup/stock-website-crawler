---
id: "url-22cade2"
type: "api"
title: "Create Research Task"
url: "https://docs.tavily.com/documentation/api-reference/endpoint/research"
description: "Tavily Research performs comprehensive research on a given topic by conducting multiple searches, analyzing sources, and generating a detailed research report."
source: ""
tags: []
crawl_time: "2026-03-18T07:49:17.244Z"
metadata:
  method: "POST"
  endpoint: "/research"
  baseUrl: "https://api.tavily.com"
  parameters:
    - {"name":"Authorization","type":"string","required":true,"default":"","description":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).","location":"header"}
    - {"name":"input","type":"string","required":true,"default":"","description":"The research task or question to investigate.Example:\"What are the latest developments in AI?\""}
    - {"name":"model","type":"enum<string>","required":false,"default":"autoThe","description":"model used by the research agent. \"mini\" is optimized for targeted, efficient research and works best for narrow or well-scoped questions. \"pro\" provides comprehensive, multi-angle research and is suited for complex topics that span multiple subtopics or domainsAvailable options: mini, pro, auto"}
    - {"name":"stream","type":"boolean","required":false,"default":"","description":"default:falseWhether to stream the research results as they are generated. When 'true', returns a Server-Sent Events (SSE) stream. See Streaming documentation for details."}
    - {"name":"citation_format","type":"enum<string>","required":false,"default":"numberedThe","description":"format for citations in the research report.Available options: numbered, mla, apa, chicago"}
    - {"name":"request_id","type":"string","required":true,"default":"","description":"A unique identifier for the research task.Example:\"123e4567-e89b-12d3-a456-426614174111\""}
    - {"name":"created_at","type":"string","required":true,"default":"","description":"Timestamp when the research task was created.Example:\"2025-01-15T10:30:00Z\""}
    - {"name":"status","type":"string","required":true,"default":"","description":"The current status of the research task.Example:\"pending\""}
    - {"name":"response_time","type":"integer","required":true,"default":"","description":"Time in seconds it took to complete the request.Example:1.23"}
    - {"name":"output_schema","type":"object","required":false,"default":"","description":"A JSON Schema object that defines the structure of the research output. When provided, the research response will be structured to match this schema, ensuring a predictable and validated output shape. Must include a 'properties' field, and may optionally include 'required' field.Hide child attributes​output_schema.propertiesobjectAn object containing property definitions. Each key is a property name, and each value is a property schema.Show child attributes​output_schema.requiredstring[]An array"}
    - {"name":"output_schema.properties","type":"object","required":false,"default":"","description":"An object containing property definitions. Each key is a property name, and each value is a property schema.Show child attributes"}
    - {"name":"output_schema.required","type":"string[]","required":false,"default":"","description":"An array of property names that are required. At least one key from the properties object must be included."}
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.research(\"What are the latest developments in AI?\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"created_at\": \"2025-01-15T10:30:00Z\",\n  \"status\": \"pending\",\n  \"input\": \"What are the latest developments in AI?\",\n  \"model\": \"mini\",\n  \"response_time\": 1.23\n}"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.research(\"What are the latest developments in AI?\")\n\nprint(response)"}
    - {"language":"json","code":"{\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"created_at\": \"2025-01-15T10:30:00Z\",\n  \"status\": \"pending\",\n  \"input\": \"What are the latest developments in AI?\",\n  \"model\": \"mini\",\n  \"response_time\": 1.23\n}"}
    - {"language":"json","code":"{  \"properties\": {    \"company\": {      \"type\": \"string\",      \"description\": \"The name of the company\"    },    \"key_metrics\": {      \"type\": \"array\",      \"description\": \"List of key performance metrics\",      \"items\": { \"type\": \"string\" }    },    \"financial_details\": {      \"type\": \"object\",      \"description\": \"Detailed financial breakdown\",      \"properties\": {        \"operating_income\": {          \"type\": \"number\",          \"description\": \"Operating income for the period\"        }      }    }  },  \"required\": [\"company\"]}"}
  mainContent:
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Body"}
    - {"type":"paragraph","content":"Parameters for the Tavily Research request."}
    - {"type":"parameter","name":"\"What are the latest developments in AI?\"","paramType":"","description":"​inputstringrequiredThe research task or question to investigate.Example:\"What are the latest developments in AI?\"​modelenum<string>default:autoThe model used by the research agent. \"mini\" is optimized for targeted, efficient research and works best for narrow or well-scoped questions. \"pro\" provides comprehensive, multi-angle research and is suited for complex topics that span multiple subtopics or domainsAvailable options: mini, pro, auto ​streambooleandefault:falseWhether to stream the research results as they are generated. When 'true', returns a Server-Sent Events (SSE) stream. See Streaming documentation for details.​output_schemaobjectA JSON Schema object that defines the structure of the research output. When provided, the research response will be structured to match this schema, ensuring a predictable and validated output shape. Must include a 'properties' field, and may optionally include 'required' field.Hide child attributes​output_schema.propertiesobjectAn object containing property definitions. Each key is a property name, and each value is a property schema.Show child attributes​output_schema.requiredstring[]An array of property names that are required. At least one key from the properties object must be included.Example:{  \"properties\": {    \"company\": {      \"type\": \"string\",      \"description\": \"The name of the company\"    },    \"key_metrics\": {      \"type\": \"array\",      \"description\": \"List of key performance metrics\",      \"items\": { \"type\": \"string\" }    },    \"financial_details\": {      \"type\": \"object\",      \"description\": \"Detailed financial breakdown\",      \"properties\": {        \"operating_income\": {          \"type\": \"number\",          \"description\": \"Operating income for the period\"        }      }    }  },  \"required\": [\"company\"]}​citation_formatenum<string>default:numberedThe format for citations in the research report.Available options: numbered, mla, apa, chicago"}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Research task queued successfully (when not streaming)"}
    - {"type":"parameter","name":"\"123e4567-e89b-12d3-a456-426614174111\"","paramType":"","description":"​request_idstringrequiredA unique identifier for the research task.Example:\"123e4567-e89b-12d3-a456-426614174111\"​created_atstringrequiredTimestamp when the research task was created.Example:\"2025-01-15T10:30:00Z\"​statusstringrequiredThe current status of the research task.Example:\"pending\"​inputstringrequiredThe research task or question investigated.Example:\"What are the latest developments in AI?\"​modelstringrequiredThe model used by the research agent.Example:\"mini\"​response_timeintegerrequiredTime in seconds it took to complete the request.Example:1.23"}
  rawContent: "Authorizations\n​\nAuthorization\nstringheaderrequired\n\nBearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).\n\nBody\napplication/json\n\nParameters for the Tavily Research request.\n\n​\ninput\nstringrequired\n\nThe research task or question to investigate.\n\nExample:\n\n\"What are the latest developments in AI?\"\n\n​\nmodel\nenum<string>default:auto\n\nThe model used by the research agent. \"mini\" is optimized for targeted, efficient research and works best for narrow or well-scoped questions. \"pro\" provides comprehensive, multi-angle research and is suited for complex topics that span multiple subtopics or domains\n\nAvailable options: mini, pro, auto \n​\nstream\nbooleandefault:false\n\nWhether to stream the research results as they are generated. When 'true', returns a Server-Sent Events (SSE) stream. See Streaming documentation for details.\n\n​\noutput_schema\nobject\n\nA JSON Schema object that defines the structure of the research output. When provided, the research response will be structured to match this schema, ensuring a predictable and validated output shape. Must include a 'properties' field, and may optionally include 'required' field.\n\nHide child attributes\n\n​\noutput_schema.properties\nobject\n\nAn object containing property definitions. Each key is a property name, and each value is a property schema.\n\nShow child attributes\n\n​\noutput_schema.required\nstring[]\n\nAn array of property names that are required. At least one key from the properties object must be included.\n\nExample:\n{\n  \"properties\": {\n    \"company\": {\n      \"type\": \"string\",\n      \"description\": \"The name of the company\"\n    },\n    \"key_metrics\": {\n      \"type\": \"array\",\n      \"description\": \"List of key performance metrics\",\n      \"items\": { \"type\": \"string\" }\n    },\n    \"financial_details\": {\n      \"type\": \"object\",\n      \"description\": \"Detailed financial breakdown\",\n      \"properties\": {\n        \"operating_income\": {\n          \"type\": \"number\",\n          \"description\": \"Operating income for the period\"\n        }\n      }\n    }\n  },\n  \"required\": [\"company\"]\n}\n​\ncitation_format\nenum<string>default:numbered\n\nThe format for citations in the research report.\n\nAvailable options: numbered, mla, apa, chicago \nResponse\n201\napplication/json\n\nResearch task queued successfully (when not streaming)\n\n​\nrequest_id\nstringrequired\n\nA unique identifier for the research task.\n\nExample:\n\n\"123e4567-e89b-12d3-a456-426614174111\"\n\n​\ncreated_at\nstringrequired\n\nTimestamp when the research task was created.\n\nExample:\n\n\"2025-01-15T10:30:00Z\"\n\n​\nstatus\nstringrequired\n\nThe current status of the research task.\n\nExample:\n\n\"pending\"\n\n​\ninput\nstringrequired\n\nThe research task or question investigated.\n\nExample:\n\n\"What are the latest developments in AI?\"\n\n​\nmodel\nstringrequired\n\nThe model used by the research agent.\n\nExample:\n\n\"mini\"\n\n​\nresponse_time\nintegerrequired\n\nTime in seconds it took to complete the request.\n\nExample:\n\n1.23"
  suggestedFilename: "endpoint_research"
---

# Create Research Task

## 源URL

https://docs.tavily.com/documentation/api-reference/endpoint/research

## 描述

Tavily Research performs comprehensive research on a given topic by conducting multiple searches, analyzing sources, and generating a detailed research report.

## API 端点

**Method**: `POST`
**Endpoint**: `/research`
**Base URL**: `https://api.tavily.com`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Authorization` | string | 是 | - | Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY). |
| `input` | string | 是 | - | The research task or question to investigate.Example:"What are the latest developments in AI?" |
| `model` | enum<string> | 否 | autoThe | model used by the research agent. "mini" is optimized for targeted, efficient research and works best for narrow or well-scoped questions. "pro" provides comprehensive, multi-angle research and is suited for complex topics that span multiple subtopics or domainsAvailable options: mini, pro, auto |
| `stream` | boolean | 否 | - | default:falseWhether to stream the research results as they are generated. When 'true', returns a Server-Sent Events (SSE) stream. See Streaming documentation for details. |
| `citation_format` | enum<string> | 否 | numberedThe | format for citations in the research report.Available options: numbered, mla, apa, chicago |
| `request_id` | string | 是 | - | A unique identifier for the research task.Example:"123e4567-e89b-12d3-a456-426614174111" |
| `created_at` | string | 是 | - | Timestamp when the research task was created.Example:"2025-01-15T10:30:00Z" |
| `status` | string | 是 | - | The current status of the research task.Example:"pending" |
| `response_time` | integer | 是 | - | Time in seconds it took to complete the request.Example:1.23 |
| `output_schema` | object | 否 | - | A JSON Schema object that defines the structure of the research output. When provided, the research response will be structured to match this schema, ensuring a predictable and validated output shape. Must include a 'properties' field, and may optionally include 'required' field.Hide child attributesoutput_schema.propertiesobjectAn object containing property definitions. Each key is a property name, and each value is a property schema.Show child attributesoutput_schema.requiredstring[]An array |
| `output_schema.properties` | object | 否 | - | An object containing property definitions. Each key is a property name, and each value is a property schema.Show child attributes |
| `output_schema.required` | string[] | 否 | - | An array of property names that are required. At least one key from the properties object must be included. |

## 代码示例

### 示例 1 (text)

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.research("What are the latest developments in AI?")

print(response)
```

### 示例 2 (json)

```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174111",
  "created_at": "2025-01-15T10:30:00Z",
  "status": "pending",
  "input": "What are the latest developments in AI?",
  "model": "mini",
  "response_time": 1.23
}
```

### 示例 3 (json)

```json
{  "properties": {    "company": {      "type": "string",      "description": "The name of the company"    },    "key_metrics": {      "type": "array",      "description": "List of key performance metrics",      "items": { "type": "string" }    },    "financial_details": {      "type": "object",      "description": "Detailed financial breakdown",      "properties": {        "operating_income": {          "type": "number",          "description": "Operating income for the period"        }      }    }  },  "required": ["company"]}
```

## 文档正文

Tavily Research performs comprehensive research on a given topic by conducting multiple searches, analyzing sources, and generating a detailed research report.

## API 端点

**Method:** `POST`
**Endpoint:** `/research`

Authorizations

Authorization
stringheaderrequired

Bearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

Body
application/json

Parameters for the Tavily Research request.

input
stringrequired

The research task or question to investigate.

Example:

"What are the latest developments in AI?"

model
enum<string>default:auto

The model used by the research agent. "mini" is optimized for targeted, efficient research and works best for narrow or well-scoped questions. "pro" provides comprehensive, multi-angle research and is suited for complex topics that span multiple subtopics or domains

Available options: mini, pro, auto 

stream
booleandefault:false

Whether to stream the research results as they are generated. When 'true', returns a Server-Sent Events (SSE) stream. See Streaming documentation for details.

output_schema
object

A JSON Schema object that defines the structure of the research output. When provided, the research response will be structured to match this schema, ensuring a predictable and validated output shape. Must include a 'properties' field, and may optionally include 'required' field.

Hide child attributes

output_schema.properties
object

An object containing property definitions. Each key is a property name, and each value is a property schema.

Show child attributes

output_schema.required
string[]

An array of property names that are required. At least one key from the properties object must be included.

Example:
{
  "properties": {
    "company": {
      "type": "string",
      "description": "The name of the company"
    },
    "key_metrics": {
      "type": "array",
      "description": "List of key performance metrics",
      "items": { "type": "string" }
    },
    "financial_details": {
      "type": "object",
      "description": "Detailed financial breakdown",
      "properties": {
        "operating_income": {
          "type": "number",
          "description": "Operating income for the period"
        }
      }
    }
  },
  "required": ["company"]
}

citation_format
enum<string>default:numbered

The format for citations in the research report.

Available options: numbered, mla, apa, chicago 
Response
201
application/json

Research task queued successfully (when not streaming)

request_id
stringrequired

A unique identifier for the research task.

Example:

"123e4567-e89b-12d3-a456-426614174111"

created_at
stringrequired

Timestamp when the research task was created.

Example:

"2025-01-15T10:30:00Z"

status
stringrequired

The current status of the research task.

Example:

"pending"

input
stringrequired

The research task or question investigated.

Example:

"What are the latest developments in AI?"

model
stringrequired

The model used by the research agent.

Example:

"mini"

response_time
integerrequired

Time in seconds it took to complete the request.

Example:

1.23
