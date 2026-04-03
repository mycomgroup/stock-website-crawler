---
id: "url-77bf1bfd"
type: "api"
title: "Historical NBBO Premium"
url: "https://finnhub.io/docs/api/stock-nbbo"
description: "Get historical best bid and offer for US stocks, LSE, TSX, Euronext and Deutsche Borse. For US market, this endpoint only serves historical NBBO from the beginning of 2023. To download more historical data, please visit our bulk download page in the Dashboard here. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T04:34:23.673Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/bbo?symbol=AAPL&date=2025-06-25&limit=500&skip=0&format=json"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Historical NBBO Premium\n\nGet historical best bid and offer for US stocks, LSE, TSX, Euronext and Deutsche Borse.\n\nFor US market, this endpoint only serves historical NBBO from the beginning of 2023. To download more historical data, please visit our bulk download page in the Dashboard here.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/bbo?symbol=AAPL&date=2025-06-25&limit=500&skip=0&format=json\n\n/stock/bbo?symbol=AC.TO&date=2025-06-25&limit=500&skip=0&format=json\n\n/stock/bbo?symbol=BARC.L&date=2025-06-25&limit=500&skip=0&format=json\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\ndateREQUIRED\n\nDate: 2020-04-02.\n\nlimitREQUIRED\n\nLimit number of ticks returned. Maximum value: 25000\n\nskipREQUIRED\n\nNumber of ticks to skip. Use this parameter to loop through the entire data.\n\nResponse Attributes:\n\na\n\nList of Ask price data.\n\nav\n\nList of Ask volume data.\n\nax\n\nList of venues/exchanges - Ask price. A list of exchange codes can be found here\n\nb\n\nList of Bid price data.\n\nbv\n\nList of Bid volume data.\n\nbx\n\nList of venues/exchanges - Bid price. A list of exchange codes can be found here\n\nc\n\nList of quote conditions. A comprehensive list of quote conditions code can be found here\n\ncount\n\nNumber of ticks returned. If count < limit, all data for that date has been returned.\n\ns\n\nSymbol.\n\nskip\n\nNumber of ticks skipped.\n\nt\n\nList of timestamp in UNIX ms.\n\ntotal\n\nTotal number of ticks for that date.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_nbbo('AAPL', '2020-03-25', 500, 0))\n\nSample response\n\n{\n  \"a\": [\n    137,\n    133.2,\n    126.08\n  ],\n  \"av\": [\n    1,\n    2,\n  ],\n  \"ax\": [\n    \"P\",\n    \"P\",\n    \"P\"\n  ],\n  \"b\": [\n    116.5,\n    116.5,\n    116.5\n  ],\n  \"bv\": [\n    1,\n    1,\n  ],\n  \"bx\": [\n    \"P\",\n    \"P\",\n    \"P\"\n  ],\n  \"c\": [\n    [\n      \"1\"\n    ],\n    [\n      \"1\"\n    ],\n    [\n      \"1\"\n    ]\n  ],\n  \"count\": 3,\n  \"s\": \"AAPL\",\n  \"skip\": 5,\n  \"t\": [\n    1615280400047,\n    1615280400047,\n  ],\n  \"total\": 2739880\n}"
  suggestedFilename: "stock-nbbo"
---

# Historical NBBO Premium

## 源URL

https://finnhub.io/docs/api/stock-nbbo

## 描述

Get historical best bid and offer for US stocks, LSE, TSX, Euronext and Deutsche Borse. For US market, this endpoint only serves historical NBBO from the beginning of 2023. To download more historical data, please visit our bulk download page in the Dashboard here. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/bbo?symbol=AAPL&date=2025-06-25&limit=500&skip=0&format=json`

## 文档正文

Get historical best bid and offer for US stocks, LSE, TSX, Euronext and Deutsche Borse. For US market, this endpoint only serves historical NBBO from the beginning of 2023. To download more historical data, please visit our bulk download page in the Dashboard here. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/bbo?symbol=AAPL&date=2025-06-25&limit=500&skip=0&format=json`

Historical NBBO Premium

Get historical best bid and offer for US stocks, LSE, TSX, Euronext and Deutsche Borse.

For US market, this endpoint only serves historical NBBO from the beginning of 2023. To download more historical data, please visit our bulk download page in the Dashboard here.

Method: GET

Premium: Premium Access Required

Examples:

/stock/bbo?symbol=AAPL&date=2025-06-25&limit=500&skip=0&format=json

/stock/bbo?symbol=AC.TO&date=2025-06-25&limit=500&skip=0&format=json

/stock/bbo?symbol=BARC.L&date=2025-06-25&limit=500&skip=0&format=json

Arguments:

symbolREQUIRED

Symbol.

dateREQUIRED

Date: 2020-04-02.

limitREQUIRED

Limit number of ticks returned. Maximum value: 25000

skipREQUIRED

Number of ticks to skip. Use this parameter to loop through the entire data.

Response Attributes:

a

List of Ask price data.

av

List of Ask volume data.

ax

List of venues/exchanges - Ask price. A list of exchange codes can be found here

b

List of Bid price data.

bv

List of Bid volume data.

bx

List of venues/exchanges - Bid price. A list of exchange codes can be found here

c

List of quote conditions. A comprehensive list of quote conditions code can be found here

count

Number of ticks returned. If count < limit, all data for that date has been returned.

s

Symbol.

skip

Number of ticks skipped.

t

List of timestamp in UNIX ms.

total

Total number of ticks for that date.

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

print(finnhub_client.stock_nbbo('AAPL', '2020-03-25', 500, 0))

Sample response

{
  "a": [
    137,
    133.2,
    126.08
  ],
  "av": [
    1,
    2,
  ],
  "ax": [
    "P",
    "P",
    "P"
  ],
  "b": [
    116.5,
    116.5,
    116.5
  ],
  "bv": [
    1,
    1,
  ],
  "bx": [
    "P",
    "P",
    "P"
  ],
  "c": [
    [
      "1"
    ],
    [
      "1"
    ],
    [
      "1"
    ]
  ],
  "count": 3,
  "s": "AAPL",
  "skip": 5,
  "t": [
    1615280400047,
    1615280400047,
  ],
  "total": 2739880
}
