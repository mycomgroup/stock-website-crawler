---
id: "url-5166d92b"
type: "api"
title: "SerpApi MCP - The Web Search MCP"
url: "https://serpapi.com/integrations/mcp"
description: "A Model Context Protocol (MCP) server implementation that integrates with SerpApi for comprehensive search engine results and data extraction.\n\nSerpApi MCP Server is available as a hosted service at mcp.serpapi.com. In order to connect to it, you need to provide an API key. You can find your API key on your SerpApi dashboard.\n\nYou can configure Claude Desktop to use the hosted server:\n\nGet your API key: serpapi.com/manage-api-key\n\nThe MCP server has one main Search Tool that supports all SerpApi engines and result types. You can find all available parameters on the SerpApi API reference. Engine parameter schemas are also exposed as MCP resources: serpapi://engines (index) and serpapi://engines/<engine>."
source: ""
tags: []
crawl_time: "2026-03-18T14:31:11.479Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example 1","description":"","requestParams":{},"responseJson":"{\n  \"mcpServers\": {\n    \"serpapi\": {\n      \"url\": \"https://mcp.serpapi.com/YOUR_SERPAPI_API_KEY/mcp\"\n    }\n  }\n}"}
    - {"title":"Example 3","description":"","requestParams":{},"responseJson":"{\n  \"mcpServers\": {\n    \"serpapi\": {\n      \"url\": \"http://localhost:8000/YOUR_SERPAPI_API_KEY/mcp\"\n    }\n  }\n}"}
    - {"title":"Example 5","description":"","requestParams":{},"responseJson":"{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"coffee shops\", \"location\": \"Austin, TX\"}}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"weather in London\"}}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"AAPL stock\"}}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"news\"}, \"mode\": \"compact\"}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"detailed search\"}, \"mode\": \"complete\"}}"}
  importantNotes: []
  rawContent: "Documentation\n\nIntegrations\n\nDocumentation\n\nIntegrations\n\nSerpApi MCP - The Web Search MCP\n\nEnabling AI agents to search and extract data from Google, Bing, and other search engines via Model Context Protocol.\n\nThe SerpApi MCP Server connects SerpApi’s multi‑engine search capabilities to MCP‑compatible clients like Claude Desktop, VS Code, Cursor, and other AI assistants.\n\nThis integration allows AI assistants to perform live searches using your SerpApi subscription without requiring custom tool implementation.\n\nSerpApi MCP Server\n\nA Model Context Protocol (MCP) server implementation that integrates with SerpApi for comprehensive search engine results and data extraction.\n\nMulti-Engine Search: Google, Bing, Yahoo, DuckDuckGo, YouTube, eBay, and more\n\nEngine Resources: Per-engine parameter schemas available via MCP resources (see Search Tool)\n\nReal-time Weather Data: Location-based weather with forecasts via search queries\n\nStock Market Data: Company financials and market data through search integration\n\nDynamic Result Processing: Automatically detects and formats different result types\n\nFlexible Response Modes: Complete or compact JSON responses\n\nJSON Responses: Structured JSON output with complete or compact modes\n\nQuick Start\n\nSerpApi MCP Server is available as a hosted service at mcp.serpapi.com. In order to connect to it, you need to provide an API key. You can find your API key on your SerpApi dashboard.\n\nYou can configure Claude Desktop to use the hosted server:\n\n{\n  \"mcpServers\": {\n    \"serpapi\": {\n      \"url\": \"https://mcp.serpapi.com/YOUR_SERPAPI_API_KEY/mcp\"\n    }\n  }\n}\n\nSelf-Hosting\n\ngit clone https://github.com/serpapi/serpapi-mcp.git\ncd serpapi-mcp\nuv sync && uv run src/server.py\n\nConfigure Claude Desktop:\n\n{\n  \"mcpServers\": {\n    \"serpapi\": {\n      \"url\": \"http://localhost:8000/YOUR_SERPAPI_API_KEY/mcp\"\n    }\n  }\n}\n\nGet your API key: serpapi.com/manage-api-key\n\nAuthentication\n\nTwo methods are supported:\n\nPath-based: /YOUR_API_KEY/mcp (recommended)\n\nHeader-based: Authorization: Bearer YOUR_API_KEY\n\n# Path-based\ncurl \"https://mcp.serpapi.com/your_key/mcp\" -d '...'\n\n# Header-based  \ncurl \"https://mcp.serpapi.com/mcp\" -H \"Authorization: Bearer your_key\" -d '...'\n\nSearch Tool\n\nThe MCP server has one main Search Tool that supports all SerpApi engines and result types. You can find all available parameters on the SerpApi API reference.\nEngine parameter schemas are also exposed as MCP resources: serpapi://engines (index) and serpapi://engines/<engine>.\n\nThe parameters you can provide are specific for each API engine. Some sample parameters are provided below:\n\nparams.q (required): Search query\n\nparams.engine: Search engine (default: \"google_light\")\n\nparams.location: Geographic filter\n\nmode: Response mode - \"complete\" (default) or \"compact\"\n\n...see other parameters on the SerpApi API reference\n\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"coffee shops\", \"location\": \"Austin, TX\"}}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"weather in London\"}}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"AAPL stock\"}}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"news\"}, \"mode\": \"compact\"}}\n{\"name\": \"search\", \"arguments\": {\"params\": {\"q\": \"detailed search\"}, \"mode\": \"complete\"}}\n\nSupported Engines: Google, Bing, Yahoo, DuckDuckGo, YouTube, eBay, and more (see serpapi://engines).\n\nResult Types: Answer boxes, organic results, news, images, shopping - automatically detected and formatted.\n\nDevelopment\n\n# Local development\nuv sync && uv run src/server.py\n\n# Docker\ndocker build -t serpapi-mcp . && docker run -p 8000:8000 serpapi-mcp\n\n# Regenerate engine resources (Playground scrape)\npython build-engines.py\n\n# Testing with MCP Inspector\nnpx @modelcontextprotocol/inspector\n# Configure: URL mcp.serpapi.com/YOUR_KEY/mcp, Transport \"Streamable HTTP transport\"\n\nTroubleshooting\n\n\"Missing API key\": Include key in URL path /{YOUR_KEY}/mcp or header Bearer YOUR_KEY\n\n\"Invalid key\": Verify at serpapi.com/dashboard\n\n\"Rate limit exceeded\": Wait or upgrade your SerpApi plan\n\n\"No results\": Try different query or engine\n\nContributing\n\nFork the repository\n\nCreate your feature branch: git checkout -b feature/amazing-feature\n\nInstall dependencies: uv install\n\nMake your changes\n\nCommit changes: git commit -m 'Add amazing feature'\n\nPush to branch: git push origin feature/amazing-feature\n\nOpen a Pull Request\n\nMIT License - see LICENSE file for details.\n\nSerpApi MCP is open source and available on GitHub.\n\nFree Plan · 250 searches / month\n\nThey trust us\n\nYou are in good company. Join them.\n\nDocumentation\n\nGoogle Search API\n\nGoogle Light Search API\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Flights API\n\nGoogle Forums API\n\nGoogle Hotels API\n\nGoogle Images API\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nGoogle Lens API\n\nGoogle Light Fast API\n\nGoogle Local API\n\nGoogle Local Services API\n\nGoogle Maps API\n\nGoogle Maps Reviews API\n\nGoogle News API\n\nGoogle News Light API\n\nGoogle Patents API\n\nGoogle Play Store API\n\nGoogle Related Questions API\n\nGoogle Reverse Image API\n\nGoogle Scholar API\n\nGoogle Shopping API\n\nGoogle Shopping Light API\n\nGoogle Short Videos API\n\nGoogle Travel Explore API\n\nGoogle Trends API\n\nGoogle Videos API\n\nGoogle Videos Light API\n\nAmazon Search API\n\nAmazon Product API"
  suggestedFilename: "integrations_mcp-api"
