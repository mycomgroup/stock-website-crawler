---
id: "url-56e2dd0e"
type: "api"
title: "GET 单产品历史K线查询（最高、最低、开盘、收盘价）"
url: "https://apis.alltick.co/rest-api/stock-http-interface-api/get-dan-chan-pin-li-shikxian-cha-xun"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:57:15.704Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["REST APIchevron-right","HTTP接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"GET /kline","content":[]}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"该接口可用来查询历史k线，但每次只能查询一个产品，建议将查询到的历史K线缓存本地数据库。"},{"type":"text","value":"使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下："},{"type":"list","ordered":false,"items":["首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。","然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。"]},{"type":"text","value":"这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。"}]}
    - {"type":"heading","level":2,"title":"请求频率","content":[{"type":"text","value":"免费"},{"type":"text","value":"每10秒，只能1次请求"},{"type":"text","value":"1、10秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"基础"},{"type":"text","value":"每1秒，只能1次请求"},{"type":"text","value":"1、同1秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"高级"},{"type":"text","value":"每1秒，最大可10次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求10次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"专业"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部港股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部A股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部美股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"}]}
    - {"type":"heading","level":2,"title":"接口限制","content":[{"type":"text","value":"1、请务必阅读：HTTP接口限制说明"},{"type":"text","value":"2、请务必阅读：错误码说明"}]}
    - {"type":"heading","level":2,"title":"接口地址","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-stock-b-api/kline","完整URL: https://quote.alltick.co/quote-stock-b-api/kline"]},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-b-api/kline","完整URL: https://quote.alltick.co/quote-b-api/kline"]}]}
    - {"type":"heading","level":2,"title":"请求示例","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据请求示例："},{"type":"text","value":"在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/kline?token=您的token&query=queryData"},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例："},{"type":"text","value":"在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/kline?token=您的token&query=queryData"}]}
    - {"type":"heading","level":2,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"query"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"查看query请求参数说明"}]}
    - {"type":"heading","level":2,"title":"query请求参数","content":[{"type":"code","language":"text","value":"复制{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}"},{"type":"text","value":"trace"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"追踪码，用来查询日志使用，请保证每次请求时唯一"},{"type":"text","value":"data"},{"type":"text","value":"object"},{"type":"text","value":"是"},{"type":"text","value":"» code"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"请查看code列表，选择你要查询的code：[点击code列表]"},{"type":"text","value":"» kline_type"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟 3、查询昨日收盘价，kline_type 传8"},{"type":"text","value":"» kline_timestamp_end"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"从指定时间往前查询K线 1、传0表示从当前最新的交易日往前查k线 2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线 3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持"},{"type":"text","value":"» query_kline_num"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"1、表示查询多少根K线，每次最大请求500根，可根据时间戳循环往前请求 2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价"},{"type":"text","value":"» adjust_type"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0"}]}
    - {"type":"heading","level":2,"title":"返回示例","content":[{"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}"}]}
    - {"type":"heading","level":2,"title":"返回结果","content":[{"type":"text","value":"200"},{"type":"text","value":"OK"},{"type":"text","value":"OK"},{"type":"text","value":"Inline"}]}
    - {"type":"heading","level":2,"title":"返回数据结构","content":[{"type":"text","value":"» ret"},{"type":"text","value":"integer"},{"type":"text","value":"true"},{"type":"text","value":"» msg"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"» trace"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"» data"},{"type":"text","value":"object"},{"type":"text","value":"true"},{"type":"text","value":"»» code"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"代码"},{"type":"text","value":"»» kline_type"},{"type":"text","value":"integer"},{"type":"text","value":"true"},{"type":"text","value":"k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟"},{"type":"text","value":"»» kline_list"},{"type":"text","value":"[object]"},{"type":"text","value":"true"},{"type":"text","value":"»»» timestamp"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线时间戳"},{"type":"text","value":"»»» open_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线开盘价"},{"type":"text","value":"»»» close_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线收盘价： 1、交易时段内，最新一根K线，该价格也是最新成交价 2、休市期间，最新一根K线，该价格是收盘价"},{"type":"text","value":"»»» high_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线最高价"},{"type":"text","value":"»»» low_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线最低价"},{"type":"text","value":"»»» volume"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线成交数量"},{"type":"text","value":"»»» turnover"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线成交金额"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}"}
    - {"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}"}
  tables: []
  parameters: []
  markdownContent: "# GET 单产品历史K线查询（最高、最低、开盘、收盘价）\n\n1. REST APIchevron-right\n1. HTTP接口API\n\nEnglish / 中文\n\n\n## GET /kline\n\n\n## 接口说明\n\n该接口可用来查询历史k线，但每次只能查询一个产品，建议将查询到的历史K线缓存本地数据库。\n\n使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下：\n\n- 首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。\n- 然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。\n\n这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。\n\n\n## 请求频率\n\n免费\n\n每10秒，只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1秒，只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1秒，最大可10次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n\n## 接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n\n## 接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n- 基本路径: /quote-stock-b-api/kline\n- 完整URL: https://quote.alltick.co/quote-stock-b-api/kline\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n- 基本路径: /quote-b-api/kline\n- 完整URL: https://quote.alltick.co/quote-b-api/kline\n\n\n## 请求示例\n\n1、美股、港股、A股、大盘数据请求示例：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/kline?token=您的token&query=queryData\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/kline?token=您的token&query=queryData\n\n\n## 请求参数\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\n\n## query请求参数\n\n```text\n复制{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_timestamp_end\": 0,\n    \"query_kline_num\": 2,\n    \"adjust_type\": 0\n  }\n}\n```\n\ntrace\n\nstring\n\n是\n\n追踪码，用来查询日志使用，请保证每次请求时唯一\n\ndata\n\nobject\n\n是\n\n» code\n\nstring\n\n是\n\n请查看code列表，选择你要查询的code：[点击code列表]\n\n» kline_type\n\ninteger\n\n是\n\nk线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟 3、查询昨日收盘价，kline_type 传8\n\n» kline_timestamp_end\n\ninteger\n\n是\n\n从指定时间往前查询K线 1、传0表示从当前最新的交易日往前查k线 2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线 3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持\n\n» query_kline_num\n\ninteger\n\n是\n\n1、表示查询多少根K线，每次最大请求500根，可根据时间戳循环往前请求 2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价\n\n» adjust_type\n\ninteger\n\n是\n\n复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0\n\n\n## 返回示例\n\n```text\n复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n  \"data\": {\n    \"code\": \"857.HK\",\n    \"kline_type\": 1,\n    \"kline_list\": [\n      {\n        \"timestamp\": \"1677829200\",\n        \"open_price\": \"136.421\",\n        \"close_price\": \"136.412\",\n        \"high_price\": \"136.422\",\n        \"low_price\": \"136.407\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      },\n      {\n        \"timestamp\": \"1677829260\",\n        \"open_price\": \"136.412\",\n        \"close_price\": \"136.401\",\n        \"high_price\": \"136.415\",\n        \"low_price\": \"136.397\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\"\n      }\n    ]\n  }\n}\n```\n\n\n## 返回结果\n\n200\n\nOK\n\nOK\n\nInline\n\n\n## 返回数据结构\n\n» ret\n\ninteger\n\ntrue\n\n» msg\n\nstring\n\ntrue\n\n» trace\n\nstring\n\ntrue\n\n» data\n\nobject\n\ntrue\n\n»» code\n\nstring\n\ntrue\n\n代码\n\n»» kline_type\n\ninteger\n\ntrue\n\nk线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟\n\n»» kline_list\n\n[object]\n\ntrue\n\n»»» timestamp\n\nstring\n\ntrue\n\n该K线时间戳\n\n»»» open_price\n\nstring\n\ntrue\n\n该K线开盘价\n\n»»» close_price\n\nstring\n\ntrue\n\n该K线收盘价： 1、交易时段内，最新一根K线，该价格也是最新成交价 2、休市期间，最新一根K线，该价格是收盘价\n\n»»» high_price\n\nstring\n\ntrue\n\n该K线最高价\n\n»»» low_price\n\nstring\n\ntrue\n\n该K线最低价\n\n»»» volume\n\nstring\n\ntrue\n\n该K线成交数量\n\n»»» turnover\n\nstring\n\ntrue\n\n该K线成交金额\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\nREST API\nHTTP接口API\nGET 单产品历史K线查询（最高、最低、开盘、收盘价）\n\nEnglish / 中文\n\nGET /kline\n接口说明\n\n该接口可用来查询历史k线，但每次只能查询一个产品，建议将查询到的历史K线缓存本地数据库。\n\n使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下：\n\n首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。\n\n然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。\n\n这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。\n\n请求频率\n计划\n单独请求\n同时请求多个http接口\n\n免费\n\n每10秒，只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒\n3、所有接口相加，1分钟最大请求10次(6秒1次)\n4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1秒，只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒\n3、所有接口相加，1分钟最大请求60次(1秒1次)\n4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1秒，最大可10次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒\n3、所有接口相加，1分钟最大请求600次(1秒10次)\n4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n基本路径: /quote-stock-b-api/kline\n\n完整URL: https://quote.alltick.co/quote-stock-b-api/kline\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n基本路径: /quote-b-api/kline\n\n完整URL: https://quote.alltick.co/quote-b-api/kline\n\n请求示例\n\n1、美股、港股、A股、大盘数据请求示例：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-stock-b-api/kline?token=您的token&query=queryData\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-b-api/kline?token=您的token&query=queryData\n\n请求参数\n名称\n位置\n类型\n必选\n说明\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\nquery请求参数\n复制\n{\n\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n  \"data\": {\n\n    \"code\": \"857.HK\",\n\n    \"kline_type\": 1,\n\n    \"kline_timestamp_end\": 0,\n\n    \"query_kline_num\": 2,\n\n    \"adjust_type\": 0\n\n  }\n\n}\n名称\n类型\n必选\n说明\n\ntrace\n\nstring\n\n是\n\n追踪码，用来查询日志使用，请保证每次请求时唯一\n\ndata\n\nobject\n\n是\n\n» code\n\nstring\n\n是\n\n请查看code列表，选择你要查询的code：[点击code列表]\n\n» kline_type\n\ninteger\n\n是\n\nk线类型\n1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K）\n2、最短的k线只支持1分钟\n3、查询昨日收盘价，kline_type 传8\n\n» kline_timestamp_end\n\ninteger\n\n是\n\n从指定时间往前查询K线\n1、传0表示从当前最新的交易日往前查k线\n2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线\n3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持\n\n» query_kline_num\n\ninteger\n\n是\n\n1、表示查询多少根K线，每次最大请求500根，可根据时间戳循环往前请求\n2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价\n\n» adjust_type\n\ninteger\n\n是\n\n复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0\n\n返回示例\n复制\n{\n\n  \"ret\": 200,\n\n  \"msg\": \"ok\",\n\n  \"trace\": \"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n\n  \"data\": {\n\n    \"code\": \"857.HK\",\n\n    \"kline_type\": 1,\n\n    \"kline_list\": [\n\n      {\n\n        \"timestamp\": \"1677829200\",\n\n        \"open_price\": \"136.421\",\n\n        \"close_price\": \"136.412\",\n\n        \"high_price\": \"136.422\",\n\n        \"low_price\": \"136.407\",\n\n        \"volume\": \"0\",\n\n        \"turnover\": \"0\"\n\n      },\n\n      {\n\n        \"timestamp\": \"1677829260\",\n\n        \"open_price\": \"136.412\",\n\n        \"close_price\": \"136.401\",\n\n        \"high_price\": \"136.415\",\n\n        \"low_price\": \"136.397\",\n\n        \"volume\": \"0\",\n\n        \"turnover\": \"0\"\n\n      }\n\n    ]\n\n  }\n\n}\n返回结果\n状态码\n状态码含义\n说明\n数据模型\n\n200\n\nOK\n\nOK\n\nInline\n\n返回数据结构\n名称\n类型\n必选\n说明\n\n» ret\n\ninteger\n\ntrue\n\n» msg\n\nstring\n\ntrue\n\n» trace\n\nstring\n\ntrue\n\n» data\n\nobject\n\ntrue\n\n»» code\n\nstring\n\ntrue\n\n代码\n\n»» kline_type\n\ninteger\n\ntrue\n\nk线类型\n1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K）\n2、最短的k线只支持1分钟\n\n»» kline_list\n\n[object]\n\ntrue\n\n»»» timestamp\n\nstring\n\ntrue\n\n该K线时间戳\n\n»»» open_price\n\nstring\n\ntrue\n\n该K线开盘价\n\n»»» close_price\n\nstring\n\ntrue\n\n该K线收盘价：\n1、交易时段内，最新一根K线，该价格也是最新成交价\n2、休市期间，最新一根K线，该价格是收盘价\n\n»»» high_price\n\nstring\n\ntrue\n\n该K线最高价\n\n»»» low_price\n\nstring\n\ntrue\n\n该K线最低价\n\n»»» volume\n\nstring\n\ntrue\n\n该K线成交数量\n\n»»» turnover\n\nstring\n\ntrue\n\n该K线成交金额\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nHTTP接口API\n下一页\nPOST 批量查询产品最新2根K线（最高、最低、开盘、收盘价）\n\n最后更新于5个月前"
  suggestedFilename: "rest-api_stock-http-interface-api_get-dan-chan-pin-li-shikxian-cha-xun"
---

# GET 单产品历史K线查询（最高、最低、开盘、收盘价）

## 源URL

https://apis.alltick.co/rest-api/stock-http-interface-api/get-dan-chan-pin-li-shikxian-cha-xun

## 文档正文

1. REST APIchevron-right
1. HTTP接口API

English / 中文

## GET /kline

## 接口说明

该接口可用来查询历史k线，但每次只能查询一个产品，建议将查询到的历史K线缓存本地数据库。

使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下：

- 首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。
- 然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。

这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。

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

- 基本路径: /quote-stock-b-api/kline
- 完整URL: https://quote.alltick.co/quote-stock-b-api/kline

2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：

- 基本路径: /quote-b-api/kline
- 完整URL: https://quote.alltick.co/quote-b-api/kline

## 请求示例

1、美股、港股、A股、大盘数据请求示例：

在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/kline?token=您的token&query=queryData

2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：

在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/kline?token=您的token&query=queryData

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

```text
复制{
  "trace": "3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
  "data": {
    "code": "857.HK",
    "kline_type": 1,
    "kline_timestamp_end": 0,
    "query_kline_num": 2,
    "adjust_type": 0
  }
}
```

```json
{
  "trace": "3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
  "data": {
    "code": "857.HK",
    "kline_type": 1,
    "kline_timestamp_end": 0,
    "query_kline_num": 2,
    "adjust_type": 0
  }
}
```

```json
{
  "trace": "3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
  "data": {
    "code": "857.HK",
    "kline_type": 1,
    "kline_timestamp_end": 0,
    "query_kline_num": 2,
    "adjust_type": 0
  }
}
```

trace

string

是

追踪码，用来查询日志使用，请保证每次请求时唯一

data

object

是

» code

string

是

请查看code列表，选择你要查询的code：[点击code列表]

» kline_type

integer

是

k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟 3、查询昨日收盘价，kline_type 传8

» kline_timestamp_end

integer

是

从指定时间往前查询K线 1、传0表示从当前最新的交易日往前查k线 2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线 3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持

» query_kline_num

integer

是

1、表示查询多少根K线，每次最大请求500根，可根据时间戳循环往前请求 2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价

» adjust_type

integer

是

复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0

## 返回示例

```text
复制{
  "ret": 200,
  "msg": "ok",
  "trace": "3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
  "data": {
    "code": "857.HK",
    "kline_type": 1,
    "kline_list": [
      {
        "timestamp": "1677829200",
        "open_price": "136.421",
        "close_price": "136.412",
        "high_price": "136.422",
        "low_price": "136.407",
        "volume": "0",
        "turnover": "0"
      },
      {
        "timestamp": "1677829260",
        "open_price": "136.412",
        "close_price": "136.401",
        "high_price": "136.415",
        "low_price": "136.397",
        "volume": "0",
        "turnover": "0"
      }
    ]
  }
}
```

```json
{
  "ret": 200,
  "msg": "ok",
  "trace": "3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
  "data": {
    "code": "857.HK",
    "kline_type": 1,
    "kline_list": [
      {
        "timestamp": "1677829200",
        "open_price": "136.421",
        "close_price": "136.412",
        "high_price": "136.422",
        "low_price": "136.407",
        "volume": "0",
        "turnover": "0"
      },
      {
        "timestamp": "1677829260",
        "open_price": "136.412",
        "close_price": "136.401",
        "high_price": "136.415",
        "low_price": "136.397",
        "volume": "0",
        "turnover": "0"
      }
    ]
  }
}
```

```json
{
  "ret": 200,
  "msg": "ok",
  "trace": "3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
  "data": {
    "code": "857.HK",
    "kline_type": 1,
    "kline_list": [
      {
        "timestamp": "1677829200",
        "open_price": "136.421",
        "close_price": "136.412",
        "high_price": "136.422",
        "low_price": "136.407",
        "volume": "0",
        "turnover": "0"
      },
      {
        "timestamp": "1677829260",
        "open_price": "136.412",
        "close_price": "136.401",
        "high_price": "136.415",
        "low_price": "136.397",
        "volume": "0",
        "turnover": "0"
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

## 返回数据结构

» ret

integer

true

» msg

string

true

» trace

string

true

» data

object

true

»» code

string

true

代码

»» kline_type

integer

true

k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟

»» kline_list

[object]

true

»»» timestamp

string

true

该K线时间戳

»»» open_price

string

true

该K线开盘价

»»» close_price

string

true

该K线收盘价： 1、交易时段内，最新一根K线，该价格也是最新成交价 2、休市期间，最新一根K线，该价格是收盘价

»»» high_price

string

true

该K线最高价

»»» low_price

string

true

该K线最低价

»»» volume

string

true

该K线成交数量

»»» turnover

string

true

该K线成交金额

#### AllTick网站

官方网站：https://alltick.co/

最后更新于5个月前
