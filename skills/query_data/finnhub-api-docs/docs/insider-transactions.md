---
id: "url-54bbc2b7"
type: "api"
title: "Insider Transactions"
url: "https://finnhub.io/docs/api/insider-transactions"
description: "Company insider transactions data sourced from Form 3,4,5, SEDI and relevant companies' filings. This endpoint covers US, UK, Canada, Australia, India, and all major EU markets. Limit to 100 transactions per API call."
source: ""
tags: []
crawl_time: "2026-03-18T08:36:26.647Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/insider-transactions?symbol=TSLA&limit=20"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL. Leave this param blank to get the latest transactions."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date: 2020-03-15."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date: 2020-03-16."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.insiderTransactions('AAPL', (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_insider_transactions('AAPL', '2021-01-01', '2021-03-01'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.InsiderTransactions(context.Background()).Symbol(\"AAPL\").From(\"2021-01-01\").To(\"2021-07-30\").Execute()"}
    - {"language":"PHP","code":"print_r($client->insiderTransactions(\"AAPL\", \"2021-01-01\", \"2021-03-01\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.insider_transactions('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.insiderTransactions(\"AAPL\", \"2021-01-01\", \"2021-07-07\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"name\": \"Kirkhorn Zachary\",\n      \"share\": 57234,\n      \"change\": -1250,\n      \"filingDate\": \"2021-03-19\",\n      \"transactionDate\": \"2021-03-17\",\n      \"transactionCode\": \"S\",\n      \"transactionPrice\": 655.81\n    },\n    {\n      \"name\": \"Baglino Andrew D\",\n      \"share\": 20614,\n      \"change\": 1000,\n      \"filingDate\": \"2021-03-31\",\n      \"transactionDate\": \"2021-03-29\",\n      \"transactionCode\": \"M\",\n      \"transactionPrice\": 41.57\n    },\n    {\n      \"name\": \"Baglino Andrew D\",\n      \"share\": 19114,\n      \"change\": -1500,\n      \"filingDate\": \"2021-03-31\",\n      \"transactionDate\": \"2021-03-29\",\n      \"transactionCode\": \"S\",\n      \"transactionPrice\": 615.75\n    }\n  ],\n  \"symbol\": \"TSLA\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"name\": \"Kirkhorn Zachary\",\n      \"share\": 57234,\n      \"change\": -1250,\n      \"filingDate\": \"2021-03-19\",\n      \"transactionDate\": \"2021-03-17\",\n      \"transactionCode\": \"S\",\n      \"transactionPrice\": 655.81\n    },\n    {\n      \"name\": \"Baglino Andrew D\",\n      \"share\": 20614,\n      \"change\": 1000,\n      \"filingDate\": \"2021-03-31\",\n      \"transactionDate\": \"2021-03-29\",\n      \"transactionCode\": \"M\",\n      \"transactionPrice\": 41.57\n    },\n    {\n      \"name\": \"Baglino Andrew D\",\n      \"share\": 19114,\n      \"change\": -1500,\n      \"filingDate\": \"2021-03-31\",\n      \"transactionDate\": \"2021-03-29\",\n      \"transactionCode\": \"S\",\n      \"transactionPrice\": 615.75\n    }\n  ],\n  \"symbol\": \"TSLA\"\n}"
  rawContent: "Insider Transactions\n\nCompany insider transactions data sourced from Form 3,4,5, SEDI and relevant companies' filings. This endpoint covers US, UK, Canada, Australia, India, and all major EU markets. Limit to 100 transactions per API call.\n\nMethod: GET\n\nExamples:\n\n/stock/insider-transactions?symbol=TSLA&limit=20\n\n/stock/insider-transactions?symbol=AC.TO\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL. Leave this param blank to get the latest transactions.\n\nfromoptional\n\nFrom date: 2020-03-15.\n\ntooptional\n\nTo date: 2020-03-16.\n\nResponse Attributes:\n\ndata\n\nArray of insider transactions.\n\nchange\n\nNumber of share changed from the last period. A positive value suggests a BUY transaction. A negative value suggests a SELL transaction.\n\nfilingDate\n\nFiling date.\n\nname\n\nInsider's name.\n\nshare\n\nNumber of shares held after the transaction.\n\nsymbol\n\nSymbol.\n\ntransactionCode\n\nTransaction code. A list of codes and their meanings can be found here.\n\ntransactionDate\n\nTransaction date.\n\ntransactionPrice\n\nAverage transaction price.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_insider_transactions('AAPL', '2021-01-01', '2021-03-01'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"name\": \"Kirkhorn Zachary\",\n      \"share\": 57234,\n      \"change\": -1250,\n      \"filingDate\": \"2021-03-19\",\n      \"transactionDate\": \"2021-03-17\",\n      \"transactionCode\": \"S\",\n      \"transactionPrice\": 655.81\n    },\n    {\n      \"name\": \"Baglino Andrew D\",\n      \"share\": 20614,\n      \"change\": 1000,\n      \"filingDate\": \"2021-03-31\",\n      \"transactionDate\": \"2021-03-29\",\n      \"transactionCode\": \"M\",\n      \"transactionPrice\": 41.57\n    },\n    {\n      \"name\": \"Baglino Andrew D\",\n      \"share\": 19114,\n      \"change\": -1500,\n      \"filingDate\": \"2021-03-31\",\n      \"transactionDate\": \"2021-03-29\",\n      \"transactionCode\": \"S\",\n      \"transactionPrice\": 615.75\n    }\n  ],\n  \"symbol\": \"TSLA\"\n}"
  suggestedFilename: "insider-transactions"
---

# Insider Transactions

## 源URL

https://finnhub.io/docs/api/insider-transactions

## 描述

Company insider transactions data sourced from Form 3,4,5, SEDI and relevant companies' filings. This endpoint covers US, UK, Canada, Australia, India, and all major EU markets. Limit to 100 transactions per API call.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/insider-transactions?symbol=TSLA&limit=20`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. Leave this param blank to get the latest transactions. |
| `from` | string | 否 | - | From date: 2020-03-15. |
| `to` | string | 否 | - | To date: 2020-03-16. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.insiderTransactions('AAPL', (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_insider_transactions('AAPL', '2021-01-01', '2021-03-01'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.InsiderTransactions(context.Background()).Symbol("AAPL").From("2021-01-01").To("2021-07-30").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->insiderTransactions("AAPL", "2021-01-01", "2021-03-01"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.insider_transactions('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.insiderTransactions("AAPL", "2021-01-01", "2021-07-07"))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "name": "Kirkhorn Zachary",
      "share": 57234,
      "change": -1250,
      "filingDate": "2021-03-19",
      "transactionDate": "2021-03-17",
      "transactionCode": "S",
      "transactionPrice": 655.81
    },
    {
      "name": "Baglino Andrew D",
      "share": 20614,
      "change": 1000,
      "filingDate": "2021-03-31",
      "transactionDate": "2021-03-29",
      "transactionCode": "M",
      "transactionPrice": 41.57
    },
    {
      "name": "Baglino Andrew D",
      "share": 19114,
      "change": -1500,
      "filingDate": "2021-03-31",
      "transactionDate": "2021-03-29",
      "transactionCode": "S",
      "transactionPrice": 615.75
    }
  ],
  "symbol": "TSLA"
}
```

## 文档正文

Company insider transactions data sourced from Form 3,4,5, SEDI and relevant companies' filings. This endpoint covers US, UK, Canada, Australia, India, and all major EU markets. Limit to 100 transactions per API call.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/insider-transactions?symbol=TSLA&limit=20`

Insider Transactions

Company insider transactions data sourced from Form 3,4,5, SEDI and relevant companies' filings. This endpoint covers US, UK, Canada, Australia, India, and all major EU markets. Limit to 100 transactions per API call.

Method: GET

Examples:

/stock/insider-transactions?symbol=TSLA&limit=20

/stock/insider-transactions?symbol=AC.TO

Arguments:

symbolREQUIRED

Symbol of the company: AAPL. Leave this param blank to get the latest transactions.

fromoptional

From date: 2020-03-15.

tooptional

To date: 2020-03-16.

Response Attributes:

data

Array of insider transactions.

change

Number of share changed from the last period. A positive value suggests a BUY transaction. A negative value suggests a SELL transaction.

filingDate

Filing date.

name

Insider's name.

share

Number of shares held after the transaction.

symbol

Symbol.

transactionCode

Transaction code. A list of codes and their meanings can be found here.

transactionDate

Transaction date.

transactionPrice

Average transaction price.

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

print(finnhub_client.stock_insider_transactions('AAPL', '2021-01-01', '2021-03-01'))

Sample response

{
  "data": [
    {
      "name": "Kirkhorn Zachary",
      "share": 57234,
      "change": -1250,
      "filingDate": "2021-03-19",
      "transactionDate": "2021-03-17",
      "transactionCode": "S",
      "transactionPrice": 655.81
    },
    {
      "name": "Baglino Andrew D",
      "share": 20614,
      "change": 1000,
      "filingDate": "2021-03-31",
      "transactionDate": "2021-03-29",
      "transactionCode": "M",
      "transactionPrice": 41.57
    },
    {
      "name": "Baglino Andrew D",
      "share": 19114,
      "change": -1500,
      "filingDate": "2021-03-31",
      "transactionDate": "2021-03-29",
      "transactionCode": "S",
      "transactionPrice": 615.75
    }
  ],
  "symbol": "TSLA"
}
