---
id: "url-78545a5a"
type: "api"
title: "Global Filings Search Premium"
url: "https://finnhub.io/docs/api/global-filings-search"
description: "Search for best-matched filings across global companies' filings, transcripts and press releases. You can filter by anything from symbol, ISIN to form type, and document sources.This endpoint will return a list of documents that match your search criteria. If you would like to get the excerpts as well, please set highlighted to true. Once you have the list of documents, you can get a list of excerpts and positions to highlight the document using the /search-in-filing endpoint"
source: ""
tags: []
crawl_time: "2026-03-18T09:52:58.306Z"
metadata:
  requestMethod: "POST"
  endpoint: "/global-filings/search"
  parameters:
    - {"name":"search","in":"body","required":false,"type":"","description":"Search body"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"cURL","code":"curl --request POST 'https://finnhub.io/api/v1/global-filings/search?token=<token>' \\\n--data-raw '{\n    \"query\": \"artificial intelligence\",\n    \"symbols\": \"AAPL,GOOGL,TSLA\",\n    \"fromDate\": \"2010-01-01\",\n    \"toDate\": \"2022-09-30\"\n}'"}
    - {"language":"JavaScript","code":"var raw = JSON.stringify({\n  \"query\": \"artificial intelligence\",\n  \"symbols\": \"AAPL,GOOGL,TSLA\",\n  \"fromDate\": \"2010-01-01\",\n  \"toDate\": \"2022-09-30\"\n});\n\nvar requestOptions = {\n  method: 'POST',\n  body: raw,\n};\n\nfetch(\"https://finnhub.io/api/v1/global-filings/search?token=<token>\", requestOptions)\n  .then(response => response.json())"}
    - {"language":"Python","code":"import requests\nimport json\n\nurl = \"https://finnhub.io/api/v1/global-filings/search?token=<token>\"\n\npayload = json.dumps({\n  \"query\": \"artificial intelligence\",\n  \"symbols\": \"AAPL,GOOGL,TSLA\",\n  \"fromDate\": \"2010-01-01\",\n  \"toDate\": \"2022-09-30\"\n})\n\n\nresponse = requests.request(\"POST\", url, data=payload)\n\nprint(response.json())"}
  sampleResponse: "{\n    \"count\": 8,\n    \"filings\": [\n        {\n            \"acceptanceDate\": \"2022-10-27 00:00:00\",\n            \"amend\": false,\n            \"documentCount\": 1,\n            \"filedDate\": \"2022-10-27\",\n            \"filerId\": \"3285503214\",\n            \"filingId\": \"AAPL_1113753\",\n            \"form\": \"TR/E\",\n            \"name\": \"Apple Inc\",\n            \"pageCount\": 4,\n            \"reportPeriod\": \"\",\n            \"source\": \"TR\",\n            \"symbols\": [\n                \"AAPL\"\n            ],\n            \"title\": \"AAPL - Earnings call Q4 2022\",\n            \"url\": \"https://alpharesearch.io/platform/share?filingId=AAPL_1113753\"\n        }\n        ...\n    ],\n    \"page\": 1,\n    \"took\": 1986\n}"
  curlExample: "curl --request POST 'https://finnhub.io/api/v1/global-filings/search?token=<token>' \\\n--data-raw '{\n    \"query\": \"artificial intelligence\",\n    \"symbols\": \"AAPL,GOOGL,TSLA\",\n    \"fromDate\": \"2010-01-01\",\n    \"toDate\": \"2022-09-30\"\n}'"
  jsonExample: "{\n    \"count\": 8,\n    \"filings\": [\n        {\n            \"acceptanceDate\": \"2022-10-27 00:00:00\",\n            \"amend\": false,\n            \"documentCount\": 1,\n            \"filedDate\": \"2022-10-27\",\n            \"filerId\": \"3285503214\",\n            \"filingId\": \"AAPL_1113753\",\n            \"form\": \"TR/E\",\n            \"name\": \"Apple Inc\",\n            \"pageCount\": 4,\n            \"reportPeriod\": \"\",\n            \"source\": \"TR\",\n            \"symbols\": [\n                \"AAPL\"\n            ],\n            \"title\": \"AAPL - Earnings call Q4 2022\",\n            \"url\": \"https://alpharesearch.io/platform/share?filingId=AAPL_1113753\"\n        }\n        ...\n    ],\n    \"page\": 1,\n    \"took\": 1986\n}"
  rawContent: "Global Filings Search Premium\n\nSearch for best-matched filings across global companies' filings, transcripts and press releases. You can filter by anything from symbol, ISIN to form type, and document sources.\n\nThis endpoint will return a list of documents that match your search criteria. If you would like to get the excerpts as well, please set highlighted to true. Once you have the list of documents, you can get a list of excerpts and positions to highlight the document using the /search-in-filing endpoint\n\nMethod: POST\n\nPremium: Premium Access Required\n\nExamples:\n\n/global-filings/search\n\nPayload:\n\nactsoptional\n\nList of SEC's exchanges act to search, comma separated. Look at /filter endpoint to see all available values.\n\ncapsoptional\n\nList of market capitalization to search, comma separated. Look at /filter endpoint to see all available values.\n\nchIdsoptional\n\nList of Companies House number to search, comma separated (Max: 50).\n\nciksoptional\n\nList of SEC Center Index Key to search, comma separated (Max: 50).\n\ncountriesoptional\n\nList of sources to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.\n\ncusipsoptional\n\nList of cusip to search, comma separated (Max: 50).\n\nexchangesoptional\n\nList of exchanges to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.\n\nexhibitsoptional\n\nList of exhibits to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.\n\nformsoptional\n\nList of forms to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.\n\nfromDateoptional\n\nSearch from date in format: YYYY-MM-DD, default from the last 2 years\n\ngicsoptional\n\nList of gics to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.\n\nhighlightedoptional\n\nEnable highlight in returned filings. If enabled, only return 10 results each time\n\nisinsoptional\n\nList of isin to search, comma separated (Max: 50).\n\nnaicsoptional\n\nList of sources to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.\n\npageoptional\n\nUse for pagination, default to page 1\n\nqueryREQUIRED\n\nSearch query\n\nsedarIdsoptional\n\nList of SEDAR issuer number to search, comma separated (Max: 50).\n\nsedolsoptional\n\nList of sedols to search, comma separated (Max: 50).\n\nsortoptional\n\nSort result by, default: sortMostRecent. Look at /filter endpoint to see all available values.\n\nsourcesoptional\n\nList of sources to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.\n\nsymbolsoptional\n\nList of symbols to search, comma separated (Max: 50).\n\ntoDateoptional\n\nSearch to date in format: YYYY-MM-DD, default to today\n\nResponse Attributes:\n\ncount\n\nTotal filing matched your search criteria.\n\nfilings\n\nFiling match your search criteria.\n\nacceptanceDate\n\nDate the filing is submitted.\n\namend\n\nAmendment\n\ndocumentCount\n\nNumber of document in this filing\n\nfiledDate\n\nDate the filing is made available to the public\n\nfilerId\n\nId of the entity submitted the filing\n\nfilingId\n\nFiling Id in Alpharesearch platform\n\nform\n\nFiling Form\n\nname\n\nFiler name\n\npageCount\n\nEstimate number of page when printing\n\nreportDate\n\nDate as which the filing is reported\n\nsource\n\nFiling Source\n\nsymbol\n\nList of symbol associate with this filing\n\ntitle\n\nFiling title\n\npage\n\nCurrent search page\n\ntook\n\nTime took to execute your search query on our server, value in ms.\n\nSample code\ncURL\nPython\nJavascript\n\nimport requests\nimport json\n\nurl = \"https://finnhub.io/api/v1/global-filings/search?token=\"\n\npayload = json.dumps({\n  \"query\": \"artificial intelligence\",\n  \"symbols\": \"AAPL,GOOGL,TSLA\",\n  \"fromDate\": \"2010-01-01\",\n  \"toDate\": \"2022-09-30\"\n})\n\nresponse = requests.request(\"POST\", url, data=payload)\n\nprint(response.json())\n\nSample response\n\n{\n    \"count\": 8,\n    \"filings\": [\n        {\n            \"acceptanceDate\": \"2022-10-27 00:00:00\",\n            \"amend\": false,\n            \"documentCount\": 1,\n            \"filedDate\": \"2022-10-27\",\n            \"filerId\": \"3285503214\",\n            \"filingId\": \"AAPL_1113753\",\n            \"form\": \"TR/E\",\n            \"name\": \"Apple Inc\",\n            \"pageCount\": 4,\n            \"reportPeriod\": \"\",\n            \"source\": \"TR\",\n            \"symbols\": [\n                \"AAPL\"\n            ],\n            \"title\": \"AAPL - Earnings call Q4 2022\",\n            \"url\": \"https://alpharesearch.io/platform/share?filingId=AAPL_1113753\"\n        }\n        ...\n    ],\n    \"page\": 1,\n    \"took\": 1986\n}"
  suggestedFilename: "global-filings-search"
