---
id: "url-457d7766"
type: "api"
title: "Analysis By Dates API"
url: "https://site.financialmodelingprep.com/developer/docs/cot-reports-analysis-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T09:08:40.677Z"
metadata:
  markdownContent: "# Analysis By Dates API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"T6\",\n\t\t\"date\": \"2022-08-23 00:00:00\",\n\t\t\"sector\": \"CURRENCIES\",\n\t\t\"currentLongMarketSituation\": 0.77,\n\t\t\"currentShortMarketSituation\": 0.23,\n\t\t\"marketSituation\": \"Bullish\",\n\t\t\"previousLongMarketSituation\": 0.69,\n\t\t\"previousShortMarketSituation\": 0.22,\n\t\t\"previousMarketSituation\": \"Bullish\",\n\t\t\"netPostion\": 6885,\n\t\t\"previousNetPosition\": 5925,\n\t\t\"changeInNetPosition\": 16.2,\n\t\t\"marketSentiment\": \"Increasing Bullish\",\n\t\t\"reversalTrend\": false,\n\t\t\"name\": \"South African Rand (T6)\",\n\t\t\"exchange\": \"SO AFRICAN RAND - CHICAGO MERCANTILE EXCHANGE\"\n\t}\n]\n```\n\n\n## About Analysis By Dates API\n\nAnalysis By Dates endpoint provides an analysis of the COT report for a given date range. This analysis includes information such as the net long and net short positions of different types of market participants, the change in these positions over time, and the open interest for all symbols.\nInvestors can use the Commitment of Traders: Analysis By Dates endpoint to:\nIdentify trends in market sentiment over a period of time.\nCompare the positions of different types of market participants over time.\nMake informed trading decisions based on historical COT report analysis.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v4/commitment_of_traders_report_analysis?from=2023-08-10&to=2023-10-10\n```\n\n\n## Related Analysis By Dates APIs\n\n\n## Analysis By Dates API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "cot-reports-analysis-api"
---

# Analysis By Dates API

## 源URL

https://site.financialmodelingprep.com/developer/docs/cot-reports-analysis-api

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "T6",
		"date": "2022-08-23 00:00:00",
		"sector": "CURRENCIES",
		"currentLongMarketSituation": 0.77,
		"currentShortMarketSituation": 0.23,
		"marketSituation": "Bullish",
		"previousLongMarketSituation": 0.69,
		"previousShortMarketSituation": 0.22,
		"previousMarketSituation": "Bullish",
		"netPostion": 6885,
		"previousNetPosition": 5925,
		"changeInNetPosition": 16.2,
		"marketSentiment": "Increasing Bullish",
		"reversalTrend": false,
		"name": "South African Rand (T6)",
		"exchange": "SO AFRICAN RAND - CHICAGO MERCANTILE EXCHANGE"
	}
]
```

## About Analysis By Dates API

Analysis By Dates endpoint provides an analysis of the COT report for a given date range. This analysis includes information such as the net long and net short positions of different types of market participants, the change in these positions over time, and the open interest for all symbols.
Investors can use the Commitment of Traders: Analysis By Dates endpoint to:
Identify trends in market sentiment over a period of time.
Compare the positions of different types of market participants over time.
Make informed trading decisions based on historical COT report analysis.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v4/commitment_of_traders_report_analysis?from=2023-08-10&to=2023-10-10
```

## Related Analysis By Dates APIs

## Analysis By Dates API FAQs

## Unlock Premium Financial Insights Today!
