---
id: "url-5bc5408d"
type: "api"
title: "Streaming"
url: "https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming"
description: "Stream real-time research progress and results from Tavily Research API"
source: ""
tags: []
crawl_time: "2026-03-18T07:50:41.805Z"
metadata:
  method: ""
  endpoint: "/research-streaming"
  baseUrl: "https://api.tavily.com"
  parameters:
    - {"name":"Planning","type":"","required":false,"description":"Initializes the research plan based on the input query"}
    - {"name":"Generating","type":"","required":false,"description":"Generates the final research report from collected information"}
    - {"name":"WebSearch","type":"","required":false,"description":"Executes web searches to gather information"}
    - {"name":"ResearchSubtopic","type":"","required":false,"description":"Conducts deep research on specific subtopics"}
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"json","code":"{\n  \"input\": \"What are the latest developments in AI?\",\n  \"stream\": true\n}"}
    - {"language":"json","code":"{\n  \"id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329000,\n  \"choices\": [\n    {\n      \"delta\": {\n        // Event-specific data here\n      }\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"id\": \"evt_002\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329005,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"tool_calls\": {\n          \"type\": \"tool_call\",\n          \"tool_call\": [\n            {\n              \"name\": \"WebSearch\",\n              \"id\": \"fc_633b5932-e66c-4523-931a-04a7b79f2578\",\n              \"arguments\": \"Executing 5 search queries\",\n              \"queries\": [\"latest AI developments 2024\", \"machine learning breakthroughs\", \"...\"]\n            }\n          ]\n        }\n      }\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"id\": \"evt_003\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329010,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"tool_calls\": {\n          \"type\": \"tool_response\",\n          \"tool_response\": [\n            {\n              \"name\": \"WebSearch\",\n              \"id\": \"fc_633b5932-e66c-4523-931a-04a7b79f2578\",\n              \"arguments\": \"Completed executing search tool call\",\n              \"sources\": [\n                {\n                  \"url\": \"https://example.com/article\",\n                  \"title\": \"Example Article\",\n                  \"favicon\": \"https://example.com/favicon.ico\"\n                }\n              ]\n            }\n          ]\n        }\n      }\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"id\": \"evt_004\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329015,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"content\": \"# Research Report\\n\\nBased on the latest sources...\"\n      }\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"id\": \"evt_005\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329020,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"sources\": [\n          {\n            \"url\": \"https://example.com/article\",\n            \"title\": \"Example Article Title\",\n            \"favicon\": \"https://example.com/favicon.ico\"\n          }\n        ]\n      }\n    }\n  ]\n}"}
    - {"language":"text","code":"event: done"}
    - {"language":"text","code":"from tavily import TavilyClient\n\n# Step 1. Instantiating your TavilyClient\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\n\n# Step 2. Creating a streaming research task\nstream = tavily_client.research(\n    input=\"Research the latest developments in AI\",\n    model=\"pro\",\n    stream=True\n)\n\nfor chunk in stream:\n    print(chunk.decode('utf-8'))"}
    - {"language":"text","code":"const { tavily } = require(\"@tavily/core\");\n\nconst tvly = tavily({ apiKey: \"tvly-YOUR_API_KEY\" });\n\nconst stream = await tvly.research(\"Research the latest developments in AI\", {\n  model: \"pro\",\n  stream: true,\n});\n\nfor await (const chunk of result as AsyncGenerator<Buffer, void, unknown>) {\n    console.log(chunk.toString('utf-8'));\n}"}
    - {"language":"json","code":"{\n  \"delta\": {\n    \"role\": \"assistant\",\n    \"content\": {\n      \"company\": \"Acme Corp\",\n      \"key_metrics\": [\"Revenue: $1M\", \"Growth: 50%\"],\n      \"summary\": \"Company showing strong growth...\"\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"id\": \"1d77bdf5-38a4-46c1-87a6-663dbc4528ec\",\n  \"object\": \"error\",\n  \"error\": \"An error occurred while streaming the research task\"\n}"}
    - {"language":"json","code":"{\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"created_at\": \"2025-01-15T10:30:00Z\",\n  \"status\": \"pending\",\n  \"input\": \"What are the latest developments in AI?\",\n  \"model\": \"mini\",\n  \"response_time\": 1.23\n}"}
  mainContent:
    - {"type":"heading","level":2,"content":"​Overview"}
    - {"type":"list","listType":"ul","items":["Displaying research progress to users in real-time","Monitoring tool calls and search queries as they execute","Receiving incremental updates during lengthy research operations","Building interactive research interfaces"]}
    - {"type":"heading","level":2,"content":"​Enabling Streaming"}
    - {"type":"codeblock","language":"json","content":"{\n  \"input\": \"What are the latest developments in AI?\",\n  \"stream\": true\n}"}
    - {"type":"heading","level":2,"content":"​Event Structure"}
    - {"type":"codeblock","language":"json","content":"{\n  \"id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329000,\n  \"choices\": [\n    {\n      \"delta\": {\n        // Event-specific data here\n      }\n    }\n  ]\n}"}
    - {"type":"heading","level":3,"content":"​Core Fields"}
    - {"type":"table","headers":["Field","Type","Description"],"rows":[["id","string","Unique identifier for the stream event"],["object","string","Always \"chat.completion.chunk\" for streaming events"],["model","string","The research model being used (\"mini\" or \"pro\")"],["created","integer","Unix timestamp when the event was created"],["choices","array","Array containing the delta with event details"]]}
    - {"type":"heading","level":2,"content":"​Event Types"}
    - {"type":"heading","level":3,"content":"​1. Tool Call Events"}
    - {"type":"codeblock","language":"json","content":"{\n  \"id\": \"evt_002\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329005,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"tool_calls\": {\n          \"type\": \"tool_call\",\n          \"tool_call\": [\n            {\n              \"name\": \"WebSearch\",\n              \"id\": \"fc_633b5932-e66c-4523-931a-04a7b79f2578\",\n              \"arguments\": \"Executing 5 search queries\",\n              \"queries\": [\"latest AI developments 2024\", \"machine learning breakthroughs\", \"...\"]\n            }\n          ]\n        }\n      }\n    }\n  ]\n}"}
    - {"type":"table","headers":["Field","Type","Description"],"rows":[["type","string","Either \"tool_call\" or \"tool_response\""],["tool_call","array","Details about the tool being invoked"],["name","string","Name of the tool (see Tool Types below)"],["id","string","Unique identifier for the tool call"],["arguments","string","Description of the action being performed"],["queries","array","(WebSearch only) The search queries being executed"],["parent_tool_call_id","string","(Pro mode only) ID of the parent tool call for nested operations"]]}
    - {"type":"heading","level":3,"content":"​2. Tool Response Events"}
    - {"type":"codeblock","language":"json","content":"{\n  \"id\": \"evt_003\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329010,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"tool_calls\": {\n          \"type\": \"tool_response\",\n          \"tool_response\": [\n            {\n              \"name\": \"WebSearch\",\n              \"id\": \"fc_633b5932-e66c-4523-931a-04a7b79f2578\",\n              \"arguments\": \"Completed executing search tool call\",\n              \"sources\": [\n                {\n                  \"url\": \"https://example.com/article\",\n                  \"title\": \"Example Article\",\n                  \"favicon\": \"https://example.com/favicon.ico\"\n                }\n              ]\n            }\n          ]\n        }\n      }\n    }\n  ]\n}"}
    - {"type":"table","headers":["Field","Type","Description"],"rows":[["name","string","Name of the tool that completed"],["id","string","Unique identifier matching the original tool call"],["arguments","string","Completion status message"],["sources","array","Sources discovered by the tool (with url, title, favicon)"],["parent_tool_call_id","string","(Pro mode only) ID of the parent tool call"]]}
    - {"type":"heading","level":3,"content":"​3. Content Events"}
    - {"type":"codeblock","language":"json","content":"{\n  \"id\": \"evt_004\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329015,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"content\": \"# Research Report\\n\\nBased on the latest sources...\"\n      }\n    }\n  ]\n}"}
    - {"type":"list","listType":"ul","items":["Can be a string (markdown-formatted report chunks) when no output_schema is provided","Can be an object (structured data) when an output_schema is specified"]}
    - {"type":"heading","level":3,"content":"​4. Sources Event"}
    - {"type":"codeblock","language":"json","content":"{\n  \"id\": \"evt_005\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329020,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"sources\": [\n          {\n            \"url\": \"https://example.com/article\",\n            \"title\": \"Example Article Title\",\n            \"favicon\": \"https://example.com/favicon.ico\"\n          }\n        ]\n      }\n    }\n  ]\n}"}
    - {"type":"table","headers":["Field","Type","Description"],"rows":[["url","string","The URL of the source"],["title","string","The title of the source page"],["favicon","string","URL to the source’s favicon"]]}
    - {"type":"heading","level":3,"content":"​5. Done Event"}
    - {"type":"codeblock","language":"text","content":"event: done"}
    - {"type":"heading","level":2,"content":"​Tool Types"}
    - {"type":"table","headers":["Tool Name","Description","Model"],"rows":[["Planning","Initializes the research plan based on the input query","Both"],["Generating","Generates the final research report from collected information","Both"],["WebSearch","Executes web searches to gather information","Both"],["ResearchSubtopic","Conducts deep research on specific subtopics","Pro only"]]}
    - {"type":"heading","level":3,"content":"​Research Flow Example"}
    - {"type":"list","listType":"ol","items":["Planning tool_call → Initializing research plan","Planning tool_response → Research plan initialized","WebSearch tool_call → Executing search queries (with queries array)","WebSearch tool_response → Search completed (with sources array)","(Pro mode) ResearchSubtopic tool_call/response cycles for deeper research","Generating tool_call → Generating final report","Generating tool_response → Report generated","Content events → Streamed report chunks","Sources event → Complete list of all sources used","Done event → Stream complete"]}
    - {"type":"heading","level":2,"content":"​Handling Streaming Responses"}
    - {"type":"heading","level":3,"content":"​Python Example"}
    - {"type":"codeblock","language":"python","content":"from tavily import TavilyClient\n\n# Step 1. Instantiating your TavilyClient\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\n\n# Step 2. Creating a streaming research task\nstream = tavily_client.research(\n    input=\"Research the latest developments in AI\",\n    model=\"pro\",\n    stream=True\n)\n\nfor chunk in stream:\n    print(chunk.decode('utf-8'))"}
    - {"type":"heading","level":3,"content":"​JavaScript Example"}
    - {"type":"codeblock","language":"javascript","content":"const { tavily } = require(\"@tavily/core\");\n\nconst tvly = tavily({ apiKey: \"tvly-YOUR_API_KEY\" });\n\nconst stream = await tvly.research(\"Research the latest developments in AI\", {\n  model: \"pro\",\n  stream: true,\n});\n\nfor await (const chunk of result as AsyncGenerator<Buffer, void, unknown>) {\n    console.log(chunk.toString('utf-8'));\n}"}
    - {"type":"heading","level":2,"content":"​Structured Output with Streaming"}
    - {"type":"codeblock","language":"json","content":"{\n  \"delta\": {\n    \"role\": \"assistant\",\n    \"content\": {\n      \"company\": \"Acme Corp\",\n      \"key_metrics\": [\"Revenue: $1M\", \"Growth: 50%\"],\n      \"summary\": \"Company showing strong growth...\"\n    }\n  }\n}"}
    - {"type":"heading","level":2,"content":"​Error Handling"}
    - {"type":"codeblock","language":"json","content":"{\n  \"id\": \"1d77bdf5-38a4-46c1-87a6-663dbc4528ec\",\n  \"object\": \"error\",\n  \"error\": \"An error occurred while streaming the research task\"\n}"}
    - {"type":"heading","level":2,"content":"​Non-Streaming Alternative"}
    - {"type":"codeblock","language":"json","content":"{\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"created_at\": \"2025-01-15T10:30:00Z\",\n  \"status\": \"pending\",\n  \"input\": \"What are the latest developments in AI?\",\n  \"model\": \"mini\",\n  \"response_time\": 1.23\n}"}
  rawContent: "​\nOverview\nWhen using the Tavily Research API, you can stream responses in real-time by setting stream: true in your request. This allows you to receive research progress updates, tool calls, and final results as they’re generated, providing a better user experience for long-running research tasks.\nStreaming is particularly useful for:\nDisplaying research progress to users in real-time\nMonitoring tool calls and search queries as they execute\nReceiving incremental updates during lengthy research operations\nBuilding interactive research interfaces\n​\nEnabling Streaming\nTo enable streaming, set the stream parameter to true when making a request to the Research endpoint:\n\n\n{\n  \"input\": \"What are the latest developments in AI?\",\n  \"stream\": true\n}\n\nThe API will respond with a text/event-stream content type, sending Server-Sent Events (SSE) as the research progresses.\n​\nEvent Structure\nEach streaming event follows a consistent structure compatible with the OpenAI chat completions format:\n\n\n{\n  \"id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329000,\n  \"choices\": [\n    {\n      \"delta\": {\n        // Event-specific data here\n      }\n    }\n  ]\n}\n\n​\nCore Fields\nField\tType\tDescription\nid\tstring\tUnique identifier for the stream event\nobject\tstring\tAlways \"chat.completion.chunk\" for streaming events\nmodel\tstring\tThe research model being used (\"mini\" or \"pro\")\ncreated\tinteger\tUnix timestamp when the event was created\nchoices\tarray\tArray containing the delta with event details\n​\nEvent Types\nThe streaming response includes different types of events in the delta object. Here are the main event types you’ll encounter:\n​\n1. Tool Call Events\nWhen the research agent performs actions like web searches, you’ll receive tool call events:\n\n\n{\n  \"id\": \"evt_002\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329005,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"tool_calls\": {\n          \"type\": \"tool_call\",\n          \"tool_call\": [\n            {\n              \"name\": \"WebSearch\",\n              \"id\": \"fc_633b5932-e66c-4523-931a-04a7b79f2578\",\n              \"arguments\": \"Executing 5 search queries\",\n              \"queries\": [\"latest AI developments 2024\", \"machine learning breakthroughs\", \"...\"]\n            }\n          ]\n        }\n      }\n    }\n  ]\n}\n\nTool Call Delta Fields:\nField\tType\tDescription\ntype\tstring\tEither \"tool_call\" or \"tool_response\"\ntool_call\tarray\tDetails about the tool being invoked\nname\tstring\tName of the tool (see Tool Types below)\nid\tstring\tUnique identifier for the tool call\narguments\tstring\tDescription of the action being performed\nqueries\tarray\t(WebSearch only) The search queries being executed\nparent_tool_call_id\tstring\t(Pro mode only) ID of the parent tool call for nested operations\n​\n2. Tool Response Events\nAfter a tool executes, you’ll receive response events with discovered sources:\n\n\n{\n  \"id\": \"evt_003\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329010,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"tool_calls\": {\n          \"type\": \"tool_response\",\n          \"tool_response\": [\n            {\n              \"name\": \"WebSearch\",\n              \"id\": \"fc_633b5932-e66c-4523-931a-04a7b79f2578\",\n              \"arguments\": \"Completed executing search tool call\",\n              \"sources\": [\n                {\n                  \"url\": \"https://example.com/article\",\n                  \"title\": \"Example Article\",\n                  \"favicon\": \"https://example.com/favicon.ico\"\n                }\n              ]\n            }\n          ]\n        }\n      }\n    }\n  ]\n}\n\nTool Response Fields:\nField\tType\tDescription\nname\tstring\tName of the tool that completed\nid\tstring\tUnique identifier matching the original tool call\narguments\tstring\tCompletion status message\nsources\tarray\tSources discovered by the tool (with url, title, favicon)\nparent_tool_call_id\tstring\t(Pro mode only) ID of the parent tool call\n​\n3. Content Events\nThe final research report is streamed as content chunks:\n\n\n{\n  \"id\": \"evt_004\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329015,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"content\": \"# Research Report\\n\\nBased on the latest sources...\"\n      }\n    }\n  ]\n}\n\nContent Field:\nCan be a string (markdown-formatted report chunks) when no output_schema is provided\nCan be an object (structured data) when an output_schema is specified\n​\n4. Sources Event\nAfter the content is streamed, a sources event is emitted containing all sources used in the research:\n\n\n{\n  \"id\": \"evt_005\",\n  \"object\": \"chat.completion.chunk\",\n  \"model\": \"mini\",\n  \"created\": 1705329020,\n  \"choices\": [\n    {\n      \"delta\": {\n        \"role\": \"assistant\",\n        \"sources\": [\n          {\n            \"url\": \"https://example.com/article\",\n            \"title\": \"Example Article Title\",\n            \"favicon\": \"https://example.com/favicon.ico\"\n          }\n        ]\n      }\n    }\n  ]\n}\n\nSource Object Fields:\nField\tType\tDescription\nurl\tstring\tThe URL of the source\ntitle\tstring\tThe title of the source page\nfavicon\tstring\tURL to the source’s favicon\n​\n5. Done Event\nSignals the completion of the streaming response:\n\n\nevent: done\n\n​\nTool Types\nDuring research, you’ll encounter the following tool types in streaming events:\nTool Name\tDescription\tModel\nPlanning\tInitializes the research plan based on the input query\tBoth\nGenerating\tGenerates the final research report from collected information\tBoth\nWebSearch\tExecutes web searches to gather information\tBoth\nResearchSubtopic\tConducts deep research on specific subtopics\tPro only\n​\nResearch Flow Example\nA typical streaming session follows this sequence:\nPlanning tool_call → Initializing research plan\nPlanning tool_response → Research plan initialized\nWebSearch tool_call → Executing search queries (with queries array)\nWebSearch tool_response → Search completed (with sources array)\n(Pro mode) ResearchSubtopic tool_call/response cycles for deeper research\nGenerating tool_call → Generating final report\nGenerating tool_response → Report generated\nContent events → Streamed report chunks\nSources event → Complete list of all sources used\nDone event → Stream complete\n​\nHandling Streaming Responses\n​\nPython Example\n\n\nfrom tavily import TavilyClient\n\n# Step 1. Instantiating your TavilyClient\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\n\n# Step 2. Creating a streaming research task\nstream = tavily_client.research(\n    input=\"Research the latest developments in AI\",\n    model=\"pro\",\n    stream=True\n)\n\nfor chunk in stream:\n    print(chunk.decode('utf-8'))\n\n​\nJavaScript Example\n\n\nconst { tavily } = require(\"@tavily/core\");\n\nconst tvly = tavily({ apiKey: \"tvly-YOUR_API_KEY\" });\n\nconst stream = await tvly.research(\"Research the latest developments in AI\", {\n  model: \"pro\",\n  stream: true,\n});\n\nfor await (const chunk of result as AsyncGenerator<Buffer, void, unknown>) {\n    console.log(chunk.toString('utf-8'));\n}\n\n​\nStructured Output with Streaming\nWhen using output_schema to request structured data, the content field will contain an object instead of a string:\n\n\n{\n  \"delta\": {\n    \"role\": \"assistant\",\n    \"content\": {\n      \"company\": \"Acme Corp\",\n      \"key_metrics\": [\"Revenue: $1M\", \"Growth: 50%\"],\n      \"summary\": \"Company showing strong growth...\"\n    }\n  }\n}\n\n​\nError Handling\nIf an error occurs during streaming, you may receive an error event:\n\n\n{\n  \"id\": \"1d77bdf5-38a4-46c1-87a6-663dbc4528ec\",\n  \"object\": \"error\",\n  \"error\": \"An error occurred while streaming the research task\"\n}\n\nAlways implement proper error handling in your streaming client to gracefully handle these cases.\n​\nNon-Streaming Alternative\nIf you don’t need real-time updates, set stream: false (or omit the parameter) to receive a single complete response:\n\n\n{\n  \"request_id\": \"123e4567-e89b-12d3-a456-426614174111\",\n  \"created_at\": \"2025-01-15T10:30:00Z\",\n  \"status\": \"pending\",\n  \"input\": \"What are the latest developments in AI?\",\n  \"model\": \"mini\",\n  \"response_time\": 1.23\n}\n\nYou can then poll the status endpoint to check when the research is complete."
  suggestedFilename: "endpoint_research-streaming"
