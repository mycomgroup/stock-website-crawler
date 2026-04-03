---
id: "url-5be773fe"
type: "api"
title: "Usage"
url: "https://docs.tavily.com/documentation/api-reference/endpoint/usage"
description: "Get API key and account usage details"
source: ""
tags: []
crawl_time: "2026-03-18T07:16:16.978Z"
metadata:
  method: "GET"
  endpoint: "/usage"
  baseUrl: "https://api.tavily.com"
  parameters:
    - {"name":"Authorization","type":"string","required":true,"default":"","description":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).","location":"header"}
    - {"name":"X-Project-ID","type":"string","required":false,"default":"","description":"Optional project ID to scope the usage query to a specific project"}
    - {"name":"key.usage","type":"integer","required":false,"default":"","description":"Total credits used for this API key during the current billing cycleExample:150"}
    - {"name":"key.limit","type":"integer","required":false,"default":"","description":"Usage limit for the API key. Returns null if unlimitedExample:1000"}
    - {"name":"key.search_usage","type":"integer","required":false,"default":"","description":"Search endpoint credits used for this API key during the current billing cycleExample:100"}
    - {"name":"key.extract_usage","type":"integer","required":false,"default":"","description":"Extract endpoint credits used for this API key during the current billing cycleExample:25"}
    - {"name":"key.crawl_usage","type":"integer","required":false,"default":"","description":"Crawl endpoint credits used for this API key during the current billing cycleExample:15"}
    - {"name":"key.map_usage","type":"integer","required":false,"default":"","description":"Map endpoint credits used for this API key during the current billing cycleExample:7"}
    - {"name":"key.research_usage","type":"integer","required":false,"default":"","description":"Research endpoint credits used for this API key during the current billing cycleExample:3"}
    - {"name":"account.current_plan","type":"string","required":false,"default":"","description":"The current subscription plan nameExample:\"Bootstrap\""}
    - {"name":"account.plan_usage","type":"integer","required":false,"default":"","description":"Total credits used for this plan during the current billing cycleExample:500"}
    - {"name":"account.plan_limit","type":"integer","required":false,"default":"","description":"Usage limit for the current planExample:15000"}
    - {"name":"account.paygo_usage","type":"integer","required":false,"default":"","description":"Current pay-as-you-go usage countExample:25"}
    - {"name":"account.paygo_limit","type":"integer","required":false,"default":"","description":"Pay-as-you-go usage limitExample:100"}
    - {"name":"account.search_usage","type":"integer","required":false,"default":"","description":"Search endpoint credits used for this plan during the current billing cycleExample:350"}
    - {"name":"account.extract_usage","type":"integer","required":false,"default":"","description":"Extract endpoint credits used for this plan during the current billing cycleExample:75"}
    - {"name":"account.crawl_usage","type":"integer","required":false,"default":"","description":"Crawl endpoint credits used for this plan during the current billing cycleExample:50"}
    - {"name":"account.map_usage","type":"integer","required":false,"default":"","description":"Map endpoint credits used for this plan during the current billing cycleExample:15"}
    - {"name":"account.research_usage","type":"integer","required":false,"default":"","description":"Research endpoint credits used for this plan during the current billing cycleExample:10"}
    - {"name":"key","type":"object","required":false,"default":"","description":"Hide child attributes​key.usageintegerTotal credits used for this API key during the current billing cycleExample:150​key.limitintegerUsage limit for the API key. Returns null if unlimitedExample:1000​key.search_usageintegerSearch endpoint credits used for this API key during the current billing cycleExample:100​key.extract_usageintegerExtract endpoint credits used for this API key during the current billing cycleExample:25​key.crawl_usageintegerCrawl endpoint credits used for this API key durin"}
    - {"name":"account","type":"object","required":false,"default":"","description":"Account plan and usage informationHide child attributes​account.current_planstringThe current subscription plan nameExample:\"Bootstrap\"​account.plan_usageintegerTotal credits used for this plan during the current billing cycleExample:500​account.plan_limitintegerUsage limit for the current planExample:15000​account.paygo_usageintegerCurrent pay-as-you-go usage countExample:25​account.paygo_limitintegerPay-as-you-go usage limitExample:100​account.search_usageintegerSearch endpoint credits used fo"}
  requestHeaders: []
  responseStructure: []
  examples:
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.tavily.com/usage \\\n  --header 'Authorization: Bearer <token>'"}
    - {"language":"json","code":"{\n  \"key\": {\n    \"usage\": 150,\n    \"limit\": 1000,\n    \"search_usage\": 100,\n    \"extract_usage\": 25,\n    \"crawl_usage\": 15,\n    \"map_usage\": 7,\n    \"research_usage\": 3\n  },\n  \"account\": {\n    \"current_plan\": \"Bootstrap\",\n    \"plan_usage\": 500,\n    \"plan_limit\": 15000,\n    \"paygo_usage\": 25,\n    \"paygo_limit\": 100,\n    \"search_usage\": 350,\n    \"extract_usage\": 75,\n    \"crawl_usage\": 50,\n    \"map_usage\": 15,\n    \"research_usage\": 10\n  }\n}"}
    - {"language":"bash","code":"curl --request GET \\\n  --url https://api.tavily.com/usage \\\n  --header 'Authorization: Bearer <token>'"}
    - {"language":"json","code":"{\n  \"key\": {\n    \"usage\": 150,\n    \"limit\": 1000,\n    \"search_usage\": 100,\n    \"extract_usage\": 25,\n    \"crawl_usage\": 15,\n    \"map_usage\": 7,\n    \"research_usage\": 3\n  },\n  \"account\": {\n    \"current_plan\": \"Bootstrap\",\n    \"plan_usage\": 500,\n    \"plan_limit\": 15000,\n    \"paygo_usage\": 25,\n    \"paygo_limit\": 100,\n    \"search_usage\": 350,\n    \"extract_usage\": 75,\n    \"crawl_usage\": 50,\n    \"map_usage\": 15,\n    \"research_usage\": 10\n  }\n}"}
  mainContent:
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Headers"}
    - {"type":"paragraph","content":"Optional project ID to scope the usage query to a specific project"}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Usage details returned successfully"}
    - {"type":"parameter","name":"150","paramType":"","description":"​keyobjectHide child attributes​key.usageintegerTotal credits used for this API key during the current billing cycleExample:150​key.limitintegerUsage limit for the API key. Returns null if unlimitedExample:1000​key.search_usageintegerSearch endpoint credits used for this API key during the current billing cycleExample:100​key.extract_usageintegerExtract endpoint credits used for this API key during the current billing cycleExample:25​key.crawl_usageintegerCrawl endpoint credits used for this API key during the current billing cycleExample:15​key.map_usageintegerMap endpoint credits used for this API key during the current billing cycleExample:7​key.research_usageintegerResearch endpoint credits used for this API key during the current billing cycleExample:3​accountobjectAccount plan and usage informationHide child attributes​account.current_planstringThe current subscription plan nameExample:\"Bootstrap\"​account.plan_usageintegerTotal credits used for this plan during the current billing cycleExample:500​account.plan_limitintegerUsage limit for the current planExample:15000​account.paygo_usageintegerCurrent pay-as-you-go usage countExample:25​account.paygo_limitintegerPay-as-you-go usage limitExample:100​account.search_usageintegerSearch endpoint credits used for this plan during the current billing cycleExample:350​account.extract_usageintegerExtract endpoint credits used for this plan during the current billing cycleExample:75​account.crawl_usageintegerCrawl endpoint credits used for this plan during the current billing cycleExample:50​account.map_usageintegerMap endpoint credits used for this plan during the current billing cycleExample:15​account.research_usageintegerResearch endpoint credits used for this plan during the current billing cycleExample:10"}
  rawContent: "Authorizations\n​\nAuthorization\nstringheaderrequired\n\nBearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).\n\nHeaders\n​\nX-Project-ID\nstring\n\nOptional project ID to scope the usage query to a specific project\n\nResponse\n200\napplication/json\n\nUsage details returned successfully\n\n​\nkey\nobject\n\nHide child attributes\n\n​\nkey.usage\ninteger\n\nTotal credits used for this API key during the current billing cycle\n\nExample:\n\n150\n\n​\nkey.limit\ninteger\n\nUsage limit for the API key. Returns null if unlimited\n\nExample:\n\n1000\n\n​\nkey.search_usage\ninteger\n\nSearch endpoint credits used for this API key during the current billing cycle\n\nExample:\n\n100\n\n​\nkey.extract_usage\ninteger\n\nExtract endpoint credits used for this API key during the current billing cycle\n\nExample:\n\n25\n\n​\nkey.crawl_usage\ninteger\n\nCrawl endpoint credits used for this API key during the current billing cycle\n\nExample:\n\n15\n\n​\nkey.map_usage\ninteger\n\nMap endpoint credits used for this API key during the current billing cycle\n\nExample:\n\n7\n\n​\nkey.research_usage\ninteger\n\nResearch endpoint credits used for this API key during the current billing cycle\n\nExample:\n\n3\n\n​\naccount\nobject\n\nAccount plan and usage information\n\nHide child attributes\n\n​\naccount.current_plan\nstring\n\nThe current subscription plan name\n\nExample:\n\n\"Bootstrap\"\n\n​\naccount.plan_usage\ninteger\n\nTotal credits used for this plan during the current billing cycle\n\nExample:\n\n500\n\n​\naccount.plan_limit\ninteger\n\nUsage limit for the current plan\n\nExample:\n\n15000\n\n​\naccount.paygo_usage\ninteger\n\nCurrent pay-as-you-go usage count\n\nExample:\n\n25\n\n​\naccount.paygo_limit\ninteger\n\nPay-as-you-go usage limit\n\nExample:\n\n100\n\n​\naccount.search_usage\ninteger\n\nSearch endpoint credits used for this plan during the current billing cycle\n\nExample:\n\n350\n\n​\naccount.extract_usage\ninteger\n\nExtract endpoint credits used for this plan during the current billing cycle\n\nExample:\n\n75\n\n​\naccount.crawl_usage\ninteger\n\nCrawl endpoint credits used for this plan during the current billing cycle\n\nExample:\n\n50\n\n​\naccount.map_usage\ninteger\n\nMap endpoint credits used for this plan during the current billing cycle\n\nExample:\n\n15\n\n​\naccount.research_usage\ninteger\n\nResearch endpoint credits used for this plan during the current billing cycle\n\nExample:\n\n10"
  suggestedFilename: "endpoint_usage"
