---
id: "url-2d2f6d8d"
type: "api"
title: "Company Executive Premium"
url: "https://finnhub.io/docs/api/company-executive"
description: "Get a list of company's executives and members of the Board."
source: ""
tags: []
crawl_time: "2026-03-18T08:12:24.520Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/executive?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.companyExecutive('AAPL', (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.company_executive('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CompanyExecutive(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->companyExecutive(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.company_executive('AAPL'))"}
    - {"language":"Kotlin","code":"println(apiClient.companyExecutive(\"AAPL\"))"}
  sampleResponse: "{\n  \"executive\": [\n    {\n      \"age\": 56,\n      \"compensation\": 25209637,\n      \"currency\": \"USD\",\n      \"name\": \"Luca Maestri\",\n      \"position\": \"Senior Vice President and Chief Financial Officer\",\n      \"sex\": \"male\",\n      \"since\": \"2014\"\n    },\n    {\n      \"age\": 59,\n      \"compensation\": 11555466,\n      \"currency\": \"USD\",\n      \"name\": \"Mr. Timothy Cook\",\n      \"position\": \"Director and Chief Executive Officer\",\n      \"sex\": \"male\",\n      \"since\": \"2011\"\n    }\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"executive\": [\n    {\n      \"age\": 56,\n      \"compensation\": 25209637,\n      \"currency\": \"USD\",\n      \"name\": \"Luca Maestri\",\n      \"position\": \"Senior Vice President and Chief Financial Officer\",\n      \"sex\": \"male\",\n      \"since\": \"2014\"\n    },\n    {\n      \"age\": 59,\n      \"compensation\": 11555466,\n      \"currency\": \"USD\",\n      \"name\": \"Mr. Timothy Cook\",\n      \"position\": \"Director and Chief Executive Officer\",\n      \"sex\": \"male\",\n      \"since\": \"2011\"\n    }\n  ]\n}"
  rawContent: "Company Executive Premium\n\nGet a list of company's executives and members of the Board.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/executive?symbol=AAPL\n\n/stock/executive?symbol=AMZN\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nResponse Attributes:\n\nexecutive\n\nArray of company's executives and members of the Board.\n\nage\n\nAge\n\ncompensation\n\nTotal compensation\n\ncurrency\n\nCompensation currency\n\nname\n\nExecutive name\n\nsex\n\nSex\n\nsince\n\nYear first appointed as executive/director of the company\n\ntitle\n\nTitle\n\nsymbol\n\nCompany symbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_executive('AAPL'))\n\nSample response\n\n{\n  \"executive\": [\n    {\n      \"age\": 56,\n      \"compensation\": 25209637,\n      \"currency\": \"USD\",\n      \"name\": \"Luca Maestri\",\n      \"position\": \"Senior Vice President and Chief Financial Officer\",\n      \"sex\": \"male\",\n      \"since\": \"2014\"\n    },\n    {\n      \"age\": 59,\n      \"compensation\": 11555466,\n      \"currency\": \"USD\",\n      \"name\": \"Mr. Timothy Cook\",\n      \"position\": \"Director and Chief Executive Officer\",\n      \"sex\": \"male\",\n      \"since\": \"2011\"\n    }\n  ]\n}"
  suggestedFilename: "company-executive"
---

# Company Executive Premium

## 源URL

https://finnhub.io/docs/api/company-executive

## 描述

Get a list of company's executives and members of the Board.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/executive?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.companyExecutive('AAPL', (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.company_executive('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CompanyExecutive(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->companyExecutive("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.company_executive('AAPL'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.companyExecutive("AAPL"))
```

### 示例 7 (json)

```json
{
  "executive": [
    {
      "age": 56,
      "compensation": 25209637,
      "currency": "USD",
      "name": "Luca Maestri",
      "position": "Senior Vice President and Chief Financial Officer",
      "sex": "male",
      "since": "2014"
    },
    {
      "age": 59,
      "compensation": 11555466,
      "currency": "USD",
      "name": "Mr. Timothy Cook",
      "position": "Director and Chief Executive Officer",
      "sex": "male",
      "since": "2011"
    }
  ]
}
```

## 文档正文

Get a list of company's executives and members of the Board.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/executive?symbol=AAPL`

Company Executive Premium

Get a list of company's executives and members of the Board.

Method: GET

Premium: Premium Access Required

Examples:

/stock/executive?symbol=AAPL

/stock/executive?symbol=AMZN

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

Response Attributes:

executive

Array of company's executives and members of the Board.

age

Age

compensation

Total compensation

currency

Compensation currency

name

Executive name

sex

Sex

since

Year first appointed as executive/director of the company

title

Title

symbol

Company symbol.

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

print(finnhub_client.company_executive('AAPL'))

Sample response

{
  "executive": [
    {
      "age": 56,
      "compensation": 25209637,
      "currency": "USD",
      "name": "Luca Maestri",
      "position": "Senior Vice President and Chief Financial Officer",
      "sex": "male",
      "since": "2014"
    },
    {
      "age": 59,
      "compensation": 11555466,
      "currency": "USD",
      "name": "Mr. Timothy Cook",
      "position": "Director and Chief Executive Officer",
      "sex": "male",
      "since": "2011"
    }
  ]
}