---

# Streaming

## 源URL

https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming

## 描述

Stream real-time research progress and results from Tavily Research API

## API 端点

**Endpoint**: `/research-streaming`
**Base URL**: `https://api.tavily.com`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Planning` | - | 否 | - | Initializes the research plan based on the input query |
| `Generating` | - | 否 | - | Generates the final research report from collected information |
| `WebSearch` | - | 否 | - | Executes web searches to gather information |
| `ResearchSubtopic` | - | 否 | - | Conducts deep research on specific subtopics |

## 代码示例

### 示例 1 (json)

```json
{
  "input": "What are the latest developments in AI?",
  "stream": true
}
```

### 示例 2 (json)

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174111",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329000,
  "choices": [
    {
      "delta": {
        // Event-specific data here
      }
    }
  ]
}
```

### 示例 3 (json)

```json
{
  "id": "evt_002",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329005,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "tool_calls": {
          "type": "tool_call",
          "tool_call": [
            {
              "name": "WebSearch",
              "id": "fc_633b5932-e66c-4523-931a-04a7b79f2578",
              "arguments": "Executing 5 search queries",
              "queries": ["latest AI developments 2024", "machine learning breakthroughs", "..."]
            }
          ]
        }
      }
    }
  ]
}
```

### 示例 4 (json)

