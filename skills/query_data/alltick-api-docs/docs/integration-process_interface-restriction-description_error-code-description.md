---
id: "url-4ba0b391"
type: "api"
title: "错误码说明"
url: "https://apis.alltick.co/integration-process/interface-restriction-description/error-code-description"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:58:20.738Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["接入流程chevron-right","接口限制说明"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"text","value":"200"}
    - {"type":"text","value":"ok"}
    - {"type":"text","value":"成功"}
    - {"type":"text","value":"400"}
    - {"type":"text","value":"request header param invalid"}
    - {"type":"text","value":"请求JSON第一层参数错误"}
    - {"type":"text","value":"排查建议："}
    - {"type":"text","value":"1、检查JSON结构是否完整。"}
    - {"type":"text","value":"2、确认所有必需字段已正确包含。"}
    - {"type":"text","value":"3、验证data字段是否为有效的对象类型。"}
    - {"type":"text","value":"4、核实trace等关键字段是否存在。"}
    - {"type":"text","value":"400"}
    - {"type":"text","value":"request data param invalid"}
    - {"type":"text","value":"请求JSON中data字段参数错误"}
    - {"type":"text","value":"排查建议："}
    - {"type":"text","value":"1、检查data字段是否为有效对象。"}
    - {"type":"text","value":"2、确认data中所有必需字段已正确填写。"}
    - {"type":"text","value":"3、对照具体接口文档，核实data字段内容。"}
    - {"type":"text","value":"4、特别注意POST请求中，确保body体中JSON参数完整且正确。"}
    - {"type":"text","value":"401"}
    - {"type":"text","value":"token invalid"}
    - {"type":"text","value":"token无效"}
    - {"type":"text","value":"可能由以下情况导致："}
    - {"type":"text","value":"1、Token格式不正确。"}
    - {"type":"text","value":"2、Token账号过期了。"}
    - {"type":"text","value":"402"}
    - {"type":"text","value":"query invalid"}
    - {"type":"text","value":"请求的query参数错误"}
    - {"type":"text","value":"排查建议："}
    - {"type":"text","value":"1、检查GET请求的query参数。"}
    - {"type":"text","value":"2、对query参数进行URL编码。"}
    - {"type":"text","value":"3、确保参数格式符合接口要求。"}
    - {"type":"text","value":"4、验证特殊字符是否正确转义。"}
    - {"type":"text","value":"429"}
    - {"type":"text","value":"Too Many Requests"}
    - {"type":"text","value":"超过套餐规定的请求频率"}
    - {"type":"text","value":"建议："}
    - {"type":"text","value":"1、优化请求频率和逻辑。"}
    - {"type":"text","value":"2、考虑升级套餐，获取更高的请求频率。 点击查看接口限制说明： HTTP接口限制 Websocket接口限制"}
    - {"type":"text","value":"600"}
    - {"type":"text","value":"code invalid"}
    - {"type":"text","value":"请求code产品无效"}
    - {"type":"text","value":"排查建议："}
    - {"type":"text","value":"1、检查请求URL： 仔细核对接口文档，股票类和外汇类贵金属类数据的请求URL是不同。 2、检查产品code："}
    - {"type":"text","value":"对照产品列表，确保代码有效且准确：[产品列表]"}
    - {"type":"text","value":"601"}
    - {"type":"text","value":"body empty"}
    - {"type":"text","value":"请求消息体数据为空"}
    - {"type":"text","value":"排查建议："}
    - {"type":"text","value":"1、检查POST请求的消息体。"}
    - {"type":"text","value":"2、确保body中包含完整的JSON参数。"}
    - {"type":"text","value":"3、特别注意批量获取/batch-kline等接口。"}
    - {"type":"text","value":"4、验证所有必需字段均已正确填写。"}
    - {"type":"text","value":"603"}
    - {"type":"text","value":"token level not enough"}
    - {"type":"text","value":"请求产品个数或者K线根数超过接口文档规定的限制"}
    - {"type":"text","value":"排查建议："}
    - {"type":"text","value":"1、检查产品数量： K线接口，确认同时请求的【产品数】加上【K线类型】的总和，是否超过套餐限制。 非K线接口，确认请求的产品数，是否超过套餐限制。"}
    - {"type":"text","value":"2、验证K线请求： 核实K线根数是否符合接口规定。 注意批量产品K线接口每次仅允许2根。 点击查看接口限制说明：HTTP接口限制"}
    - {"type":"text","value":"604"}
    - {"type":"text","value":"code unauthorized"}
    - {"type":"text","value":"您的token没有请求该code的权限"}
    - {"type":"text","value":"605"}
    - {"type":"text","value":"too many requests"}
    - {"type":"text","value":"请求频率限制"}
    - {"type":"text","value":"建议："}
    - {"type":"text","value":"1、优化请求频率和逻辑。"}
    - {"type":"text","value":"2、考虑升级套餐，获取更高的请求频率。 点击查看接口限制说明： HTTP接口限制 Websocket接口限制"}
    - {"type":"text","value":"606"}
    - {"type":"text","value":"too many requests and connection will be closed"}
    - {"type":"text","value":"一般是Websocket接口请求频率限制"}
    - {"type":"text","value":"排查建议："}
    - {"type":"text","value":"1、检查Websocket连接数。 确认是否超过套餐规定的最大连接数。"}
    - {"type":"text","value":"2、控制请求频率 确保多个Websocket请求时间隔至少3秒。 点击查看接口限制说明： Websocket接口限制"}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于3个月前"}]}
  codeExamples: []
  tables: []
  parameters: []
  markdownContent: "# 错误码说明\n\n1. 接入流程chevron-right\n1. 接口限制说明\n\nEnglish / 中文\n\n200\n\nok\n\n成功\n\n400\n\nrequest header param invalid\n\n请求JSON第一层参数错误\n\n排查建议：\n\n1、检查JSON结构是否完整。\n\n2、确认所有必需字段已正确包含。\n\n3、验证data字段是否为有效的对象类型。\n\n4、核实trace等关键字段是否存在。\n\n400\n\nrequest data param invalid\n\n请求JSON中data字段参数错误\n\n排查建议：\n\n1、检查data字段是否为有效对象。\n\n2、确认data中所有必需字段已正确填写。\n\n3、对照具体接口文档，核实data字段内容。\n\n4、特别注意POST请求中，确保body体中JSON参数完整且正确。\n\n401\n\ntoken invalid\n\ntoken无效\n\n可能由以下情况导致：\n\n1、Token格式不正确。\n\n2、Token账号过期了。\n\n402\n\nquery invalid\n\n请求的query参数错误\n\n排查建议：\n\n1、检查GET请求的query参数。\n\n2、对query参数进行URL编码。\n\n3、确保参数格式符合接口要求。\n\n4、验证特殊字符是否正确转义。\n\n429\n\nToo Many Requests\n\n超过套餐规定的请求频率\n\n建议：\n\n1、优化请求频率和逻辑。\n\n2、考虑升级套餐，获取更高的请求频率。 点击查看接口限制说明： HTTP接口限制 Websocket接口限制\n\n600\n\ncode invalid\n\n请求code产品无效\n\n排查建议：\n\n1、检查请求URL： 仔细核对接口文档，股票类和外汇类贵金属类数据的请求URL是不同。 2、检查产品code：\n\n对照产品列表，确保代码有效且准确：[产品列表]\n\n601\n\nbody empty\n\n请求消息体数据为空\n\n排查建议：\n\n1、检查POST请求的消息体。\n\n2、确保body中包含完整的JSON参数。\n\n3、特别注意批量获取/batch-kline等接口。\n\n4、验证所有必需字段均已正确填写。\n\n603\n\ntoken level not enough\n\n请求产品个数或者K线根数超过接口文档规定的限制\n\n排查建议：\n\n1、检查产品数量： K线接口，确认同时请求的【产品数】加上【K线类型】的总和，是否超过套餐限制。 非K线接口，确认请求的产品数，是否超过套餐限制。\n\n2、验证K线请求： 核实K线根数是否符合接口规定。 注意批量产品K线接口每次仅允许2根。 点击查看接口限制说明：HTTP接口限制\n\n604\n\ncode unauthorized\n\n您的token没有请求该code的权限\n\n605\n\ntoo many requests\n\n请求频率限制\n\n建议：\n\n1、优化请求频率和逻辑。\n\n2、考虑升级套餐，获取更高的请求频率。 点击查看接口限制说明： HTTP接口限制 Websocket接口限制\n\n606\n\ntoo many requests and connection will be closed\n\n一般是Websocket接口请求频率限制\n\n排查建议：\n\n1、检查Websocket连接数。 确认是否超过套餐规定的最大连接数。\n\n2、控制请求频率 确保多个Websocket请求时间隔至少3秒。 点击查看接口限制说明： Websocket接口限制\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于3个月前\n"
  rawContent: "复制\n接入流程\n接口限制说明\n错误码说明\n\nEnglish / 中文\n\n错误码\n错误内容\n含义\n\n200\n\nok\n\n成功\n\n400\n\nrequest header param invalid\n\n请求JSON第一层参数错误\n\n排查建议：\n\n1、检查JSON结构是否完整。\n\n2、确认所有必需字段已正确包含。\n\n3、验证data字段是否为有效的对象类型。\n\n4、核实trace等关键字段是否存在。\n\n400\n\nrequest data param invalid\n\n请求JSON中data字段参数错误\n\n排查建议：\n\n1、检查data字段是否为有效对象。\n\n2、确认data中所有必需字段已正确填写。\n\n3、对照具体接口文档，核实data字段内容。\n\n4、特别注意POST请求中，确保body体中JSON参数完整且正确。\n\n401\n\ntoken invalid\n\ntoken无效\n\n可能由以下情况导致：\n\n1、Token格式不正确。\n\n2、Token账号过期了。\n\n402\n\nquery invalid\n\n请求的query参数错误\n\n排查建议：\n\n1、检查GET请求的query参数。\n\n2、对query参数进行URL编码。\n\n3、确保参数格式符合接口要求。\n\n4、验证特殊字符是否正确转义。\n\n429\n\nToo Many Requests\n\n超过套餐规定的请求频率\n\n建议：\n\n1、优化请求频率和逻辑。\n\n2、考虑升级套餐，获取更高的请求频率。\n\n点击查看接口限制说明：\nHTTP接口限制\nWebsocket接口限制\n\n600\n\ncode invalid\n\n请求code产品无效\n\n排查建议：\n\n1、检查请求URL：\n仔细核对接口文档，股票类和外汇类贵金属类数据的请求URL是不同。\n2、检查产品code：\n\n对照产品列表，确保代码有效且准确：[产品列表]\n\n601\n\nbody empty\n\n请求消息体数据为空\n\n\n排查建议：\n\n1、检查POST请求的消息体。\n\n2、确保body中包含完整的JSON参数。\n\n3、特别注意批量获取/batch-kline等接口。\n\n4、验证所有必需字段均已正确填写。\n\n603 \n\ntoken level not enough \n\n请求产品个数或者K线根数超过接口文档规定的限制\n\n\n排查建议：\n\n1、检查产品数量：\nK线接口，确认同时请求的【产品数】加上【K线类型】的总和，是否超过套餐限制。\n非K线接口，确认请求的产品数，是否超过套餐限制。\n\n2、验证K线请求：\n核实K线根数是否符合接口规定。\n注意批量产品K线接口每次仅允许2根。\n\n点击查看接口限制说明：HTTP接口限制\n\n604\n\ncode unauthorized\n\n您的token没有请求该code的权限\n\n605\n\ntoo many requests\n\n请求频率限制\n\n\n建议：\n\n1、优化请求频率和逻辑。\n\n2、考虑升级套餐，获取更高的请求频率。\n\n点击查看接口限制说明：\nHTTP接口限制\nWebsocket接口限制\n\n606\n\ntoo many requests and connection will be closed\n\n一般是Websocket接口请求频率限制\n\n\n排查建议：\n\n1、检查Websocket连接数。\n确认是否超过套餐规定的最大连接数。\n\n2、控制请求频率\n确保多个Websocket请求时间隔至少3秒。\n\n点击查看接口限制说明：\nWebsocket接口限制\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nWebsocket 接口限制\n下一页\n通用标准头说明\n\n最后更新于3个月前"
  suggestedFilename: "integration-process_interface-restriction-description_error-code-description"
