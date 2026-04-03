---
id: "url-2675f60e"
type: "api"
title: "Company News"
url: "https://finnhub.io/docs/api/company-news"
description: "List latest company news by symbol. This endpoint is only available for North American companies."
source: ""
tags: []
crawl_time: "2026-03-18T04:35:29.093Z"
metadata:
  requestMethod: "GET"
  endpoint: "/company-news?symbol=AAPL&from=2025-05-15&to=2025-06-20"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Company symbol."}
    - {"name":"from","in":"query","required":true,"type":"string","description":"From date YYYY-MM-DD."}
    - {"name":"to","in":"query","required":true,"type":"string","description":"To date YYYY-MM-DD."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.companyNews(\"AAPL\", \"2020-01-01\", \"2020-05-01\", (error, data, response) => {\n\tconsole.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.company_news('AAPL', _from=\"2020-06-01\", to=\"2020-06-10\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CompanyNews(context.Background()).Symbol(\"AAPL\").From(\"2020-05-01\").To(\"2020-05-01\").Execute()"}
    - {"language":"PHP","code":"print_r($client->companyNews(\"AAPL\", \"2020-06-01\", \"2020-06-10\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.company_news('AAPL', \"2020-06-01\", \"2020-06-10\"))"}
    - {"language":"Kotlin","code":"println(apiClient.companyNews(\"AAPL\", from = \"2020-06-01\", to = \"2020-06-10\"))"}
  sampleResponse: "[\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569550360,\n    \"headline\": \"More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official.  More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official\",\n    \"id\": 25286,\n    \"image\": \"https://img.etimg.com/thumb/msid-71321314,width-1070,height-580,imgsize-481831,overlay-economictimes/photo.jpg\",\n    \"related\": \"AAPL\",\n    \"source\": \"The Economic Times India\",\n    \"summary\": \"NEW DELHI | CHENNAI: India may have to offer electronic manufacturers additional sops such as cheap credit and incentives for export along with infrastructure support in order to boost production and help the sector compete with China, Vietnam and Thailand, according to a top government official.These incentives, over and above the proposed reduction of corporate tax to 15% for new manufacturing units, are vital for India to successfully attract companies looking to relocate manufacturing facilities.“While the tax announcements made last week send a very good signal, in order to help attract investments, we will need additional initiatives,” the official told ET, pointing out that Indian electronic manufacturers incur 8-10% higher costs compared with other Asian countries.Sops that are similar to the incentives for export under the existing Merchandise Exports from India Scheme (MEIS) are what the industry requires, the person said.MEIS gives tax credit in the range of 2-5%. An interest subvention scheme for cheaper loans and a credit guarantee scheme for plant and machinery are some other possible measures that will help the industry, the official added.“This should be 2.0 (second) version of the electronic manufacturing cluster (EMC) scheme, which is aimed at creating an ecosystem with an anchor company plus its suppliers to operate in the same area,” he said.Last week, finance minister Nirmala Sitharaman announced a series of measures to boost economic growth including a scheme allowing any new manufacturing company incorporated on or after October 1, to pay income tax at 15% provided the company does not avail of any other exemption or incentives.\",\n    \"url\": \"https://economictimes.indiatimes.com/industry/cons-products/electronics/more-sops-needed-to-boost-electronic-manufacturing-top-govt-official/articleshow/71321308.cms\"\n  },\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569528720,\n    \"headline\": \"How to disable comments on your YouTube videos in 2 different ways\",\n    \"id\": 25287,\n    \"image\": \"https://amp.businessinsider.com/images/5d8d16182e22af6ab66c09e9-1536-768.jpg\",\n    \"related\": \"AAPL\",\n    \"source\": \"Business Insider\",\n    \"summary\": \"You can disable comments on your own YouTube video if you don't want people to comment on it. It's easy to disable comments on YouTube by adjusting the settings for one of your videos in the beta or classic version of YouTube Studio. Visit Business Insider's homepage for more stories . The comments section has a somewhat complicated reputation for creators, especially for those making videos on YouTube . While it can be useful to get the unfiltered opinions of your YouTube viewers and possibly forge a closer connection with them, it can also open you up to quite a bit of negativity. So it makes sense that there may be times when you want to turn off the feature entirely. Just keep in mind that the action itself can spark conversation. If you decide that you don't want to let people leave comments on your YouTube video, here's how to turn off the feature, using either the classic or beta version of the creator studio: How to disable comments on YouTube in YouTube Studio (beta) 1. Go to youtube.com and log into your account, if necessary. 2.\",\n    \"url\": \"https://www.businessinsider.com/how-to-disable-comments-on-youtube\"\n  },\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569526180,\n    \"headline\": \"Apple iPhone 11 Pro Teardowns Look Encouraging for STMicro and Sony\",\n    \"id\": 25341,\n    \"image\": \"http://s.thestreet.com/files/tsc/v2008/photos/contrib/uploads/ba140938-d409-11e9-822b-fda891ce1fc1.png\",\n    \"related\": \"AAPL\",\n    \"source\": \"TheStreet\",\n    \"summary\": \"STMicroelectronics and Sony each appear to be supplying four chips for Apple's latest flagship iPhones. Many other historical iPhone suppliers also make appearances in the latest teardowns….STM\",\n    \"url\": \"https://realmoney.thestreet.com/investing/technology/iphone-11-pro-teardowns-look-encouraging-for-stmicro-sony-15105767\"\n  },\n]"
  curlExample: ""
  jsonExample: "[\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569550360,\n    \"headline\": \"More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official.  More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official\",\n    \"id\": 25286,\n    \"image\": \"https://img.etimg.com/thumb/msid-71321314,width-1070,height-580,imgsize-481831,overlay-economictimes/photo.jpg\",\n    \"related\": \"AAPL\",\n    \"source\": \"The Economic Times India\",\n    \"summary\": \"NEW DELHI | CHENNAI: India may have to offer electronic manufacturers additional sops such as cheap credit and incentives for export along with infrastructure support in order to boost production and help the sector compete with China, Vietnam and Thailand, according to a top government official.These incentives, over and above the proposed reduction of corporate tax to 15% for new manufacturing units, are vital for India to successfully attract companies looking to relocate manufacturing facilities.“While the tax announcements made last week send a very good signal, in order to help attract investments, we will need additional initiatives,” the official told ET, pointing out that Indian electronic manufacturers incur 8-10% higher costs compared with other Asian countries.Sops that are similar to the incentives for export under the existing Merchandise Exports from India Scheme (MEIS) are what the industry requires, the person said.MEIS gives tax credit in the range of 2-5%. An interest subvention scheme for cheaper loans and a credit guarantee scheme for plant and machinery are some other possible measures that will help the industry, the official added.“This should be 2.0 (second) version of the electronic manufacturing cluster (EMC) scheme, which is aimed at creating an ecosystem with an anchor company plus its suppliers to operate in the same area,” he said.Last week, finance minister Nirmala Sitharaman announced a series of measures to boost economic growth including a scheme allowing any new manufacturing company incorporated on or after October 1, to pay income tax at 15% provided the company does not avail of any other exemption or incentives.\",\n    \"url\": \"https://economictimes.indiatimes.com/industry/cons-products/electronics/more-sops-needed-to-boost-electronic-manufacturing-top-govt-official/articleshow/71321308.cms\"\n  },\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569528720,\n    \"headline\": \"How to disable comments on your YouTube videos in 2 different ways\",\n    \"id\": 25287,\n    \"image\": \"https://amp.businessinsider.com/images/5d8d16182e22af6ab66c09e9-1536-768.jpg\",\n    \"related\": \"AAPL\",\n    \"source\": \"Business Insider\",\n    \"summary\": \"You can disable comments on your own YouTube video if you don't want people to comment on it. It's easy to disable comments on YouTube by adjusting the settings for one of your videos in the beta or classic version of YouTube Studio. Visit Business Insider's homepage for more stories . The comments section has a somewhat complicated reputation for creators, especially for those making videos on YouTube . While it can be useful to get the unfiltered opinions of your YouTube viewers and possibly forge a closer connection with them, it can also open you up to quite a bit of negativity. So it makes sense that there may be times when you want to turn off the feature entirely. Just keep in mind that the action itself can spark conversation. If you decide that you don't want to let people leave comments on your YouTube video, here's how to turn off the feature, using either the classic or beta version of the creator studio: How to disable comments on YouTube in YouTube Studio (beta) 1. Go to youtube.com and log into your account, if necessary. 2.\",\n    \"url\": \"https://www.businessinsider.com/how-to-disable-comments-on-youtube\"\n  },\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569526180,\n    \"headline\": \"Apple iPhone 11 Pro Teardowns Look Encouraging for STMicro and Sony\",\n    \"id\": 25341,\n    \"image\": \"http://s.thestreet.com/files/tsc/v2008/photos/contrib/uploads/ba140938-d409-11e9-822b-fda891ce1fc1.png\",\n    \"related\": \"AAPL\",\n    \"source\": \"TheStreet\",\n    \"summary\": \"STMicroelectronics and Sony each appear to be supplying four chips for Apple's latest flagship iPhones. Many other historical iPhone suppliers also make appearances in the latest teardowns….STM\",\n    \"url\": \"https://realmoney.thestreet.com/investing/technology/iphone-11-pro-teardowns-look-encouraging-for-stmicro-sony-15105767\"\n  },\n]"
  rawContent: "Company News\n\nList latest company news by symbol. This endpoint is only available for North American companies.\n\nMethod: GET\n\nFree Tier: 1 year of historical news and new updates\n\nExamples:\n\n/company-news?symbol=AAPL&from=2025-05-15&to=2025-06-20\n\nArguments:\n\nsymbolREQUIRED\n\nCompany symbol.\n\nfromREQUIRED\n\nFrom date YYYY-MM-DD.\n\ntoREQUIRED\n\nTo date YYYY-MM-DD.\n\nResponse Attributes:\n\ncategory\n\nNews category.\n\ndatetime\n\nPublished time in UNIX timestamp.\n\nheadline\n\nNews headline.\n\nid\n\nNews ID. This value can be used for minId params to get the latest news only.\n\nimage\n\nThumbnail image URL.\n\nrelated\n\nRelated stocks and companies mentioned in the article.\n\nsource\n\nNews source.\n\nsummary\n\nNews summary.\n\nurl\n\nURL of the original article.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.company_news('AAPL', _from=\"2020-06-01\", to=\"2020-06-10\"))\n\nSample response\n\n[\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569550360,\n    \"headline\": \"More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official.  More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official\",\n    \"id\": 25286,\n    \"image\": \"https://img.etimg.com/thumb/msid-71321314,width-1070,height-580,imgsize-481831,overlay-economictimes/photo.jpg\",\n    \"related\": \"AAPL\",\n    \"source\": \"The Economic Times India\",\n    \"summary\": \"NEW DELHI | CHENNAI: India may have to offer electronic manufacturers additional sops such as cheap credit and incentives for export along with infrastructure support in order to boost production and help the sector compete with China, Vietnam and Thailand, according to a top government official.These incentives, over and above the proposed reduction of corporate tax to 15% for new manufacturing units, are vital for India to successfully attract companies looking to relocate manufacturing facilities.“While the tax announcements made last week send a very good signal, in order to help attract investments, we will need additional initiatives,” the official told ET, pointing out that Indian electronic manufacturers incur 8-10% higher costs compared with other Asian countries.Sops that are similar to the incentives for export under the existing Merchandise Exports from India Scheme (MEIS) are what the industry requires, the person said.MEIS gives tax credit in the range of 2-5%. An interest subvention scheme for cheaper loans and a credit guarantee scheme for plant and machinery are some other possible measures that will help the industry, the official added.“This should be 2.0 (second) version of the electronic manufacturing cluster (EMC) scheme, which is aimed at creating an ecosystem with an anchor company plus its suppliers to operate in the same area,” he said.Last week, finance minister Nirmala Sitharaman announced a series of measures to boost economic growth including a scheme allowing any new manufacturing company incorporated on or after October 1, to pay income tax at 15% provided the company does not avail of any other exemption or incentives.\",\n    \"url\": \"https://economictimes.indiatimes.com/industry/cons-products/electronics/more-sops-needed-to-boost-electronic-manufacturing-top-govt-official/articleshow/71321308.cms\"\n  },\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569528720,\n    \"headline\": \"How to disable comments on your YouTube videos in 2 different ways\",\n    \"id\": 25287,\n    \"image\": \"https://amp.businessinsider.com/images/5d8d16182e22af6ab66c09e9-1536-768.jpg\",\n    \"related\": \"AAPL\",\n    \"source\": \"Business Insider\",\n    \"summary\": \"You can disable comments on your own YouTube video if you don't want people to comment on it. It's easy to disable comments on YouTube by adjusting the settings for one of your videos in the beta or classic version of YouTube Studio. Visit Business Insider's homepage for more stories . The comments section has a somewhat complicated reputation for creators, especially for those making videos on YouTube . While it can be useful to get the unfiltered opinions of your YouTube viewers and possibly forge a closer connection with them, it can also open you up to quite a bit of negativity. So it makes sense that there may be times when you want to turn off the feature entirely. Just keep in mind that the action itself can spark conversation. If you decide that you don't want to let people leave comments on your YouTube video, here's how to turn off the feature, using either the classic or beta version of the creator studio: How to disable comments on YouTube in YouTube Studio (beta) 1. Go to youtube.com and log into your account, if necessary. 2.\",\n    \"url\": \"https://www.businessinsider.com/how-to-disable-comments-on-youtube\"\n  },\n  {\n    \"category\": \"company news\",\n    \"datetime\": 1569526180,\n    \"headline\": \"Apple iPhone 11 Pro Teardowns Look Encouraging for STMicro and Sony\",\n    \"id\": 25341,\n    \"image\": \"http://s.thestreet.com/files/tsc/v2008/photos/contrib/uploads/ba140938-d409-11e9-822b-fda891ce1fc1.png\",\n    \"related\": \"AAPL\",\n    \"source\": \"TheStreet\",\n    \"summary\": \"STMicroelectronics and Sony each appear to be supplying four chips for Apple's latest flagship iPhones. Many other historical iPhone suppliers also make appearances in the latest teardowns….STM\",\n    \"url\": \"https://realmoney.thestreet.com/investing/technology/iphone-11-pro-teardowns-look-encouraging-for-stmicro-sony-15105767\"\n  },\n]"
  suggestedFilename: "company-news"
---

# Company News

## 源URL

https://finnhub.io/docs/api/company-news

## 描述

List latest company news by symbol. This endpoint is only available for North American companies.

## API 端点

**Method**: `GET`
**Endpoint**: `/company-news?symbol=AAPL&from=2025-05-15&to=2025-06-20`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Company symbol. |
| `from` | string | 是 | - | From date YYYY-MM-DD. |
| `to` | string | 是 | - | To date YYYY-MM-DD. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.companyNews("AAPL", "2020-01-01", "2020-05-01", (error, data, response) => {
	console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.company_news('AAPL', _from="2020-06-01", to="2020-06-10"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CompanyNews(context.Background()).Symbol("AAPL").From("2020-05-01").To("2020-05-01").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->companyNews("AAPL", "2020-06-01", "2020-06-10"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.company_news('AAPL', "2020-06-01", "2020-06-10"))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.companyNews("AAPL", from = "2020-06-01", to = "2020-06-10"))
```

### 示例 7 (json)

```json
[
  {
    "category": "company news",
    "datetime": 1569550360,
    "headline": "More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official.  More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official",
    "id": 25286,
    "image": "https://img.etimg.com/thumb/msid-71321314,width-1070,height-580,imgsize-481831,overlay-economictimes/photo.jpg",
    "related": "AAPL",
    "source": "The Economic Times India",
    "summary": "NEW DELHI | CHENNAI: India may have to offer electronic manufacturers additional sops such as cheap credit and incentives for export along with infrastructure support in order to boost production and help the sector compete with China, Vietnam and Thailand, according to a top government official.These incentives, over and above the proposed reduction of corporate tax to 15% for new manufacturing units, are vital for India to successfully attract companies looking to relocate manufacturing facilities.“While the tax announcements made last week send a very good signal, in order to help attract investments, we will need additional initiatives,” the official told ET, pointing out that Indian electronic manufacturers incur 8-10% higher costs compared with other Asian countries.Sops that are similar to the incentives for export under the existing Merchandise Exports from India Scheme (MEIS) are what the industry requires, the person said.MEIS gives tax credit in the range of 2-5%. An interest subvention scheme for cheaper loans and a credit guarantee scheme for plant and machinery are some other possible measures that will help the industry, the official added.“This should be 2.0 (second) version of the electronic manufacturing cluster (EMC) scheme, which is aimed at creating an ecosystem with an anchor company plus its suppliers to operate in the same area,” he said.Last week, finance minister Nirmala Sitharaman announced a series of measures to boost economic growth including a scheme allowing any new manufacturing company incorporated on or after October 1, to pay income tax at 15% provided the company does not avail of any other exemption or incentives.",
    "url": "https://economictimes.indiatimes.com/industry/cons-products/electronics/more-sops-needed-to-boost-electronic-manufacturing-top-govt-official/articleshow/71321308.cms"
  },
  {
    "category": "company news",
    "datetime": 1569528720,
    "headline": "How to disable comments on your YouTube videos in 2 different ways",
    "id": 25287,
    "image": "https://amp.businessinsider.com/images/5d8d16182e22af6ab66c09e9-1536-768.jpg",
    "related": "AAPL",
    "source": "Business Insider",
    "summary": "You can disable comments on your own YouTube video if you don't want people to comment on it. It's easy to disable comments on YouTube by adjusting the settings for one of your videos in the beta or classic version of YouTube Studio. Visit Business Insider's homepage for more stories . The comments section has a somewhat complicated reputation for creators, especially for those making videos on YouTube . While it can be useful to get the unfiltered opinions of your YouTube viewers and possibly forge a closer connection with them, it can also open you up to quite a bit of negativity. So it makes sense that there may be times when you want to turn off the feature entirely. Just keep in mind that the action itself can spark conversation. If you decide that you don't want to let people leave comments on your YouTube video, here's how to turn off the feature, using either the classic or beta version of the creator studio: How to disable comments on YouTube in YouTube Studio (beta) 1. Go to youtube.com and log into your account, if necessary. 2.",
    "url": "https://www.businessinsider.com/how-to-disable-comments-on-youtube"
  },
  {
    "category": "company news",
    "datetime": 1569526180,
    "headline": "Apple iPhone 11 Pro Teardowns Look Encouraging for STMicro and Sony",
    "id": 25341,
    "image": "http://s.thestreet.com/files/tsc/v2008/photos/contrib/uploads/ba140938-d409-11e9-822b-fda891ce1fc1.png",
    "related": "AAPL",
    "source": "TheStreet",
    "summary": "STMicroelectronics and Sony each appear to be supplying four chips for Apple's latest flagship iPhones. Many other historical iPhone suppliers also make appearances in the latest teardowns….STM",
    "url": "https://realmoney.thestreet.com/investing/technology/iphone-11-pro-teardowns-look-encouraging-for-stmicro-sony-15105767"
  },
]
```

## 文档正文

List latest company news by symbol. This endpoint is only available for North American companies.

## API 端点

**Method:** `GET`
**Endpoint:** `/company-news?symbol=AAPL&from=2025-05-15&to=2025-06-20`

Company News

List latest company news by symbol. This endpoint is only available for North American companies.

Method: GET

Free Tier: 1 year of historical news and new updates

Examples:

/company-news?symbol=AAPL&from=2025-05-15&to=2025-06-20

Arguments:

symbolREQUIRED

Company symbol.

fromREQUIRED

From date YYYY-MM-DD.

toREQUIRED

To date YYYY-MM-DD.

Response Attributes:

category

News category.

datetime

Published time in UNIX timestamp.

headline

News headline.

id

News ID. This value can be used for minId params to get the latest news only.

image

Thumbnail image URL.

related

Related stocks and companies mentioned in the article.

source

News source.

summary

News summary.

url

URL of the original article.

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

print(finnhub_client.company_news('AAPL', _from="2020-06-01", to="2020-06-10"))

Sample response

[
  {
    "category": "company news",
    "datetime": 1569550360,
    "headline": "More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official.  More sops needed to boost electronic manufacturing: Top govt official More sops needed to boost electronic manufacturing: Top govt official",
    "id": 25286,
    "image": "https://img.etimg.com/thumb/msid-71321314,width-1070,height-580,imgsize-481831,overlay-economictimes/photo.jpg",
    "related": "AAPL",
    "source": "The Economic Times India",
    "summary": "NEW DELHI | CHENNAI: India may have to offer electronic manufacturers additional sops such as cheap credit and incentives for export along with infrastructure support in order to boost production and help the sector compete with China, Vietnam and Thailand, according to a top government official.These incentives, over and above the proposed reduction of corporate tax to 15% for new manufacturing units, are vital for India to successfully attract companies looking to relocate manufacturing facilities.“While the tax announcements made last week send a very good signal, in order to help attract investments, we will need additional initiatives,” the official told ET, pointing out that Indian electronic manufacturers incur 8-10% higher costs compared with other Asian countries.Sops that are similar to the incentives for export under the existing Merchandise Exports from India Scheme (MEIS) are what the industry requires, the person said.MEIS gives tax credit in the range of 2-5%. An interest subvention scheme for cheaper loans and a credit guarantee scheme for plant and machinery are some other possible measures that will help the industry, the official added.“This should be 2.0 (second) version of the electronic manufacturing cluster (EMC) scheme, which is aimed at creating an ecosystem with an anchor company plus its suppliers to operate in the same area,” he said.Last week, finance minister Nirmala Sitharaman announced a series of measures to boost economic growth including a scheme allowing any new manufacturing company incorporated on or after October 1, to pay income tax at 15% provided the company does not avail of any other exemption or incentives.",
    "url": "https://economictimes.indiatimes.com/industry/cons-products/electronics/more-sops-needed-to-boost-electronic-manufacturing-top-govt-official/articleshow/71321308.cms"
  },
  {
    "category": "company news",
    "datetime": 1569528720,
    "headline": "How to disable comments on your YouTube videos in 2 different ways",
    "id": 25287,
    "image": "https://amp.businessinsider.com/images/5d8d16182e22af6ab66c09e9-1536-768.jpg",
    "related": "AAPL",
    "source": "Business Insider",
    "summary": "You can disable comments on your own YouTube video if you don't want people to comment on it. It's easy to disable comments on YouTube by adjusting the settings for one of your videos in the beta or classic version of YouTube Studio. Visit Business Insider's homepage for more stories . The comments section has a somewhat complicated reputation for creators, especially for those making videos on YouTube . While it can be useful to get the unfiltered opinions of your YouTube viewers and possibly forge a closer connection with them, it can also open you up to quite a bit of negativity. So it makes sense that there may be times when you want to turn off the feature entirely. Just keep in mind that the action itself can spark conversation. If you decide that you don't want to let people leave comments on your YouTube video, here's how to turn off the feature, using either the classic or beta version of the creator studio: How to disable comments on YouTube in YouTube Studio (beta) 1. Go to youtube.com and log into your account, if necessary. 2.",
    "url": "https://www.businessinsider.com/how-to-disable-comments-on-youtube"
  },
  {
    "category": "company news",
    "datetime": 1569526180,
    "headline": "Apple iPhone 11 Pro Teardowns Lo