---

# SerpApi MCP - The Web Search MCP

## 源URL

https://serpapi.com/integrations/mcp

## 描述

A Model Context Protocol (MCP) server implementation that integrates with SerpApi for comprehensive search engine results and data extraction.

SerpApi MCP Server is available as a hosted service at mcp.serpapi.com. In order to connect to it, you need to provide an API key. You can find your API key on your SerpApi dashboard.

You can configure Claude Desktop to use the hosted server:

Get your API key: serpapi.com/manage-api-key

The MCP server has one main Search Tool that supports all SerpApi engines and result types. You can find all available parameters on the SerpApi API reference. Engine parameter schemas are also exposed as MCP resources: serpapi://engines (index) and serpapi://engines/<engine>.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

A Model Context Protocol (MCP) server implementation that integrates with SerpApi for comprehensive search engine results and data extraction.

SerpApi MCP Server is available as a hosted service at mcp.serpapi.com. In order to connect to it, you need to provide an API key. You can find your API key on your SerpApi dashboard.

You can configure Claude Desktop to use the hosted server:

Get your API key: serpapi.com/manage-api-key

The MCP server has one main Search Tool that supports all SerpApi engines and result types. You can find all available parameters on the SerpApi API reference. Engine parameter schemas are also exposed as MCP resources: serpapi://engines (index) and serpapi://engines/<engine>.

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Documentation

Integrations

Documentation

Integrations

SerpApi MCP - The Web Search MCP

