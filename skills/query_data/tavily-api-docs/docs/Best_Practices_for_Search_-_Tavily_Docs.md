---
id: "url-326805bf"
type: "website"
title: "Best Practices for Search"
url: "https://docs.tavily.com/documentation/best-practices/best-practices-search"
description: ""
source: ""
tags: []
crawl_time: "2026-03-25T00:00:00.000Z"
metadata:
  subtype: "article"
  headings: []
---

# Best Practices for Search - Tavily Docs

## 源URL

https://docs.tavily.com/documentation/best-practices/best-practices-search


## 表格 1

| Depth | Latency | Relevance | Content Type |
| --- | --- | --- | --- |
| ultra-fast | Lowest | Lower | Content |
| fast | Low | Good | Chunks |
| basic | Medium | High | Content |
| advanced | Higher | Highest | Chunks |

## 表格 2

| Type | Description |
| --- | --- |
| Content | NLP-based summary of the page, providing general context |
| Chunks | Short snippets reranked by relevance to your search query |

## 表格 3

| Depth | When to use |
| --- | --- |
| ultra-fast | When latency is absolutely crucial. Delivers near-instant results, prioritizing speed over relevance. Ideal for real-time applications where response time is critical. |
| fast | When latency is more important than relevance, but you want results in reranked chunks format. Good for applications that need quick, targeted snippets. |
| basic | A solid balance between relevance and latency. Best for general-purpose searches where you need quality results without the overhead of advanced processing. |
| advanced | When you need the highest relevance and are willing to trade off latency. Best for queries seeking specific, detailed information. |

## 表格 4

| Parameter | Description |
| --- | --- |
| time_range | Filter by relative time: day, week, month, year |
| start_date / end_date | Filter by specific date range (format: YYYY-MM-DD) |

## 表格 5

| Parameter | Description |
| --- | --- |
| include_domains | Limit to specific domains |
| exclude_domains | Filter out specific domains |
| country | Boost results from a specific country |

## 表格 6

| Field | Use case |
| --- | --- |
| score | Filter/rank by relevance score |
| title | Keyword filtering on headlines |
| content | Quick relevance check |
| raw_content | Deep analysis and regex extraction |
