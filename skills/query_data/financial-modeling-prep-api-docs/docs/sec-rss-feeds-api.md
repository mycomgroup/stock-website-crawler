---
id: "url-466dfca1"
type: "api"
title: "RSS Feed API"
url: "https://site.financialmodelingprep.com/developer/docs/sec-rss-feeds-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T06:53:52.057Z"
metadata:
  markdownContent: "# RSS Feed API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"title\": \"6-K - Sangoma Technologies Corp (0001753368) (Filer)\",\n\t\t\"date\": \"2023-09-27 17:07:28\",\n\t\t\"link\": \"https://www.sec.gov/Archives/edgar/data/1753368/000175336823000021/0001753368-23-000021-index.htm\",\n\t\t\"cik\": \"0001753368\",\n\t\t\"form_type\": \"6-K\",\n\t\t\"ticker\": \"SANG\",\n\t\t\"done\": true\n\t}\n]\n```\n\n\n## About RSS Feed API\n\nThe FMP SEC Filings RSS Feed endpoint provides a real-time feed of SEC filings from publicly traded companies, including the filing type, link to SEC page, and direct link to the filing. This endpoint can be used to stay up-to-date on the latest SEC filings for all companies or for a specific set of companies.\nThe FMP SEC Filings RSS Feed endpoint is updated in real time, so you can always be sure that you are getting the latest information. The feed is also very easy to use. Simply subscribe to the feed using an RSS reader and you will be automatically notified whenever a new SEC filing is published.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v4/rss_feed?limit=100&type=10&from=2021-03-10&to=2021-05-04&isDone=true\n```\n\n\n## Related RSS Feed APIs\n\n\n## RSS Feed API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "sec-rss-feeds-api"
---

# RSS Feed API

## 源URL

https://site.financialmodelingprep.com/developer/docs/sec-rss-feeds-api

## 文档正文

**Response Example:**

```json
[
	{
		"title": "6-K - Sangoma Technologies Corp (0001753368) (Filer)",
		"date": "2023-09-27 17:07:28",
		"link": "https://www.sec.gov/Archives/edgar/data/1753368/000175336823000021/0001753368-23-000021-index.htm",
		"cik": "0001753368",
		"form_type": "6-K",
		"ticker": "SANG",
		"done": true
	}
]
```

## About RSS Feed API

The FMP SEC Filings RSS Feed endpoint provides a real-time feed of SEC filings from publicly traded companies, including the filing type, link to SEC page, and direct link to the filing. This endpoint can be used to stay up-to-date on the latest SEC filings for all companies or for a specific set of companies.
The FMP SEC Filings RSS Feed endpoint is updated in real time, so you can always be sure that you are getting the latest information. The feed is also very easy to use. Simply subscribe to the feed using an RSS reader and you will be automatically notified whenever a new SEC filing is published.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v4/rss_feed?limit=100&type=10&from=2021-03-10&to=2021-05-04&isDone=true
```

## Related RSS Feed APIs

## RSS Feed API FAQs

## Unlock Premium Financial Insights Today!