```json
{
  "id": "evt_003",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329010,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "tool_calls": {
          "type": "tool_response",
          "tool_response": [
            {
              "name": "WebSearch",
              "id": "fc_633b5932-e66c-4523-931a-04a7b79f2578",
              "arguments": "Completed executing search tool call",
              "sources": [
                {
                  "url": "https://example.com/article",
                  "title": "Example Article",
                  "favicon": "https://example.com/favicon.ico"
                }
              ]
            }
          ]
        }
      }
    }
  ]
}
```

### 示例 5 (json)

```json
{
  "id": "evt_004",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329015,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "content": "# Research Report\n\nBased on the latest sources..."
      }
    }
  ]
}
```

### 示例 6 (json)

```json
{
  "id": "evt_005",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329020,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "sources": [
          {
            "url": "https://example.com/article",
            "title": "Example Article Title",
            "favicon": "https://example.com/favicon.ico"
          }
        ]
      }
    }
  ]
}
```

### 示例 7 (text)

```text
event: done
```

### 示例 8 (text)

```text
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")

# Step 2. Creating a streaming research task
stream = tavily_client.research(
    input="Research the latest developments in AI",
    model="pro",
    stream=True
)

for chunk in stream:
    print(chunk.decode('utf-8'))
```

### 示例 9 (text)

