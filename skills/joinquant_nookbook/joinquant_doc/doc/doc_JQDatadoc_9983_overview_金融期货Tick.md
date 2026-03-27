---
id: "url-7a226f2d"
type: "website"
title: "金融期货Tick"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9983"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:24:05.706Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9983"
  headings:
    - {"level":3,"text":"金融期货Tick","id":"tick"}
    - {"level":5,"text":"金融期货Tick返回结果","id":"tick-1"}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "金融期货Tick参数"
  lists:
    - {"type":"ul","items":["历史范围：2010年至今；"]}
    - {"type":"ul","items":["支持 2010-01-01 至今的商品期货tick数据，提供买一卖一数据。每0.5秒一条数据，盘后15:00更新，24:00校对完成入库。","如果要获取主力合约的tick数据，可以先使用get_dominant_future(underlying_symbol,dt)获取主力合约对应的标的，然后再用get_ticks()获取该合约的tick数据"]}
    - {"type":"ul","items":["用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"ul","items":["security: 期货代码,不支持传入多个标的","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（手）","float"],["money","累计成交额","float"],["position","持仓量","float"],["a1_v","一档卖量","float"],["a1_p","一档卖价","float"],["b1_v","一档买量","float"],["b1_p","一档买价","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"language":"python","code":"#获取IF1905期货合约在“2019-04-03”前8个时间单位的tick数据,start_dt和count只能有一个不为None值\ndf=get_ticks('IF1905.CCFX',end_dt='2019-04-03',count=8)\nprint(df)\n\n                     time  current    high     low  volume         money  \\\n0 2019-04-02 14:59:28.000   3975.4  4001.8  3963.8  2200.0  2.628635e+09   \n1 2019-04-02 14:59:30.000   3976.2  4001.8  3963.8  2201.0  2.629827e+09   \n2 2019-04-02 14:59:31.000   3976.8  4001.8  3963.8  2202.0  2.631021e+09   \n3 2019-04-02 14:59:50.000   3975.0  4001.8  3963.8  2203.0  2.632213e+09   \n4 2019-04-02 14:59:50.500   3975.6  4001.8  3963.8  2204.0  2.633406e+09   \n5 2019-04-02 14:59:54.000   3975.0  4001.8  3963.8  2205.0  2.634598e+09   \n6 2019-04-02 14:59:58.000   3974.2  4001.8  3963.8  2207.0  2.636983e+09   \n7 2019-04-02 14:59:59.000   3978.0  4001.8  3963.8  2208.0  2.638176e+09   \n\n   position    a1_p  a1_v    b1_p  b1_v  \n0    4881.0  3977.0   1.0  3975.8   4.0  \n1    4882.0  3976.2   1.0  3975.4   1.0  \n2    4882.0  3978.8   1.0  3975.4   1.0  \n3    4883.0  3975.6   2.0  3975.0   1.0  \n4    4883.0  3978.0   1.0  3975.0   1.0  \n5    4883.0  3976.4   4.0  3973.0   1.0  \n6    4885.0  3978.0   1.0  3973.4   1.0  \n7    4886.0  3978.8   2.0  3973.4   1.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"金融期货Tick"}
    - {"type":"list","listType":"ul","items":["历史范围：2010年至今；"]}
    - {"type":"codeblock","language":"python","content":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["支持 2010-01-01 至今的商品期货tick数据，提供买一卖一数据。每0.5秒一条数据，盘后15:00更新，24:00校对完成入库。","如果要获取主力合约的tick数据，可以先使用get_dominant_future(underlying_symbol,dt)获取主力合约对应的标的，然后再用get_ticks()获取该合约的tick数据"]}
    - {"type":"list","listType":"ul","items":["用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"paragraph","content":"金融期货Tick参数"}
    - {"type":"list","listType":"ul","items":["security: 期货代码,不支持传入多个标的","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"list","listType":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
    - {"type":"heading","level":5,"content":"金融期货Tick返回结果"}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（手）","float"],["money","累计成交额","float"],["position","持仓量","float"],["a1_v","一档卖量","float"],["a1_p","一档卖价","float"],["b1_v","一档买量","float"],["b1_p","一档买价","float"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#获取IF1905期货合约在“2019-04-03”前8个时间单位的tick数据,start_dt和count只能有一个不为None值\ndf=get_ticks('IF1905.CCFX',end_dt='2019-04-03',count=8)\nprint(df)\n\n                     time  current    high     low  volume         money  \\\n0 2019-04-02 14:59:28.000   3975.4  4001.8  3963.8  2200.0  2.628635e+09   \n1 2019-04-02 14:59:30.000   3976.2  4001.8  3963.8  2201.0  2.629827e+09   \n2 2019-04-02 14:59:31.000   3976.8  4001.8  3963.8  2202.0  2.631021e+09   \n3 2019-04-02 14:59:50.000   3975.0  4001.8  3963.8  2203.0  2.632213e+09   \n4 2019-04-02 14:59:50.500   3975.6  4001.8  3963.8  2204.0  2.633406e+09   \n5 2019-04-02 14:59:54.000   3975.0  4001.8  3963.8  2205.0  2.634598e+09   \n6 2019-04-02 14:59:58.000   3974.2  4001.8  3963.8  2207.0  2.636983e+09   \n7 2019-04-02 14:59:59.000   3978.0  4001.8  3963.8  2208.0  2.638176e+09   \n\n   position    a1_p  a1_v    b1_p  b1_v  \n0    4881.0  3977.0   1.0  3975.8   4.0  \n1    4882.0  3976.2   1.0  3975.4   1.0  \n2    4882.0  3978.8   1.0  3975.4   1.0  \n3    4883.0  3975.6   2.0  3975.0   1.0  \n4    4883.0  3978.0   1.0  3975.0   1.0  \n5    4883.0  3976.4   4.0  3973.0   1.0  \n6    4885.0  3978.0   1.0  3973.4   1.0  \n7    4886.0  3978.8   2.0  3973.4   1.0"}
  suggestedFilename: "doc_JQDatadoc_9983_overview_金融期货Tick"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9983"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 金融期货Tick

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9983

## 描述

描述

## 内容

#### 金融期货Tick

- 历史范围：2010年至今；

```python
get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)
```

描述

- 支持 2010-01-01 至今的商品期货tick数据，提供买一卖一数据。每0.5秒一条数据，盘后15:00更新，24:00校对完成入库。
- 如果要获取主力合约的tick数据，可以先使用get_dominant_future(underlying_symbol,dt)获取主力合约对应的标的，然后再用get_ticks()获取该合约的tick数据

- 用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com

金融期货Tick参数

- security: 期货代码,不支持传入多个标的
- start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'
- end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'
- count: 取出指定时间区间内前多少条的tick数据。
- fields: 选择要获取的行情数据字段，默认为None，返回结果如下：
- skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据
- df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray

- 同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据

###### 金融期货Tick返回结果

| 字段名 | 说明 | 字段类型 |
| --- | --- | --- |
| time | 时间 | datetime |
| current | 当前价 | float |
| high | 当日最高价 | float |
| low | 当日最低价 | float |
| volume | 累计成交量（手） | float |
| money | 累计成交额 | float |
| position | 持仓量 | float |
| a1_v | 一档卖量 | float |
| a1_p | 一档卖价 | float |
| b1_v | 一档买量 | float |
| b1_p | 一档买价 | float |

###### 示例：

```python
#获取IF1905期货合约在“2019-04-03”前8个时间单位的tick数据,start_dt和count只能有一个不为None值
df=get_ticks('IF1905.CCFX',end_dt='2019-04-03',count=8)
print(df)

                     time  current    high     low  volume         money  \
0 2019-04-02 14:59:28.000   3975.4  4001.8  3963.8  2200.0  2.628635e+09   
1 2019-04-02 14:59:30.000   3976.2  4001.8  3963.8  2201.0  2.629827e+09   
2 2019-04-02 14:59:31.000   3976.8  4001.8  3963.8  2202.0  2.631021e+09   
3 2019-04-02 14:59:50.000   3975.0  4001.8  3963.8  2203.0  2.632213e+09   
4 2019-04-02 14:59:50.500   3975.6  4001.8  3963.8  2204.0  2.633406e+09   
5 2019-04-02 14:59:54.000   3975.0  4001.8  3963.8  2205.0  2.634598e+09   
6 2019-04-02 14:59:58.000   3974.2  4001.8  3963.8  2207.0  2.636983e+09   
7 2019-04-02 14:59:59.000   3978.0  4001.8  3963.8  2208.0  2.638176e+09   

   position    a1_p  a1_v    b1_p  b1_v  
0    4881.0  3977.0   1.0  3975.8   4.0  
1    4882.0  3976.2   1.0  3975.4   1.0  
2    4882.0  3978.8   1.0  3975.4   1.0  
3    4883.0  3975.6   2.0  3975.0   1.0  
4    4883.0  3978.0   1.0  3975.0   1.0  
5    4883.0  3976.4   4.0  3973.0   1.0  
6    4885.0  3978.0   1.0  3973.4   1.0  
7    4886.0  3978.8   2.0  3973.4   1.0
```
