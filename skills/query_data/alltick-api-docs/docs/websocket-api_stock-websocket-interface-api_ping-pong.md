---
id: "url-e4430bb"
type: "api"
title: "心跳"
url: "https://apis.alltick.co/websocket-api/stock-websocket-interface-api/ping-pong"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T03:34:04.592Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["Websocket APIchevron-right","Websocket接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"要求请求者每10秒发送一次，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接"}]}
    - {"type":"heading","level":2,"title":"请求-协议号：22000","content":[]}
    - {"type":"heading","level":3,"title":"数据结构(json)","content":[{"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}]}
    - {"type":"heading","level":2,"title":"应答-协议号：22001","content":[]}
    - {"type":"heading","level":3,"title":"数据结构(json)","content":[{"type":"code","language":"text","value":"复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于1年前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"text","value":"复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}"}
  tables: []
  parameters: []
  markdownContent: "# 心跳\n\n1. Websocket APIchevron-right\n1. Websocket接口API\n\nEnglish / 中文\n\n\n## 接口说明\n\n要求请求者每10秒发送一次，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接\n\n\n## 请求-协议号：22000\n\n\n### 数据结构(json)\n\n```text\n复制{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}\n```\n\n\n## 应答-协议号：22001\n\n\n### 数据结构(json)\n\n```text\n复制{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"ret\":200,\n    \"msg\":\"ok\",\n    \"cmd_id\":22001,\n    \"seq_id\":123,\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n    \"data\":{\n    }\n}\n```\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于1年前\n"
  rawContent: "复制\nWEBSOCKET API\nWEBSOCKET接口API\n心跳\n\nEnglish / 中文\n\n接口说明\n\n要求请求者每10秒发送一次，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接\n\n请求-协议号：22000\n数据结构(json)\n复制\n{\n\n    \"cmd_id\":22000,\n\n    \"seq_id\":123,\n\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n    \"data\":{\n\n    }\n\n}\n应答-协议号：22001\n数据结构(json)\n复制\n{\n\n    \"ret\":200,\n\n    \"msg\":\"ok\",\n\n    \"cmd_id\":22001,\n\n    \"seq_id\":123,\n\n    \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n    \"data\":{\n\n    }\n\n}\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n取消报价订阅\n下一页\nK线推送(不支持)\n\n最后更新于1年前"
  suggestedFilename: "websocket-api_stock-websocket-interface-api_ping-pong"
---

# 心跳

## 源URL

https://apis.alltick.co/websocket-api/stock-websocket-interface-api/ping-pong

## 文档正文

1. Websocket APIchevron-right
1. Websocket接口API

English / 中文

## 接口说明

要求请求者每10秒发送一次，在30秒内如果没有收到心跳请求，就会认为超时，断开请求者的websocket连接

## 请求-协议号：22000

### 数据结构(json)

```text
复制{
    "cmd_id":22000,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }
}
```

```json
{
    "cmd_id":22000,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }
}
```

```json
{
    "cmd_id":22000,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }
}
```

## 应答-协议号：22001

### 数据结构(json)

```text
复制{
    "ret":200,
    "msg":"ok",
    "cmd_id":22001,
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
    "cmd_id":22001,
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
    "cmd_id":22001,
    "seq_id":123,
    "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
    "data":{
    }
}
```

#### AllTick网站

官方网站：https://alltick.co/

最后更新于1年前
