---
id: "url-1136ddd7"
type: "api"
title: "List of dates and Links API"
url: "https://site.financialmodelingprep.com/developer/docs/financial-reports-dates"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T08:48:47.844Z"
metadata:
  markdownContent: "# List of dates and Links API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"AAPL\",\n\t\t\"date\": \"2022\",\n\t\t\"period\": \"FY\",\n\t\t\"linkXlsx\": \"https://fmpcloud.io/api/v4/financial-reports-xlsx?symbol=AAPL&year=2022&period=FY&apikey=YOUR_API_KEY\",\n\t\t\"linkJson\": \"https://fmpcloud.io/api/v4/financial-reports-json?symbol=AAPL&year=2022&period=FY&apikey=YOUR_API_KEY\"\n\t}\n]\n```\n\n\n## About List of dates and Links API\n\nThis endpoint provides a list of all the dates for which financial statements are available for a company.\nThe reported financial values from the company's statements are returned by this endpoint, which can be used to obtain values that are missing from the financial statements endpoint. Because they are based on the tag from the company's statements and the quantity of information they give, the number of fields and their titles vary.\nExamine each indicator's meaning as it relates to the particular company during the study process. Please be aware that two firms may use different methods to count the same statistic in their reports even though they have the same data in theirs.\nThe general information that this endpoint typically returns for each business is listed below:\nDate: The report's publication date.\nSymbol: the emblem of a business.\nThis endpoint can be used to identify the dates for which financial statements are available and to track a company's financial performance over time.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v4/financial-reports-dates?symbol=AAPL\n```\n\n\n## Related List of dates and Links APIs\n\n\n## List of dates and Links API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "financial-reports-dates"
---

# List of dates and Links API

## 源URL

https://site.financialmodelingprep.com/developer/docs/financial-reports-dates

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "AAPL",
		"date": "2022",
		"period": "FY",
		"linkXlsx": "https://fmpcloud.io/api/v4/financial-reports-xlsx?symbol=AAPL&year=2022&period=FY&apikey=YOUR_API_KEY",
		"linkJson": "https://fmpcloud.io/api/v4/financial-reports-json?symbol=AAPL&year=2022&period=FY&apikey=YOUR_API_KEY"
	}
]
```

## About List of dates and Links API

This endpoint provides a list of all the dates for which financial statements are available for a company.
The reported financial values from the company's statements are returned by this endpoint, which can be used to obtain values that are missing from the financial statements endpoint. Because they are based on the tag from the company's statements and the quantity of information they give, the number of fields and their titles vary.
Examine each indicator's meaning as it relates to the particular company during the study process. Please be aware that two firms may use different methods to count the same statistic in their reports even though they have the same data in theirs.
The general information that this endpoint typically returns for each business is listed below:
Date: The report's publication date.
Symbol: the emblem of a business.
This endpoint can be used to identify the dates for which financial statements are available and to track a company's financial performance over time.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v4/financial-reports-dates?symbol=AAPL
```

## Related List of dates and Links APIs

## List of dates and Links API FAQs

## Unlock Premium Financial Insights Today!