Enabling AI agents to search and extract data from Google, Bing, and other search engines via Model Context Protocol.

The SerpApi MCP Server connects SerpApi’s multi‑engine search capabilities to MCP‑compatible clients like Claude Desktop, VS Code, Cursor, and other AI assistants.

This integration allows AI assistants to perform live searches using your SerpApi subscription without requiring custom tool implementation.

SerpApi MCP Server

A Model Context Protocol (MCP) server implementation that integrates with SerpApi for comprehensive search engine results and data extraction.

Multi-Engine Search: Google, Bing, Yahoo, DuckDuckGo, YouTube, eBay, and more

Engine Resources: Per-engine parameter schemas available via MCP resources (see Search Tool)

Real-time Weather Data: Location-based weather with forecasts via search queries

Stock Market Data: Company financials and market data through search integration

Dynamic Result Processing: Automatically detects and formats different result types

Flexible Response Modes: Complete or compact JSON responses

JSON Responses: Structured JSON output with complete or compact modes

Quick Start

SerpApi MCP Server is available as a hosted service at mcp.serpapi.com. In order to connect to it, you need to provide an API key. You can find your API key on your SerpApi dashboard.

You can configure Claude Desktop to use the hosted server:

{
  "mcpServers": {
    "serpapi": {
      "url": "https://mcp.serpapi.com/YOUR_SERPAPI_API_KEY/mcp"
    }
  }
}

Self-Hosting

git clone https://github.com/serpapi/serpapi-mcp.git
cd serpapi-mcp
uv sync && uv run src/server.py

Configure Claude Desktop:

{
  "mcpServers": {
    "serpapi": {
      "url": "http://localhost:8000/YOUR_SERPAPI_API_KEY/mcp"
    }
  }
}

Get your API key: serpapi.com/manage-api-key

Authentication

Two methods are supported:

Path-based: /YOUR_API_KEY/mcp (recommended)

Header-based: Authorization: Bearer YOUR_API_KEY

# Path-based
curl "https://mcp.serpapi.com/your_key/mcp" -d '...'

# Header-based  
curl "https://mcp.serpapi.com/mcp" -H "Authorization: Bearer your_key" -d '...'

Search Tool

The MCP server has one main Search Tool that supports all SerpApi engines and result types. You can find all available parameters on the SerpApi API reference.
Engine parameter schemas are also exposed as MCP resources: serpapi://engines (index) and serpapi://engines/<engine>.

The parameters you can provide are specific for each API engine. Some sample parameters are provided below:

params.q (required): Search query

params.engine: Search engine (default: "google_light")

params.location: Geographic filter

mode: Response mode - "complete" (default) or "compact"

...see other parameters on the SerpApi API reference

{"name": "search", "arguments": {"params": {"q": "coffee shops", "location": "Austin, TX"}}}
{"name": "search", "arguments": {"params": {"q": "weather in London"}}}
{"name": "search", "arguments": {"params": {"q": "AAPL stock"}}}
{"name": "search", "arguments": {"params": {"q": "news"}, "mode": "compact"}}
{"name": "search", "arguments": {"params": {"q": "detailed search"}, "mode": "complete"}}

Supported Engines: Google, Bing, Yahoo, DuckDuckGo, YouTube, eBay, and more (see serpapi://engines).

Result Types: Answer boxes, organic results, news, images, shopping - automatically detected and formatted.

Development

# Local development
uv sync && uv run src/server.py

# Docker
docker build -t serpapi-mcp . && docker run -p 8000:8000 serpapi-mcp

# Regenerate engine resources (Playground scrape)
python build-engines.py

# Testing with MCP Inspector
npx @modelcontextprotocol/inspector
# Configure: URL mcp.serpapi.com/YOUR_KEY/mcp, Transport "Streamable HTTP transport"

Troubleshooting

"Missing API key": Include key in URL path /{YOUR_KEY}/mcp or header Bearer YOUR_KEY

"Invalid key": Verify at serpapi.com/dashboard

"Rate limit exceeded": Wait or upgrade your SerpApi plan

"No results": Try different query or engine

Contributing

Fork the repository

Create your feature branch: git checkout -b feature/amazing-feature

Install dependencies: uv install

Make your changes

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request

MIT License - see LICENSE file for details.

SerpApi MCP is open source and available on GitHub.

Free Plan · 250 searches / month

They trust us

You are in good company. Join them.

Documentation

Google Search API

Google Light Search API

Google AI Mode API

Google AI Overview API

Google Ads Transparency API

Google Autocomplete API

Google Events API

Google Finance API

Google Flights API

Google Forums API

Google Hotels API

Google Images API

Google Images Light API

Google Immersive Product API

Google Jobs API

Google Lens API

Google Light Fast API

Google Local API

Google Local Services API

Google Maps
