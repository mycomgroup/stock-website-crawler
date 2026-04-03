---
id: "url-69068567"
type: "api"
title: "Search In Filing Premium"
url: "https://finnhub.io/docs/api/search-in-filing"
description: "Get a list of excerpts and highlight positions within a document using your query."
source: ""
tags: []
crawl_time: "2026-03-18T08:12:13.935Z"
metadata:
  requestMethod: "POST"
  endpoint: "/global-filings/search-in-filing"
  parameters:
    - {"name":"search","in":"body","required":false,"type":"","description":"Search body"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"cURL","code":"curl --request POST 'https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>' \\\n--data-raw '{\n    \"query\": \"covid\",\n    \"filingId\": \"AAPL_1113753\"\n}'"}
    - {"language":"JavaScript","code":"var raw = JSON.stringify({\n  \"query\": \"covid\",\n  \"filingId\": \"AAPL_1113753\"\n});\n\nvar requestOptions = {\n  method: 'POST',\n  body: raw,\n  redirect: 'follow'\n};\n\nfetch(\"https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>\", requestOptions)\n  .then(response => response.json())"}
    - {"language":"Python","code":"import requests\nimport json\n\nurl = \"https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>\"\n\npayload = json.dumps({\n  \"query\": \"covid\",\n  \"filingId\": \"AAPL_1113753\"\n})\n\nresponse = requests.request(\"POST\", url,  data=payload)\n\nprint(response.json())"}
  sampleResponse: "{\n  \"acceptanceDate\": \"2022-10-27 00:00:00\",\n  \"amend\": false,\n  \"documentCount\": 1,\n  \"documents\": [\n      {\n          \"documentId\": \"AAPL_1113753\",\n          \"excerpts\": [\n              {\n                  \"content\": \"If you compare it to pre-<span class='search-highlight'>pandemic</span> kind of levels, that has not returned to pre <span class='search-highlight'>pandemic</span> levels by any means.\\n\",\n                  \"endOffset\": 494,\n                  \"snippetId\": \"tran-46\",\n                  \"startOffset\": 385\n              }\n              ...\n          ],\n          \"format\": \"html\",\n          \"hits\": 5,\n          \"title\": \"Transcript\",\n          \"url\": \"https://alpharesearch.io/filing/transcript?documentId=AAPL_1113753\"\n      }\n  ],\n  \"filedDate\": \"2022-10-27\",\n  \"filerId\": \"4295905573\",\n  \"filingId\": \"AAPL_1113753\",\n  \"form\": \"TR/E\",\n  \"name\": \"Apple Inc\",\n  \"pageCount\": 4,\n  \"reportPeriod\": \"\",\n  \"source\": \"TR\",\n  \"symbols\": [\n      \"AAPL\"\n  ],\n  \"title\": \"AAPL - Earnings call Q4 2022\",\n  \"url\": \"https://alpharesearch.io/platform/share?filingId=AAPL_1113753\"\n}"
  curlExample: "curl --request POST 'https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>' \\\n--data-raw '{\n    \"query\": \"covid\",\n    \"filingId\": \"AAPL_1113753\"\n}'"
  jsonExample: "{\n  \"acceptanceDate\": \"2022-10-27 00:00:00\",\n  \"amend\": false,\n  \"documentCount\": 1,\n  \"documents\": [\n      {\n          \"documentId\": \"AAPL_1113753\",\n          \"excerpts\": [\n              {\n                  \"content\": \"If you compare it to pre-<span class='search-highlight'>pandemic</span> kind of levels, that has not returned to pre <span class='search-highlight'>pandemic</span> levels by any means.\\n\",\n                  \"endOffset\": 494,\n                  \"snippetId\": \"tran-46\",\n                  \"startOffset\": 385\n              }\n              ...\n          ],\n          \"format\": \"html\",\n          \"hits\": 5,\n          \"title\": \"Transcript\",\n          \"url\": \"https://alpharesearch.io/filing/transcript?documentId=AAPL_1113753\"\n      }\n  ],\n  \"filedDate\": \"2022-10-27\",\n  \"filerId\": \"4295905573\",\n  \"filingId\": \"AAPL_1113753\",\n  \"form\": \"TR/E\",\n  \"name\": \"Apple Inc\",\n  \"pageCount\": 4,\n  \"reportPeriod\": \"\",\n  \"source\": \"TR\",\n  \"symbols\": [\n      \"AAPL\"\n  ],\n  \"title\": \"AAPL - Earnings call Q4 2022\",\n  \"url\": \"https://alpharesearch.io/platform/share?filingId=AAPL_1113753\"\n}"
  rawContent: "Search In Filing Premium\n\nGet a list of excerpts and highlight positions within a document using your query.\n\nMethod: POST\n\nPremium: Premium Access Required\n\nExamples:\n\n/global-filings/search-in-filing\n\nPayload:\n\nfilingIdREQUIRED\n\nFiling Id to search\n\nqueryREQUIRED\n\nSearch query\n\nResponse Attributes:\n\nacceptanceDate\n\nDate the filing is submitted.\n\namend\n\nAmendment\n\ndocumentCount\n\nNumber of document in this filing\n\ndocuments\n\nDocument for this filing.\n\ndocumentId\n\nAlphaResearch internal document id.\n\nexcerpts\n\nHighlighted excerpts for this document\n\ncontent\n\nHighlighted content\n\nendOffset\n\nEnd offset of highlighted content\n\nsnippetId\n\nLocation of the content in the rendered document\n\nstartOffset\n\nStart offset of highlighted content\n\nformat\n\nFormat of this document (can be html or pdf)\n\nhits\n\nNumber of hit in this document\n\ntitle\n\nTitle for this document.\n\nurl\n\nLink to render this document\n\nfiledDate\n\nDate the filing is make available to the public\n\nfilerId\n\nId of the entity submitted the filing\n\nfilingId\n\nFiling Id in Alpharesearch platform\n\nform\n\nFiling Form\n\nname\n\nFiler name\n\npageCount\n\nEstimate number of page when printing\n\nreportDate\n\nDate as which the filing is reported\n\nsource\n\nFiling Source\n\nsymbol\n\nList of symbol associate with this filing\n\ntitle\n\nFiling title\n\nSample code\ncURL\nPython\nJavascript\n\nimport requests\nimport json\n\nurl = \"https://finnhub.io/api/v1/global-filings/search-in-filing?token=\"\n\npayload = json.dumps({\n  \"query\": \"covid\",\n  \"filingId\": \"AAPL_1113753\"\n})\n\nresponse = requests.request(\"POST\", url,  data=payload)\n\nprint(response.json())\n\nSample response\n\n{\n  \"acceptanceDate\": \"2022-10-27 00:00:00\",\n  \"amend\": false,\n  \"documentCount\": 1,\n  \"documents\": [\n      {\n          \"documentId\": \"AAPL_1113753\",\n          \"excerpts\": [\n              {\n                  \"content\": \"If you compare it to pre-<span class='search-highlight'>pandemic</span> kind of levels, that has not returned to pre <span class='search-highlight'>pandemic</span> levels by any means.\\n\",\n                  \"endOffset\": 494,\n                  \"snippetId\": \"tran-46\",\n                  \"startOffset\": 385\n              }\n              ...\n          ],\n          \"format\": \"html\",\n          \"hits\": 5,\n          \"title\": \"Transcript\",\n          \"url\": \"https://alpharesearch.io/filing/transcript?documentId=AAPL_1113753\"\n      }\n  ],\n  \"filedDate\": \"2022-10-27\",\n  \"filerId\": \"4295905573\",\n  \"filingId\": \"AAPL_1113753\",\n  \"form\": \"TR/E\",\n  \"name\": \"Apple Inc\",\n  \"pageCount\": 4,\n  \"reportPeriod\": \"\",\n  \"source\": \"TR\",\n  \"symbols\": [\n      \"AAPL\"\n  ],\n  \"title\": \"AAPL - Earnings call Q4 2022\",\n  \"url\": \"https://alpharesearch.io/platform/share?filingId=AAPL_1113753\"\n}"
  suggestedFilename: "search-in-filing"