---

# Usage

## 源URL

https://docs.tavily.com/documentation/api-reference/endpoint/usage

## 描述

Get API key and account usage details

## API 端点

**Method**: `GET`
**Endpoint**: `/usage`
**Base URL**: `https://api.tavily.com`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `Authorization` | string | 是 | - | Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY). |
| `X-Project-ID` | string | 否 | - | Optional project ID to scope the usage query to a specific project |
| `key.usage` | integer | 否 | - | Total credits used for this API key during the current billing cycleExample:150 |
| `key.limit` | integer | 否 | - | Usage limit for the API key. Returns null if unlimitedExample:1000 |
| `key.search_usage` | integer | 否 | - | Search endpoint credits used for this API key during the current billing cycleExample:100 |
| `key.extract_usage` | integer | 否 | - | Extract endpoint credits used for this API key during the current billing cycleExample:25 |
| `key.crawl_usage` | integer | 否 | - | Crawl endpoint credits used for this API key during the current billing cycleExample:15 |
| `key.map_usage` | integer | 否 | - | Map endpoint credits used for this API key during the current billing cycleExample:7 |
| `key.research_usage` | integer | 否 | - | Research endpoint credits used for this API key during the current billing cycleExample:3 |
| `account.current_plan` | string | 否 | - | The current subscription plan nameExample:"Bootstrap" |
| `account.plan_usage` | integer | 否 | - | Total credits used for this plan during the current billing cycleExample:500 |
| `account.plan_limit` | integer | 否 | - | Usage limit for the current planExample:15000 |
| `account.paygo_usage` | integer | 否 | - | Current pay-as-you-go usage countExample:25 |
| `account.paygo_limit` | integer | 否 | - | Pay-as-you-go usage limitExample:100 |
| `account.search_usage` | integer | 否 | - | Search endpoint credits used for this plan during the current billing cycleExample:350 |
| `account.extract_usage` | integer | 否 | - | Extract endpoint credits used for this plan during the current billing cycleExample:75 |
| `account.crawl_usage` | integer | 否 | - | Crawl endpoint credits used for this plan during the current billing cycleExample:50 |
| `account.map_usage` | integer | 否 | - | Map endpoint credits used for this plan during the current billing cycleExample:15 |
| `account.research_usage` | integer | 否 | - | Research endpoint credits used for this plan during the current billing cycleExample:10 |
| `key` | object | 否 | - | Hide child attributeskey.usageintegerTotal credits used for this API key during the current billing cycleExample:150key.limitintegerUsage limit for the API key. Returns null if unlimitedExample:1000key.search_usageintegerSearch endpoint credits used for this API key during the current billing cycleExample:100key.extract_usageintegerExtract endpoint credits used for this API key during the current billing cycleExample:25key.crawl_usageintegerCrawl endpoint credits used for this API key durin |
| `account` | object | 否 | - | Account plan and usage informationHide child attributesaccount.current_planstringThe current subscription plan nameExample:"Bootstrap"account.plan_usageintegerTotal credits used for this plan during the current billing cycleExample:500account.plan_limitintegerUsage limit for the current planExample:15000account.paygo_usageintegerCurrent pay-as-you-go usage countExample:25account.paygo_limitintegerPay-as-you-go usage limitExample:100account.search_usageintegerSearch endpoint credits used fo |

