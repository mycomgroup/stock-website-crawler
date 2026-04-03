---
id: "url-647f37d0"
type: "api"
title: "USA Spending"
url: "https://finnhub.io/docs/api/stock-usa-spending"
description: "Get a list of government's spending activities from USASpending dataset for public companies. This dataset can help you identify companies that win big government contracts which is extremely important for industries such as Defense, Aerospace, and Education. Only recent data is available via the API.For historical data, you can download it here: Pre-2021, 2021, 2022, 2023, 2024"
source: ""
tags: []
crawl_time: "2026-03-18T08:35:10.557Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/usa-spending?symbol=LMT&from=2021-01-01&to=2022-12-31"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD. Filter for actionDate"}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD. Filter for actionDate"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.stockUsaSpending(\"AAPL\", \"2020-01-01\", \"2022-05-01\", (error, data, response) => {\n\tconsole.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_usa_spending(\"AAPL\", \"2021-01-01\", \"2022-06-15\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.StockUsaSpending(context.Background()).Symbol(\"AAPL\").From(\"2020-05-01\").To(\"2022-05-01\").Execute()"}
    - {"language":"PHP","code":"print_r($client->stockUsaSpending(\"AAPL\", \"2020-06-01\", \"2022-06-10\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.stock_usa_spending('AAPL', \"2020-06-01\", \"2022-06-10\"))"}
    - {"language":"Kotlin","code":"println(apiClient.stockUsaSpending(\"AAPL\", from = \"2020-06-01\", to = \"2022-06-10\"))"}
  sampleResponse: "{\n  \"data\":[\n    {\n      \"symbol\":\"AAPL\",\n      \"recipientName\":\"APPLE INC.\",\n      \"recipientParentName\":\"APPLE INC.\",\n      \"country\":\"USA\",\n      \"totalValue\":4238,\n      \"actionDate\":\"2021-11-12\",\n      \"performanceStartDate\":\"2021-11-12\",\n      \"performanceEndDate\":\"2021-12-10\",\n      \"awardingAgencyName\":\"SMITHSONIAN INSTITUTION (SI)\",\n      \"awardingSubAgencyName\":\"SMITHSONIAN INSTITUTION\",\n      \"awardingOfficeName\":\"SMITHSONIAN ASTROPHYSICAL OBSERVATORY\",\n      \"performanceCountry\":\"USA\",\n      \"performanceCity\":\"CUPERTINO\",\n      \"performanceCounty\":\"SANTA CLARA\",\n      \"performanceState\":\"CALIFORNIA\",\n      \"performanceZipCode\":\"950140642\",\n      \"performanceCongressionalDistrict\":\"17\",\n      \"awardDescription\":\"MACBOOK PRO\",\n      \"naicsCode\":\"334111\",\n      \"permalink\":\"https://www.usaspending.gov/award/CONT_AWD_33131222P00465925_3300_-NONE-_-NONE-/\"\n    }\n  ],\n  \"symbol\":\"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\":[\n    {\n      \"symbol\":\"AAPL\",\n      \"recipientName\":\"APPLE INC.\",\n      \"recipientParentName\":\"APPLE INC.\",\n      \"country\":\"USA\",\n      \"totalValue\":4238,\n      \"actionDate\":\"2021-11-12\",\n      \"performanceStartDate\":\"2021-11-12\",\n      \"performanceEndDate\":\"2021-12-10\",\n      \"awardingAgencyName\":\"SMITHSONIAN INSTITUTION (SI)\",\n      \"awardingSubAgencyName\":\"SMITHSONIAN INSTITUTION\",\n      \"awardingOfficeName\":\"SMITHSONIAN ASTROPHYSICAL OBSERVATORY\",\n      \"performanceCountry\":\"USA\",\n      \"performanceCity\":\"CUPERTINO\",\n      \"performanceCounty\":\"SANTA CLARA\",\n      \"performanceState\":\"CALIFORNIA\",\n      \"performanceZipCode\":\"950140642\",\n      \"performanceCongressionalDistrict\":\"17\",\n      \"awardDescription\":\"MACBOOK PRO\",\n      \"naicsCode\":\"334111\",\n      \"permalink\":\"https://www.usaspending.gov/award/CONT_AWD_33131222P00465925_3300_-NONE-_-NONE-/\"\n    }\n  ],\n  \"symbol\":\"AAPL\"\n}"
  rawContent: "USA Spending\n\nGet a list of government's spending activities from USASpending dataset for public companies. This dataset can help you identify companies that win big government contracts which is extremely important for industries such as Defense, Aerospace, and Education. Only recent data is available via the API.\n\nFor historical data, you can download it here: Pre-2021, 2021, 2022, 2023, 2024\n\nMethod: GET\n\nExamples:\n\n/stock/usa-spending?symbol=LMT&from=2021-01-01&to=2022-12-31\n\n/stock/usa-spending?symbol=BA&from=2021-01-01&to=2022-12-31\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol.\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD. Filter for actionDate\n\ntoREQUIRED\n\nTo date YYYY-MM-DD. Filter for actionDate\n\nResponse Attributes:\n\ndata\n\nArray of government's spending data points.\n\nactionDate\n\nPeriod.\n\nawardDescription\n\nDescription.\n\nawardingAgencyName\n\nAward agency.\n\nawardingOfficeName\n\nAward office name.\n\nawardingSubAgencyName\n\nAward sub-agency.\n\ncountry\n\nRecipient's country.\n\nnaicsCode\n\nNAICS code.\n\nperformanceCity\n\nPerformance city.\n\nperformanceCongressionalDistrict\n\nPerformance congressional district.\n\nperformanceCountry\n\nPerformance country.\n\nperformanceCounty\n\nPerformance county.\n\nperformanceEndDate\n\nPerformance end date.\n\nperformanceStartDate\n\nPerformance start date.\n\nperformanceState\n\nPerformance state.\n\nperformanceZipCode\n\nPerformance zip code.\n\npermalink\n\nPermalink.\n\nrecipientName\n\nCompany's name.\n\nrecipientParentName\n\nCompany's name.\n\nsymbol\n\nSymbol.\n\ntotalValue\n\nIncome reported by lobbying firms.\n\nsymbol\n\nSymbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_usa_spending(\"AAPL\", \"2021-01-01\", \"2022-06-15\"))\n\nSample response\n\n{\n  \"data\":[\n    {\n      \"symbol\":\"AAPL\",\n      \"recipientName\":\"APPLE INC.\",\n      \"recipientParentName\":\"APPLE INC.\",\n      \"country\":\"USA\",\n      \"totalValue\":4238,\n      \"actionDate\":\"2021-11-12\",\n      \"performanceStartDate\":\"2021-11-12\",\n      \"performanceEndDate\":\"2021-12-10\",\n      \"awardingAgencyName\":\"SMITHSONIAN INSTITUTION (SI)\",\n      \"awardingSubAgencyName\":\"SMITHSONIAN INSTITUTION\",\n      \"awardingOfficeName\":\"SMITHSONIAN ASTROPHYSICAL OBSERVATORY\",\n      \"performanceCountry\":\"USA\",\n      \"performanceCity\":\"CUPERTINO\",\n      \"performanceCounty\":\"SANTA CLARA\",\n      \"performanceState\":\"CALIFORNIA\",\n      \"performanceZipCode\":\"950140642\",\n      \"performanceCongressionalDistrict\":\"17\",\n      \"awardDescription\":\"MACBOOK PRO\",\n      \"naicsCode\":\"334111\",\n      \"permalink\":\"https://www.usaspending.gov/award/CONT_AWD_33131222P00465925_3300_-NONE-_-NONE-/\"\n    }\n  ],\n  \"symbol\":\"AAPL\"\n}"
  suggestedFilename: "stock-usa-spending"
