---
id: "url-c3294a5"
type: "api"
title: "Revenue Breakdown Premium"
url: "https://finnhub.io/docs/api/revenue-breakdown"
description: "Get revenue breakdown as-reporetd by product and geography. Users on personal plans can access data for US companies which disclose their revenue breakdown in the annual or quarterly reports.Global standardized revenue breakdown/segments data is available for Enterprise users. Contact us to inquire about the access for Global standardized data."
source: ""
tags: []
crawl_time: "2026-03-18T08:12:45.768Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/revenue-breakdown?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Symbol."}
    - {"name":"cik","in":"query","required":false,"type":"string","description":"CIK."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.revenueBreakdown({'symbol': 'AAPL'}, (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.stock_revenue_breakdown('AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.RevenueBreakdown(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->revenueBreakdown(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.revenue_breakdown({symbol:'AAPL'}))"}
    - {"language":"Kotlin","code":"println(apiClient.revenueBreakdown(\"AAPL\", \"\"))"}
  sampleResponse: "{\n  \"cik\": \"320193\",\n  \"data\": [\n    {\n      \"accessNumber\": \"0000320193-21-000010\",\n      \"breakdown\": {\n        \"unit\": \"usd\",\n        \"value\": 111439000000,\n        \"concept\": \"us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax\",\n        \"endDate\": \"2020-12-26\",\n        \"startDate\": \"2020-09-27\",\n        \"revenueBreakdown\": [\n          {\n            \"axis\": \"srt:ProductOrServiceAxis\",\n            \"data\": [\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Products\",\n                \"value\": 95678000000,\n                \"member\": \"us-gaap:ProductMember\",\n                \"percentage\": 85.85683647556061\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Services\",\n                \"value\": 15761000000,\n                \"member\": \"us-gaap:ServiceMember\",\n                \"percentage\": 14.14316352443938\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Services\",\n                \"value\": 15761000000,\n                \"member\": \"us-gaap:ServiceMember\",\n                \"percentage\": 14.14316352443938\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"iPhone\",\n                \"value\": 65597000000,\n                \"member\": \"aapl:IPhoneMember\",\n                \"percentage\": 58.86359353547681\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Mac\",\n                \"value\": 8675000000,\n                \"member\": \"aapl:MacMember\",\n                \"percentage\": 7.784527858290185\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"iPad\",\n                \"value\": 8435000000,\n                \"member\": \"aapl:IPadMember\",\n                \"percentage\": 7.569163398810111\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Wearables, Home and Accessories\",\n                \"value\": 12971000000,\n                \"member\": \"aapl:WearablesHomeandAccessoriesMember\",\n                \"percentage\": 11.639551682983516\n              }\n            ],\n            \"label\": \"Product and Service [Axis]\"\n          },\n        ]\n      }\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"cik\": \"320193\",\n  \"data\": [\n    {\n      \"accessNumber\": \"0000320193-21-000010\",\n      \"breakdown\": {\n        \"unit\": \"usd\",\n        \"value\": 111439000000,\n        \"concept\": \"us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax\",\n        \"endDate\": \"2020-12-26\",\n        \"startDate\": \"2020-09-27\",\n        \"revenueBreakdown\": [\n          {\n            \"axis\": \"srt:ProductOrServiceAxis\",\n            \"data\": [\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Products\",\n                \"value\": 95678000000,\n                \"member\": \"us-gaap:ProductMember\",\n                \"percentage\": 85.85683647556061\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Services\",\n                \"value\": 15761000000,\n                \"member\": \"us-gaap:ServiceMember\",\n                \"percentage\": 14.14316352443938\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Services\",\n                \"value\": 15761000000,\n                \"member\": \"us-gaap:ServiceMember\",\n                \"percentage\": 14.14316352443938\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"iPhone\",\n                \"value\": 65597000000,\n                \"member\": \"aapl:IPhoneMember\",\n                \"percentage\": 58.86359353547681\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Mac\",\n                \"value\": 8675000000,\n                \"member\": \"aapl:MacMember\",\n                \"percentage\": 7.784527858290185\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"iPad\",\n                \"value\": 8435000000,\n                \"member\": \"aapl:IPadMember\",\n                \"percentage\": 7.569163398810111\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Wearables, Home and Accessories\",\n                \"value\": 12971000000,\n                \"member\": \"aapl:WearablesHomeandAccessoriesMember\",\n                \"percentage\": 11.639551682983516\n              }\n            ],\n            \"label\": \"Product and Service [Axis]\"\n          },\n        ]\n      }\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  rawContent: "Revenue Breakdown Premium\n\nGet revenue breakdown as-reporetd by product and geography. Users on personal plans can access data for US companies which disclose their revenue breakdown in the annual or quarterly reports.\n\nGlobal standardized revenue breakdown/segments data is available for Enterprise users. Contact us to inquire about the access for Global standardized data.\n\nMethod: GET\n\nPremium: Premium\n\nExamples:\n\n/stock/revenue-breakdown?symbol=AAPL\n\n/stock/revenue-breakdown?cik=320193\n\nArguments:\n\nsymboloptional\n\nSymbol.\n\ncikoptional\n\nCIK.\n\nResponse Attributes:\n\ncik\n\nCIK\n\ndata\n\nArray of revenue breakdown over multiple periods.\n\naccessNumber\n\nAccess number of the report from which the data is sourced.\n\nbreakdown\n\nRevenue breakdown.\n\nsymbol\n\nSymbol\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.stock_revenue_breakdown('AAPL'))\n\nSample response\n\n{\n  \"cik\": \"320193\",\n  \"data\": [\n    {\n      \"accessNumber\": \"0000320193-21-000010\",\n      \"breakdown\": {\n        \"unit\": \"usd\",\n        \"value\": 111439000000,\n        \"concept\": \"us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax\",\n        \"endDate\": \"2020-12-26\",\n        \"startDate\": \"2020-09-27\",\n        \"revenueBreakdown\": [\n          {\n            \"axis\": \"srt:ProductOrServiceAxis\",\n            \"data\": [\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Products\",\n                \"value\": 95678000000,\n                \"member\": \"us-gaap:ProductMember\",\n                \"percentage\": 85.85683647556061\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Services\",\n                \"value\": 15761000000,\n                \"member\": \"us-gaap:ServiceMember\",\n                \"percentage\": 14.14316352443938\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Services\",\n                \"value\": 15761000000,\n                \"member\": \"us-gaap:ServiceMember\",\n                \"percentage\": 14.14316352443938\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"iPhone\",\n                \"value\": 65597000000,\n                \"member\": \"aapl:IPhoneMember\",\n                \"percentage\": 58.86359353547681\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Mac\",\n                \"value\": 8675000000,\n                \"member\": \"aapl:MacMember\",\n                \"percentage\": 7.784527858290185\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"iPad\",\n                \"value\": 8435000000,\n                \"member\": \"aapl:IPadMember\",\n                \"percentage\": 7.569163398810111\n              },\n              {\n                \"unit\": \"usd\",\n                \"label\": \"Wearables, Home and Accessories\",\n                \"value\": 12971000000,\n                \"member\": \"aapl:WearablesHomeandAccessoriesMember\",\n                \"percentage\": 11.639551682983516\n              }\n            ],\n            \"label\": \"Product and Service [Axis]\"\n          },\n        ]\n      }\n    }\n  ],\n  \"symbol\": \"AAPL\"\n}"
  suggestedFilename: "revenue-breakdown"
---

# Revenue Breakdown Premium

## 源URL

https://finnhub.io/docs/api/revenue-breakdown

## 描述

Get revenue breakdown as-reporetd by product and geography. Users on personal plans can access data for US companies which disclose their revenue breakdown in the annual or quarterly reports.Global standardized revenue breakdown/segments data is available for Enterprise users. Contact us to inquire about the access for Global standardized data.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/revenue-breakdown?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Symbol. |
| `cik` | string | 否 | - | CIK. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.revenueBreakdown({'symbol': 'AAPL'}, (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.stock_revenue_breakdown('AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.RevenueBreakdown(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->revenueBreakdown("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.revenue_breakdown({symbol:'AAPL'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.revenueBreakdown("AAPL", ""))
```

### 示例 7 (json)

```json
{
  "cik": "320193",
  "data": [
    {
      "accessNumber": "0000320193-21-000010",
      "breakdown": {
        "unit": "usd",
        "value": 111439000000,
        "concept": "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
        "endDate": "2020-12-26",
        "startDate": "2020-09-27",
        "revenueBreakdown": [
          {
            "axis": "srt:ProductOrServiceAxis",
            "data": [
              {
                "unit": "usd",
                "label": "Products",
                "value": 95678000000,
                "member": "us-gaap:ProductMember",
                "percentage": 85.85683647556061
              },
              {
                "unit": "usd",
                "label": "Services",
                "value": 15761000000,
                "member": "us-gaap:ServiceMember",
                "percentage": 14.14316352443938
              },
              {
                "unit": "usd",
                "label": "Services",
                "value": 15761000000,
                "member": "us-gaap:ServiceMember",
                "percentage": 14.14316352443938
              },
              {
                "unit": "usd",
                "label": "iPhone",
                "value": 65597000000,
                "member": "aapl:IPhoneMember",
                "percentage": 58.86359353547681
              },
              {
                "unit": "usd",
                "label": "Mac",
                "value": 8675000000,
                "member": "aapl:MacMember",
                "percentage": 7.784527858290185
              },
              {
                "unit": "usd",
                "label": "iPad",
                "value": 8435000000,
                "member": "aapl:IPadMember",
                "percentage": 7.569163398810111
              },
              {
                "unit": "usd",
                "label": "Wearables, Home and Accessories",
                "value": 12971000000,
                "member": "aapl:WearablesHomeandAccessoriesMember",
                "percentage": 11.639551682983516
              }
            ],
            "label": "Product and Service [Axis]"
          },
        ]
      }
    }
  ],
  "symbol": "AAPL"
}
```

## 文档正文

Get revenue breakdown as-reporetd by product and geography. Users on personal plans can access data for US companies which disclose their revenue breakdown in the annual or quarterly reports.Global standardized revenue breakdown/segments data is available for Enterprise users. Contact us to inquire about the access for Global standardized data.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/revenue-breakdown?symbol=AAPL`

Revenue Breakdown Premium

Get revenue breakdown as-reporetd by product and geography. Users on personal plans can access data for US companies which disclose their revenue breakdown in the annual or quarterly reports.

Global standardized revenue breakdown/segments data is available for Enterprise users. Contact us to inquire about the access for Global standardized data.

Method: GET

Premium: Premium

Examples:

/stock/revenue-breakdown?symbol=AAPL

/stock/revenue-breakdown?cik=320193

Arguments:

symboloptional

Symbol.

cikoptional

CIK.

Response Attributes:

cik

CIK

data

Array of revenue breakdown over multiple periods.

accessNumber

Access number of the report from which the data is sourced.

breakdown

Revenue breakdown.

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

print(finnhub_client.stock_revenue_breakdown('AAPL'))

Sample response

{
  "cik": "320193",
  "data": [
    {
      "accessNumber": "0000320193-21-000010",
      "breakdown": {
        "unit": "usd",
        "value": 111439000000,
        "concept": "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
        "endDate": "2020-12-26",
        "startDate": "2020-09-27",
        "revenueBreakdown": [
          {
            "axis": "srt:ProductOrServiceAxis",
            "data": [
              {
                "unit": "usd",
                "label": "Products",
                "value": 95678000000,
                "member": "us-gaap:ProductMember",
                "percentage": 85.85683647556061
              },
              {
                "unit": "usd",
                "label": "Services",
                "value": 15761000000,
                "member": "us-gaap:ServiceMember",
                "percentage": 14.14316352443938
              },
              {
                "unit": "usd",
                "label": "Services",
                "value": 15761000000,
                "member": "us-gaap:ServiceMember",
                "percentage": 14.14316352443938
              },
              {
                "unit": "usd",
                "label": "iPhone",
                "value": 65597000000,
                "member": "aapl:IPhoneMember",
                "percentage": 58.86359353547681
              },
              {
                "unit": "usd",
                "label": "Mac",
                "value": 8675000000,
                "member": "aapl:MacMember",
                "percentage": 7.784527858290185
              },
              {
                "unit": "usd",
                "label": "iPad",
                "value": 8435000000,
                "member": "aapl:IPadMember",
                "percentage": 7.569163398810111
              },
              {
                "unit": "usd",
                "label": "Wearables, Home and Accessories",
                "value": 12971000000,
                "member": "aapl:WearablesHomeandAccessoriesMember",
                "percentage": 11.639551682983516
              }
            ],
            "label": "Product and Service [Axis]"
          },
        ]
      }
    }
  ],
  "symbol": "AAPL"
}