---

# Global Filings Search Premium

## 源URL

https://finnhub.io/docs/api/global-filings-search

## 描述

Search for best-matched filings across global companies' filings, transcripts and press releases. You can filter by anything from symbol, ISIN to form type, and document sources.This endpoint will return a list of documents that match your search criteria. If you would like to get the excerpts as well, please set highlighted to true. Once you have the list of documents, you can get a list of excerpts and positions to highlight the document using the /search-in-filing endpoint

## API 端点

**Method**: `POST`
**Endpoint**: `/global-filings/search`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `search` | - | 否 | - | Search body |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (cURL)

```cURL
curl --request POST 'https://finnhub.io/api/v1/global-filings/search?token=<token>' \
--data-raw '{
    "query": "artificial intelligence",
    "symbols": "AAPL,GOOGL,TSLA",
    "fromDate": "2010-01-01",
    "toDate": "2022-09-30"
}'
```

### 示例 2 (JavaScript)

```JavaScript
var raw = JSON.stringify({
  "query": "artificial intelligence",
  "symbols": "AAPL,GOOGL,TSLA",
  "fromDate": "2010-01-01",
  "toDate": "2022-09-30"
});

var requestOptions = {
  method: 'POST',
  body: raw,
};

fetch("https://finnhub.io/api/v1/global-filings/search?token=<token>", requestOptions)
  .then(response => response.json())
```

