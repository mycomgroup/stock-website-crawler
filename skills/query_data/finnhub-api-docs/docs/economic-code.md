---
id: "url-283b7e3a"
type: "api"
title: "Economic Code Premium"
url: "https://finnhub.io/docs/api/economic-code"
description: "List codes of supported economic data."
source: ""
tags: []
crawl_time: "2026-03-18T06:28:01.269Z"
metadata:
  requestMethod: "GET"
  endpoint: "/economic/code"
  parameters: []
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.economicCode((error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.economic_code())"}
    - {"language":"Go","code":"res, _, err := finnhubClient.EconomicCode(context.Background()).Execute()"}
    - {"language":"PHP","code":"print_r($client->economicCode());"}
    - {"language":"Ruby","code":"puts(finnhub_client.economic_code())"}
    - {"language":"Kotlin","code":"println(apiClient.economicCode())"}
  sampleResponse: "[\n  {\n    \"code\": \"MA-USA-656880\",\n    \"country\": \"USA\",\n    \"name\": \"1-Day Repo Rate\",\n    \"unit\": \"%\"\n  },\n  {\n    \"code\": \"MA-USA-6667797870\",\n    \"country\": \"USA\",\n    \"name\": \"ISM Purchasing Managers Index\",\n    \"unit\": \"unit\"\n  }\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"code\": \"MA-USA-656880\",\n    \"country\": \"USA\",\n    \"name\": \"1-Day Repo Rate\",\n    \"unit\": \"%\"\n  },\n  {\n    \"code\": \"MA-USA-6667797870\",\n    \"country\": \"USA\",\n    \"name\": \"ISM Purchasing Managers Index\",\n    \"unit\": \"unit\"\n  }\n]"
  rawContent: "Economic Code Premium\n\nList codes of supported economic data.\n\nMethod: GET\n\nPremium: Accessible with Fundamental data or All in One subscription.\n\nExamples:\n\n/economic/code\n\nArguments:\n\nResponse Attributes:\n\ncode\n\nFinnhub economic code used to get historical data\n\ncountry\n\nCountry\n\nname\n\nIndicator name\n\nunit\n\nUnit\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.economic_code())\n\nSample response\n\n[\n  {\n    \"code\": \"MA-USA-656880\",\n    \"country\": \"USA\",\n    \"name\": \"1-Day Repo Rate\",\n    \"unit\": \"%\"\n  },\n  {\n    \"code\": \"MA-USA-6667797870\",\n    \"country\": \"USA\",\n    \"name\": \"ISM Purchasing Managers Index\",\n    \"unit\": \"unit\"\n  }\n]"
  suggestedFilename: "economic-code"
---

# Economic Code Premium

## 源URL

https://finnhub.io/docs/api/economic-code

## 描述

List codes of supported economic data.

## API 端点

**Method**: `GET`
**Endpoint**: `/economic/code`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.economicCode((error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.economic_code())
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.EconomicCode(context.Background()).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->economicCode());
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.economic_code())
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.economicCode())
```

### 示例 7 (json)

```json
[
  {
    "code": "MA-USA-656880",
    "country": "USA",
    "name": "1-Day Repo Rate",
    "unit": "%"
  },
  {
    "code": "MA-USA-6667797870",
    "country": "USA",
    "name": "ISM Purchasing Managers Index",
    "unit": "unit"
  }
]
```

## 文档正文

List codes of supported economic data.

## API 端点

**Method:** `GET`
**Endpoint:** `/economic/code`

Economic Code Premium

List codes of supported economic data.

Method: GET

Premium: Accessible with Fundamental data or All in One subscription.

Examples:

/economic/code

Arguments:

Response Attributes:

code

Finnhub economic code used to get historical data

country

Country

name

Indicator name

unit

Unit

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

print(finnhub_client.economic_code())

Sample response

[
  {
    "code": "MA-USA-656880",
    "country": "USA",
    "name": "1-Day Repo Rate",
    "unit": "%"
  },
  {
    "code": "MA-USA-6667797870",
    "country": "USA",
    "name": "ISM Purchasing Managers Index",
    "unit": "unit"
  }
]
