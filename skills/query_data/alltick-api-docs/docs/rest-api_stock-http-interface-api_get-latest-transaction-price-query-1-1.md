---
id: "url-5074d5a4"
type: "api"
title: "GET 停复牌信息查询接口"
url: "https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-transaction-price-query-1-1"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:57:33.956Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["REST APIchevron-right","HTTP接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"GET /api/suspension","content":[]}
    - {"type":"heading","level":2,"title":"接口说明","content":[{"type":"text","value":"该接口提供全球主要交易所（SSE、NYSE、NASDAQ）的停复牌信息查询，所有接口均返回JSON格式数据，按公告时间倒序排列。"}]}
    - {"type":"heading","level":2,"title":"请求频率","content":[{"type":"text","value":"免费"},{"type":"text","value":"每1分钟只能1次请求"},{"type":"text","value":"1、10秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"基础"},{"type":"text","value":"每1分钟只能1次请求"},{"type":"text","value":"1、同1秒只能请求1个接口"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用"},{"type":"text","value":"高级"},{"type":"text","value":"每1分钟只能1次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求10次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"专业"},{"type":"text","value":"每1分钟只能1次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部港股"},{"type":"text","value":"每1分钟只能1次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部A股"},{"type":"text","value":"每1分钟只能1次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"},{"type":"text","value":"全部美股"},{"type":"text","value":"每1分钟只能1次请求"},{"type":"text","value":"1、所以接口相加，每1秒可请求20次"},{"type":"text","value":"2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用"}]}
    - {"type":"heading","level":2,"title":"接口限制","content":[{"type":"text","value":"1、请务必阅读：HTTP接口限制说明"},{"type":"text","value":"2、请务必阅读：错误码说明"}]}
    - {"type":"heading","level":2,"title":"接口地址","content":[{"type":"text","value":"1、查询上海证券交易所停复牌信息："},{"type":"list","ordered":false,"items":["基本路径: /api/suspension/sse","完整URL: https://quote.alltick.co/api/suspension/sse"]},{"type":"text","value":"2、查询纽约证券交易所停复牌信息："},{"type":"list","ordered":false,"items":["基本路径: /api/suspension/nyse","完整URL: https://quote.alltick.co/api/suspension/nyse"]},{"type":"text","value":"3、查询纳斯达克交易所停复牌信息："},{"type":"list","ordered":false,"items":["基本路径: /api/suspension/nasdaq","完整URL: https://quote.alltick.co/api/suspension/nasdaq"]}]}
    - {"type":"heading","level":2,"title":"请求示例","content":[]}
    - {"type":"heading","level":3,"title":"1. 获取上证所数据接口","content":[]}
    - {"type":"heading","level":4,"title":"接口信息","content":[{"type":"list","ordered":false,"items":["URL: /api/suspension/sse","方法: GET","描述: 获取上海证券交易所（SSE）全部停复牌信息"]},{"type":"code","language":"text","value":"/api/suspension/sse"}]}
    - {"type":"heading","level":4,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"用户套餐token"},{"type":"text","value":"page"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"查询页码"},{"type":"text","value":"size"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"每页数据大小"}]}
    - {"type":"heading","level":4,"title":"响应示例","content":[{"type":"code","language":"text","value":"复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}"},{"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}"},{"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}"}]}
    - {"type":"heading","level":4,"title":"响应字段说明","content":[]}
    - {"type":"heading","level":4,"title":"公共字段","content":[{"type":"text","value":"» success"},{"type":"text","value":"boolean"},{"type":"text","value":"是"},{"type":"text","value":"请求是否成功"},{"type":"text","value":"» timestamp"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）"},{"type":"text","value":"» totalCount"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"数据总条数"},{"type":"text","value":"» data"},{"type":"text","value":"array"},{"type":"text","value":"是"},{"type":"text","value":"停复牌信息列表"},{"type":"text","value":"» totalPages"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"数据总页数（分页查询时返回）"},{"type":"text","value":"» currentPage"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"当前页（分页查询时返回）"},{"type":"text","value":"» currentSize"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"当前页的数据条数（分页查询时返回）"}]}
    - {"type":"heading","level":4,"title":"data字段（停复牌信息列表中的对象）","content":[{"type":"text","value":"每个对象包含以下字段："},{"type":"text","value":"» symbol"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"股票代码"},{"type":"text","value":"» symbolName"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"股票名称"},{"type":"text","value":"» haltReason"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌原因"},{"type":"text","value":"» haltDate"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌日期"},{"type":"text","value":"» haltTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌时间"},{"type":"text","value":"» haltPeriod"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌期限"},{"type":"text","value":"» resumeDate"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"复牌日期"},{"type":"text","value":"» resumeTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"复牌时间"},{"type":"text","value":"» publishDate"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"公告时间"}]}
    - {"type":"heading","level":4,"title":"调用示例","content":[{"type":"code","language":"http","value":"复制curl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""},{"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""},{"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}]}
    - {"type":"heading","level":3,"title":"2. 获取纽交所数据接口","content":[]}
    - {"type":"heading","level":4,"title":"接口信息","content":[{"type":"list","ordered":false,"items":["URL: /api/suspension/nyse","方法: GET","描述: 获取纽约证券交易所（NYSE）全部停复牌信息"]},{"type":"code","language":"text","value":"/api/suspension/nyse"}]}
    - {"type":"heading","level":4,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"用户套餐token"},{"type":"text","value":"page"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"查询页码"},{"type":"text","value":"size"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"每页数据大小"}]}
    - {"type":"heading","level":4,"title":"响应示例","content":[{"type":"code","language":"text","value":"复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}"},{"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}"},{"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}"}]}
    - {"type":"heading","level":4,"title":"响应字段说明","content":[]}
    - {"type":"heading","level":4,"title":"公共字段","content":[{"type":"text","value":"» success"},{"type":"text","value":"boolean"},{"type":"text","value":"是"},{"type":"text","value":"请求是否成功"},{"type":"text","value":"» timestamp"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）"},{"type":"text","value":"» totalCount"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"数据总条数"},{"type":"text","value":"» data"},{"type":"text","value":"array"},{"type":"text","value":"是"},{"type":"text","value":"停复牌信息列表"},{"type":"text","value":"» totalPages"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"数据总页数（分页查询时返回）"},{"type":"text","value":"» currentPage"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"当前页（分页查询时返回）"},{"type":"text","value":"» currentSize"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"当前页的数据条数（分页查询时返回"}]}
    - {"type":"heading","level":4,"title":"data字段（停复牌信息列表中的对象）","content":[{"type":"text","value":"每个对象包含以下字段："},{"type":"text","value":"» symbol"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"股票代码"},{"type":"text","value":"» symbolName"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"股票名称"},{"type":"text","value":"» haltReason"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌原因"},{"type":"text","value":"» haltTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌时间"},{"type":"text","value":"» haltDateTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌日期时间"},{"type":"text","value":"» resumeDate"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"复牌日期"},{"type":"text","value":"» resumeTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"复牌时间"},{"type":"text","value":"» resumeDateTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"复牌日期时间"},{"type":"text","value":"» sourceExchange"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"交易所代码"},{"type":"text","value":"» publishDate"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"公告时间"}]}
    - {"type":"heading","level":4,"title":"调用示例","content":[{"type":"code","language":"http","value":"复制curl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""},{"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""},{"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}]}
    - {"type":"heading","level":3,"title":"3. 获取纳斯达克数据接口","content":[]}
    - {"type":"heading","level":4,"title":"接口信息","content":[{"type":"list","ordered":false,"items":["URL: /api/suspension/nasdaq","方法: GET","描述: 获取纳斯达克交易所（NASDAQ）全部停复牌信息"]},{"type":"code","language":"text","value":"/api/suspension/nasdaq"}]}
    - {"type":"heading","level":4,"title":"请求参数","content":[{"type":"text","value":"token"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"用户套餐token"},{"type":"text","value":"page"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"查询页码"},{"type":"text","value":"size"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"每页数据大小"}]}
    - {"type":"heading","level":4,"title":"响应示例","content":[{"type":"code","language":"text","value":"复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}"},{"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}"},{"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}"}]}
    - {"type":"heading","level":4,"title":"响应字段说明","content":[]}
    - {"type":"heading","level":4,"title":"公共字段","content":[{"type":"text","value":"» success"},{"type":"text","value":"boolean"},{"type":"text","value":"是"},{"type":"text","value":"请求是否成功"},{"type":"text","value":"» timestamp"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）"},{"type":"text","value":"» totalCount"},{"type":"text","value":"integer"},{"type":"text","value":"是"},{"type":"text","value":"数据总条数"},{"type":"text","value":"» data"},{"type":"text","value":"array"},{"type":"text","value":"是"},{"type":"text","value":"停复牌信息列表"},{"type":"text","value":"» totalPages"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"数据总页数（分页查询时返回）"},{"type":"text","value":"» currentPage"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"当前页（分页查询时返回）"},{"type":"text","value":"» currentSize"},{"type":"text","value":"integer"},{"type":"text","value":"否"},{"type":"text","value":"当前页的数据条数（分页查询时返回）"}]}
    - {"type":"heading","level":4,"title":"data字段（停复牌信息列表中的对象）","content":[{"type":"text","value":"每个对象包含以下字段："},{"type":"text","value":"» symbol"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"股票代码"},{"type":"text","value":"» symbolName"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"股票名称"},{"type":"text","value":"» haltDate"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌日期"},{"type":"text","value":"» haltTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌时间"},{"type":"text","value":"» haltDateTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌日期时间"},{"type":"text","value":"» sourceExchange"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"交易所代码"},{"type":"text","value":"» haltReason"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"停牌原因"},{"type":"text","value":"» pauseThresholdPrice"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"暂停阈值价格"},{"type":"text","value":"» resumeDate"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"恢复日期"},{"type":"text","value":"» resumeTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"恢复报价时间"},{"type":"text","value":"» resumeDateTime"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"恢复交易时间"},{"type":"text","value":"» publishDate"},{"type":"text","value":"string"},{"type":"text","value":"否"},{"type":"text","value":"公告时间"}]}
    - {"type":"heading","level":4,"title":"调用示例","content":[{"type":"code","language":"http","value":"复制curl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""},{"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""},{"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}]}
    - {"type":"heading","level":3,"title":"错误响应","content":[{"type":"text","value":"所有接口在发生错误时返回以下格式："},{"type":"code","language":"text","value":"复制{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}"},{"type":"code","language":"json","value":"{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}"},{"type":"code","language":"json","value":"{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}"},{"type":"text","value":"HTTP状态码: 500"}]}
    - {"type":"heading","level":4,"title":"错误响应字段说明","content":[{"type":"text","value":"success"},{"type":"text","value":"boolean"},{"type":"text","value":"是"},{"type":"text","value":"请求是否成功，固定为false"},{"type":"text","value":"error"},{"type":"text","value":"string"},{"type":"text","value":"是"},{"type":"text","value":"错误描述信息"}]}
    - {"type":"heading","level":3,"title":"注意事项","content":[{"type":"list","ordered":true,"items":["所有接口均不支持分页，返回最近一年的全量数据","数据已按公告时间倒序排列（最新的在前）","响应中的时间格式：timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）其他时间字段：yyyy-MM-dd HH:mm:ss","timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）","其他时间字段：yyyy-MM-dd HH:mm:ss","建议设置适当的超时时间，大数据量时可能需要较长时间","字段为空说明：\"否\"：字段始终有值，不会为null\"是\"：字段可能为null或空字符串，调用方需进行空值判断","\"否\"：字段始终有值，不会为null","\"是\"：字段可能为null或空字符串，调用方需进行空值判断"]},{"type":"list","ordered":false,"items":["timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）","其他时间字段：yyyy-MM-dd HH:mm:ss"]},{"type":"code","language":"text","value":"yyyy-MM-dd'T'HH:mm:ss"},{"type":"list","ordered":false,"items":["\"否\"：字段始终有值，不会为null","\"是\"：字段可能为null或空字符串，调用方需进行空值判断"]}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于2个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"/api/suspension/sse"}
    - {"type":"code","language":"text","value":"复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}"}
    - {"type":"code","language":"http","value":"复制curl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"text","value":"/api/suspension/nyse"}
    - {"type":"code","language":"text","value":"复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}"}
    - {"type":"code","language":"http","value":"复制curl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"text","value":"/api/suspension/nasdaq"}
    - {"type":"code","language":"text","value":"复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}"}
    - {"type":"code","language":"http","value":"复制curl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"http","value":"curl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\""}
    - {"type":"code","language":"text","value":"复制{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}"}
    - {"type":"code","language":"json","value":"{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}"}
    - {"type":"code","language":"text","value":"yyyy-MM-dd'T'HH:mm:ss"}
  tables: []
  parameters: []
  markdownContent: "# GET 停复牌信息查询接口\n\n1. REST APIchevron-right\n1. HTTP接口API\n\nEnglish / 中文\n\n\n## GET /api/suspension\n\n\n## 接口说明\n\n该接口提供全球主要交易所（SSE、NYSE、NASDAQ）的停复牌信息查询，所有接口均返回JSON格式数据，按公告时间倒序排列。\n\n\n## 请求频率\n\n免费\n\n每1分钟只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1分钟只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n\n## 接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n\n## 接口地址\n\n1、查询上海证券交易所停复牌信息：\n\n- 基本路径: /api/suspension/sse\n- 完整URL: https://quote.alltick.co/api/suspension/sse\n\n2、查询纽约证券交易所停复牌信息：\n\n- 基本路径: /api/suspension/nyse\n- 完整URL: https://quote.alltick.co/api/suspension/nyse\n\n3、查询纳斯达克交易所停复牌信息：\n\n- 基本路径: /api/suspension/nasdaq\n- 完整URL: https://quote.alltick.co/api/suspension/nasdaq\n\n\n## 请求示例\n\n\n### 1. 获取上证所数据接口\n\n\n#### 接口信息\n\n- URL: /api/suspension/sse\n- 方法: GET\n- 描述: 获取上海证券交易所（SSE）全部停复牌信息\n\n```text\n/api/suspension/sse\n```\n\n\n#### 请求参数\n\ntoken\n\nstring\n\n是\n\n用户套餐token\n\npage\n\ninteger\n\n否\n\n查询页码\n\nsize\n\ninteger\n\n否\n\n每页数据大小\n\n\n#### 响应示例\n\n```text\n复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}\n```\n\n```json\n{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}\n```\n\n```json\n{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 125,\n  \"data\": [\n    {\n      \"symbol\": \"600000\",\n      \"symbolName\": \"浦发银行\",\n      \"haltReason\": \"重大事项停牌\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"09:30:00\",\n      \"haltPeriod\": \"全天停牌\",\n      \"resumeDate\": \"2024-01-16\",\n      \"resumeTime\": \"09:30:00\",\n      \"publishDate\": \"2024-01-14 18:00:00\"\n    }\n  ]\n}\n```\n\n\n#### 响应字段说明\n\n\n#### 公共字段\n\n» success\n\nboolean\n\n是\n\n请求是否成功\n\n» timestamp\n\nstring\n\n是\n\n响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）\n\n» totalCount\n\ninteger\n\n是\n\n数据总条数\n\n» data\n\narray\n\n是\n\n停复牌信息列表\n\n» totalPages\n\ninteger\n\n否\n\n数据总页数（分页查询时返回）\n\n» currentPage\n\ninteger\n\n否\n\n当前页（分页查询时返回）\n\n» currentSize\n\ninteger\n\n否\n\n当前页的数据条数（分页查询时返回）\n\n\n#### data字段（停复牌信息列表中的对象）\n\n每个对象包含以下字段：\n\n» symbol\n\nstring\n\n否\n\n股票代码\n\n» symbolName\n\nstring\n\n是\n\n股票名称\n\n» haltReason\n\nstring\n\n是\n\n停牌原因\n\n» haltDate\n\nstring\n\n是\n\n停牌日期\n\n» haltTime\n\nstring\n\n是\n\n停牌时间\n\n» haltPeriod\n\nstring\n\n是\n\n停牌期限\n\n» resumeDate\n\nstring\n\n是\n\n复牌日期\n\n» resumeTime\n\nstring\n\n是\n\n复牌时间\n\n» publishDate\n\nstring\n\n否\n\n公告时间\n\n\n#### 调用示例\n\n```http\n复制curl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n```http\ncurl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n```http\ncurl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n\n### 2. 获取纽交所数据接口\n\n\n#### 接口信息\n\n- URL: /api/suspension/nyse\n- 方法: GET\n- 描述: 获取纽约证券交易所（NYSE）全部停复牌信息\n\n```text\n/api/suspension/nyse\n```\n\n\n#### 请求参数\n\ntoken\n\nstring\n\n是\n\n用户套餐token\n\npage\n\ninteger\n\n否\n\n查询页码\n\nsize\n\ninteger\n\n否\n\n每页数据大小\n\n\n#### 响应示例\n\n```text\n复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}\n```\n\n```json\n{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}\n```\n\n```json\n{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 89,\n  \"data\": [\n    {\n      \"symbol\": \"AAPL\",\n      \"haltReason\": \"新闻待公布\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"10:15:00\",\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"11:00:00\",\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n      \"sourceExchange\": \"NYSE\"\n      \"publishDate\": \"2024-01-15 10:10:00\n    }\n  ]\n}\n```\n\n\n#### 响应字段说明\n\n\n#### 公共字段\n\n» success\n\nboolean\n\n是\n\n请求是否成功\n\n» timestamp\n\nstring\n\n是\n\n响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）\n\n» totalCount\n\ninteger\n\n是\n\n数据总条数\n\n» data\n\narray\n\n是\n\n停复牌信息列表\n\n» totalPages\n\ninteger\n\n否\n\n数据总页数（分页查询时返回）\n\n» currentPage\n\ninteger\n\n否\n\n当前页（分页查询时返回）\n\n» currentSize\n\ninteger\n\n否\n\n当前页的数据条数（分页查询时返回\n\n\n#### data字段（停复牌信息列表中的对象）\n\n每个对象包含以下字段：\n\n» symbol\n\nstring\n\n否\n\n股票代码\n\n» symbolName\n\nstring\n\n是\n\n股票名称\n\n» haltReason\n\nstring\n\n是\n\n停牌原因\n\n» haltTime\n\nstring\n\n是\n\n停牌时间\n\n» haltDateTime\n\nstring\n\n是\n\n停牌日期时间\n\n» resumeDate\n\nstring\n\n是\n\n复牌日期\n\n» resumeTime\n\nstring\n\n是\n\n复牌时间\n\n» resumeDateTime\n\nstring\n\n是\n\n复牌日期时间\n\n» sourceExchange\n\nstring\n\n是\n\n交易所代码\n\n» publishDate\n\nstring\n\n否\n\n公告时间\n\n\n#### 调用示例\n\n```http\n复制curl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n```http\ncurl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n```http\ncurl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n\n### 3. 获取纳斯达克数据接口\n\n\n#### 接口信息\n\n- URL: /api/suspension/nasdaq\n- 方法: GET\n- 描述: 获取纳斯达克交易所（NASDAQ）全部停复牌信息\n\n```text\n/api/suspension/nasdaq\n```\n\n\n#### 请求参数\n\ntoken\n\nstring\n\n是\n\n用户套餐token\n\npage\n\ninteger\n\n否\n\n查询页码\n\nsize\n\ninteger\n\n否\n\n每页数据大小\n\n\n#### 响应示例\n\n```text\n复制{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}\n```\n\n```json\n{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}\n```\n\n```json\n{\n  \"success\": true,\n  \"timestamp\": \"2024-01-15T10:30:00\",\n  \"totalCount\": 156,\n  \"data\": [\n    {\n      \"symbol\": \"GOOGL\",\n      \"haltDate\": \"2024-01-15\",\n      \"haltTime\": \"13:45:00\",\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n      \"sourceExchange\": \"NASDAQ\",\n      \"haltReason\": \"波动性暂停\",\n      \"pauseThresholdPrice\": \"145.50\",\n      \"resumeDate\": \"2024-01-15\",\n      \"resumeTime\": \"14:00:00\",\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n      \"publishDate\": \"2024-01-15 13:44:30\"\n    }\n  ]\n}\n```\n\n\n#### 响应字段说明\n\n\n#### 公共字段\n\n» success\n\nboolean\n\n是\n\n请求是否成功\n\n» timestamp\n\nstring\n\n是\n\n响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）\n\n» totalCount\n\ninteger\n\n是\n\n数据总条数\n\n» data\n\narray\n\n是\n\n停复牌信息列表\n\n» totalPages\n\ninteger\n\n否\n\n数据总页数（分页查询时返回）\n\n» currentPage\n\ninteger\n\n否\n\n当前页（分页查询时返回）\n\n» currentSize\n\ninteger\n\n否\n\n当前页的数据条数（分页查询时返回）\n\n\n#### data字段（停复牌信息列表中的对象）\n\n每个对象包含以下字段：\n\n» symbol\n\nstring\n\n否\n\n股票代码\n\n» symbolName\n\nstring\n\n是\n\n股票名称\n\n» haltDate\n\nstring\n\n是\n\n停牌日期\n\n» haltTime\n\nstring\n\n是\n\n停牌时间\n\n» haltDateTime\n\nstring\n\n是\n\n停牌日期时间\n\n» sourceExchange\n\nstring\n\n是\n\n交易所代码\n\n» haltReason\n\nstring\n\n是\n\n停牌原因\n\n» pauseThresholdPrice\n\nstring\n\n是\n\n暂停阈值价格\n\n» resumeDate\n\nstring\n\n是\n\n恢复日期\n\n» resumeTime\n\nstring\n\n是\n\n恢复报价时间\n\n» resumeDateTime\n\nstring\n\n是\n\n恢复交易时间\n\n» publishDate\n\nstring\n\n否\n\n公告时间\n\n\n#### 调用示例\n\n```http\n复制curl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n```http\ncurl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n```http\ncurl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n```\n\n\n### 错误响应\n\n所有接口在发生错误时返回以下格式：\n\n```text\n复制{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}\n```\n\n```json\n{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}\n```\n\n```json\n{\n  \"success\": false,\n  \"error\": \"错误描述信息\"\n}\n```\n\nHTTP状态码: 500\n\n\n#### 错误响应字段说明\n\nsuccess\n\nboolean\n\n是\n\n请求是否成功，固定为false\n\nerror\n\nstring\n\n是\n\n错误描述信息\n\n\n### 注意事项\n\n1. 所有接口均不支持分页，返回最近一年的全量数据\n1. 数据已按公告时间倒序排列（最新的在前）\n1. 响应中的时间格式：timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）其他时间字段：yyyy-MM-dd HH:mm:ss\n1. timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）\n1. 其他时间字段：yyyy-MM-dd HH:mm:ss\n1. 建议设置适当的超时时间，大数据量时可能需要较长时间\n1. 字段为空说明：\"否\"：字段始终有值，不会为null\"是\"：字段可能为null或空字符串，调用方需进行空值判断\n1. \"否\"：字段始终有值，不会为null\n1. \"是\"：字段可能为null或空字符串，调用方需进行空值判断\n\n- timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）\n- 其他时间字段：yyyy-MM-dd HH:mm:ss\n\n```text\nyyyy-MM-dd'T'HH:mm:ss\n```\n\n- \"否\"：字段始终有值，不会为null\n- \"是\"：字段可能为null或空字符串，调用方需进行空值判断\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于2个月前\n"
  rawContent: "复制\nREST API\nHTTP接口API\nGET 停复牌信息查询接口\n\nEnglish / 中文\n\nGET /api/suspension\n接口说明\n\n该接口提供全球主要交易所（SSE、NYSE、NASDAQ）的停复牌信息查询，所有接口均返回JSON格式数据，按公告时间倒序排列。\n\n请求频率\n计划\n单个接口单独请求\n同时请求多个http接口\n\n免费\n\n每1分钟只能1次请求\n\n1、10秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔10秒\n3、所有接口相加，1分钟最大请求10次(6秒1次)\n4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用\n\n基础\n\n每1分钟只能1次请求\n\n1、同1秒只能请求1个接口\n\n2、多个接口请求时，需注意/batch-kline接口需间隔3秒\n3、所有接口相加，1分钟最大请求60次(1秒1次)\n4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用\n\n高级\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求10次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔2秒\n3、所有接口相加，1分钟最大请求600次(1秒10次)\n4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用\n\n专业\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部港股\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部A股\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n全部美股\n\n每1分钟只能1次请求\n\n1、所以接口相加，每1秒可请求20次\n\n2、多个接口请求时，需注意/batch-kline接口需间隔1秒\n3、所有接口相加，1分钟最大请求1200次(1秒20次)\n4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用\n\n接口限制\n\n1、请务必阅读：HTTP接口限制说明\n\n2、请务必阅读：错误码说明\n\n接口地址\n\n1、查询上海证券交易所停复牌信息：\n\n基本路径: /api/suspension/sse\n\n完整URL: https://quote.alltick.co/api/suspension/sse\n\n2、查询纽约证券交易所停复牌信息：\n\n基本路径: /api/suspension/nyse\n\n完整URL: https://quote.alltick.co/api/suspension/nyse\n\n3、查询纳斯达克交易所停复牌信息：\n\n基本路径: /api/suspension/nasdaq\n\n完整URL: https://quote.alltick.co/api/suspension/nasdaq\n\n请求示例\n1. 获取上证所数据接口\n接口信息\n\nURL: /api/suspension/sse\n\n方法: GET\n\n描述: 获取上海证券交易所（SSE）全部停复牌信息\n\n请求参数\n字段名\n类型\n是否必填\n描述\n\ntoken\n\nstring\n\n是\n\n用户套餐token\n\npage\n\ninteger\n\n否\n\n查询页码\n\nsize\n\ninteger\n\n否\n\n每页数据大小\n\n响应示例\n复制\n{\n\n  \"success\": true,\n\n  \"timestamp\": \"2024-01-15T10:30:00\",\n\n  \"totalCount\": 125,\n\n  \"data\": [\n\n    {\n\n      \"symbol\": \"600000\",\n\n      \"symbolName\": \"浦发银行\",\n\n      \"haltReason\": \"重大事项停牌\",\n\n      \"haltDate\": \"2024-01-15\",\n\n      \"haltTime\": \"09:30:00\",\n\n      \"haltPeriod\": \"全天停牌\",\n\n      \"resumeDate\": \"2024-01-16\",\n\n      \"resumeTime\": \"09:30:00\",\n\n      \"publishDate\": \"2024-01-14 18:00:00\"\n\n    }\n\n  ]\n\n}\n\n\n响应字段说明\n公共字段\n字段名\n类型\n是否必填\n描述\n\n» success\n\nboolean\n\n是\n\n请求是否成功\n\n» timestamp\n\nstring\n\n是\n\n响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）\n\n» totalCount\n\ninteger\n\n是\n\n数据总条数\n\n» data\n\narray\n\n是\n\n停复牌信息列表\n\n» totalPages\n\ninteger\n\n否\n\n数据总页数（分页查询时返回）\n\n» currentPage\n\ninteger\n\n否\n\n当前页（分页查询时返回）\n\n» currentSize\n\ninteger\n\n否\n\n当前页的数据条数（分页查询时返回）\n\ndata字段（停复牌信息列表中的对象）\n\n每个对象包含以下字段：\n\n字段名\n类型\n是否允许为空\n描述\n\n» symbol\n\nstring\n\n否\n\n股票代码\n\n» symbolName\n\nstring\n\n是\n\n股票名称\n\n» haltReason\n\nstring\n\n是\n\n停牌原因\n\n» haltDate\n\nstring\n\n是\n\n停牌日期\n\n» haltTime\n\nstring\n\n是\n\n停牌时间\n\n» haltPeriod\n\nstring\n\n是\n\n停牌期限\n\n» resumeDate\n\nstring\n\n是\n\n复牌日期\n\n» resumeTime\n\nstring\n\n是\n\n复牌时间\n\n» publishDate\n\nstring\n\n否\n\n公告时间\n\n调用示例\n复制\ncurl -X GET \"<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n2. 获取纽交所数据接口\n接口信息\n\nURL: /api/suspension/nyse\n\n方法: GET\n\n描述: 获取纽约证券交易所（NYSE）全部停复牌信息\n\n请求参数\n字段名\n类型\n是否必填\n描述\n\ntoken\n\nstring\n\n是\n\n用户套餐token\n\npage\n\ninteger\n\n否\n\n查询页码\n\nsize\n\ninteger\n\n否\n\n每页数据大小\n\n响应示例\n复制\n{\n\n  \"success\": true,\n\n  \"timestamp\": \"2024-01-15T10:30:00\",\n\n  \"totalCount\": 89,\n\n  \"data\": [\n\n    {\n\n      \"symbol\": \"AAPL\",\n\n      \"haltReason\": \"新闻待公布\",\n\n      \"haltDate\": \"2024-01-15\",\n\n      \"haltTime\": \"10:15:00\",\n\n      \"haltDateTime\": \"2024-01-15 10:15:00\",\n\n      \"resumeDate\": \"2024-01-15\",\n\n      \"resumeTime\": \"11:00:00\",\n\n      \"resumeDateTime\": \"2024-01-15 11:00:00\",\n\n      \"sourceExchange\": \"NYSE\"\n\n      \"publishDate\": \"2024-01-15 10:10:00\n\n    }\n\n  ]\n\n}\n\n\n响应字段说明\n公共字段\n字段名\n类型\n是否必填\n描述\n\n» success\n\nboolean\n\n是\n\n请求是否成功\n\n» timestamp\n\nstring\n\n是\n\n响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）\n\n» totalCount\n\ninteger\n\n是\n\n数据总条数\n\n» data\n\narray\n\n是\n\n停复牌信息列表\n\n» totalPages\n\ninteger\n\n否\n\n数据总页数（分页查询时返回）\n\n» currentPage\n\ninteger\n\n否\n\n当前页（分页查询时返回）\n\n» currentSize\n\ninteger\n\n否\n\n当前页的数据条数（分页查询时返回\n\ndata字段（停复牌信息列表中的对象）\n\n每个对象包含以下字段：\n\n字段名\n类型\n是否允许为空\n描述\n\n» symbol\n\nstring\n\n否\n\n股票代码\n\n» symbolName\n\nstring\n\n是\n\n股票名称\n\n» haltReason\n\nstring\n\n是\n\n停牌原因\n\n» haltTime\n\nstring\n\n是\n\n停牌时间\n\n» haltDateTime\n\nstring\n\n是\n\n停牌日期时间\n\n» resumeDate\n\nstring\n\n是\n\n复牌日期\n\n» resumeTime\n\nstring\n\n是\n\n复牌时间\n\n» resumeDateTime\n\nstring\n\n是\n\n复牌日期时间\n\n» sourceExchange\n\nstring\n\n是\n\n交易所代码\n\n» publishDate\n\nstring\n\n否\n\n公告时间\n\n调用示例\n复制\ncurl -X GET \"<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n3. 获取纳斯达克数据接口\n接口信息\n\nURL: /api/suspension/nasdaq\n\n方法: GET\n\n描述: 获取纳斯达克交易所（NASDAQ）全部停复牌信息\n\n请求参数\n字段名\n类型\n是否必填\n描述\n\ntoken\n\nstring\n\n是\n\n用户套餐token\n\npage\n\ninteger\n\n否\n\n查询页码\n\nsize\n\ninteger\n\n否\n\n每页数据大小\n\n响应示例\n复制\n{\n\n  \"success\": true,\n\n  \"timestamp\": \"2024-01-15T10:30:00\",\n\n  \"totalCount\": 156,\n\n  \"data\": [\n\n    {\n\n      \"symbol\": \"GOOGL\",\n\n      \"haltDate\": \"2024-01-15\",\n\n      \"haltTime\": \"13:45:00\",\n\n      \"haltDateTime\": \"2024-01-15 13:45:00\",\n\n      \"sourceExchange\": \"NASDAQ\",\n\n      \"haltReason\": \"波动性暂停\",\n\n      \"pauseThresholdPrice\": \"145.50\",\n\n      \"resumeDate\": \"2024-01-15\",\n\n      \"resumeTime\": \"14:00:00\",\n\n      \"resumeDateTime\": \"2024-01-15 14:00:00\",\n\n      \"publishDate\": \"2024-01-15 13:44:30\"\n\n    }\n\n  ]\n\n}\n\n\n响应字段说明\n公共字段\n字段名\n类型\n是否必填\n描述\n\n» success\n\nboolean\n\n是\n\n请求是否成功\n\n» timestamp\n\nstring\n\n是\n\n响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）\n\n» totalCount\n\ninteger\n\n是\n\n数据总条数\n\n» data\n\narray\n\n是\n\n停复牌信息列表\n\n» totalPages\n\ninteger\n\n否\n\n数据总页数（分页查询时返回）\n\n» currentPage\n\ninteger\n\n否\n\n当前页（分页查询时返回）\n\n» currentSize\n\ninteger\n\n否\n\n当前页的数据条数（分页查询时返回）\n\ndata字段（停复牌信息列表中的对象）\n\n每个对象包含以下字段：\n\n字段名\n类型\n是否允许为空\n描述\n\n» symbol\n\nstring\n\n否\n\n股票代码\n\n» symbolName\n\nstring\n\n是\n\n股票名称\n\n» haltDate\n\nstring\n\n是\n\n停牌日期\n\n» haltTime\n\nstring\n\n是\n\n停牌时间\n\n» haltDateTime\n\nstring\n\n是\n\n停牌日期时间\n\n» sourceExchange\n\nstring\n\n是\n\n交易所代码\n\n» haltReason\n\nstring\n\n是\n\n停牌原因\n\n» pauseThresholdPrice\n\nstring\n\n是\n\n暂停阈值价格\n\n» resumeDate\n\nstring\n\n是\n\n恢复日期\n\n» resumeTime\n\nstring\n\n是\n\n恢复报价时间\n\n» resumeDateTime\n\nstring\n\n是\n\n恢复交易时间\n\n» publishDate\n\nstring\n\n否\n\n公告时间\n\n调用示例\n复制\ncurl -X GET \"<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>\" -H \"Accept: application/json\"\n错误响应\n\n所有接口在发生错误时返回以下格式：\n\n复制\n{\n\n  \"success\": false,\n\n  \"error\": \"错误描述信息\"\n\n}\n\n\n\nHTTP状态码: 500\n\n错误响应字段说明\n字段名\n类型\n是否必填\n描述\n\nsuccess\n\nboolean\n\n是\n\n请求是否成功，固定为false\n\nerror\n\nstring\n\n是\n\n错误描述信息\n\n注意事项\n\n所有接口均不支持分页，返回最近一年的全量数据\n\n数据已按公告时间倒序排列（最新的在前）\n\n响应中的时间格式：\n\ntimestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）\n\n其他时间字段：yyyy-MM-dd HH:mm:ss\n\n建议设置适当的超时时间，大数据量时可能需要较长时间\n\n字段为空说明：\n\n\"否\"：字段始终有值，不会为null\n\n\"是\"：字段可能为null或空字符串，调用方需进行空值判断\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nGET 股票产品基础信息批量查询\n下一页\n涨跌幅、休市、假期、涨停跌停、新股上市和退市\n\n最后更新于2个月前"
  suggestedFilename: "rest-api_stock-http-interface-api_get-latest-transaction-price-query-1-1"
---

# GET 停复牌信息查询接口

## 源URL

https://apis.alltick.co/rest-api/stock-http-interface-api/get-latest-transaction-price-query-1-1

## 文档正文

1. REST APIchevron-right
1. HTTP接口API

English / 中文

## GET /api/suspension

## 接口说明

该接口提供全球主要交易所（SSE、NYSE、NASDAQ）的停复牌信息查询，所有接口均返回JSON格式数据，按公告时间倒序排列。

## 请求频率

免费

每1分钟只能1次请求

1、10秒只能请求1个接口

2、多个接口请求时，需注意/batch-kline接口需间隔10秒 3、所有接口相加，1分钟最大请求10次(6秒1次) 4、每天总共最大可请求14400次，超过则第二天凌晨恢复使用

基础

每1分钟只能1次请求

1、同1秒只能请求1个接口

2、多个接口请求时，需注意/batch-kline接口需间隔3秒 3、所有接口相加，1分钟最大请求60次(1秒1次) 4、每天总共最大可请求86400次，超过则第二天凌晨恢复使用

高级

每1分钟只能1次请求

1、所以接口相加，每1秒可请求10次

2、多个接口请求时，需注意/batch-kline接口需间隔2秒 3、所有接口相加，1分钟最大请求600次(1秒10次) 4、每天总共最大可请求864000次，超过则第二天凌晨恢复使用

专业

每1分钟只能1次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部港股

每1分钟只能1次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部A股

每1分钟只能1次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

全部美股

每1分钟只能1次请求

1、所以接口相加，每1秒可请求20次

2、多个接口请求时，需注意/batch-kline接口需间隔1秒 3、所有接口相加，1分钟最大请求1200次(1秒20次) 4、每天总共最大可请求1728000次，超过则第二天凌晨恢复使用

## 接口限制

1、请务必阅读：HTTP接口限制说明

2、请务必阅读：错误码说明

## 接口地址

1、查询上海证券交易所停复牌信息：

- 基本路径: /api/suspension/sse
- 完整URL: https://quote.alltick.co/api/suspension/sse

2、查询纽约证券交易所停复牌信息：

- 基本路径: /api/suspension/nyse
- 完整URL: https://quote.alltick.co/api/suspension/nyse

3、查询纳斯达克交易所停复牌信息：

- 基本路径: /api/suspension/nasdaq
- 完整URL: https://quote.alltick.co/api/suspension/nasdaq

## 请求示例

### 1. 获取上证所数据接口

#### 接口信息

- URL: /api/suspension/sse
- 方法: GET
- 描述: 获取上海证券交易所（SSE）全部停复牌信息

```text
/api/suspension/sse
```

#### 请求参数

token

string

是

用户套餐token

page

integer

否

查询页码

size

integer

否

每页数据大小

#### 响应示例

```text
复制{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 125,
  "data": [
    {
      "symbol": "600000",
      "symbolName": "浦发银行",
      "haltReason": "重大事项停牌",
      "haltDate": "2024-01-15",
      "haltTime": "09:30:00",
      "haltPeriod": "全天停牌",
      "resumeDate": "2024-01-16",
      "resumeTime": "09:30:00",
      "publishDate": "2024-01-14 18:00:00"
    }
  ]
}
```

```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 125,
  "data": [
    {
      "symbol": "600000",
      "symbolName": "浦发银行",
      "haltReason": "重大事项停牌",
      "haltDate": "2024-01-15",
      "haltTime": "09:30:00",
      "haltPeriod": "全天停牌",
      "resumeDate": "2024-01-16",
      "resumeTime": "09:30:00",
      "publishDate": "2024-01-14 18:00:00"
    }
  ]
}
```

```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 125,
  "data": [
    {
      "symbol": "600000",
      "symbolName": "浦发银行",
      "haltReason": "重大事项停牌",
      "haltDate": "2024-01-15",
      "haltTime": "09:30:00",
      "haltPeriod": "全天停牌",
      "resumeDate": "2024-01-16",
      "resumeTime": "09:30:00",
      "publishDate": "2024-01-14 18:00:00"
    }
  ]
}
```

#### 响应字段说明

#### 公共字段

» success

boolean

是

请求是否成功

» timestamp

string

是

响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）

» totalCount

integer

是

数据总条数

» data

array

是

停复牌信息列表

» totalPages

integer

否

数据总页数（分页查询时返回）

» currentPage

integer

否

当前页（分页查询时返回）

» currentSize

integer

否

当前页的数据条数（分页查询时返回）

#### data字段（停复牌信息列表中的对象）

每个对象包含以下字段：

» symbol

string

否

股票代码

» symbolName

string

是

股票名称

» haltReason

string

是

停牌原因

» haltDate

string

是

停牌日期

» haltTime

string

是

停牌时间

» haltPeriod

string

是

停牌期限

» resumeDate

string

是

复牌日期

» resumeTime

string

是

复牌时间

» publishDate

string

否

公告时间

#### 调用示例

```http
复制curl -X GET "<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

```http
curl -X GET "<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

```http
curl -X GET "<https://quote.alltick.co/api/suspension/sse?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

### 2. 获取纽交所数据接口

#### 接口信息

- URL: /api/suspension/nyse
- 方法: GET
- 描述: 获取纽约证券交易所（NYSE）全部停复牌信息

```text
/api/suspension/nyse
```

#### 请求参数

token

string

是

用户套餐token

page

integer

否

查询页码

size

integer

否

每页数据大小

#### 响应示例

```text
复制{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 89,
  "data": [
    {
      "symbol": "AAPL",
      "haltReason": "新闻待公布",
      "haltDate": "2024-01-15",
      "haltTime": "10:15:00",
      "haltDateTime": "2024-01-15 10:15:00",
      "resumeDate": "2024-01-15",
      "resumeTime": "11:00:00",
      "resumeDateTime": "2024-01-15 11:00:00",
      "sourceExchange": "NYSE"
      "publishDate": "2024-01-15 10:10:00
    }
  ]
}
```

```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 89,
  "data": [
    {
      "symbol": "AAPL",
      "haltReason": "新闻待公布",
      "haltDate": "2024-01-15",
      "haltTime": "10:15:00",
      "haltDateTime": "2024-01-15 10:15:00",
      "resumeDate": "2024-01-15",
      "resumeTime": "11:00:00",
      "resumeDateTime": "2024-01-15 11:00:00",
      "sourceExchange": "NYSE"
      "publishDate": "2024-01-15 10:10:00
    }
  ]
}
```

```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 89,
  "data": [
    {
      "symbol": "AAPL",
      "haltReason": "新闻待公布",
      "haltDate": "2024-01-15",
      "haltTime": "10:15:00",
      "haltDateTime": "2024-01-15 10:15:00",
      "resumeDate": "2024-01-15",
      "resumeTime": "11:00:00",
      "resumeDateTime": "2024-01-15 11:00:00",
      "sourceExchange": "NYSE"
      "publishDate": "2024-01-15 10:10:00
    }
  ]
}
```

#### 响应字段说明

#### 公共字段

» success

boolean

是

请求是否成功

» timestamp

string

是

响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）

» totalCount

integer

是

数据总条数

» data

array

是

停复牌信息列表

» totalPages

integer

否

数据总页数（分页查询时返回）

» currentPage

integer

否

当前页（分页查询时返回）

» currentSize

integer

否

当前页的数据条数（分页查询时返回

#### data字段（停复牌信息列表中的对象）

每个对象包含以下字段：

» symbol

string

否

股票代码

» symbolName

string

是

股票名称

» haltReason

string

是

停牌原因

» haltTime

string

是

停牌时间

» haltDateTime

string

是

停牌日期时间

» resumeDate

string

是

复牌日期

» resumeTime

string

是

复牌时间

» resumeDateTime

string

是

复牌日期时间

» sourceExchange

string

是

交易所代码

» publishDate

string

否

公告时间

#### 调用示例

```http
复制curl -X GET "<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

```http
curl -X GET "<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

```http
curl -X GET "<https://quote.alltick.co/api/suspension/nyse?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

### 3. 获取纳斯达克数据接口

#### 接口信息

- URL: /api/suspension/nasdaq
- 方法: GET
- 描述: 获取纳斯达克交易所（NASDAQ）全部停复牌信息

```text
/api/suspension/nasdaq
```

#### 请求参数

token

string

是

用户套餐token

page

integer

否

查询页码

size

integer

否

每页数据大小

#### 响应示例

```text
复制{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 156,
  "data": [
    {
      "symbol": "GOOGL",
      "haltDate": "2024-01-15",
      "haltTime": "13:45:00",
      "haltDateTime": "2024-01-15 13:45:00",
      "sourceExchange": "NASDAQ",
      "haltReason": "波动性暂停",
      "pauseThresholdPrice": "145.50",
      "resumeDate": "2024-01-15",
      "resumeTime": "14:00:00",
      "resumeDateTime": "2024-01-15 14:00:00",
      "publishDate": "2024-01-15 13:44:30"
    }
  ]
}
```

```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 156,
  "data": [
    {
      "symbol": "GOOGL",
      "haltDate": "2024-01-15",
      "haltTime": "13:45:00",
      "haltDateTime": "2024-01-15 13:45:00",
      "sourceExchange": "NASDAQ",
      "haltReason": "波动性暂停",
      "pauseThresholdPrice": "145.50",
      "resumeDate": "2024-01-15",
      "resumeTime": "14:00:00",
      "resumeDateTime": "2024-01-15 14:00:00",
      "publishDate": "2024-01-15 13:44:30"
    }
  ]
}
```

```json
{
  "success": true,
  "timestamp": "2024-01-15T10:30:00",
  "totalCount": 156,
  "data": [
    {
      "symbol": "GOOGL",
      "haltDate": "2024-01-15",
      "haltTime": "13:45:00",
      "haltDateTime": "2024-01-15 13:45:00",
      "sourceExchange": "NASDAQ",
      "haltReason": "波动性暂停",
      "pauseThresholdPrice": "145.50",
      "resumeDate": "2024-01-15",
      "resumeTime": "14:00:00",
      "resumeDateTime": "2024-01-15 14:00:00",
      "publishDate": "2024-01-15 13:44:30"
    }
  ]
}
```

#### 响应字段说明

#### 公共字段

» success

boolean

是

请求是否成功

» timestamp

string

是

响应时间戳（格式：yyyy-MM-dd'T'HH:mm:ss）

» totalCount

integer

是

数据总条数

» data

array

是

停复牌信息列表

» totalPages

integer

否

数据总页数（分页查询时返回）

» currentPage

integer

否

当前页（分页查询时返回）

» currentSize

integer

否

当前页的数据条数（分页查询时返回）

#### data字段（停复牌信息列表中的对象）

每个对象包含以下字段：

» symbol

string

否

股票代码

» symbolName

string

是

股票名称

» haltDate

string

是

停牌日期

» haltTime

string

是

停牌时间

» haltDateTime

string

是

停牌日期时间

» sourceExchange

string

是

交易所代码

» haltReason

string

是

停牌原因

» pauseThresholdPrice

string

是

暂停阈值价格

» resumeDate

string

是

恢复日期

» resumeTime

string

是

恢复报价时间

» resumeDateTime

string

是

恢复交易时间

» publishDate

string

否

公告时间

#### 调用示例

```http
复制curl -X GET "<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

```http
curl -X GET "<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

```http
curl -X GET "<https://quote.alltick.co/api/suspension/nasdaq?token=您的Token&page=1&size=10>" -H "Accept: application/json"
```

### 错误响应

所有接口在发生错误时返回以下格式：

```text
复制{
  "success": false,
  "error": "错误描述信息"
}
```

```json
{
  "success": false,
  "error": "错误描述信息"
}
```

```json
{
  "success": false,
  "error": "错误描述信息"
}
```

HTTP状态码: 500

#### 错误响应字段说明

success

boolean

是

请求是否成功，固定为false

error

string

是

错误描述信息

### 注意事项

1. 所有接口均不支持分页，返回最近一年的全量数据
1. 数据已按公告时间倒序排列（最新的在前）
1. 响应中的时间格式：timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）其他时间字段：yyyy-MM-dd HH:mm:ss
1. timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）
1. 其他时间字段：yyyy-MM-dd HH:mm:ss
1. 建议设置适当的超时时间，大数据量时可能需要较长时间
1. 字段为空说明："否"：字段始终有值，不会为null"是"：字段可能为null或空字符串，调用方需进行空值判断
1. "否"：字段始终有值，不会为null
1. "是"：字段可能为null或空字符串，调用方需进行空值判断

- timestamp字段：ISO格式（yyyy-MM-dd'T'HH:mm:ss）
- 其他时间字段：yyyy-MM-dd HH:mm:ss

```text
yyyy-MM-dd'T'HH:mm:ss
```

- "否"：字段始终有值，不会为null
- "是"：字段可能为null或空字符串，调用方需进行空值判断

#### AllTick网站

官方网站：https://alltick.co/

最后更新于2个月前
