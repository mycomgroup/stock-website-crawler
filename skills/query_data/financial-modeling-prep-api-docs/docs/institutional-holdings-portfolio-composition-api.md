---
id: "url-66215ae9"
type: "api"
title: "Portfolio Composition API"
url: "https://site.financialmodelingprep.com/developer/docs/institutional-holdings-portfolio-composition-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T19:47:20.123Z"
metadata:
  markdownContent: "# Portfolio Composition API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"date\": \"2021-09-30\",\n\t\t\"cik\": \"0001067983\",\n\t\t\"filingDate\": \"2021-11-15\",\n\t\t\"investorName\": \"BERKSHIRE HATHAWAY INC\",\n\t\t\"symbol\": \"AAPL\",\n\t\t\"securityName\": \"APPLE INC\",\n\t\t\"typeOfSecurity\": \"COM\",\n\t\t\"securityCusip\": \"037833100\",\n\t\t\"sharesType\": \"SH\",\n\t\t\"putCallShare\": \"Share\",\n\t\t\"investmentDiscretion\": \"DFND\",\n\t\t\"industryTitle\": \"ELECTRONIC COMPUTERS\",\n\t\t\"weight\": 42.7776,\n\t\t\"lastWeight\": 41.465,\n\t\t\"changeInWeight\": 1.3126,\n\t\t\"changeInWeightPercentage\": 3.1656,\n\t\t\"marketValue\": 125529681000,\n\t\t\"lastMarketValue\": 121502087000,\n\t\t\"changeInMarketValue\": 4027594000,\n\t\t\"changeInMarketValuePercentage\": 3.3148,\n\t\t\"sharesNumber\": 887135554,\n\t\t\"lastSharesNumber\": 887135554,\n\t\t\"changeInSharesNumber\": 0,\n\t\t\"changeInSharesNumberPercentage\": 0,\n\t\t\"quarterEndPrice\": 141.2945214521,\n\t\t\"avgPricePaid\": 136.5555426888,\n\t\t\"isNew\": false,\n\t\t\"isSoldOut\": false,\n\t\t\"ownership\": 5.3118,\n\t\t\"lastOwnership\": 5.3348,\n\t\t\"changeInOwnership\": -0.023,\n\t\t\"changeInOwnershipPercentage\": -0.4305,\n\t\t\"holdingPeriod\": 23,\n\t\t\"firstAdded\": \"2016-03-31\",\n\t\t\"performance\": 4204116550.5744,\n\t\t\"performancePercentage\": 3.4704,\n\t\t\"lastPerformance\": 13281918464.8517,\n\t\t\"changeInPerformance\": -9077801914.2773,\n\t\t\"isCountedForPerformance\": true\n\t}\n]\n```\n\n\n## About Portfolio Composition API\n\nThe portfolio composition endpoint provides the composition of portfolios, including the asset allocation, sector allocation, and industry allocation. This information is useful for investors who need to get a detailed overview of the investment portfolio of a particular institutional investor or to compare the investment portfolios of multiple institutional investors.\n  For example, investors may want to use the portfolio composition data to see the asset allocation of a particular institutional investor or to compare the sector and industry allocation of two institutional investors.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v4/institutional-ownership/portfolio-holdings?date=2023-06-30&cik=0001067983&page=0\n```\n\n\n## Related Portfolio Composition APIs\n\n\n## Portfolio Composition API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "institutional-holdings-portfolio-composition-api"
---

# Portfolio Composition API

## 源URL

https://site.financialmodelingprep.com/developer/docs/institutional-holdings-portfolio-composition-api

## 文档正文

**Response Example:**

```json
[
	{
		"date": "2021-09-30",
		"cik": "0001067983",
		"filingDate": "2021-11-15",
		"investorName": "BERKSHIRE HATHAWAY INC",
		"symbol": "AAPL",
		"securityName": "APPLE INC",
		"typeOfSecurity": "COM",
		"securityCusip": "037833100",
		"sharesType": "SH",
		"putCallShare": "Share",
		"investmentDiscretion": "DFND",
		"industryTitle": "ELECTRONIC COMPUTERS",
		"weight": 42.7776,
		"lastWeight": 41.465,
		"changeInWeight": 1.3126,
		"changeInWeightPercentage": 3.1656,
		"marketValue": 125529681000,
		"lastMarketValue": 121502087000,
		"changeInMarketValue": 4027594000,
		"changeInMarketValuePercentage": 3.3148,
		"sharesNumber": 887135554,
		"lastSharesNumber": 887135554,
		"changeInSharesNumber": 0,
		"changeInSharesNumberPercentage": 0,
		"quarterEndPrice": 141.2945214521,
		"avgPricePaid": 136.5555426888,
		"isNew": false,
		"isSoldOut": false,
		"ownership": 5.3118,
		"lastOwnership": 5.3348,
		"changeInOwnership": -0.023,
		"changeInOwnershipPercentage": -0.4305,
		"holdingPeriod": 23,
		"firstAdded": "2016-03-31",
		"performance": 4204116550.5744,
		"performancePercentage": 3.4704,
		"lastPerformance": 13281918464.8517,
		"changeInPerformance": -9077801914.2773,
		"isCountedForPerformance": true
	}
]
```

## About Portfolio Composition API

The portfolio composition endpoint provides the composition of portfolios, including the asset allocation, sector allocation, and industry allocation. This information is useful for investors who need to get a detailed overview of the investment portfolio of a particular institutional investor or to compare the investment portfolios of multiple institutional investors.
  For example, investors may want to use the portfolio composition data to see the asset allocation of a particular institutional investor or to compare the sector and industry allocation of two institutional investors.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v4/institutional-ownership/portfolio-holdings?date=2023-06-30&cik=0001067983&page=0
```

## Related Portfolio Composition APIs

## Portfolio Composition API FAQs

## Unlock Premium Financial Insights Today!
