---
id: "url-8030c4b"
type: "api"
title: "Basic Financials"
url: "https://finnhub.io/docs/api/financials"
description: "Get standardized balance sheet, income statement and cash flow for global companies going back 30+ years. Data is sourced from original filings most of which made available through SEC Filings and International Filings endpoints.Set preliminary param to true for faster updates for US companies.Wondering why our standardized data is different from Bloomberg, Reuters, Factset, S&P or Yahoo Finance ? Check out our FAQ page to learn more"
source: ""
tags: []
crawl_time: "2026-03-18T03:14:02.862Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/metric?symbol=AAPL&metric=all"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol of the company: AAPL."}
    - {"name":"statement","in":"query","required":true,"type":"string","description":"Statement can take 1 of these values bs, ic, cf for Balance Sheet, Income Statement, Cash Flow respectively."}
    - {"name":"freq","in":"query","required":true,"type":"string","description":"Frequency can take 1 of these values annual, quarterly, ttm, ytd.  TTM (Trailing Twelve Months) option is available for Income Statement and Cash Flow. YTD (Year To Date) option is only available for Cash Flow."}
    - {"name":"preliminary","in":"query","required":false,"type":"string","description":"If set to true, it will return Preliminary financial statements for the latest period which are usually available within an hour of the earnings announcement if finalized data is not available yet. This preliminary data is currently available for US companies. You will see \"preliminary\": true in the data if that period is using preliminary data."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.financials(\"AAPL\", \"ic\", \"annual\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.financials('AAPL', 'bs', 'annual'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.Financials(context.Background()).Symbol(\"AAPL\").Statement(\"bs\").Freq(\"annual\").Execute()"}
    - {"language":"PHP","code":"print_r($client->financials(\"AAPL\", \"bs\", \"annual\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.financials('AAPL', 'bs', 'annual'))"}
    - {"language":"Kotlin","code":"println(apiClient.financials(\"AAPL\", \"bs\", \"annual\"))"}
  sampleResponse: "{\n  \"financials\": [\n    {\n      \"costOfGoodsSold\": 161782,\n      \"ebit\": 63930,\n      \"grossIncome\": 98392,\n      \"interestExpense\": 3576,\n      \"netIncome\": 55256,\n      \"netIncomeAfterTaxes\": 55256,\n      \"period\": \"2019-09-28\",\n      \"pretaxIncome\": 65737,\n      \"provisionforIncomeTaxes\": 10481,\n      \"researchDevelopment\": 16217,\n      \"revenue\": 260174,\n      \"sgaExpense\": 18245,\n      \"totalOperatingExpense\": 34462,\n      \"year\": 2019\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"financials\": [\n    {\n      \"costOfGoodsSold\": 161782,\n      \"ebit\": 63930,\n      \"grossIncome\": 98392,\n      \"interestExpense\": 3576,\n      \"netIncome\": 55256,\n      \"netIncomeAfterTaxes\": 55256,\n      \"period\": \"2019-09-28\",\n      \"pretaxIncome\": 65737,\n      \"provisionforIncomeTaxes\": 10481,\n      \"researchDevelopment\": 16217,\n      \"revenue\": 260174,\n      \"sgaExpense\": 18245,\n      \"totalOperatingExpense\": 34462,\n      \"year\": 2019\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: "Basic Financials\n\nGet company basic financials such as margin, P/E ratio, 52-week high/low etc.\n\nMethod: GET\n\nExamples:\n\n/stock/metric?symbol=AAPL&metric=all\n\nArguments:\n\nsymbolREQUIRED\n\nSymbol of the company: AAPL.\n\nmetricREQUIRED\n\nMetric type. Can be 1 of the following values all\n\nResponse Attributes:\n\nmetric\n\nMap key-value pair of key ratios and metrics.\n\nmetricType\n\nMetric type.\n\nseries\n\nMap key-value pair of time-series ratios.\n\nsymbol\n\nSymbol of the company.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_basic_financials('AAPL', 'all'))\n\nSample response\n\n{\n   \"series\": {\n    \"annual\": {\n      \"currentRatio\": [\n        {\n          \"period\": \"2019-09-28\",\n          \"v\": 1.5401\n        },\n        {\n          \"period\": \"2018-09-29\",\n          \"v\": 1.1329\n        }\n      ],\n      \"salesPerShare\": [\n        {\n          \"period\": \"2019-09-28\",\n          \"v\": 55.9645\n        },\n        {\n          \"period\": \"2018-09-29\",\n          \"v\": 53.1178\n        }\n      ],\n      \"netMargin\": [\n        {\n          \"period\": \"2019-09-28\",\n          \"v\": 0.2124\n        },\n        {\n          \"period\": \"2018-09-29\",\n          \"v\": 0.2241\n        }\n      ]\n    }\n  },\n  \"metric\": {\n    \"10DayAverageTradingVolume\": 32.50147,\n    \"52WeekHigh\": 310.43,\n    \"52WeekLow\": 149.22,\n    \"52WeekLowDate\": \"2019-01-14\",\n    \"52WeekPriceReturnDaily\": 101.96334,\n    \"beta\": 1.2989,\n  },\n  \"metricType\": \"all\",\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "financials"
---

# Basic Financials

## 源URL

https://finnhub.io/docs/api/financials

## 描述

Get standardized balance sheet, income statement and cash flow for global companies going back 30+ years. Data is sourced from original filings most of which made available through SEC Filings and International Filings endpoints.Set preliminary param to true for faster updates for US companies.Wondering why our standardized data is different from Bloomberg, Reuters, Factset, S&P or Yahoo Finance ? Check out our FAQ page to learn more

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/metric?symbol=AAPL&metric=all`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol of the company: AAPL. |
| `statement` | string | 是 | - | Statement can take 1 of these values bs, ic, cf for Balance Sheet, Income Statement, Cash Flow respectively. |
| `freq` | string | 是 | - | Frequency can take 1 of these values annual, quarterly, ttm, ytd.  TTM (Trailing Twelve Months) option is available for Income Statement and Cash Flow. YTD (Year To Date) option is only available for Cash Flow. |
| `preliminary` | string | 否 | - | If set to true, it will return Preliminary financial statements for the latest period which are usually available within an hour of the earnings announcement if finalized data is not available yet. This preliminary data is currently available for US companies. You will see "preliminary": true in the data if that period is using preliminary data. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.financials("AAPL", "ic", "annual", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.financials('AAPL', 'bs', 'annual'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.Financials(context.Background()).Symbol("AAPL").Statement("bs").Freq("annual").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->financials("AAPL", "bs", "annual"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.financials('AAPL', 'bs', 'annual'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.financials("AAPL", "bs", "annual"))
```

### 示例 7 (json)

```json
{
  "financials": [
    {
      "costOfGoodsSold": 161782,
      "ebit": 63930,
      "grossIncome": 98392,
      "interestExpense": 3576,
      "netIncome": 55256,
      "netIncomeAfterTaxes": 55256,
      "period": "2019-09-28",
      "pretaxIncome": 65737,
      "provisionforIncomeTaxes": 10481,
      "researchDevelopment": 16217,
      "revenue": 260174,
      "sgaExpense": 18245,
      "totalOperatingExpense": 34462,
      "year": 2019
    }
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Get standardized balance sheet, income statement and cash flow for global companies going back 30+ years. Data is sourced from original filings most of which made available through SEC Filings and International Filings endpoints.Set preliminary param to true for faster updates for US companies.Wondering why our standardized data is different from Bloomberg, Reuters, Factset, S&P or Yahoo Finance ? Check out our FAQ page to learn more

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/metric?symbol=AAPL&metric=all`

Basic Financials

Get company basic financials such as margin, P/E ratio, 52-week high/low etc.

Method: GET

Examples:

/stock/metric?symbol=AAPL&metric=all

Arguments:

symbolREQUIRED

Symbol of the company: AAPL.

metricREQUIRED

Metric type. Can be 1 of the following values all

Response Attributes:

metric

Map key-value pair of key ratios and metrics.

metricType

Metric type.

series

Map key-value pair of time-series ratios.

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

print(finnhub_client.company_basic_financials('AAPL', 'all'))

Sample response

{
   "series": {
    "annual": {
      "currentRatio": [
        {
          "period": "2019-09-28",
          "v": 1.5401
        },
        {
          "period": "2018-09-29",
          "v": 1.1329
        }
      ],
      "salesPerShare": [
        {
          "period": "2019-09-28",
          "v": 55.9645
        },
        {
          "period": "2018-09-29",
          "v": 53.1178
        }
      ],
      "netMargin": [
        {
          "period": "2019-09-28",
          "v": 0.2124
        },
        {
          "period": "2018-09-29",
          "v": 0.2241
        }
      ]
    }
  },
  "metric": {
    "10DayAverageTradingVolume": 32.50147,
    "52WeekHigh": 310.43,
    "52WeekLow": 149.22,
    "52WeekLowDate": "2019-01-14",
    "52WeekPriceReturnDaily": 101.96334,
    "beta": 1.2989,
  },
  "metricType": "all",
  "symbol": "AAPL"
}