```text
const { tavily } = require("@tavily/core");

const tvly = tavily({ apiKey: "tvly-YOUR_API_KEY" });

const stream = await tvly.research("Research the latest developments in AI", {
  model: "pro",
  stream: true,
});

for await (const chunk of result as AsyncGenerator<Buffer, void, unknown>) {
    console.log(chunk.toString('utf-8'));
}
```

### 示例 10 (json)

```json
{
  "delta": {
    "role": "assistant",
    "content": {
      "company": "Acme Corp",
      "key_metrics": ["Revenue: $1M", "Growth: 50%"],
      "summary": "Company showing strong growth..."
    }
  }
}
```

### 示例 11 (json)

```json
{
  "id": "1d77bdf5-38a4-46c1-87a6-663dbc4528ec",
  "object": "error",
  "error": "An error occurred while streaming the research task"
}
```

### 示例 12 (json)

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

## 文档正文

Stream real-time research progress and results from Tavily Research API

## API 端点

**Endpoint:** `/research-streaming`

Overview
When using the Tavily Research API, you can stream responses in real-time by setting stream: true in your request. This allows you to receive research progress updates, tool calls, and final results as they’re generated, providing a better user experience for long-running research tasks.
Streaming is particularly useful for:
Displaying research progress to users in real-time
Monitoring tool calls and search queries as they execute
Receiving incremental updates during lengthy research operations
Building interactive research interfaces

