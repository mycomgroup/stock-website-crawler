---
id: "url-5740298b"
type: "website"
title: "Tavily CLI"
url: "https://docs.tavily.com/documentation/tavily-cli"
description: ""
source: ""
tags: []
crawl_time: "2026-03-25T00:00:00.000Z"
metadata:
  subtype: "article"
  headings: []
---

# Tavily CLI - Tavily Docs

## 源URL

https://docs.tavily.com/documentation/tavily-cli


## 表格 1

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| --depth | ultra-fast | fast | basic | advanced | basic | Search depth. Higher depth returns more detailed results. |
| --max-results | 0–20 | 5 | Number of results to return. |
| --topic | general | news | finance | general | Optimize search for a specific topic. |
| --time-range | day | week | month | year | — | Filter results to a relative time window. |
| --start-date | YYYY-MM-DD | — | Only include results published after this date. |
| --end-date | YYYY-MM-DD | — | Only include results published before this date. |
| --include-domains | comma-separated | — | Restrict results to these domains. |
| --exclude-domains | comma-separated | — | Exclude results from these domains. |
| --country | country code | — | Boost results from a specific country. |
| --include-answer | basic | advanced | — | Include an AI-generated answer with results. |
| --include-raw-content | markdown | text | — | Include full page content for each result. |
| --include-images | flag | false | Include image results. |
| --include-image-descriptions | flag | false | Include AI-generated image descriptions. |
| --chunks-per-source | integer | — | Number of content chunks per source (requires fast or advanced depth). |
| -o / --output | file path | — | Save output to a file. |
| --json | flag | false | Output raw JSON. |

## 表格 2

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| --query | string | — | Rerank extracted chunks by relevance to this query. |
| --chunks-per-source | 1–5 | — | Number of content chunks per URL (requires --query). |
| --extract-depth | basic | advanced | basic | Extraction depth. advanced handles JavaScript-rendered pages. |
| --format | markdown | text | markdown | Output format for extracted content. |
| --include-images | flag | false | Include image URLs found on the page. |
| --timeout | 1–60 | — | Maximum wait time in seconds. |
| -o / --output | file path | — | Save output to a file. |
| --json | flag | false | Output raw JSON. |

## 表格 3

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| --max-depth | 1–5 | 1 | How many levels deep to crawl from the start URL. |
| --max-breadth | integer | 20 | Maximum links to follow per page. |
| --limit | integer | 50 | Total page cap for the crawl. |
| --instructions | string | — | Natural language guidance for the crawler (e.g., “only follow documentation pages”). |
| --chunks-per-source | 1–5 | — | Chunks per page (requires --instructions). |
| --extract-depth | basic | advanced | basic | Extraction depth for crawled pages. |
| --format | markdown | text | markdown | Output format for extracted content. |
| --select-paths | comma-separated regex | — | Only crawl paths matching these patterns. |
| --exclude-paths | comma-separated regex | — | Skip paths matching these patterns. |
| --select-domains | comma-separated regex | — | Only follow links to matching domains. |
| --exclude-domains | comma-separated regex | — | Skip links to matching domains. |
| --allow-external / --no-external | flag | — | Whether to follow links to external domains. |
| --include-images | flag | false | Include images found on pages. |
| --timeout | 10–150 | — | Maximum wait time in seconds. |
| -o / --output | file path | — | Save full JSON output to a file. |
| --output-dir | directory path | — | Save each crawled page as a separate .md file. |
| --json | flag | false | Output raw JSON. |

## 表格 4

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| --max-depth | 1–5 | 1 | How many levels deep to discover links. |
| --max-breadth | integer | 20 | Maximum links to follow per page. |
| --limit | integer | 50 | Maximum total URLs to discover. |
| --instructions | string | — | Natural language guidance for URL discovery. |
| --select-paths | comma-separated regex | — | Only include URLs matching these path patterns. |
| --exclude-paths | comma-separated regex | — | Exclude URLs matching these path patterns. |
| --select-domains | comma-separated regex | — | Only include URLs from matching domains. |
| --exclude-domains | comma-separated regex | — | Exclude URLs from matching domains. |
| --allow-external / --no-external | flag | — | Whether to include external domain links. |
| --timeout | 10–150 | — | Maximum wait time in seconds. |
| -o / --output | file path | — | Save output to a file. |
| --json | flag | false | Output raw JSON. |

## 表格 5

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| --model | mini | pro | auto | auto | Research model. mini is faster, pro is more thorough, auto picks the best fit. |
| --no-wait | flag | false | Return the request_id immediately without waiting for completion. |
| --stream | flag | false | Stream results in real-time as the research progresses. |
| --output-schema | file path | — | Path to a JSON schema file for structured output. |
| --citation-format | numbered | mla | apa | chicago | — | Citation style for the research report. |
| --poll-interval | seconds | 10 | How often to check for completion. |
| --timeout | seconds | 600 | Maximum time to wait for results. |
| -o / --output | file path | — | Save the report to a file. |
| --json | flag | false | Output raw JSON. |

## 表格 6

| Option | Description |
| --- | --- |
| --version | Print the CLI version and exit. |
| --status | Print the version and authentication status. |
| --json | Output as JSON (applies to --version and --status). |
| --help | Show help for any command. |

## 表格 7

| Variable | Description |
| --- | --- |
| TAVILY_API_KEY | Your Tavily API key. Takes precedence over stored credentials. |

## 表格 8

| Code | Meaning |
| --- | --- |
| 0 | Success. |
| 2 | Invalid input or usage error (e.g., missing required argument). |
| 3 | Authentication error (no API key found, or login failed). |
| 4 | API error (rate limit, invalid request, server error). |
