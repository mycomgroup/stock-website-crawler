---
id: "url-77e489cc"
type: "api"
title: "Institutional Profile Premium"
url: "https://finnhub.io/docs/api/institutional-profile"
description: "Get a list of well-known institutional investors. Currently support 60+ profiles."
source: ""
tags: []
crawl_time: "2026-03-18T09:27:25.724Z"
metadata:
  requestMethod: "GET"
  endpoint: "/institutional/profile"
  parameters:
    - {"name":"cik","in":"query","required":false,"type":"string","description":"Filter by CIK. Leave blank to get the full list."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.institutionalProfile({\"cik\": \"\"}, (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.institutional_profile()"}
    - {"language":"Go","code":"res, _, err := finnhubClient.InstitutionalProfile(context.Background()).Execute()"}
    - {"language":"PHP","code":"print_r($client->institutionalProfile());"}
    - {"language":"Ruby","code":"puts(finnhub_client.institutional_profile({cik: \"\"}))"}
    - {"language":"Kotlin","code":"println(apiClient.institutionalProfile())"}
  sampleResponse: "{\n  \"cik\": \"1067983\",\n  \"data\": [\n    {\n      \"cik\": \"1067983\",\n      \"firmType\": \"Institutional Investment Manager\",\n      \"manager\": \"Warren Buffett\",\n      \"philosophy\": \"Value investing is the hallmark of Warren Buffett's investment approach. By choosing stocks whose share price is below their intrinsic or book value, value investors can increase their returns. This suggests that the stock will increase in value going forward and that the market is now undervaluing it. Only enterprises that Buffett is familiar with are chosen for investment by Berkshire, and a safety margin is always required.\",\n      \"profile\": \"Warren Edward Buffett (born August 30, 1930) is an American business magnate, investor, and philanthropist. He is currently the chairman and CEO of Berkshire Hathaway. He is one of the most successful investors in the world and has a net worth of over $103 billion as of August 2022, making him the world's seventh-wealthiest person. Buffett has been the chairman and largest shareholder of Berkshire Hathaway since 1970. He has been referred to as the \\\"Oracle\\\" or \\\"Sage\\\" of Omaha by global media. He is noted for his adherence to value investing, and his personal frugality despite his immense wealth. Buffett is a philanthropist, having pledged to give away 99 percent of his fortune to philanthropic causes, primarily via the Bill \\u0026 Melinda Gates Foundation. He founded The Giving Pledge in 2010 with Bill Gates, whereby billionaires pledge to give away at least half of their fortunes.\",\n      \"profileImg\": \"https://static4.finnhub.io/file/publicdatany5/guru_profile_pic/1067983.jpg\"\n    }\n  ]\n}"
  curlExample: ""
  jsonExample: "{\n  \"cik\": \"1067983\",\n  \"data\": [\n    {\n      \"cik\": \"1067983\",\n      \"firmType\": \"Institutional Investment Manager\",\n      \"manager\": \"Warren Buffett\",\n      \"philosophy\": \"Value investing is the hallmark of Warren Buffett's investment approach. By choosing stocks whose share price is below their intrinsic or book value, value investors can increase their returns. This suggests that the stock will increase in value going forward and that the market is now undervaluing it. Only enterprises that Buffett is familiar with are chosen for investment by Berkshire, and a safety margin is always required.\",\n      \"profile\": \"Warren Edward Buffett (born August 30, 1930) is an American business magnate, investor, and philanthropist. He is currently the chairman and CEO of Berkshire Hathaway. He is one of the most successful investors in the world and has a net worth of over $103 billion as of August 2022, making him the world's seventh-wealthiest person. Buffett has been the chairman and largest shareholder of Berkshire Hathaway since 1970. He has been referred to as the \\\"Oracle\\\" or \\\"Sage\\\" of Omaha by global media. He is noted for his adherence to value investing, and his personal frugality despite his immense wealth. Buffett is a philanthropist, having pledged to give away 99 percent of his fortune to philanthropic causes, primarily via the Bill \\u0026 Melinda Gates Foundation. He founded The Giving Pledge in 2010 with Bill Gates, whereby billionaires pledge to give away at least half of their fortunes.\",\n      \"profileImg\": \"https://static4.finnhub.io/file/publicdatany5/guru_profile_pic/1067983.jpg\"\n    }\n  ]\n}"
  rawContent: "Institutional Profile Premium\n\nGet a list of well-known institutional investors. Currently support 60+ profiles.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/institutional/profile\n\nArguments:\n\ncikoptional\n\nFilter by CIK. Leave blank to get the full list.\n\nResponse Attributes:\n\ncik\n\nCIK.\n\ndata\n\nArray of investors.\n\ncik\n\nInvestor's company CIK.\n\nfirmType\n\nFirm type.\n\nmanager\n\nManager.\n\nphilosophy\n\nInvesting philosophy.\n\nprofile\n\nProfile info.\n\nprofileImg\n\nProfile image.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.institutional_profile()\n\nSample response\n\n{\n  \"cik\": \"1067983\",\n  \"data\": [\n    {\n      \"cik\": \"1067983\",\n      \"firmType\": \"Institutional Investment Manager\",\n      \"manager\": \"Warren Buffett\",\n      \"philosophy\": \"Value investing is the hallmark of Warren Buffett's investment approach. By choosing stocks whose share price is below their intrinsic or book value, value investors can increase their returns. This suggests that the stock will increase in value going forward and that the market is now undervaluing it. Only enterprises that Buffett is familiar with are chosen for investment by Berkshire, and a safety margin is always required.\",\n      \"profile\": \"Warren Edward Buffett (born August 30, 1930) is an American business magnate, investor, and philanthropist. He is currently the chairman and CEO of Berkshire Hathaway. He is one of the most successful investors in the world and has a net worth of over $103 billion as of August 2022, making him the world's seventh-wealthiest person. Buffett has been the chairman and largest shareholder of Berkshire Hathaway since 1970. He has been referred to as the \\\"Oracle\\\" or \\\"Sage\\\" of Omaha by global media. He is noted for his adherence to value investing, and his personal frugality despite his immense wealth. Buffett is a philanthropist, having pledged to give away 99 percent of his fortune to philanthropic causes, primarily via the Bill \\u0026 Melinda Gates Foundation. He founded The Giving Pledge in 2010 with Bill Gates, whereby billionaires pledge to give away at least half of their fortunes.\",\n      \"profileImg\": \"https://static4.finnhub.io/file/publicdatany5/guru_profile_pic/1067983.jpg\"\n    }\n  ]\n}"
  suggestedFilename: "institutional-profile"
---

# Institutional Profile Premium

## 源URL

https://finnhub.io/docs/api/institutional-profile

## 描述

Get a list of well-known institutional investors. Currently support 60+ profiles.

## API 端点

**Method**: `GET`
**Endpoint**: `/institutional/profile`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `cik` | string | 否 | - | Filter by CIK. Leave blank to get the full list. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.institutionalProfile({"cik": ""}, (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.institutional_profile()
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.InstitutionalProfile(context.Background()).Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->institutionalProfile());
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.institutional_profile({cik: ""}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.institutionalProfile())
```

### 示例 7 (json)

```json
{
  "cik": "1067983",
  "data": [
    {
      "cik": "1067983",
      "firmType": "Institutional Investment Manager",
      "manager": "Warren Buffett",
      "philosophy": "Value investing is the hallmark of Warren Buffett's investment approach. By choosing stocks whose share price is below their intrinsic or book value, value investors can increase their returns. This suggests that the stock will increase in value going forward and that the market is now undervaluing it. Only enterprises that Buffett is familiar with are chosen for investment by Berkshire, and a safety margin is always required.",
      "profile": "Warren Edward Buffett (born August 30, 1930) is an American business magnate, investor, and philanthropist. He is currently the chairman and CEO of Berkshire Hathaway. He is one of the most successful investors in the world and has a net worth of over $103 billion as of August 2022, making him the world's seventh-wealthiest person. Buffett has been the chairman and largest shareholder of Berkshire Hathaway since 1970. He has been referred to as the \"Oracle\" or \"Sage\" of Omaha by global media. He is noted for his adherence to value investing, and his personal frugality despite his immense wealth. Buffett is a philanthropist, having pledged to give away 99 percent of his fortune to philanthropic causes, primarily via the Bill \u0026 Melinda Gates Foundation. He founded The Giving Pledge in 2010 with Bill Gates, whereby billionaires pledge to give away at least half of their fortunes.",
      "profileImg": "https://static4.finnhub.io/file/publicdatany5/guru_profile_pic/1067983.jpg"
    }
  ]
}
```

## 文档正文

Get a list of well-known institutional investors. Currently support 60+ profiles.

## API 端点

**Method:** `GET`
**Endpoint:** `/institutional/profile`

Institutional Profile Premium

Get a list of well-known institutional investors. Currently support 60+ profiles.

Method: GET

Premium: Premium Access Required

Examples:

/institutional/profile

Arguments:

cikoptional

Filter by CIK. Leave blank to get the full list.

Response Attributes:

cik

CIK.

data

Array of investors.

cik

Investor's company CIK.

firmType

Firm type.

manager

Manager.

philosophy

Investing philosophy.

profile

Profile info.

profileImg

Profile image.

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

print(finnhub_client.institutional_profile()

Sample response

{
  "cik": "1067983",
  "data": [
    {
      "cik": "1067983",
      "firmType": "Institutional Investment Manager",
      "manager": "Warren Buffett",
      "philosophy": "Value investing is the hallmark of Warren Buffett's investment approach. By choosing stocks whose share price is below their intrinsic or book value, value investors can increase their returns. This suggests that the stock will increase in value going forward and that the market is now undervaluing it. Only enterprises that Buffett is familiar with are chosen for investment by Berkshire, and a safety margin is always required.",
      "profile": "Warren Edward Buffett (born August 30, 1930) is an American business magnate, investor, and philanthropist. He is currently the chairman and CEO of Berkshire Hathaway. He is one of the most successful investors in the world and has a net worth of over $103 billion as of August 2022, making him the world's seventh-wealthiest person. Buffett has been the chairman and largest shareholder of Berkshire Hathaway since 1970. He has been referred to as the \"Oracle\" or \"Sage\" of Omaha by global media. He is noted for his adherence to value investing, and his personal frugality despite his immense wealth. Buffett is a philanthropist, having pledged to give away 99 percent of his fortune to philanthropic causes, primarily via the Bill \u0026 Melinda Gates Foundation. He founded The Giving Pledge in 2010 with Bill Gates, whereby billionaires pledge to give away at least half of their fortunes.",
      "profileImg": "https://static4.finnhub.io/file/publicdatany5/guru_profile_pic/1067983.jpg"
    }
  ]
}
