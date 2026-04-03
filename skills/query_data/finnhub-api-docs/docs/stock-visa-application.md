---
id: "url-2d6f123a"
type: "api"
title: "stock-visa-application"
url: "https://finnhub.io/docs/api/stock-visa-application"
description: "Get a list of H1-B and Permanent visa applications for companies from the DOL. The data is updated quarterly."
source: ""
tags: []
crawl_time: "2026-03-18T09:53:29.630Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/stock/visa-application"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD. Filter on the beginDate column."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD. Filter on the beginDate column."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.stockVisaApplication(\"AAPL\", \"2020-01-01\", \"2021-05-01\", (error, data, response) => {\n\tconsole.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_visa_application(\"AAPL\", \"2021-01-01\", \"2022-06-15\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.StockVisaApplication(context.Background()).Symbol(\"AAPL\").From(\"2020-05-01\").To(\"2021-05-01\").Execute()"}
    - {"language":"PHP","code":"print_r($client->stockVisaApplication(\"AAPL\", \"2020-06-01\", \"2021-06-10\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.stock_visa_application('AAPL', \"2020-06-01\", \"2021-06-10\"))"}
    - {"language":"Kotlin","code":"println(apiClient.stockVisaApplication(\"AAPL\", from = \"2020-06-01\", to = \"2021-06-10\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"year\": 2020,\n      \"quarter\": 1,\n      \"symbol\": \"AAPL\",\n      \"caseNumber\": \"I-200-19268-472068\",\n      \"caseStatus\": \"Certified\",\n      \"receivedDate\": \"2019-09-25\",\n      \"visaClass\": \"H-1B\",\n      \"jobTitle\": \"ASIC DESIGN VERIFICATION ENGINEER\",\n      \"socCode\": \"17-2072\",\n      \"fullTimePosition\": \"Y\",\n      \"beginDate\": \"2019-10-14\",\n      \"endDate\": \"2022-10-13\",\n      \"employerName\": \"APPLE INC.\",\n      \"worksiteAddress\": \"320 S Capital of Texas Highway\",\n      \"worksiteCity\": \"West Lake Hills\",\n      \"worksiteCounty\": \"Travis\",\n      \"worksiteState\": \"TX\",\n      \"worksitePostalCode\": \"78746\",\n      \"wageRangeFrom\": 120000,\n      \"wageRangeTo\": null,\n      \"wageUnitOfPay\": \"Year\",\n      \"wageLevel\": \"II\",\n      \"h1bDependent\": \"N\"\n    },\n    ...\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"year\": 2020,\n      \"quarter\": 1,\n      \"symbol\": \"AAPL\",\n      \"caseNumber\": \"I-200-19268-472068\",\n      \"caseStatus\": \"Certified\",\n      \"receivedDate\": \"2019-09-25\",\n      \"visaClass\": \"H-1B\",\n      \"jobTitle\": \"ASIC DESIGN VERIFICATION ENGINEER\",\n      \"socCode\": \"17-2072\",\n      \"fullTimePosition\": \"Y\",\n      \"beginDate\": \"2019-10-14\",\n      \"endDate\": \"2022-10-13\",\n      \"employerName\": \"APPLE INC.\",\n      \"worksiteAddress\": \"320 S Capital of Texas Highway\",\n      \"worksiteCity\": \"West Lake Hills\",\n      \"worksiteCounty\": \"Travis\",\n      \"worksiteState\": \"TX\",\n      \"worksitePostalCode\": \"78746\",\n      \"wageRangeFrom\": 120000,\n      \"wageRangeTo\": null,\n      \"wageUnitOfPay\": \"Year\",\n      \"wageLevel\": \"II\",\n      \"h1bDependent\": \"N\"\n    },\n    ...\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: ""
  suggestedFilename: "stock-visa-application"
---

# stock-visa-application

## 源URL

https://finnhub.io/docs/api/stock-visa-application

## 描述

Get a list of H1-B and Permanent visa applications for companies from the DOL. The data is updated quarterly.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/stock/visa-application`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol. |
| `from` | string | 是 | - | From date YYYY-MM-DD. Filter on the beginDate column. |
| `to` | string | 是 | - | To date YYYY-MM-DD. Filter on the beginDate column. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.stockVisaApplication("AAPL", "2020-01-01", "2021-05-01", (error, data, response) => {
	console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_visa_application("AAPL", "2021-01-01", "2022-06-15"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.StockVisaApplication(context.Background()).Symbol("AAPL").From("2020-05-01").To("2021-05-01").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->stockVisaApplication("AAPL", "2020-06-01", "2021-06-10"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.stock_visa_application('AAPL', "2020-06-01", "2021-06-10"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.stockVisaApplication("AAPL", from = "2020-06-01", to = "2021-06-10"))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "year": 2020,
      "quarter": 1,
      "symbol": "AAPL",
      "caseNumber": "I-200-19268-472068",
      "caseStatus": "Certified",
      "receivedDate": "2019-09-25",
      "visaClass": "H-1B",
      "jobTitle": "ASIC DESIGN VERIFICATION ENGINEER",
      "socCode": "17-2072",
      "fullTimePosition": "Y",
      "beginDate": "2019-10-14",
      "endDate": "2022-10-13",
      "employerName": "APPLE INC.",
      "worksiteAddress": "320 S Capital of Texas Highway",
      "worksiteCity": "West Lake Hills",
      "worksiteCounty": "Travis",
      "worksiteState": "TX",
      "worksitePostalCode": "78746",
      "wageRangeFrom": 120000,
      "wageRangeTo": null,
      "wageUnitOfPay": "Year",
      "wageLevel": "II",
      "h1bDependent": "N"
    },
    ...
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Get a list of H1-B and Permanent visa applications for companies from the DOL. The data is updated quarterly.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/stock/visa-application`
