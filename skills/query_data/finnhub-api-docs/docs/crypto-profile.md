---
id: "url-4725fdc8"
type: "api"
title: "Crypto Profile Premium"
url: "https://finnhub.io/docs/api/crypto-profile"
description: "Get crypto's profile."
source: ""
tags: []
crawl_time: "2026-03-18T06:58:39.654Z"
metadata:
  requestMethod: "GET"
  endpoint: "/crypto/profile?symbol=BTC"
  parameters:
    - {"name":"symbol","in":"query","required":true,"type":"string","description":"Crypto symbol such as BTC or ETH."}
  responses:
    - {"code":"200","description":"successful operation"}
  codeExamples:
    - {"language":"JavaScript","code":"finnhubClient.cryptoProfile(\"BTC\", (error, data, response) => {\n  console.log(data)\n});"}
    - {"language":"Python","code":"print(finnhub_client.crypto_profile('BTC'))"}
    - {"language":"Go","code":"res, _, err := finnhubClient.CryptoProfile(context.Background()).Symbol(\"BTC\").Execute()"}
    - {"language":"PHP","code":"print_r($client->cryptoProfile(\"BTC\"));"}
    - {"language":"Ruby","code":"puts(finnhub_client.crypto_profile('BTC'))"}
    - {"language":"Kotlin","code":"println(apiClient.cryptoProfile(\"BTC\"))"}
  sampleResponse: "{\n  \"name\": \"Bitcoin\",\n  \"longName\": \"Bitcoin (BTC)\",\n  \"description\": \"Bitcoin uses peer-to-peer technology to operate with no central authority or banks; managing transactions and the issuing of bitcoins is carried out collectively by the network. Although other cryptocurrencies have come before, Bitcoin is the first decentralized cryptocurrency - Its reputation has spawned copies and evolution in the space.With the largest variety of markets and the biggest value - having reached a peak of 318 billion USD - Bitcoin is here to stay. As with any new invention, there can be improvements or flaws in the initial model however the community and a team of dedicated developers are pushing to overcome any obstacle they come across. It is also the most traded cryptocurrency and one of the main entry points for all the other cryptocurrencies. The price is as unstable as always and it can go up or down by 10%-20% in a single day.Bitcoin is an SHA-256 POW coin with almost 21,000,000 total minable coins. The block time is 10 minutes. See below for a full range of Bitcoin markets where you can trade US Dollars for Bitcoin, crypto to Bitcoin and many other fiat currencies too.Bitcoin Whitepaper PDF - A Peer-to-Peer Electronic Cash SystemBlockchain data provided by: Blockchain (main source), Blockchair (backup)\",\n  \"marketCap\": 1119891535870.4905,\n  \"totalSupply\": 18876550,\n  \"maxSupply\": 21000000,\n  \"circulatingSupply\": 18876550,\n  \"logo\": \"\",\n  \"launchDate\": \"2009-01-03\",\n  \"website\": \"https://bitcoin.org/en/\",\n  \"proofType\": \"PoW\"\n}"
  curlExample: ""
  jsonExample: "{\n  \"name\": \"Bitcoin\",\n  \"longName\": \"Bitcoin (BTC)\",\n  \"description\": \"Bitcoin uses peer-to-peer technology to operate with no central authority or banks; managing transactions and the issuing of bitcoins is carried out collectively by the network. Although other cryptocurrencies have come before, Bitcoin is the first decentralized cryptocurrency - Its reputation has spawned copies and evolution in the space.With the largest variety of markets and the biggest value - having reached a peak of 318 billion USD - Bitcoin is here to stay. As with any new invention, there can be improvements or flaws in the initial model however the community and a team of dedicated developers are pushing to overcome any obstacle they come across. It is also the most traded cryptocurrency and one of the main entry points for all the other cryptocurrencies. The price is as unstable as always and it can go up or down by 10%-20% in a single day.Bitcoin is an SHA-256 POW coin with almost 21,000,000 total minable coins. The block time is 10 minutes. See below for a full range of Bitcoin markets where you can trade US Dollars for Bitcoin, crypto to Bitcoin and many other fiat currencies too.Bitcoin Whitepaper PDF - A Peer-to-Peer Electronic Cash SystemBlockchain data provided by: Blockchain (main source), Blockchair (backup)\",\n  \"marketCap\": 1119891535870.4905,\n  \"totalSupply\": 18876550,\n  \"maxSupply\": 21000000,\n  \"circulatingSupply\": 18876550,\n  \"logo\": \"\",\n  \"launchDate\": \"2009-01-03\",\n  \"website\": \"https://bitcoin.org/en/\",\n  \"proofType\": \"PoW\"\n}"
  rawContent: "Crypto Profile Premium\n\nGet crypto's profile.\n\nMethod: GET\n\nPremium: Premium Access Required\n\nExamples:\n\n/crypto/profile?symbol=BTC\n\n/crypto/profile?symbol=ETH\n\nArguments:\n\nsymbolREQUIRED\n\nCrypto symbol such as BTC or ETH.\n\nResponse Attributes:\n\ncirculatingSupply\n\nCirculating supply.\n\ndescription\n\nDescription.\n\nlaunchDate\n\nLaunch date.\n\nlogo\n\nLogo image.\n\nlongName\n\nLong name.\n\nmarketCap\n\nMarket capitalization.\n\nmaxSupply\n\nMax supply.\n\nname\n\nName.\n\nproofType\n\nProof type.\n\ntotalSupply\n\nTotal supply.\n\nwebsite\n\nProject's website.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.crypto_profile('BTC'))\n\nSample response\n\n{\n  \"name\": \"Bitcoin\",\n  \"longName\": \"Bitcoin (BTC)\",\n  \"description\": \"Bitcoin uses peer-to-peer technology to operate with no central authority or banks; managing transactions and the issuing of bitcoins is carried out collectively by the network. Although other cryptocurrencies have come before, Bitcoin is the first decentralized cryptocurrency - Its reputation has spawned copies and evolution in the space.With the largest variety of markets and the biggest value - having reached a peak of 318 billion USD - Bitcoin is here to stay. As with any new invention, there can be improvements or flaws in the initial model however the community and a team of dedicated developers are pushing to overcome any obstacle they come across. It is also the most traded cryptocurrency and one of the main entry points for all the other cryptocurrencies. The price is as unstable as always and it can go up or down by 10%-20% in a single day.Bitcoin is an SHA-256 POW coin with almost 21,000,000 total minable coins. The block time is 10 minutes. See below for a full range of Bitcoin markets where you can trade US Dollars for Bitcoin, crypto to Bitcoin and many other fiat currencies too.Bitcoin Whitepaper PDF - A Peer-to-Peer Electronic Cash SystemBlockchain data provided by: Blockchain (main source), Blockchair (backup)\",\n  \"marketCap\": 1119891535870.4905,\n  \"totalSupply\": 18876550,\n  \"maxSupply\": 21000000,\n  \"circulatingSupply\": 18876550,\n  \"logo\": \"\",\n  \"launchDate\": \"2009-01-03\",\n  \"website\": \"https://bitcoin.org/en/\",\n  \"proofType\": \"PoW\"\n}"
  suggestedFilename: "crypto-profile"
