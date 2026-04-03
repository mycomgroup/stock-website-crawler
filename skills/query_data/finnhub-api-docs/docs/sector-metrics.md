---
id: "url-35722687"
type: "api"
title: "Sector Metrics Premium"
url: "https://finnhub.io/docs/api/sector-metrics"
description: "Get ratios for different sectors and regions/indices."
source: ""
tags: []
crawl_time: "2026-03-18T06:58:18.155Z"
metadata:
  requestMethod: "GET"
  endpoint: "/sector/metrics?region=NA"
  parameters:
    - {"name":"region","in":"query","required":true,"type":"string","description":"Region. A list of supported values for this field can be found here."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.sectorMetric(\"NA\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.sector_metric('NA'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.SectorMetric(context.Background()).Region(\"NA\").Execute()"}
    - {"language":"PHP","code":"print_r($client->sectorMetric(\"NA\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.sector_metric('NA'))"}
    - {"language":"Kotlin","code":"println(apiClient.sectorMetric(\"NA\"))"}
  sampleResponse: "{\n  \"data\": [\n    {\n      \"metrics\": {\n        \"assetTurnoverAnnual\": {\n          \"a\": 0.7245,\n          \"m\": 0.5426\n        },\n        \"assetTurnoverTTM\": {\n          \"a\": 0.7254,\n          \"m\": 0.5463\n        },\n      },\n      \"sector\": \"Communication Services\"\n    },\n    {\n      \"metrics\": {\n        \"currentDividendYieldTTM\": {\n          \"a\": 30.9763,\n          \"m\": 2.09\n        },\n        \"currentEv/freeCashFlowAnnual\": {\n          \"a\": 286.4793,\n          \"m\": 19.8488\n        },\n      },\n      \"sector\": \"Consumer Discretionary\"\n    }\n  ],\n  \"region\": \"Asia_Ocenia\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"data\": [\n    {\n      \"metrics\": {\n        \"assetTurnoverAnnual\": {\n          \"a\": 0.7245,\n          \"m\": 0.5426\n        },\n        \"assetTurnoverTTM\": {\n          \"a\": 0.7254,\n          \"m\": 0.5463\n        },\n      },\n      \"sector\": \"Communication Services\"\n    },\n    {\n      \"metrics\": {\n        \"currentDividendYieldTTM\": {\n          \"a\": 30.9763,\n          \"m\": 2.09\n        },\n        \"currentEv/freeCashFlowAnnual\": {\n          \"a\": 286.4793,\n          \"m\": 19.8488\n        },\n      },\n      \"sector\": \"Consumer Discretionary\"\n    }\n  ],\n  \"region\": \"Asia_Ocenia\"\n}"
  rawContent: "Sector Metrics Premium\n\nGet ratios for different sectors and regions/indices.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/sector/metrics?region=NA\n\nArguments:\n\nregionREQUIRED\n\nRegion. A list of supported values for this field can be found here.\n\nResponse Attributes:\n\ndata\n\nMetrics for each sector.\n\nmetrics\n\nMetrics data in key-value format. a and m fields are for average and median respectively.\n\nsector\n\nSector\n\nregion\n\nRegion.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.sector_metric('NA'))\n\nSample response\n\n{\n  \"data\": [\n    {\n      \"metrics\": {\n        \"assetTurnoverAnnual\": {\n          \"a\": 0.7245,\n          \"m\": 0.5426\n        },\n        \"assetTurnoverTTM\": {\n          \"a\": 0.7254,\n          \"m\": 0.5463\n        },\n      },\n      \"sector\": \"Communication Services\"\n    },\n    {\n      \"metrics\": {\n        \"currentDividendYieldTTM\": {\n          \"a\": 30.9763,\n          \"m\": 2.09\n        },\n        \"currentEv/freeCashFlowAnnual\": {\n          \"a\": 286.4793,\n          \"m\": 19.8488\n        },\n      },\n      \"sector\": \"Consumer Discretionary\"\n    }\n  ],\n  \"region\": \"Asia_Ocenia\"\n}"
  suggestedFilename: "sector-metrics"
---

# Sector Metrics Premium

## 源URL

https://finnhub.io/docs/api/sector-metrics

## 描述

Get ratios for different sectors and regions/indices.

## API 端点

**Method**: `GET`
**Endpoint**: `/sector/metrics?region=NA`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `region` | string | 是 | - | Region. A list of supported values for this field can be found here. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.sectorMetric("NA", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.sector_metric('NA'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.SectorMetric(context.Background()).Region("NA").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->sectorMetric("NA"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.sector_metric('NA'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.sectorMetric("NA"))
```

### 示例 7 (json)

```json
{
  "data": [
    {
      "metrics": {
        "assetTurnoverAnnual": {
          "a": 0.7245,
          "m": 0.5426
        },
        "assetTurnoverTTM": {
          "a": 0.7254,
          "m": 0.5463
        },
      },
      "sector": "Communication Services"
    },
    {
      "metrics": {
        "currentDividendYieldTTM": {
          "a": 30.9763,
          "m": 2.09
        },
        "currentEv/freeCashFlowAnnual": {
          "a": 286.4793,
          "m": 19.8488
        },
      },
      "sector": "Consumer Discretionary"
    }
  ],
  "region": "Asia_Ocenia"
}
```

## 文档正文

Get ratios for different sectors and regions/indices.

## API 端点

**Method:** `GET`
**Endpoint:** `/sector/metrics?region=NA`

Sector Metrics Premium

Get ratios for different sectors and regions/indices.

Method: GET

Premium: Premium Access Required

Examples:

/sector/metrics?region=NA

Arguments:

regionREQUIRED

Region. A list of supported values for this field can be found here.

Response Attributes:

data

Metrics for each sector.

metrics

Metrics data in key-value format. a and m fields are for average and median respectively.

sector

Sector

region

Region.

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

print(finnhub_client.sector_metric('NA'))

Sample response

{
  "data": [
    {
      "metrics": {
        "assetTurnoverAnnual": {
          "a": 0.7245,
          "m": 0.5426
        },
        "assetTurnoverTTM": {
          "a": 0.7254,
          "m": 0.5463
        },
      },
      "sector": "Communication Services"
    },
    {
      "metrics": {
        "currentDividendYieldTTM": {
          "a": 30.9763,
          "m": 2.09
        },
        "currentEv/freeCashFlowAnnual": {
          "a": 286.4793,
          "m": 19.8488
        },
      },
      "sector": "Consumer Discretionary"
    }
  ],
  "region": "Asia_Ocenia"
}
