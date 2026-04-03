---
id: "url-500c6cca"
type: "api"
title: "Institutional Portfolio Premium"
url: "https://finnhub.io/docs/api/institutional-portfolio-13f"
description: "Get the holdings/portfolio data of institutional investors from 13-F filings. Limit to 1 year of data at a time. You can get a list of supported CIK here. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T10:38:02.283Z"
metadata:
  requestMethod: "GET"
  endpoint: "/institutional/portfolio?cik=1000097&from=2022-05-01&to=2022-09-01"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Institutional Portfolio Premium\n\nGet the holdings/portfolio data of institutional investors from 13-F filings. Limit to 1 year of data at a time. You can get a list of supported CIK here.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/institutional/portfolio?cik=1000097&from=2022-05-01&to=2022-09-01\n\nArguments:\n\ncikREQUIRED\n\nFund's CIK.\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ncik\n\nCIK.\n\ndata\n\nArray of positions.\n\nfilingDate\n\nFiling date.\n\nportfolio\n\nArray of positions.\n\nchange\n\nNumber of shares change.\n\ncusip\n\nCUSIP.\n\nname\n\nPosition's name.\n\nnoVoting\n\nNumber of shares with no voting rights.\n\npercentage\n\nPercentage of portfolio.\n\nputCall\n\nput or call for options.\n\nshare\n\nNumber of shares.\n\nsharedVoting\n\nNumber of shares with shared voting rights.\n\nsoleVoting\n\nNumber of shares with sole voting rights.\n\nsymbol\n\nSymbol.\n\nvalue\n\nPosition value.\n\nreportDate\n\nReport date.\n\nname\n\nInvestor's name.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.institutional_portfolio(cik=\"1000097\", _from=\"2022-10-01\", to=\"2022-10-11\"))\n\nSample response\n\n{\n  \"cik\": \"1000097\",\n  \"data\": [\n    {\n      \"filingDate\": \"2022-06-30\",\n      \"portfolio\": [\n        {\n          \"change\": -41600,\n          \"name\": \"ABBOTT LABS\",\n          \"noVoting\": 0,\n          \"percentage\": 0,\n          \"putCall\": \"\",\n          \"share\": 0,\n          \"sharedVoting\": 0,\n          \"soleVoting\": 41600,\n          \"symbol\": \"ABT\",\n          \"value\": 0\n        },\n        {\n          \"change\": -275000,\n          \"name\": \"ADICET BIO INC\",\n          \"noVoting\": 0,\n          \"percentage\": 0,\n          \"putCall\": \"\",\n          \"share\": 0,\n          \"sharedVoting\": 0,\n          \"soleVoting\": 275000,\n          \"symbol\": \"ACET\",\n          \"value\": 0\n        }\n      ],\n      \"reportDate\": \"2022-06-30\"\n    }\n  ],\n  \"name\": \"KINGDON CAPITAL MANAGEMENT, L.L.C.\"\n}"
  suggestedFilename: "institutional-portfolio-13f"
---

# Institutional Portfolio Premium

## 源URL

https://finnhub.io/docs/api/institutional-portfolio-13f

## 描述

Get the holdings/portfolio data of institutional investors from 13-F filings. Limit to 1 year of data at a time. You can get a list of supported CIK here. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/institutional/portfolio?cik=1000097&from=2022-05-01&to=2022-09-01`

## 文档正文

Get the holdings/portfolio data of institutional investors from 13-F filings. Limit to 1 year of data at a time. You can get a list of supported CIK here. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/institutional/portfolio?cik=1000097&from=2022-05-01&to=2022-09-01`

Institutional Portfolio Premium

Get the holdings/portfolio data of institutional investors from 13-F filings. Limit to 1 year of data at a time. You can get a list of supported CIK here.

Method: GET

Premium: Premium Access Required

Examples:

/institutional/portfolio?cik=1000097&from=2022-05-01&to=2022-09-01

Arguments:

cikREQUIRED

Fund's CIK.

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

cik

CIK.

data

Array of positions.

filingDate

Filing date.

portfolio

Array of positions.

change

Number of shares change.

cusip

CUSIP.

name

Position's name.

noVoting

Number of shares with no voting rights.

percentage

Percentage of portfolio.

putCall

put or call for options.

share

Number of shares.

sharedVoting

Number of shares with shared voting rights.

soleVoting

Number of shares with sole voting rights.

symbol

Symbol.

value

Position value.

reportDate

Report date.

name

Investor's name.

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

print(finnhub_client.institutional_portfolio(cik="1000097", _from="2022-10-01", to="2022-10-11"))

Sample response

{
  "cik": "1000097",
  "data": [
    {
      "filingDate": "2022-06-30",
      "portfolio": [
        {
          "change": -41600,
          "name": "ABBOTT LABS",
          "noVoting": 0,
          "percentage": 0,
          "putCall": "",
          "share": 0,
          "sharedVoting": 0,
          "soleVoting": 41600,
          "symbol": "ABT",
          "value": 0
        },
        {
          "change": -275000,
          "name": "ADICET BIO INC",
          "noVoting": 0,
          "percentage": 0,
          "putCall": "",
          "share": 0,
          "sharedVoting": 0,
          "soleVoting": 275000,
          "symbol": "ACET",
          "value": 0
        }
      ],
      "reportDate": "2022-06-30"
    }
  ],
  "name": "KINGDON CAPITAL MANAGEMENT, L.L.C."
}