---

# USA Spending

## 源URL

https://finnhub.io/docs/api/stock-usa-spending

## 描述

Get a list of government's spending activities from USASpending dataset for public companies. This dataset can help you identify companies that win big government contracts which is extremely important for industries such as Defense, Aerospace, and Education. Only recent data is available via the API.For historical data, you can download it here: Pre-2021, 2021, 2022, 2023, 2024

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/usa-spending?symbol=LMT&from=2021-01-01&to=2022-12-31`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol. |
| `from` | string | 是 | - | From date YYYY-MM-DD. Filter for actionDate |
| `to` | string | 是 | - | To date YYYY-MM-DD. Filter for actionDate |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.stockUsaSpending("AAPL", "2020-01-01", "2022-05-01", (error, data, response) => {
	console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_usa_spending("AAPL", "2021-01-01", "2022-06-15"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.StockUsaSpending(context.Background()).Symbol("AAPL").From("2020-05-01").To("2022-05-01").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->stockUsaSpending("AAPL", "2020-06-01", "2022-06-10"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.stock_usa_spending('AAPL', "2020-06-01", "2022-06-10"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.stockUsaSpending("AAPL", from = "2020-06-01", to = "2022-06-10"))
```

### 示例 7 (json)

```json
{
  "data":[
    {
      "symbol":"AAPL",
      "recipientName":"APPLE INC.",
      "recipientParentName":"APPLE INC.",
      "country":"USA",
      "totalValue":4238,
      "actionDate":"2021-11-12",
      "performanceStartDate":"2021-11-12",
      "performanceEndDate":"2021-12-10",
      "awardingAgencyName":"SMITHSONIAN INSTITUTION (SI)",
      "awardingSubAgencyName":"SMITHSONIAN INSTITUTION",
      "awardingOfficeName":"SMITHSONIAN ASTROPHYSICAL OBSERVATORY",
      "performanceCountry":"USA",
      "performanceCity":"CUPERTINO",
      "performanceCounty":"SANTA CLARA",
      "performanceState":"CALIFORNIA",
      "performanceZipCode":"950140642",
      "performanceCongressionalDistrict":"17",
      "awardDescription":"MACBOOK PRO",
      "naicsCode":"334111",
      "permalink":"https://www.usaspending.gov/award/CONT_AWD_33131222P00465925_3300_-NONE-_-NONE-/"
    }
  ],
  "symbol":"AAPL"
}
```

