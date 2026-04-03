---
id: "url-43c40623"
type: "api"
title: "ISIN Change Premium"
url: "https://finnhub.io/docs/api/isin-change"
description: "Get a list of ISIN changes for EU-listed securities. Limit to 2000 events at a time."
source: ""
tags: []
crawl_time: "2026-03-18T04:34:55.718Z"
metadata:
  requestMethod: "GET"
  endpoint: "/ca/isin-change?from=2022-09-01&to=2022-10-30"
  parameters:
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.isinChange({\"from\": \"2022-10-01\", \"to\": \"2022-10-11\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.isin_change(_from=\"2022-10-01\", to=\"2022-10-11\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.IsinChange(context.Background()).From(\"2022-10-01\").To(\"2022-10-11\").Execute()"}
    - {"language":"PHP","code":"print_r($client->isinChange(\"2020-01-01\", \"2020-06-11\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.isin_change({from: \"2020-01-01\", to: \"2020-06-11\"}))"}
    - {"language":"Kotlin","code":"println(\n            apiClient.isinChange(\n                from = \"2022-10-01\",\n                to = \"2020-10-11\")\n        )"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"atDate\": \"2021-08-30\",\n      \"newIsin\": \"DE000A3E5CP0\",\n      \"oldIsin\": \"DE0007239402\"\n    }\n  ],\n  \"fromDate\": \"2021-08-07\",\n  \"toDate\": \"2021-10-07\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"atDate\": \"2021-08-30\",\n      \"newIsin\": \"DE000A3E5CP0\",\n      \"oldIsin\": \"DE0007239402\"\n    }\n  ],\n  \"fromDate\": \"2021-08-07\",\n  \"toDate\": \"2021-10-07\"\n}"
  rawContent: "ISIN Change Premium\n\nGet a list of ISIN changes for EU-listed securities. Limit to 2000 events at a time.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/ca/isin-change?from=2022-09-01&to=2022-10-30\n\nArguments:\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ndata\n\nArray of ISIN change events.\n\natDate\n\nEvent's date.\n\nnewIsin\n\nNew ISIN.\n\noldIsin\n\nOld ISIN.\n\nfromDate\n\nFrom date.\n\ntoDate\n\nTo date.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.isin_change(_from=\"2022-10-01\", to=\"2022-10-11\"))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"atDate\": \"2021-08-30\",\n      \"newIsin\": \"DE000A3E5CP0\",\n      \"oldIsin\": \"DE0007239402\"\n    }\n  ],\n  \"fromDate\": \"2021-08-07\",\n  \"toDate\": \"2021-10-07\"\n}"
  suggestedFilename: "isin-change"
---

# ISIN Change Premium

## 源URL

https://finnhub.io/docs/api/isin-change

## 描述

Get a list of ISIN changes for EU-listed securities. Limit to 2000 events at a time.

## API 端点

**Method**: `GET`
**Endpoint**: `/ca/isin-change?from=2022-09-01&to=2022-10-30`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.isinChange({"from": "2022-10-01", "to": "2022-10-11"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.isin_change(_from="2022-10-01", to="2022-10-11"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.IsinChange(context.Background()).From("2022-10-01").To("2022-10-11").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->isinChange("2020-01-01", "2020-06-11"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.isin_change({from: "2020-01-01", to: "2020-06-11"}))
```

### 示例 6 (Kotlin)

```Kotlin
println(
            apiClient.isinChange(
                from = "2022-10-01",
                to = "2020-10-11")
        )
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "atDate": "2021-08-30",
      "newIsin": "DE000A3E5CP0",
      "oldIsin": "DE0007239402"
    }
  ],
  "fromDate": "2021-08-07",
  "toDate": "2021-10-07"
}
```

## 文档正文

Get a list of ISIN changes for EU-listed securities. Limit to 2000 events at a time.

## API 端点

**Method:** `GET`
**Endpoint:** `/ca/isin-change?from=2022-09-01&to=2022-10-30`

ISIN Change Premium

Get a list of ISIN changes for EU-listed securities. Limit to 2000 events at a time.

Method: GET

Premium: Premium Access Required

Examples:

/ca/isin-change?from=2022-09-01&to=2022-10-30

Arguments:

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

data

Array of ISIN change events.

atDate

Event's date.

newIsin

New ISIN.

oldIsin

Old ISIN.

fromDate

From date.

toDate

To date.

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

print(finnhub_client.isin_change(_from="2022-10-01", to="2022-10-11"))

Sample response

{
  "data": [
    {
      "atDate": "2021-08-30",
      "newIsin": "DE000A3E5CP0",
      "oldIsin": "DE0007239402"
    }
  ],
  "fromDate": "2021-08-07",
  "toDate": "2021-10-07"
}
