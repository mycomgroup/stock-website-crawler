---
id: "url-74d7da83"
type: "api"
title: "ETFs Profile Premium"
url: "https://finnhub.io/docs/api/etfs-profile"
description: "Get ETF profile information. This endpoint has global coverage. A list of supported ETFs can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T04:45:23.977Z"
metadata:
  requestMethod: "GET"
  endpoint: "/etf/profile?symbol=SPY"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"ETF symbol."}
    - {"name":"isin","in":"query","required":false,"type":"string","description":"ETF isin."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.etfsProfile({'symbol': 'SPY'}, (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.etfs_profile('SPY'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.EtfsProfile(context.Background()).Symbol(\"SPY\").Execute()"}
    - {"language":"PHP","code":"print_r($client->etfsProfile(\"SPY\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.etfs_profile({symbol:'SPY'}))"}
    - {"language":"Kotlin","code":"println(apiClient.etfsProfile(\"SPY\", \"\"))"}
  sampleResponse: "{\n  \"profile\": {\n    \"assetClass\": \"Equity\",\n    \"aum\": 318374000000,\n    \"avgVolume\": 63794600,\n    \"cusip\": \"\",\n    \"description\": \"SPY was created on 1993-01-22 by SPDR. The fund's investment portfolio concentrates primarily on large cap equity. The ETF currently has 318374.0m in AUM and 504 holdings. SPY tracks a market-cap-weighted index of US large- and midcap stocks selected by the S\\u0026P Committee.\",\n    \"domicile\": \"US\",\n    \"etfCompany\": \"SPDR\",\n    \"expenseRatio\": 0.0945,\n    \"inceptionDate\": \"1993-01-22\",\n    \"investmentSegment\": \"Large Cap\",\n    \"isin\": \"\",\n    \"name\": \"SPDR S\\u0026P 500 ETF Trust\",\n    \"nav\": 366.2784,\n    \"navCurrency\": \"USD\",\n    \"priceToBook\": 3.943968,\n    \"priceToEarnings\": 26.82968,\n    \"trackingIndex\": \"S\\u0026P 500\",\n    \"logo\": \"https://static2.finnhub.io/file/publicdatany/finnhubimage/etf_logo/spdr.png\",\n    \"website\": \"https://us.spdrs.com/en/etf/spdr-sp-500-etf-SPY\"\n  },\n  \"symbol\": \"SPY\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"profile\": {\n    \"assetClass\": \"Equity\",\n    \"aum\": 318374000000,\n    \"avgVolume\": 63794600,\n    \"cusip\": \"\",\n    \"description\": \"SPY was created on 1993-01-22 by SPDR. The fund's investment portfolio concentrates primarily on large cap equity. The ETF currently has 318374.0m in AUM and 504 holdings. SPY tracks a market-cap-weighted index of US large- and midcap stocks selected by the S\\u0026P Committee.\",\n    \"domicile\": \"US\",\n    \"etfCompany\": \"SPDR\",\n    \"expenseRatio\": 0.0945,\n    \"inceptionDate\": \"1993-01-22\",\n    \"investmentSegment\": \"Large Cap\",\n    \"isin\": \"\",\n    \"name\": \"SPDR S\\u0026P 500 ETF Trust\",\n    \"nav\": 366.2784,\n    \"navCurrency\": \"USD\",\n    \"priceToBook\": 3.943968,\n    \"priceToEarnings\": 26.82968,\n    \"trackingIndex\": \"S\\u0026P 500\",\n    \"logo\": \"https://static2.finnhub.io/file/publicdatany/finnhubimage/etf_logo/spdr.png\",\n    \"website\": \"https://us.spdrs.com/en/etf/spdr-sp-500-etf-SPY\"\n  },\n  \"symbol\": \"SPY\"\n}"
  rawContent: "ETFs Profile Premium\n\nGet ETF profile information. This endpoint has global coverage. A list of supported ETFs can be found here.\n\nMethod: GET\n\nPremium: Premium required.\n\nExamples:\n\n/etf/profile?symbol=SPY\n\n/etf/profile?isin=US78462F1030\n\nArguments:\n\nsymboloptional\n\nETF symbol.\n\nisinoptional\n\nETF isin.\n\nResponse Attributes:\n\nprofile\n\nProfile data.\n\nassetClass\n\nAsset Class.\n\naum\n\nAUM.\n\navgVolume\n\n30-day average volume.\n\ncusip\n\nCUSIP.\n\ndescription\n\nETF's description.\n\ndividendYield\n\nDividend yield.\n\ndomicile\n\nETF domicile.\n\netfCompany\n\nETF issuer.\n\nexpenseRatio\n\nExpense ratio. For non-US funds, this is the KID ongoing charges.\n\ninceptionDate\n\nInception date.\n\ninvestmentSegment\n\nInvestment Segment.\n\nisInverse\n\nWhether the ETF is inverse\n\nisLeveraged\n\nWhether the ETF is leveraged\n\nisin\n\nISIN.\n\nleverageFactor\n\nLeverage factor.\n\nlogo\n\nLogo.\n\nname\n\nName\n\nnav\n\nNAV.\n\nnavCurrency\n\nNAV currency.\n\npriceToBook\n\nP/B.\n\npriceToEarnings\n\nP/E.\n\ntrackingIndex\n\nTracking Index.\n\nwebsite\n\nETF's website.\n\nsymbol\n\nSymbol.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.etfs_profile('SPY'))\n\nSample response\n\n{\n  \"profile\": {\n    \"assetClass\": \"Equity\",\n    \"aum\": 318374000000,\n    \"avgVolume\": 63794600,\n    \"cusip\": \"\",\n    \"description\": \"SPY was created on 1993-01-22 by SPDR. The fund's investment portfolio concentrates primarily on large cap equity. The ETF currently has 318374.0m in AUM and 504 holdings. SPY tracks a market-cap-weighted index of US large- and midcap stocks selected by the S\\u0026P Committee.\",\n    \"domicile\": \"US\",\n    \"etfCompany\": \"SPDR\",\n    \"expenseRatio\": 0.0945,\n    \"inceptionDate\": \"1993-01-22\",\n    \"investmentSegment\": \"Large Cap\",\n    \"isin\": \"\",\n    \"name\": \"SPDR S\\u0026P 500 ETF Trust\",\n    \"nav\": 366.2784,\n    \"navCurrency\": \"USD\",\n    \"priceToBook\": 3.943968,\n    \"priceToEarnings\": 26.82968,\n    \"trackingIndex\": \"S\\u0026P 500\",\n    \"logo\": \"https://static2.finnhub.io/file/publicdatany/finnhubimage/etf_logo/spdr.png\",\n    \"website\": \"https://us.spdrs.com/en/etf/spdr-sp-500-etf-SPY\"\n  },\n  \"symbol\": \"SPY\"\n}"
  suggestedFilename: "etfs-profile"
---

# ETFs Profile Premium

## 源URL

https://finnhub.io/docs/api/etfs-profile

## 描述

Get ETF profile information. This endpoint has global coverage. A list of supported ETFs can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/etf/profile?symbol=SPY`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | ETF symbol. |
| `isin` | string | 否 | - | ETF isin. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.etfsProfile({'symbol': 'SPY'}, (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.etfs_profile('SPY'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.EtfsProfile(context.Background()).Symbol("SPY").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->etfsProfile("SPY"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.etfs_profile({symbol:'SPY'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.etfsProfile("SPY", ""))
```

### 示例 7 (json)

```json
{
  "profile": {
    "assetClass": "Equity",
    "aum": 318374000000,
    "avgVolume": 63794600,
    "cusip": "",
    "description": "SPY was created on 1993-01-22 by SPDR. The fund's investment portfolio concentrates primarily on large cap equity. The ETF currently has 318374.0m in AUM and 504 holdings. SPY tracks a market-cap-weighted index of US large- and midcap stocks selected by the S\u0026P Committee.",
    "domicile": "US",
    "etfCompany": "SPDR",
    "expenseRatio": 0.0945,
    "inceptionDate": "1993-01-22",
    "investmentSegment": "Large Cap",
    "isin": "",
    "name": "SPDR S\u0026P 500 ETF Trust",
    "nav": 366.2784,
    "navCurrency": "USD",
    "priceToBook": 3.943968,
    "priceToEarnings": 26.82968,
    "trackingIndex": "S\u0026P 500",
    "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/etf_logo/spdr.png",
    "website": "https://us.spdrs.com/en/etf/spdr-sp-500-etf-SPY"
  },
  "symbol": "SPY"
}
```

## 文档正文

Get ETF profile information. This endpoint has global coverage. A list of supported ETFs can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/etf/profile?symbol=SPY`

ETFs Profile Premium

Get ETF profile information. This endpoint has global coverage. A list of supported ETFs can be found here.

Method: GET

Premium: Premium required.

Examples:

/etf/profile?symbol=SPY

/etf/profile?isin=US78462F1030

Arguments:

symboloptional

ETF symbol.

isinoptional

ETF isin.

Response Attributes:

profile

Profile data.

assetClass

Asset Class.

aum

AUM.

avgVolume

30-day average volume.

cusip

CUSIP.

description

ETF's description.

dividendYield

Dividend yield.

domicile

ETF domicile.

etfCompany

ETF issuer.

expenseRatio

Expense ratio. For non-US funds, this is the KID ongoing charges.

inceptionDate

Inception date.

investmentSegment

Investment Segment.

isInverse

Whether the ETF is inverse

isLeveraged

Whether the ETF is leveraged

isin

ISIN.

leverageFactor

Leverage factor.

logo

Logo.

name

Name

nav

NAV.

navCurrency

NAV currency.

priceToBook

P/B.

priceToEarnings

P/E.

trackingIndex

Tracking Index.

website

ETF's website.

symbol

Symbol.

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

print(finnhub_client.etfs_profile('SPY'))

Sample response

{
  "profile": {
    "assetClass": "Equity",
    "aum": 318374000000,
    "avgVolume": 63794600,
    "cusip": "",
    "description": "SPY was created on 1993-01-22 by SPDR. The fund's investment portfolio concentrates primarily on large cap equity. The ETF currently has 318374.0m in AUM and 504 holdings. SPY tracks a market-cap-weighted index of US large- and midcap stocks selected by the S\u0026P Committee.",
    "domicile": "US",
    "etfCompany": "SPDR",
    "expenseRatio": 0.0945,
    "inceptionDate": "1993-01-22",
    "investmentSegment": "Large Cap",
    "isin": "",
    "name": "SPDR S\u0026P 500 ETF Trust",
    "nav": 366.2784,
    "navCurrency": "USD",
    "priceToBook": 3.943968,
    "priceToEarnings": 26.82968,
    "trackingIndex": "S\u0026P 500",
    "logo": "https://static2.finnhub.io/file/publicdatany/finnhubimage/etf_logo/spdr.png",
    "website": "https://us.spdrs.com/en/etf/spdr-sp-500-etf-SPY"
  },
  "symbol": "SPY"
}
