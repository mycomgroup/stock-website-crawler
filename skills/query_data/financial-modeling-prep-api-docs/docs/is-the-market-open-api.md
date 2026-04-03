---
id: "url-353435d3"
type: "api"
title: "Holidays and Trading Hours API"
url: "https://site.financialmodelingprep.com/developer/docs/is-the-market-open-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T08:00:18.517Z"
metadata:
  markdownContent: "# Holidays and Trading Hours API\n\n**Response Example:**\n\n```json\n{\n\t\"stockExchangeName\": \"Euronext\",\n\t\"stockMarketHours\": {\n\t\t\"openingHour\": \"09:00 a.m. CET\",\n\t\t\"closingHour\": \"05:30 p.m. CET\"\n\t},\n\t\"stockMarketHolidays\": [\n\t\t{\n\t\t\t\"year\": 2019,\n\t\t\t\"Assumption Day\": \"2019-08-15\",\n\t\t\t\"Easter Monday\": \"2019-04-22\",\n\t\t\t\"Labour Day\": \"2019-05-01\",\n\t\t\t\"New Year's Eve\": \"2019-12-31\",\n\t\t\t\"Christmas Day\": \"2019-12-25\",\n\t\t\t\"Boxing Day\": \"2019-12-26\",\n\t\t\t\"Good Friday\": \"2019-04-19\",\n\t\t\t\"Christmas Eve\": \"2019-12-24\"\n\t\t}\n\t],\n\t\"isTheStockMarketOpen\": true,\n\t\"isTheEuronextMarketOpen\": true,\n\t\"isTheForexMarketOpen\": true,\n\t\"isTheCryptoMarketOpen\": true\n}\n```\n\n\n## About Holidays and Trading Hours API\n\nThe FMP Market Open endpoint provides information on whether the US market and EURONEXT are open or closed. Investors can use this information to make informed investment decisions and to avoid trading during market closures.\n  For example, if an investor is planning to sell a stock, they should check the FMP Market Open endpoint to make sure that the market is open before they place their order. Otherwise, their order may not be executed until the next trading day.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v3/is-the-market-open?exchange=EURONEXT\n```\n\n\n## Related Holidays and Trading Hours APIs\n\n\n## Holidays and Trading Hours API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "is-the-market-open-api"
---

# Holidays and Trading Hours API

## 源URL

https://site.financialmodelingprep.com/developer/docs/is-the-market-open-api

## 文档正文

**Response Example:**

```json
{
	"stockExchangeName": "Euronext",
	"stockMarketHours": {
		"openingHour": "09:00 a.m. CET",
		"closingHour": "05:30 p.m. CET"
	},
	"stockMarketHolidays": [
		{
			"year": 2019,
			"Assumption Day": "2019-08-15",
			"Easter Monday": "2019-04-22",
			"Labour Day": "2019-05-01",
			"New Year's Eve": "2019-12-31",
			"Christmas Day": "2019-12-25",
			"Boxing Day": "2019-12-26",
			"Good Friday": "2019-04-19",
			"Christmas Eve": "2019-12-24"
		}
	],
	"isTheStockMarketOpen": true,
	"isTheEuronextMarketOpen": true,
	"isTheForexMarketOpen": true,
	"isTheCryptoMarketOpen": true
}
```

## About Holidays and Trading Hours API

The FMP Market Open endpoint provides information on whether the US market and EURONEXT are open or closed. Investors can use this information to make informed investment decisions and to avoid trading during market closures.
  For example, if an investor is planning to sell a stock, they should check the FMP Market Open endpoint to make sure that the market is open before they place their order. Otherwise, their order may not be executed until the next trading day.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v3/is-the-market-open?exchange=EURONEXT
```

## Related Holidays and Trading Hours APIs

## Holidays and Trading Hours API FAQs

## Unlock Premium Financial Insights Today!
