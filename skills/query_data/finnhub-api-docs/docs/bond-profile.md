---
id: "url-6794748a"
type: "api"
title: "Bond Profile Premium"
url: "https://finnhub.io/docs/api/bond-profile"
description: "Get general information of a bond. You can query by FIGI, ISIN or CUSIP. A list of supported bonds can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T04:45:34.611Z"
metadata:
  requestMethod: "GET"
  endpoint: "/bond/profile?figi=BBG0152KFHS6"
  parameters:
    - {"name":"isin","in":"query","required":false,"type":"string","description":"ISIN"}
    - {"name":"cusip","in":"query","required":false,"type":"string","description":"CUSIP"}
    - {"name":"figi","in":"query","required":false,"type":"string","description":"FIGI"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.bondProfile({'isin': 'US912810TD00'}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.bond_profile(isin='US912810TD00'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.BondProfile(context.Background()).Isin(\"US912810TD00\").Execute()"}
    - {"language":"PHP","code":"print_r($client->bondProfile(\"US912810TD00\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.bond_profile({isin: 'US912810TD00'}))"}
    - {"language":"Kotlin","code":"println(apiClient.bondProfile(isin = \"US912810TD00\", cusip = null, figi = null))"}
  sampleResponse: "{\n  \"isin\":\"US912810TD00\",\n  \"cusip\":\"\",\n  \"figi\":\"BBG0152KFHS6\",\n  \"coupon\":2.25,\n  \"maturityDate\":\"2052-02-15\",\n  \"offeringPrice\":100,\n  \"issueDate\":\"2022-03-15\",\n  \"bondType\":\"US Government\",\n  \"debtType\":\"\",\n  \"industryGroup\":\"Government\",\n  \"industrySubGroup\":\"U.S. Treasuries\",\n  \"asset\":\"\",\n  \"assetType\":\"\",\n  \"datedDate\":\"2022-02-15\",\n  \"firstCouponDate\":\"2022-08-15\",\n  \"originalOffering\":20000000000,\n  \"amountOutstanding\":36914000000,\n  \"paymentFrequency\":\"Semi-Annual\",\n  \"securityLevel\":\"\",\n  \"callable\":null,\n  \"couponType\":\"\",\n  \"dayCount\":\"\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"isin\":\"US912810TD00\",\n  \"cusip\":\"\",\n  \"figi\":\"BBG0152KFHS6\",\n  \"coupon\":2.25,\n  \"maturityDate\":\"2052-02-15\",\n  \"offeringPrice\":100,\n  \"issueDate\":\"2022-03-15\",\n  \"bondType\":\"US Government\",\n  \"debtType\":\"\",\n  \"industryGroup\":\"Government\",\n  \"industrySubGroup\":\"U.S. Treasuries\",\n  \"asset\":\"\",\n  \"assetType\":\"\",\n  \"datedDate\":\"2022-02-15\",\n  \"firstCouponDate\":\"2022-08-15\",\n  \"originalOffering\":20000000000,\n  \"amountOutstanding\":36914000000,\n  \"paymentFrequency\":\"Semi-Annual\",\n  \"securityLevel\":\"\",\n  \"callable\":null,\n  \"couponType\":\"\",\n  \"dayCount\":\"\"\n}"
  rawContent: "Bond Profile Premium\n\nGet general information of a bond. You can query by FIGI, ISIN or CUSIP. A list of supported bonds can be found here.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/bond/profile?figi=BBG0152KFHS6\n\n/bond/profile?isin=US912810TD00\n\n/bond/profile?cusip=912810TD0\n\nArguments:\n\nisinoptional\n\nISIN\n\ncusipoptional\n\nCUSIP\n\nfigioptional\n\nFIGI\n\nResponse Attributes:\n\namountOutstanding\n\nOutstanding amount.\n\nasset\n\nAsset.\n\nassetType\n\nAsset.\n\nbondType\n\nBond type.\n\ncallable\n\nCallable.\n\ncoupon\n\nCoupon.\n\ncouponType\n\nCoupon type.\n\ncusip\n\nCusip.\n\ndatedDate\n\nDated date.\n\ndebtType\n\nBond type.\n\nfigi\n\nFIGI.\n\nfirstCouponDate\n\nFirst coupon date.\n\nindustryGroup\n\nIndustry.\n\nindustrySubGroup\n\nSub-Industry.\n\nisin\n\nISIN.\n\nissueDate\n\nIssue date.\n\nmaturityDate\n\nPeriod.\n\nofferingPrice\n\nOffering price.\n\noriginalOffering\n\nOffering amount.\n\npaymentFrequency\n\nPayment frequency.\n\nsecurityLevel\n\nSecurity level.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.bond_profile(isin='US912810TD00'))\n\nSample response\n\n{\n  \"isin\":\"US912810TD00\",\n  \"cusip\":\"\",\n  \"figi\":\"BBG0152KFHS6\",\n  \"coupon\":2.25,\n  \"maturityDate\":\"2052-02-15\",\n  \"offeringPrice\":100,\n  \"issueDate\":\"2022-03-15\",\n  \"bondType\":\"US Government\",\n  \"debtType\":\"\",\n  \"industryGroup\":\"Government\",\n  \"industrySubGroup\":\"U.S. Treasuries\",\n  \"asset\":\"\",\n  \"assetType\":\"\",\n  \"datedDate\":\"2022-02-15\",\n  \"firstCouponDate\":\"2022-08-15\",\n  \"originalOffering\":20000000000,\n  \"amountOutstanding\":36914000000,\n  \"paymentFrequency\":\"Semi-Annual\",\n  \"securityLevel\":\"\",\n  \"callable\":null,\n  \"couponType\":\"\",\n  \"dayCount\":\"\"\n}"
  suggestedFilename: "bond-profile"
---

# Bond Profile Premium

## 源URL

https://finnhub.io/docs/api/bond-profile

## 描述

Get general information of a bond. You can query by FIGI, ISIN or CUSIP. A list of supported bonds can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/bond/profile?figi=BBG0152KFHS6`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `isin` | string | 否 | - | ISIN |
| `cusip` | string | 否 | - | CUSIP |
| `figi` | string | 否 | - | FIGI |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.bondProfile({'isin': 'US912810TD00'}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.bond_profile(isin='US912810TD00'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.BondProfile(context.Background()).Isin("US912810TD00").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->bondProfile("US912810TD00"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.bond_profile({isin: 'US912810TD00'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.bondProfile(isin = "US912810TD00", cusip = null, figi = null))
```

### 示例 7 (json)

```json
{
  "isin":"US912810TD00",
  "cusip":"",
  "figi":"BBG0152KFHS6",
  "coupon":2.25,
  "maturityDate":"2052-02-15",
  "offeringPrice":100,
  "issueDate":"2022-03-15",
  "bondType":"US Government",
  "debtType":"",
  "industryGroup":"Government",
  "industrySubGroup":"U.S. Treasuries",
  "asset":"",
  "assetType":"",
  "datedDate":"2022-02-15",
  "firstCouponDate":"2022-08-15",
  "originalOffering":20000000000,
  "amountOutstanding":36914000000,
  "paymentFrequency":"Semi-Annual",
  "securityLevel":"",
  "callable":null,
  "couponType":"",
  "dayCount":""
}
```

## 文档正文

Get general information of a bond. You can query by FIGI, ISIN or CUSIP. A list of supported bonds can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/bond/profile?figi=BBG0152KFHS6`

Bond Profile Premium

Get general information of a bond. You can query by FIGI, ISIN or CUSIP. A list of supported bonds can be found here.

Method: GET

Premium: Premium Access Required

Examples:

/bond/profile?figi=BBG0152KFHS6

/bond/profile?isin=US912810TD00

/bond/profile?cusip=912810TD0

Arguments:

isinoptional

ISIN

cusipoptional

CUSIP

figioptional

FIGI

Response Attributes:

amountOutstanding

Outstanding amount.

asset

Asset.

assetType

Asset.

bondType

Bond type.

callable

Callable.

coupon

Coupon.

couponType

Coupon type.

cusip

Cusip.

datedDate

Dated date.

debtType

Bond type.

figi

FIGI.

firstCouponDate

First coupon date.

industryGroup

Industry.

industrySubGroup

Sub-Industry.

isin

ISIN.

issueDate

Issue date.

maturityDate

Period.

offeringPrice

Offering price.

originalOffering

Offering amount.

paymentFrequency

Payment frequency.

securityLevel

Security level.

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

print(finnhub_client.bond_profile(isin='US912810TD00'))

Sample response

{
  "isin":"US912810TD00",
  "cusip":"",
  "figi":"BBG0152KFHS6",
  "coupon":2.25,
  "maturityDate":"2052-02-15",
  "offeringPrice":100,
  "issueDate":"2022-03-15",
  "bondType":"US Government",
  "debtType":"",
  "industryGroup":"Government",
  "industrySubGroup":"U.S. Treasuries",
  "asset":"",
  "assetType":"",
  "datedDate":"2022-02-15",
  "firstCouponDate":"2022-08-15",
  "originalOffering":20000000000,
  "amountOutstanding":36914000000,
  "paymentFrequency":"Semi-Annual",
  "securityLevel":"",
  "callable":null,
  "couponType":"",
  "dayCount":""
}
