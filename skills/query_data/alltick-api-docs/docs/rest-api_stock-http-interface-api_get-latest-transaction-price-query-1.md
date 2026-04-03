---
id: "url-78973000"
type: "api"
title: "GET 股票产品基础信息批量查询"
url: "https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-transaction-price-query-1"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:57:22.057Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["REST APIchevron-right","HTTP接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"GET /static_info","content":[]}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"该接口仅支持批量请求美股、港股、A股产品的部分基础信息。"}]}
    - {"type":"heading","level":2,"title":"请求频率","content":[{"type":"text","value":"免费"},{"type":"text","value":"每10秒，只能1次请求"},{"type":"text","value":"1、10秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"基础"},{"type":"text","value":"每1秒，只能1次请求"},{"type":"text","value":"1、同1秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"高级"},{"type":"text","value":"每1秒，最大可10次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求10次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"专业"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部港股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部A股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部美股"},{"type":"text","value":"每1秒，最大可20次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"}]}
    - {"type":"heading","level":2,"title":"接口限制","content":[{"type":"text","value":"1、请务必阅读：HTTP接口限制说明"},{"type":"text","value":"2、请务必阅读：错误码说明"}]}
    - {"type":"heading","level":2,"title":"接口地址","content":[{"type":"list","ordered":false,"items":["基本路径: /quote-stock-b-api/static_info","完整URL: https://quote.alltick.co/quote-stock-b-api/static_info"]},{"type":"code","language":"text","value":"/quote-stock-b-api/static_info"},{"type":"code","language":"http","value":"https://quote.alltick.co/quote-stock-b-api/static_info"}]}
    - {"type":"heading","level":2,"title":"请求示例","content":[{"type":"text","value":"在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下："},{"type":"code","language":"http","value":"复制https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData"},{"type":"code","language":"http","value":"https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData"},{"type":"code","language":"http","value":"https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData"}]}
    - {"type":"heading","level":2,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"query"},{"type":"text","value":"query"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"查看query请求参数说明"},{"type":"text","value":"将如下json进行UrlEncode编码，赋值到url的查询字符串的query里"},{"type":"code","language":"text","value":"复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}]}
    - {"type":"heading","level":2,"title":"query请求参数","content":[{"type":"text","value":"trace"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"data"},{"type":"text","value":"object"},{"type":"text","value":"是"},{"type":"text","value":"» symbol_list"},{"type":"text","value":"[object]"},{"type":"text","value":"是"},{"type":"text","value":"»» code"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"代码：[点击code列表]"}]}
    - {"type":"heading","level":2,"title":"返回示例","content":[{"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}"},{"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}"}]}
    - {"type":"heading","level":2,"title":"返回结果","content":[{"type":"text","value":"200"},{"type":"text","value":"OK"},{"type":"text","value":"OK"},{"type":"text","value":"Inline"}]}
    - {"type":"heading","level":2,"title":"返回数据结构","content":[{"type":"text","value":"» ret"},{"type":"text","value":"integer"},{"type":"text","value":"true"},{"type":"text","value":"返回code"},{"type":"text","value":"» msg"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"返回code对应消息"},{"type":"text","value":"» trace"},{"type":"text","value":"string"},{"type":"text","value":"true"},{"type":"text","value":"请求的trace"},{"type":"text","value":"» data"},{"type":"text","value":"object"},{"type":"text","value":"true"},{"type":"text","value":"»» static_info_list"},{"type":"text","value":"[object]"},{"type":"text","value":"true"},{"type":"text","value":"»»» board"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"股票所属板块"},{"type":"text","value":"»»» bps"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"每股净资产"},{"type":"text","value":"»»» circulating_shares"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"流通股本"},{"type":"text","value":"»»» currency"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"交易币种"},{"type":"text","value":"»»» dividend_yield"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"股息"},{"type":"text","value":"»»» eps"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"每股盈利"},{"type":"text","value":"»»» eps_ttm"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"每股盈利 (TTM)"},{"type":"text","value":"»»» exchange"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"产品所属交易所"},{"type":"text","value":"»»» hk_shares"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"港股股本 (仅港股)"},{"type":"text","value":"»»» lot_size"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"每手股数"},{"type":"text","value":"»»» name_cn"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"中文简体产品的名称"},{"type":"text","value":"»»» name_en"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"英文产品的名称"},{"type":"text","value":"»»» name_hk"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"中文繁体产品的名称"},{"type":"text","value":"»»» symbol"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"产品code"},{"type":"text","value":"»»» total_shares"},{"type":"text","value":"string"},{"type":"text","value":"false"},{"type":"text","value":"总股本"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于2个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"/quote-stock-b-api/static_info"}
    - {"type":"code","language":"http","value":"https://quote.alltick.co/quote-stock-b-api/static_info"}
    - {"type":"code","language":"http","value":"复制https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData"}
    - {"type":"code","language":"http","value":"https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData"}
    - {"type":"code","language":"http","value":"https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData"}
    - {"type":"code","language":"text","value":"复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"text","value":"复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}"}
    - {"type":"code","language":"json","value":"{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}"}
  tables: []
  parameters: []
  markdownContent: "# GET 股票产品基础信息批量查询\n\n1. REST APIchevron-right\n1. HTTP接口API\n\nEnglish / 中文\n\n\n## GET /static_info\n\n\n## 接口说明\n\n该接口仅支持批量请求美股、港股、A股产品的部分基础信息。\n\n\n## 请求频率\n\n免费\n\n每10秒，只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1秒，只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1秒，最大可10次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n\n## 接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n\n## 接口地址\n\n- 基本路径: /quote-stock-b-api/static_info\n- 完整URL: https://quote.alltick.co/quote-stock-b-api/static_info\n\n```text\n/quote-stock-b-api/static_info\n```\n\n```http\nhttps://quote.alltick.co/quote-stock-b-api/static_info\n```\n\n\n## 请求示例\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\n\n```http\n复制https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData\n```\n\n```http\nhttps://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData\n```\n\n```http\nhttps://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData\n```\n\n\n## 请求参数\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\n将如下json进行UrlEncode编码，赋值到url的查询字符串的query里\n\n```text\n复制{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"symbol_list\": [\n      {\n        \"code\": \"857.HK\"\n      },\n      {\n        \"code\": \"UNH.US\"\n      }\n    ]\n  }\n}\n```\n\n\n## query请求参数\n\ntrace\n\nstring\n\n是\n\ndata\n\nobject\n\n是\n\n» symbol_list\n\n[object]\n\n是\n\n»» code\n\nstring\n\n否\n\n代码：[点击code列表]\n\n\n## 返回示例\n\n```text\n复制{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}\n```\n\n```json\n{\n  \"ret\": 200,\n  \"msg\": \"ok\",\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n  \"data\": {\n    \"static_info_list\": [\n      {\n        \"board\": \"HKEquity\",\n        \"bps\": \"101.7577888985738336\",\n        \"circulating_shares\": \"9267359712\",\n        \"currency\": \"HKD\",\n        \"dividend_yield\": \"3.4558141358352833\",\n        \"eps\": \"13.7190213011686429\",\n        \"eps_ttm\": \"18.0567016900844671\",\n        \"exchange\": \"SEHK\",\n        \"hk_shares\": \"9267359712\",\n        \"lot_size\": \"100\",\n        \"name_cn\": \"腾讯控股\",\n        \"name_en\": \"TENCENT\",\n        \"name_hk\": \"騰訊控股\",\n        \"symbol\": \"700.HK\",\n        \"total_shares\": \"9267359712\"\n      }\n    ]\n  }\n}\n```\n\n\n## 返回结果\n\n200\n\nOK\n\nOK\n\nInline\n\n\n## 返回数据结构\n\n» ret\n\ninteger\n\ntrue\n\n返回code\n\n» msg\n\nstring\n\ntrue\n\n返回code对应消息\n\n» trace\n\nstring\n\ntrue\n\n请求的trace\n\n» data\n\nobject\n\ntrue\n\n»» static_info_list\n\n[object]\n\ntrue\n\n»»» board\n\nstring\n\nfalse\n\n股票所属板块\n\n»»» bps\n\nstring\n\nfalse\n\n每股净资产\n\n»»» circulating_shares\n\nstring\n\nfalse\n\n流通股本\n\n»»» currency\n\nstring\n\nfalse\n\n交易币种\n\n»»» dividend_yield\n\nstring\n\nfalse\n\n股息\n\n»»» eps\n\nstring\n\nfalse\n\n每股盈利\n\n»»» eps_ttm\n\nstring\n\nfalse\n\n每股盈利 (TTM)\n\n»»» exchange\n\nstring\n\nfalse\n\n产品所属交易所\n\n»»» hk_shares\n\nstring\n\nfalse\n\n港股股本 (仅港股)\n\n»»» lot_size\n\nstring\n\nfalse\n\n每手股数\n\n»»» name_cn\n\nstring\n\nfalse\n\n中文简体产品的名称\n\n»»» name_en\n\nstring\n\nfalse\n\n英文产品的名称\n\n»»» name_hk\n\nstring\n\nfalse\n\n中文繁体产品的名称\n\n»»» symbol\n\nstring\n\nfalse\n\n产品code\n\n»»» total_shares\n\nstring\n\nfalse\n\n总股本\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于2个月前\n"
  rawContent: "复制\nREST API\nHTTP接口API\nGET 股票产品基础信息批量查询\n\nEnglish / 中文\n\nGET /static_info\n接口说明\n\n该接口仅支持批量请求美股、港股、A股产品的部分基础信息。\n\n请求频率\n计划\n单独请求\n同时请求多个http接口\n\n免费\n\n每10秒，只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒\n3、所有接口相加，1分钟最大请求10次(6秒1次)\n4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1秒，只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒\n3、所有接口相加，1分钟最大请求60次(1秒1次)\n4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1秒，最大可10次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒\n3、所有接口相加，1分钟最大请求600次(1秒10次)\n4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1秒，最大可20次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n接口地址\n\n基本路径: /quote-stock-b-api/static_info\n\n完整URL: https://quote.alltick.co/quote-stock-b-api/static_info\n\n请求示例\n\n在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：\n\n复制\nhttps://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData\n请求参数\n名称\n位置\n类型\n必选\n说明\n\ntoken\n\nquery\n\nstring\n\n否\n\nquery\n\nquery\n\nstring\n\n否\n\n查看query请求参数说明\n\n将如下json进行UrlEncode编码，赋值到url的查询字符串的query里\n\n复制\n{\n\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n\n  \"data\": {\n\n    \"symbol_list\": [\n\n      {\n\n        \"code\": \"857.HK\"\n\n      },\n\n      {\n\n        \"code\": \"UNH.US\"\n\n      }\n\n    ]\n\n  }\n\n}\nquery请求参数\n名称\n类型\n必选\n说明\n\ntrace\n\nstring\n\n是\n\ndata\n\nobject\n\n是\n\n» symbol_list\n\n[object]\n\n是\n\n»» code\n\nstring\n\n否\n\n代码：[点击code列表]\n\n返回示例\n复制\n{\n\n  \"ret\": 200,\n\n  \"msg\": \"ok\",\n\n  \"trace\": \"edd5df80-df7f-4acf-8f67-68fd2f096426\",\n\n  \"data\": {\n\n    \"static_info_list\": [\n\n      {\n\n        \"board\": \"HKEquity\",\n\n        \"bps\": \"101.7577888985738336\",\n\n        \"circulating_shares\": \"9267359712\",\n\n        \"currency\": \"HKD\",\n\n        \"dividend_yield\": \"3.4558141358352833\",\n\n        \"eps\": \"13.7190213011686429\",\n\n        \"eps_ttm\": \"18.0567016900844671\",\n\n        \"exchange\": \"SEHK\",\n\n        \"hk_shares\": \"9267359712\",\n\n        \"lot_size\": \"100\",\n\n        \"name_cn\": \"腾讯控股\",\n\n        \"name_en\": \"TENCENT\",\n\n        \"name_hk\": \"騰訊控股\",\n\n        \"symbol\": \"700.HK\",\n\n        \"total_shares\": \"9267359712\"\n\n      }\n\n    ]\n\n  }\n\n}\n返回结果\n状态码\n状态码含义\n说明\n数据模型\n\n200\n\nOK\n\nOK\n\nInline\n\n返回数据结构\n名称\n类型\n必选\n说明\n\n» ret\n\ninteger\n\ntrue\n\n返回code\n\n» msg\n\nstring\n\ntrue\n\n返回code对应消息\n\n» trace\n\nstring\n\ntrue\n\n请求的trace\n\n» data\n\nobject\n\ntrue\n\n»» static_info_list\n\n[object]\n\ntrue\n\n»»» board\n\nstring\n\nfalse\n\n股票所属板块\n\n»»» bps\n\nstring\n\nfalse\n\n每股净资产\n\n»»» circulating_shares\n\nstring\n\nfalse\n\n流通股本\n\n»»» currency\n\nstring\n\nfalse\n\n交易币种\n\n»»» dividend_yield\n\nstring\n\nfalse\n\n股息\n\n»»» eps\n\nstring\n\nfalse\n\n每股盈利\n\n»»» eps_ttm\n\nstring\n\nfalse\n\n每股盈利 (TTM)\n\n»»» exchange\n\nstring\n\nfalse\n\n产品所属交易所\n\n»»» hk_shares\n\nstring\n\nfalse\n\n港股股本 (仅港股)\n\n»»» lot_size\n\nstring\n\nfalse\n\n每手股数\n\n»»» name_cn\n\nstring\n\nfalse\n\n中文简体产品的名称\n\n»»» name_en\n\nstring\n\nfalse\n\n英文产品的名称\n\n»»» name_hk\n\nstring\n\nfalse\n\n中文繁体产品的名称\n\n»»» symbol\n\nstring\n\nfalse\n\n产品code\n\n»»» total_shares\n\nstring\n\nfalse\n\n总股本\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nGET 最新成交价(最新tick、当前价、最新价)批量查询\n下一页\nGET 停复牌信息查询接口\n\n最后更新于2个月前"
  suggestedFilename: "rest-api_stock-http-interface-api_get-latest-transaction-price-query-1"
---

# GET 股票产品基础信息批量查询

## 源URL

https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-transaction-price-query-1

## 文档正文

1. REST APIchevron-right
1. HTTP接口API

English / 中文

## GET /static_info

## 接口说明

该接口仅支持批量请求美股、港股、A股产品的部分基础信息。

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

- 基本路径: /quote-stock-b-api/static_info
- 完整URL: https://quote.alltick.co/quote-stock-b-api/static_info

```text
/quote-stock-b-api/static_info
```

```http
https://quote.alltick.co/quote-stock-b-api/static_info
```

## 请求示例

在发送查询请求时，必须包含方法名和token信息。一个请求的示例如下：

```http
复制https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData
```

```http
https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData
```

```http
https://quote.alltick.co/quote-stock-b-api/static_info?token=您的token&query=queryData
```

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

## query请求参数

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
    "static_info_list": [
      {
        "board": "HKEquity",
        "bps": "101.7577888985738336",
        "circulating_shares": "9267359712",
        "currency": "HKD",
        "dividend_yield": "3.4558141358352833",
        "eps": "13.7190213011686429",
        "eps_ttm": "18.0567016900844671",
        "exchange": "SEHK",
        "hk_shares": "9267359712",
        "lot_size": "100",
        "name_cn": "腾讯控股",
        "name_en": "TENCENT",
        "name_hk": "騰訊控股",
        "symbol": "700.HK",
        "total_shares": "9267359712"
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
    "static_info_list": [
      {
        "board": "HKEquity",
        "bps": "101.7577888985738336",
        "circulating_shares": "9267359712",
        "currency": "HKD",
        "dividend_yield": "3.4558141358352833",
        "eps": "13.7190213011686429",
        "eps_ttm": "18.0567016900844671",
        "exchange": "SEHK",
        "hk_shares": "9267359712",
        "lot_size": "100",
        "name_cn": "腾讯控股",
        "name_en": "TENCENT",
        "name_hk": "騰訊控股",
        "symbol": "700.HK",
        "total_shares": "9267359712"
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
    "static_info_list": [
      {
        "board": "HKEquity",
        "bps": "101.7577888985738336",
        "circulating_shares": "9267359712",
        "currency": "HKD",
        "dividend_yield": "3.4558141358352833",
        "eps": "13.7190213011686429",
        "eps_ttm": "18.0567016900844671",
        "exchange": "SEHK",
        "hk_shares": "9267359712",
        "lot_size": "100",
        "name_cn": "腾讯控股",
        "name_en": "TENCENT",
        "name_hk": "騰訊控股",
        "symbol": "700.HK",
        "total_shares": "9267359712"
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

»» static_info_list

[object]

true

»»» board

string

false

股票所属板块

»»» bps

string

false

每股净资产

»»» circulating_shares

string

false

流通股本

»»» currency

string

false

交易币种

»»» dividend_yield

string

false

股息

»»» eps

string

false

每股盈利

»»» eps_ttm

string

false

每股盈利 (TTM)

»»» exchange

string

false

产品所属交易所

»»» hk_shares

string

false

港股股本 (仅港股)

»»» lot_size

string

false

每手股数

»»» name_cn

string

false

中文简体产品的名称

»»» name_en

string

false

英文产品的名称

»»» name_hk

string

false

中文繁体产品的名称

»»» symbol

string

false

产品code

»»» total_shares

string

false

总股本

#### AllTick网站

官方网站：https://alltick.co/

最后更新于2个月前
