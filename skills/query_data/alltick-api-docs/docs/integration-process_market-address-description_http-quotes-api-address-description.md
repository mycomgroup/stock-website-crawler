---
id: "url-19a9ed78"
type: "api"
title: "HTTP 行情 API 地址说明"
url: "https://apis.alltick.co/integration-process/market-address-description/http-quotes-api-address-description"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:59:03.692Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["接入流程chevron-right","行情地址说明"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"API地址说明","content":[]}
    - {"type":"heading","level":3,"title":"股票HTTP接口API地址","content":[{"type":"text","value":"/quote-stock-b-api 股票查询API"},{"type":"text","value":"查询API为https协议，完整的url为： https://quote.alltick.co/quote-stock-b-api"},{"type":"text","value":"每发送一次查询请求时，需要带上方法名和token信息\\"},{"type":"text","value":"单产品请求K线示例： https://quote.alltick.co/quote-stock-b-api/kline?token=你的token&query=queryData\\"},{"type":"text","value":"批产品请求K线示例： https://quote.alltick.co/quote-stock-b-api/batch-kline?token=你的token 注意：批产品请求K线时，请求参数放在body中"},{"type":"text","value":"请求最新成交价示例： https://quote.alltick.co/quote-stock-b-api/trade-tick?token=你的token&query=queryData\\"},{"type":"text","value":"请求最新盘口示例： https://quote.alltick.co/quote-stock-b-api/depth-tick?token=你的token&query=queryData\\"},{"type":"text","value":"具体调用方式，请查看http接口列表"}]}
    - {"type":"heading","level":3,"title":"外汇,加密货币(数字币),商品(贵金属) HTTP接口API地址","content":[{"type":"text","value":"/quote-b-api 外汇,加密货币(数字币),商品(贵金属)查询API\\"},{"type":"text","value":"查询API为https协议，完整的url为： https://quote.alltick.co/quote-b-api\\"},{"type":"text","value":"每发送一次查询请求时，需要带上方法名和token信息\\"},{"type":"text","value":"单产品请求K线示例： https://quote.alltick.co/quote-b-api/kline?token=你的token&query=queryData\\"},{"type":"text","value":"批产品请求K线示例： https://quote.alltick.co/quote-b-api/batch-kline?token=你的token 注意：批产品请求K线时，请求参数放在body中"},{"type":"text","value":"请求最新成交价示例： https://quote.alltick.co/quote-b-api/trade-tick?token=你的token&query=queryData\\"},{"type":"text","value":"请求最新盘口示例： https://quote.alltick.co/quote-b-api/depth-tick?token=你的token&query=queryData\\"},{"type":"text","value":"具体调用方式，请查看http接口列表"}]}
    - {"type":"heading","level":4,"title":"官方网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples: []
  tables: []
  parameters: []
  markdownContent: "# HTTP 行情 API 地址说明\n\n1. 接入流程chevron-right\n1. 行情地址说明\n\nEnglish / 中文\n\n\n## API地址说明\n\n\n### 股票HTTP接口API地址\n\n/quote-stock-b-api 股票查询API\n\n查询API为https协议，完整的url为： https://quote.alltick.co/quote-stock-b-api\n\n每发送一次查询请求时，需要带上方法名和token信息\\\n\n单产品请求K线示例： https://quote.alltick.co/quote-stock-b-api/kline?token=你的token&query=queryData\\\n\n批产品请求K线示例： https://quote.alltick.co/quote-stock-b-api/batch-kline?token=你的token 注意：批产品请求K线时，请求参数放在body中\n\n请求最新成交价示例： https://quote.alltick.co/quote-stock-b-api/trade-tick?token=你的token&query=queryData\\\n\n请求最新盘口示例： https://quote.alltick.co/quote-stock-b-api/depth-tick?token=你的token&query=queryData\\\n\n具体调用方式，请查看http接口列表\n\n\n### 外汇,加密货币(数字币),商品(贵金属) HTTP接口API地址\n\n/quote-b-api 外汇,加密货币(数字币),商品(贵金属)查询API\\\n\n查询API为https协议，完整的url为： https://quote.alltick.co/quote-b-api\\\n\n每发送一次查询请求时，需要带上方法名和token信息\\\n\n单产品请求K线示例： https://quote.alltick.co/quote-b-api/kline?token=你的token&query=queryData\\\n\n批产品请求K线示例： https://quote.alltick.co/quote-b-api/batch-kline?token=你的token 注意：批产品请求K线时，请求参数放在body中\n\n请求最新成交价示例： https://quote.alltick.co/quote-b-api/trade-tick?token=你的token&query=queryData\\\n\n请求最新盘口示例： https://quote.alltick.co/quote-b-api/depth-tick?token=你的token&query=queryData\\\n\n具体调用方式，请查看http接口列表\n\n\n#### 官方网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\n接入流程\n行情地址说明\nHTTP 行情 API 地址说明\n\nEnglish / 中文\n\nAPI地址说明\n股票HTTP接口API地址\n\n/quote-stock-b-api 股票查询API\n\n查询API为https协议，完整的url为：\nhttps://quote.alltick.co/quote-stock-b-api\n\n每发送一次查询请求时，需要带上方法名和token信息\\\n\n单产品请求K线示例：\nhttps://quote.alltick.co/quote-stock-b-api/kline?token=你的token&query=queryData\\\n\n批产品请求K线示例：\nhttps://quote.alltick.co/quote-stock-b-api/batch-kline?token=你的token\n注意：批产品请求K线时，请求参数放在body中\n\n请求最新成交价示例：\nhttps://quote.alltick.co/quote-stock-b-api/trade-tick?token=你的token&query=queryData\\\n\n请求最新盘口示例：\nhttps://quote.alltick.co/quote-stock-b-api/depth-tick?token=你的token&query=queryData\\\n\n具体调用方式，请查看http接口列表\n\n外汇,加密货币(数字币),商品(贵金属) HTTP接口API地址\n\n/quote-b-api 外汇,加密货币(数字币),商品(贵金属)查询API\\\n\n查询API为https协议，完整的url为：\nhttps://quote.alltick.co/quote-b-api\\\n\n每发送一次查询请求时，需要带上方法名和token信息\\\n\n单产品请求K线示例：\nhttps://quote.alltick.co/quote-b-api/kline?token=你的token&query=queryData\\\n\n批产品请求K线示例：\nhttps://quote.alltick.co/quote-b-api/batch-kline?token=你的token\n注意：批产品请求K线时，请求参数放在body中\n\n请求最新成交价示例：\nhttps://quote.alltick.co/quote-b-api/trade-tick?token=你的token&query=queryData\\\n\n请求最新盘口示例：\nhttps://quote.alltick.co/quote-b-api/depth-tick?token=你的token&query=queryData\\\n\n具体调用方式，请查看http接口列表\n\n官方网站\n\n官方网站：https://alltick.co/\n\n上一页\n行情地址说明\n下一页\nWebsocket 行情 API 地址说明\n\n最后更新于5个月前"
  suggestedFilename: "integration-process_market-address-description_http-quotes-api-address-description"
---

# HTTP 行情 API 地址说明

## 源URL

https://apis.alltick.co/integration-process/market-address-description/http-quotes-api-address-description

## 文档正文

1. 接入流程chevron-right
1. 行情地址说明

English / 中文

## API地址说明

### 股票HTTP接口API地址

/quote-stock-b-api 股票查询API

查询API为https协议，完整的url为： https://quote.alltick.co/quote-stock-b-api

每发送一次查询请求时，需要带上方法名和token信息\

单产品请求K线示例： https://quote.alltick.co/quote-stock-b-api/kline?token=你的token&query=queryData\

批产品请求K线示例： https://quote.alltick.co/quote-stock-b-api/batch-kline?token=你的token 注意：批产品请求K线时，请求参数放在body中

请求最新成交价示例： https://quote.alltick.co/quote-stock-b-api/trade-tick?token=你的token&query=queryData\

请求最新盘口示例： https://quote.alltick.co/quote-stock-b-api/depth-tick?token=你的token&query=queryData\

具体调用方式，请查看http接口列表

### 外汇,加密货币(数字币),商品(贵金属) HTTP接口API地址

/quote-b-api 外汇,加密货币(数字币),商品(贵金属)查询API\

查询API为https协议，完整的url为： https://quote.alltick.co/quote-b-api\

每发送一次查询请求时，需要带上方法名和token信息\

单产品请求K线示例： https://quote.alltick.co/quote-b-api/kline?token=你的token&query=queryData\

批产品请求K线示例： https://quote.alltick.co/quote-b-api/batch-kline?token=你的token 注意：批产品请求K线时，请求参数放在body中

请求最新成交价示例： https://quote.alltick.co/quote-b-api/trade-tick?token=你的token&query=queryData\

请求最新盘口示例： https://quote.alltick.co/quote-b-api/depth-tick?token=你的token&query=queryData\

具体调用方式，请查看http接口列表

#### 官方网站

官方网站：https://alltick.co/

最后更新于5个月前