---

# Crypto Profile Premium

## 源URL

https://finnhub.io/docs/api/crypto-profile

## 描述

Get crypto's profile.

## API 端点

**Method**: `GET`
**Endpoint**: `/crypto/profile?symbol=BTC`

## 请求参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `symbol` | string | 是 | - | Crypto symbol such as BTC or ETH. |

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | successful operation |

## 代码示例

### 示例 1 (JavaScript)

```JavaScript
finnhubClient.cryptoProfile("BTC", (error, data, response) => {
  console.log(data)
});
```

### 示例 2 (Python)

```Python
print(finnhub_client.crypto_profile('BTC'))
```

### 示例 3 (Go)

```Go
res, _, err := finnhubClient.CryptoProfile(context.Background()).Symbol("BTC").Execute()
```

### 示例 4 (PHP)

```PHP
print_r($client->cryptoProfile("BTC"));
```

### 示例 5 (Ruby)

```Ruby
puts(finnhub_client.crypto_profile('BTC'))
```

### 示例 6 (Kotlin)

```Kotlin
println(apiClient.cryptoProfile("BTC"))
```

### 示例 7 (json)

```json
{
  "name": "Bitcoin",
  "longName": "Bitcoin (BTC)",
  "description": "Bitcoin uses peer-to-peer technology to operate with no central authority or banks; managing transactions and the issuing of bitcoins is carried out collectively by the network. Although other cryptocurrencies have come before, Bitcoin is the first decentralized cryptocurrency - Its reputation has spawned copies and evolution in the space.With the largest variety of markets and the biggest value - having reached a peak of 318 billion USD - Bitcoin is here to stay. As with any new invention, there can be improvements or flaws in the initial model however the community and a team of dedicated developers are pushing to overcome any obstacle they come across. It is also the most traded cryptocurrency and one of the main entry points for all the other cryptocurrencies. The price is as unstable as always and it can go up or down by 10%-20% in a single day.Bitcoin is an SHA-256 POW coin with almost 21,000,000 total minable coins. The block time is 10 minutes. See below for a full range of Bitcoin markets where you can trade US Dollars for Bitcoin, crypto to Bitcoin and many other fiat currencies too.Bitcoin Whitepaper PDF - A Peer-to-Peer Electronic Cash SystemBlockchain data provided by: Blockchain (main source), Blockchair (backup)",
  "marketCap": 1119891535870.4905,
  "totalSupply": 18876550,
  "maxSupply": 21000000,
  "circulatingSupply": 18876550,
  "logo": "",
  "launchDate": "2009-01-03",
  "website": "https://bitcoin.org/en/",
  "proofType": "PoW"
}
```

