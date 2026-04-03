---
id: "url-6fcd85ac"
type: "api"
title: "5.3 Symbology"
url: "https://www.tiingo.com/documentation/appendix/symbology"
description: "This guide is covers Tiingo's symbol format for querying different assets throughout the API."
source: ""
tags: []
crawl_time: "2026-03-18T02:54:45.734Z"
metadata:
  sections:
    - {"title":"5.3 Symbology","content":[{"type":"text","content":"This guide is covers Tiingo's symbol format for querying different assets throughout the API."}]}
    - {"title":"5.3.1 Introduction","content":[{"type":"text","content":"Tiingo follows a symbology format to help disambiguate share classes, preferreds, and other types of assets. This section will be expanded as we ready to expand our API into permatickers and delisted ticker support."}]}
    - {"title":"5.3.2 Equities","content":[{"type":"text","content":"Right now the Tiingo API supports Equity, Mutual Fund, and ETF prices for US markets and Equity Prices for Chinese markets."},{"type":"text","content":"Since periods are often used in URLs to signify file extensions, we do not use periods in our symbol names given our REST APIs. Instead of periods (\".\"), we use hypens (\"-\"). This means \"BRK.A\" is \"BRK-A\" within Tiingo."},{"type":"text","content":"All tickers that have separate share classes follow the format:"},{"type":"text","content":"For example Berkshire Hathaway Class A shares are \"BRK-A\"."},{"type":"text","content":"Similarly, for preferred shares, you may use the format:"},{"type":"text","content":"For example Simon Property Group's Preferred J series shares would be \"SPG-P-J\"."},{"type":"text","content":"Mutual funds and Closed-End-Funds (CEFs) follow their typical format. Mutual Funds usually end with the letter \"X\" (e.g. \"VFINX\") and CEFs begin and end with the letter \"X\" (e.g. \"XAIFX\")."},{"type":"text","content":"Tiingo supports delisted data for tickers that have not yet been recycled. You may see some delisted data that ends in a digit. These are typically tickers that are stored in our database, but we do not yet have price data. As Tiingo expands, we will expand the offering into even older delisted data."},{"type":"code","content":"{SYMBOL}-{SHARE CLASS}"},{"type":"code","content":"{SYMBOL}-P-{SHARE CLASS}"}]}
    - {"title":"5.3.3 CryptoCurrency & FX","content":[{"type":"text","content":"Tiingo's methodology for CryptoCurrencies and FX currencies follow the same symbol method."},{"type":"text","content":"Because forward slashes (\"/\") are used to separate locations within URLs and directories, Tiingo does not use forward slashes within currency symbols to prevent URL amibiguity. Instead we remove the forward slashes. Therefore the format for currencies is:"},{"type":"text","content":"For \"EUR/USD\" the base currency is \"EUR\" and the quote currency is \"USD\". This means the Tiingo symbol is \"EURUSD\"."},{"type":"text","content":"For \"BTC/ETH\" the base currency is \"BTC\" and the quote currency is \"ETH\". This means the Tiingo symbol is \"BTCETH\"."},{"type":"code","content":"{BASE_CURRENCY}{QUOTE_CURRENCY}"}]}
  codeExamples:
    - "{SYMBOL}-{SHARE CLASS}"
    - "{SYMBOL}-P-{SHARE CLASS}"
    - "{BASE_CURRENCY}{QUOTE_CURRENCY}"
  tables: []
  tabContents: []
  rawContent: "5. APPENDIX\n5.3 Symbology\n\nThis guide is covers Tiingo's symbol format for querying different assets throughout the API.\n\n5.3 APPENDIX - SYMBOLOGY\n5.3.1 Introduction\n\nTiingo follows a symbology format to help disambiguate share classes, preferreds, and other types of assets. This section will be expanded as we ready to expand our API into permatickers and delisted ticker support.\n\n5.3 APPENDIX - SYMBOLOGY\n5.3.2 Equities\n\nRight now the Tiingo API supports Equity, Mutual Fund, and ETF prices for US markets and Equity Prices for Chinese markets.\n\nSince periods are often used in URLs to signify file extensions, we do not use periods in our symbol names given our REST APIs. Instead of periods (\".\"), we use hypens (\"-\"). This means \"BRK.A\" is \"BRK-A\" within Tiingo.\n\nAll tickers that have separate share classes follow the format:\n\n{SYMBOL}-{SHARE CLASS}\n\nFor example Berkshire Hathaway Class A shares are \"BRK-A\".\n\nSimilarly, for preferred shares, you may use the format:\n\n{SYMBOL}-P-{SHARE CLASS}\n\nFor example Simon Property Group's Preferred J series shares would be \"SPG-P-J\".\n\nMutual funds and Closed-End-Funds (CEFs) follow their typical format. Mutual Funds usually end with the letter \"X\" (e.g. \"VFINX\") and CEFs begin and end with the letter \"X\" (e.g. \"XAIFX\").\n\nTiingo supports delisted data for tickers that have not yet been recycled. You may see some delisted data that ends in a digit. These are typically tickers that are stored in our database, but we do not yet have price data. As Tiingo expands, we will expand the offering into even older delisted data.\n\n5.3 APPENDIX - SYMBOLOGY\n5.3.3 CryptoCurrency & FX\n\nTiingo's methodology for CryptoCurrencies and FX currencies follow the same symbol method.\n\nBecause forward slashes (\"/\") are used to separate locations within URLs and directories, Tiingo does not use forward slashes within currency symbols to prevent URL amibiguity. Instead we remove the forward slashes. Therefore the format for currencies is:\n\n{BASE_CURRENCY}{QUOTE_CURRENCY}\n\nFor \"EUR/USD\" the base currency is \"EUR\" and the quote currency is \"USD\". This means the Tiingo symbol is \"EURUSD\".\n\nFor \"BTC/ETH\" the base currency is \"BTC\" and the quote currency is \"ETH\". This means the Tiingo symbol is \"BTCETH\"."
  suggestedFilename: "appendix_symbology"
