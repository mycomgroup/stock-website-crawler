---
id: "url-7336c14e"
type: "api"
title: "HTTP 接口限制"
url: "https://apis.alltick.co/integration-process/interface-restriction-description/http-interface-restrictions"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:58:57.945Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["接入流程chevron-right","接口限制说明"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"HTTP接口限制","content":[]}
    - {"type":"heading","level":3,"title":"1. 频率类限制","content":[{"type":"text","value":"免费"},{"type":"text","value":"/kline接口：每10秒，只能1次请求 /batch-kline接口：每10秒，可1次请求 /depth-tick接口：每10秒，只能请求1次 /trade-tick接口：每10秒，只能请求1次 /static_info接口：每10秒，只能1次请求 /api/suspension/sse 接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求"},{"type":"text","value":"1、10秒只能请求1个接口"},{"type":"text","value":"2、需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"基础"},{"type":"text","value":"/kline接口：每1秒，只能1次请求 /batch-kline接口：每3秒，只能1次请求 /depth-tick接口：每1秒，只能1次请求 /trade-tick接口：每1秒，只能1次请求 /static_info接口：每1秒，只能1次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求"},{"type":"text","value":"1、同1秒只能请求1个接口"},{"type":"text","value":"2、需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"高级"},{"type":"text","value":"/kline接口：每1秒，最大可10次请求 /batch-kline接口：每2秒，只能1次请求 /depth-tick接口：每1秒，最大10次请求 /trade-tick接口：每1秒，最大10次请求 /static_info接口：每1秒，最大可10次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求"},{"type":"text","value":"1、所有接口相加，每1秒可请求10次"},{"type":"text","value":"2、需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"专业"},{"type":"text","value":"/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求"},{"type":"text","value":"1、所有接口相加，每1秒可请求20次"},{"type":"text","value":"2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部港股"},{"type":"text","value":"/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求"},{"type":"text","value":"1、所有接口相加，每1秒可请求20次"},{"type":"text","value":"2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部A股"},{"type":"text","value":"/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求"},{"type":"text","value":"1、所有接口相加，每1秒可请求20次"},{"type":"text","value":"2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部美股"},{"type":"text","value":"/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求"},{"type":"text","value":"1、所有接口相加，每1秒可请求20次"},{"type":"text","value":"2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"}]}
    - {"type":"heading","level":3,"title":"2. IP类限制","content":[{"type":"list","ordered":false,"items":["HTTP接口只会根据Token限制请求频率，对IP没有限制","示例：基础计划规定1秒只能请求1次，如果Token在14:03:01请求了/kline接口1次，并在相同的一分钟内调用了/trade-tick接口1次，后台服务都将正常提供服务。如果Token在14:03:01内对/kline接口发出2次请求，第一次请求将正常得到服务，而第二次请求则会收到错误响应。"]}]}
    - {"type":"heading","level":3,"title":"3. K线查询限制","content":[{"type":"list","ordered":false,"items":["/kline接口：每次查询请求只能针对一个产品代码（code）查询K线数据，每次查询最多返回500根K线数据。如果请求查询超过500根的K线，系统将按500根数据进行查询并返回结果。","/batch-kline接口：每次查询请求可针对多个产品代码（code）查询K线数据，但购买的计划不同，可批量请求的代码（code）数量也不同，每次查询最多返回2根K线数据。如果请求查询超过2根的K线，系统将按2根数据进行查询并返回结果，详见下面表格。"]},{"type":"text","value":"免费"},{"type":"text","value":"每1次请求，最大可请求 5组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"基础"},{"type":"text","value":"每1次请求，最大可请求 100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"高级"},{"type":"text","value":"每1次请求，最大可请求 200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"专业"},{"type":"text","value":"每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"全部港股"},{"type":"text","value":"每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"全部A股"},{"type":"text","value":"每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"},{"type":"text","value":"全部美股"},{"type":"text","value":"每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据"}]}
    - {"type":"heading","level":3,"title":"4. 最新成交价查询限制","content":[{"type":"list","ordered":false,"items":["/trade-tick接口：每次查询请求可针对多个产品代码（code）查询最新成交价格，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格","如果查询请求超过购买的计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。"]},{"type":"text","value":"免费"},{"type":"text","value":"每1次请求，最大可请求 5个code"},{"type":"text","value":"基础"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"高级"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"专业"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"全部港股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"全部A股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"全部美股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"}]}
    - {"type":"heading","level":3,"title":"5. 盘口深度(Order Book)查询限制","content":[{"type":"list","ordered":false,"items":["/depth-tick接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格","如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。"]},{"type":"text","value":"免费"},{"type":"text","value":"每1次请求，最大可请求 5个code"},{"type":"text","value":"基础"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"高级"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"专业"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"全部港股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"全部A股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"},{"type":"text","value":"全部美股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口"}]}
    - {"type":"heading","level":3,"title":"6. 基础信息查询限制","content":[{"type":"list","ordered":false,"items":["/static_info接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格","如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。"]},{"type":"text","value":"免费"},{"type":"text","value":"每1次请求，最大可请求 5个code"},{"type":"text","value":"基础"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"高级"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"专业"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"全部港股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"全部A股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code"},{"type":"text","value":"全部美股"},{"type":"text","value":"由于GET请求url长度限制，每次最大建议请求50个code"}]}
    - {"type":"heading","level":4,"title":"注意事项","content":[{"type":"list","ordered":false,"items":["请根据上述限制合理规划您的请求策略，以避免不必要的服务中断。","上述限制是为了保证所有用户能够公平地享受服务，同时保护后台系统免受过度负载的影响。","如有疑问或需要进一步的帮助，请联系客服支持。"]}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于2个月前"}]}
  codeExamples: []
  tables: []
  parameters: []
  markdownContent: "# HTTP 接口限制\n\n1. 接入流程chevron-right\n1. 接口限制说明\n\nEnglish / 中文\n\n\n## HTTP接口限制\n\n\n### 1. 频率类限制\n\n免费\n\n/kline接口：每10秒，只能1次请求 /batch-kline接口：每10秒，可1次请求 /depth-tick接口：每10秒，只能请求1次 /trade-tick接口：每10秒，只能请求1次 /static_info接口：每10秒，只能1次请求 /api/suspension/sse 接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、10秒只能请求1个接口\n\n2、需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n/kline接口：每1秒，只能1次请求 /batch-kline接口：每3秒，只能1次请求 /depth-tick接口：每1秒，只能1次请求 /trade-tick接口：每1秒，只能1次请求 /static_info接口：每1秒，只能1次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n/kline接口：每1秒，最大可10次请求 /batch-kline接口：每2秒，只能1次请求 /depth-tick接口：每1秒，最大10次请求 /trade-tick接口：每1秒，最大10次请求 /static_info接口：每1秒，最大可10次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求10次\n\n2、需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n\n### 2. IP类限制\n\n- HTTP接口只会根据Token限制请求频率，对IP没有限制\n- 示例：基础计划规定1秒只能请求1次，如果Token在14:03:01请求了/kline接口1次，并在相同的一分钟内调用了/trade-tick接口1次，后台服务都将正常提供服务。如果Token在14:03:01内对/kline接口发出2次请求，第一次请求将正常得到服务，而第二次请求则会收到错误响应。\n\n\n### 3. K线查询限制\n\n- /kline接口：每次查询请求只能针对一个产品代码（code）查询K线数据，每次查询最多返回500根K线数据。如果请求查询超过500根的K线，系统将按500根数据进行查询并返回结果。\n- /batch-kline接口：每次查询请求可针对多个产品代码（code）查询K线数据，但购买的计划不同，可批量请求的代码（code）数量也不同，每次查询最多返回2根K线数据。如果请求查询超过2根的K线，系统将按2根数据进行查询并返回结果，详见下面表格。\n\n免费\n\n每1次请求，最大可请求 5组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n基础\n\n每1次请求，最大可请求 100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n高级\n\n每1次请求，最大可请求 200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n专业\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n全部港股\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n全部A股\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n全部美股\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n\n### 4. 最新成交价查询限制\n\n- /trade-tick接口：每次查询请求可针对多个产品代码（code）查询最新成交价格，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格\n- 如果查询请求超过购买的计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。\n\n免费\n\n每1次请求，最大可请求 5个code\n\n基础\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n高级\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n专业\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部港股\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部A股\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部美股\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n\n### 5. 盘口深度(Order Book)查询限制\n\n- /depth-tick接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格\n- 如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。\n\n免费\n\n每1次请求，最大可请求 5个code\n\n基础\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n高级\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n专业\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部港股\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部A股\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部美股\n\n由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口\n\n\n### 6. 基础信息查询限制\n\n- /static_info接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格\n- 如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。\n\n免费\n\n每1次请求，最大可请求 5个code\n\n基础\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n高级\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n专业\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n全部港股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n全部A股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n全部美股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n\n#### 注意事项\n\n- 请根据上述限制合理规划您的请求策略，以避免不必要的服务中断。\n- 上述限制是为了保证所有用户能够公平地享受服务，同时保护后台系统免受过度负载的影响。\n- 如有疑问或需要进一步的帮助，请联系客服支持。\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于2个月前\n"
  rawContent: "复制\n接入流程\n接口限制说明\nHTTP 接口限制\n\nEnglish / 中文\n\nHTTP接口限制\n1. 频率类限制\n计划\n单独请求\n同时请求多个http接口\n\n免费\n\n/kline接口：每10秒，只能1次请求\n/batch-kline接口：每10秒，可1次请求\n/depth-tick接口：每10秒，只能请求1次\n/trade-tick接口：每10秒，只能请求1次\n/static_info接口：每10秒，只能1次请求\n\n/api/suspension/sse 接口：每1分钟只能1次请求\n/api/suspension/nyse接口：每1分钟只能1次请求\n/api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、10秒只能请求1个接口\n\n2、需注意/batch-kline接口需间隔10秒\n3、所有接口相加，1分钟最大请求10次(6秒1次) \n4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n/kline接口：每1秒，只能1次请求\n/batch-kline接口：每3秒，只能1次请求\n/depth-tick接口：每1秒，只能1次请求\n/trade-tick接口：每1秒，只能1次请求\n/static_info接口：每1秒，只能1次请求\n\n/api/suspension/sse接口：每1分钟只能1次请求\n/api/suspension/nyse接口：每1分钟只能1次请求\n/api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、需注意/batch-kline接口需间隔3秒\n3、所有接口相加，1分钟最大请求60次(1秒1次)\n4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n/kline接口：每1秒，最大可10次请求\n/batch-kline接口：每2秒，只能1次请求\n/depth-tick接口：每1秒，最大10次请求\n/trade-tick接口：每1秒，最大10次请求\n/static_info接口：每1秒，最大可10次请求\n\n/api/suspension/sse接口：每1分钟只能1次请求\n/api/suspension/nyse接口：每1分钟只能1次请求\n/api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求10次\n\n2、需注意/batch-kline接口需间隔2秒\n3、所有接口相加，1分钟最大请求600次(1秒10次)\n4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n/kline接口：每1秒，最大可20次请求\n/batch-kline接口：每1秒，只能1次请求\n/depth-tick接口：每1秒，最大20次请求\n/trade-tick接口：每1秒，最大20次请求\n/static_info接口：每1秒，最大可20次请求\n\n/api/suspension/sse接口：每1分钟只能1次请求\n/api/suspension/nyse接口：每1分钟只能1次请求\n/api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n/kline接口：每1秒，最大可20次请求\n/batch-kline接口：每1秒，只能1次请求\n/depth-tick接口：每1秒，最大20次请求\n/trade-tick接口：每1秒，最大20次请求\n/static_info接口：每1秒，最大可20次请求\n\n/api/suspension/sse接口：每1分钟只能1次请求\n/api/suspension/nyse接口：每1分钟只能1次请求\n/api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n/kline接口：每1秒，最大可20次请求\n/batch-kline接口：每1秒，只能1次请求\n/depth-tick接口：每1秒，最大20次请求\n/trade-tick接口：每1秒，最大20次请求\n/static_info接口：每1秒，最大可20次请求\n\n/api/suspension/sse接口：每1分钟只能1次请求\n/api/suspension/nyse接口：每1分钟只能1次请求\n/api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n/kline接口：每1秒，最大可20次请求\n/batch-kline接口：每1秒，只能1次请求\n/depth-tick接口：每1秒，最大20次请求\n/trade-tick接口：每1秒，最大20次请求\n/static_info接口：每1秒，最大可20次请求\n\n/api/suspension/sse接口：每1分钟只能1次请求\n/api/suspension/nyse接口：每1分钟只能1次请求\n/api/suspension/nasdaq接口：每1分钟只能1次请求\n\n1、所有接口相加，每1秒可请求20次\n\n2、需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n2. IP类限制\n\nHTTP接口只会根据Token限制请求频率，对IP没有限制\n\n示例：基础计划规定1秒只能请求1次，如果Token在14:03:01请求了/kline接口1次，并在相同的一分钟内调用了/trade-tick接口1次，后台服务都将正常提供服务。如果Token在14:03:01内对/kline接口发出2次请求，第一次请求将正常得到服务，而第二次请求则会收到错误响应。\n\n3. K线查询限制\n\n/kline接口：每次查询请求只能针对一个产品代码（code）查询K线数据，每次查询最多返回500根K线数据。如果请求查询超过500根的K线，系统将按500根数据进行查询并返回结果。\n\n/batch-kline接口：每次查询请求可针对多个产品代码（code）查询K线数据，但购买的计划不同，可批量请求的代码（code）数量也不同，每次查询最多返回2根K线数据。如果请求查询超过2根的K线，系统将按2根数据进行查询并返回结果，详见下面表格。\n\n计划\n/batch-kline接口，最大可请求代码（code）数量\n\n免费\n\n每1次请求，最大可请求 5组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n基础\n\n每1次请求，最大可请求 100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n高级\n\n每1次请求，最大可请求 200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n专业\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n全部港股\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n全部A股\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n全部美股\n\n每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据\n\n4. 最新成交价查询限制\n\n/trade-tick接口：每次查询请求可针对多个产品代码（code）查询最新成交价格，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格\n\n如果查询请求超过购买的计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。\n\n计划\n最大可请求代码（code）数量\n\n免费\n\n每1次请求，最大可请求 5个code\n\n基础\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n高级\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n专业\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部港股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部A股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部美股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n5. 盘口深度(Order Book)查询限制\n\n/depth-tick接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格\n\n如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。\n\n计划\n最大可请求代码（code）数量\n\n免费\n\n每1次请求，最大可请求 5个code\n\n基础\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n高级\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n专业\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部港股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部A股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n全部美股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n推荐使用websocket接口，支持批量订阅更多code：接口\n\n6. 基础信息查询限制\n\n/static_info接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格\n\n如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。\n\n计划\n最大可请求代码（code）数量\n\n免费\n\n每1次请求，最大可请求 5个code\n\n基础\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n高级\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n专业\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n全部港股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n全部A股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n全部美股\n\n由于GET请求url长度限制，每次最大建议请求50个code\n\n注意事项\n\n请根据上述限制合理规划您的请求策略，以避免不必要的服务中断。\n\n上述限制是为了保证所有用户能够公平地享受服务，同时保护后台系统免受过度负载的影响。\n\n如有疑问或需要进一步的帮助，请联系客服支持。\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n接口限制说明\n下一页\nWebsocket 接口限制\n\n最后更新于2个月前"
  suggestedFilename: "integration-process_interface-restriction-description_http-interface-restrictions"
---

# HTTP 接口限制

## 源URL

https://apis.alltick.co/integration-process/interface-restriction-description/http-interface-restrictions

## 文档正文

1. 接入流程chevron-right
1. 接口限制说明

English / 中文

## HTTP接口限制

### 1. 频率类限制

免费

/kline接口：每10秒，只能1次请求 /batch-kline接口：每10秒，可1次请求 /depth-tick接口：每10秒，只能请求1次 /trade-tick接口：每10秒，只能请求1次 /static_info接口：每10秒，只能1次请求 /api/suspension/sse 接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求

1、10秒只能请求1个接口

2、需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用

基础

/kline接口：每1秒，只能1次请求 /batch-kline接口：每3秒，只能1次请求 /depth-tick接口：每1秒，只能1次请求 /trade-tick接口：每1秒，只能1次请求 /static_info接口：每1秒，只能1次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求

1、同1秒只能请求1个接口

2、需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用

高级

/kline接口：每1秒，最大可10次请求 /batch-kline接口：每2秒，只能1次请求 /depth-tick接口：每1秒，最大10次请求 /trade-tick接口：每1秒，最大10次请求 /static_info接口：每1秒，最大可10次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求

1、所有接口相加，每1秒可请求10次

2、需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用

专业

/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求

1、所有接口相加，每1秒可请求20次

2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部港股

/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求

1、所有接口相加，每1秒可请求20次

2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部A股

/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求

1、所有接口相加，每1秒可请求20次

2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部美股

/kline接口：每1秒，最大可20次请求 /batch-kline接口：每1秒，只能1次请求 /depth-tick接口：每1秒，最大20次请求 /trade-tick接口：每1秒，最大20次请求 /static_info接口：每1秒，最大可20次请求 /api/suspension/sse接口：每1分钟只能1次请求 /api/suspension/nyse接口：每1分钟只能1次请求 /api/suspension/nasdaq接口：每1分钟只能1次请求

1、所有接口相加，每1秒可请求20次

2、需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

### 2. IP类限制

- HTTP接口只会根据Token限制请求频率，对IP没有限制
- 示例：基础计划规定1秒只能请求1次，如果Token在14:03:01请求了/kline接口1次，并在相同的一分钟内调用了/trade-tick接口1次，后台服务都将正常提供服务。如果Token在14:03:01内对/kline接口发出2次请求，第一次请求将正常得到服务，而第二次请求则会收到错误响应。

### 3. K线查询限制

- /kline接口：每次查询请求只能针对一个产品代码（code）查询K线数据，每次查询最多返回500根K线数据。如果请求查询超过500根的K线，系统将按500根数据进行查询并返回结果。
- /batch-kline接口：每次查询请求可针对多个产品代码（code）查询K线数据，但购买的计划不同，可批量请求的代码（code）数量也不同，每次查询最多返回2根K线数据。如果请求查询超过2根的K线，系统将按2根数据进行查询并返回结果，详见下面表格。

免费

每1次请求，最大可请求 5组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

基础

每1次请求，最大可请求 100组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

高级

每1次请求，最大可请求 200组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

专业

每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

全部港股

每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

全部A股

每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

全部美股

每1次请求，最大可请求 500组数据，每1组数据=1只产品数量+1种K线类型，例如同时获取BTCUSDT的1分钟k线和5分钟k线，这就是2组数据

### 4. 最新成交价查询限制

- /trade-tick接口：每次查询请求可针对多个产品代码（code）查询最新成交价格，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格
- 如果查询请求超过购买的计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。

免费

每1次请求，最大可请求 5个code

基础

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

高级

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

专业

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

全部港股

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

全部A股

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

全部美股

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

### 5. 盘口深度(Order Book)查询限制

- /depth-tick接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格
- 如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。

免费

每1次请求，最大可请求 5个code

基础

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

高级

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

专业

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

全部港股

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

全部A股

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

全部美股

由于GET请求url长度限制，每次最大建议请求50个code 推荐使用websocket接口，支持批量订阅更多code：接口

### 6. 基础信息查询限制

- /static_info接口：每次查询请求可针对多个产品代码（code）查询盘口，但购买的计划不同，可批量请求的代码（code）数量也不同，详见下面表格
- 如果查询请求超过计划所规定的代码（code）数量，系统将仅针在规定数量内的最前面的代码进行查询并返回结果。

免费

每1次请求，最大可请求 5个code

基础

由于GET请求url长度限制，每次最大建议请求50个code

高级

由于GET请求url长度限制，每次最大建议请求50个code

专业

由于GET请求url长度限制，每次最大建议请求50个code

全部港股

由于GET请求url长度限制，每次最大建议请求50个code

全部A股

由于GET请求url长度限制，每次最大建议请求50个code

全部美股

由于GET请求url长度限制，每次最大建议请求50个code

#### 注意事项

- 请根据上述限制合理规划您的请求策略，以避免不必要的服务中断。
- 上述限制是为了保证所有用户能够公平地享受服务，同时保护后台系统免受过度负载的影响。
- 如有疑问或需要进一步的帮助，请联系客服支持。

#### AllTick网站

官方网站：https://alltick.co/

最后更新于2个月前
