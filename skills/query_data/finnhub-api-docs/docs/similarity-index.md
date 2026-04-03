---
id: "url-2e9af02d"
type: "api"
title: "Similarity Index Premium"
url: "https://finnhub.io/docs/api/similarity-index"
description: "Calculate the textual difference between a company's 10-K / 10-Q reports and the same type of report in the previous year using Cosine Similarity. For example, this endpoint compares 2019's 10-K with 2018's 10-K. Companies breaking from its routines in disclosure of financial condition and risk analysis section can signal a significant change in the company's stock price in the upcoming 4 quarters."
source: ""
tags: []
crawl_time: "2026-03-18T07:31:13.202Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/similarity-index?symbol=AAPL&freq=annual"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Symbol. Required if cik is empty"}
    - {"name":"cik","in":"query","required":false,"type":"string","description":"CIK. Required if symbol is empty"}
    - {"name":"freq","in":"query","required":false,"type":"string","description":"annual or quarterly. Default to annual"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.similarityIndex({\"symbol\": \"AAPL\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.sec_similarity_index('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.SimilarityIndex(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->similarityIndex(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.similarity_index({symbol: 'AAPL'}))"}
    - {"language":"Kotlin","code":"println(apiClient.similarityIndex(\"AAPL\", \"\", \"annual\"))"}
  sampleResponse: "{\n  \"cik\": \"320193\",\n  \"similarity\": [\n    {\n      \"cik\": \"320193\",\n      \"accessNumber\": \"0000320193-19-000119\",\n      \"item1\": 0.8833750347608914,\n      \"item2\": 0,\n      \"item1a\": 0.994836154829746,\n      \"item7\": 0.897030072745,\n      \"item7a\": 0.9843052590436008,\n      \"form\": \"10-K\",\n      \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm\",\n      \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/0000320193-19-000119-index.html\",\n      \"filedDate\": \"2019-10-31 00:00:00\",\n      \"acceptedDate\": \"2019-10-30 18:12:36\"\n    },\n    {\n      \"cik\": \"320193\",\n      \"accessNumber\": \"0000320193-18-000145\",\n      \"item1\": 0.9737784696339462,\n      \"item2\": 0,\n      \"item1a\": 0.9931651573630014,\n      \"item7\": 0.9441063774798184,\n      \"item7a\": 0.9856181212005336,\n      \"form\": \"10-K\",\n      \"reportUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm\",\n      \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145-index.html\",\n      \"filedDate\": \"2018-11-05 00:00:00\",\n      \"acceptedDate\": \"2018-11-05 08:01:40\"\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"cik\": \"320193\",\n  \"similarity\": [\n    {\n      \"cik\": \"320193\",\n      \"accessNumber\": \"0000320193-19-000119\",\n      \"item1\": 0.8833750347608914,\n      \"item2\": 0,\n      \"item1a\": 0.994836154829746,\n      \"item7\": 0.897030072745,\n      \"item7a\": 0.9843052590436008,\n      \"form\": \"10-K\",\n      \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm\",\n      \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/0000320193-19-000119-index.html\",\n      \"filedDate\": \"2019-10-31 00:00:00\",\n      \"acceptedDate\": \"2019-10-30 18:12:36\"\n    },\n    {\n      \"cik\": \"320193\",\n      \"accessNumber\": \"0000320193-18-000145\",\n      \"item1\": 0.9737784696339462,\n      \"item2\": 0,\n      \"item1a\": 0.9931651573630014,\n      \"item7\": 0.9441063774798184,\n      \"item7a\": 0.9856181212005336,\n      \"form\": \"10-K\",\n      \"reportUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm\",\n      \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145-index.html\",\n      \"filedDate\": \"2018-11-05 00:00:00\",\n      \"acceptedDate\": \"2018-11-05 08:01:40\"\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: "Similarity Index Premium\n\nCalculate the textual difference between a company's 10-K / 10-Q reports and the same type of report in the previous year using Cosine Similarity. For example, this endpoint compares 2019's 10-K with 2018's 10-K. Companies breaking from its routines in disclosure of financial condition and risk analysis section can signal a significant change in the company's stock price in the upcoming 4 quarters.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/similarity-index?symbol=AAPL&freq=annual\n\n/stock/similarity-index?cik=320193&freq=quarterly\n\nArguments:\n\nsymboloptional\n\nSymbol. Required if cik is empty\n\ncikoptional\n\nCIK. Required if symbol is empty\n\nfreqoptional\n\nannual or quarterly. Default to annual\n\nResponse Attributes:\n\ncik\n\nCIK.\n\nsimilarity\n\nArray of filings with its cosine similarity compared to the same report of the previous year.\n\nacceptedDate\n\nAccepted date %Y-%m-%d %H:%M:%S.\n\naccessNumber\n\nAccess number.\n\ncik\n\nCIK.\n\nfiledDate\n\nFiled date %Y-%m-%d %H:%M:%S.\n\nfilingUrl\n\nFiling's URL.\n\nform\n\nForm type.\n\nitem1\n\nCosine similarity of Item 1 (Business). This number is only available for Annual reports.\n\nitem1a\n\nCosine similarity of Item 1A (Risk Factors). This number is available for both Annual and Quarterly reports.\n\nitem2\n\nCosine similarity of Item 2 (Management’s Discussion and Analysis of Financial Condition and Results of Operations). This number is only available for Quarterly reports.\n\nitem7\n\nCosine similarity of Item 7 (Management’s Discussion and Analysis of Financial Condition and Results of Operations). This number is only available for Annual reports.\n\nitem7a\n\nCosine similarity of Item 7A (Quantitative and Qualitative Disclosures About Market Risk). This number is only available for Annual reports.\n\nreportUrl\n\nReport's URL.\n\nsymbol\n\nSymbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.sec_similarity_index('AAPL'))\n\nSample response\n\n{\n  \"cik\": \"320193\",\n  \"similarity\": [\n    {\n      \"cik\": \"320193\",\n      \"accessNumber\": \"0000320193-19-000119\",\n      \"item1\": 0.8833750347608914,\n      \"item2\": 0,\n      \"item1a\": 0.994836154829746,\n      \"item7\": 0.897030072745,\n      \"item7a\": 0.9843052590436008,\n      \"form\": \"10-K\",\n      \"reportUrl\": \"https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm\",\n      \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/0000320193-19-000119-index.html\",\n      \"filedDate\": \"2019-10-31 00:00:00\",\n      \"acceptedDate\": \"2019-10-30 18:12:36\"\n    },\n    {\n      \"cik\": \"320193\",\n      \"accessNumber\": \"0000320193-18-000145\",\n      \"item1\": 0.9737784696339462,\n      \"item2\": 0,\n      \"item1a\": 0.9931651573630014,\n      \"item7\": 0.9441063774798184,\n      \"item7a\": 0.9856181212005336,\n      \"form\": \"10-K\",\n      \"reportUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm\",\n      \"filingUrl\": \"https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145-index.html\",\n      \"filedDate\": \"2018-11-05 00:00:00\",\n      \"acceptedDate\": \"2018-11-05 08:01:40\"\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "similarity-index"
---

# Similarity Index Premium

## 源URL

https://finnhub.io/docs/api/similarity-index

## 描述

Calculate the textual difference between a company's 10-K / 10-Q reports and the same type of report in the previous year using Cosine Similarity. For example, this endpoint compares 2019's 10-K with 2018's 10-K. Companies breaking from its routines in disclosure of financial condition and risk analysis section can signal a significant change in the company's stock price in the upcoming 4 quarters.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/similarity-index?symbol=AAPL&freq=annual`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Symbol. Required if cik is empty |
| `cik` | string | 否 | - | CIK. Required if symbol is empty |
| `freq` | string | 否 | - | annual or quarterly. Default to annual |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.similarityIndex({"symbol": "AAPL"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.sec_similarity_index('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.SimilarityIndex(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->similarityIndex("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.similarity_index({symbol: 'AAPL'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.similarityIndex("AAPL", "", "annual"))
```

### 示例 7 (json)

```json
{
  "cik": "320193",
  "similarity": [
    {
      "cik": "320193",
      "accessNumber": "0000320193-19-000119",
      "item1": 0.8833750347608914,
      "item2": 0,
      "item1a": 0.994836154829746,
      "item7": 0.897030072745,
      "item7a": 0.9843052590436008,
      "form": "10-K",
      "reportUrl": "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm",
      "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/0000320193-19-000119-index.html",
      "filedDate": "2019-10-31 00:00:00",
      "acceptedDate": "2019-10-30 18:12:36"
    },
    {
      "cik": "320193",
      "accessNumber": "0000320193-18-000145",
      "item1": 0.9737784696339462,
      "item2": 0,
      "item1a": 0.9931651573630014,
      "item7": 0.9441063774798184,
      "item7a": 0.9856181212005336,
      "form": "10-K",
      "reportUrl": "https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm",
      "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145-index.html",
      "filedDate": "2018-11-05 00:00:00",
      "acceptedDate": "2018-11-05 08:01:40"
    }
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Calculate the textual difference between a company's 10-K / 10-Q reports and the same type of report in the previous year using Cosine Similarity. For example, this endpoint compares 2019's 10-K with 2018's 10-K. Companies breaking from its routines in disclosure of financial condition and risk analysis section can signal a significant change in the company's stock price in the upcoming 4 quarters.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/similarity-index?symbol=AAPL&freq=annual`

Similarity Index Premium

Calculate the textual difference between a company's 10-K / 10-Q reports and the same type of report in the previous year using Cosine Similarity. For example, this endpoint compares 2019's 10-K with 2018's 10-K. Companies breaking from its routines in disclosure of financial condition and risk analysis section can signal a significant change in the company's stock price in the upcoming 4 quarters.

Method: GET

Premium: Premium Access Required

Examples:

/stock/similarity-index?symbol=AAPL&freq=annual

/stock/similarity-index?cik=320193&freq=quarterly

Arguments:

symboloptional

Symbol. Required if cik is empty

cikoptional

CIK. Required if symbol is empty

freqoptional

annual or quarterly. Default to annual

Response Attributes:

cik

CIK.

similarity

Array of filings with its cosine similarity compared to the same report of the previous year.

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

item1

Cosine similarity of Item 1 (Business). This number is only available for Annual reports.

item1a

Cosine similarity of Item 1A (Risk Factors). This number is available for both Annual and Quarterly reports.

item2

Cosine similarity of Item 2 (Management’s Discussion and Analysis of Financial Condition and Results of Operations). This number is only available for Quarterly reports.

item7

Cosine similarity of Item 7 (Management’s Discussion and Analysis of Financial Condition and Results of Operations). This number is only available for Annual reports.

item7a

Cosine similarity of Item 7A (Quantitative and Qualitative Disclosures About Market Risk). This number is only available for Annual reports.

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

print(finnhub_client.sec_similarity_index('AAPL'))

Sample response

{
  "cik": "320193",
  "similarity": [
    {
      "cik": "320193",
      "accessNumber": "0000320193-19-000119",
      "item1": 0.8833750347608914,
      "item2": 0,
      "item1a": 0.994836154829746,
      "item7": 0.897030072745,
      "item7a": 0.9843052590436008,
      "form": "10-K",
      "reportUrl": "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019319000119/a10-k20199282019.htm",
      "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/0000320193-19-000119-index.html",
      "filedDate": "2019-10-31 00:00:00",
      "acceptedDate": "2019-10-30 18:12:36"
    },
    {
      "cik": "320193",
      "accessNumber": "0000320193-18-000145",
      "item1": 0.9737784696339462,
      "item2": 0,
      "item1a": 0.9931651573630014,
      "item7": 0.9441063774798184,
      "item7a": 0.9856181212005336,
      "form": "10-K",
      "reportUrl": "https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm",
      "filingUrl": "https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/0000320193-18-000145-index.html",
      "filedDate": "2018-11-05 00:00:00",
      "acceptedDate": "2018-11-05 08:01:40"
    }
  ],
  "symbol": "AAPL"
}