---

# Search In Filing Premium

## 源URL

https://finnhub.io/docs/api/search-in-filing

## 描述

Get a list of excerpts and highlight positions within a document using your query.

## API 端点

**Method**: `POST`
**Endpoint**: `/global-filings/search-in-filing`

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
curl --request POST 'https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>' \
--data-raw '{
    "query": "covid",
    "filingId": "AAPL_1113753"
}'
```

### 示例 2 (JavaScript)

```JavaScript
var raw = JSON.stringify({
  "query": "covid",
  "filingId": "AAPL_1113753"
});

var requestOptions = {
  method: 'POST',
  body: raw,
  redirect: 'follow'
};

fetch("https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>", requestOptions)
  .then(response => response.json())
```

### 示例 3 (Python)

```Python
import requests
import json

url = "https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>"

payload = json.dumps({
  "query": "covid",
  "filingId": "AAPL_1113753"
})

response = requests.request("POST", url,  data=payload)

print(response.json())
```

### 示例 4 (bash)

```bash
curl --request POST 'https://finnhub.io/api/v1/global-filings/search-in-filing?token=<token>' \
--data-raw '{
    "query": "covid",
    "filingId": "AAPL_1113753"
}'
```

### 示例 5 (json)

```json
{
  "acceptanceDate": "2022-10-27 00:00:00",
  "amend": false,
  "documentCount": 1,
  "documents": [
      {
          "documentId": "AAPL_1113753",
          "excerpts": [
              {
                  "content": "If you compare it to pre-<span class='search-highlight'>pandemic</span> kind of levels, that has not returned to pre <span class='search-highlight'>pandemic</span> levels by any means.\n",
                  "endOffset": 494,
                  "snippetId": "tran-46",
                  "startOffset": 385
              }
              ...
          ],
          "format": "html",
          "hits": 5,
          "title": "Transcript",
          "url": "https://alpharesearch.io/filing/transcript?documentId=AAPL_1113753"
      }
  ],
  "filedDate": "2022-10-27",
  "filerId": "4295905573",
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
```

## 文档正文

Get a list of excerpts and highlight positions within a document using your query.

## API 端点

**Method:** `POST`
**Endpoint:** `/global-filings/search-in-filing`

Search In Filing Premium

Get a list of excerpts and highlight positions within a document using your query.

Method: POST

Premium: Premium Access Required

Examples:

/global-filings/search-in-filing

Payload:

filingIdREQUIRED

Filing Id to search

queryREQUIRED

Search query

Response Attributes:

acceptanceDate

Date the filing is submitted.

amend

Amendment

documentCount

Number of document in this filing

documents

Document for this filing.

documentId

AlphaResearch internal document id.

excerpts

Highlighted excerpts for this document

content

Highlighted content

endOffset

End offset of highlighted content

snippetId

Location of the content in the rendered document

startOffset

Start offset of highlighted content

format

Format of this document (can be html or pdf)

hits

Number of hit in this document

title

Title for this document.

url

Link to render this document

filedDate

Date the filing is make available to the public

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

Sample code
cURL
Python
Javascript

import requests
import json

url = "https://finnhub.io/api/v1/global-filings/search-in-filing?token="

payload = json.dumps({
  "query": "covid",
  "filingId": "AAPL_1113753"
})

response = requests.request("POST", url,  data=payload)

print(response.json())

Sample response

{
  "acceptanceDate": "2022-10-27 00:00:00",
  "amend": false,
  "documentCount": 1,
  "documents": [
      {
          "documentId": "AAPL_1113753",
          "excerpts": [
              {
                  "content": "If you compare it to pre-<span class='search-highlight'>pandemic</span> kind of levels, that has not returned to pre <span class='search-highlight'>pandemic</span> levels by any means.\n",
                  "endOffset": 494,
                  "snippetId": "tran-46",
                  "startOffset": 385
              }
              ...
          ],
          "format": "html",
          "hits": 5,
          "title": "Transcript",
          "url": "https://alpharesearch.io/filing/transcript?documentId=AAPL_1113753"
      }
  ],
  "filedDate": "2022-10-27",
  "filerId": "4295905573",
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
