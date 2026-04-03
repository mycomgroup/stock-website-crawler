---
id: "url-f629db5"
type: "api"
title: "Search Filter Premium"
url: "https://finnhub.io/docs/api/global-filings-search-filter"
description: "Get available values for each filter in search body. Method: GET Premium: Premium Access Required"
source: ""
tags: []
crawl_time: "2026-03-18T10:38:53.047Z"
metadata:
  requestMethod: "GET"
  endpoint: "/global-filings/filter?field=forms&source=SEC"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Search Filter Premium\n\nGet available values for each filter in search body.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/global-filings/filter?field=forms&source=SEC\n\nArguments:\n\nfieldREQUIRED\n\nField to get available filters. Available filters are \"countries\", \"exchanges\", \"exhibits\", \"forms\", \"gics\", \"naics\", \"caps\", \"acts\", and \"sort\".\n\nsourceoptional\n\nGet available forms for each source.\n\nResponse Attributes:\n\nid\n\nFilter id, use with respective field in search query body.\n\nname\n\nDisplay name.\n\nSample code\ncURL\nPython\nJavascript\n\nimport requests\n\nurl = \"https://finnhub.io/api/v1/global-filings/filter?field=sources&token=\"\n\nresponse = requests.request(\"GET\", url)\n\nprint(response.json())\n\nSample response\n\n[\n    {\n        \"id\": \"SEC\",\n        \"name\": \"US SEC Edgar Filings\"\n    },\n    {\n        \"id\": \"TR\",\n        \"name\": \"Event Transcripts\"\n    },\n    {\n        \"id\": \"SEDAR\",\n        \"name\": \"Canada SEDAR Filings\"\n    },\n    {\n        \"id\": \"CH\",\n        \"name\": \"UK Companies House Filings\"\n    },\n    {\n        \"id\": \"PR\",\n        \"name\": \"Press Releases\"\n    },\n    {\n        \"id\": \"RR\",\n        \"name\": \"Research Reports\"\n    },\n    {\n        \"id\": \"GF\",\n        \"name\": \"Global Filings\"\n    }\n]"
  suggestedFilename: "global-filings-search-filter"
---

# Search Filter Premium

## 源URL

https://finnhub.io/docs/api/global-filings-search-filter

## 描述

Get available values for each filter in search body. Method: GET Premium: Premium Access Required

## API 端点

**Method**: `GET`
**Endpoint**: `/global-filings/filter?field=forms&source=SEC`

## 文档正文

Get available values for each filter in search body. Method: GET Premium: Premium Access Required

## API 端点

**Method:** `GET`
**Endpoint:** `/global-filings/filter?field=forms&source=SEC`

Search Filter Premium

Get available values for each filter in search body.

Method: GET

Premium: Premium Access Required

Examples:

/global-filings/filter?field=forms&source=SEC

Arguments:

fieldREQUIRED

Field to get available filters. Available filters are "countries", "exchanges", "exhibits", "forms", "gics", "naics", "caps", "acts", and "sort".

sourceoptional

Get available forms for each source.

Response Attributes:

id

Filter id, use with respective field in search query body.

name

Display name.

Sample code
cURL
Python
Javascript

import requests

url = "https://finnhub.io/api/v1/global-filings/filter?field=sources&token="

response = requests.request("GET", url)

print(response.json())

Sample response

[
    {
        "id": "SEC",
        "name": "US SEC Edgar Filings"
    },
    {
        "id": "TR",
        "name": "Event Transcripts"
    },
    {
        "id": "SEDAR",
        "name": "Canada SEDAR Filings"
    },
    {
        "id": "CH",
        "name": "UK Companies House Filings"
    },
    {
        "id": "PR",
        "name": "Press Releases"
    },
    {
        "id": "RR",
        "name": "Research Reports"
    },
    {
        "id": "GF",
        "name": "Global Filings"
    }
]