---

# 错误码说明

## 源URL

https://apis.alltick.co/integration-process/interface-restriction-description/error-code-description

## 文档正文

1. 接入流程chevron-right
1. 接口限制说明

English / 中文

200

ok

成功

400

request header param invalid

请求JSON第一层参数错误

排查建议：

1、检查JSON结构是否完整。

2、确认所有必需字段已正确包含。

3、验证data字段是否为有效的对象类型。

4、核实trace等关键字段是否存在。

400

request data param invalid

请求JSON中data字段参数错误

排查建议：

1、检查data字段是否为有效对象。

2、确认data中所有必需字段已正确填写。

3、对照具体接口文档，核实data字段内容。

4、特别注意POST请求中，确保body体中JSON参数完整且正确。

401

token invalid

token无效

可能由以下情况导致：

1、Token格式不正确。

2、Token账号过期了。

402

query invalid

请求的query参数错误

排查建议：

1、检查GET请求的query参数。

2、对query参数进行URL编码。

3、确保参数格式符合接口要求。

4、验证特殊字符是否正确转义。

429

Too Many Requests

超过套餐规定的请求频率

建议：

1、优化请求频率和逻辑。

2、考虑升级套餐，获取更高的请求频率。 点击查看接口限制说明： HTTP接口限制 Websocket接口限制

