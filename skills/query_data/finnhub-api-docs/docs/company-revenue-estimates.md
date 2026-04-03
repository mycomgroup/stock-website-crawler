---
id: "url-52ab207f"
type: "api"
title: "Revenue Estimates Premium"
url: "https://finnhub.io/docs/api/company-revenue-estimates"
description: "Get company's revenue estimates. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T10:37:20.406Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/revenue-estimate?symbol=AAPL"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Revenue Estimates Premium\n\nGet company's revenue estimates.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/revenue-estimate?symbol=AAPL\n\n/stock/revenue-estimate?symbol=TSLA&freq=annual\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nfreqoptional\n\nCan take 1 of the following values: annual, quarterly. Default to quarterly\n\nResponse Attributes:\n\ndata\n\nList of estimates\n\nnumberAnalysts\n\nNumber of Analysts.\n\nperiod\n\nPeriod.\n\nquarter\n\nFiscal quarter.\n\nrevenueAvg\n\nAverage revenue estimates including Finnhub's proprietary estimates.\n\nrevenueHigh\n\nHighest estimate.\n\nrevenueLow\n\nLowest estimate.\n\nyear\n\nFiscal year.\n\nfreq\n\nFrequency: annual or quarterly.\n\nsymbol\n\nCompany symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_revenue_estimates('TSLA', freq='quarterly'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"numberAnalysts\": 31,\n      \"period\": \"2020-06-30\",\n      \"revenueAvg\": 58800500000,\n      \"revenueHigh\": 64060000000,\n      \"revenueLow\": 54072000000,\n      \"quarter\": 3,\n      \"year\": 2020\n    },\n    {\n      \"numberAnalysts\": 31,\n      \"period\": \"2020-03-31\",\n      \"revenueAvg\": 61287300000,\n      \"revenueHigh\": 66557000000,\n      \"revenueLow\": 54871000000,\n      \"quarter\": 2,\n      \"year\": 2020\n    }\n  ],\n  \"freq\": \"quarterly\",\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "company-revenue-estimates"
---

# Revenue Estimates Premium

## 源URL

https://finnhub.io/docs/api/company-revenue-estimates

## 描述

Get company's revenue estimates. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/revenue-estimate?symbol=AAPL`

## 文档正文

Get company's revenue estimates. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/revenue-estimate?symbol=AAPL`

Revenue Estimates Premium

Get company's revenue estimates.

Method: GET

Premium: Premium Access Required

Examples:

/stock/revenue-estimate?symbol=AAPL

/stock/revenue-estimate?symbol=TSLA&freq=annual

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

freqoptional

Can take 1 of the following values: annual, quarterly. Default to quarterly

Response Attributes:

data

List of estimates

numberAnalysts

Number of Analysts.

period

Period.

quarter

Fiscal quarter.

revenueAvg

Average revenue estimates including Finnhub's proprietary estimates.

revenueHigh

Highest estimate.

revenueLow

Lowest estimate.

year

Fiscal year.

freq

Frequency: annual or quarterly.

symbol

Company symbol.

Sample code
cURL
Python
Javascript
Go
Ruby
Kotlin
PHP

import finnhub
finnhub_client = finnhub.Client(api_key="")

print(finnhub_client.company_revenue_estimates('TSLA', freq='quarterly'))

Sample response

{
  "data": [
    {
      "numberAnalysts": 31,
      "period": "2020-06-30",
      "revenueAvg": 58800500000,
      "revenueHigh": 64060000000,
      "revenueLow": 54072000000,
      "quarter": 3,
      "year": 2020
    },
    {
      "numberAnalysts": 31,
      "period": "2020-03-31",
      "revenueAvg": 61287300000,
      "revenueHigh": 66557000000,
      "revenueLow": 54871000000,
      "quarter": 2,
      "year": 2020
    }
  ],
  "freq": "quarterly",
  "symbol": "AAPL"
}
