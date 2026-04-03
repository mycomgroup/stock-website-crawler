---
id: "url-7a440271"
type: "api"
title: "SEC Filings"
url: "https://finnhub.io/docs/api/filings"
description: "List company's filing. Limit to 250 documents at a time. This data is available for bulk download on Kaggle SEC Filings database."
source: ""
tags: []
crawl_time: "2026-03-18T03:12:43.157Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/filings?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Symbol. Leave symbol,cik and accessNumber empty to list latest filings."}
    - {"name":"cik","in":"query","required":false,"type":"string","description":"CIK."}
    - {"name":"accessNumber","in":"query","required":false,"type":"string","description":"Access number of a specific report you want to retrieve data from."}
    - {"name":"form","in":"query","required":false,"type":"string","description":"Filter by form. You can use this value NT 10-K to find non-timely filings for a company."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date: 2023-03-15."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date: 2023-03-16."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.filings({\"symbol\": \"AAPL\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.filings(symbol='AAPL', _from=\"2020-01-01\", to=\"2020-06-11\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.Filings(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->filings(\"AAPL\", \"2020-01-01\", \"2020-06-11\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.filings({symbol: 'AAPL', from: \"2020-01-01\", to: \"2020-06-11\"}))"}
    - {"language":"Kotlin","code":"println(\n            apiClient.filings(\n                symbol = \"AAPL\",\n                from = \"2020-01-01\",\n                to = \"2020-06-11\",\n                accessNumber = null,\n                cik = null,\n                form = null\n            )\n        )"}
  sampleResponse: "[\n  {\n    \"accessNumber\": \"0001193125-20-050884\",\n    \"symbol\": \"AAPL\",\n    \"cik\": \"320193\",\n    \"form\": \"8-K\",\n    \"filedDate\": \"2020-02-27 00:00:00\",\n    \"acceptedDate\": \"2020-02-27 06:14:21\",\n    \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520050884/d865740d8k.htm\",\n    \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000119312520050884/0001193125-20-050884-index.html\"\n  },\n  {\n    \"accessNumber\": \"0001193125-20-039203\",\n    \"symbol\": \"AAPL\",\n    \"cik\": \"320193\",\n    \"form\": \"8-K\",\n    \"filedDate\": \"2020-02-18 00:00:00\",\n    \"acceptedDate\": \"2020-02-18 06:24:57\",\n    \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520039203/d845033d8k.htm\",\n    \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000119312520039203/0001193125-20-039203-index.html\"\n  },\n  ...\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"accessNumber\": \"0001193125-20-050884\",\n    \"symbol\": \"AAPL\",\n    \"cik\": \"320193\",\n    \"form\": \"8-K\",\n    \"filedDate\": \"2020-02-27 00:00:00\",\n    \"acceptedDate\": \"2020-02-27 06:14:21\",\n    \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520050884/d865740d8k.htm\",\n    \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000119312520050884/0001193125-20-050884-index.html\"\n  },\n  {\n    \"accessNumber\": \"0001193125-20-039203\",\n    \"symbol\": \"AAPL\",\n    \"cik\": \"320193\",\n    \"form\": \"8-K\",\n    \"filedDate\": \"2020-02-18 00:00:00\",\n    \"acceptedDate\": \"2020-02-18 06:24:57\",\n    \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520039203/d845033d8k.htm\",\n    \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000119312520039203/0001193125-20-039203-index.html\"\n  },\n  ...\n]"
  rawContent: "SEC Filings\n\nList company's filing. Limit to 250 documents at a time. This data is available for bulk download on Kaggle SEC Filings database.\n\nMethod: GET\n\nExamples:\n\n/stock/filings?symbol=AAPL\n\n/stock/filings?cik=320193\n\n/stock/filings?accessNumber=0000320193-20-000052\n\nArguments:\n\nsymboloptional\n\nSymbol. Leave symbol,cik and accessNumber empty to list latest filings.\n\ncikoptional\n\nCIK.\n\naccessNumberoptional\n\nAccess number of a specific report you want to retrieve data from.\n\nformoptional\n\nFilter by form. You can use this value NT 10-K to find non-timely filings for a company.\n\nfromoptional\n\nFrom date: 2023-03-15.\n\ntooptional\n\nTo date: 2023-03-16.\n\nResponse Attributes:\n\nacceptedDate\n\nAccepted date %Y-%m-%d %H:%M:%S.\n\naccessNumber\n\nAccess number.\n\ncik\n\nCIK.\n\nfiledDate\n\nFiled date %Y-%m-%d %H:%M:%S.\n\nfilingUrl\n\nFiling's URL.\n\nform\n\nForm type.\n\nreportUrl\n\nReport's URL.\n\nsymbol\n\nSymbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.filings(symbol='AAPL', _from=\"2020-01-01\", to=\"2020-06-11\"))\n\nSample response\n\n[\n  {\n    \"accessNumber\": \"0001193125-20-050884\",\n    \"symbol\": \"AAPL\",\n    \"cik\": \"320193\",\n    \"form\": \"8-K\",\n    \"filedDate\": \"2020-02-27 00:00:00\",\n    \"acceptedDate\": \"2020-02-27 06:14:21\",\n    \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520050884/d865740d8k.htm\",\n    \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000119312520050884/0001193125-20-050884-index.html\"\n  },\n  {\n    \"accessNumber\": \"0001193125-20-039203\",\n    \"symbol\": \"AAPL\",\n    \"cik\": \"320193\",\n    \"form\": \"8-K\",\n    \"filedDate\": \"2020-02-18 00:00:00\",\n    \"acceptedDate\": \"2020-02-18 06:24:57\",\n    \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520039203/d845033d8k.htm\",\n    \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000119312520039203/0001193125-20-039203-index.html\"\n  },\n  ...\n]"
  suggestedFilename: "filings"
---

# SEC Filings

## 源URL

https://finnhub.io/docs/api/filings

## 描述

List company's filing. Limit to 250 documents at a time. This data is available for bulk download on Kaggle SEC Filings database.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/filings?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Symbol. Leave symbol,cik and accessNumber empty to list latest filings. |
| `cik` | string | 否 | - | CIK. |
| `accessNumber` | string | 否 | - | Access number of a specific report you want to retrieve data from. |
| `form` | string | 否 | - | Filter by form. You can use this value NT 10-K to find non-timely filings for a company. |
| `from` | string | 否 | - | From date: 2023-03-15. |
| `to` | string | 否 | - | To date: 2023-03-16. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.filings({"symbol": "AAPL"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.filings(symbol='AAPL', _from="2020-01-01", to="2020-06-11"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.Filings(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->filings("AAPL", "2020-01-01", "2020-06-11"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.filings({symbol: 'AAPL', from: "2020-01-01", to: "2020-06-11"}))
```

### 示例 6 (Kotlin)

```Kotlin
println(
            apiClient.filings(
                symbol = "AAPL",
                from = "2020-01-01",
                to = "2020-06-11",
                accessNumber = null,
                cik = null,
                form = null
            )
        )
```

### 示例 7 (json)

```json
[
  {
    "accessNumber": "0001193125-20-050884",
    "symbol": "AAPL",
    "cik": "320193",
    "form": "8-K",
    "filedDate": "2020-02-27 00:00:00",
    "acceptedDate": "2020-02-27 06:14:21",
    "reportUrl": "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520050884/d865740d8k.htm",
    "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000119312520050884/0001193125-20-050884-index.html"
  },
  {
    "accessNumber": "0001193125-20-039203",
    "symbol": "AAPL",
    "cik": "320193",
    "form": "8-K",
    "filedDate": "2020-02-18 00:00:00",
    "acceptedDate": "2020-02-18 06:24:57",
    "reportUrl": "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520039203/d845033d8k.htm",
    "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000119312520039203/0001193125-20-039203-index.html"
  },
  ...
]
```

## 文档正文

List company's filing. Limit to 250 documents at a time. This data is available for bulk download on Kaggle SEC Filings database.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/filings?symbol=AAPL`

SEC Filings

List company's filing. Limit to 250 documents at a time. This data is available for bulk download on Kaggle SEC Filings database.

Method: GET

Examples:

/stock/filings?symbol=AAPL

/stock/filings?cik=320193

/stock/filings?accessNumber=0000320193-20-000052

Arguments:

symboloptional

Symbol. Leave symbol,cik and accessNumber empty to list latest filings.

cikoptional

CIK.

accessNumberoptional

Access number of a specific report you want to retrieve data from.

formoptional

Filter by form. You can use this value NT 10-K to find non-timely filings for a company.

fromoptional

From date: 2023-03-15.

tooptional

To date: 2023-03-16.

Response Attributes:

acceptedDate

Accepted date %Y-%m-%d %H:%M:%S.

accessNumber

Access number.

cik

CIK.

filedDate

Filed date %Y-%m-%d %H:%M:%S.

filingUrl

Filing's URL.

form

Form type.

reportUrl

Report's URL.

symbol

Symbol.

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

print(finnhub_client.filings(symbol='AAPL', _from="2020-01-01", to="2020-06-11"))

Sample response

[
  {
    "accessNumber": "0001193125-20-050884",
    "symbol": "AAPL",
    "cik": "320193",
    "form": "8-K",
    "filedDate": "2020-02-27 00:00:00",
    "acceptedDate": "2020-02-27 06:14:21",
    "reportUrl": "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520050884/d865740d8k.htm",
    "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000119312520050884/0001193125-20-050884-index.html"
  },
  {
    "accessNumber": "0001193125-20-039203",
    "symbol": "AAPL",
    "cik": "320193",
    "form": "8-K",
    "filedDate": "2020-02-18 00:00:00",
    "acceptedDate": "2020-02-18 06:24:57",
    "reportUrl": "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000119312520039203/d845033d8k.htm",
    "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000119312520039203/0001193125-20-039203-index.html"
  },
  ...
]
