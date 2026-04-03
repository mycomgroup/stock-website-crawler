---
id: "url-309cf52c"
type: "api"
title: "Websocket 通用标准头"
url: "https://apis.alltick.co/integration-process/universal-standard-header-description/websocket-common-standard-header"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:20:54.465Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["接入流程chevron-right","通用标准头说明"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"请求通用标准头介绍","content":[{"type":"text","value":"cmd_id"},{"type":"text","value":"协议号"},{"type":"text","value":"uint32"},{"type":"text","value":"详见各个接口定义有提供"},{"type":"text","value":"seq_id"},{"type":"text","value":"序列号"},{"type":"text","value":"uint32"},{"type":"text","value":"是"},{"type":"text","value":"请求者生成唯一，响应与请求将保持一致"},{"type":"text","value":"trace"},{"type":"text","value":"跟踪号"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"请求者生成唯一，响应与请求将保持一致,最大长度64"},{"type":"text","value":"data"},{"type":"text","value":"数据体"},{"type":"text","value":"object"},{"type":"text","value":"是"},{"type":"text","value":"具体数据格式见各个接口定义"},{"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}"}]}
    - {"type":"heading","level":2,"title":"应答通用标准头介绍","content":[{"type":"text","value":"ret"},{"type":"text","value":"返回值"},{"type":"text","value":"int32"},{"type":"text","value":"错误码说明"},{"type":"text","value":"msg"},{"type":"text","value":"消息"},{"type":"text","value":"string"},{"type":"text","value":"对成功或者失败具体的描述"},{"type":"text","value":"cmd_id"},{"type":"text","value":"协议号"},{"type":"text","value":"uint32"},{"type":"text","value":"详见各个接口定义有提供"},{"type":"text","value":"seq_id"},{"type":"text","value":"序列号"},{"type":"text","value":"uint32"},{"type":"text","value":"请求者生成唯一，响应与请求将保持一致"},{"type":"text","value":"trace"},{"type":"text","value":"跟踪号"},{"type":"text","value":"string"},{"type":"text","value":"请求者生成唯一，响应与请求将保持一致,最大长度64"},{"type":"text","value":"data"},{"type":"text","value":"数据体"},{"type":"text","value":"object"},{"type":"text","value":"具体数据格式见各个接口定义"},{"type":"code","language":"text","value":"复制{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于1年前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"text","value":"复制{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}"}
  tables: []
  parameters: []
  markdownContent: "# Websocket 通用标准头\n\n1. 接入流程chevron-right\n1. 通用标准头说明\n\nEnglish / 中文\n\n\n## 请求通用标准头介绍\n\ncmd_id\n\n协议号\n\nuint32\n\n详见各个接口定义有提供\n\nseq_id\n\n序列号\n\nuint32\n\n是\n\n请求者生成唯一，响应与请求将保持一致\n\ntrace\n\n跟踪号\n\nstring\n\n是\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n是\n\n具体数据格式见各个接口定义\n\n```text\n复制{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"cmd_id\":22000,\n    \"seq_id\":123,\n    \"trace\":\"asdfsdfa\",\n    \"data\":{\n    }\n}\n```\n\n\n## 应答通用标准头介绍\n\nret\n\n返回值\n\nint32\n\n错误码说明\n\nmsg\n\n消息\n\nstring\n\n对成功或者失败具体的描述\n\ncmd_id\n\n协议号\n\nuint32\n\n详见各个接口定义有提供\n\nseq_id\n\n序列号\n\nuint32\n\n请求者生成唯一，响应与请求将保持一致\n\ntrace\n\n跟踪号\n\nstring\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n具体数据格式见各个接口定义\n\n```text\n复制{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":201,\n    \"msg\":\"request header param invalid\",\n    \"cmd_id\":0,\n    \"seq_id\":0,\n    \"trace\":\"\",\n    \"data\":{\n    }    \n}\n```\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于1年前\n"
  rawContent: "复制\n接入流程\n通用标准头说明\nWebsocket 通用标准头\n\nEnglish / 中文\n\n请求通用标准头介绍\n字段\n名称\n类型\n必填项\n说明\n\ncmd_id\n\n协议号\n\nuint32\n\n详见各个接口定义有提供\n\nseq_id\n\n序列号\n\nuint32\n\n是\n\n请求者生成唯一，响应与请求将保持一致\n\ntrace\n\n跟踪号\n\nstring\n\n是\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n是\n\n具体数据格式见各个接口定义\n\n复制\n{\n\n    \"cmd_id\":22000,\n\n    \"seq_id\":123,\n\n    \"trace\":\"asdfsdfa\",\n\n    \"data\":{\n\n    }\n\n}\n应答通用标准头介绍\n字段\n名称\n类型\n说明\n\nret\n\n返回值\n\nint32\n\n错误码说明\n\nmsg\n\n消息\n\nstring\n\n对成功或者失败具体的描述\n\ncmd_id\n\n协议号\n\nuint32\n\n详见各个接口定义有提供\n\nseq_id\n\n序列号\n\nuint32\n\n请求者生成唯一，响应与请求将保持一致\n\ntrace\n\n跟踪号\n\nstring\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n具体数据格式见各个接口定义\n\n复制\n{\n\n    \"ret\":201,\n\n    \"msg\":\"request header param invalid\",\n\n    \"cmd_id\":0,\n\n    \"seq_id\":0,\n\n    \"trace\":\"\",\n\n    \"data\":{\n\n    }    \n\n}\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nHTTP 通用标准头\n下一页\n产品 Code 列表\n\n最后更新于1年前"
  suggestedFilename: "integration-process_universal-standard-header-description_websocket-common-standard-header"
---

# Websocket 通用标准头

## 源URL

https://apis.alltick.co/integration-process/universal-standard-header-description/websocket-common-standard-header

## 文档正文

1. 接入流程chevron-right
1. 通用标准头说明

English / 中文

## 请求通用标准头介绍

cmd_id

协议号

uint32

详见各个接口定义有提供

seq_id

序列号

uint32

是

请求者生成唯一，响应与请求将保持一致

trace

跟踪号

string

是

请求者生成唯一，响应与请求将保持一致,最大长度64

data

数据体

object

是

具体数据格式见各个接口定义

```text
复制{
    "cmd_id":22000,
    "seq_id":123,
    "trace":"asdfsdfa",
    "data":{
    }
}
```

```json
{
    "cmd_id":22000,
    "seq_id":123,
    "trace":"asdfsdfa",
    "data":{
    }
}
```

```json
{
    "cmd_id":22000,
    "seq_id":123,
    "trace":"asdfsdfa",
    "data":{
    }
}
```

## 应答通用标准头介绍

ret

返回值

int32

错误码说明

msg

消息

string

对成功或者失败具体的描述

cmd_id

协议号

uint32

详见各个接口定义有提供

seq_id

序列号

uint32

请求者生成唯一，响应与请求将保持一致

trace

跟踪号

string

请求者生成唯一，响应与请求将保持一致,最大长度64

data

数据体

object

具体数据格式见各个接口定义

```text
复制{
    "ret":201,
    "msg":"request header param invalid",
    "cmd_id":0,
    "seq_id":0,
    "trace":"",
    "data":{
    }    
}
```

```json
{
    "ret":201,
    "msg":"request header param invalid",
    "cmd_id":0,
    "seq_id":0,
    "trace":"",
    "data":{
    }    
}
```

```json
{
    "ret":201,
    "msg":"request header param invalid",
    "cmd_id":0,
    "seq_id":0,
    "trace":"",
    "data":{
    }    
}
```

#### AllTick网站

官方网站：https://alltick.co/

最后更新于1年前
