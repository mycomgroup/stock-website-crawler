---
id: "url-505512d"
type: "api"
title: "取消报价订阅"
url: "https://apis.alltick.co/websocket-api/stock-websocket-interface-api/cancel-quote-subscription"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:57:10.763Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["Websocket APIchevron-right","Websocket接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"取消报价订阅"}]}
    - {"type":"heading","level":2,"title":"请求-协议号：22006","content":[]}
    - {"type":"heading","level":4,"title":"data定义","content":[{"type":"text","value":"cancel_type"},{"type":"text","value":"取消类型"},{"type":"text","value":"uint32"},{"type":"text","value":"是"},{"type":"text","value":"0：取消所有报价订阅，1：取消盘口报价订阅，2：取消成交报价订阅，3：取消汇率订阅"}]}
    - {"type":"heading","level":3,"title":"数据结构(json)","content":[{"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}"}]}
    - {"type":"heading","level":2,"title":"应答-协议号：22007","content":[]}
    - {"type":"heading","level":3,"title":"数据结构(json)","content":[{"type":"code","language":"text","value":"复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于9个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}"}
    - {"type":"code","language":"text","value":"复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}"}
  tables: []
  parameters: []
  markdownContent: "# 取消报价订阅\n\n1. Websocket APIchevron-right\n1. Websocket接口API\n\nEnglish / 中文\n\n\n## 接口说明\n\n取消报价订阅\n\n\n## 请求-协议号：22006\n\n\n#### data定义\n\ncancel_type\n\n取消类型\n\nuint32\n\n是\n\n0：取消所有报价订阅，1：取消盘口报价订阅，2：取消成交报价订阅，3：取消汇率订阅\n\n\n### 数据结构(json)\n\n```text\n复制{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22006,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n        \"cancel_type\": 1\n    }\n}\n```\n\n\n## 应答-协议号：22007\n\n\n### 数据结构(json)\n\n```text\n复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22007,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }    \n}\n```\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于9个月前\n"
  rawContent: "复制\nWEBSOCKET API\nWEBSOCKET接口API\n取消报价订阅\n\nEnglish / 中文\n\n接口说明\n\n取消报价订阅\n\n请求-协议号：22006\ndata定义\n字段\n名称\n类型\n必填项\n说明\n\ncancel_type\n\n取消类型\n\nuint32\n\n是\n\n0：取消所有报价订阅，1：取消盘口报价订阅，2：取消成交报价订阅，3：取消汇率订阅\n\n数据结构(json)\n复制\n{\n\n    \"cmd_id\":22006,\n\n    \"seq_id\":123,\n\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n    \"data\":{\n\n        \"cancel_type\": 1\n\n    }\n\n}\n应答-协议号：22007\n数据结构(json)\n复制\n{\n\n    \"ret\":200,\n\n    \"msg\":\"ok\",\n\n    \"cmd_id\":22007,\n\n    \"seq_id\":123,\n\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n    \"data\":{\n\n    }    \n\n}\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n最新盘口(实时逐笔深度、Order Book)订阅\n下一页\n心跳\n\n最后更新于9个月前"
  suggestedFilename: "websocket-api_stock-websocket-interface-api_cancel-quote-subscription"
---

# 取消报价订阅

## 源URL

https://apis.alltick.co/websocket-api/stock-websocket-interface-api/cancel-quote-subscription

## 文档正文

1. Websocket APIchevron-right
1. Websocket接口API

English / 中文

## 接口说明

取消报价订阅

## 请求-协议号：22006

#### data定义

cancel_type

取消类型

uint32

是

0：取消所有报价订阅，1：取消盘口报价订阅，2：取消成交报价订阅，3：取消汇率订阅

### 数据结构(json)

```text
复制{
    "cmd_id":22006,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
        "cancel_type": 1
    }
}
```

```json
{
    "cmd_id":22006,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
        "cancel_type": 1
    }
}
```

```json
{
    "cmd_id":22006,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
        "cancel_type": 1
    }
}
```

## 应答-协议号：22007

### 数据结构(json)

```text
复制{
    "ret":200,
    "msg":"ok",
    "cmd_id":22007,
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
    "cmd_id":22007,
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
    "cmd_id":22007,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }    
}
```

#### AllTick网站

官方网站：https://alltick.co/

最后更新于9个月前
