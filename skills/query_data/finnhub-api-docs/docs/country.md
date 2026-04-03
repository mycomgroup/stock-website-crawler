---
id: "url-e386f35"
type: "api"
title: "Country Metadata"
url: "https://finnhub.io/docs/api/country"
description: "List all countries and metadata."
source: ""
tags: []
crawl_time: "2026-03-18T03:12:53.223Z"
metadata:
  requestMethod: "GET"
  endpoint: "/country"
  parameters: []
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.country((error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.country())"}
    - {"language":"Go","code":"res, _, err := finnhubClient.Country(context.Background()).Execute()"}
    - {"language":"PHP","code":"print_r($client->country());"}
    - {"language":"Ruby","code":"puts(finnhub_client.country())"}
    - {"language":"Kotlin","code":"println(apiClient.country())"}
  sampleResponse: "[\n  {\n    \"code2\": \"US\",\n    \"code3\": \"USA\",\n    \"codeNo\": \"840\",\n    \"country\": \"United States\",\n    \"countryRiskPremium\": 0,\n    \"currency\": \"US Dollar\",\n    \"currencyCode\": \"USD\",\n    \"defaultSpread\": 0,\n    \"equityRiskPremium\": 5,\n    \"rating\": \"Aaa\",\n    \"region\": \"Americas\",\n    \"subRegion\": \"Northern America\"\n  },\n  {\n    \"code2\": \"GB\",\n    \"code3\": \"GBR\",\n    \"codeNo\": \"826\",\n    \"country\": \"United Kingdom of Great Britain and Northern Ireland\",\n    \"countryRiskPremium\": 0.91,\n    \"currency\": \"Sterling\",\n    \"currencyCode\": \"GBP\",\n    \"defaultSpread\": 0.64,\n    \"equityRiskPremium\": 5.91,\n    \"rating\": \"Aa3\",\n    \"region\": \"Europe\",\n    \"subRegion\": \"Northern Europe\"\n  }\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"code2\": \"US\",\n    \"code3\": \"USA\",\n    \"codeNo\": \"840\",\n    \"country\": \"United States\",\n    \"countryRiskPremium\": 0,\n    \"currency\": \"US Dollar\",\n    \"currencyCode\": \"USD\",\n    \"defaultSpread\": 0,\n    \"equityRiskPremium\": 5,\n    \"rating\": \"Aaa\",\n    \"region\": \"Americas\",\n    \"subRegion\": \"Northern America\"\n  },\n  {\n    \"code2\": \"GB\",\n    \"code3\": \"GBR\",\n    \"codeNo\": \"826\",\n    \"country\": \"United Kingdom of Great Britain and Northern Ireland\",\n    \"countryRiskPremium\": 0.91,\n    \"currency\": \"Sterling\",\n    \"currencyCode\": \"GBP\",\n    \"defaultSpread\": 0.64,\n    \"equityRiskPremium\": 5.91,\n    \"rating\": \"Aa3\",\n    \"region\": \"Europe\",\n    \"subRegion\": \"Northern Europe\"\n  }\n]"
  rawContent: "Country Metadata\n\nList all countries and metadata.\n\nMethod: GET\n\nExamples:\n\n/country\n\nArguments:\n\nResponse Attributes:\n\ncode2\n\nAlpha 2 code\n\ncode3\n\nAlpha 3 code\n\ncodeNo\n\nUN code\n\ncountry\n\nCountry name\n\ncountryRiskPremium\n\nCountry risk premium\n\ncurrency\n\nCurrency name\n\ncurrencyCode\n\nCurrency code\n\ndefaultSpread\n\nDefault spread\n\nequityRiskPremium\n\nEquity risk premium\n\nrating\n\nMoody's credit risk rating.\n\nregion\n\nRegion\n\nsubRegion\n\nSub-Region\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.country())\n\nSample response\n\n[\n  {\n    \"code2\": \"US\",\n    \"code3\": \"USA\",\n    \"codeNo\": \"840\",\n    \"country\": \"United States\",\n    \"countryRiskPremium\": 0,\n    \"currency\": \"US Dollar\",\n    \"currencyCode\": \"USD\",\n    \"defaultSpread\": 0,\n    \"equityRiskPremium\": 5,\n    \"rating\": \"Aaa\",\n    \"region\": \"Americas\",\n    \"subRegion\": \"Northern America\"\n  },\n  {\n    \"code2\": \"GB\",\n    \"code3\": \"GBR\",\n    \"codeNo\": \"826\",\n    \"country\": \"United Kingdom of Great Britain and Northern Ireland\",\n    \"countryRiskPremium\": 0.91,\n    \"currency\": \"Sterling\",\n    \"currencyCode\": \"GBP\",\n    \"defaultSpread\": 0.64,\n    \"equityRiskPremium\": 5.91,\n    \"rating\": \"Aa3\",\n    \"region\": \"Europe\",\n    \"subRegion\": \"Northern Europe\"\n  }\n]"
  suggestedFilename: "country"
---

# Country Metadata

## 源URL

https://finnhub.io/docs/api/country

## 描述

List all countries and metadata.

## API 端点

**Method**: `GET`
**Endpoint**: `/country`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.country((error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.country())
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.Country(context.Background()).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->country());
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.country())
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.country())
```

### 示例 7 (json)

```json
[
  {
    "code2": "US",
    "code3": "USA",
    "codeNo": "840",
    "country": "United States",
    "countryRiskPremium": 0,
    "currency": "US Dollar",
    "currencyCode": "USD",
    "defaultSpread": 0,
    "equityRiskPremium": 5,
    "rating": "Aaa",
    "region": "Americas",
    "subRegion": "Northern America"
  },
  {
    "code2": "GB",
    "code3": "GBR",
    "codeNo": "826",
    "country": "United Kingdom of Great Britain and Northern Ireland",
    "countryRiskPremium": 0.91,
    "currency": "Sterling",
    "currencyCode": "GBP",
    "defaultSpread": 0.64,
    "equityRiskPremium": 5.91,
    "rating": "Aa3",
    "region": "Europe",
    "subRegion": "Northern Europe"
  }
]
```

## 文档正文

List all countries and metadata.

## API 端点

**Method:** `GET`
**Endpoint:** `/country`

Country Metadata

List all countries and metadata.

Method: GET

Examples:

/country

Arguments:

Response Attributes:

code2

Alpha 2 code

code3

Alpha 3 code

codeNo

UN code

country

Country name

countryRiskPremium

Country risk premium

currency

Currency name

currencyCode

Currency code

defaultSpread

Default spread

equityRiskPremium

Equity risk premium

rating

Moody's credit risk rating.

region

Region

subRegion

Sub-Region

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

print(finnhub_client.country())

Sample response

[
  {
    "code2": "US",
    "code3": "USA",
    "codeNo": "840",
    "country": "United States",
    "countryRiskPremium": 0,
    "currency": "US Dollar",
    "currencyCode": "USD",
    "defaultSpread": 0,
    "equityRiskPremium": 5,
    "rating": "Aaa",
    "region": "Americas",
    "subRegion": "Northern America"
  },
  {
    "code2": "GB",
    "code3": "GBR",
    "codeNo": "826",
    "country": "United Kingdom of Great Britain and Northern Ireland",
    "countryRiskPremium": 0.91,
    "currency": "Sterling",
    "currencyCode": "GBP",
    "defaultSpread": 0.64,
    "equityRiskPremium": 5.91,
    "rating": "Aa3",
    "region": "Europe",
    "subRegion": "Northern Europe"
  }
]
