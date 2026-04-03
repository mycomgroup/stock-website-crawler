---
id: "url-15e643dd"
type: "api"
title: "Filings Extract With Analytics By Holder API"
url: "https://site.financialmodelingprep.com/developer/docs/stock-ownership-by-holders-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T13:21:06.988Z"
metadata:
  markdownContent: "# Filings Extract With Analytics By Holder API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"date\": \"2023-09-30\",\n\t\t\"cik\": \"0000102909\",\n\t\t\"filingDate\": \"2023-12-18\",\n\t\t\"investorName\": \"VANGUARD GROUP INC\",\n\t\t\"symbol\": \"AAPL\",\n\t\t\"securityName\": \"APPLE INC\",\n\t\t\"typeOfSecurity\": \"COM\",\n\t\t\"securityCusip\": \"037833100\",\n\t\t\"sharesType\": \"SH\",\n\t\t\"putCallShare\": \"Share\",\n\t\t\"investmentDiscretion\": \"SOLE\",\n\t\t\"industryTitle\": \"ELECTRONIC COMPUTERS\",\n\t\t\"weight\": 5.4673,\n\t\t\"lastWeight\": 5.996,\n\t\t\"changeInWeight\": -0.5287,\n\t\t\"changeInWeightPercentage\": -8.8175,\n\t\t\"marketValue\": 222572509140,\n\t\t\"lastMarketValue\": 252876459509,\n\t\t\"changeInMarketValue\": -30303950369,\n\t\t\"changeInMarketValuePercentage\": -11.9837,\n\t\t\"sharesNumber\": 1299997133,\n\t\t\"lastSharesNumber\": 1303688506,\n\t\t\"changeInSharesNumber\": -3691373,\n\t\t\"changeInSharesNumberPercentage\": -0.2831,\n\t\t\"quarterEndPrice\": 171.21,\n\t\t\"avgPricePaid\": 95.86,\n\t\t\"isNew\": false,\n\t\t\"isSoldOut\": false,\n\t\t\"ownership\": 8.3336,\n\t\t\"lastOwnership\": 8.305,\n\t\t\"changeInOwnership\": 0.0286,\n\t\t\"changeInOwnershipPercentage\": 0.3445,\n\t\t\"holdingPeriod\": 42,\n\t\t\"firstAdded\": \"2013-06-30\",\n\t\t\"performance\": -29671950396,\n\t\t\"performancePercentage\": -11.7338,\n\t\t\"lastPerformance\": 38078179274,\n\t\t\"changeInPerformance\": -67750129670,\n\t\t\"isCountedForPerformance\": true\n\t}\n]\n```\n\n\n## About Filings Extract With Analytics By Holder API\n\nThe Filings Extract With Analytics By Holder API allows users to extract detailed analytics from filings by institutional investors. It offers information such as shares held, changes in stock weight and market value, ownership percentages, and other important metrics that provide an analytical view of institutional investment strategies.\n\nInstitutional Investor Analysis: Track the behavior of large institutional holders such as Vanguard, including their changes in stock positions and market value.\nPortfolio Movement Monitoring: Analyze stock movements and holding period data to see how long institutions have held a stock and when they increased or reduced their positions.\nInvestment Strategy Insights: Understand investment strategies by looking at changes in weight, market value, and ownership over time.\n\nThis API offers granular insights into how institutions manage their portfolios, providing data to investors and analysts for deeper investment analysis.\nExample Use CaseAn investment analyst can use the Filings Extract With Analytics By Holder API to monitor Vanguard Group's activity in Apple Inc. stocks, seeing how much stock Vanguard holds, any changes in weight or market value, and when the stock was first added to their portfolio.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/extract-analytics/holder?symbol=AAPL&year=2023&quarter=3&page=0&limit=10\n```\n\n- Institutional Investor Analysis: Track the behavior of large institutional holders such as Vanguard, including their changes in stock positions and market value.\n- Portfolio Movement Monitoring: Analyze stock movements and holding period data to see how long institutions have held a stock and when they increased or reduced their positions.\n- Investment Strategy Insights: Understand investment strategies by looking at changes in weight, market value, and ownership over time.\n\n\n## Related Filings Extract With Analytics By Holder APIs\n\n\n## Filings Extract With Analytics By Holder API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "stock-ownership-by-holders-api"
---

# Filings Extract With Analytics By Holder API

## 源URL

https://site.financialmodelingprep.com/developer/docs/stock-ownership-by-holders-api

## 文档正文

**Response Example:**

```json
[
	{
		"date": "2023-09-30",
		"cik": "0000102909",
		"filingDate": "2023-12-18",
		"investorName": "VANGUARD GROUP INC",
		"symbol": "AAPL",
		"securityName": "APPLE INC",
		"typeOfSecurity": "COM",
		"securityCusip": "037833100",
		"sharesType": "SH",
		"putCallShare": "Share",
		"investmentDiscretion": "SOLE",
		"industryTitle": "ELECTRONIC COMPUTERS",
		"weight": 5.4673,
		"lastWeight": 5.996,
		"changeInWeight": -0.5287,
		"changeInWeightPercentage": -8.8175,
		"marketValue": 222572509140,
		"lastMarketValue": 252876459509,
		"changeInMarketValue": -30303950369,
		"changeInMarketValuePercentage": -11.9837,
		"sharesNumber": 1299997133,
		"lastSharesNumber": 1303688506,
		"changeInSharesNumber": -3691373,
		"changeInSharesNumberPercentage": -0.2831,
		"quarterEndPrice": 171.21,
		"avgPricePaid": 95.86,
		"isNew": false,
		"isSoldOut": false,
		"ownership": 8.3336,
		"lastOwnership": 8.305,
		"changeInOwnership": 0.0286,
		"changeInOwnershipPercentage": 0.3445,
		"holdingPeriod": 42,
		"firstAdded": "2013-06-30",
		"performance": -29671950396,
		"performancePercentage": -11.7338,
		"lastPerformance": 38078179274,
		"changeInPerformance": -67750129670,
		"isCountedForPerformance": true
	}
]
```

## About Filings Extract With Analytics By Holder API

The Filings Extract With Analytics By Holder API allows users to extract detailed analytics from filings by institutional investors. It offers information such as shares held, changes in stock weight and market value, ownership percentages, and other important metrics that provide an analytical view of institutional investment strategies.

Institutional Investor Analysis: Track the behavior of large institutional holders such as Vanguard, including their changes in stock positions and market value.
Portfolio Movement Monitoring: Analyze stock movements and holding period data to see how long institutions have held a stock and when they increased or reduced their positions.
Investment Strategy Insights: Understand investment strategies by looking at changes in weight, market value, and ownership over time.

This API offers granular insights into how institutions manage their portfolios, providing data to investors and analysts for deeper investment analysis.
Example Use CaseAn investment analyst can use the Filings Extract With Analytics By Holder API to monitor Vanguard Group's activity in Apple Inc. stocks, seeing how much stock Vanguard holds, any changes in weight or market value, and when the stock was first added to their portfolio.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/extract-analytics/holder?symbol=AAPL&year=2023&quarter=3&page=0&limit=10
```

- Institutional Investor Analysis: Track the behavior of large institutional holders such as Vanguard, including their changes in stock positions and market value.
- Portfolio Movement Monitoring: Analyze stock movements and holding period data to see how long institutions have held a stock and when they increased or reduced their positions.
- Investment Strategy Insights: Understand investment strategies by looking at changes in weight, market value, and ownership over time.

## Related Filings Extract With Analytics By Holder APIs

## Filings Extract With Analytics By Holder API FAQs

## Unlock Premium Financial Insights Today!
