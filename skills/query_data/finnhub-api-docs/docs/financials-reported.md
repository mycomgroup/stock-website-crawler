---
id: "url-579b3015"
type: "api"
title: "financials-reported"
url: "https://finnhub.io/docs/api/financials-reported"
description: "Get financials as reported. This data is available for bulk download on Kaggle SEC Financials database."
source: ""
tags: []
crawl_time: "2026-03-18T08:35:20.967Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/stock/financials-reported"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Symbol."}
    - {"name":"cik","in":"query","required":false,"type":"string","description":"CIK."}
    - {"name":"accessNumber","in":"query","required":false,"type":"string","description":"Access number of a specific report you want to retrieve financials from."}
    - {"name":"freq","in":"query","required":false,"type":"string","description":"Frequency. Can be either annual or quarterly. Default to annual."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date YYYY-MM-DD. Filter for endDate."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date YYYY-MM-DD. Filter for endDate."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.financialsReported({\"symbol\": \"AAPL\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.financials_reported(symbol='AAPL', freq='annual'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.FinancialsReported(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->financialsReported($symbol = \"AAPL\", $freq = \"annual\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.financials_reported({symbol: 'AAPL', freq: 'annual'}))"}
    - {"language":"Kotlin","code":"println(apiClient.financialsReported(symbol = \"AAPL\", freq = \"annual\", accessNumber = null, cik = null))"}
  sampleResponse: "{\n  \"cik\": \"320193\",\n  \"data\": [\n    {\n      \"accessNumber\": \"0000320193-19-000119\",\n      \"symbol\": \"AAPL\",\n      \"cik\": \"320193\",\n      \"year\": 2019,\n      \"quarter\": 0,\n      \"form\": \"10-K\",\n      \"startDate\": \"2018-09-30 00:00:00\",\n      \"endDate\": \"2019-09-28 00:00:00\",\n      \"filedDate\": \"2019-10-31 00:00:00\",\n      \"acceptedDate\": \"2019-10-30 18:12:36\",\n      \"report\": {\n        \"bs\": {\n          \"Assets\": 338516000000,\n          \"Liabilities\": 248028000000,\n          \"InventoryNet\": 4106000000,\n          ...\n        },\n        \"cf\": {\n          \"NetIncomeLoss\": 55256000000,\n          \"InterestPaidNet\": 3423000000,\n          ...\n        },\n        \"ic\": {\n          \"GrossProfit\": 98392000000,\n          \"NetIncomeLoss\": 55256000000,\n          \"OperatingExpenses\": 34462000000,\n           ...\n        }\n      }\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"cik\": \"320193\",\n  \"data\": [\n    {\n      \"accessNumber\": \"0000320193-19-000119\",\n      \"symbol\": \"AAPL\",\n      \"cik\": \"320193\",\n      \"year\": 2019,\n      \"quarter\": 0,\n      \"form\": \"10-K\",\n      \"startDate\": \"2018-09-30 00:00:00\",\n      \"endDate\": \"2019-09-28 00:00:00\",\n      \"filedDate\": \"2019-10-31 00:00:00\",\n      \"acceptedDate\": \"2019-10-30 18:12:36\",\n      \"report\": {\n        \"bs\": {\n          \"Assets\": 338516000000,\n          \"Liabilities\": 248028000000,\n          \"InventoryNet\": 4106000000,\n          ...\n        },\n        \"cf\": {\n          \"NetIncomeLoss\": 55256000000,\n          \"InterestPaidNet\": 3423000000,\n          ...\n        },\n        \"ic\": {\n          \"GrossProfit\": 98392000000,\n          \"NetIncomeLoss\": 55256000000,\n          \"OperatingExpenses\": 34462000000,\n           ...\n        }\n      }\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: ""
  suggestedFilename: "financials-reported"
---

# financials-reported

## 源URL

https://finnhub.io/docs/api/financials-reported

## 描述

Get financials as reported. This data is available for bulk download on Kaggle SEC Financials database.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/stock/financials-reported`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Symbol. |
| `cik` | string | 否 | - | CIK. |
| `accessNumber` | string | 否 | - | Access number of a specific report you want to retrieve financials from. |
| `freq` | string | 否 | - | Frequency. Can be either annual or quarterly. Default to annual. |
| `from` | string | 否 | - | From date YYYY-MM-DD. Filter for endDate. |
| `to` | string | 否 | - | To date YYYY-MM-DD. Filter for endDate. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.financialsReported({"symbol": "AAPL"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.financials_reported(symbol='AAPL', freq='annual'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.FinancialsReported(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->financialsReported($symbol = "AAPL", $freq = "annual"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.financials_reported({symbol: 'AAPL', freq: 'annual'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.financialsReported(symbol = "AAPL", freq = "annual", accessNumber = null, cik = null))
```

### 示例 7 (json)

```json
{
  "cik": "320193",
  "data": [
    {
      "accessNumber": "0000320193-19-000119",
      "symbol": "AAPL",
      "cik": "320193",
      "year": 2019,
      "quarter": 0,
      "form": "10-K",
      "startDate": "2018-09-30 00:00:00",
      "endDate": "2019-09-28 00:00:00",
      "filedDate": "2019-10-31 00:00:00",
      "acceptedDate": "2019-10-30 18:12:36",
      "report": {
        "bs": {
          "Assets": 338516000000,
          "Liabilities": 248028000000,
          "InventoryNet": 4106000000,
          ...
        },
        "cf": {
          "NetIncomeLoss": 55256000000,
          "InterestPaidNet": 3423000000,
          ...
        },
        "ic": {
          "GrossProfit": 98392000000,
          "NetIncomeLoss": 55256000000,
          "OperatingExpenses": 34462000000,
           ...
        }
      }
    }
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Get financials as reported. This data is available for bulk download on Kaggle SEC Financials database.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/stock/financials-reported`
