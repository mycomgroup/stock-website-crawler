---
id: "url-17da1c63"
type: "api"
title: "EODHD Claude Skills: Teach Your AI Assistant the Entire Financial API"
url: "https://eodhd.com/financial-apis/eodhd-claude-skills"
description: "AI coding assistants like Claude and Codex are transforming how developers work with APIs. But without structured knowledge about specific APIs, these assistants rely on general training data – which means outdated endpoints, wrong parameter names, and hallucinated responses. EODHD Claude Skills solves this by giving your AI assistant expert-level knowledge of the entire EODHD Financial API."
source: ""
tags: []
crawl_time: "2026-03-18T17:27:33.243Z"
metadata:
  endpoint: ""
  parameters:
    - {"name":"Historical Stock Prices (EOD)","description":"End-of-day OHLCV data for stocks, ETFs, funds"}
  markdownContent: "# EODHD Claude Skills: Teach Your AI Assistant the Entire Financial API\n\nAI coding assistants like Claude and Codex are transforming how developers work with APIs. But without structured knowledge about specific APIs, these assistants rely on general training data – which means outdated endpoints, wrong parameter names, and hallucinated responses. EODHD Claude Skills solves this by giving your AI assistant expert-level knowledge of the entire EODHD Financial API.\n\n## Parameters\n\n| Parameter | Description |\n|-----------|-------------|\n| Historical Stock Prices (EOD) | End-of-day OHLCV data for stocks, ETFs, funds |\n\n\n## What Are Claude Skills?\n\nClaude Skills are structured knowledge packs that teach AI assistants how to use specific tools and APIs correctly. Think of them as a detailed instruction manual that Claude reads before answering your questions.\n\nWithout skills, when you ask Claude “get me AAPL historical prices from EODHD”, it has to guess the endpoint URL, parameter names, and response format. It might get it right, or it might hallucinate an endpoint that doesn’t exist.\n\nWith the EODHD skills installed, Claude knows the exact endpoint (/api/eod/AAPL.US), the correct parameters (from, to, fmt, api_token), and the precise response structure. It can also write working Python scripts, handle edge cases, and explain what each field means.\n\n## What Is EODHD Claude Skills?\n\nEODHD Claude Skills is an open-source skill adapter library that enables AI agents (Claude, Codex) to interact with the EODHD Financial API accurately and reliably. It includes:\n\n## Why You Need This\n\nIf you use Claude Code, Codex, or any AI coding assistant with EODHD data, you have likely encountered these problems:\n\nEODHD Claude Skills eliminates all of these issues. Once installed, your AI assistant has complete, up-to-date knowledge of every EODHD endpoint, parameter, and response format.\n\n## Claude Code (Plugin System)\n\nThe fastest way to install is via the Claude Code plugin system. Open your terminal and run:\n\nThat’s it. Set your API token and start working:\n\nTo manage the plugin later:\n\n## Manual Setup\n\nIf you prefer manual installation, clone the repository:\n\n## What Is Covered\n\nThe skills library documents 72 EODHD API endpoints across all major categories:\n\n## Marketplace Products\n\nThe skills also cover EODHD Marketplace products, including US Options (EOD + contracts), Tick Data, TradingHours, Illio Analytics, Investverte ESG, and PRAAMS risk analytics.\n\n## Reference Guides\n\nBeyond endpoints, the library includes 28 reference guides that help Claude understand the EODHD ecosystem:\n\n## Usage Examples\n\nOnce the skill is installed, you can interact with EODHD data through natural language prompts. Here are practical examples across different use cases.\n\n## Fetch Historical Prices\n\nClaude will call the correct endpoint (/api/eod/AAPL.US), use the right parameters, and format the output in a readable table.\n\n## Write Python Scripts\n\nBecause Claude has the skill loaded, it will use the correct EODHD endpoints, handle pagination for bulk data, and respect rate limits — all without you having to specify any of that.\n\n## Built-in Python Client\n\nThe skills library ships with a lightweight Python client that requires zero external dependencies. It works with Python 3.8+ and supports the most common EODHD endpoints out of the box.\n\n## Tips for Best Results\n\nClaude Code treats installed skills as optional context. To make sure the skill is always used when you work with financial data, follow these tips:\n\n## Reference the Skill in Your Prompt\n\nStart your message with a line like:\n\n## Add a Project-Level Instruction\n\nCreate or edit a CLAUDE.md in your project root and add:\n\nClaude Code reads CLAUDE.md at the start of every session, so this acts as a persistent hint.\n\n## Add a Global Instruction\n\nTo apply the hint across all your projects, add the following to your ~/.claude/CLAUDE.md:\n\n## Code Examples\n\n```text\n# Register the marketplace\n/plugin marketplace add EodHistoricalData/eodhd-claude-skills\n\n# Install the plugin\n/plugin install eodhd-api@eodhd-claude-skills\n```\n\n```text\nexport EODHD_API_TOKEN=\"your_token_here\"\n```\n\n```text\n/plugin update eodhd-api@eodhd-claude-skills      # Update to latest version\n/plugin enable eodhd-api@eodhd-claude-skills       # Enable\n/plugin disable eodhd-api@eodhd-claude-skills      # Disable\n/plugin uninstall eodhd-api@eodhd-claude-skills    # Uninstall\n```\n\n```text\ngit clone https://github.com/EodHistoricalData/eodhd-claude-skills.git\nexport EODHD_API_TOKEN=\"your_token_here\"\n```\n\n```text\nUse the eodhd-api plugin. Fetch daily OHLCV for AAPL.US from 2024-01-01 to 2024-12-31\nand show the first and last 5 rows. API key: demo.\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "eodhd-claude-skills"
