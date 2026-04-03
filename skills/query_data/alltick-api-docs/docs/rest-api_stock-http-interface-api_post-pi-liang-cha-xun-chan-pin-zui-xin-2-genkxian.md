---
id: "url-5216fe64"
type: "api"
title: "POST 批量查询产品最新2根K线（最高、最低、开盘、收盘价）"
url: "https://apis.alltick.co/rest-api/stock-http-interface-api/post-pi-liang-cha-xun-chan-pin-zui-xin-2-genkxian"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:59:09.593Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["REST APIchevron-right","HTTP接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"POST /batch-kline","content":[]}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"该接口可以一次性批量查询多个产品，且可批量一次性查询多个k线类型（k线类型指的是1分钟，15分钟，30分钟等），但只能批量查询最新的2根k线。"},{"type":"text","value":"使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下："},{"type":"list","ordered":false,"items":["首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。","然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。"]},{"type":"text","value":"这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。"}]}
    - {"type":"heading","level":2,"title":"请求频率","content":[{"type":"text","value":"免费"},{"type":"text","value":"1、每10秒，可1次请求 2、每次可批量查询10组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"1、10秒只能请求1个接口 2、所有接口相加，1分钟最大请求10次(6秒1次) 3、需注意/batch-kline接口需间隔10秒 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"基础"},{"type":"text","value":"1、每3秒，只能1次请求 2、每次可批量查询100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"1、同1秒只能请求1个接口 2、所有接口相加，1分钟最大请求60次(1秒1次) 3、需注意/batch-kline接口需间隔3秒 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"高级"},{"type":"text","value":"1、每2秒，只能1次请求 2、每次可批量查询200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"1、所有接口相加，1分钟最大请求600次(1秒10次) 2、需注意/batch-kline接口需间隔2秒 3、每天总共最大可请求864000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"专业"},{"type":"text","value":"1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部港股"},{"type":"text","value":"1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部A股"},{"type":"text","value":"1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部美股"},{"type":"text","value":"1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"}]}
    - {"type":"heading","level":2,"title":"接口限制","content":[{"type":"text","value":"1、请务必阅读：HTTP接口限制说明"},{"type":"text","value":"2、请务必阅读：错误码说明"}]}
    - {"type":"heading","level":2,"title":"接口地址","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-stock-b-api/batch-kline","完整URL: https://quote.alltick.co/quote-stock-b-api/batch-kline"]},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-b-api/batch-kline","完整URL: https://quote.alltick.co/quote-b-api/batch-kline"]}]}
    - {"type":"heading","level":2,"title":"请求示例","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据请求示例："},{"type":"text","value":"批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。 在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/batch-kline?token=您的token"},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例："},{"type":"text","value":"批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。 在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/batch-kline?token=您的token"}]}
    - {"type":"heading","level":2,"title":"批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。","content":[]}
    - {"type":"heading","level":2,"title":"Body 请求参数","content":[{"type":"code","language":"text","value":"复制{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}"}]}
    - {"type":"heading","level":2,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"如果不知道你的token，请联系相关人员索要"},{"type":"text","value":"body"},{"type":"text","value":"body"},{"type":"text","value":"object"},{"type":"text","value":"否"},{"type":"text","value":"» trace"},{"type":"text","value":"body"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"追踪码，用来查询日志使用，请保证每次请求时唯一"},{"type":"text","value":"» data"},{"type":"text","value":"body"},{"type":"text","value":"object"},{"type":"text","value":"是"},{"type":"text","value":"»» data_list"},{"type":"text","value":"body"},{"type":"text","value":"[object]"},{"type":"text","value":"是"},{"type":"text","value":"»»» code"},{"type":"text","value":"body"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"请查看code列表，选择你要查询的code：[点击code列表]"},{"type":"text","value":"»»» kline_type"},{"type":"text","value":"body"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟 3、查询昨日收盘价，kline_type 传8"},{"type":"text","value":"»»» kline_timestamp_end"},{"type":"text","value":"body"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"从指定时间往前查询K线 1、传0表示从当前最新的交易日往前查k线 2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线 3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持"},{"type":"text","value":"»»» query_kline_num"},{"type":"text","value":"body"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"1、表示查询多少根K线，该接口最大只能查询2根k线 2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价"},{"type":"text","value":"»»» adjust_type"},{"type":"text","value":"body"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0"}]}
    - {"type":"heading","level":2,"title":"返回示例","content":[{"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}"}]}
    - {"type":"heading","level":2,"title":"返回结果","content":[{"type":"text","value":"200"},{"type":"text","value":"OK"},{"type":"text","value":"OK"},{"type":"text","value":"Inline"},{"type":"text","value":"» ret"},{"type":"text","value":"integer"},{"type":"text","value":"true"},{"type":"text","value":"» msg"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"» trace"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"» data"},{"type":"text","value":"object"},{"type":"text","value":"true"},{"type":"text","value":"»» kline_list"},{"type":"text","value":"[array]"},{"type":"text","value":"true"},{"type":"text","value":"»»» code"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"产品代码"},{"type":"text","value":"»»» kline_type"},{"type":"text","value":"integer"},{"type":"text","value":"true"},{"type":"text","value":"k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟"},{"type":"text","value":"»»» kline_data"},{"type":"text","value":"[array]"},{"type":"text","value":"true"},{"type":"text","value":"»»»» timestamp"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线时间戳"},{"type":"text","value":"»»»» open_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线开盘价"},{"type":"text","value":"»»»» close_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线收盘价： 1、交易时段内，最新一根K线，该价格也是最新成交价 2、休市期间，最新一根K线，该价格是收盘价"},{"type":"text","value":"»»»» high_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线最高价"},{"type":"text","value":"»»»» low_price"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线最低价"},{"type":"text","value":"»»»» volume"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线成交数量"},{"type":"text","value":"»»»» turnover"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"该K线成交金额"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}"}
  tables: []
  parameters: []
  markdownContent: "# POST 批量查询产品最新2根K线（最高、最低、开盘、收盘价）\n\n1. REST APIchevron-right\n1. HTTP接口API\n\nEnglish / 中文\n\n\n## POST /batch-kline\n\n\n## 接口说明\n\n该接口可以一次性批量查询多个产品，且可批量一次性查询多个k线类型（k线类型指的是1分钟，15分钟，30分钟等），但只能批量查询最新的2根k线。\n\n使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下：\n\n- 首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。\n- 然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。\n\n这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。\n\n\n## 请求频率\n\n免费\n\n1、每10秒，可1次请求 2、每次可批量查询10组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、10秒只能请求1个接口 2、所有接口相加，1分钟最大请求10次(6秒1次) 3、需注意/batch-kline接口需间隔10秒 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n1、每3秒，只能1次请求 2、每次可批量查询100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、同1秒只能请求1个接口 2、所有接口相加，1分钟最大请求60次(1秒1次) 3、需注意/batch-kline接口需间隔3秒 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n1、每2秒，只能1次请求 2、每次可批量查询200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求600次(1秒10次) 2、需注意/batch-kline接口需间隔2秒 3、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n\n## 接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n\n## 接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n- 基本路径: /quote-stock-b-api/batch-kline\n- 完整URL: https://quote.alltick.co/quote-stock-b-api/batch-kline\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n- 基本路径: /quote-b-api/batch-kline\n- 完整URL: https://quote.alltick.co/quote-b-api/batch-kline\n\n\n## 请求示例\n\n1、美股、港股、A股、大盘数据请求示例：\n\n批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。 在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/batch-kline?token=您的token\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：\n\n批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。 在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/batch-kline?token=您的token\n\n\n## 批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。\n\n\n## Body 请求参数\n\n```text\n复制{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"data_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_timestamp_end\": 0,\n        \"query_kline_num\": 1,\n        \"adjust_type\": 0\n      }\n    ]\n  }\n}\n```\n\n\n## 请求参数\n\ntoken\n\nquery\n\nstring\n\n是\n\n如果不知道你的token，请联系相关人员索要\n\nbody\n\nbody\n\nobject\n\n否\n\n» trace\n\nbody\n\nstring\n\n是\n\n追踪码，用来查询日志使用，请保证每次请求时唯一\n\n» data\n\nbody\n\nobject\n\n是\n\n»» data_list\n\nbody\n\n[object]\n\n是\n\n»»» code\n\nbody\n\nstring\n\n是\n\n请查看code列表，选择你要查询的code：[点击code列表]\n\n»»» kline_type\n\nbody\n\ninteger\n\n是\n\nk线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟 3、查询昨日收盘价，kline_type 传8\n\n»»» kline_timestamp_end\n\nbody\n\ninteger\n\n是\n\n从指定时间往前查询K线 1、传0表示从当前最新的交易日往前查k线 2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线 3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持\n\n»»» query_kline_num\n\nbody\n\ninteger\n\n是\n\n1、表示查询多少根K线，该接口最大只能查询2根k线 2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价\n\n»»» adjust_type\n\nbody\n\ninteger\n\n是\n\n复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0\n\n\n## 返回示例\n\n```text\n复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n  \"data\": {\n    \"kline_list\": [\n      {\n        \"code\": \"700.HK\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      },\n      {\n        \"code\": \"GOOGL.US\",\n        \"kline_type\": 1,\n        \"kline_data\": [\n          {\n            \"timestamp\": \"1677829200\",\n            \"open_price\": \"136.421\",\n            \"close_price\": \"136.412\",\n            \"high_price\": \"136.422\",\n            \"low_price\": \"136.407\",\n            \"volume\": \"0\",\n            \"turnover\": \"0\"\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n\n## 返回结果\n\n200\n\nOK\n\nOK\n\nInline\n\n» ret\n\ninteger\n\ntrue\n\n» msg\n\nstring\n\ntrue\n\n» trace\n\nstring\n\ntrue\n\n» data\n\nobject\n\ntrue\n\n»» kline_list\n\n[array]\n\ntrue\n\n»»» code\n\nstring\n\ntrue\n\n产品代码\n\n»»» kline_type\n\ninteger\n\ntrue\n\nk线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟\n\n»»» kline_data\n\n[array]\n\ntrue\n\n»»»» timestamp\n\nstring\n\ntrue\n\n该K线时间戳\n\n»»»» open_price\n\nstring\n\ntrue\n\n该K线开盘价\n\n»»»» close_price\n\nstring\n\ntrue\n\n该K线收盘价： 1、交易时段内，最新一根K线，该价格也是最新成交价 2、休市期间，最新一根K线，该价格是收盘价\n\n»»»» high_price\n\nstring\n\ntrue\n\n该K线最高价\n\n»»»» low_price\n\nstring\n\ntrue\n\n该K线最低价\n\n»»»» volume\n\nstring\n\ntrue\n\n该K线成交数量\n\n»»»» turnover\n\nstring\n\ntrue\n\n该K线成交金额\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\nREST API\nHTTP接口API\nPOST 批量查询产品最新2根K线（最高、最低、开盘、收盘价）\n\nEnglish / 中文\n\nPOST /batch-kline\n接口说明\n\n该接口可以一次性批量查询多个产品，且可批量一次性查询多个k线类型（k线类型指的是1分钟，15分钟，30分钟等），但只能批量查询最新的2根k线。\n\n使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下：\n\n首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。\n\n然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。 \n\n这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。\n\n请求频率\n计划\n单独请求\n同时请求多个http接口\n\n免费\n\n1、每10秒，可1次请求\n2、每次可批量查询10组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、10秒只能请求1个接口\n2、所有接口相加，1分钟最大请求10次(6秒1次)\n3、需注意/batch-kline接口需间隔10秒\n4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n1、每3秒，只能1次请求\n2、每次可批量查询100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、同1秒只能请求1个接口\n2、所有接口相加，1分钟最大请求60次(1秒1次)\n3、需注意/batch-kline接口需间隔3秒\n4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n1、每2秒，只能1次请求\n2、每次可批量查询200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求600次(1秒10次)\n2、需注意/batch-kline接口需间隔2秒\n3、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n1、每1秒，只能1次请求\n2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次)\n2、需注意/batch-kline接口需间隔1秒\n3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n1、每1秒，只能1次请求\n2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次)\n2、需注意/batch-kline接口需间隔1秒\n3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n1、每1秒，只能1次请求\n2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次)\n2、需注意/batch-kline接口需间隔1秒\n3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n1、每1秒，只能1次请求\n2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n1、所有接口相加，1分钟最大请求1200次(1秒20次)\n2、需注意/batch-kline接口需间隔1秒\n3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n基本路径: /quote-stock-b-api/batch-kline\n\n完整URL: https://quote.alltick.co/quote-stock-b-api/batch-kline\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n基本路径: /quote-b-api/batch-kline\n\n完整URL: https://quote.alltick.co/quote-b-api/batch-kline\n\n请求示例\n\n1、美股、港股、A股、大盘数据请求示例：\n\n批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-stock-b-api/batch-kline?token=您的token\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：\n\n批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-b-api/batch-kline?token=您的token\n\n批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。\nBody 请求参数\n复制\n{\n\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n\n  \"data\": {\n\n    \"data_list\": [\n\n      {\n\n        \"code\": \"700.HK\",\n\n        \"kline_type\": 1,\n\n        \"kline_timestamp_end\": 0,\n\n        \"query_kline_num\": 1,\n\n        \"adjust_type\": 0\n\n      },\n\n      {\n\n        \"code\": \"GOOGL.US\",\n\n        \"kline_type\": 1,\n\n        \"kline_timestamp_end\": 0,\n\n        \"query_kline_num\": 1,\n\n        \"adjust_type\": 0\n\n      }\n\n    ]\n\n  }\n\n}\n请求参数\n名称\n位置\n类型\n必选\n说明\n\ntoken\n\nquery\n\nstring\n\n是\n\n如果不知道你的token，请联系相关人员索要\n\nbody\n\nbody\n\nobject\n\n否\n\n» trace\n\nbody\n\nstring\n\n是\n\n追踪码，用来查询日志使用，请保证每次请求时唯一\n\n» data\n\nbody\n\nobject\n\n是\n\n»» data_list\n\nbody\n\n[object]\n\n是\n\n»»» code\n\nbody\n\nstring\n\n是\n\n请查看code列表，选择你要查询的code：[点击code列表]\n\n»»» kline_type\n\nbody\n\ninteger\n\n是\n\nk线类型\n1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K）\n2、最短的k线只支持1分钟\n3、查询昨日收盘价，kline_type 传8\n\n»»» kline_timestamp_end\n\nbody\n\ninteger\n\n是\n\n从指定时间往前查询K线\n1、传0表示从当前最新的交易日往前查k线\n2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线\n3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持\n\n»»» query_kline_num\n\nbody\n\ninteger\n\n是\n\n1、表示查询多少根K线，该接口最大只能查询2根k线\n2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价\n\n»»» adjust_type\n\nbody\n\ninteger\n\n是\n\n复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0\n\n返回示例\n复制\n{\n\n  \"ret\": 200,\n\n  \"msg\": \"ok\",\n\n  \"trace\": \"c2a8a146-a647-4d6f-ac07-8c4805bf0b74\",\n\n  \"data\": {\n\n    \"kline_list\": [\n\n      {\n\n        \"code\": \"700.HK\",\n\n        \"kline_type\": 1,\n\n        \"kline_data\": [\n\n          {\n\n            \"timestamp\": \"1677829200\",\n\n            \"open_price\": \"136.421\",\n\n            \"close_price\": \"136.412\",\n\n            \"high_price\": \"136.422\",\n\n            \"low_price\": \"136.407\",\n\n            \"volume\": \"0\",\n\n            \"turnover\": \"0\"\n\n          }\n\n        ]\n\n      },\n\n      {\n\n        \"code\": \"GOOGL.US\",\n\n        \"kline_type\": 1,\n\n        \"kline_data\": [\n\n          {\n\n            \"timestamp\": \"1677829200\",\n\n            \"open_price\": \"136.421\",\n\n            \"close_price\": \"136.412\",\n\n            \"high_price\": \"136.422\",\n\n            \"low_price\": \"136.407\",\n\n            \"volume\": \"0\",\n\n            \"turnover\": \"0\"\n\n          }\n\n        ]\n\n      }\n\n    ]\n\n  }\n\n}\n返回结果\n状态码\n状态码含义\n说明\n数据模型\n\n200\n\nOK\n\nOK\n\nInline\n\n名称\n类型\n必选\n说明\n\n» ret\n\ninteger\n\ntrue\n\n» msg\n\nstring\n\ntrue\n\n» trace\n\nstring\n\ntrue\n\n» data\n\nobject\n\ntrue\n\n»» kline_list\n\n[array]\n\ntrue\n\n»»» code\n\nstring\n\ntrue\n\n产品代码\n\n»»» kline_type\n\ninteger\n\ntrue\n\nk线类型\n1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K）\n2、最短的k线只支持1分钟\n\n»»» kline_data\n\n[array]\n\ntrue\n\n»»»» timestamp\n\nstring\n\ntrue\n\n该K线时间戳\n\n»»»» open_price\n\nstring\n\ntrue\n\n该K线开盘价\n\n»»»» close_price\n\nstring\n\ntrue\n\n该K线收盘价：\n1、交易时段内，最新一根K线，该价格也是最新成交价\n2、休市期间，最新一根K线，该价格是收盘价\n\n»»»» high_price\n\nstring\n\ntrue\n\n该K线最高价\n\n»»»» low_price\n\nstring\n\ntrue\n\n该K线最低价\n\n»»»» volume\n\nstring\n\ntrue\n\n该K线成交数量\n\n»»»» turnover\n\nstring\n\ntrue\n\n该K线成交金额\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nGET 单产品历史K线查询（最高、最低、开盘、收盘价）\n下一页\nGET 最新盘口(最新深度、Order Book)查询\n\n最后更新于5个月前"
  suggestedFilename: "rest-api_stock-http-interface-api_post-pi-liang-cha-xun-chan-pin-zui-xin-2-genkxian"
---

# POST 批量查询产品最新2根K线（最高、最低、开盘、收盘价）

## 源URL

https://apis.alltick.co/rest-api/stock-http-interface-api/post-pi-liang-cha-xun-chan-pin-zui-xin-2-genkxian

## 文档正文

1. REST APIchevron-right
1. HTTP接口API

English / 中文

## POST /batch-kline

## 接口说明

该接口可以一次性批量查询多个产品，且可批量一次性查询多个k线类型（k线类型指的是1分钟，15分钟，30分钟等），但只能批量查询最新的2根k线。

使用HTTP接口获取K线的客户，建议将/kline和/batch-kline这2个接口结合使用,步骤如下：

- 首先，通过 /kline 接口轮询请求历史数据并存储到本地数据库，后续历史数据可直接从客户的数据库获取，无需再通过接口请求。
- 然后，后续持续使用 /batch-kline 接口批量请求多个产品的最新2根K线，并将数据更新到数据库。

这种方式能够快速更新最新的K线，同时避免频繁请求历史K线造成频率受到限制。

## 请求频率

免费

1、每10秒，可1次请求 2、每次可批量查询10组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

1、10秒只能请求1个接口 2、所有接口相加，1分钟最大请求10次(6秒1次) 3、需注意/batch-kline接口需间隔10秒 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用

基础

1、每3秒，只能1次请求 2、每次可批量查询100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

1、同1秒只能请求1个接口 2、所有接口相加，1分钟最大请求60次(1秒1次) 3、需注意/batch-kline接口需间隔3秒 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用

高级

1、每2秒，只能1次请求 2、每次可批量查询200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

1、所有接口相加，1分钟最大请求600次(1秒10次) 2、需注意/batch-kline接口需间隔2秒 3、每天总共最大可请求864000次，超过则第二天凌晨恢复使用

专业

1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部港股

1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部A股

1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部美股

1、每1秒，只能1次请求 2、每次可批量查询500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

1、所有接口相加，1分钟最大请求1200次(1秒20次) 2、需注意/batch-kline接口需间隔1秒 3、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

## 接口限制

1、请务必阅读：HTTP接口限制说明

2、请务必阅读：错误码说明

## 接口地址

1、美股、港股、A股、大盘数据接口地址：

- 基本路径: /quote-stock-b-api/batch-kline
- 完整URL: https://quote.alltick.co/quote-stock-b-api/batch-kline

2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：

- 基本路径: /quote-b-api/batch-kline
- 完整URL: https://quote.alltick.co/quote-b-api/batch-kline

## 请求示例

1、美股、港股、A股、大盘数据请求示例：

批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。 在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/batch-kline?token=您的token

2、外汇、贵金属、加密货币、原油、CFD指数、商品请求示例：

批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。 在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/batch-kline?token=您的token

## 批量查询产品最新K线功能，由于批量查询参数比较多，放入body中，url参数中只保留token字段参数。

## Body 请求参数

```text
复制{
  "trace": "c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
  "data": {
    "data_list": [
      {
        "code": "700.HK",
        "kline_type": 1,
        "kline_timestamp_end": 0,
        "query_kline_num": 1,
        "adjust_type": 0
      },
      {
        "code": "GOOGL.US",
        "kline_type": 1,
        "kline_timestamp_end": 0,
        "query_kline_num": 1,
        "adjust_type": 0
      }
    ]
  }
}
```

```json
{
  "trace": "c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
  "data": {
    "data_list": [
      {
        "code": "700.HK",
        "kline_type": 1,
        "kline_timestamp_end": 0,
        "query_kline_num": 1,
        "adjust_type": 0
      },
      {
        "code": "GOOGL.US",
        "kline_type": 1,
        "kline_timestamp_end": 0,
        "query_kline_num": 1,
        "adjust_type": 0
      }
    ]
  }
}
```

```json
{
  "trace": "c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
  "data": {
    "data_list": [
      {
        "code": "700.HK",
        "kline_type": 1,
        "kline_timestamp_end": 0,
        "query_kline_num": 1,
        "adjust_type": 0
      },
      {
        "code": "GOOGL.US",
        "kline_type": 1,
        "kline_timestamp_end": 0,
        "query_kline_num": 1,
        "adjust_type": 0
      }
    ]
  }
}
```

## 请求参数

token

query

string

是

如果不知道你的token，请联系相关人员索要

body

body

object

否

» trace

body

string

是

追踪码，用来查询日志使用，请保证每次请求时唯一

» data

body

object

是

»» data_list

body

[object]

是

»»» code

body

string

是

请查看code列表，选择你要查询的code：[点击code列表]

»»» kline_type

body

integer

是

k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟 3、查询昨日收盘价，kline_type 传8

»»» kline_timestamp_end

body

integer

是

从指定时间往前查询K线 1、传0表示从当前最新的交易日往前查k线 2、指定时间请传时间戳，传时间戳表示从该时间戳往前查k线 3、只有外汇贵金属加密货币支持传时间戳，股票类的code不支持

»»» query_kline_num

body

integer

是

1、表示查询多少根K线，该接口最大只能查询2根k线 2、通过该字段可查询昨日收盘价，kline_type 传8，query_kline_num传2，返回2根k线数据中，时间戳较小的数据是昨日收盘价

»»» adjust_type

body

integer

是

复权类型,对于股票类的code才有效，例如：0:除权,1:前复权，目前仅支持0

## 返回示例

```text
复制{
  "ret": 200,
  "msg": "ok",
  "trace": "c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
  "data": {
    "kline_list": [
      {
        "code": "700.HK",
        "kline_type": 1,
        "kline_data": [
          {
            "timestamp": "1677829200",
            "open_price": "136.421",
            "close_price": "136.412",
            "high_price": "136.422",
            "low_price": "136.407",
            "volume": "0",
            "turnover": "0"
          }
        ]
      },
      {
        "code": "GOOGL.US",
        "kline_type": 1,
        "kline_data": [
          {
            "timestamp": "1677829200",
            "open_price": "136.421",
            "close_price": "136.412",
            "high_price": "136.422",
            "low_price": "136.407",
            "volume": "0",
            "turnover": "0"
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
  "trace": "c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
  "data": {
    "kline_list": [
      {
        "code": "700.HK",
        "kline_type": 1,
        "kline_data": [
          {
            "timestamp": "1677829200",
            "open_price": "136.421",
            "close_price": "136.412",
            "high_price": "136.422",
            "low_price": "136.407",
            "volume": "0",
            "turnover": "0"
          }
        ]
      },
      {
        "code": "GOOGL.US",
        "kline_type": 1,
        "kline_data": [
          {
            "timestamp": "1677829200",
            "open_price": "136.421",
            "close_price": "136.412",
            "high_price": "136.422",
            "low_price": "136.407",
            "volume": "0",
            "turnover": "0"
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
  "trace": "c2a8a146-a647-4d6f-ac07-8c4805bf0b74",
  "data": {
    "kline_list": [
      {
        "code": "700.HK",
        "kline_type": 1,
        "kline_data": [
          {
            "timestamp": "1677829200",
            "open_price": "136.421",
            "close_price": "136.412",
            "high_price": "136.422",
            "low_price": "136.407",
            "volume": "0",
            "turnover": "0"
          }
        ]
      },
      {
        "code": "GOOGL.US",
        "kline_type": 1,
        "kline_data": [
          {
            "timestamp": "1677829200",
            "open_price": "136.421",
            "close_price": "136.412",
            "high_price": "136.422",
            "low_price": "136.407",
            "volume": "0",
            "turnover": "0"
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

» msg

string

true

» trace

string

true

» data

object

true

»» kline_list

[array]

true

»»» code

string

true

产品代码

»»» kline_type

integer

true

k线类型 1、1是1分钟K，2是5分钟K，3是15分钟K，4是30分钟K，5是小时K，6是2小时K(股票不支持2小时)，7是4小时K(股票不支持4小时)，8是日K，9是周K，10是月K （注：股票不支持2小时K、4小时K） 2、最短的k线只支持1分钟

»»» kline_data

[array]

true

»»»» timestamp

string

true

该K线时间戳

»»»» open_price

string

true

该K线开盘价

»»»» close_price

string

true

该K线收盘价： 1、交易时段内，最新一根K线，该价格也是最新成交价 2、休市期间，最新一根K线，该价格是收盘价

»»»» high_price

string

true

该K线最高价

»»»» low_price

string

true

该K线最低价

»»»» volume

string

true

该K线成交数量

»»»» turnover

string

true

该K线成交金额

#### AllTick网站

官方网站：https://alltick.co/

最后更新于5个月前
