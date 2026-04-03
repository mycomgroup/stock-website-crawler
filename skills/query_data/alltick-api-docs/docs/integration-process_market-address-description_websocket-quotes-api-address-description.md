---
id: "url-12481df7"
type: "api"
title: "Websocket 行情 API 地址说明"
url: "https://apis.alltick.co/integration-process/market-address-description/websocket-quotes-api-address-description"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:20:44.622Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["接入流程chevron-right","行情地址说明"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"股票市场数据WebSocket订阅","content":[{"type":"text","value":"接口地址"},{"type":"list","ordered":false,"items":["基本路径: /quote-stock-b-ws-api","完整URL: wss://quote.alltick.co/quote-stock-b-ws-api"]},{"type":"code","language":"text","value":"/quote-stock-b-ws-api"},{"type":"code","language":"text","value":"wss://quote.alltick.co/quote-stock-b-ws-api"},{"type":"text","value":"认证信息"},{"type":"text","value":"每次建立连接时，必须在URL中附加您的认证token，如下所示："},{"type":"code","language":"text","value":"复制wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token"},{"type":"code","language":"text","value":"wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token"},{"type":"code","language":"text","value":"wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token"},{"type":"text","value":"订阅说明"},{"type":"text","value":"连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考我们的WebSocket接口列表。"}]}
    - {"type":"heading","level":2,"title":"外汇、加密货币与商品市场数据WebSocket订阅","content":[{"type":"text","value":"接口地址"},{"type":"list","ordered":false,"items":["基本路径: /quote-b-ws-api","完整URL: wss://quote.alltick.co/quote-b-ws-api"]},{"type":"code","language":"text","value":"/quote-b-ws-api"},{"type":"code","language":"text","value":"wss://quote.alltick.co/quote-b-ws-api"},{"type":"text","value":"认证信息"},{"type":"text","value":"建立连接时，同样需要在URL中附加您的认证token，以确保数据传输的安全性。正确的格式应如下："},{"type":"code","language":"text","value":"复制wss://quote.alltick.co/quote-b-ws-api?token=您的token"},{"type":"code","language":"text","value":"wss://quote.alltick.co/quote-b-ws-api?token=您的token"},{"type":"code","language":"text","value":"wss://quote.alltick.co/quote-b-ws-api?token=您的token"},{"type":"text","value":"订阅说明"},{"type":"text","value":"一旦连接建立，您即可根据需求订阅外汇、加密货币（数字货币）、以及商品（贵金属）的市场数据。具体的接口调用方式，请查看我们的WebSocket接口列表。"},{"type":"text","value":"注意事项：为了您的账户安全，请确保妥善保管您的token信息。若需进一步帮助或有任何疑问，欢迎随时联系我们的技术支持团队。"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"/quote-stock-b-ws-api"}
    - {"type":"code","language":"text","value":"wss://quote.alltick.co/quote-stock-b-ws-api"}
    - {"type":"code","language":"text","value":"复制wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token"}
    - {"type":"code","language":"text","value":"wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token"}
    - {"type":"code","language":"text","value":"wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token"}
    - {"type":"code","language":"text","value":"/quote-b-ws-api"}
    - {"type":"code","language":"text","value":"wss://quote.alltick.co/quote-b-ws-api"}
    - {"type":"code","language":"text","value":"复制wss://quote.alltick.co/quote-b-ws-api?token=您的token"}
    - {"type":"code","language":"text","value":"wss://quote.alltick.co/quote-b-ws-api?token=您的token"}
    - {"type":"code","language":"text","value":"wss://quote.alltick.co/quote-b-ws-api?token=您的token"}
  tables: []
  parameters: []
  markdownContent: "# Websocket 行情 API 地址说明\n\n1. 接入流程chevron-right\n1. 行情地址说明\n\nEnglish / 中文\n\n\n## 股票市场数据WebSocket订阅\n\n接口地址\n\n- 基本路径: /quote-stock-b-ws-api\n- 完整URL: wss://quote.alltick.co/quote-stock-b-ws-api\n\n```text\n/quote-stock-b-ws-api\n```\n\n```text\nwss://quote.alltick.co/quote-stock-b-ws-api\n```\n\n认证信息\n\n每次建立连接时，必须在URL中附加您的认证token，如下所示：\n\n```text\n复制wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token\n```\n\n```text\nwss://quote.alltick.co/quote-stock-b-ws-api?token=您的token\n```\n\n```text\nwss://quote.alltick.co/quote-stock-b-ws-api?token=您的token\n```\n\n订阅说明\n\n连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考我们的WebSocket接口列表。\n\n\n## 外汇、加密货币与商品市场数据WebSocket订阅\n\n接口地址\n\n- 基本路径: /quote-b-ws-api\n- 完整URL: wss://quote.alltick.co/quote-b-ws-api\n\n```text\n/quote-b-ws-api\n```\n\n```text\nwss://quote.alltick.co/quote-b-ws-api\n```\n\n认证信息\n\n建立连接时，同样需要在URL中附加您的认证token，以确保数据传输的安全性。正确的格式应如下：\n\n```text\n复制wss://quote.alltick.co/quote-b-ws-api?token=您的token\n```\n\n```text\nwss://quote.alltick.co/quote-b-ws-api?token=您的token\n```\n\n```text\nwss://quote.alltick.co/quote-b-ws-api?token=您的token\n```\n\n订阅说明\n\n一旦连接建立，您即可根据需求订阅外汇、加密货币（数字货币）、以及商品（贵金属）的市场数据。具体的接口调用方式，请查看我们的WebSocket接口列表。\n\n注意事项：为了您的账户安全，请确保妥善保管您的token信息。若需进一步帮助或有任何疑问，欢迎随时联系我们的技术支持团队。\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\n接入流程\n行情地址说明\nWebsocket 行情 API 地址说明\n\nEnglish / 中文\n\n股票市场数据WebSocket订阅\n\n接口地址\n\n基本路径: /quote-stock-b-ws-api\n\n完整URL: wss://quote.alltick.co/quote-stock-b-ws-api\n\n认证信息\n\n每次建立连接时，必须在URL中附加您的认证token，如下所示：\n\n复制\nwss://quote.alltick.co/quote-stock-b-ws-api?token=您的token\n\n订阅说明\n\n连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考我们的WebSocket接口列表。\n\n外汇、加密货币与商品市场数据WebSocket订阅\n\n接口地址\n\n基本路径: /quote-b-ws-api\n\n完整URL: wss://quote.alltick.co/quote-b-ws-api\n\n认证信息\n\n建立连接时，同样需要在URL中附加您的认证token，以确保数据传输的安全性。正确的格式应如下：\n\n复制\nwss://quote.alltick.co/quote-b-ws-api?token=您的token\n\n订阅说明\n\n一旦连接建立，您即可根据需求订阅外汇、加密货币（数字货币）、以及商品（贵金属）的市场数据。具体的接口调用方式，请查看我们的WebSocket接口列表。\n\n注意事项：为了您的账户安全，请确保妥善保管您的token信息。若需进一步帮助或有任何疑问，欢迎随时联系我们的技术支持团队。\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nHTTP 行情 API 地址说明\n下一页\nToken 申请\n\n最后更新于5个月前"
  suggestedFilename: "integration-process_market-address-description_websocket-quotes-api-address-description"
---

# Websocket 行情 API 地址说明

## 源URL

https://apis.alltick.co/integration-process/market-address-description/websocket-quotes-api-address-description

## 文档正文

1. 接入流程chevron-right
1. 行情地址说明

English / 中文

## 股票市场数据WebSocket订阅

接口地址

- 基本路径: /quote-stock-b-ws-api
- 完整URL: wss://quote.alltick.co/quote-stock-b-ws-api

```text
/quote-stock-b-ws-api
```

```text
wss://quote.alltick.co/quote-stock-b-ws-api
```

认证信息

每次建立连接时，必须在URL中附加您的认证token，如下所示：

```text
复制wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token
```

```text
wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token
```

```text
wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token
```

订阅说明

连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考我们的WebSocket接口列表。

## 外汇、加密货币与商品市场数据WebSocket订阅

接口地址

- 基本路径: /quote-b-ws-api
- 完整URL: wss://quote.alltick.co/quote-b-ws-api

```text
/quote-b-ws-api
```

```text
wss://quote.alltick.co/quote-b-ws-api
```

认证信息

建立连接时，同样需要在URL中附加您的认证token，以确保数据传输的安全性。正确的格式应如下：

```text
复制wss://quote.alltick.co/quote-b-ws-api?token=您的token
```

```text
wss://quote.alltick.co/quote-b-ws-api?token=您的token
```

```text
wss://quote.alltick.co/quote-b-ws-api?token=您的token
```

订阅说明

一旦连接建立，您即可根据需求订阅外汇、加密货币（数字货币）、以及商品（贵金属）的市场数据。具体的接口调用方式，请查看我们的WebSocket接口列表。

注意事项：为了您的账户安全，请确保妥善保管您的token信息。若需进一步帮助或有任何疑问，欢迎随时联系我们的技术支持团队。

#### AllTick网站

官方网站：https://alltick.co/

最后更新于5个月前
