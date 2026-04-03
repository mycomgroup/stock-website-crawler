---
id: "url-19300c82"
type: "api"
title: "Holder Performance Summary API"
url: "https://site.financialmodelingprep.com/developer/docs/institutional-holdings-portfolio-positions-summary-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T19:53:10.057Z"
metadata:
  markdownContent: "# Holder Performance Summary API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"date\": \"2024-09-30\",\n\t\t\"cik\": \"0001067983\",\n\t\t\"investorName\": \"BERKSHIRE HATHAWAY INC\",\n\t\t\"portfolioSize\": 40,\n\t\t\"securitiesAdded\": 3,\n\t\t\"securitiesRemoved\": 4,\n\t\t\"marketValue\": 266378900503,\n\t\t\"previousMarketValue\": 279969062343,\n\t\t\"changeInMarketValue\": -13590161840,\n\t\t\"changeInMarketValuePercentage\": -4.8542,\n\t\t\"averageHoldingPeriod\": 18,\n\t\t\"averageHoldingPeriodTop10\": 31,\n\t\t\"averageHoldingPeriodTop20\": 27,\n\t\t\"turnover\": 0.175,\n\t\t\"turnoverAlternateSell\": 13.9726,\n\t\t\"turnoverAlternateBuy\": 1.1974,\n\t\t\"performance\": 17707926874,\n\t\t\"performancePercentage\": 6.325,\n\t\t\"lastPerformance\": 38318168662,\n\t\t\"changeInPerformance\": -20610241788,\n\t\t\"performance1year\": 89877376224,\n\t\t\"performancePercentage1year\": 28.5368,\n\t\t\"performance3year\": 91730847239,\n\t\t\"performancePercentage3year\": 31.2597,\n\t\t\"performance5year\": 157058602844,\n\t\t\"performancePercentage5year\": 73.1617,\n\t\t\"performanceSinceInception\": 182067479115,\n\t\t\"performanceSinceInceptionPercentage\": 198.2138,\n\t\t\"performanceRelativeToSP500Percentage\": 6.325,\n\t\t\"performance1yearRelativeToSP500Percentage\": 28.5368,\n\t\t\"performance3yearRelativeToSP500Percentage\": 36.5632,\n\t\t\"performance5yearRelativeToSP500Percentage\": 36.1296,\n\t\t\"performanceSinceInceptionRelativeToSP500Percentage\": 37.0968\n\t}\n]\n```\n\n\n## About Holder Performance Summary API\n\nThe Holder Performance Summary API allows users to view performance metrics for institutional holders, such as market value changes, portfolio turnover, and relative performance against benchmarks. This API is ideal for:\n\nInstitutional Investor Analysis: Track how well institutional investors are performing based on stock picks, changes in holdings, and market value.\nPortfolio Turnover Analysis: See how frequently an institution buys or sells securities, providing insights into their trading strategy.\nPerformance Benchmarking: Compare an institution's performance against the S&P 500 and other benchmarks over different timeframes (1 year, 3 years, 5 years).\n\nThis API offers a comprehensive view of an institutional holder’s performance over time, helping investors and analysts track key players in the market.\nExample Use CaseAn investment manager can use the Holder Performance Summary API to analyze Berkshire Hathaway's performance over the last five years and compare it to the S&P 500, assessing how well their investment strategy has fared.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/stable/institutional-ownership/holder-performance-summary?cik=0001067983&page=0\n```\n\n- Institutional Investor Analysis: Track how well institutional investors are performing based on stock picks, changes in holdings, and market value.\n- Portfolio Turnover Analysis: See how frequently an institution buys or sells securities, providing insights into their trading strategy.\n- Performance Benchmarking: Compare an institution's performance against the S&P 500 and other benchmarks over different timeframes (1 year, 3 years, 5 years).\n\n\n## Related Holder Performance Summary APIs\n\n\n## Holder Performance Summary API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "institutional-holdings-portfolio-positions-summary-api"
---

# Holder Performance Summary API

## 源URL

https://site.financialmodelingprep.com/developer/docs/institutional-holdings-portfolio-positions-summary-api

## 文档正文

**Response Example:**

```json
[
	{
		"date": "2024-09-30",
		"cik": "0001067983",
		"investorName": "BERKSHIRE HATHAWAY INC",
		"portfolioSize": 40,
		"securitiesAdded": 3,
		"securitiesRemoved": 4,
		"marketValue": 266378900503,
		"previousMarketValue": 279969062343,
		"changeInMarketValue": -13590161840,
		"changeInMarketValuePercentage": -4.8542,
		"averageHoldingPeriod": 18,
		"averageHoldingPeriodTop10": 31,
		"averageHoldingPeriodTop20": 27,
		"turnover": 0.175,
		"turnoverAlternateSell": 13.9726,
		"turnoverAlternateBuy": 1.1974,
		"performance": 17707926874,
		"performancePercentage": 6.325,
		"lastPerformance": 38318168662,
		"changeInPerformance": -20610241788,
		"performance1year": 89877376224,
		"performancePercentage1year": 28.5368,
		"performance3year": 91730847239,
		"performancePercentage3year": 31.2597,
		"performance5year": 157058602844,
		"performancePercentage5year": 73.1617,
		"performanceSinceInception": 182067479115,
		"performanceSinceInceptionPercentage": 198.2138,
		"performanceRelativeToSP500Percentage": 6.325,
		"performance1yearRelativeToSP500Percentage": 28.5368,
		"performance3yearRelativeToSP500Percentage": 36.5632,
		"performance5yearRelativeToSP500Percentage": 36.1296,
		"performanceSinceInceptionRelativeToSP500Percentage": 37.0968
	}
]
```

## About Holder Performance Summary API

The Holder Performance Summary API allows users to view performance metrics for institutional holders, such as market value changes, portfolio turnover, and relative performance against benchmarks. This API is ideal for:

Institutional Investor Analysis: Track how well institutional investors are performing based on stock picks, changes in holdings, and market value.
Portfolio Turnover Analysis: See how frequently an institution buys or sells securities, providing insights into their trading strategy.
Performance Benchmarking: Compare an institution's performance against the S&P 500 and other benchmarks over different timeframes (1 year, 3 years, 5 years).

This API offers a comprehensive view of an institutional holder’s performance over time, helping investors and analysts track key players in the market.
Example Use CaseAn investment manager can use the Holder Performance Summary API to analyze Berkshire Hathaway's performance over the last five years and compare it to the S&P 500, assessing how well their investment strategy has fared.

**Endpoint:**

```text
https://financialmodelingprep.com/stable/institutional-ownership/holder-performance-summary?cik=0001067983&page=0
```

- Institutional Investor Analysis: Track how well institutional investors are performing based on stock picks, changes in holdings, and market value.
- Portfolio Turnover Analysis: See how frequently an institution buys or sells securities, providing insights into their trading strategy.
- Performance Benchmarking: Compare an institution's performance against the S&P 500 and other benchmarks over different timeframes (1 year, 3 years, 5 years).

## Related Holder Performance Summary APIs

## Holder Performance Summary API FAQs

## Unlock Premium Financial Insights Today!
