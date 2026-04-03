---
id: "url-5b38d5c4"
type: "api"
title: "ETFs Country Exposure Premium"
url: "https://finnhub.io/docs/api/etfs-country-exposure"
description: "Get ETF country exposure data. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T09:28:18.956Z"
metadata:
  requestMethod: "GET"
  endpoint: "/etf/country?symbol=SPY"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "ETFs Country Exposure Premium\n\nGet ETF country exposure data.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/etf/country?symbol=SPY\n\n/etf/country?symbol=VOO\n\nArguments:\n\nsymboloptional\n\nETF symbol.\n\nisinoptional\n\nETF isin.\n\nResponse Attributes:\n\ncountryExposure\n\nArray of countries and and exposure levels.\n\ncountry\n\nCountry\n\nexposure\n\nPercent of exposure.\n\nsymbol\n\nETF symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.etfs_country_exp('SPY'))\n\nSample response\n\n{\n  \"countryExposure\": [\n    {\n      \"country\": \"United States of America (the)\",\n      \"exposure\": 97.02\n    },\n    {\n      \"country\": \"Ireland\",\n      \"exposure\": 1.65\n    },\n    {\n      \"country\": \"United Kingdom of Great Britain and Northern Ireland (the)\",\n      \"exposure\": 0.88\n    },\n    {\n      \"country\": \"Switzerland\",\n      \"exposure\": 0.41\n    },\n    {\n      \"country\": \"Bermuda\",\n      \"exposure\": 0.03\n    }\n  ],\n  \"symbol\": \"SPY\"\n}"
  suggestedFilename: "etfs-country-exposure"
---

# ETFs Country Exposure Premium

## 源URL

https://finnhub.io/docs/api/etfs-country-exposure

## 描述

Get ETF country exposure data. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/etf/country?symbol=SPY`

## 文档正文

Get ETF country exposure data. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/etf/country?symbol=SPY`

ETFs Country Exposure Premium

Get ETF country exposure data.

Method: GET

Premium: Premium Access Required

Examples:

/etf/country?symbol=SPY

/etf/country?symbol=VOO

Arguments:

symboloptional

ETF symbol.

isinoptional

ETF isin.

Response Attributes:

countryExposure

Array of countries and and exposure levels.

country

Country

exposure

Percent of exposure.

symbol

ETF symbol.

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

print(finnhub_client.etfs_country_exp('SPY'))

Sample response

{
  "countryExposure": [
    {
      "country": "United States of America (the)",
      "exposure": 97.02
    },
    {
      "country": "Ireland",
      "exposure": 1.65
    },
    {
      "country": "United Kingdom of Great Britain and Northern Ireland (the)",
      "exposure": 0.88
    },
    {
      "country": "Switzerland",
      "exposure": 0.41
    },
    {
      "country": "Bermuda",
      "exposure": 0.03
    }
  ],
  "symbol": "SPY"
}
