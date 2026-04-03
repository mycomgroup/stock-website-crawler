---
id: "url-182cb566"
type: "api"
title: "mutual-fund-eet"
url: "https://finnhub.io/docs/api/mutual-fund-eet"
description: "Get EET data for EU funds. For PAIs data, please see the EET PAI endpoint."
source: ""
tags: []
crawl_time: "2026-03-18T07:30:21.428Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/mutual-fund/eet"
  parameters:
    - {"name":"isin","in":"query","required":true,"type":"string","description":"ISIN."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.mutualFundEet('LU2036931686', (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.mutual_fund_eet(\"LU2036931686\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.MutualFundEet(context.Background()).Isin(\"LU2036931686\").Execute()"}
    - {"language":"PHP","code":"print_r($client->mutualFundEet(\"LU2036931686\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.mutual_fund_eet('LU2036931686'))"}
    - {"language":"Kotlin","code":"println(apiClient.mutualFundEet(\"LU2036931686\"))"}
  sampleResponse: "{\n   \"data\":{\n      \"boardGenderDiversityConsidered\":true,\n      \"carbonFootprintScope123Considered\":false,\n      \"carbonFootprintScope12Considered\":false,\n      \"clientSustainabilityPreferencesConsidered\":true,\n      \"controversialWeaponsConsidered\":true,\n      \"energyConsumptionIntensityNACEAConsidered\":false,\n      \"exposuretoEnergyEfficientRealEstateAssetsConsidered\":false,\n      \"exposuretoFossilFuelSectorConsidered\":false,\n      \"exposuretoFossilFuelsExtractionStorageTransportManufactureConsidered\":false,\n      \"greenhouseGasEmissionsScope1Considered\":false,\n      \"greenhouseGasEmissionsScope2Considered\":false,\n      \"greenhouseGasEmissionsScope3Considered\":false,\n   },\n   \"isin\":\"LU2036931686\"\n}"
  curlExample: ""
  jsonExample: "{\n   \"data\":{\n      \"boardGenderDiversityConsidered\":true,\n      \"carbonFootprintScope123Considered\":false,\n      \"carbonFootprintScope12Considered\":false,\n      \"clientSustainabilityPreferencesConsidered\":true,\n      \"controversialWeaponsConsidered\":true,\n      \"energyConsumptionIntensityNACEAConsidered\":false,\n      \"exposuretoEnergyEfficientRealEstateAssetsConsidered\":false,\n      \"exposuretoFossilFuelSectorConsidered\":false,\n      \"exposuretoFossilFuelsExtractionStorageTransportManufactureConsidered\":false,\n      \"greenhouseGasEmissionsScope1Considered\":false,\n      \"greenhouseGasEmissionsScope2Considered\":false,\n      \"greenhouseGasEmissionsScope3Considered\":false,\n   },\n   \"isin\":\"LU2036931686\"\n}"
  rawContent: ""
  suggestedFilename: "mutual-fund-eet"
---

# mutual-fund-eet

## 源URL

https://finnhub.io/docs/api/mutual-fund-eet

## 描述

Get EET data for EU funds. For PAIs data, please see the EET PAI endpoint.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/mutual-fund/eet`

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
finnhubClient.mutualFundEet('LU2036931686', (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.mutual_fund_eet("LU2036931686"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.MutualFundEet(context.Background()).Isin("LU2036931686").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->mutualFundEet("LU2036931686"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.mutual_fund_eet('LU2036931686'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.mutualFundEet("LU2036931686"))
```

### 示例 7 (json)

```json
{
   "data":{
      "boardGenderDiversityConsidered":true,
      "carbonFootprintScope123Considered":false,
      "carbonFootprintScope12Considered":false,
      "clientSustainabilityPreferencesConsidered":true,
      "controversialWeaponsConsidered":true,
      "energyConsumptionIntensityNACEAConsidered":false,
      "exposuretoEnergyEfficientRealEstateAssetsConsidered":false,
      "exposuretoFossilFuelSectorConsidered":false,
      "exposuretoFossilFuelsExtractionStorageTransportManufactureConsidered":false,
      "greenhouseGasEmissionsScope1Considered":false,
      "greenhouseGasEmissionsScope2Considered":false,
      "greenhouseGasEmissionsScope3Considered":false,
   },
   "isin":"LU2036931686"
}
```

## 文档正文

Get EET data for EU funds. For PAIs data, please see the EET PAI endpoint.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/mutual-fund/eet`
