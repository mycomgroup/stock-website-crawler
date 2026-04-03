---
id: "url-25b22fab"
type: "api"
title: "最新盘口(实时逐笔深度、Order Book)订阅"
url: "https://apis.alltick.co/websocket-api/stock-websocket-interface-api/handicap-quote-subscription"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:57:27.532Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["Websocket APIchevron-right","Websocket接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"该接口支持订阅产品的最新盘口(实时逐笔深度、Order Book)数据，不支持历史盘口和历史逐笔tick数据。"},{"type":"text","value":"该接口特性：对于每一个websocket连接，每发送一次该请求，后台会默认覆盖上一次订阅请求（例如，如果您最初订阅了A、B、C这三只产品，想要追加订阅E、F、G，则需要重新发送一次A、B、C、E、F、G），订阅成功后会进行推送数据。"},{"type":"text","value":"注意："},{"type":"text","value":"1、订阅一次成功后，不需要再频繁的发起订阅请求，要求每10秒发送一次心跳，接口就会实时推送数据，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接"},{"type":"text","value":"2、接入时，客户可增加断开自动重连的逻辑，确保因网络等原因断开可自动重连"},{"type":"text","value":"3、以下是每类产品最大的盘口深度："},{"type":"text","value":"3.1 不活跃的产品存在小于下面列的最大档的情况，属于正常情况"},{"type":"text","value":"3.2 存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的"},{"type":"text","value":"深度说明"},{"type":"text","value":"最大1 档 (只有委托价，没有量)"},{"type":"text","value":"最大5档"},{"type":"text","value":"最大10档"},{"type":"text","value":"最大1档"},{"type":"text","value":"最大5档"}]}
    - {"type":"heading","level":2,"title":"接口限制","content":[{"type":"text","value":"1、请务必阅读：Websocket限制说明"},{"type":"text","value":"2、请务必阅读：错误码说明"}]}
    - {"type":"heading","level":2,"title":"接口地址","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-stock-b-ws-api","完整URL: wss://quote.alltick.co/quote-stock-b-ws-api"]},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-b-ws-api","完整URL: wss://quote.alltick.co/quote-b-ws-api"]}]}
    - {"type":"heading","level":2,"title":"请求示例","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据请求示例："},{"type":"text","value":"每次建立连接时，必须在URL中附加您的认证token，如下所示："},{"type":"text","value":"wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token"},{"type":"text","value":"连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考下面的文档说明。"},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例："},{"type":"text","value":"每次建立连接时，必须在URL中附加您的认证token，如下所示："},{"type":"text","value":"wss://quote.alltick.co/quote-b-ws-api?token=您的token"},{"type":"text","value":"连接成功后，您可以根据需要订阅特定的外汇、加密货币、贵金属、商品数据。详细的调用方法请参考下面的文档说明。"}]}
    - {"type":"heading","level":2,"title":"请求-协议号：22002","content":[]}
    - {"type":"heading","level":4,"title":"json定义","content":[{"type":"text","value":"cmd_id"},{"type":"text","value":"协议号"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"最新盘口请求协议号固定：22002"},{"type":"text","value":"seq_id"},{"type":"text","value":"响应id"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"订阅请求标识，响应回传(自定义，每次请求可重复)"},{"type":"text","value":"trace"},{"type":"text","value":"可追溯id"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"请求日志信息可追溯id(自定义，每次请求不可重复)"},{"type":"text","value":"symbol_list"},{"type":"text","value":"产品列表"},{"type":"text","value":"array"},{"type":"text","value":"是"},{"type":"text","value":"具体格式见下面symbol定义"}]}
    - {"type":"heading","level":4,"title":"symbol定义","content":[{"type":"text","value":"code"},{"type":"text","value":"代码"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"具体内容，请查阅code列表：[点击code列表]"},{"type":"text","value":"depth_level"},{"type":"text","value":"深度层级"},{"type":"text","value":"uint32"},{"type":"text","value":"否"},{"type":"text","value":"如果没有depth_level字段时，后台只会提供一层的报价，请求的层级大于实际报价层级，或者如果没有depth_level字段时，则后台按实际报价有多少层给多少层"}]}
    - {"type":"heading","level":3,"title":"数据结构(json)","content":[{"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}"}]}
    - {"type":"heading","level":2,"title":"应答-协议号：22003","content":[]}
    - {"type":"heading","level":3,"title":"数据结构(json)","content":[{"type":"code","language":"text","value":"复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}]}
    - {"type":"heading","level":2,"title":"推送-协议号：22999","content":[]}
    - {"type":"heading","level":4,"title":"data定义","content":[{"type":"text","value":"code"},{"type":"text","value":"代码"},{"type":"text","value":"string"},{"type":"text","value":"具体内容，请查阅code列表：[点击code列表]"},{"type":"text","value":"seq"},{"type":"text","value":"报价序号"},{"type":"text","value":"string"},{"type":"text","value":"tick_time"},{"type":"text","value":"报价时间戳"},{"type":"text","value":"string"},{"type":"text","value":"单位毫秒"},{"type":"text","value":"bids"},{"type":"text","value":"bid深度"},{"type":"text","value":"string"},{"type":"text","value":"见下面bids定义"},{"type":"text","value":"asks"},{"type":"text","value":"ask深度"},{"type":"text","value":"string"},{"type":"text","value":"见下面asks定义"}]}
    - {"type":"heading","level":4,"title":"bids定义","content":[{"type":"text","value":"price"},{"type":"text","value":"买一价，买盘价格"},{"type":"text","value":"string"},{"type":"text","value":"volume"},{"type":"text","value":"买一量，买盘量"},{"type":"text","value":"string"},{"type":"text","value":"1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume"}]}
    - {"type":"heading","level":4,"title":"asks定义","content":[{"type":"text","value":"price"},{"type":"text","value":"卖一价，卖盘价格"},{"type":"text","value":"string"},{"type":"text","value":"volume"},{"type":"text","value":"卖一量，卖盘量"},{"type":"text","value":"string"},{"type":"text","value":"1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume"}]}
    - {"type":"heading","level":3,"title":"数据结构(json)","content":[{"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}"}
    - {"type":"code","language":"text","value":"复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}"}
  tables: []
  parameters: []
  markdownContent: "# 最新盘口(实时逐笔深度、Order Book)订阅\n\n1. Websocket APIchevron-right\n1. Websocket接口API\n\nEnglish / 中文\n\n\n## 接口说明\n\n该接口支持订阅产品的最新盘口(实时逐笔深度、Order Book)数据，不支持历史盘口和历史逐笔tick数据。\n\n该接口特性：对于每一个websocket连接，每发送一次该请求，后台会默认覆盖上一次订阅请求（例如，如果您最初订阅了A、B、C这三只产品，想要追加订阅E、F、G，则需要重新发送一次A、B、C、E、F、G），订阅成功后会进行推送数据。\n\n注意：\n\n1、订阅一次成功后，不需要再频繁的发起订阅请求，要求每10秒发送一次心跳，接口就会实时推送数据，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接\n\n2、接入时，客户可增加断开自动重连的逻辑，确保因网络等原因断开可自动重连\n\n3、以下是每类产品最大的盘口深度：\n\n3.1 不活跃的产品存在小于下面列的最大档的情况，属于正常情况\n\n3.2 存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的\n\n深度说明\n\n最大1 档 (只有委托价，没有量)\n\n最大5档\n\n最大10档\n\n最大1档\n\n最大5档\n\n\n## 接口限制\n\n1、请务必阅读：Websocket限制说明\n\n2、请务必阅读：错误码说明\n\n\n## 接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n- 基本路径: /quote-stock-b-ws-api\n- 完整URL: wss://quote.alltick.co/quote-stock-b-ws-api\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n- 基本路径: /quote-b-ws-api\n- 完整URL: wss://quote.alltick.co/quote-b-ws-api\n\n\n## 请求示例\n\n1、美股、港股、A股、大盘数据请求示例：\n\n每次建立连接时，必须在URL中附加您的认证token，如下所示：\n\nwss://quote.alltick.co/quote-stock-b-ws-api?token=您的token\n\n连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考下面的文档说明。\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：\n\n每次建立连接时，必须在URL中附加您的认证token，如下所示：\n\nwss://quote.alltick.co/quote-b-ws-api?token=您的token\n\n连接成功后，您可以根据需要订阅特定的外汇、加密货币、贵金属、商品数据。详细的调用方法请参考下面的文档说明。\n\n\n## 请求-协议号：22002\n\n\n#### json定义\n\ncmd_id\n\n协议号\n\ninteger\n\n是\n\n最新盘口请求协议号固定：22002\n\nseq_id\n\n响应id\n\ninteger\n\n是\n\n订阅请求标识，响应回传(自定义，每次请求可重复)\n\ntrace\n\n可追溯id\n\nstring\n\n是\n\n请求日志信息可追溯id(自定义，每次请求不可重复)\n\nsymbol_list\n\n产品列表\n\narray\n\n是\n\n具体格式见下面symbol定义\n\n\n#### symbol定义\n\ncode\n\n代码\n\nstring\n\n是\n\n具体内容，请查阅code列表：[点击code列表]\n\ndepth_level\n\n深度层级\n\nuint32\n\n否\n\n如果没有depth_level字段时，后台只会提供一层的报价，请求的层级大于实际报价层级，或者如果没有depth_level字段时，则后台按实际报价有多少层给多少层\n\n\n### 数据结构(json)\n\n```text\n复制{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22002,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"symbol_list\": [\n            {\n                \"code\": \"BTCUSDT\",\n                \"depth_level\": 5\n            },\n            {\n                \"code\": \"ETHUSDT\",\n                \"depth_level\": 5\n            }\n        ]\n    }\n}\n```\n\n\n## 应答-协议号：22003\n\n\n### 数据结构(json)\n\n```text\n复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22003,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}\n```\n\n\n## 推送-协议号：22999\n\n\n#### data定义\n\ncode\n\n代码\n\nstring\n\n具体内容，请查阅code列表：[点击code列表]\n\nseq\n\n报价序号\n\nstring\n\ntick_time\n\n报价时间戳\n\nstring\n\n单位毫秒\n\nbids\n\nbid深度\n\nstring\n\n见下面bids定义\n\nasks\n\nask深度\n\nstring\n\n见下面asks定义\n\n\n#### bids定义\n\nprice\n\n买一价，买盘价格\n\nstring\n\nvolume\n\n买一量，买盘量\n\nstring\n\n1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume\n\n\n#### asks定义\n\nprice\n\n卖一价，卖盘价格\n\nstring\n\nvolume\n\n卖一量，卖盘量\n\nstring\n\n1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume\n\n\n### 数据结构(json)\n\n```text\n复制{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22999,\n    \"data\":{\n\t\"code\": \"HK-1288\",\n        \"seq\": \"1605509068000001\",\n        \"tick_time\": \"1605509068\",\n        \"bids\": [\n            {\n                \"price\": \"9.12\",\n                \"volume\": \"9.12\"\n            }\n        ],\n        \"asks\": [\n            {\n                \"price\": \"147.12\",\n                \"volume\": \"147.12\"\n            }\n        ]\n    }\n}\n```\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\nWEBSOCKET API\nWEBSOCKET接口API\n最新盘口(实时逐笔深度、Order Book)订阅\n\nEnglish / 中文\n\n接口说明\n\n该接口支持订阅产品的最新盘口(实时逐笔深度、Order Book)数据，不支持历史盘口和历史逐笔tick数据。\n\n该接口特性：对于每一个websocket连接，每发送一次该请求，后台会默认覆盖上一次订阅请求（例如，如果您最初订阅了A、B、C这三只产品，想要追加订阅E、F、G，则需要重新发送一次A、B、C、E、F、G），订阅成功后会进行推送数据。\n\n注意：\n\n1、订阅一次成功后，不需要再频繁的发起订阅请求，要求每10秒发送一次心跳，接口就会实时推送数据，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接\n\n2、接入时，客户可增加断开自动重连的逻辑，确保因网络等原因断开可自动重连\n\n3、以下是每类产品最大的盘口深度：\n\n3.1 不活跃的产品存在小于下面列的最大档的情况，属于正常情况\n\n3.2 存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的\n\n外汇、贵金属、原油\n加密货币\n港股\n美股\n沪深A股\n\n深度说明\n\n最大1 档\n(只有委托价，没有量)\n\n最大5档\n\n最大10档\n\n最大1档\n\n最大5档\n\n接口限制\n\n1、请务必阅读：Websocket限制说明\n\n2、请务必阅读：错误码说明\n\n接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n基本路径: /quote-stock-b-ws-api\n\n完整URL: wss://quote.alltick.co/quote-stock-b-ws-api\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n基本路径: /quote-b-ws-api\n\n完整URL: wss://quote.alltick.co/quote-b-ws-api\n\n请求示例\n\n1、美股、港股、A股、大盘数据请求示例：\n\n每次建立连接时，必须在URL中附加您的认证token，如下所示：\n\nwss://quote.alltick.co/quote-stock-b-ws-api?token=您的token\n\n连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考下面的文档说明。\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：\n\n每次建立连接时，必须在URL中附加您的认证token，如下所示：\n\nwss://quote.alltick.co/quote-b-ws-api?token=您的token\n\n连接成功后，您可以根据需要订阅特定的外汇、加密货币、贵金属、商品数据。详细的调用方法请参考下面的文档说明。\n\n请求-协议号：22002\njson定义\n字段\n名称\n类型\n必填项\n说明\n\ncmd_id\n\n协议号\n\ninteger\n\n是\n\n最新盘口请求协议号固定：22002\n\nseq_id\n\n响应id\n\ninteger\n\n是\n\n订阅请求标识，响应回传(自定义，每次请求可重复)\n\ntrace\n\n可追溯id\n\nstring\n\n是\n\n请求日志信息可追溯id(自定义，每次请求不可重复)\n\nsymbol_list\n\n产品列表\n\narray\n\n是\n\n具体格式见下面symbol定义\n\nsymbol定义\n字段\n名称\n类型\n必填项\n说明\n\ncode\n\n代码\n\nstring\n\n是\n\n具体内容，请查阅code列表：[点击code列表]\n\ndepth_level\n\n深度层级\n\nuint32\n\n否\n\n如果没有depth_level字段时，后台只会提供一层的报价，请求的层级大于实际报价层级，或者如果没有depth_level字段时，则后台按实际报价有多少层给多少层\n\n数据结构(json)\n复制\n{\n\n    \"cmd_id\":22002,\n\n    \"seq_id\":123,\n\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n    \"data\":{\n\n        \"symbol_list\": [\n\n            {\n\n                \"code\": \"BTCUSDT\",\n\n                \"depth_level\": 5\n\n            },\n\n            {\n\n                \"code\": \"ETHUSDT\",\n\n                \"depth_level\": 5\n\n            }\n\n        ]\n\n    }\n\n}\n应答-协议号：22003\n数据结构(json)\n复制\n{\n\n    \"ret\":200,\n\n    \"msg\":\"ok\",\n\n    \"cmd_id\":22003,\n\n    \"seq_id\":123,\n\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n    \"data\":{\n\n    }    \n\n}\n推送-协议号：22999\ndata定义\n字段\n名称\n类型\n说明\n\ncode\n\n代码\n\nstring\n\n具体内容，请查阅code列表：[点击code列表]\n\nseq\n\n报价序号\n\nstring\n\ntick_time\n\n报价时间戳\n\nstring\n\n单位毫秒\n\nbids\n\nbid深度\n\nstring\n\n见下面bids定义\n\nasks\n\nask深度\n\nstring\n\n见下面asks定义\n\nbids定义\n字段\n名称\n类型\n说明\n\nprice\n\n买一价，买盘价格\n\nstring\n\nvolume\n\n买一量，买盘量\n\nstring\n\n1、外汇、贵金属、CFD指数不提供volume\n2、股票，加密货币数据均提供volume\n\nasks定义\n字段\n名称\n类型\n说明\n\nprice\n\n卖一价，卖盘价格\n\nstring\n\nvolume\n\n卖一量，卖盘量\n\nstring\n\n1、外汇、贵金属、CFD指数不提供volume\n2、股票，加密货币数据均提供volume\n\n数据结构(json)\n复制\n{\n\n    \"cmd_id\":22999,\n\n    \"data\":{\n\n\t\"code\": \"HK-1288\",\n\n        \"seq\": \"1605509068000001\",\n\n        \"tick_time\": \"1605509068\",\n\n        \"bids\": [\n\n            {\n\n                \"price\": \"9.12\",\n\n                \"volume\": \"9.12\"\n\n            }\n\n        ],\n\n        \"asks\": [\n\n            {\n\n                \"price\": \"147.12\",\n\n                \"volume\": \"147.12\"\n\n            }\n\n        ]\n\n    }\n\n}\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n最新成交价(实时逐笔Tick数据、当前价、最新价)批量订阅\n下一页\n取消报价订阅\n\n最后更新于5个月前"
  suggestedFilename: "websocket-api_stock-websocket-interface-api_handicap-quote-subscription"
---

# 最新盘口(实时逐笔深度、Order Book)订阅

## 源URL

https://apis.alltick.co/websocket-api/stock-websocket-interface-api/handicap-quote-subscription

## 文档正文

1. Websocket APIchevron-right
1. Websocket接口API

English / 中文

## 接口说明

该接口支持订阅产品的最新盘口(实时逐笔深度、Order Book)数据，不支持历史盘口和历史逐笔tick数据。

该接口特性：对于每一个websocket连接，每发送一次该请求，后台会默认覆盖上一次订阅请求（例如，如果您最初订阅了A、B、C这三只产品，想要追加订阅E、F、G，则需要重新发送一次A、B、C、E、F、G），订阅成功后会进行推送数据。

注意：

1、订阅一次成功后，不需要再频繁的发起订阅请求，要求每10秒发送一次心跳，接口就会实时推送数据，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接

2、接入时，客户可增加断开自动重连的逻辑，确保因网络等原因断开可自动重连

3、以下是每类产品最大的盘口深度：

3.1 不活跃的产品存在小于下面列的最大档的情况，属于正常情况

3.2 存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的

深度说明

最大1 档 (只有委托价，没有量)

最大5档

最大10档

最大1档

最大5档

## 接口限制

1、请务必阅读：Websocket限制说明

2、请务必阅读：错误码说明

## 接口地址

1、美股、港股、A股、大盘数据接口地址：

- 基本路径: /quote-stock-b-ws-api
- 完整URL: wss://quote.alltick.co/quote-stock-b-ws-api

2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：

- 基本路径: /quote-b-ws-api
- 完整URL: wss://quote.alltick.co/quote-b-ws-api

## 请求示例

1、美股、港股、A股、大盘数据请求示例：

每次建立连接时，必须在URL中附加您的认证token，如下所示：

wss://quote.alltick.co/quote-stock-b-ws-api?token=您的token

连接成功后，您可以根据需要订阅特定的股票市场数据。详细的调用方法请参考下面的文档说明。

2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：

每次建立连接时，必须在URL中附加您的认证token，如下所示：

wss://quote.alltick.co/quote-b-ws-api?token=您的token

连接成功后，您可以根据需要订阅特定的外汇、加密货币、贵金属、商品数据。详细的调用方法请参考下面的文档说明。

## 请求-协议号：22002

#### json定义

cmd_id

协议号

integer

是

最新盘口请求协议号固定：22002

seq_id

响应id

integer

是

订阅请求标识，响应回传(自定义，每次请求可重复)

trace

可追溯id

string

是

请求日志信息可追溯id(自定义，每次请求不可重复)

symbol_list

产品列表

array

是

具体格式见下面symbol定义

#### symbol定义

code

代码

string

是

具体内容，请查阅code列表：[点击code列表]

depth_level

深度层级

uint32

否

如果没有depth_level字段时，后台只会提供一层的报价，请求的层级大于实际报价层级，或者如果没有depth_level字段时，则后台按实际报价有多少层给多少层

### 数据结构(json)

```text
复制{
    "cmd_id":22002,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
        "symbol_list": [
            {
                "code": "BTCUSDT",
                "depth_level": 5
            },
            {
                "code": "ETHUSDT",
                "depth_level": 5
            }
        ]
    }
}
```

```json
{
    "cmd_id":22002,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
        "symbol_list": [
            {
                "code": "BTCUSDT",
                "depth_level": 5
            },
            {
                "code": "ETHUSDT",
                "depth_level": 5
            }
        ]
    }
}
```

```json
{
    "cmd_id":22002,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
        "symbol_list": [
            {
                "code": "BTCUSDT",
                "depth_level": 5
            },
            {
                "code": "ETHUSDT",
                "depth_level": 5
            }
        ]
    }
}
```

## 应答-协议号：22003

### 数据结构(json)

```text
复制{
    "ret":200,
    "msg":"ok",
    "cmd_id":22003,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }    
}
```

```json
{
    "ret":200,
    "msg":"ok",
    "cmd_id":22003,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }    
}
```

```json
{
    "ret":200,
    "msg":"ok",
    "cmd_id":22003,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }    
}
```

## 推送-协议号：22999

#### data定义

code

代码

string

具体内容，请查阅code列表：[点击code列表]

seq

报价序号

string

tick_time

报价时间戳

string

单位毫秒

bids

bid深度

string

见下面bids定义

asks

ask深度

string

见下面asks定义

#### bids定义

price

买一价，买盘价格

string

volume

买一量，买盘量

string

1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume

#### asks定义

price

卖一价，卖盘价格

string

volume

卖一量，卖盘量

string

1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume

### 数据结构(json)

```text
复制{
    "cmd_id":22999,
    "data":{
	"code": "HK-1288",
        "seq": "1605509068000001",
        "tick_time": "1605509068",
        "bids": [
            {
                "price": "9.12",
                "volume": "9.12"
            }
        ],
        "asks": [
            {
                "price": "147.12",
                "volume": "147.12"
            }
        ]
    }
}
```

```json
{
    "cmd_id":22999,
    "data":{
	"code": "HK-1288",
        "seq": "1605509068000001",
        "tick_time": "1605509068",
        "bids": [
            {
                "price": "9.12",
                "volume": "9.12"
            }
        ],
        "asks": [
            {
                "price": "147.12",
                "volume": "147.12"
            }
        ]
    }
}
```

```json
{
    "cmd_id":22999,
    "data":{
	"code": "HK-1288",
        "seq": "1605509068000001",
        "tick_time": "1605509068",
        "bids": [
            {
                "price": "9.12",
                "volume": "9.12"
            }
        ],
        "asks": [
            {
                "price": "147.12",
                "volume": "147.12"
            }
        ]
    }
}
```

#### AllTick网站

官方网站：https://alltick.co/

最后更新于5个月前