Enabling Streaming
To enable streaming, set the stream parameter to true when making a request to the Research endpoint:

{
  "input": "What are the latest developments in AI?",
  "stream": true
}

The API will respond with a text/event-stream content type, sending Server-Sent Events (SSE) as the research progresses.

Event Structure
Each streaming event follows a consistent structure compatible with the OpenAI chat completions format:

{
  "id": "123e4567-e89b-12d3-a456-426614174111",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329000,
  "choices": [
    {
      "delta": {
        // Event-specific data here
      }
    }
  ]
}

Core Fields
Field	Type	Description
id	string	Unique identifier for the stream event
object	string	Always "chat.completion.chunk" for streaming events
model	string	The research model being used ("mini" or "pro")
created	integer	Unix timestamp when the event was created
choices	array	Array containing the delta with event details

Event Types
The streaming response includes different types of events in the delta object. Here are the main event types you’ll encounter:

1. Tool Call Events
When the research agent performs actions like web searches, you’ll receive tool call events:

{
  "id": "evt_002",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329005,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "tool_calls": {
          "type": "tool_call",
          "tool_call": [
            {
              "name": "WebSearch",
              "id": "fc_633b5932-e66c-4523-931a-04a7b79f2578",
              "arguments": "Executing 5 search queries",
              "queries": ["latest AI developments 2024", "machine learning breakthroughs", "..."]
            }
          ]
        }
      }
    }
  ]
}

