---
id: "url-2b36c5b2"
type: "api"
title: "stock-lobbying"
url: "https://finnhub.io/docs/api/stock-lobbying"
description: "Get a list of reported lobbying activities in the Senate and the House."
source: ""
tags: []
crawl_time: "2026-03-18T06:59:01.497Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/stock/lobbying"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.stockLobbying(\"AAPL\", \"2020-01-01\", \"2022-05-01\", (error, data, response) => {\n\tconsole.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_lobbying(\"AAPL\", \"2021-01-01\", \"2022-06-15\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.StockLobbying(context.Background()).Symbol(\"AAPL\").From(\"2020-05-01\").To(\"2022-05-01\").Execute()"}
    - {"language":"PHP","code":"print_r($client->stockLobbying(\"AAPL\", \"2020-06-01\", \"2022-06-10\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.stock_lobbying('AAPL', \"2020-06-01\", \"2022-06-10\"))"}
    - {"language":"Kotlin","code":"println(apiClient.stockLobbying(\"AAPL\", from = \"2020-06-01\", to = \"2022-06-10\"))"}
  sampleResponse: "{\n  \"data\":[\n    {\n      \"symbol\":\"AAPL\",\n      \"name\":\"APPLE, INC.\",\n      \"description\":\"Hardware and software maunfacturer\",\n      \"country\":\"US\",\n      \"uuid\":\"db75bb6f-162a-433a-a997-a679eb4c6af6\",\n      \"year\":2020,\n      \"period\":\"fourth_quarter\",\n      \"type\":\"Q4\",\n      \"documentUrl\":\"https://lda.senate.gov/filings/public/filing/db75bb6f-162a-433a-a997-a679eb4c6af6/print/\",\n      \"income\":40000,\n      \"expenses\":null,\n      \"postedName\":\"\",\n      \"dtPosted\":\"\",\n      \"clientId\":\"173094\",\n      \"registrantId\":\"86196\",\n      \"senateId\":\"86196-173094\",\n      \"houseRegistrantId\":\"36548\"\n    },\n    {\n      \"symbol\":\"AAPL\",\n      \"name\":\"APPLE INC\",\n      \"description\":\"\",\n      \"country\":\"US\",\n      \"uuid\":\"cad6db2f-c3ca-4b9d-bc24-4c56fc7eaadb\",\n      \"year\":2020,\n      \"period\":\"fourth_quarter\",\n      \"type\":\"Q4\",\n      \"documentUrl\":\"https://lda.senate.gov/filings/public/filing/cad6db2f-c3ca-4b9d-bc24-4c56fc7eaadb/print/\",\n      \"income\":null,\n      \"expenses\":1450000,\n      \"postedName\":\"\",\n      \"dtPosted\":\"\",\n      \"clientId\":\"103979\",\n      \"registrantId\":\"4152\",\n      \"senateId\":\"4152-103979\",\n      \"houseRegistrantId\":\"31450\"\n    }\n  ],\n  \"symbol\":\"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\":[\n    {\n      \"symbol\":\"AAPL\",\n      \"name\":\"APPLE, INC.\",\n      \"description\":\"Hardware and software maunfacturer\",\n      \"country\":\"US\",\n      \"uuid\":\"db75bb6f-162a-433a-a997-a679eb4c6af6\",\n      \"year\":2020,\n      \"period\":\"fourth_quarter\",\n      \"type\":\"Q4\",\n      \"documentUrl\":\"https://lda.senate.gov/filings/public/filing/db75bb6f-162a-433a-a997-a679eb4c6af6/print/\",\n      \"income\":40000,\n      \"expenses\":null,\n      \"postedName\":\"\",\n      \"dtPosted\":\"\",\n      \"clientId\":\"173094\",\n      \"registrantId\":\"86196\",\n      \"senateId\":\"86196-173094\",\n      \"houseRegistrantId\":\"36548\"\n    },\n    {\n      \"symbol\":\"AAPL\",\n      \"name\":\"APPLE INC\",\n      \"description\":\"\",\n      \"country\":\"US\",\n      \"uuid\":\"cad6db2f-c3ca-4b9d-bc24-4c56fc7eaadb\",\n      \"year\":2020,\n      \"period\":\"fourth_quarter\",\n      \"type\":\"Q4\",\n      \"documentUrl\":\"https://lda.senate.gov/filings/public/filing/cad6db2f-c3ca-4b9d-bc24-4c56fc7eaadb/print/\",\n      \"income\":null,\n      \"expenses\":1450000,\n      \"postedName\":\"\",\n      \"dtPosted\":\"\",\n      \"clientId\":\"103979\",\n      \"registrantId\":\"4152\",\n      \"senateId\":\"4152-103979\",\n      \"houseRegistrantId\":\"31450\"\n    }\n  ],\n  \"symbol\":\"AAPL\"\n}"
  rawContent: ""
  suggestedFilename: "stock-lobbying"
---

# stock-lobbying

## 源URL

https://finnhub.io/docs/api/stock-lobbying

## 描述

Get a list of reported lobbying activities in the Senate and the House.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/stock/lobbying`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Symbol. |
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.stockLobbying("AAPL", "2020-01-01", "2022-05-01", (error, data, response) => {
	console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_lobbying("AAPL", "2021-01-01", "2022-06-15"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.StockLobbying(context.Background()).Symbol("AAPL").From("2020-05-01").To("2022-05-01").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->stockLobbying("AAPL", "2020-06-01", "2022-06-10"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.stock_lobbying('AAPL', "2020-06-01", "2022-06-10"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.stockLobbying("AAPL", from = "2020-06-01", to = "2022-06-10"))
```

### 示例 7 (json)

```json
{
  "data":[
    {
      "symbol":"AAPL",
      "name":"APPLE, INC.",
      "description":"Hardware and software maunfacturer",
      "country":"US",
      "uuid":"db75bb6f-162a-433a-a997-a679eb4c6af6",
      "year":2020,
      "period":"fourth_quarter",
      "type":"Q4",
      "documentUrl":"https://lda.senate.gov/filings/public/filing/db75bb6f-162a-433a-a997-a679eb4c6af6/print/",
      "income":40000,
      "expenses":null,
      "postedName":"",
      "dtPosted":"",
      "clientId":"173094",
      "registrantId":"86196",
      "senateId":"86196-173094",
      "houseRegistrantId":"36548"
    },
    {
      "symbol":"AAPL",
      "name":"APPLE INC",
      "description":"",
      "country":"US",
      "uuid":"cad6db2f-c3ca-4b9d-bc24-4c56fc7eaadb",
      "year":2020,
      "period":"fourth_quarter",
      "type":"Q4",
      "documentUrl":"https://lda.senate.gov/filings/public/filing/cad6db2f-c3ca-4b9d-bc24-4c56fc7eaadb/print/",
      "income":null,
      "expenses":1450000,
      "postedName":"",
      "dtPosted":"",
      "clientId":"103979",
      "registrantId":"4152",
      "senateId":"4152-103979",
      "houseRegistrantId":"31450"
    }
  ],
  "symbol":"AAPL"
}
```

## 文档正文

Get a list of reported lobbying activities in the Senate and the House.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/stock/lobbying`
