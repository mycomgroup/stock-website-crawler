---
id: "url-2b35a746"
type: "api"
title: "global-filings-download"
url: "https://finnhub.io/docs/api/global-filings-download"
description: "Download filings using document ids."
source: ""
tags: []
crawl_time: "2026-03-18T09:53:50.163Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/global-filings/download"
  parameters:
    - {"name":"documentId","in":"query","required":true,"type":"string","description":"Document's id. Note that this is different from filingId as 1 filing can contain multiple documents."}
  responses: []
  codeExamples:
    - {"language":"cURL","code":"curl --request GET 'https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>'"}
    - {"language":"JavaScript","code":"var requestOptions = {\n  method: 'GET'\n};\n\nfetch(\"https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>\", requestOptions)\n  .then(response => response.json())"}
    - {"language":"Python","code":"import requests\n\nurl = \"https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>\"\n\nresponse = requests.request(\"GET\", url)\n\nprint(response.json())"}
  sampleResponse: ""
  curlExample: "curl --request GET 'https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>'"
  jsonExample: ""
  rawContent: ""
  suggestedFilename: "global-filings-download"
---

# global-filings-download

## 源URL

https://finnhub.io/docs/api/global-filings-download

## 描述

Download filings using document ids.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/global-filings/download`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `documentId` | string | 是 | - | Document's id. Note that this is different from filingId as 1 filing can contain multiple documents. |

## 代码示例

### 示例 1 (cURL)

```cURL
curl --request GET 'https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>'
```

### 示例 2 (JavaScript)

```JavaScript
var requestOptions = {
  method: 'GET'
};

fetch("https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>", requestOptions)
  .then(response => response.json())
```

### 示例 3 (Python)

```Python
import requests

url = "https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>"

response = requests.request("GET", url)

print(response.json())
```

### 示例 4 (bash)

```bash
curl --request GET 'https://finnhub.io/api/v1/global-filings/download?documentId=AAPL_1113753&token=<token>'
```

## 文档正文

Download filings using document ids.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/global-filings/download`