600

code invalid

请求code产品无效

排查建议：

1、检查请求URL： 仔细核对接口文档，股票类和外汇类贵金属类数据的请求URL是不同。 2、检查产品code：

对照产品列表，确保代码有效且准确：[产品列表]

601

body empty

请求消息体数据为空

排查建议：

1、检查POST请求的消息体。

2、确保body中包含完整的JSON参数。

3、特别注意批量获取/batch-kline等接口。

4、验证所有必需字段均已正确填写。

603

token level not enough

请求产品个数或者K线根数超过接口文档规定的限制

排查建议：

1、检查产品数量： K线接口，确认同时请求的【产品数】加上【K线类型】的总和，是否超过套餐限制。 非K线接口，确认请求的产品数，是否超过套餐限制。

2、验证K线请求： 核实K线根数是否符合接口规定。 注意批量产品K线接口每次仅允许2根。 点击查看接口限制说明：HTTP接口限制

604

code unauthorized

您的token没有请求该code的权限

605

too many requests

请求频率限制

建议：

1、优化请求频率和逻辑。

2、考虑升级套餐，获取更高的请求频率。 点击查看接口限制说明： HTTP接口限制 Websocket接口限制

606

too many requests and connection will be closed

一般是Websocket接口请求频率限制

排查建议：

1、检查Websocket连接数。 确认是否超过套餐规定的最大连接数。

2、控制请求频率 确保多个Websocket请求时间隔至少3秒。 点击查看接口限制说明： Websocket接口限制

#### AllTick网站

官方网站：https://alltick.co/

最后更新于3个月前