## 代码示例

### 示例 1 (bash)

```bash
curl --request GET \
  --url https://api.tavily.com/usage \
  --header 'Authorization: Bearer <token>'
```

### 示例 2 (json)

```json
{
  "key": {
    "usage": 150,
    "limit": 1000,
    "search_usage": 100,
    "extract_usage": 25,
    "crawl_usage": 15,
    "map_usage": 7,
    "research_usage": 3
  },
  "account": {
    "current_plan": "Bootstrap",
    "plan_usage": 500,
    "plan_limit": 15000,
    "paygo_usage": 25,
    "paygo_limit": 100,
    "search_usage": 350,
    "extract_usage": 75,
    "crawl_usage": 50,
    "map_usage": 15,
    "research_usage": 10
  }
}
```

## 文档正文

Get API key and account usage details

## API 端点

**Method:** `GET`
**Endpoint:** `/usage`

Authorizations

Authorization
stringheaderrequired

Bearer authentication header in the form Bearer , where is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

Headers

X-Project-ID
string

Optional project ID to scope the usage query to a specific project

Response
200
application/json

Usage details returned successfully

key
object

Hide child attributes

key.usage
integer

Total credits used for this API key during the current billing cycle

Example:

150

key.limit
integer

Usage limit for the API key. Returns null if unlimited

