---
id: "url-149f2f44"
type: "website"
title: "Best Practices for Crawl"
url: "https://docs.tavily.com/documentation/best-practices/best-practices-crawl"
description: ""
source: ""
tags: []
crawl_time: "2026-03-25T00:00:00.000Z"
metadata:
  subtype: "article"
  headings: []
---

# Best Practices for Crawl - Tavily Docs

## 源URL

https://docs.tavily.com/documentation/best-practices/best-practices-crawl


## 表格 1

| Feature | Crawl | Map |
| --- | --- | --- |
| Content extraction | Full content | URLs only |
| Use case | Deep content analysis | Site structure discovery |
| Speed | Slower (extracts content) | Faster (URLs only) |
| Best for | RAG, analysis, documentation | Sitemap generation |

## 表格 2

| Parameter | Description | Impact |
| --- | --- | --- |
| max_depth | How many levels deep to crawl from starting URL | Exponential latency growth |
| max_breadth | Maximum links to follow per page | Horizontal spread |
| limit | Total maximum pages to crawl | Hard cap on pages |

## 表格 3

| Depth | When to use |
| --- | --- |
| basic (default) | Simple content, faster processing |
| advanced | Complex pages, tables, structured data |
