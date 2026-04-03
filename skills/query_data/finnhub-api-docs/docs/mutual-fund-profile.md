---
id: "url-3d95796f"
type: "api"
title: "mutual-fund-profile"
url: "https://finnhub.io/docs/api/mutual-fund-profile"
description: "Get mutual funds profile information. This endpoint covers both US and global mutual funds. For international funds, you must query the data using ISIN. A list of supported funds can be found here."
source: ""
tags: []
crawl_time: "2026-03-18T08:35:31.013Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/v1/mutual-fund/profile"
  parameters:
    - {"name":"symbol","in":"query","required":false,"type":"string","description":"Fund's symbol."}
    - {"name":"isin","in":"query","required":false,"type":"string","description":"Fund's isin."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.mutualFundProfile({'symbol': 'VTSAX'}, (error, data, response) => {\n  console.log(data);\n});"}
    - {"language":"Python","code":"print(finnhub_client.mutual_fund_profile(\"VTSAX\"))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.MutualFundProfile(context.Background()).Symbol(\"VTSAX\").Execute()"}
    - {"language":"PHP","code":"print_r($client->mutualFundProfile(\"VTSAX\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.mutual_fund_profile({symbol:'VTSAX'}))"}
    - {"language":"Kotlin","code":"println(apiClient.mutualFundProfile(\"VTSAX\", \"\"))"}
  sampleResponse: "{\n  \"profile\": {\n    \"benchmark\": \"CRSP US Total Stock Market TR\",\n    \"beta\": 1.05,\n    \"category\": \"Multi-Cap Core\",\n    \"cusip\": \"\",\n    \"deferredLoad\": 0,\n    \"description\": \"Created in 1992, Vanguard Total Stock Market Index Fund is designed to provide investors with exposure to the entire U.S. equity market, including small-, mid-, and large-cap growth and value stocks. The fund’s key attributes are its low costs, broad diversification, and the potential for tax efficiency. Investors looking for a low-cost way to gain broad exposure to the U.S. stock market who are willing to accept the volatility that comes with stock market investing may wish to consider this fund as either a core equity holding or your only domestic stock fund.\",\n    \"expenseRatio\": 0.04,\n    \"fee12b1\": 0,\n    \"frontLoad\": 0,\n    \"fundFamily\": \"VANGUARD ADMIRAL\",\n    \"inceptionDate\": \"2000-11-13\",\n    \"investmentSegment\": \"Growth & Income\",\n    \"iraMinInvestment\": 0,\n    \"isin\": \"\",\n    \"manager\": \"O'Reilly,Nejman\",\n    \"maxRedemptionFee\": 0,\n    \"name\": \"Vanguard Index Funds: Vanguard Total Stock Market Index Fund; Admiral Class Shares\",\n    \"standardMinInvestment\": 3000,\n    \"status\": \"Open\",\n    \"totalNav\": 280758000000,\n    \"turnover\": 8\n  },\n  \"symbol\": \"VTSAX\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"profile\": {\n    \"benchmark\": \"CRSP US Total Stock Market TR\",\n    \"beta\": 1.05,\n    \"category\": \"Multi-Cap Core\",\n    \"cusip\": \"\",\n    \"deferredLoad\": 0,\n    \"description\": \"Created in 1992, Vanguard Total Stock Market Index Fund is designed to provide investors with exposure to the entire U.S. equity market, including small-, mid-, and large-cap growth and value stocks. The fund’s key attributes are its low costs, broad diversification, and the potential for tax efficiency. Investors looking for a low-cost way to gain broad exposure to the U.S. stock market who are willing to accept the volatility that comes with stock market investing may wish to consider this fund as either a core equity holding or your only domestic stock fund.\",\n    \"expenseRatio\": 0.04,\n    \"fee12b1\": 0,\n    \"frontLoad\": 0,\n    \"fundFamily\": \"VANGUARD ADMIRAL\",\n    \"inceptionDate\": \"2000-11-13\",\n    \"investmentSegment\": \"Growth & Income\",\n    \"iraMinInvestment\": 0,\n    \"isin\": \"\",\n    \"manager\": \"O'Reilly,Nejman\",\n    \"maxRedemptionFee\": 0,\n    \"name\": \"Vanguard Index Funds: Vanguard Total Stock Market Index Fund; Admiral Class Shares\",\n    \"standardMinInvestment\": 3000,\n    \"status\": \"Open\",\n    \"totalNav\": 280758000000,\n    \"turnover\": 8\n  },\n  \"symbol\": \"VTSAX\"\n}"
  rawContent: ""
  suggestedFilename: "mutual-fund-profile"
---

# mutual-fund-profile

## 源URL

https://finnhub.io/docs/api/mutual-fund-profile

## 描述

Get mutual funds profile information. This endpoint covers both US and global mutual funds. For international funds, you must query the data using ISIN. A list of supported funds can be found here.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/v1/mutual-fund/profile`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 否 | - | Fund's symbol. |
| `isin` | string | 否 | - | Fund's isin. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.mutualFundProfile({'symbol': 'VTSAX'}, (error, data, response) => {
  console.log(data);
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.mutual_fund_profile("VTSAX"))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.MutualFundProfile(context.Background()).Symbol("VTSAX").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->mutualFundProfile("VTSAX"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.mutual_fund_profile({symbol:'VTSAX'}))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.mutualFundProfile("VTSAX", ""))
```

### 示例 7 (json)

```json
{
  "profile": {
    "benchmark": "CRSP US Total Stock Market TR",
    "beta": 1.05,
    "category": "Multi-Cap Core",
    "cusip": "",
    "deferredLoad": 0,
    "description": "Created in 1992, Vanguard Total Stock Market Index Fund is designed to provide investors with exposure to the entire U.S. equity market, including small-, mid-, and large-cap growth and value stocks. The fund’s key attributes are its low costs, broad diversification, and the potential for tax efficiency. Investors looking for a low-cost way to gain broad exposure to the U.S. stock market who are willing to accept the volatility that comes with stock market investing may wish to consider this fund as either a core equity holding or your only domestic stock fund.",
    "expenseRatio": 0.04,
    "fee12b1": 0,
    "frontLoad": 0,
    "fundFamily": "VANGUARD ADMIRAL",
    "inceptionDate": "2000-11-13",
    "investmentSegment": "Growth & Income",
    "iraMinInvestment": 0,
    "isin": "",
    "manager": "O'Reilly,Nejman",
    "maxRedemptionFee": 0,
    "name": "Vanguard Index Funds: Vanguard Total Stock Market Index Fund; Admiral Class Shares",
    "standardMinInvestment": 3000,
    "status": "Open",
    "totalNav": 280758000000,
    "turnover": 8
  },
  "symbol": "VTSAX"
}
```

## 文档正文

Get mutual funds profile information. This endpoint covers both US and global mutual funds. For international funds, you must query the data using ISIN. A list of supported funds can be found here.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/v1/mutual-fund/profile`
