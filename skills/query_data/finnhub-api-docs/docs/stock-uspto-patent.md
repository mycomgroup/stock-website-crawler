---
id: "url-6e16c0aa"
type: "api"
title: "stock-uspto-patent"
url: "https://finnhub.io/docs/api/stock-uspto-patent"
description: "List USPTO patents for companies. Limit to 250 records per API call."
source: ""
tags: []
crawl_time: "2026-03-18T08:34:59.974Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/stock/uspto-patent"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Symbol."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.stockUsptoPatent(\"NVDA\", \"2020-01-01\", \"2021-05-01\", (error, data, response) => {\n\tconsole.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_uspto_patent('NVDA', _from=\"2020-06-01\", to=\"2021-06-10\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.StockUsptoPatent(context.Background()).Symbol(\"NVDA\").From(\"2020-05-01\").To(\"2021-05-01\").Execute()"}
    - {"language":"PHP","code":"print_r($client->stockUsptoPatent(\"NVDA\", \"2020-06-01\", \"2021-06-10\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.stock_uspto_patent('NVDA', \"2020-06-01\", \"2021-06-10\"))"}
    - {"language":"Kotlin","code":"println(apiClient.stockUsptoPatent(\"NVDA\", from = \"2020-06-01\", to = \"2021-06-10\"))"}
  sampleResponse: "{\n   \"data\":[\n      {\n         \"applicationNumber\":\"17163855\",\n         \"companyFilingName\":[\n            \"NVIDIA CORPORATION\"\n         ],\n         \"description\":\"DYNAMIC DIRECTIONAL ROUNDING\",\n         \"filingDate\":\"2021-02-01 00:00:00\",\n         \"filingStatus\":\"Application\",\n         \"patentNumber\":\"US20210232366A1\",\n         \"publicationDate\":\"2021-07-29 00:00:00\",\n         \"type\":\"Utility\",\n         \"url\":\"https://patentimages.storage.googleapis.com/33/ed/0c/0b6b6f87e55fea/US20210232366A1.pdf\"\n      },\n      {\n         \"applicationNumber\":\"17162550\",\n         \"companyFilingName\":[\n            \"NVIDIA CORPORATION\"\n         ],\n         \"description\":\"REAL-TIME HARDWARE-ASSISTED GPU TUNING USING MACHINE LEARNING\",\n         \"filingDate\":\"2021-01-29 00:00:00\",\n         \"filingStatus\":\"Application\",\n         \"patentNumber\":\"US20210174569A1\",\n         \"publicationDate\":\"2021-06-10 00:00:00\",\n         \"type\":\"Utility\",\n         \"url\":\"https://patentimages.storage.googleapis.com/23/40/45/98b27a921d657c/US20210174569A1.pdf\"\n      }\n   ],\n   \"symbol\":\"NVDA\"\n}"
  curlExample: ""
  jsonExample: "{\n   \"data\":[\n      {\n         \"applicationNumber\":\"17163855\",\n         \"companyFilingName\":[\n            \"NVIDIA CORPORATION\"\n         ],\n         \"description\":\"DYNAMIC DIRECTIONAL ROUNDING\",\n         \"filingDate\":\"2021-02-01 00:00:00\",\n         \"filingStatus\":\"Application\",\n         \"patentNumber\":\"US20210232366A1\",\n         \"publicationDate\":\"2021-07-29 00:00:00\",\n         \"type\":\"Utility\",\n         \"url\":\"https://patentimages.storage.googleapis.com/33/ed/0c/0b6b6f87e55fea/US20210232366A1.pdf\"\n      },\n      {\n         \"applicationNumber\":\"17162550\",\n         \"companyFilingName\":[\n            \"NVIDIA CORPORATION\"\n         ],\n         \"description\":\"REAL-TIME HARDWARE-ASSISTED GPU TUNING USING MACHINE LEARNING\",\n         \"filingDate\":\"2021-01-29 00:00:00\",\n         \"filingStatus\":\"Application\",\n         \"patentNumber\":\"US20210174569A1\",\n         \"publicationDate\":\"2021-06-10 00:00:00\",\n         \"type\":\"Utility\",\n         \"url\":\"https://patentimages.storage.googleapis.com/23/40/45/98b27a921d657c/US20210174569A1.pdf\"\n      }\n   ],\n   \"symbol\":\"NVDA\"\n}"
  rawContent: ""
  suggestedFilename: "stock-uspto-patent"
---

# stock-uspto-patent

## 源URL

https://finnhub.io/docs/api/stock-uspto-patent

## 描述

List USPTO patents for companies. Limit to 250 records per API call.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/stock/uspto-patent`

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
finnhubClient.stockUsptoPatent("NVDA", "2020-01-01", "2021-05-01", (error, data, response) => {
	console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_uspto_patent('NVDA', _from="2020-06-01", to="2021-06-10"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.StockUsptoPatent(context.Background()).Symbol("NVDA").From("2020-05-01").To("2021-05-01").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->stockUsptoPatent("NVDA", "2020-06-01", "2021-06-10"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.stock_uspto_patent('NVDA', "2020-06-01", "2021-06-10"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.stockUsptoPatent("NVDA", from = "2020-06-01", to = "2021-06-10"))
```

### 示例 7 (json)

```json
{
   "data":[
      {
         "applicationNumber":"17163855",
         "companyFilingName":[
            "NVIDIA CORPORATION"
         ],
         "description":"DYNAMIC DIRECTIONAL ROUNDING",
         "filingDate":"2021-02-01 00:00:00",
         "filingStatus":"Application",
         "patentNumber":"US20210232366A1",
         "publicationDate":"2021-07-29 00:00:00",
         "type":"Utility",
         "url":"https://patentimages.storage.googleapis.com/33/ed/0c/0b6b6f87e55fea/US20210232366A1.pdf"
      },
      {
         "applicationNumber":"17162550",
         "companyFilingName":[
            "NVIDIA CORPORATION"
         ],
         "description":"REAL-TIME HARDWARE-ASSISTED GPU TUNING USING MACHINE LEARNING",
         "filingDate":"2021-01-29 00:00:00",
         "filingStatus":"Application",
         "patentNumber":"US20210174569A1",
         "publicationDate":"2021-06-10 00:00:00",
         "type":"Utility",
         "url":"https://patentimages.storage.googleapis.com/23/40/45/98b27a921d657c/US20210174569A1.pdf"
      }
   ],
   "symbol":"NVDA"
}
```

## 文档正文

List USPTO patents for companies. Limit to 250 records per API call.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/stock/uspto-patent`
