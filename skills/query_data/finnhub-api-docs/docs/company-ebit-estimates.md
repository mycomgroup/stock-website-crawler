---
id: "url-79121cc1"
type: "api"
title: "EBIT Estimates Premium"
url: "https://finnhub.io/docs/api/company-ebit-estimates"
description: "Get company's ebit estimates. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T09:53:09.317Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/ebit-estimate?symbol=AAPL"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "EBIT Estimates Premium\n\nGet company's ebit estimates.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/ebit-estimate?symbol=AAPL\n\n/stock/ebit-estimate?symbol=TSLA&freq=annual\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nfreqoptional\n\nCan take 1 of the following values: annual, quarterly. Default to quarterly\n\nResponse Attributes:\n\ndata\n\nList of estimates\n\nebitAvg\n\nAverage EBIT estimates including Finnhub's proprietary estimates.\n\nebitHigh\n\nHighest estimate.\n\nebitLow\n\nLowest estimate.\n\nnumberAnalysts\n\nNumber of Analysts.\n\nperiod\n\nPeriod.\n\nquarter\n\nFiscal quarter.\n\nyear\n\nFiscal year.\n\nfreq\n\nFrequency: annual or quarterly.\n\nsymbol\n\nCompany symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_ebit_estimates('TSLA', freq='quarterly'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"numberAnalysts\": 31,\n      \"period\": \"2020-06-30\",\n      \"ebitAvg\": 58800500000,\n      \"ebitHigh\": 64060000000,\n      \"ebitLow\": 54072000000\n      \"quarter\": 3,\n      \"year\": 2020,\n    },\n    {\n      \"numberAnalysts\": 31,\n      \"period\": \"2020-03-31\",\n      \"ebitAvg\": 61287300000,\n      \"ebitHigh\": 66557000000,\n      \"ebitLow\": 54871000000,\n      \"quarter\": 2,\n      \"year\": 2020,\n    }\n  ],\n  \"freq\": \"quarterly\",\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "company-ebit-estimates"
---

# EBIT Estimates Premium

## 源URL

https://finnhub.io/docs/api/company-ebit-estimates

## 描述

Get company's ebit estimates. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/ebit-estimate?symbol=AAPL`

## 文档正文

Get company's ebit estimates. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/ebit-estimate?symbol=AAPL`

EBIT Estimates Premium

Get company's ebit estimates.

Method: GET

Premium: Premium Access Required

Examples:

/stock/ebit-estimate?symbol=AAPL

/stock/ebit-estimate?symbol=TSLA&freq=annual

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

freqoptional

Can take 1 of the following values: annual, quarterly. Default to quarterly

Response Attributes:

data

List of estimates

ebitAvg

Average EBIT estimates including Finnhub's proprietary estimates.

ebitHigh

Highest estimate.

ebitLow

Lowest estimate.

numberAnalysts

Number of Analysts.

period

Period.

quarter

Fiscal quarter.

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

print(finnhub_client.company_ebit_estimates('TSLA', freq='quarterly'))

Sample response

{
  "data": [
    {
      "numberAnalysts": 31,
      "period": "2020-06-30",
      "ebitAvg": 58800500000,
      "ebitHigh": 64060000000,
      "ebitLow": 54072000000
      "quarter": 3,
      "year": 2020,
    },
    {
      "numberAnalysts": 31,
      "period": "2020-03-31",
      "ebitAvg": 61287300000,
      "ebitHigh": 66557000000,
      "ebitLow": 54871000000,
      "quarter": 2,
      "year": 2020,
    }
  ],
  "freq": "quarterly",
  "symbol": "AAPL"
}
