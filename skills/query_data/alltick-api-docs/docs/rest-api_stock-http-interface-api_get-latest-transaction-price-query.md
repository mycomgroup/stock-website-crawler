---
id: "url-6c8fb15c"
type: "api"
title: "GET 最新成交价(最新tick、当前价、最新价)批量查询"
url: "https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-transaction-price-query"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:57:00.698Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["REST APIchevron-right","HTTP接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"GET /trade-tick","content":[]}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"该接口支持批量请求产品的最新成交价(最新逐笔Tick数据、也是当前价、最新价)，不支持请求历史成交价(历史逐笔tick数据)。"}]}
    - {"type":"heading","level":2,"title":"请求频率","content":[{"type":"text","value":"免费"},{"type":"text","value":"1、每10秒，只能1次请求 2、每次最大可批量查询5个产品"},{"type":"text","value":"1、10秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"基础"},{"type":"text","value":"1、每1秒，只能1次请求 2、由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"1、同1秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"高级"},{"type":"text","value":"1、每1秒，最大可10次请求 2、由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"1、所以接口相加，每1秒可请求10次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"专业"},{"type":"text","value":"1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部港股"},{"type":"text","value":"1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部A股"},{"type":"text","value":"1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部美股"},{"type":"text","value":"1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"}]}
    - {"type":"heading","level":2,"title":"接口限制","content":[{"type":"text","value":"1、请务必阅读：HTTP接口限制说明"},{"type":"text","value":"2、请务必阅读：错误码说明"}]}
    - {"type":"heading","level":2,"title":"接口地址","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-stock-b-api/trade-tick","完整URL: https://quote.alltick.co/quote-stock-b-api/trade-tick"]},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址："},{"type":"list","ordered":false,"items":["基本路径: /quote-b-api/trade-tick","完整URL: https://quote.alltick.co/quote-b-api/trade-tick"]}]}
    - {"type":"heading","level":2,"title":"请求示例","content":[{"type":"text","value":"1、美股、港股、A股、大盘数据接口地址："},{"type":"text","value":"在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/trade-tick?token=您的token&query=queryData"},{"type":"text","value":"2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址："},{"type":"text","value":"在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/trade-tick?token=您的token&query=queryData"}]}
    - {"type":"heading","level":2,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"query"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"查看query请求参数说明"}]}
    - {"type":"heading","level":2,"title":"query请求参数","content":[{"type":"text","value":"将如下json进行UrlEncode编码，赋值到url的查询字符串的query里"},{"type":"code","language":"text","value":"复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"text","value":"trace"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"data"},{"type":"text","value":"object"},{"type":"text","value":"是"},{"type":"text","value":"» symbol_list"},{"type":"text","value":"[object]"},{"type":"text","value":"是"},{"type":"text","value":"»» code"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"代码：[点击code列表]"}]}
    - {"type":"heading","level":2,"title":"返回示例","content":[{"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}"}]}
    - {"type":"heading","level":2,"title":"返回结果","content":[{"type":"text","value":"200"},{"type":"text","value":"OK"},{"type":"text","value":"OK"},{"type":"text","value":"Inline"},{"type":"text","value":"» ret"},{"type":"text","value":"integer"},{"type":"text","value":"true"},{"type":"text","value":"返回code"},{"type":"text","value":"» msg"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"返回code对应消息"},{"type":"text","value":"» trace"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"请求的trace"},{"type":"text","value":"» data"},{"type":"text","value":"object"},{"type":"text","value":"true"},{"type":"text","value":"»» tick_list"},{"type":"text","value":"[object]"},{"type":"text","value":"true"},{"type":"text","value":"»»» code"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"代码"},{"type":"text","value":"»»» seq"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"序号"},{"type":"text","value":"»»» tick_time"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"时间戳"},{"type":"text","value":"»»» price"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"成交价"},{"type":"text","value":"»»» volume"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"成交量"},{"type":"text","value":"»»» turnover"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"成交额： 1、外汇、贵金属、能源不返回成交额，可自行根据每次推送的数据计算，计算公式：turnover = price * volume 2、股票、加密货币正常返回成交额。"},{"type":"text","value":"»»» trade_direction"},{"type":"text","value":"integer"},{"type":"text","value":"false"},{"type":"text","value":"交易方向： 1、0为默认值，1为Buy，2为SELL 2、外汇、贵金属、能源默认只会返回0 3、股票、加密货币根据市场情况会返回0、1、2 4、详细说明： 0:表示中性盘，即以买一价与卖一价之间的价格撮合成交。 1:表示主动买入，即以卖一价或者更高价格成交的股票 2:表示主动卖出，即以买一价或者更低价格成交的股票"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}"}
  tables: []
  parameters: []
  markdownContent: "# GET 最新成交价(最新tick、当前价、最新价)批量查询\n\n1. REST APIchevron-right\n1. HTTP接口API\n\nEnglish / 中文\n\n\n## GET /trade-tick\n\n\n## 接口说明\n\n该接口支持批量请求产品的最新成交价(最新逐笔Tick数据、也是当前价、最新价)，不支持请求历史成交价(历史逐笔tick数据)。\n\n\n## 请求频率\n\n免费\n\n1、每10秒，只能1次请求 2、每次最大可批量查询5个产品\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n1、每1秒，只能1次请求 2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n1、每1秒，最大可10次请求 2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n\n## 接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n\n## 接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n- 基本路径: /quote-stock-b-api/trade-tick\n- 完整URL: https://quote.alltick.co/quote-stock-b-api/trade-tick\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n- 基本路径: /quote-b-api/trade-tick\n- 完整URL: https://quote.alltick.co/quote-b-api/trade-tick\n\n\n## 请求示例\n\n1、美股、港股、A股、大盘数据接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/trade-tick?token=您的token&query=queryData\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/trade-tick?token=您的token&query=queryData\n\n\n## 请求参数\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\n\n## query请求参数\n\n将如下json进行UrlEncode编码，赋值到url的查询字符串的query里\n\n```text\n复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\ntrace\n\nstring\n\n是\n\ndata\n\nobject\n\n是\n\n» symbol_list\n\n[object]\n\n是\n\n»» code\n\nstring\n\n否\n\n代码：[点击code列表]\n\n\n## 返回示例\n\n```text\n复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"tick_list\": [\n      {\n        \"code\": \"857.HK\",\n        \"seq\": \"30841439\",\n        \"tick_time\": \"1677831545217\",\n        \"price\": \"136.302\",\n        \"volume\": \"0\",\n        \"turnover\": \"0\",\n        \"trade_direction\": 0\n      }\n    ]\n  }\n}\n```\n\n\n## 返回结果\n\n200\n\nOK\n\nOK\n\nInline\n\n» ret\n\ninteger\n\ntrue\n\n返回code\n\n» msg\n\nstring\n\ntrue\n\n返回code对应消息\n\n» trace\n\nstring\n\ntrue\n\n请求的trace\n\n» data\n\nobject\n\ntrue\n\n»» tick_list\n\n[object]\n\ntrue\n\n»»» code\n\nstring\n\nfalse\n\n代码\n\n»»» seq\n\nstring\n\nfalse\n\n序号\n\n»»» tick_time\n\nstring\n\nfalse\n\n时间戳\n\n»»» price\n\nstring\n\nfalse\n\n成交价\n\n»»» volume\n\nstring\n\nfalse\n\n成交量\n\n»»» turnover\n\nstring\n\nfalse\n\n成交额： 1、外汇、贵金属、能源不返回成交额，可自行根据每次推送的数据计算，计算公式：turnover = price * volume 2、股票、加密货币正常返回成交额。\n\n»»» trade_direction\n\ninteger\n\nfalse\n\n交易方向： 1、0为默认值，1为Buy，2为SELL 2、外汇、贵金属、能源默认只会返回0 3、股票、加密货币根据市场情况会返回0、1、2 4、详细说明： 0:表示中性盘，即以买一价与卖一价之间的价格撮合成交。 1:表示主动买入，即以卖一价或者更高价格成交的股票 2:表示主动卖出，即以买一价或者更低价格成交的股票\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\nREST API\nHTTP接口API\nGET 最新成交价(最新tick、当前价、最新价)批量查询\n\nEnglish / 中文\n\nGET /trade-tick\n接口说明\n\n该接口支持批量请求产品的最新成交价(最新逐笔Tick数据、也是当前价、最新价)，不支持请求历史成交价(历史逐笔tick数据)。\n\n请求频率\n计划\n单独请求\n同时请求多个http接口\n\n免费\n\n1、每10秒，只能1次请求\n2、每次最大可批量查询5个产品\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒\n3、所有接口相加，1分钟最大请求10次(6秒1次)\n4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n1、每1秒，只能1次请求\n2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒\n3、所有接口相加，1分钟最大请求60次(1秒1次)\n4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n1、每1秒，最大可10次请求\n2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒\n3、所有接口相加，1分钟最大请求600次(1秒10次)\n4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n1、每1秒，最大可20次请求\n2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n1、每1秒，最大可20次请求\n2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n1、每1秒，最大可20次请求\n2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n1、每1秒，最大可20次请求\n2、由于GET请求url长度限制，每次最大建议请求50个code\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n接口地址\n\n1、美股、港股、A股、大盘数据接口地址：\n\n基本路径: /quote-stock-b-api/trade-tick\n\n完整URL: https://quote.alltick.co/quote-stock-b-api/trade-tick\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n基本路径: /quote-b-api/trade-tick\n\n完整URL: https://quote.alltick.co/quote-b-api/trade-tick\n\n请求示例\n\n1、美股、港股、A股、大盘数据接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-stock-b-api/trade-tick?token=您的token&query=queryData\n\n2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\nhttps://quote.alltick.co/quote-b-api/trade-tick?token=您的token&query=queryData\n\n请求参数\n名称\n位置\n类型\n必选\n说明\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\nquery请求参数\n\n将如下json进行UrlEncode编码，赋值到url的查询字符串的query里\n\n复制\n{\n\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n\n  \"data\": {\n\n    \"symbol_list\": [\n\n      {\n\n        \"code\": \"857.HK\"\n\n      },\n\n      {\n\n        \"code\": \"UNH.US\"\n\n      }\n\n    ]\n\n  }\n\n}\n名称\n类型\n必选\n说明\n\ntrace\n\nstring\n\n是\n\ndata\n\nobject\n\n是\n\n» symbol_list\n\n[object]\n\n是\n\n»» code\n\nstring\n\n否\n\n代码：[点击code列表]\n\n返回示例\n复制\n{\n\n  \"ret\": 200,\n\n  \"msg\": \"ok\",\n\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n\n  \"data\": {\n\n    \"tick_list\": [\n\n      {\n\n        \"code\": \"857.HK\",\n\n        \"seq\": \"30841439\",\n\n        \"tick_time\": \"1677831545217\",\n\n        \"price\": \"136.302\",\n\n        \"volume\": \"0\",\n\n        \"turnover\": \"0\",\n\n        \"trade_direction\": 0\n\n      }\n\n    ]\n\n  }\n\n}\n返回结果\n状态码\n状态码含义\n说明\n数据模型\n\n200\n\nOK\n\nOK\n\nInline\n\n名称\n类型\n必选\n说明\n\n» ret\n\ninteger\n\ntrue\n\n返回code\n\n» msg\n\nstring\n\ntrue\n\n返回code对应消息\n\n» trace\n\nstring\n\ntrue\n\n请求的trace\n\n» data\n\nobject\n\ntrue\n\n»» tick_list\n\n[object]\n\ntrue\n\n»»» code\n\nstring\n\nfalse\n\n代码\n\n»»» seq\n\nstring\n\nfalse\n\n序号\n\n»»» tick_time\n\nstring\n\nfalse\n\n时间戳\n\n»»» price\n\nstring\n\nfalse\n\n成交价\n\n»»» volume\n\nstring\n\nfalse\n\n成交量\n\n»»» turnover\n\nstring\n\nfalse\n\n成交额：\n1、外汇、贵金属、能源不返回成交额，可自行根据每次推送的数据计算，计算公式：turnover = price * volume\n2、股票、加密货币正常返回成交额。\n\n»»» trade_direction\n\ninteger\n\nfalse\n\n交易方向：\n1、0为默认值，1为Buy，2为SELL\n2、外汇、贵金属、能源默认只会返回0\n3、股票、加密货币根据市场情况会返回0、1、2\n4、详细说明：\n0:表示中性盘，即以买一价与卖一价之间的价格撮合成交。\n1:表示主动买入，即以卖一价或者更高价格成交的股票\n2:表示主动卖出，即以买一价或者更低价格成交的股票\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nGET 最新盘口(最新深度、Order Book)查询\n下一页\nGET 股票产品基础信息批量查询\n\n最后更新于5个月前"
  suggestedFilename: "rest-api_stock-http-interface-api_get-latest-transaction-price-query"
---

# GET 最新成交价(最新tick、当前价、最新价)批量查询

## 源URL

https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-transaction-price-query

## 文档正文

1. REST APIchevron-right
1. HTTP接口API

English / 中文

## GET /trade-tick

## 接口说明

该接口支持批量请求产品的最新成交价(最新逐笔Tick数据、也是当前价、最新价)，不支持请求历史成交价(历史逐笔tick数据)。

## 请求频率

免费

1、每10秒，只能1次请求 2、每次最大可批量查询5个产品

1、10秒只能请求1个接口

2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用

基础

1、每1秒，只能1次请求 2、由于GET请求url长度限制，每次最大建议请求50个code

1、同1秒只能请求1个接口

2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用

高级

1、每1秒，最大可10次请求 2、由于GET请求url长度限制，每次最大建议请求50个code

1、所以接口相加，每1秒可请求10次

2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用

专业

1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部港股

1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部A股

1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部美股

1、每1秒，最大可20次请求 2、由于GET请求url长度限制，每次最大建议请求50个code

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

## 接口限制

1、请务必阅读：HTTP接口限制说明

2、请务必阅读：错误码说明

## 接口地址

1、美股、港股、A股、大盘数据接口地址：

- 基本路径: /quote-stock-b-api/trade-tick
- 完整URL: https://quote.alltick.co/quote-stock-b-api/trade-tick

2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：

- 基本路径: /quote-b-api/trade-tick
- 完整URL: https://quote.alltick.co/quote-b-api/trade-tick

## 请求示例

1、美股、港股、A股、大盘数据接口地址：

在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-stock-b-api/trade-tick?token=您的token&query=queryData

2、外汇、贵金属、加密货币、原油、CFD指数、商品接口地址：

在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下： https://quote.alltick.co/quote-b-api/trade-tick?token=您的token&query=queryData

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

代码：[点击code列表]

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
        "seq": "30841439",
        "tick_time": "1677831545217",
        "price": "136.302",
        "volume": "0",
        "turnover": "0",
        "trade_direction": 0
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
        "seq": "30841439",
        "tick_time": "1677831545217",
        "price": "136.302",
        "volume": "0",
        "turnover": "0",
        "trade_direction": 0
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
        "seq": "30841439",
        "tick_time": "1677831545217",
        "price": "136.302",
        "volume": "0",
        "turnover": "0",
        "trade_direction": 0
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

序号

»»» tick_time

string

false

时间戳

»»» price

string

false

成交价

»»» volume

string

false

成交量

»»» turnover

string

false

成交额： 1、外汇、贵金属、能源不返回成交额，可自行根据每次推送的数据计算，计算公式：turnover = price * volume 2、股票、加密货币正常返回成交额。

»»» trade_direction

integer

false

交易方向： 1、0为默认值，1为Buy，2为SELL 2、外汇、贵金属、能源默认只会返回0 3、股票、加密货币根据市场情况会返回0、1、2 4、详细说明： 0:表示中性盘，即以买一价与卖一价之间的价格撮合成交。 1:表示主动买入，即以卖一价或者更高价格成交的股票 2:表示主动卖出，即以买一价或者更低价格成交的股票

#### AllTick网站

官方网站：https://alltick.co/

最后更新于5个月前