### 示例 3 (Python)

```Python
import requests
import json

url = "https://finnhub.io/api/v1/global-filings/search?token=<token>"

payload = json.dumps({
  "query": "artificial intelligence",
  "symbols": "AAPL,GOOGL,TSLA",
  "fromDate": "2010-01-01",
  "toDate": "2022-09-30"
})

response = requests.request("POST", url, data=payload)

print(response.json())
```

### 示例 4 (bash)

```bash
curl --request POST 'https://finnhub.io/api/v1/global-filings/search?token=<token>' \
--data-raw '{
    "query": "artificial intelligence",
    "symbols": "AAPL,GOOGL,TSLA",
    "fromDate": "2010-01-01",
    "toDate": "2022-09-30"
}'
```

### 示例 5 (json)

```json
{
    "count": 8,
    "filings": [
        {
            "acceptanceDate": "2022-10-27 00:00:00",
            "amend": false,
            "documentCount": 1,
            "filedDate": "2022-10-27",
            "filerId": "3285503214",
            "filingId": "AAPL_1113753",
            "form": "TR/E",
            "name": "Apple Inc",
            "pageCount": 4,
            "reportPeriod": "",
            "source": "TR",
            "symbols": [
                "AAPL"
            ],
            "title": "AAPL - Earnings call Q4 2022",
            "url": "https://alpharesearch.io/platform/share?filingId=AAPL_1113753"
        }
        ...
    ],
    "page": 1,
    "took": 1986
}
```

## 文档正文