Tool Call Delta Fields:
Field	Type	Description
type	string	Either "tool_call" or "tool_response"
tool_call	array	Details about the tool being invoked
name	string	Name of the tool (see Tool Types below)
id	string	Unique identifier for the tool call
arguments	string	Description of the action being performed
queries	array	(WebSearch only) The search queries being executed
parent_tool_call_id	string	(Pro mode only) ID of the parent tool call for nested operations

2. Tool Response Events
After a tool executes, you’ll receive response events with discovered sources:

{
  "id": "evt_003",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329010,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "tool_calls": {
          "type": "tool_response",
          "tool_response": [
            {
              "name": "WebSearch",
              "id": "fc_633b5932-e66c-4523-931a-04a7b79f2578",
              "arguments": "Completed executing search tool call",
              "sources": [
                {
                  "url": "https://example.com/article",
                  "title": "Example Article",
                  "favicon": "https://example.com/favicon.ico"
                }
              ]
            }
          ]
        }
      }
    }
  ]
}

Tool Response Fields:
Field	Type	Description
name	string	Name of the tool that completed
id	string	Unique identifier matching the original tool call
arguments	string	Completion status message
sources	array	Sources discovered by the tool (with url, title, favicon)
parent_tool_call_id	string	(Pro mode only) ID of the parent tool call

3. Content Events
The final research report is streamed as content chunks:

{
  "id": "evt_004",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329015,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "content": "# Research Report\n\nBased on the latest sources..."
      }
    }
  ]
}

Content Field:
Can be a string (markdown-formatted report chunks) when no output_schema is provided
Can be an object (structured data) when an output_schema is specified

4. Sources Event
After the content is streamed, a sources event is emitted containing all sources used in the research:

{
  "id": "evt_005",
  "object": "chat.completion.chunk",
  "model": "mini",
  "created": 1705329020,
  "choices": [
    {
      "delta": {
        "role": "assistant",
        "sources": [
          {
            "url": "https://example.com/article",
            "title": "Example Article Title",
            "favicon": "https://example.com/