---

# EODHD Claude Skills: Teach Your AI Assistant the Entire Financial API

## 源URL

https://eodhd.com/financial-apis/eodhd-claude-skills

## 描述

AI coding assistants like Claude and Codex are transforming how developers work with APIs. But without structured knowledge about specific APIs, these assistants rely on general training data – which means outdated endpoints, wrong parameter names, and hallucinated responses. EODHD Claude Skills solves this by giving your AI assistant expert-level knowledge of the entire EODHD Financial API.

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Historical Stock Prices (EOD)` | - | 否 | - | End-of-day OHLCV data for stocks, ETFs, funds |

## 文档正文

AI coding assistants like Claude and Codex are transforming how developers work with APIs. But without structured knowledge about specific APIs, these assistants rely on general training data – which means outdated endpoints, wrong parameter names, and hallucinated responses. EODHD Claude Skills solves this by giving your AI assistant expert-level knowledge of the entire EODHD Financial API.

## Parameters

| Parameter | Description |
|-----------|-------------|
| Historical Stock Prices (EOD) | End-of-day OHLCV data for stocks, ETFs, funds |

## What Are Claude Skills?

Claude Skills are structured knowledge packs that teach AI assistants how to use specific tools and APIs correctly. Think of them as a detailed instruction manual that Claude reads before answering your questions.

Without skills, when you ask Claude “get me AAPL historical prices from EODHD”, it has to guess the endpoint URL, parameter names, and response format. It might get it right, or it might hallucinate an endpoint that doesn’t exist.

With the EODHD skills installed, Claude knows the exact endpoint (/api/eod/AAPL.US), the correct parameters (from, to, fmt, api_token), and the precise response structure. It can also write working Python scripts, handle edge cases, and explain what each field means.

## What Is EODHD Claude Skills?

EODHD Claude Skills is an open-source skill adapter library that enables AI agents (Claude, Codex) to interact with the EODHD Financial API accurately and reliably. It includes:

## Why You Need This

If you use Claude Code, Codex, or any AI coding assistant with EODHD data, you have likely encountered these problems:

EODHD Claude Skills eliminates all of these issues. Once installed, your AI assistant has complete, up-to-date knowledge of every EODHD endpoint, parameter, and response format.

## Claude Code (Plugin System)

The fastest way to install is via the Claude Code plugin system. Open your terminal and run:

That’s it. Set your API token and start working:

To manage the plugin later:

## Manual Setup

If you prefer manual installation, clone the repository:

## What Is Covered

The skills library documents 72 EODHD API endpoints across all major categories:

## Marketplace Products

The skills also cover EODHD Marketplace products, including US Options (EOD + contracts), Tick Data, TradingHours, Illio Analytics, Investverte ESG, and PRAAMS risk analytics.

## Reference Guides

Beyond endpoints, the library includes 28 reference guides that help Claude understand the EODHD ecosystem:

## Usage Examples

Once the skill is installed, you can interact with EODHD data through natural language prompts. Here are practical examples across different use cases.

## Fetch Historical Prices

Claude will call the correct endpoint (/api/eod/AAPL.US), use the right parameters, and format the output in a readable table.

## Write Python Scripts

Because Claude has the skill loaded, it will use the correct EODHD endpoints, handle pagination for bulk data, and respect rate limits — all without you having to specify any of that.

## Built-in Python Client

The skills library ships with a lightweight Python client that requires zero external dependencies. It works with Python 3.8+ and supports the most common EODHD endpoints out of the box.

## Tips for Best Results

Claude Code treats installed skills as optional context. To make sure the skill is always used when you work with financial data, follow these tips:

## Reference the Skill in Your Prompt

Start your message with a line like:

## Add a Project-Level Instruction

Create or edit a CLAUDE.md in your project root and add:

Claude Code reads CLAUDE.md at the start of every session, so this acts as a persistent hint.

## Add a Global Instruction

To apply the hint across all your projects, add the following to your ~/.claude/CLAUDE.md:

## Code Examples

```text
# Register the marketplace
/plugin marketplace add EodHistoricalData/eodhd-claude-skills

# Install the plugin
/plugin install eodhd-api@eodhd-claude-skills
```

```text
export EODHD_API_TOKEN="your_token_here"
```

```text
/plugin update eodhd-api@eodhd-claude-skills      # Update to latest version
/plugin enable eodhd-api@eodhd-claude-skills       # Enable
/plugin disable eodhd-api@eodhd-claude-skills      # Disable
/plugin uninstall eodhd-api@eodhd-claude-skills    # Uninstall
```

```text
git clone https://github.com/EodHistoricalData/eodhd-claude-skills.git
export EODHD_API_TOKEN="your_token_here"
```

```text
Use the eodhd-api plugin. Fetch daily OHLCV for AAPL.US from 2024-01-01 to 2024-12-31
and show the first and last 5 rows. API key: demo.
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