Example:

1000

key.search_usage
integer

Search endpoint credits used for this API key during the current billing cycle

Example:

100

key.extract_usage
integer

Extract endpoint credits used for this API key during the current billing cycle

Example:

25

key.crawl_usage
integer

Crawl endpoint credits used for this API key during the current billing cycle

Example:

15

key.map_usage
integer

Map endpoint credits used for this API key during the current billing cycle

Example:

7

key.research_usage
integer

Research endpoint credits used for this API key during the current billing cycle

Example:

3

account
object

Account plan and usage information

Hide child attributes

account.current_plan
string

The current subscription plan name

Example:

"Bootstrap"

account.plan_usage
integer

Total credits used for this plan during the current billing cycle

Example:

500

account.plan_limit
integer

Usage limit for the current plan

Example:

15000

account.paygo_usage
integer

Current pay-as-you-go usage count

Example:

25

account.paygo_limit
integer

Pay-as-you-go usage limit

Example:

100

account.search_usage
integer

Search endpoint credits used for this plan during the current billing cycle

Example:

350

account.extract_usage
integer

Extract endpoint credits used for this plan during the current billing cycle

Example:

75

account.crawl_usage
integer

Crawl endpoint credits used for this plan during the current billing cycle

Example:

50

account.map_usage
integer

Map endpoint credits used for this plan during the current billing cycle

Example:

15

account.research_usage
integer

Research endpoint credits used for this plan during the current billing cycle

Example:

10
