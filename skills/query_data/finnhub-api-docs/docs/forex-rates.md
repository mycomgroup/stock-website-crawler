---
id: "url-67482877"
type: "api"
title: "Forex rates Premium"
url: "https://finnhub.io/docs/api/forex-rates"
description: "Get rates for all forex pairs. Ideal for currency conversion"
source: ""
tags: []
crawl_time: "2026-03-18T04:35:07.120Z"
metadata:
  requestMethod: "GET"
  endpoint: "/forex/rates?base=USD"
  parameters:
    - {"name":"base","in":"query","required":false,"type":"string","description":"Base currency. Default to EUR."}
    - {"name":"date","in":"query","required":false,"type":"string","description":"Date. Leave blank to get the latest data."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.forexRates({\"base\": \"USD\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.forex_rates(base='USD'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.ForexRates(context.Background()).Base(\"USD\").Execute()"}
    - {"language":"PHP","code":"print_r($client->forexRates(\"USD\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.forex_rates({base: 'USD'}))"}
    - {"language":"Kotlin","code":"println(apiClient.forexRates(base = \"USD\"))"}
  sampleResponse: "{\n  \"base\": \"USD\",\n  \"quote\": {\n    \"AED\": 3.968012,\n    \"AFN\": 82.373308,\n    \"ALL\": 124.235408,\n    \"AMD\": 520.674275,\n    \"CAD\": 1.525368,\n    \"CDF\": 1904.576741,\n    \"CHF\": 1.053259,\n    \"CNY\": 7.675235,\n    \"COP\": 4282.32676,\n    \"CRC\": 614.796995,\n    \"CUC\": 1.080304,\n    \"CUP\": 28.628067,\n    \"CVE\": 110.517004,\n    \"CZK\": 27.096737,\n    \"DJF\": 191.991344,\n    \"DKK\": 7.461229,\n    \"DOP\": 59.195018,\n    \"DZD\": 139.384021,\n    \"EGP\": 17.018597,\n    \"ERN\": 16.204913,\n    \"ETB\": 36.296767,\n    \"EUR\": 0.91,\n    \"GBP\": 0.874841,\n    \"JPY\": 114.583548,\n    \"MDL\": 19.120251,\n    \"MGA\": 4105.156776,\n    \"USD\": 1,\n  }\n}"
  curlExample: ""
  jsonExample: "{\n  \"base\": \"USD\",\n  \"quote\": {\n    \"AED\": 3.968012,\n    \"AFN\": 82.373308,\n    \"ALL\": 124.235408,\n    \"AMD\": 520.674275,\n    \"CAD\": 1.525368,\n    \"CDF\": 1904.576741,\n    \"CHF\": 1.053259,\n    \"CNY\": 7.675235,\n    \"COP\": 4282.32676,\n    \"CRC\": 614.796995,\n    \"CUC\": 1.080304,\n    \"CUP\": 28.628067,\n    \"CVE\": 110.517004,\n    \"CZK\": 27.096737,\n    \"DJF\": 191.991344,\n    \"DKK\": 7.461229,\n    \"DOP\": 59.195018,\n    \"DZD\": 139.384021,\n    \"EGP\": 17.018597,\n    \"ERN\": 16.204913,\n    \"ETB\": 36.296767,\n    \"EUR\": 0.91,\n    \"GBP\": 0.874841,\n    \"JPY\": 114.583548,\n    \"MDL\": 19.120251,\n    \"MGA\": 4105.156776,\n    \"USD\": 1,\n  }\n}"
  rawContent: "Forex rates Premium\n\nGet rates for all forex pairs. Ideal for currency conversion\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/forex/rates?base=USD\n\n/forex/rates?base=EUR&date=2022-02-10\n\nArguments:\n\nbaseoptional\n\nBase currency. Default to EUR.\n\ndateoptional\n\nDate. Leave blank to get the latest data.\n\nResponse Attributes:\n\nbase\n\nBase currency.\n\nquote\n\nA map of base/quote rates for all currency pair.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.forex_rates(base='USD'))\n\nSample response\n\n{\n  \"base\": \"USD\",\n  \"quote\": {\n    \"AED\": 3.968012,\n    \"AFN\": 82.373308,\n    \"ALL\": 124.235408,\n    \"AMD\": 520.674275,\n    \"CAD\": 1.525368,\n    \"CDF\": 1904.576741,\n    \"CHF\": 1.053259,\n    \"CNY\": 7.675235,\n    \"COP\": 4282.32676,\n    \"CRC\": 614.796995,\n    \"CUC\": 1.080304,\n    \"CUP\": 28.628067,\n    \"CVE\": 110.517004,\n    \"CZK\": 27.096737,\n    \"DJF\": 191.991344,\n    \"DKK\": 7.461229,\n    \"DOP\": 59.195018,\n    \"DZD\": 139.384021,\n    \"EGP\": 17.018597,\n    \"ERN\": 16.204913,\n    \"ETB\": 36.296767,\n    \"EUR\": 0.91,\n    \"GBP\": 0.874841,\n    \"JPY\": 114.583548,\n    \"MDL\": 19.120251,\n    \"MGA\": 4105.156776,\n    \"USD\": 1,\n  }\n}"
  suggestedFilename: "forex-rates"
---

# Forex rates Premium

## 源URL

https://finnhub.io/docs/api/forex-rates

## 描述

Get rates for all forex pairs. Ideal for currency conversion

## API 端点

**Method**: `GET`
**Endpoint**: `/forex/rates?base=USD`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `base` | string | 否 | - | Base currency. Default to EUR. |
| `date` | string | 否 | - | Date. Leave blank to get the latest data. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.forexRates({"base": "USD"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.forex_rates(base='USD'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.ForexRates(context.Background()).Base("USD").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->forexRates("USD"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.forex_rates({base: 'USD'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.forexRates(base = "USD"))
```

### 示例 7 (json)

```json
{
  "base": "USD",
  "quote": {
    "AED": 3.968012,
    "AFN": 82.373308,
    "ALL": 124.235408,
    "AMD": 520.674275,
    "CAD": 1.525368,
    "CDF": 1904.576741,
    "CHF": 1.053259,
    "CNY": 7.675235,
    "COP": 4282.32676,
    "CRC": 614.796995,
    "CUC": 1.080304,
    "CUP": 28.628067,
    "CVE": 110.517004,
    "CZK": 27.096737,
    "DJF": 191.991344,
    "DKK": 7.461229,
    "DOP": 59.195018,
    "DZD": 139.384021,
    "EGP": 17.018597,
    "ERN": 16.204913,
    "ETB": 36.296767,
    "EUR": 0.91,
    "GBP": 0.874841,
    "JPY": 114.583548,
    "MDL": 19.120251,
    "MGA": 4105.156776,
    "USD": 1,
  }
}
```

## 文档正文

Get rates for all forex pairs. Ideal for currency conversion

## API 端点

**Method:** `GET`
**Endpoint:** `/forex/rates?base=USD`

Forex rates Premium

Get rates for all forex pairs. Ideal for currency conversion

Method: GET

Premium: Premium Access Required

Examples:

/forex/rates?base=USD

/forex/rates?base=EUR&date=2022-02-10

Arguments:

baseoptional

Base currency. Default to EUR.

dateoptional

Date. Leave blank to get the latest data.

Response Attributes:

base

Base currency.

quote

A map of base/quote rates for all currency pair.

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

print(finnhub_client.forex_rates(base='USD'))

Sample response

{
  "base": "USD",
  "quote": {
    "AED": 3.968012,
    "AFN": 82.373308,
    "ALL": 124.235408,
    "AMD": 520.674275,
    "CAD": 1.525368,
    "CDF": 1904.576741,
    "CHF": 1.053259,
    "CNY": 7.675235,
    "COP": 4282.32676,
    "CRC": 614.796995,
    "CUC": 1.080304,
    "CUP": 28.628067,
    "CVE": 110.517004,
    "CZK": 27.096737,
    "DJF": 191.991344,
    "DKK": 7.461229,
    "DOP": 59.195018,
    "DZD": 139.384021,
    "EGP": 17.018597,
    "ERN": 16.204913,
    "ETB": 36.296767,
    "EUR": 0.91,
    "GBP": 0.874841,
    "JPY": 114.583548,
    "MDL": 19.120251,
    "MGA": 4105.156776,
    "USD": 1,
  }
}
