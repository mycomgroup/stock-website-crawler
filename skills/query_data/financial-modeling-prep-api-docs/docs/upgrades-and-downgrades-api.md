---
id: "url-20d0154d"
type: "api"
title: "Upgrades & Downgrades API"
url: "https://site.financialmodelingprep.com/developer/docs/upgrades-and-downgrades-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T11:03:43.749Z"
metadata:
  markdownContent: "# Upgrades & Downgrades API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"publishedDate\": \"2023-09-12T10:48:00.000Z\",\n\t\t\"newsURL\": \"https://www.benzinga.com/analyst-ratings/analyst-color/23/09/34490640/apple-wonderlust-iphone-15-event-will-reveal-shift-to-premium-products-analyst\",\n\t\t\"newsTitle\": \"Apple 'Wonderlust' iPhone 15 Event Will Reveal Shift To Premium Products: Analyst\",\n\t\t\"newsBaseURL\": \"benzinga.com\",\n\t\t\"newsPublisher\": \"Benzinga\",\n\t\t\"newGrade\": \"Neutral\",\n\t\t\"previousGrade\": \"Neutral\",\n\t\t\"gradingCompany\": \"Rosenblatt Securities\",\n\t\t\"action\": \"hold\",\n\t\t\"priceWhenPosted\": 176.6009\n\t}\n]\n```\n\n\n## About Upgrades & Downgrades API\n\nThe FMP Upgrades & Downgrades endpoint provides access to a list of all stock upgrades and downgrades from different analysts. This endpoint is updated on a daily basis, so you can always get the most up-to-date information on analyst ratings.\nTo use the Upgrades & Downgrades endpoint, simply provide the date range that you want to see data for. The endpoint will return a list of all stock upgrades and downgrades that occurred during the specified date range.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v4/upgrades-downgrades?symbol=AAPL\n```\n\n\n## Related Upgrades & Downgrades APIs\n\n\n## Upgrades & Downgrades API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "upgrades-and-downgrades-api"
---

# Upgrades & Downgrades API

## 源URL

https://site.financialmodelingprep.com/developer/docs/upgrades-and-downgrades-api

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"publishedDate": "2023-09-12T10:48:00.000Z",
		"newsURL": "https://www.benzinga.com/analyst-ratings/analyst-color/23/09/34490640/apple-wonderlust-iphone-15-event-will-reveal-shift-to-premium-products-analyst",
		"newsTitle": "Apple 'Wonderlust' iPhone 15 Event Will Reveal Shift To Premium Products: Analyst",
		"newsBaseURL": "benzinga.com",
		"newsPublisher": "Benzinga",
		"newGrade": "Neutral",
		"previousGrade": "Neutral",
		"gradingCompany": "Rosenblatt Securities",
		"action": "hold",
		"priceWhenPosted": 176.6009
	}
]
```

## About Upgrades & Downgrades API

The FMP Upgrades & Downgrades endpoint provides access to a list of all stock upgrades and downgrades from different analysts. This endpoint is updated on a daily basis, so you can always get the most up-to-date information on analyst ratings.
To use the Upgrades & Downgrades endpoint, simply provide the date range that you want to see data for. The endpoint will return a list of all stock upgrades and downgrades that occurred during the specified date range.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v4/upgrades-downgrades?symbol=AAPL
```

## Related Upgrades & Downgrades APIs

## Upgrades & Downgrades API FAQs

## Unlock Premium Financial Insights Today!
