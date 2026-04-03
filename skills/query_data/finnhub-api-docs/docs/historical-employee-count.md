---
id: "url-50d26a88"
type: "api"
title: "Historical Employee Count Premium"
url: "https://finnhub.io/docs/api/historical-employee-count"
description: "Get historical employee count for global companies."
source: ""
tags: []
crawl_time: "2026-03-18T10:37:07.612Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/historical-employee-count?symbol=AAPL&from=2022-01-01&to=2024-05-06"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.historicalEmployeeCount(\"AAPL\", \"2020-01-01\", \"2020-05-01\", (error, data, response) => {\n\tconsole.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.historical_employee_count('AAPL', _from=\"2020-06-01\", to=\"2020-06-10\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.HistoricalEmployeeCount(context.Background()).Symbol(\"AAPL\").From(\"2020-05-01\").To(\"2020-05-01\").Execute()"}
    - {"language":"PHP","code":"print_r($client->historicalEmployeeCount(\"AAPL\", \"2020-06-01\", \"2020-06-10\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.historical_employee_count('AAPL', \"2020-06-01\", \"2020-06-10\"))"}
    - {"language":"Kotlin","code":"println(apiClient.historicalEmployeeCount(\"AAPL\", from = \"2020-06-01\", to = \"2020-06-10\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"atDate\": \"2023-09-30\",\n      \"employee\": 161000\n    },\n    {\n      \"atDate\": \"2022-09-24\",\n      \"employee\": 164000\n    },\n    {\n      \"atDate\": \"2021-09-25\",\n      \"employee\": 154000\n    },\n    {\n      \"atDate\": \"2020-09-26\",\n      \"employee\": 147000\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"atDate\": \"2023-09-30\",\n      \"employee\": 161000\n    },\n    {\n      \"atDate\": \"2022-09-24\",\n      \"employee\": 164000\n    },\n    {\n      \"atDate\": \"2021-09-25\",\n      \"employee\": 154000\n    },\n    {\n      \"atDate\": \"2020-09-26\",\n      \"employee\": 147000\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: "Historical Employee Count Premium\n\nGet historical employee count for global companies.\n\nMethod: GET\n\nPremium: Accessible with Fundamental 2 or All in One subscription.\n\nExamples:\n\n/stock/historical-employee-count?symbol=AAPL&from=2022-01-01&to=2024-05-06\n\nArguments:\n\nsymbolREQUIRED\n\nCompany symbol.\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ndata\n\nArray of market data.\n\natDate\n\nDate of the reading\n\nemployee\n\nValue\n\nsymbol\n\nSymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.historical_employee_count('AAPL', _from=\"2020-06-01\", to=\"2020-06-10\"))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"atDate\": \"2023-09-30\",\n      \"employee\": 161000\n    },\n    {\n      \"atDate\": \"2022-09-24\",\n      \"employee\": 164000\n    },\n    {\n      \"atDate\": \"2021-09-25\",\n      \"employee\": 154000\n    },\n    {\n      \"atDate\": \"2020-09-26\",\n      \"employee\": 147000\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "historical-employee-count"
---

# Historical Employee Count Premium

## 源URL

https://finnhub.io/docs/api/historical-employee-count

## 描述

Get historical employee count for global companies.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/historical-employee-count?symbol=AAPL&from=2022-01-01&to=2024-05-06`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol. |
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.historicalEmployeeCount("AAPL", "2020-01-01", "2020-05-01", (error, data, response) => {
	console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.historical_employee_count('AAPL', _from="2020-06-01", to="2020-06-10"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.HistoricalEmployeeCount(context.Background()).Symbol("AAPL").From("2020-05-01").To("2020-05-01").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->historicalEmployeeCount("AAPL", "2020-06-01", "2020-06-10"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.historical_employee_count('AAPL', "2020-06-01", "2020-06-10"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.historicalEmployeeCount("AAPL", from = "2020-06-01", to = "2020-06-10"))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "atDate": "2023-09-30",
      "employee": 161000
    },
    {
      "atDate": "2022-09-24",
      "employee": 164000
    },
    {
      "atDate": "2021-09-25",
      "employee": 154000
    },
    {
      "atDate": "2020-09-26",
      "employee": 147000
    }
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Get historical employee count for global companies.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/historical-employee-count?symbol=AAPL&from=2022-01-01&to=2024-05-06`

Historical Employee Count Premium

Get historical employee count for global companies.

Method: GET

Premium: Accessible with Fundamental 2 or All in One subscription.

Examples:

/stock/historical-employee-count?symbol=AAPL&from=2022-01-01&to=2024-05-06

Arguments:

symbolREQUIRED

Company symbol.

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

data

Array of market data.

atDate

Date of the reading

employee

Value

symbol

Symbol

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

print(finnhub_client.historical_employee_count('AAPL', _from="2020-06-01", to="2020-06-10"))

Sample response

{
  "data": [
    {
      "atDate": "2023-09-30",
      "employee": 161000
    },
    {
      "atDate": "2022-09-24",
      "employee": 164000
    },
    {
      "atDate": "2021-09-25",
      "employee": 154000
    },
    {
      "atDate": "2020-09-26",
      "employee": 147000
    }
  ],
  "symbol": "AAPL"
}