## 文档正文

Get a list of government's spending activities from USASpending dataset for public companies. This dataset can help you identify companies that win big government contracts which is extremely important for industries such as Defense, Aerospace, and Education. Only recent data is available via the API.For historical data, you can download it here: Pre-2021, 2021, 2022, 2023, 2024

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/usa-spending?symbol=LMT&from=2021-01-01&to=2022-12-31`

USA Spending

Get a list of government's spending activities from USASpending dataset for public companies. This dataset can help you identify companies that win big government contracts which is extremely important for industries such as Defense, Aerospace, and Education. Only recent data is available via the API.

For historical data, you can download it here: Pre-2021, 2021, 2022, 2023, 2024

Method: GET

Examples:

/stock/usa-spending?symbol=LMT&from=2021-01-01&to=2022-12-31

/stock/usa-spending?symbol=BA&from=2021-01-01&to=2022-12-31

Arguments:

symbolREQUIRED

Symbol.

fromREQUIRED

From date YYYY-MM-DD. Filter for actionDate

toREQUIRED

To date YYYY-MM-DD. Filter for actionDate

Response Attributes:

data

Array of government's spending data points.

actionDate

Period.

awardDescription

Description.

awardingAgencyName

Award agency.

awardingOfficeName

Award office name.

awardingSubAgencyName

Award sub-agency.

country

Recipient's country.

naicsCode

NAICS code.

performanceCity

Performance city.

performanceCongressionalDistrict

Performance congressional district.

performanceCountry

Performance country.

performanceCounty

Performance county.

performanceEndDate

Performance end date.

performanceStartDate

Performance start date.

performanceState

Performance state.

performanceZipCode

Performance zip code.

permalink

Permalink.

recipientName

Company's name.

recipientParentName

Company's name.

symbol

Symbol.

totalValue

Income reported by lobbying firms.

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

print(finnhub_client.stock_usa_spending("AAPL", "2021-01-01", "2022-06-15"))

Sample response

{
  "data":[
    {
      "symbol":"AAPL",
      "recipientName":"APPLE INC.",
      "recipientParentName":"APPLE INC.",
      "country":"USA",
      "totalValue":4238,
      "actionDate":"2021-11-12",
      "performanceStartDate":"2021-11-12",
      "performanceEndDate":"2021-12-10",
      "awardingAgencyName":"SMITHSONIAN INSTITUTION (SI)",
      "awardingSubAgencyName":"SMITHSONIAN INSTITUTION",
      "awardingOfficeName":"SMITHSONIAN ASTROPHYSICAL OBSERVATORY",
      "performanceCountry":"USA",
      "performanceCity":"CUPERTINO",
      "performanceCounty":"SANTA CLARA",
      "performanceState":"CALIFORNIA",
      "performanceZipCode":"950140642",
      "performanceCongressionalDistrict":"17",
      "awardDescription":"MACBOOK PRO",
      "naicsCode":"334111",
      "permalink":"https://www.usaspending.gov/award/CONT_AWD_33131222P00465925_3300_-NONE-_-NONE-/"
    }
  ],
  "symbol":"AAPL"
}
