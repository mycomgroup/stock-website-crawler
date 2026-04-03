---
id: "url-2fdb3f92"
type: "api"
title: "Fund Ownership Premium"
url: "https://finnhub.io/docs/api/fund-ownership"
description: "Get a full list fund and institutional investors of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T06:58:07.840Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/fund-ownership?symbol=TSLA&limit=20"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Fund Ownership Premium\n\nGet a full list fund and institutional investors of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/fund-ownership?symbol=TSLA&limit=20\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nlimitoptional\n\nLimit number of results. Leave empty to get the full list.\n\nResponse Attributes:\n\nownership\n\nArray of investors with detailed information about their holdings.\n\nchange\n\nNumber of share changed (net buy or sell) from the last period.\n\nfilingDate\n\nFiling date.\n\nname\n\nInvestor's name.\n\nportfolioPercent\n\nPercent of the fund's portfolio comprised of the company's share.\n\nshare\n\nNumber of shares held by the investor.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.fund_ownership('AAPL', limit=5))\n\nSample response\n\n{\n  \"ownership\": [\n    {\n      \"name\": \"AGTHX | American Funds Growth Fund of America\",\n      \"share\": 5145353,\n      \"change\": 57427,\n      \"filingDate\": \"2020-03-31\",\n      \"portfolioPercent\": 1.88\n    },\n    {\n      \"name\": \"Vanguard Total Stock Market Index Fund\",\n      \"share\": 4227464,\n      \"change\": 73406,\n      \"filingDate\": \"2020-03-31\",\n      \"portfolioPercent\": 0.45\n    },\n    {\n      \"name\": \"ANWPX | American Funds New Perspective\",\n      \"share\": 3377612,\n      \"change\": 0,\n      \"filingDate\": \"2020-03-31\",\n      \"portfolioPercent\": 2.64\n    }\n  ],\n  \"symbol\": \"TSLA\"\n}"
  suggestedFilename: "fund-ownership"
---

# Fund Ownership Premium

## 源URL

https://finnhub.io/docs/api/fund-ownership

## 描述

Get a full list fund and institutional investors of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/fund-ownership?symbol=TSLA&limit=20`

## 文档正文

Get a full list fund and institutional investors of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/fund-ownership?symbol=TSLA&limit=20`

Fund Ownership Premium

Get a full list fund and institutional investors of a company in descending order of the number of shares held. Data is sourced from 13F form, Schedule 13D and 13G for US market, UK Share Register for UK market, SEDI for Canadian market and equivalent filings for other international markets.

Method: GET

Premium: Premium Access Required

Examples:

/stock/fund-ownership?symbol=TSLA&limit=20

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

limitoptional

Limit number of results. Leave empty to get the full list.

Response Attributes:

ownership

Array of investors with detailed information about their holdings.

change

Number of share changed (net buy or sell) from the last period.

filingDate

Filing date.

name

Investor's name.

portfolioPercent

Percent of the fund's portfolio comprised of the company's share.

share

Number of shares held by the investor.

symbol

Symbol of the company.

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

print(finnhub_client.fund_ownership('AAPL', limit=5))

Sample response

{
  "ownership": [
    {
      "name": "AGTHX | American Funds Growth Fund of America",
      "share": 5145353,
      "change": 57427,
      "filingDate": "2020-03-31",
      "portfolioPercent": 1.88
    },
    {
      "name": "Vanguard Total Stock Market Index Fund",
      "share": 4227464,
      "change": 73406,
      "filingDate": "2020-03-31",
      "portfolioPercent": 0.45
    },
    {
      "name": "ANWPX | American Funds New Perspective",
      "share": 3377612,
      "change": 0,
      "filingDate": "2020-03-31",
      "portfolioPercent": 2.64
    }
  ],
  "symbol": "TSLA"
}
