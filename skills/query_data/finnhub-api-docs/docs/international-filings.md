---
id: "url-38202090"
type: "api"
title: "International Filings Premium"
url: "https://finnhub.io/docs/api/international-filings"
description: "List filings for international companies. Limit to 500 documents at a time. These are the documents we use to source our fundamental data. Enterprise clients who need access to the full filings for global markets should contact us for the access."
source: ""
tags: []
crawl_time: "2026-03-18T09:52:48.082Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/international-filings?symbol=RY.TO"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Symbol. Leave empty to list latest filings."}
    - {"name":"country","in":"query","required":false,"type":"string","description":"Filter by country using country's 2-letter code."}
    - {"name":"from","in":"query","required":false,"type":"string","description":"From date: 2023-01-15."}
    - {"name":"to","in":"query","required":false,"type":"string","description":"To date: 2023-12-16."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.internationalFilings({\"symbol\": \"AC.TO\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.international_filings('AC.TO'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.InternationalFilings(context.Background()).Symbol(\"AC.TO\").Execute()"}
    - {"language":"PHP","code":"print_r($client->internationalFilings(\"AC.TO\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.international_filings({symbol: 'AC.TO'}))"}
    - {"language":"Kotlin","code":"println(apiClient.internationalFilings(\"AC.TO\", \"\"))"}
  sampleResponse: "[\n  {\n    \"symbol\": \"MINDTREE.NS\",\n    \"companyName\": \"MindTree Limited\",\n    \"filedDate\": \"2015-03-31 20:27:00\",\n    \"category\": \"Resignation of Director\",\n    \"title\": \"MindTree Limited has informed the Exchange that Mr. David B Yoffie has resigned as Independent Director of the company. The Board of Directors have accepted his resignation effective March 30, 2015.\",\n    \"description\": \"\",\n    \"url\": \"https://finnhub.io/international-filings?id=523566\",\n    \"language\": \"en\",\n    \"country\": \"IN\"\n  },\n  {\n    \"symbol\": \"INOXLEISUR.NS\",\n    \"companyName\": \"INOX Leisure Limited\",\n    \"filedDate\": \"2015-03-31 20:24:00\",\n    \"category\": \"Updates\",\n    \"title\": \"INOX Leisure Limited has informed the Exchange regarding Commencement of Commercial Operations of Multiplex Cinema Theatre situated at E-wing, Osia Commercial Arcade, SGPDA Market Complex, Margao, Goa 403601.\",\n    \"description\": \"\",\n    \"url\": \"https://finnhub.io/international-filings?id=52152\",\n    \"language\": \"en\",\n    \"country\": \"IN\"\n  }\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"symbol\": \"MINDTREE.NS\",\n    \"companyName\": \"MindTree Limited\",\n    \"filedDate\": \"2015-03-31 20:27:00\",\n    \"category\": \"Resignation of Director\",\n    \"title\": \"MindTree Limited has informed the Exchange that Mr. David B Yoffie has resigned as Independent Director of the company. The Board of Directors have accepted his resignation effective March 30, 2015.\",\n    \"description\": \"\",\n    \"url\": \"https://finnhub.io/international-filings?id=523566\",\n    \"language\": \"en\",\n    \"country\": \"IN\"\n  },\n  {\n    \"symbol\": \"INOXLEISUR.NS\",\n    \"companyName\": \"INOX Leisure Limited\",\n    \"filedDate\": \"2015-03-31 20:24:00\",\n    \"category\": \"Updates\",\n    \"title\": \"INOX Leisure Limited has informed the Exchange regarding Commencement of Commercial Operations of Multiplex Cinema Theatre situated at E-wing, Osia Commercial Arcade, SGPDA Market Complex, Margao, Goa 403601.\",\n    \"description\": \"\",\n    \"url\": \"https://finnhub.io/international-filings?id=52152\",\n    \"language\": \"en\",\n    \"country\": \"IN\"\n  }\n]"
  rawContent: "International Filings Premium\n\nList filings for international companies. Limit to 500 documents at a time. These are the documents we use to source our fundamental data. Enterprise clients who need access to the full filings for global markets should contact us for the access.\n\nMethod: GET\n\nPremium: Access approved on a case by case basis\n\nExamples:\n\n/stock/international-filings?symbol=RY.TO\n\n/stock/international-filings?country=CA\n\nArguments:\n\nsymboloptional\n\nSymbol. Leave empty to list latest filings.\n\ncountryoptional\n\nFilter by country using country's 2-letter code.\n\nfromoptional\n\nFrom date: 2023-01-15.\n\ntooptional\n\nTo date: 2023-12-16.\n\nResponse Attributes:\n\ncategory\n\nCategory.\n\ncompanyName\n\nCompany name.\n\ncountry\n\nCountry.\n\ndescription\n\nDocument's description.\n\nfiledDate\n\nFiled date %Y-%m-%d %H:%M:%S.\n\nlanguage\n\nLanguage.\n\nsymbol\n\nSymbol.\n\ntitle\n\nDocument's title.\n\nurl\n\nUrl.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.international_filings('AC.TO'))\n\nSample response\n\n[\n  {\n    \"symbol\": \"MINDTREE.NS\",\n    \"companyName\": \"MindTree Limited\",\n    \"filedDate\": \"2015-03-31 20:27:00\",\n    \"category\": \"Resignation of Director\",\n    \"title\": \"MindTree Limited has informed the Exchange that Mr. David B Yoffie has resigned as Independent Director of the company. The Board of Directors have accepted his resignation effective March 30, 2015.\",\n    \"description\": \"\",\n    \"url\": \"https://finnhub.io/international-filings?id=523566\",\n    \"language\": \"en\",\n    \"country\": \"IN\"\n  },\n  {\n    \"symbol\": \"INOXLEISUR.NS\",\n    \"companyName\": \"INOX Leisure Limited\",\n    \"filedDate\": \"2015-03-31 20:24:00\",\n    \"category\": \"Updates\",\n    \"title\": \"INOX Leisure Limited has informed the Exchange regarding Commencement of Commercial Operations of Multiplex Cinema Theatre situated at E-wing, Osia Commercial Arcade, SGPDA Market Complex, Margao, Goa 403601.\",\n    \"description\": \"\",\n    \"url\": \"https://finnhub.io/international-filings?id=52152\",\n    \"language\": \"en\",\n    \"country\": \"IN\"\n  }\n]"
  suggestedFilename: "international-filings"
---

# International Filings Premium

## 源URL

https://finnhub.io/docs/api/international-filings

## 描述

List filings for international companies. Limit to 500 documents at a time. These are the documents we use to source our fundamental data. Enterprise clients who need access to the full filings for global markets should contact us for the access.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/international-filings?symbol=RY.TO`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Symbol. Leave empty to list latest filings. |
| `country` | string | 否 | - | Filter by country using country's 2-letter code. |
| `from` | string | 否 | - | From date: 2023-01-15. |
| `to` | string | 否 | - | To date: 2023-12-16. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.internationalFilings({"symbol": "AC.TO"}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.international_filings('AC.TO'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.InternationalFilings(context.Background()).Symbol("AC.TO").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->internationalFilings("AC.TO"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.international_filings({symbol: 'AC.TO'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.internationalFilings("AC.TO", ""))
```

### 示例 7 (json)

```json
[
  {
    "symbol": "MINDTREE.NS",
    "companyName": "MindTree Limited",
    "filedDate": "2015-03-31 20:27:00",
    "category": "Resignation of Director",
    "title": "MindTree Limited has informed the Exchange that Mr. David B Yoffie has resigned as Independent Director of the company. The Board of Directors have accepted his resignation effective March 30, 2015.",
    "description": "",
    "url": "https://finnhub.io/international-filings?id=523566",
    "language": "en",
    "country": "IN"
  },
  {
    "symbol": "INOXLEISUR.NS",
    "companyName": "INOX Leisure Limited",
    "filedDate": "2015-03-31 20:24:00",
    "category": "Updates",
    "title": "INOX Leisure Limited has informed the Exchange regarding Commencement of Commercial Operations of Multiplex Cinema Theatre situated at E-wing, Osia Commercial Arcade, SGPDA Market Complex, Margao, Goa 403601.",
    "description": "",
    "url": "https://finnhub.io/international-filings?id=52152",
    "language": "en",
    "country": "IN"
  }
]
```

## 文档正文

List filings for international companies. Limit to 500 documents at a time. These are the documents we use to source our fundamental data. Enterprise clients who need access to the full filings for global markets should contact us for the access.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/international-filings?symbol=RY.TO`

International Filings Premium

List filings for international companies. Limit to 500 documents at a time. These are the documents we use to source our fundamental data. Enterprise clients who need access to the full filings for global markets should contact us for the access.

Method: GET

Premium: Access approved on a case by case basis

Examples:

/stock/international-filings?symbol=RY.TO

/stock/international-filings?country=CA

Arguments:

symboloptional

Symbol. Leave empty to list latest filings.

countryoptional

Filter by country using country's 2-letter code.

fromoptional

From date: 2023-01-15.

tooptional

To date: 2023-12-16.

Response Attributes:

category

Category.

companyName

Company name.

country

Country.

description

Document's description.

filedDate

Filed date %Y-%m-%d %H:%M:%S.

language

Language.

symbol

Symbol.

title

Document's title.

url

Url.

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

print(finnhub_client.international_filings('AC.TO'))

Sample response

[
  {
    "symbol": "MINDTREE.NS",
    "companyName": "MindTree Limited",
    "filedDate": "2015-03-31 20:27:00",
    "category": "Resignation of Director",
    "title": "MindTree Limited has informed the Exchange that Mr. David B Yoffie has resigned as Independent Director of the company. The Board of Directors have accepted his resignation effective March 30, 2015.",
    "description": "",
    "url": "https://finnhub.io/international-filings?id=523566",
    "language": "en",
    "country": "IN"
  },
  {
    "symbol": "INOXLEISUR.NS",
    "companyName": "INOX Leisure Limited",
    "filedDate": "2015-03-31 20:24:00",
    "category": "Updates",
    "title": "INOX Leisure Limited has informed the Exchange regarding Commencement of Commercial Operations of Multiplex Cinema Theatre situated at E-wing, Osia Commercial Arcade, SGPDA Market Complex, Margao, Goa 403601.",
    "description": "",
    "url": "https://finnhub.io/international-filings?id=52152",
    "language": "en",
    "country": "IN"
  }
]
