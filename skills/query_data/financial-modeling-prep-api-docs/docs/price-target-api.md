---
id: "url-36b6cbd4"
type: "api"
title: "Price Targets API"
url: "https://site.financialmodelingprep.com/developer/docs/price-target-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:33:05.184Z"
metadata:
  markdownContent: "# Price Targets API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"publishedDate\": \"2023-09-18T02:36:00.000Z\",\n\t\t\"newsURL\": \"https://www.benzinga.com/analyst-ratings/analyst-color/23/09/34673717/apple-analyst-says-iphone-15-pro-pro-max-preorders-strong-out-of-the-gates-increasi\",\n\t\t\"newsTitle\": \"Apple Analyst Says iPhone 15 Pro, Pro Max Preorders Strong Out Of The Gates, Increasing Confidence In Estimates For Holiday Quarter\",\n\t\t\"analystName\": \"Daniel Ives\",\n\t\t\"priceTarget\": 240,\n\t\t\"adjPriceTarget\": 240,\n\t\t\"priceWhenPosted\": 175.01,\n\t\t\"newsPublisher\": \"Benzinga\",\n\t\t\"newsBaseURL\": \"benzinga.com\",\n\t\t\"analystCompany\": \"Wedbush\"\n\t}\n]\n```\n\n\n## About Price Targets API\n\nThe FMP Price Target endpoint provides access to the price target for a company, which is the price at which an analyst believes the company's stock is fairly valued. Price targets are based on a variety of factors, such as the company's financial performance, its industry outlook, and its competitive landscape.\nAnalysts use price targets to make investment decisions, such as whether to buy, sell, or hold a stock. Investors can use price targets to make their own investment decisions. \nFor example, an investor may decide to buy a stock if the price target is above the current market price. Conversely, an investor may decide to sell a stock if the price target is below the current market price.\nTo use the FMP Price Target endpoint, simply provide the company's symbol or name. The endpoint will return the price target for the company, as well as the name of the analyst who issued the price target and the date on which the price target was issued.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v4/price-target?symbol=AAPL\n```\n\n\n## Related Price Targets APIs\n\n\n## Price Targets API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "price-target-api"
---

# Price Targets API

## 源URL

https://site.financialmodelingprep.com/developer/docs/price-target-api

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"publishedDate": "2023-09-18T02:36:00.000Z",
		"newsURL": "https://www.benzinga.com/analyst-ratings/analyst-color/23/09/34673717/apple-analyst-says-iphone-15-pro-pro-max-preorders-strong-out-of-the-gates-increasi",
		"newsTitle": "Apple Analyst Says iPhone 15 Pro, Pro Max Preorders Strong Out Of The Gates, Increasing Confidence In Estimates For Holiday Quarter",
		"analystName": "Daniel Ives",
		"priceTarget": 240,
		"adjPriceTarget": 240,
		"priceWhenPosted": 175.01,
		"newsPublisher": "Benzinga",
		"newsBaseURL": "benzinga.com",
		"analystCompany": "Wedbush"
	}
]
```

## About Price Targets API

The FMP Price Target endpoint provides access to the price target for a company, which is the price at which an analyst believes the company's stock is fairly valued. Price targets are based on a variety of factors, such as the company's financial performance, its industry outlook, and its competitive landscape.
Analysts use price targets to make investment decisions, such as whether to buy, sell, or hold a stock. Investors can use price targets to make their own investment decisions. 
For example, an investor may decide to buy a stock if the price target is above the current market price. Conversely, an investor may decide to sell a stock if the price target is below the current market price.
To use the FMP Price Target endpoint, simply provide the company's symbol or name. The endpoint will return the price target for the company, as well as the name of the analyst who issued the price target and the date on which the price target was issued.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v4/price-target?symbol=AAPL
```

## Related Price Targets APIs

## Price Targets API FAQs

## Unlock Premium Financial Insights Today!
