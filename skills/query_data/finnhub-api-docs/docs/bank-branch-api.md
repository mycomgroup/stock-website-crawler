---
id: "url-22f00fd5"
type: "api"
title: "Bank Branch List Premium"
url: "https://finnhub.io/docs/api/bank-branch-api"
description: "Retrieve list of US bank branches information for a given symbol. Method: GET Premium: Accessible with Fundamental or All in One subscription."
source: ""
tags: []
crawl_time: "2026-03-18T07:30:42.051Z"
metadata:
  requestMethod: "GET"
  endpoint: "/bank-branch?symbol=JPM"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Bank Branch List Premium\n\nRetrieve list of US bank branches information for a given symbol.\n\nMethod: GET\n\nPremium: Accessible with Fundamental or All in One subscription.\n\nExamples:\n\n/bank-branch?symbol=JPM\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\nResponse Attributes:\n\ndata\n\nArray of branches.\n\naddress\n\nBranch address\n\nbranchId\n\nBranch ID\n\ndate\n\nDate opened\n\nstate\n\nState\n\nzipCode\n\nZip code\n\nsymbol\n\nSymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.bank_branch(\"JPM\"))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"branchId\": \"201601\",\n      \"address\": \"1910 E 95th St\",\n      \"state\": \"IL\",\n      \"zipCode\": \"60617\",\n      \"date\": \"2000-02-28\"\n    },\n    {\n      \"branchId\": \"359157\",\n      \"address\": \"401 W 49th St\",\n      \"state\": \"FL\",\n      \"zipCode\": \"33012\",\n      \"date\": \"2000-02-01\"\n    }\n  ],\n  \"symbol\": \"JPM\"\n}"
  suggestedFilename: "bank-branch-api"
---

# Bank Branch List Premium

## 源URL

https://finnhub.io/docs/api/bank-branch-api

## 描述

Retrieve list of US bank branches information for a given symbol. Method: GET Premium: Accessible with Fundamental or All in One subscription.

## API 端点

**Method**: `GET`
**Endpoint**: `/bank-branch?symbol=JPM`

## 文档正文

Retrieve list of US bank branches information for a given symbol. Method: GET Premium: Accessible with Fundamental or All in One subscription.

## API 端点

**Method:** `GET`
**Endpoint:** `/bank-branch?symbol=JPM`

Bank Branch List Premium

Retrieve list of US bank branches information for a given symbol.

Method: GET

Premium: Accessible with Fundamental or All in One subscription.

Examples:

/bank-branch?symbol=JPM

Arguments:

symbolREQUIRED

Symbol.

Response Attributes:

data

Array of branches.

address

Branch address

branchId

Branch ID

date

Date opened

state

State

zipCode

Zip code

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

print(finnhub_client.bank_branch("JPM"))

Sample response

{
  "data": [
    {
      "branchId": "201601",
      "address": "1910 E 95th St",
      "state": "IL",
      "zipCode": "60617",
      "date": "2000-02-28"
    },
    {
      "branchId": "359157",
      "address": "401 W 49th St",
      "state": "FL",
      "zipCode": "33012",
      "date": "2000-02-01"
    }
  ],
  "symbol": "JPM"
}
