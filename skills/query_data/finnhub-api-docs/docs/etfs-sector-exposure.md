---
id: "url-46b8d98"
type: "api"
title: "ETFs Sector Exposure Premium"
url: "https://finnhub.io/docs/api/etfs-sector-exposure"
description: "Get ETF sector exposure data. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T09:27:04.627Z"
metadata:
  requestMethod: "GET"
  endpoint: "/etf/sector?symbol=SPY"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "ETFs Sector Exposure Premium\n\nGet ETF sector exposure data.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/etf/sector?symbol=SPY\n\n/etf/sector?symbol=VOO\n\nArguments:\n\nsymboloptional\n\nETF symbol.\n\nisinoptional\n\nETF isin.\n\nResponse Attributes:\n\nsectorExposure\n\nArray of industries and exposure levels.\n\nexposure\n\nPercent of exposure.\n\nindustry\n\nIndustry\n\nsymbol\n\nETF symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.etfs_sector_exp('SPY'))\n\nSample response\n\n{\n  \"sectorExposure\": [\n    {\n      \"exposure\": 31.96,\n      \"industry\": \"Technology\"\n    },\n    {\n      \"exposure\": 14.79,\n      \"industry\": \"Healthcare\"\n    },\n    {\n      \"exposure\": 13.46,\n      \"industry\": \"Consumer Cyclicals\"\n    }\n  ],\n  \"symbol\": \"SPY\"\n}"
  suggestedFilename: "etfs-sector-exposure"
---

# ETFs Sector Exposure Premium

## 源URL

https://finnhub.io/docs/api/etfs-sector-exposure

## 描述

Get ETF sector exposure data. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/etf/sector?symbol=SPY`

## 文档正文

Get ETF sector exposure data. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/etf/sector?symbol=SPY`

ETFs Sector Exposure Premium

Get ETF sector exposure data.

Method: GET

Premium: Premium Access Required

Examples:

/etf/sector?symbol=SPY

/etf/sector?symbol=VOO

Arguments:

symboloptional

ETF symbol.

isinoptional

ETF isin.

Response Attributes:

sectorExposure

Array of industries and exposure levels.

exposure

Percent of exposure.

industry

Industry

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

print(finnhub_client.etfs_sector_exp('SPY'))

Sample response

{
  "sectorExposure": [
    {
      "exposure": 31.96,
      "industry": "Technology"
    },
    {
      "exposure": 14.79,
      "industry": "Healthcare"
    },
    {
      "exposure": 13.46,
      "industry": "Consumer Cyclicals"
    }
  ],
  "symbol": "SPY"
}
