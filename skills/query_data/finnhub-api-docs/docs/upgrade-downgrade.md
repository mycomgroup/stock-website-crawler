---
id: "url-37bb4f9"
type: "api"
title: "Stock Upgrade/Downgrade Premium"
url: "https://finnhub.io/docs/api/upgrade-downgrade"
description: "Get latest stock upgrade and downgrade."
source: ""
tags: []
crawl_time: "2026-03-18T08:13:06.693Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/upgrade-downgrade?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Symbol of the company: AAPL. If left blank, the API will return latest stock upgrades/downgrades."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date: 2000-03-15."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date: 2020-03-16."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.upgradeDowngrade({\"symbol\": \"AAPL\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.upgrade_downgrade(symbol='AAPL', _from='2020-01-01', to='2020-06-30'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.UpgradeDowngrade(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->upgradeDowngrade(\"AAPL\", \"2020-01-01\", \"2020-06-30\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.upgrade_downgrade({symbol: 'AAPL', from: '2020-01-01', to: '2020-06-30'}))"}
    - {"language":"Kotlin","code":"println(apiClient.upgradeDowngrade(symbol = \"AAPL\", from = \"2020-01-01\", to = \"2020-06-30\"))"}
  sampleResponse: "[\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1567728000,\n    \"company\": \"DA Davidson\",\n    \"fromGrade\": \"\",\n    \"toGrade\": \"Underperform\",\n    \"action\": \"init\"\n  },\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1566259200,\n    \"company\": \"JP Morgan\",\n    \"fromGrade\": \"Neutral\",\n    \"toGrade\": \"Overweight\",\n    \"action\": \"up\"\n  },\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1564704000,\n    \"company\": \"Bank of America\",\n    \"fromGrade\": \"\",\n    \"toGrade\": \"Neutral\",\n    \"action\": \"reit\"\n  }\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1567728000,\n    \"company\": \"DA Davidson\",\n    \"fromGrade\": \"\",\n    \"toGrade\": \"Underperform\",\n    \"action\": \"init\"\n  },\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1566259200,\n    \"company\": \"JP Morgan\",\n    \"fromGrade\": \"Neutral\",\n    \"toGrade\": \"Overweight\",\n    \"action\": \"up\"\n  },\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1564704000,\n    \"company\": \"Bank of America\",\n    \"fromGrade\": \"\",\n    \"toGrade\": \"Neutral\",\n    \"action\": \"reit\"\n  }\n]"
  rawContent: "Stock Upgrade/Downgrade Premium\n\nGet latest stock upgrade and downgrade.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/upgrade-downgrade?symbol=AAPL\n\n/stock/upgrade-downgrade?symbol=BYND\n\nArguments:\n\nsymboloptional\n\nSymbol of the company: AAPL. If left blank, the API will return latest stock upgrades/downgrades.\n\nfromoptional\n\nFrom date: 2000-03-15.\n\ntooptional\n\nTo date: 2020-03-16.\n\nResponse Attributes:\n\naction\n\nAction can take any of the following values: up(upgrade), down(downgrade), main(maintains), init(initiate), reit(reiterate).\n\ncompany\n\nCompany/analyst who did the upgrade/downgrade.\n\nfromGrade\n\nFrom grade.\n\ngradeTime\n\nUpgrade/downgrade time in UNIX timestamp.\n\nsymbol\n\nCompany symbol.\n\ntoGrade\n\nTo grade.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.upgrade_downgrade(symbol='AAPL', _from='2020-01-01', to='2020-06-30'))\n\nSample response\n\n[\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1567728000,\n    \"company\": \"DA Davidson\",\n    \"fromGrade\": \"\",\n    \"toGrade\": \"Underperform\",\n    \"action\": \"init\"\n  },\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1566259200,\n    \"company\": \"JP Morgan\",\n    \"fromGrade\": \"Neutral\",\n    \"toGrade\": \"Overweight\",\n    \"action\": \"up\"\n  },\n  {\n    \"symbol\": \"BYND\",\n    \"gradeTime\": 1564704000,\n    \"company\": \"Bank of America\",\n    \"fromGrade\": \"\",\n    \"toGrade\": \"Neutral\",\n    \"action\": \"reit\"\n  }\n]"
  suggestedFilename: "upgrade-downgrade"
---

# Stock Upgrade/Downgrade Premium

## 源URL

https://finnhub.io/docs/api/upgrade-downgrade

## 描述

Get latest stock upgrade and downgrade.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/upgrade-downgrade?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Symbol of the company: AAPL. If left blank, the API will return latest stock upgrades/downgrades. |
| `from` | string | 否 | - | From date: 2000-03-15. |
| `to` | string | 否 | - | To date: 2020-03-16. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.upgradeDowngrade({"symbol": "AAPL"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.upgrade_downgrade(symbol='AAPL', _from='2020-01-01', to='2020-06-30'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.UpgradeDowngrade(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->upgradeDowngrade("AAPL", "2020-01-01", "2020-06-30"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.upgrade_downgrade({symbol: 'AAPL', from: '2020-01-01', to: '2020-06-30'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.upgradeDowngrade(symbol = "AAPL", from = "2020-01-01", to = "2020-06-30"))
```

### 示例 7 (json)

```json
[
  {
    "symbol": "BYND",
    "gradeTime": 1567728000,
    "company": "DA Davidson",
    "fromGrade": "",
    "toGrade": "Underperform",
    "action": "init"
  },
  {
    "symbol": "BYND",
    "gradeTime": 1566259200,
    "company": "JP Morgan",
    "fromGrade": "Neutral",
    "toGrade": "Overweight",
    "action": "up"
  },
  {
    "symbol": "BYND",
    "gradeTime": 1564704000,
    "company": "Bank of America",
    "fromGrade": "",
    "toGrade": "Neutral",
    "action": "reit"
  }
]
```

## 文档正文

Get latest stock upgrade and downgrade.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/upgrade-downgrade?symbol=AAPL`

Stock Upgrade/Downgrade Premium

Get latest stock upgrade and downgrade.

Method: GET

Premium: Premium Access Required

Examples:

/stock/upgrade-downgrade?symbol=AAPL

/stock/upgrade-downgrade?symbol=BYND

Arguments:

symboloptional

Symbol of the company: AAPL. If left blank, the API will return latest stock upgrades/downgrades.

fromoptional

From date: 2000-03-15.

tooptional

To date: 2020-03-16.

Response Attributes:

action

Action can take any of the following values: up(upgrade), down(downgrade), main(maintains), init(initiate), reit(reiterate).

company

Company/analyst who did the upgrade/downgrade.

fromGrade

From grade.

gradeTime

Upgrade/downgrade time in UNIX timestamp.

symbol

Company symbol.

toGrade

To grade.

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

print(finnhub_client.upgrade_downgrade(symbol='AAPL', _from='2020-01-01', to='2020-06-30'))

Sample response

[
  {
    "symbol": "BYND",
    "gradeTime": 1567728000,
    "company": "DA Davidson",
    "fromGrade": "",
    "toGrade": "Underperform",
    "action": "init"
  },
  {
    "symbol": "BYND",
    "gradeTime": 1566259200,
    "company": "JP Morgan",
    "fromGrade": "Neutral",
    "toGrade": "Overweight",
    "action": "up"
  },
  {
    "symbol": "BYND",
    "gradeTime": 1564704000,
    "company": "Bank of America",
    "fromGrade": "",
    "toGrade": "Neutral",
    "action": "reit"
  }
]
