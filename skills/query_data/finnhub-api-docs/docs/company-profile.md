---
id: "url-38cb108e"
type: "api"
title: "Company Profile Premium"
url: "https://finnhub.io/docs/api/company-profile"
description: "Get general information of a company. You can query by symbol, ISIN or CUSIP"
source: ""
tags: []
crawl_time: "2026-03-18T06:59:33.854Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/profile?symbol=AAPL"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Symbol of the company: AAPL e.g."}
    - {"name":"isin","in":"query","required":false,"type":"string","description":"ISIN"}
    - {"name":"cusip","in":"query","required":false,"type":"string","description":"CUSIP"}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.companyProfile({'symbol': 'AAPL'}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.company_profile(symbol='AAPL'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CompanyProfile(context.Background()).Symbol(\"AAPL\").Execute()"}
    - {"language":"PHP","code":"print_r($client->companyProfile(\"AAPL\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.company_profile({symbol: 'AAPL'}))"}
    - {"language":"Kotlin","code":"println(apiClient.companyProfile(symbol = \"AAPL\", isin = null, cusip = null))"}
  sampleResponse: "{\n  \"address\": \"1 Apple Park Way\",\n  \"city\": \"CUPERTINO\",\n  \"country\": \"US\",\n  \"currency\": \"USD\",\n  \"cusip\": \"\",\n  \"sedol\":\"2046251\",\n  \"description\": \"Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Four technology companies, alongside Amazon, Google, and Microsoft. The company's hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds and the HomePod smart speaker. Apple's software includes the macOS, iOS, iPadOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam acoustic fingerprint utility, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Music, Apple TV+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.\",\n  \"employeeTotal\": \"137000\",\n  \"exchange\": \"NASDAQ/NMS (GLOBAL MARKET)\",\n  \"ggroup\": \"Technology Hardware & Equipment\",\n  \"gind\": \"Technology Hardware, Storage & Peripherals\",\n  \"gsector\": \"Information Technology\",\n  \"gsubind\": \"Technology Hardware, Storage & Peripherals\",\n  \"ipo\": \"1980-12-12\",\n  \"isin\": \"\",\n  \"marketCapitalization\": 1415993,\n  \"naics\": \"Communications Equipment Manufacturing\",\n  \"naicsNationalIndustry\": \"Radio and Television Broadcasting and Wireless Communications Equipment Manufacturing\",\n  \"naicsSector\": \"Manufacturing\",\n  \"naicsSubsector\": \"Computer and Electronic Product Manufacturing\",\n  \"name\": \"Apple Inc\",\n  \"phone\": \"14089961010\",\n  \"shareOutstanding\": 4375.47998046875,\n  \"state\": \"CALIFORNIA\",\n  \"ticker\": \"AAPL\",\n  \"weburl\": \"https://www.apple.com/\",\n  \"logo\": \"https://static.finnhub.io/logo/87cb30d8-80df-11ea-8951-00000000092a.png\",\n  \"finnhubIndustry\":\"Technology\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"address\": \"1 Apple Park Way\",\n  \"city\": \"CUPERTINO\",\n  \"country\": \"US\",\n  \"currency\": \"USD\",\n  \"cusip\": \"\",\n  \"sedol\":\"2046251\",\n  \"description\": \"Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Four technology companies, alongside Amazon, Google, and Microsoft. The company's hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds and the HomePod smart speaker. Apple's software includes the macOS, iOS, iPadOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam acoustic fingerprint utility, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Music, Apple TV+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.\",\n  \"employeeTotal\": \"137000\",\n  \"exchange\": \"NASDAQ/NMS (GLOBAL MARKET)\",\n  \"ggroup\": \"Technology Hardware & Equipment\",\n  \"gind\": \"Technology Hardware, Storage & Peripherals\",\n  \"gsector\": \"Information Technology\",\n  \"gsubind\": \"Technology Hardware, Storage & Peripherals\",\n  \"ipo\": \"1980-12-12\",\n  \"isin\": \"\",\n  \"marketCapitalization\": 1415993,\n  \"naics\": \"Communications Equipment Manufacturing\",\n  \"naicsNationalIndustry\": \"Radio and Television Broadcasting and Wireless Communications Equipment Manufacturing\",\n  \"naicsSector\": \"Manufacturing\",\n  \"naicsSubsector\": \"Computer and Electronic Product Manufacturing\",\n  \"name\": \"Apple Inc\",\n  \"phone\": \"14089961010\",\n  \"shareOutstanding\": 4375.47998046875,\n  \"state\": \"CALIFORNIA\",\n  \"ticker\": \"AAPL\",\n  \"weburl\": \"https://www.apple.com/\",\n  \"logo\": \"https://static.finnhub.io/logo/87cb30d8-80df-11ea-8951-00000000092a.png\",\n  \"finnhubIndustry\":\"Technology\"\n}"
  rawContent: "Company Profile Premium\n\nGet general information of a company. You can query by symbol, ISIN or CUSIP\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/stock/profile?symbol=AAPL\n\n/stock/profile?symbol=IBM\n\n/stock/profile?isin=US5949181045\n\n/stock/profile?cusip=023135106\n\nArguments:\n\nsymboloptional\n\nSymbol of the company: AAPL e.g.\n\nisinoptional\n\nISIN\n\ncusipoptional\n\nCUSIP\n\nResponse Attributes:\n\naddress\n\nAddress of company's headquarter.\n\nalias\n\nCompany name alias.\n\ncity\n\nCity of company's headquarter.\n\ncountry\n\nCountry of company's headquarter.\n\ncurrency\n\nCurrency used in company filings and financials.\n\ncusip\n\nCUSIP number.\n\ndescription\n\nCompany business summary.\n\nemployeeTotal\n\nNumber of employee.\n\nestimateCurrency\n\nCurrency used in Estimates data.\n\nexchange\n\nListed exchange.\n\nfinnhubIndustry\n\nFinnhub industry classification.\n\nggroup\n\nIndustry group.\n\ngind\n\nIndustry.\n\ngsector\n\nSector.\n\ngsubind\n\nSub-industry.\n\nipo\n\nIPO date.\n\nirUrl\n\nInvestor relations website.\n\nisin\n\nISIN number.\n\nlei\n\nLEI number.\n\nlogo\n\nLogo image.\n\nmarketCapCurrency\n\nCurrency used in market capitalization.\n\nmarketCapitalization\n\nMarket Capitalization.\n\nnaics\n\nNAICS industry.\n\nnaicsNationalIndustry\n\nNAICS national industry.\n\nnaicsSector\n\nNAICS sector.\n\nnaicsSubsector\n\nNAICS subsector.\n\nname\n\nCompany name.\n\nphone\n\nCompany phone number.\n\nsedol\n\nSedol number.\n\nshareOutstanding\n\nNumber of oustanding shares.\n\nstate\n\nState of company's headquarter.\n\nticker\n\nCompany symbol/ticker as used on the listed exchange.\n\nweburl\n\nCompany website.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_profile(symbol='AAPL'))\n\nSample response\n\n{\n  \"address\": \"1 Apple Park Way\",\n  \"city\": \"CUPERTINO\",\n  \"country\": \"US\",\n  \"currency\": \"USD\",\n  \"cusip\": \"\",\n  \"sedol\":\"2046251\",\n  \"description\": \"Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Four technology companies, alongside Amazon, Google, and Microsoft. The company's hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds and the HomePod smart speaker. Apple's software includes the macOS, iOS, iPadOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam acoustic fingerprint utility, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Music, Apple TV+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.\",\n  \"employeeTotal\": \"137000\",\n  \"exchange\": \"NASDAQ/NMS (GLOBAL MARKET)\",\n  \"ggroup\": \"Technology Hardware & Equipment\",\n  \"gind\": \"Technology Hardware, Storage & Peripherals\",\n  \"gsector\": \"Information Technology\",\n  \"gsubind\": \"Technology Hardware, Storage & Peripherals\",\n  \"ipo\": \"1980-12-12\",\n  \"isin\": \"\",\n  \"marketCapitalization\": 1415993,\n  \"naics\": \"Communications Equipment Manufacturing\",\n  \"naicsNationalIndustry\": \"Radio and Television Broadcasting and Wireless Communications Equipment Manufacturing\",\n  \"naicsSector\": \"Manufacturing\",\n  \"naicsSubsector\": \"Computer and Electronic Product Manufacturing\",\n  \"name\": \"Apple Inc\",\n  \"phone\": \"14089961010\",\n  \"shareOutstanding\": 4375.47998046875,\n  \"state\": \"CALIFORNIA\",\n  \"ticker\": \"AAPL\",\n  \"weburl\": \"https://www.apple.com/\",\n  \"logo\": \"https://static.finnhub.io/logo/87cb30d8-80df-11ea-8951-00000000092a.png\",\n  \"finnhubIndustry\":\"Technology\"\n}"
  suggestedFilename: "company-profile"
---

# Company Profile Premium

## 源URL

https://finnhub.io/docs/api/company-profile

## 描述

Get general information of a company. You can query by symbol, ISIN or CUSIP

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/profile?symbol=AAPL`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Symbol of the company: AAPL e.g. |
| `isin` | string | 否 | - | ISIN |
| `cusip` | string | 否 | - | CUSIP |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.companyProfile({'symbol': 'AAPL'}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.company_profile(symbol='AAPL'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CompanyProfile(context.Background()).Symbol("AAPL").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->companyProfile("AAPL"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.company_profile({symbol: 'AAPL'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.companyProfile(symbol = "AAPL", isin = null, cusip = null))
```

### 示例 7 (json)

```json
{
  "address": "1 Apple Park Way",
  "city": "CUPERTINO",
  "country": "US",
  "currency": "USD",
  "cusip": "",
  "sedol":"2046251",
  "description": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Four technology companies, alongside Amazon, Google, and Microsoft. The company's hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds and the HomePod smart speaker. Apple's software includes the macOS, iOS, iPadOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam acoustic fingerprint utility, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Music, Apple TV+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.",
  "employeeTotal": "137000",
  "exchange": "NASDAQ/NMS (GLOBAL MARKET)",
  "ggroup": "Technology Hardware & Equipment",
  "gind": "Technology Hardware, Storage & Peripherals",
  "gsector": "Information Technology",
  "gsubind": "Technology Hardware, Storage & Peripherals",
  "ipo": "1980-12-12",
  "isin": "",
  "marketCapitalization": 1415993,
  "naics": "Communications Equipment Manufacturing",
  "naicsNationalIndustry": "Radio and Television Broadcasting and Wireless Communications Equipment Manufacturing",
  "naicsSector": "Manufacturing",
  "naicsSubsector": "Computer and Electronic Product Manufacturing",
  "name": "Apple Inc",
  "phone": "14089961010",
  "shareOutstanding": 4375.47998046875,
  "state": "CALIFORNIA",
  "ticker": "AAPL",
  "weburl": "https://www.apple.com/",
  "logo": "https://static.finnhub.io/logo/87cb30d8-80df-11ea-8951-00000000092a.png",
  "finnhubIndustry":"Technology"
}
```

## 文档正文

Get general information of a company. You can query by symbol, ISIN or CUSIP

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/profile?symbol=AAPL`

Company Profile Premium

Get general information of a company. You can query by symbol, ISIN or CUSIP

Method: GET

Premium: Premium Access Required

Examples:

/stock/profile?symbol=AAPL

/stock/profile?symbol=IBM

/stock/profile?isin=US5949181045

/stock/profile?cusip=023135106

Arguments:

symboloptional

Symbol of the company: AAPL e.g.

isinoptional

ISIN

cusipoptional

CUSIP

Response Attributes:

address

Address of company's headquarter.

alias

Company name alias.

city

City of company's headquarter.

country

Country of company's headquarter.

currency

Currency used in company filings and financials.

cusip

CUSIP number.

description

Company business summary.

employeeTotal

Number of employee.

estimateCurrency

Currency used in Estimates data.

exchange

Listed exchange.

finnhubIndustry

Finnhub industry classification.

ggroup

Industry group.

gind

Industry.

gsector

Sector.

gsubind

Sub-industry.

ipo

IPO date.

irUrl

Investor relations website.

isin

ISIN number.

lei

LEI number.

logo

Logo image.

marketCapCurrency

Currency used in market capitalization.

marketCapitalization

Market Capitalization.

naics

NAICS industry.

naicsNationalIndustry

NAICS national industry.

naicsSector

NAICS sector.

naicsSubsector

NAICS subsector.

name

Company name.

phone

Company phone number.

sedol

Sedol number.

shareOutstanding

Number of oustanding shares.

state

State of company's headquarter.

ticker

Company symbol/ticker as used on the listed exchange.

weburl

Company website.

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

print(finnhub_client.company_profile(symbol='AAPL'))

Sample response

{
  "address": "1 Apple Park Way",
  "city": "CUPERTINO",
  "country": "US",
  "currency": "USD",
  "cusip": "",
  "sedol":"2046251",
  "description": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Four technology companies, alongside Amazon, Google, and Microsoft. The company's hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds and the HomePod smart speaker. Apple's software includes the macOS, iOS, iPadOS, watchOS, and tvOS operating systems, the iTunes media player, the Safari web browser, the Shazam acoustic fingerprint utility, and the iLife and iWork creativity and productivity suites, as well as professional applications like Final Cut Pro, Logic Pro, and Xcode. Its online services include the iTunes Store, the iOS App Store, Mac App Store, Apple Music, Apple TV+, iMessage, and iCloud. Other services include Apple Store, Genius Bar, AppleCare, Apple Pay, Apple Pay Cash, and Apple Card.",
  "employeeTotal": "137000",
  "exchange": "NASDAQ/NMS (GLOBAL MARKET)",
  "ggroup": "Technology Hardware & Equipment",
  "gind": "Technology Hardware, Storage & Peripherals",
  "gsector": "Information Technology",
  "gsubind": "Technology Hardware, Storage & Peripherals",
  "ipo": "1980-12-12",
  "isin": "",
  "marketCapitalization": 1415993,
  "naics": "Communications Equipment Manufacturing",
  "naicsNationalIndustry": "Radio and Television Broadcasting and Wireless Communications Equipment Manufacturing",
  "naicsSector": "Manufacturing",
  "naicsSubsector": "Computer and Electronic Product Manufacturing",
  "name": "Apple Inc",
  "phone": "14089961010",
  "shareOutstanding": 4375.47998046875,
  "state": "CALIFORNIA",
  "ticker": "AAPL",
  "weburl": "https://www.apple.com/",
  "logo": "https://static.finnhub.io/logo/87cb30d8-80df-11ea-8951-00000000092a.png",
  "finnhubIndustry":"Technology"
}