## 文档正文

Get crypto's profile.

## API 端点

**Method:** `GET`
**Endpoint:** `/crypto/profile?symbol=BTC`

Crypto Profile Premium

Get crypto's profile.

Method: GET

Premium: Premium Access Required

Examples:

/crypto/profile?symbol=BTC

/crypto/profile?symbol=ETH

Arguments:

symbolREQUIRED

Crypto symbol such as BTC or ETH.

Response Attributes:

circulatingSupply

Circulating supply.

description

Description.

launchDate

Launch date.

logo

Logo image.

longName

Long name.

marketCap

Market capitalization.

maxSupply

Max supply.

name

Name.

proofType

Proof type.

totalSupply

Total supply.

website

Project's website.

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

print(finnhub_client.crypto_profile('BTC'))

Sample response

{
  "name": "Bitcoin",
  "longName": "Bitcoin (BTC)",
  "description": "Bitcoin uses peer-to-peer technology to operate with no central authority or banks; managing transactions and the issuing of bitcoins is carried out collectively by the network. Although other cryptocurrencies have come before, Bitcoin is the first decentralized cryptocurrency - Its reputation has spawned copies and evolution in the space.With the largest variety of markets and the biggest value - having reached a peak of 318 billion USD - Bitcoin is here to stay. As with any new invention, there can be improvements or flaws in the initial model however the community and a team of dedicated developers are pushing to overcome any obstacle they come across. It is also the most traded cryptocurrency and one of the main entry points for all the other cryptocurrencies. The price is as unstable as always and it can go up or down by 10%-20% in a single day.Bitcoin is an SHA-256 POW coin with almost 21,000,000 total minable coins. The block time is 10 minutes. See below for a full range of Bitcoin markets where you can trade US Dollars for Bitcoin, crypto to Bitcoin and many other fiat currencies too.Bitcoin Whitepaper PDF - A Peer-to-Peer Electronic Cash SystemBlockchain data provided by: Blockchain (main source), Blockchair (backup)",
  "marketCap": 1119891535870.4905,
  "totalSupply": 18876550,
  "maxSupply": 21000000,
  "circulatingSupply": 18876550,
  "logo": "",
  "launchDate": "2009-01-03",
  "website": "https://bitcoin.org/en/",
  "proofType": "PoW"
}
