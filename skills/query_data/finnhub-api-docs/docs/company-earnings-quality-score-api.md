---
id: "url-356ada18"
type: "api"
title: "Company Earnings Quality Score Premium"
url: "https://finnhub.io/docs/api/company-earnings-quality-score-api"
description: "This endpoint provides Earnings Quality Score for global companies. Earnings quality refers to the extent to which current earnings predict future earnings. \"High-quality\" earnings are expected to persist, while \"low-quality\" earnings do not. A higher score means a higher earnings quality Finnhub uses a proprietary model which takes into consideration 4 criteria: Profitability Growth Cash Generation & Capital Allocation Leverage We then compare the metrics of each company in each category against its peers in the same industry to gauge how quality its earnings is. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T11:21:58.184Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/earnings-quality-score?symbol=AAPL&freq=quarterly"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Company Earnings Quality Score Premium\n\nThis endpoint provides Earnings Quality Score for global companies.\n\nEarnings quality refers to the extent to which current earnings predict future earnings. \"High-quality\" earnings are expected to persist, while \"low-quality\" earnings do not. A higher score means a higher earnings quality\n\nFinnhub uses a proprietary model which takes into consideration 4 criteria:\n\nProfitability\nGrowth\nCash Generation & Capital Allocation\nLeverage\n\n\n\nWe then compare the metrics of each company in each category against its peers in the same industry to gauge how quality its earnings is.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/earnings-quality-score?symbol=AAPL&freq=quarterly\n\n/stock/earnings-quality-score?symbol=WMT&freq=quarterly\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\nfreqREQUIRED\n\nFrequency. Currently support annual and quarterly\n\nResponse Attributes:\n\ndata\n\nArray of earnings quality score.\n\ncashGenerationCapitalAllocation\n\nCash Generation and Capital Allocation\n\ngrowth\n\nGrowth Score\n\nletterScore\n\nLetter Score\n\nleverage\n\nLeverage Score\n\nperiod\n\nPeriod\n\nprofitability\n\nProfitability Score\n\nscore\n\nTotal Score\n\nfreq\n\nFrequency\n\nsymbol\n\nSymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_earnings_quality_score('AAPL', 'quarterly'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"capitalAllocation\": 67.6878,\n      \"growth\": 55.8022,\n      \"letterScore\": \"B+\",\n      \"leverage\": 24.5122,\n      \"period\": \"2021-06-01\",\n      \"profitability\": 82.3843,\n      \"score\": 57.5966\n    },\n    {\n      \"capitalAllocation\": 75.1464,\n      \"growth\": 70.2461,\n      \"letterScore\": \"A-\",\n      \"leverage\": 39.5682,\n      \"period\": \"2021-03-01\",\n      \"profitability\": 88.4613,\n      \"score\": 68.3555\n    },\n    {\n      \"capitalAllocation\": 43.8708,\n      \"growth\": 68.1803,\n      \"letterScore\": \"A-\",\n      \"leverage\": 56.1926,\n      \"period\": \"2020-12-01\",\n      \"profitability\": 92.6311,\n      \"score\": 65.2187\n    },\n  ],\n  \"freq\": \"quarterly\",\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "company-earnings-quality-score-api"
---

# Company Earnings Quality Score Premium

## 源URL

https://finnhub.io/docs/api/company-earnings-quality-score-api

## 描述

This endpoint provides Earnings Quality Score for global companies. Earnings quality refers to the extent to which current earnings predict future earnings. "High-quality" earnings are expected to persist, while "low-quality" earnings do not. A higher score means a higher earnings quality Finnhub uses a proprietary model which takes into consideration 4 criteria: Profitability Growth Cash Generation & Capital Allocation Leverage We then compare the metrics of each company in each category against its peers in the same industry to gauge how quality its earnings is. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/earnings-quality-score?symbol=AAPL&freq=quarterly`

## 文档正文

This endpoint provides Earnings Quality Score for global companies. Earnings quality refers to the extent to which current earnings predict future earnings. "High-quality" earnings are expected to persist, while "low-quality" earnings do not. A higher score means a higher earnings quality Finnhub uses a proprietary model which takes into consideration 4 criteria: Profitability Growth Cash Generation & Capital Allocation Leverage We then compare the metrics of each company in each category against its peers in the same industry to gauge how quality its earnings is. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/earnings-quality-score?symbol=AAPL&freq=quarterly`

Company Earnings Quality Score Premium

This endpoint provides Earnings Quality Score for global companies.

Earnings quality refers to the extent to which current earnings predict future earnings. "High-quality" earnings are expected to persist, while "low-quality" earnings do not. A higher score means a higher earnings quality

Finnhub uses a proprietary model which takes into consideration 4 criteria:

Profitability
Growth
Cash Generation & Capital Allocation
Leverage

We then compare the metrics of each company in each category against its peers in the same industry to gauge how quality its earnings is.

Method: GET

Premium: Premium Access Required

Examples:

/stock/earnings-quality-score?symbol=AAPL&freq=quarterly

/stock/earnings-quality-score?symbol=WMT&freq=quarterly

Arguments:

symbolREQUIRED

Symbol.

freqREQUIRED

Frequency. Currently support annual and quarterly

Response Attributes:

data

Array of earnings quality score.

cashGenerationCapitalAllocation

Cash Generation and Capital Allocation

growth

Growth Score

letterScore

Letter Score

leverage

Leverage Score

period

Period

profitability

Profitability Score

score

Total Score

freq

Frequency

symbol

Symbol

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

print(finnhub_client.company_earnings_quality_score('AAPL', 'quarterly'))

Sample response

{
  "data": [
    {
      "capitalAllocation": 67.6878,
      "growth": 55.8022,
      "letterScore": "B+",
      "leverage": 24.5122,
      "period": "2021-06-01",
      "profitability": 82.3843,
      "score": 57.5966
    },
    {
      "capitalAllocation": 75.1464,
      "growth": 70.2461,
      "letterScore": "A-",
      "leverage": 39.5682,
      "period": "2021-03-01",
      "profitability": 88.4613,
      "score": 68.3555
    },
    {
      "capitalAllocation": 43.8708,
      "growth": 68.1803,
      "letterScore": "A-",
      "leverage": 56.1926,
      "period": "2020-12-01",
      "profitability": 92.6311,
      "score": 65.2187
    },
  ],
  "freq": "quarterly",
  "symbol": "AAPL"
}
