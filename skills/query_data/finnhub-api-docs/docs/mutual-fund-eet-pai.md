---
id: "url-1e516d1b"
type: "api"
title: "mutual-fund-eet-pai"
url: "https://finnhub.io/docs/api/mutual-fund-eet-pai"
description: "Get EET PAI data for EU funds."
source: ""
tags: []
crawl_time: "2026-03-18T08:35:43.113Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/mutual-fund/eet-pai"
  parameters:
    - {"name":"isin","in":"query","required":true,"type":"string","description":"ISIN."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.mutualFundEetPai('LU2036931686', (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.mutual_fund_eet_pai(\"LU2036931686\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.MutualFundEetPai(context.Background()).Isin(\"LU2036931686\").Execute()"}
    - {"language":"PHP","code":"print_r($client->mutualFundEetPai(\"LU2036931686\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.mutual_fund_eet_pai('LU2036931686'))"}
    - {"language":"Kotlin","code":"println(apiClient.mutualFundEetPai(\"LU2036931686\"))"}
  sampleResponse: "{\n   \"data\":{\n      \"airPollutantEmissionsCoveredHoldings\":27.94263,\n      \"airPollutantEmissionsEligibleHoldings\":490.89858,\n      \"airPollutantEmissionsNumberHoldingsCovered\":14,\n      \"airPollutantEmissionsPctPortfolioCoverage\":4.57,\n      \"airPollutantEmissionsPctPortfolioEligibleAssets\":79.65,\n      \"airPollutantEmissionsTonnesPerEURm\":1.28271,\n      \"antiHumanTraffickingNumberHoldingsCovered\":67,\n   },\n   \"isin\":\"LU2036931686\"\n}"
  curlExample: ""
  jsonExample: "{\n   \"data\":{\n      \"airPollutantEmissionsCoveredHoldings\":27.94263,\n      \"airPollutantEmissionsEligibleHoldings\":490.89858,\n      \"airPollutantEmissionsNumberHoldingsCovered\":14,\n      \"airPollutantEmissionsPctPortfolioCoverage\":4.57,\n      \"airPollutantEmissionsPctPortfolioEligibleAssets\":79.65,\n      \"airPollutantEmissionsTonnesPerEURm\":1.28271,\n      \"antiHumanTraffickingNumberHoldingsCovered\":67,\n   },\n   \"isin\":\"LU2036931686\"\n}"
  rawContent: ""
  suggestedFilename: "mutual-fund-eet-pai"
---

# mutual-fund-eet-pai

## 源URL

https://finnhub.io/docs/api/mutual-fund-eet-pai

## 描述

Get EET PAI data for EU funds.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/mutual-fund/eet-pai`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `isin` | string | 是 | - | ISIN. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.mutualFundEetPai('LU2036931686', (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.mutual_fund_eet_pai("LU2036931686"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.MutualFundEetPai(context.Background()).Isin("LU2036931686").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->mutualFundEetPai("LU2036931686"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.mutual_fund_eet_pai('LU2036931686'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.mutualFundEetPai("LU2036931686"))
```

### 示例 7 (json)

```json
{
   "data":{
      "airPollutantEmissionsCoveredHoldings":27.94263,
      "airPollutantEmissionsEligibleHoldings":490.89858,
      "airPollutantEmissionsNumberHoldingsCovered":14,
      "airPollutantEmissionsPctPortfolioCoverage":4.57,
      "airPollutantEmissionsPctPortfolioEligibleAssets":79.65,
      "airPollutantEmissionsTonnesPerEURm":1.28271,
      "antiHumanTraffickingNumberHoldingsCovered":67,
   },
   "isin":"LU2036931686"
}
```

## 文档正文

Get EET PAI data for EU funds.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/mutual-fund/eet-pai`