---

# 5.3 Symbology

## 源URL

https://www.tiingo.com/documentation/appendix/symbology

## 描述

This guide is covers Tiingo's symbol format for querying different assets throughout the API.

## 代码示例

### 示例 1 (json)

```json
{SYMBOL}-{SHARE CLASS}
```

### 示例 2 (json)

```json
{SYMBOL}-P-{SHARE CLASS}
```

### 示例 3 (json)

```json
{BASE_CURRENCY}{QUOTE_CURRENCY}
```

## 文档正文

This guide is covers Tiingo's symbol format for querying different assets throughout the API.

5. APPENDIX
5.3 Symbology

This guide is covers Tiingo's symbol format for querying different assets throughout the API.

5.3 APPENDIX - SYMBOLOGY
5.3.1 Introduction

Tiingo follows a symbology format to help disambiguate share classes, preferreds, and other types of assets. This section will be expanded as we ready to expand our API into permatickers and delisted ticker support.

5.3 APPENDIX - SYMBOLOGY
5.3.2 Equities

Right now the Tiingo API supports Equity, Mutual Fund, and ETF prices for US markets and Equity Prices for Chinese markets.

Since periods are often used in URLs to signify file extensions, we do not use periods in our symbol names given our REST APIs. Instead of periods ("."), we use hypens ("-"). This means "BRK.A" is "BRK-A" within Tiingo.

All tickers that have separate share classes follow the format:

{SYMBOL}-{SHARE CLASS}

For example Berkshire Hathaway Class A shares are "BRK-A".

Similarly, for preferred shares, you may use the format:

{SYMBOL}-P-{SHARE CLASS}

For example Simon Property Group's Preferred J series shares would be "SPG-P-J".

Mutual funds and Closed-End-Funds (CEFs) follow their typical format. Mutual Funds usually end with the letter "X" (e.g. "VFINX") and CEFs begin and end with the letter "X" (e.g. "XAIFX").

Tiingo supports delisted data for tickers that have not yet been recycled. You may see some delisted data that ends in a digit. These are typically tickers that are stored in our database, but we do not yet have price data. As Tiingo expands, we will expand the offering into even older delisted data.

5.3 APPENDIX - SYMBOLOGY
5.3.3 CryptoCurrency & FX

Tiingo's methodology for CryptoCurrencies and FX currencies follow the same symbol method.

Because forward slashes ("/") are used to separate locations within URLs and directories, Tiingo does not use forward slashes within currency symbols to prevent URL amibiguity. Instead we remove the forward slashes. Therefore the format for currencies is:

{BASE_CURRENCY}{QUOTE_CURRENCY}

For "EUR/USD" the base currency is "EUR" and the quote currency is "USD". This means the Tiingo symbol is "EURUSD".

For "BTC/ETH" the base currency is "BTC" and the quote currency is "ETH". This means the Tiingo symbol is "BTCETH".
