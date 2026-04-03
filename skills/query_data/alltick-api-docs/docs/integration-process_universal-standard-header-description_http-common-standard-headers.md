---
id: "url-8f4fbfe"
type: "api"
title: "HTTP 通用标准头"
url: "https://apis.alltick.co/integration-process/universal-standard-header-description/http-common-standard-headers"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:20:34.867Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["接入流程chevron-right","通用标准头说明"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"请求通用标准头介绍","content":[{"type":"text","value":"trace"},{"type":"text","value":"跟踪号"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"请求者生成唯一，响应与请求将保持一致,最大长度64"},{"type":"text","value":"data"},{"type":"text","value":"数据体"},{"type":"text","value":"object"},{"type":"text","value":"是"},{"type":"text","value":"具体数据格式见各个接口定义"},{"type":"code","language":"text","value":"复制{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}"},{"type":"code","language":"json","value":"{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}"}]}
    - {"type":"heading","level":2,"title":"应答通用标准头介绍","content":[{"type":"text","value":"ret"},{"type":"text","value":"返回值"},{"type":"text","value":"int32"},{"type":"text","value":"错误码说明"},{"type":"text","value":"msg"},{"type":"text","value":"消息"},{"type":"text","value":"string"},{"type":"text","value":"对成功或者失败具体的描述"},{"type":"text","value":"trace"},{"type":"text","value":"跟踪号"},{"type":"text","value":"string"},{"type":"text","value":"请求者生成唯一，响应与请求将保持一致,最大长度64"},{"type":"text","value":"data"},{"type":"text","value":"数据体"},{"type":"text","value":"object"},{"type":"text","value":"具体数据格式见各个接口定义"},{"type":"code","language":"text","value":"复制{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}"},{"type":"code","language":"json","value":"{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于1年前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"json","value":"{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}"}
    - {"type":"code","language":"text","value":"复制{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}"}
    - {"type":"code","language":"json","value":"{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}"}
  tables: []
  parameters: []
  markdownContent: "# HTTP 通用标准头\n\n1. 接入流程chevron-right\n1. 通用标准头说明\n\nEnglish / 中文\n\n\n## 请求通用标准头介绍\n\ntrace\n\n跟踪号\n\nstring\n\n是\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n是\n\n具体数据格式见各个接口定义\n\n```text\n复制{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}\n```\n\n```json\n{\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }\n}\n```\n\n\n## 应答通用标准头介绍\n\nret\n\n返回值\n\nint32\n\n错误码说明\n\nmsg\n\n消息\n\nstring\n\n对成功或者失败具体的描述\n\ntrace\n\n跟踪号\n\nstring\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n具体数据格式见各个接口定义\n\n```text\n复制{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}\n```\n\n```json\n{\n    \"ret\":202,\n    \"msg\":\"request data param invalid\",\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n    \"data\":{\n    }    \n}\n```\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于1年前\n"
  rawContent: "复制\n接入流程\n通用标准头说明\nHTTP 通用标准头\n\nEnglish / 中文\n\n请求通用标准头介绍\n字段\n名称\n类型\n必填项\n说明\n\ntrace\n\n跟踪号\n\nstring\n\n是\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n是\n\n具体数据格式见各个接口定义\n\n复制\n{\n\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n\n    \"data\":{\n\n    }\n\n}\n应答通用标准头介绍\n字段\n名称\n类型\n说明\n\nret\n\n返回值\n\nint32\n\n错误码说明\n\nmsg\n\n消息\n\nstring\n\n对成功或者失败具体的描述\n\ntrace\n\n跟踪号\n\nstring\n\n请求者生成唯一，响应与请求将保持一致,最大长度64\n\ndata\n\n数据体\n\nobject\n\n具体数据格式见各个接口定义\n\n复制\n{\n\n    \"ret\":202,\n\n    \"msg\":\"request data param invalid\",\n\n    \"trace\":\"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n\n    \"data\":{\n\n    }    \n\n}\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n通用标准头说明\n下一页\nWebsocket 通用标准头\n\n最后更新于1年前"
  suggestedFilename: "integration-process_universal-standard-header-description_http-common-standard-headers"
---

# HTTP 通用标准头

## 源URL

https://apis.alltick.co/integration-process/universal-standard-header-description/http-common-standard-headers

## 文档正文

1. 接入流程chevron-right
1. 通用标准头说明

English / 中文

## 请求通用标准头介绍

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
    "trace":"c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
    "data":{
    }
}
```

```json
{
    "trace":"c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
    "data":{
    }
}
```

```json
{
    "trace":"c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
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
    "ret":202,
    "msg":"request data param invalid",
    "trace":"c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
    "data":{
    }    
}
```

```json
{
    "ret":202,
    "msg":"request data param invalid",
    "trace":"c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
    "data":{
    }    
}
```

```json
{
    "ret":202,
    "msg":"request data param invalid",
    "trace":"c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
    "data":{
    }    
}
```

#### AllTick网站

官方网站：https://alltick.co/

最后更新于1年前
