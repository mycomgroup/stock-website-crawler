---
id: "url-b1f2103"
type: "api"
title: "Historical Market Cap Premium"
url: "https://finnhub.io/docs/api/company-historical-esg-score-api"
description: "Get historical market cap data for global companies. Method: GET Premium: Accessible with Fundamental 2 or All in One subscription."
source: ""
tags: []
crawl_time: "2026-03-18T11:21:45.451Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Historical Market Cap Premium\n\nGet historical market cap data for global companies.\n\nMethod: GET\n\nPremium: Accessible with Fundamental 2 or All in One subscription.\n\nExamples:\n\n/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06\n\nArguments:\n\nsymbolREQUIRED\n\nCompany symbol.\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ncurrency\n\nCurrency\n\ndata\n\nArray of market data.\n\natDate\n\nDate of the reading\n\nmarketCapitalization\n\nValue\n\nsymbol\n\nSymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.historical_market_cap('AAPL', _from=\"2020-06-01\", to=\"2020-06-10\"))\n\nSample response\n\n{\n  \"currency\": \"USD\",\n  \"data\": [\n    {\n      \"atDate\": \"2024-06-10\",\n      \"marketCapitalization\": 3759.182\n    },\n    {\n      \"atDate\": \"2024-06-09\",\n      \"marketCapitalization\": 21508.447\n    }\n  ],\n  \"symbol\": \"SYM\"\n}"
  suggestedFilename: "company-historical-esg-score-api"
---

# Historical Market Cap Premium

## 源URL

https://finnhub.io/docs/api/company-historical-esg-score-api

## 描述

Get historical market cap data for global companies. Method: GET Premium: Accessible with Fundamental 2 or All in One subscription.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06`

## 文档正文

Get historical market cap data for global companies. Method: GET Premium: Accessible with Fundamental 2 or All in One subscription.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06`

Historical Market Cap Premium

Get historical market cap data for global companies.

Method: GET

Premium: Accessible with Fundamental 2 or All in One subscription.

Examples:

/stock/historical-market-cap?symbol=AAPL&from=2022-01-01&to=2024-05-06

Arguments:

symbolREQUIRED

Company symbol.

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

currency

Currency

data

Array of market data.

atDate

Date of the reading

marketCapitalization

Value

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

print(finnhub_client.historical_market_cap('AAPL', _from="2020-06-01", to="2020-06-10"))

Sample response

{
  "currency": "USD",
  "data": [
    {
      "atDate": "2024-06-10",
      "marketCapitalization": 3759.182
    },
    {
      "atDate": "2024-06-09",
      "marketCapitalization": 21508.447
    }
  ],
  "symbol": "SYM"
}
