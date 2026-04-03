---
id: "url-7642e1bf"
type: "api"
title: "MCP Server For Financial Data by EODHD"
url: "https://eodhd.com/financial-apis/mcp-server-for-financial-data-by-eodhd"
description: "The official MCP-server for EODHD makes it easy for AI agents and large language models (LLMs) to connect with real-time and historical financial data using the Model Context Protocol (MCP). With this integration, not only popular AI platforms like ChatGPT and Claude can access EODHD’s rich financial datasets, but also any custom-trained LLMs, AI assistants, or autonomous agents. This gives developers and fintech teams a powerful way to bring stock market data, fundamental datasets, and intraday quotes directly into their AI workflows."
source: ""
tags: []
crawl_time: "2026-03-18T04:40:54.777Z"
metadata:
  endpoint: ""
  parameters:
    - {"name":"3. Go to Connectors (or “Sources”) tab and click Add connector / source","description":"You should see an option to “Add MCP server” or similar."}
    - {"name":"6. In a new Chat, click “Add sources” (or “+ / Sources”) and select your newly added MCP connector","description":"This attaches the MCP to that chat session. (Vercel)"}
  markdownContent: "# MCP Server For Financial Data by EODHD\n\nThe official MCP-server for EODHD makes it easy for AI agents and large language models (LLMs) to connect with real-time and historical financial data using the Model Context Protocol (MCP). With this integration, not only popular AI platforms like ChatGPT and Claude can access EODHD’s rich financial datasets, but also any custom-trained LLMs, AI assistants, or autonomous agents. This gives developers and fintech teams a powerful way to bring stock market data, fundamental datasets, and intraday quotes directly into their AI workflows.\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| 3. Go to Connectors (or “Sources”) tab and click Add connector / source | You should see an option to “Add MCP server” or similar. |\n| 6. In a new Chat, click “Add sources” (or “+ / Sources”) and select your newly added MCP connector | This attaches the MCP to that chat session. (Vercel) |\n\n\n## Parameters\n\nTo access our server, you need to provide an API key as a parameter. This is how we determine which data a user can access. Sign up for free to get your API key. The free plan grants access to limited data – you can compare access levels on our pricing page. You can also use the “demo” key:\n\n## How to add MCP server to ChatGPT\n\nUse a tool through the MCP For example, ask ChatGPT:“Use the get_stock_price tool via EODHD to fetch AAPL historical data for 2024”ChatGPT will call the MCP server under the hood, execute the tool, and return results.\n\n## Install and Run Locally\n\nOur MCP server is open source and can be downloaded and run locally. Visit the EODHD GitHub repository to get started – setup instructions are provided in the readme.md file.\n\n## Tools\n\nEODHD main datasets:\n\nMarketplace products (by EODHD):\n\nMarketplace products (third party providers):\n\nPraams products:\n\nESG by Investverte:\n\nMore endpoints and datasets to be added soon. Feel free to contact our support if you are expecting something specific.\n\n## Code Examples\n\n```text\nhttps://mcp.eodhd.dev/mcp\n```\n\n```text\nhttps://mcp.eodhd.dev/mcp?apikey=YOUR_API_KEY\n```\n\n```json\n{\n  \"mcpServers\": {\n    \"eodhd-mcp\": {\n      \"command\": \"python3\",\n      \"args\": [\n        \"/home/user/EODHD_MCP_server/server.py\", //actual path to the library\n        \"--stdio\"\n      ],\n       \"env\": {\n           \"EODHD_API_KEY\": \"YOUR_EODHD_API_KEY\" //your valid EODHD API key\n         }\n    }\n  }\n}\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "mcp-server-for-financial-data-by-eodhd"
---

# MCP Server For Financial Data by EODHD

## 源URL

https://eodhd.com/financial-apis/mcp-server-for-financial-data-by-eodhd

## 描述

The official MCP-server for EODHD makes it easy for AI agents and large language models (LLMs) to connect with real-time and historical financial data using the Model Context Protocol (MCP). With this integration, not only popular AI platforms like ChatGPT and Claude can access EODHD’s rich financial datasets, but also any custom-trained LLMs, AI assistants, or autonomous agents. This gives developers and fintech teams a powerful way to bring stock market data, fundamental datasets, and intraday quotes directly into their AI workflows.

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `3. Go to Connectors (or “Sources”) tab and click Add connector / source` | - | 否 | - | You should see an option to “Add MCP server” or similar. |
| `6. In a new Chat, click “Add sources” (or “+ / Sources”) and select your newly added MCP connector` | - | 否 | - | This attaches the MCP to that chat session. (Vercel) |

## 文档正文

The official MCP-server for EODHD makes it easy for AI agents and large language models (LLMs) to connect with real-time and historical financial data using the Model Context Protocol (MCP). With this integration, not only popular AI platforms like ChatGPT and Claude can access EODHD’s rich financial datasets, but also any custom-trained LLMs, AI assistants, or autonomous agents. This gives developers and fintech teams a powerful way to bring stock market data, fundamental datasets, and intraday quotes directly into their AI workflows.

## Parameters

| Parameter | Description |
|-----------|-------------|
| 3. Go to Connectors (or “Sources”) tab and click Add connector / source | You should see an option to “Add MCP server” or similar. |
| 6. In a new Chat, click “Add sources” (or “+ / Sources”) and select your newly added MCP connector | This attaches the MCP to that chat session. (Vercel) |

## Parameters

To access our server, you need to provide an API key as a parameter. This is how we determine which data a user can access. Sign up for free to get your API key. The free plan grants access to limited data – you can compare access levels on our pricing page. You can also use the “demo” key:

## How to add MCP server to ChatGPT

Use a tool through the MCP For example, ask ChatGPT:“Use the get_stock_price tool via EODHD to fetch AAPL historical data for 2024”ChatGPT will call the MCP server under the hood, execute the tool, and return results.

## Install and Run Locally

Our MCP server is open source and can be downloaded and run locally. Visit the EODHD GitHub repository to get started – setup instructions are provided in the readme.md file.

## Tools

EODHD main datasets:

Marketplace products (by EODHD):

Marketplace products (third party providers):

Praams products:

ESG by Investverte:

More endpoints and datasets to be added soon. Feel free to contact our support if you are expecting something specific.

## Code Examples

```text
https://mcp.eodhd.dev/mcp
```

```text
https://mcp.eodhd.dev/mcp?apikey=YOUR_API_KEY
```

```json
{
  "mcpServers": {
    "eodhd-mcp": {
      "command": "python3",
      "args": [
        "/home/user/EODHD_MCP_server/server.py", //actual path to the library
        "--stdio"
      ],
       "env": {
           "EODHD_API_KEY": "YOUR_EODHD_API_KEY" //your valid EODHD API key
         }
    }
  }
}
```

## Related APIs

- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)
- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)
- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)
- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)
- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)
- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)
- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)
- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)
- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)
- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)
