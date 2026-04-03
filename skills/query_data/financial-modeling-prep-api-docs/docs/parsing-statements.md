---
id: "url-7d10a2eb"
type: "api"
title: "Parsing Statement - Financial Modeling Prep API"
url: "https://site.financialmodelingprep.com/developer/docs/parsing-statements"
description: "We parse statements from SEC so company needs to report it first (not every company reports their statement the same time as their earnings, there can be even few weeks delay between earnings date and report to SEC). For example To check if Apple reported their statement already you should look here: Apple SEC 10-Q/K Filings."
source: ""
tags: []
crawl_time: "2026-03-18T05:03:36.684Z"
metadata:
  markdownContent: "# Parsing Statement - Financial Modeling Prep API\n\nWe parse statements from SEC so company needs to report it first (not every company reports their statement the same time as their earnings, there can be even few weeks delay between earnings date and report to SEC). For example To check if Apple reported their statement already you should look here: Apple SEC 10-Q/K Filings.\n\n\n#### 1. Company Reports Statement\n\nWe parse statements from SEC so company needs to report it first (not every company reports their statement the same time as their earnings, there can be even few weeks delay between earnings date and report to SEC). For example To check if Apple reported their statement already you should look here: Apple SEC 10-Q/K Filings.\n\n\n#### 2. Parsing Statement\n\nWe use our own script to get all informations from statement and calculations in some cases when specific fields are not mentioned. Time period between statement reported to SEC and statement parsed into FMP is around 15 minutes. Here are a few of the formulas we use for the fields in case if statement doesn't include them:\n\noperatingExpenses = SellingAndMarketingExpenses + ResearchAndDevelopmentExpenses + GeneralAndAdministrativeExpenses\n\ncostAndExpenses = operatingExpenses + costOfRevenue\n\ngrossProfit = revenue - costOfRevenue\n\nEPS = netIncome / weightedAverageShsOut\n\nEBITDA = netIncome + depreciationAndAmortization + incomeTaxExpense + interestExpense\n\ntotalDebt = longTermDebt + shortTermDebt\n\nnetDebt = totalDebt - cashAndCashEquivalents\n\nlongTermDebt = totalDebt - shortTermDebt\n\ncashAndShortTermInvestments = cashAndCashEquivalents + shortTermInvestments\n\ntotalLiabilities = totalLiabilitiesAndStockholdersEquity + totalStockholdersEquity\n\ntotalInvestments = shortTermInvestments + longTermInvestments\n\ntotalStockholdersEquity = totalLiabilitiesAndStockholdersEquity - totalLiabilities\n\nfreeCashFlow = netCashProvidedByOperatingActivites + investmentsInPropertyPlantAndEquipment\n\ngoodwillAndIntangibleAssets = goodwill + intangibleAssets\n\nnetChangeInCash = cashAtEndOfPeriod - cashAtBeginningOfPeriod\n\n\n#### 3. Financials update and CSV files\n\nAt the end when statement is added, we are generating new financial growth entry, update our TTM ratios and generate CSV files with new parsed quarter or annual statement.\n\n\n#### Stay Ahead with Fresh Data!\n\nYour session has been inactive. For the latest financial insights, please refresh.\n\nRefresh Now\n"
  rawContent: ""
  suggestedFilename: "parsing-statements"
---

# Parsing Statement - Financial Modeling Prep API

## 源URL

https://site.financialmodelingprep.com/developer/docs/parsing-statements

## 描述

We parse statements from SEC so company needs to report it first (not every company reports their statement the same time as their earnings, there can be even few weeks delay between earnings date and report to SEC). For example To check if Apple reported their statement already you should look here: Apple SEC 10-Q/K Filings.

## 文档正文

We parse statements from SEC so company needs to report it first (not every company reports their statement the same time as their earnings, there can be even few weeks delay between earnings date and report to SEC). For example To check if Apple reported their statement already you should look here: Apple SEC 10-Q/K Filings.

#### 1. Company Reports Statement

We parse statements from SEC so company needs to report it first (not every company reports their statement the same time as their earnings, there can be even few weeks delay between earnings date and report to SEC). For example To check if Apple reported their statement already you should look here: Apple SEC 10-Q/K Filings.

#### 2. Parsing Statement

We use our own script to get all informations from statement and calculations in some cases when specific fields are not mentioned. Time period between statement reported to SEC and statement parsed into FMP is around 15 minutes. Here are a few of the formulas we use for the fields in case if statement doesn't include them:

operatingExpenses = SellingAndMarketingExpenses + ResearchAndDevelopmentExpenses + GeneralAndAdministrativeExpenses

costAndExpenses = operatingExpenses + costOfRevenue

grossProfit = revenue - costOfRevenue

EPS = netIncome / weightedAverageShsOut

EBITDA = netIncome + depreciationAndAmortization + incomeTaxExpense + interestExpense

totalDebt = longTermDebt + shortTermDebt

netDebt = totalDebt - cashAndCashEquivalents

longTermDebt = totalDebt - shortTermDebt

cashAndShortTermInvestments = cashAndCashEquivalents + shortTermInvestments

totalLiabilities = totalLiabilitiesAndStockholdersEquity + totalStockholdersEquity

totalInvestments = shortTermInvestments + longTermInvestments

totalStockholdersEquity = totalLiabilitiesAndStockholdersEquity - totalLiabilities

freeCashFlow = netCashProvidedByOperatingActivites + investmentsInPropertyPlantAndEquipment

goodwillAndIntangibleAssets = goodwill + intangibleAssets

netChangeInCash = cashAtEndOfPeriod - cashAtBeginningOfPeriod

#### 3. Financials update and CSV files

At the end when statement is added, we are generating new financial growth entry, update our TTM ratios and generate CSV files with new parsed quarter or annual statement.

#### Stay Ahead with Fresh Data!

Your session has been inactive. For the latest financial insights, please refresh.

Refresh Now
