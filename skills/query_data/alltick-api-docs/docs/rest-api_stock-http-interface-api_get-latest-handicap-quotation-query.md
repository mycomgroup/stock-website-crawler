---
id: "url-3fcecf8b"
type: "api"
title: "GET 最新盘口(最新深度、Order Book)查询"
url: "https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-handicap-quotation-query"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:57:05.786Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["REST APIchevron-right","HTTP接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"GET /depth-tick","content":[]}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"以下是每类产品最大的盘口深度："},{"type":"text","value":"1、不活跃的产品存在小于下面列的最大档的情况，属于正常情况"},{"type":"text","value":"2、存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的"},{"type":"text","value":"深度说明"},{"type":"text","value":"最大1 档 (只有委托价，没有量)"},{"type":"text","value":"最大5档"},{"type":"text","value":"最大10档"},{"type":"text","value":"最大1档"},{"type":"text","value":"最大5档"}]}
    - {"type":"heading","level":2,"title":"请求频率","content":[{"type":"text","value":"免费"},{"type":"text","value":"每10秒，只能1次请求"},{"type":"text","value":"1、10秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"基础"},{"type":"text","value":"每1秒，只能1次请求"},{"type":"text","value":"1、同1秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"高级"},{"type":"text","value":"每1秒，最大可10次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求10次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"专业"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部港股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部A股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部美股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"}]}
    - {"type":"heading","level":2,"title":"接口限制","content":[{"type":"text","value":"1、请务必阅读：HTTP接口限制说明"},{"type":"text","value":"2、请务必阅读：错误码说明"}]}
    - {"type":"heading","level":2,"title":"接口地址","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-stock-b-api/depth-tick","完整URL: https://quote.alltick.co/quote-stock-b-api/depth-tick"]},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-b-api/depth-tick","完整URL: https://quote.alltick.co/quote-b-api/depth-tick"]}]}
    - {"type":"heading","level":2,"title":"请求示例","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据接口地址："},{"type":"text","value":"在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/depth-tick?token=您的token&query=queryData"},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址："},{"type":"text","value":"在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/depth-tick?token=您的token&query=queryData"}]}
    - {"type":"heading","level":2,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"query"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"查看query请求参数说明"}]}
    - {"type":"heading","level":2,"title":"query请求参数","content":[{"type":"text","value":"将如下json进行UrlEncode编码，赋值到url的查询字符串的query里"},{"type":"code","language":"text","value":"复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"text","value":"trace"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"data"},{"type":"text","value":"object"},{"type":"text","value":"是"},{"type":"text","value":"» symbol_list"},{"type":"text","value":"[object]"},{"type":"text","value":"是"},{"type":"text","value":"»» code"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"代码，选择你要查询的code：[点击code列表]"}]}
    - {"type":"heading","level":2,"title":"返回示例","content":[{"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}"}]}
    - {"type":"heading","level":2,"title":"返回结果","content":[{"type":"text","value":"200"},{"type":"text","value":"OK"},{"type":"text","value":"OK"},{"type":"text","value":"Inline"},{"type":"text","value":"» ret"},{"type":"text","value":"integer"},{"type":"text","value":"true"},{"type":"text","value":"返回code"},{"type":"text","value":"» msg"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"返回code对应消息"},{"type":"text","value":"» trace"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"请求的trace"},{"type":"text","value":"» data"},{"type":"text","value":"object"},{"type":"text","value":"true"},{"type":"text","value":"»» tick_list"},{"type":"text","value":"[object]"},{"type":"text","value":"true"},{"type":"text","value":"»»» code"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"代码"},{"type":"text","value":"»»» seq"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"报价序号"},{"type":"text","value":"»»» tick_time"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"报价时间戳"},{"type":"text","value":"»»» bids"},{"type":"text","value":"[object]"},{"type":"text","value":"false"},{"type":"text","value":"bid列表"},{"type":"text","value":"»»»» price"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"价"},{"type":"text","value":"»»»» volume"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"量"},{"type":"text","value":"»»» asks"},{"type":"text","value":"[object]"},{"type":"text","value":"false"},{"type":"text","value":"ask列表"},{"type":"text","value":"»»»» price"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"价"},{"type":"text","value":"»»»» volume"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"量 1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}"}
  tables: []
  parameters: []
  markdownContent: "# GET 最新盘口(最新深度、Order Book)查询\n\n1. REST APIchevron-right\n1. HTTP接口API\n\nEnglish / 中文\n\n\n## GET /depth-tick\n\n\n## 接口说明\n\n以下是每类产品最大的盘口深度：\n\n1、不活跃的产品存在小于下面列的最大档的情况，属于正常情况\n\n2、存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的\n\n深度说明\n\n最大1 档 (只有委托价，没有量)\n\n最大5档\n\n最大10档\n\n最大1档\n\n最大5档\n\n\n## 请求频率\n\n免费\n\n每10秒，只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1秒，只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1秒，最大可10次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n\n## 接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n\n## 接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n- 基本路径: /quote-stock-b-api/depth-tick\n- 完整URL: https://quote.alltick.co/quote-stock-b-api/depth-tick\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n- 基本路径: /quote-b-api/depth-tick\n- 完整URL: https://quote.alltick.co/quote-b-api/depth-tick\n\n\n## 请求示例\n\n1、美股、港股、A股、大盘数据接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/depth-tick?token=您的token&query=queryData\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/depth-tick?token=您的token&query=queryData\n\n\n## 请求参数\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\n\n## query请求参数\n\n将如下json进行UrlEncode编码，赋值到url的查询字符串的query里\n\n```text\n复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\ntrace\n\nstring\n\n是\n\ndata\n\nobject\n\n是\n\n» symbol_list\n\n[object]\n\n是\n\n»» code\n\nstring\n\n否\n\n代码，选择你要查询的code：[点击code列表]\n\n\n## 返回示例\n\n```text\n复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30686349\",\n        \"tick_time\": \"1677830357227\",\n        \"bids\": [\n          {\n            \"price\": \"136.424\",\n            \"volume\": \"100000.00\"\n          }\n        ],\n        \"asks\": [\n          {\n            \"price\": \"136.427\",\n            \"volume\": \"400000.00\"\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n\n## 返回结果\n\n200\n\nOK\n\nOK\n\nInline\n\n» ret\n\ninteger\n\ntrue\n\n返回code\n\n» msg\n\nstring\n\ntrue\n\n返回code对应消息\n\n» trace\n\nstring\n\ntrue\n\n请求的trace\n\n» data\n\nobject\n\ntrue\n\n»» tick_list\n\n[object]\n\ntrue\n\n»»» code\n\nstring\n\nfalse\n\n代码\n\n»»» seq\n\nstring\n\nfalse\n\n报价序号\n\n»»» tick_time\n\nstring\n\nfalse\n\n报价时间戳\n\n»»» bids\n\n[object]\n\nfalse\n\nbid列表\n\n»»»» price\n\nstring\n\nfalse\n\n价\n\n»»»» volume\n\nstring\n\nfalse\n\n量\n\n»»» asks\n\n[object]\n\nfalse\n\nask列表\n\n»»»» price\n\nstring\n\nfalse\n\n价\n\n»»»» volume\n\nstring\n\nfalse\n\n量 1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\nREST API\nHTTP接口API\nGET 最新盘口(最新深度、Order Book)查询\n\nEnglish / 中文\n\nGET /depth-tick\n接口说明\n\n以下是每类产品最大的盘口深度：\n\n1、不活跃的产品存在小于下面列的最大档的情况，属于正常情况\n\n2、存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的\n\n外汇、贵金属、原油\n加密货币\n港股\n美股\n沪深A股\n\n深度说明\n\n最大1 档\n(只有委托价，没有量)\n\n最大5档\n\n最大10档\n\n最大1档\n\n最大5档\n\n请求频率\n计划\n单独请求\n同时请求多个http接口\n\n免费\n\n每10秒，只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒\n3、所有接口相加，1分钟最大请求10次(6秒1次)\n4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1秒，只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒\n3、所有接口相加，1分钟最大请求60次(1秒1次)\n4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1秒，最大可10次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒\n3、所有接口相加，1分钟最大请求600次(1秒10次)\n4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n基本路径: /quote-stock-b-api/depth-tick\n\n完整URL: https://quote.alltick.co/quote-stock-b-api/depth-tick\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n基本路径: /quote-b-api/depth-tick\n\n完整URL: https://quote.alltick.co/quote-b-api/depth-tick\n\n请求示例\n\n1、美股、港股、A股、大盘数据接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-stock-b-api/depth-tick?token=您的token&query=queryData\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-b-api/depth-tick?token=您的token&query=queryData\n\n请求参数\n名称\n位置\n类型\n必选\n说明\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\nquery请求参数\n\n将如下json进行UrlEncode编码，赋值到url的查询字符串的query里\n\n复制\n{\n\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n\n  \"data\": {\n\n    \"symbol_list\": [\n\n      {\n\n        \"code\": \"857.HK\"\n\n      },\n\n      {\n\n        \"code\": \"UNH.US\"\n\n      }\n\n    ]\n\n  }\n\n}\n名称\n类型\n必选\n说明\n\ntrace\n\nstring\n\n是\n\ndata\n\nobject\n\n是\n\n» symbol_list\n\n[object]\n\n是\n\n»» code\n\nstring\n\n否\n\n代码，选择你要查询的code：[点击code列表]\n\n返回示例\n复制\n{\n\n  \"ret\": 200,\n\n  \"msg\": \"ok\",\n\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n\n  \"data\": {\n\n    \"tick_list\": [\n\n      {\n\n        \"code\": \"857.HK\",\n\n        \"seq\": \"30686349\",\n\n        \"tick_time\": \"1677830357227\",\n\n        \"bids\": [\n\n          {\n\n            \"price\": \"136.424\",\n\n            \"volume\": \"100000.00\"\n\n          }\n\n        ],\n\n        \"asks\": [\n\n          {\n\n            \"price\": \"136.427\",\n\n            \"volume\": \"400000.00\"\n\n          }\n\n        ]\n\n      }\n\n    ]\n\n  }\n\n}\n返回结果\n状态码\n状态码含义\n说明\n数据模型\n\n200\n\nOK\n\nOK\n\nInline\n\n名称\n类型\n必选\n说明\n\n» ret\n\ninteger\n\ntrue\n\n返回code\n\n» msg\n\nstring\n\ntrue\n\n返回code对应消息\n\n» trace\n\nstring\n\ntrue\n\n请求的trace\n\n» data\n\nobject\n\ntrue\n\n»» tick_list\n\n[object]\n\ntrue\n\n»»» code\n\nstring\n\nfalse\n\n代码\n\n»»» seq\n\nstring\n\nfalse\n\n报价序号\n\n»»» tick_time\n\nstring\n\nfalse\n\n报价时间戳\n\n»»» bids\n\n[object]\n\nfalse\n\nbid列表\n\n»»»» price\n\nstring\n\nfalse\n\n价\n\n»»»» volume\n\nstring\n\nfalse\n\n量\n\n»»» asks\n\n[object]\n\nfalse\n\nask列表\n\n»»»» price\n\nstring\n\nfalse\n\n价\n\n»»»» volume\n\nstring\n\nfalse\n\n量\n1、外汇、贵金属、CFD指数不提供volume\n2、股票，加密货币数据均提供volume\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nPOST 批量查询产品最新2根K线（最高、最低、开盘、收盘价）\n下一页\nGET 最新成交价(最新tick、当前价、最新价)批量查询\n\n最后更新于5个月前"
  suggestedFilename: "rest-api_stock-http-interface-api_get-latest-handicap-quotation-query"
---

# GET 最新盘口(最新深度、Order Book)查询

## 源URL

https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-handicap-quotation-query

## 文档正文

1. REST APIchevron-right
1. HTTP接口API

English / 中文

## GET /depth-tick

## 接口说明

以下是每类产品最大的盘口深度：

1、不活跃的产品存在小于下面列的最大档的情况，属于正常情况

2、存在单边深度是空的情况，例如股票涨停跌停时，单边盘口可能是空的

深度说明

最大1 档 (只有委托价，没有量)

最大5档

最大10档

最大1档

最大5档

## 请求频率

免费

每10秒，只能1次请求

1、10秒只能请求1个接口

2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用

基础

每1秒，只能1次请求

1、同1秒只能请求1个接口

2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用

高级

每1秒，最大可10次请求

1、所以接口相加，每1秒可请求10次

2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用

专业

每1秒，最大可20次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部港股

每1秒，最大可20次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部A股

每1秒，最大可20次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部美股

每1秒，最大可20次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

## 接口限制

1、请务必阅读：HTTP接口限制说明

2、请务必阅读：错误码说明

## 接口地址

1、美股、港股、A股、大盘数据接口地址：

- 基本路径: /quote-stock-b-api/depth-tick
- 完整URL: https://quote.alltick.co/quote-stock-b-api/depth-tick

2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：

- 基本路径: /quote-b-api/depth-tick
- 完整URL: https://quote.alltick.co/quote-b-api/depth-tick

## 请求示例

1、美股、港股、A股、大盘数据接口地址：

在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/depth-tick?token=您的token&query=queryData

2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：

在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/depth-tick?token=您的token&query=queryData

## 请求参数

token

query

string

否

query

query

string

否

查看query请求参数说明

## query请求参数

将如下json进行UrlEncode编码，赋值到url的查询字符串的query里

```text
复制{
  "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
  "data": {
    "symbol_list": [
      {
        "code": "857.HK"
      },
      {
        "code": "UNH.US"
      }
    ]
  }
}
```

```json
{
  "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
  "data": {
    "symbol_list": [
      {
        "code": "857.HK"
      },
      {
        "code": "UNH.US"
      }
    ]
  }
}
```

```json
{
  "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
  "data": {
    "symbol_list": [
      {
        "code": "857.HK"
      },
      {
        "code": "UNH.US"
      }
    ]
  }
}
```

trace

string

是

data

object

是

» symbol_list

[object]

是

»» code

string

否

代码，选择你要查询的code：[点击code列表]

## 返回示例

```text
复制{
  "ret": 200,
  "msg": "ok",
  "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
  "data": {
    "tick_list": [
      {
        "code": "857.HK",
        "seq": "30686349",
        "tick_time": "1677830357227",
        "bids": [
          {
            "price": "136.424",
            "volume": "100000.00"
          }
        ],
        "asks": [
          {
            "price": "136.427",
            "volume": "400000.00"
          }
        ]
      }
    ]
  }
}
```

```json
{
  "ret": 200,
  "msg": "ok",
  "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
  "data": {
    "tick_list": [
      {
        "code": "857.HK",
        "seq": "30686349",
        "tick_time": "1677830357227",
        "bids": [
          {
            "price": "136.424",
            "volume": "100000.00"
          }
        ],
        "asks": [
          {
            "price": "136.427",
            "volume": "400000.00"
          }
        ]
      }
    ]
  }
}
```

```json
{
  "ret": 200,
  "msg": "ok",
  "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
  "data": {
    "tick_list": [
      {
        "code": "857.HK",
        "seq": "30686349",
        "tick_time": "1677830357227",
        "bids": [
          {
            "price": "136.424",
            "volume": "100000.00"
          }
        ],
        "asks": [
          {
            "price": "136.427",
            "volume": "400000.00"
          }
        ]
      }
    ]
  }
}
```

## 返回结果

200

OK

OK

Inline

» ret

integer

true

返回code

» msg

string

true

返回code对应消息

» trace

string

true

请求的trace

» data

object

true

»» tick_list

[object]

true

»»» code

string

false

代码

»»» seq

string

false

报价序号

»»» tick_time

string

false

报价时间戳

»»» bids

[object]

false

bid列表

»»»» price

string

false

价

»»»» volume

string

false

量

»»» asks

[object]

false

ask列表

»»»» price

string

false

价

»»»» volume

string

false

量 1、外汇、贵金属、CFD指数不提供volume 2、股票，加密货币数据均提供volume

#### AllTick网站

官方网站：https://alltick.co/

最后更新于5个月前