Search for best-matched filings across global companies' filings, transcripts and press releases. You can filter by anything from symbol, ISIN to form type, and document sources.This endpoint will return a list of documents that match your search criteria. If you would like to get the excerpts as well, please set highlighted to true. Once you have the list of documents, you can get a list of excerpts and positions to highlight the document using the /search-in-filing endpoint

## API 端点

**Method:** `POST`
**Endpoint:** `/global-filings/search`

Global Filings Search Premium

Search for best-matched filings across global companies' filings, transcripts and press releases. You can filter by anything from symbol, ISIN to form type, and document sources.

This endpoint will return a list of documents that match your search criteria. If you would like to get the excerpts as well, please set highlighted to true. Once you have the list of documents, you can get a list of excerpts and positions to highlight the document using the /search-in-filing endpoint

Method: POST

Premium: Premium Access Required

Examples:

/global-filings/search

Payload:

actsoptional

List of SEC's exchanges act to search, comma separated. Look at /filter endpoint to see all available values.

capsoptional

List of market capitalization to search, comma separated. Look at /filter endpoint to see all available values.

chIdsoptional

List of Companies House number to search, comma separated (Max: 50).

ciksoptional

List of SEC Center Index Key to search, comma separated (Max: 50).

countriesoptional

List of sources to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.

cusipsoptional

List of cusip to search, comma separated (Max: 50).

exchangesoptional

List of exchanges to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.

exhibitsoptional

List of exhibits to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.

formsoptional

List of forms to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.

fromDateoptional

Search from date in format: YYYY-MM-DD, default from the last 2 years

gicsoptional

List of gics to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.

highlightedoptional

Enable highlight in returned filings. If enabled, only return 10 results each time

isinsoptional

List of isin to search, comma separated (Max: 50).

naicsoptional

List of sources to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.

pageoptional

Use for pagination, default to page 1

queryREQUIRED

Search query

sedarIdsoptional

List of SEDAR issuer number to search, comma separated (Max: 50).

sedolsoptional

List of sedols to search, comma separated (Max: 50).

sortoptional

Sort result by, default: sortMostRecent. Look at /filter endpoint to see all available values.

sourcesoptional

List of sources to search, comma separated (Max: 50). Look at /filter endpoint to see all available values.

symbolsoptional

List of symbols to search, comma separated (Max: 50).

toDateoptional

Search to date in format: YYYY-MM-DD, default to today

Response Attributes:

count

Total filing matched your search criteria.

filings

Filing match your search criteria.

acceptanceDate

Date the filing is submitted.

amend

Amendment

documentCount

Number of document in this filing

filedDate

Date the filing is made available to the public

filerId

Id of the entity submitted the filing

filingId

Filing Id in Alpharesearch platform

form

Filing Form

name

Filer name

pageCount

Estimate number of page when printing

reportDate

Date as which the filing is reported

source

Filing Source

symbol

List of symbol associate with this filing

title

Filing title

page

Current search page

took

Time took to execute your search query on our server, value in ms.

Sample code
cURL
Python
Javascript

import requests
import json

url = "https://finnhub.io/api/v1/global-filings/search?token="

payload = json.dumps({
  "query": "artificial intelligence",
  "symbols": "AAPL,GOOGL,TSLA",
  "fromDate": "2010-01-01",
  "toDate": "2022-09-30"
})

response = requests.request("POST", url, data=payload)

print(response.json())

Sample response

{
    "count": 8,
    "filings": [
        {
            "acceptanceDate": "2022-10-27 00:00:00",
            "amend": false,
            "documentCount": 1,
            "filedDate": "2022-10-27",
            "filerId": "3285503214",
            "filingId": "AAPL_1113753",
            "form": "TR/E",
            "name": "Apple Inc",
            "pageCount": 4,
            "reportPeriod": "",
            "source": "TR",
            "symbols": [
                "AAPL"
            ],
            "title": "AAPL - Earnings call Q4 2022",
            "url": "https://alpharesearch.io/platform/share?filingId=AAPL_1113753"
        }
        ...
    ],
    "page": 1,
    "took": 1986
}
