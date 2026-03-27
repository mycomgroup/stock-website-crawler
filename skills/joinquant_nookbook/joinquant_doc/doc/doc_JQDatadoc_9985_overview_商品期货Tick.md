---
id: "url-7a226f2f"
type: "website"
title: "商品期货Tick"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9985"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:24:09.662Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9985"
  headings:
    - {"level":3,"text":"商品期货Tick","id":"tick"}
    - {"level":5,"text":"商品期货Tick返回结果","id":"tick-1"}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "商品期货Tick参数"
    - "注意："
  lists:
    - {"type":"ul","items":["历史范围：2010年至今；"]}
    - {"type":"ul","items":["支持 2010-01-01 至今的商品期货tick数据，提供买一卖一数据。每0.5秒一条数据，盘后15:00更新，24:00校对完成入库。","如果要获取主力合约的tick数据，可以先使用get_dominant_future(underlying_symbol,dt)获取主力合约对应的标的，然后再用get_ticks()获取该合约的tick数据"]}
    - {"type":"ul","items":["用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"ul","items":["security: 期货代码,不支持传入多个标的","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray","自2020年1月1日起，交易所调整商品期货【成交量和持仓量和成交额】的统计、发布和报送口径由双边计算统一为单边计算。聚宽的数据处理规则与交易所保持一致，如考虑前后统计口径保持一尺，可将相关字段的数值除以二用于获得大致结果。"]}
    - {"type":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（手）","float"],["money","累计成交额","float"],["position","持仓量","float"],["a1_v","一档卖量","float"],["a1_p","一档卖价","float"],["b1_v","一档买量","float"],["b1_p","一档买价","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"language":"python","code":"#获取AU1812期货合约在“2018-07-03”前8个时间单位的tick数据,start_dt和count只能有一个不为None值\ndf=get_ticks('AU1812.XSGE',end_dt='2018-07-03',count=8)\nprint(df)\n                     time  current    high    low   volume         money  \\\n0 2018-07-02 23:59:35.500   272.00  272.95  272.0  42922.0  1.170027e+10   \n1 2018-07-02 23:59:37.000   272.05  272.95  272.0  42942.0  1.170571e+10   \n2 2018-07-02 23:59:37.500   272.05  272.95  272.0  42966.0  1.171224e+10   \n3 2018-07-02 23:59:38.000   272.05  272.95  272.0  42974.0  1.171442e+10   \n4 2018-07-02 23:59:43.000   272.05  272.95  272.0  42978.0  1.171550e+10   \n5 2018-07-02 23:59:45.500   272.05  272.95  272.0  42986.0  1.171768e+10   \n6 2018-07-02 23:59:46.000   272.05  272.95  272.0  42994.0  1.171986e+10   \n7 2018-07-02 23:59:59.000   272.05  272.95  272.0  42998.0  1.172094e+10   \n\n   position    a1_p  a1_v    b1_p   b1_v  \n0  361578.0  272.05  57.0  272.00  281.0  \n1  361570.0  272.05  12.0  272.00  289.0  \n2  361562.0  272.10  96.0  272.05   14.0  \n3  361554.0  272.10  97.0  272.05   25.0  \n4  361554.0  272.10  97.0  272.05   24.0  \n5  361546.0  272.10  95.0  272.05   20.0  \n6  361538.0  272.10  91.0  272.05   16.0  \n7  361534.0  272.10  85.0  272.05   17.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"商品期货Tick"}
    - {"type":"list","listType":"ul","items":["历史范围：2010年至今；"]}
    - {"type":"codeblock","language":"python","content":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["支持 2010-01-01 至今的商品期货tick数据，提供买一卖一数据。每0.5秒一条数据，盘后15:00更新，24:00校对完成入库。","如果要获取主力合约的tick数据，可以先使用get_dominant_future(underlying_symbol,dt)获取主力合约对应的标的，然后再用get_ticks()获取该合约的tick数据"]}
    - {"type":"list","listType":"ul","items":["用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"paragraph","content":"商品期货Tick参数"}
    - {"type":"list","listType":"ul","items":["security: 期货代码,不支持传入多个标的","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray","自2020年1月1日起，交易所调整商品期货【成交量和持仓量和成交额】的统计、发布和报送口径由双边计算统一为单边计算。聚宽的数据处理规则与交易所保持一致，如考虑前后统计口径保持一尺，可将相关字段的数值除以二用于获得大致结果。"]}
    - {"type":"paragraph","content":"注意："}
    - {"type":"list","listType":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
    - {"type":"heading","level":5,"content":"商品期货Tick返回结果"}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（手）","float"],["money","累计成交额","float"],["position","持仓量","float"],["a1_v","一档卖量","float"],["a1_p","一档卖价","float"],["b1_v","一档买量","float"],["b1_p","一档买价","float"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#获取AU1812期货合约在“2018-07-03”前8个时间单位的tick数据,start_dt和count只能有一个不为None值\ndf=get_ticks('AU1812.XSGE',end_dt='2018-07-03',count=8)\nprint(df)\n                     time  current    high    low   volume         money  \\\n0 2018-07-02 23:59:35.500   272.00  272.95  272.0  42922.0  1.170027e+10   \n1 2018-07-02 23:59:37.000   272.05  272.95  272.0  42942.0  1.170571e+10   \n2 2018-07-02 23:59:37.500   272.05  272.95  272.0  42966.0  1.171224e+10   \n3 2018-07-02 23:59:38.000   272.05  272.95  272.0  42974.0  1.171442e+10   \n4 2018-07-02 23:59:43.000   272.05  272.95  272.0  42978.0  1.171550e+10   \n5 2018-07-02 23:59:45.500   272.05  272.95  272.0  42986.0  1.171768e+10   \n6 2018-07-02 23:59:46.000   272.05  272.95  272.0  42994.0  1.171986e+10   \n7 2018-07-02 23:59:59.000   272.05  272.95  272.0  42998.0  1.172094e+10   \n\n   position    a1_p  a1_v    b1_p   b1_v  \n0  361578.0  272.05  57.0  272.00  281.0  \n1  361570.0  272.05  12.0  272.00  289.0  \n2  361562.0  272.10  96.0  272.05   14.0  \n3  361554.0  272.10  97.0  272.05   25.0  \n4  361554.0  272.10  97.0  272.05   24.0  \n5  361546.0  272.10  95.0  272.05   20.0  \n6  361538.0  272.10  91.0  272.05   16.0  \n7  361534.0  272.10  85.0  272.05   17.0"}
  suggestedFilename: "doc_JQDatadoc_9985_overview_商品期货Tick"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9985"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 商品期货Tick

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9985

## 描述

描述

## 内容

#### 商品期货Tick

- 历史范围：2010年至今；

```python
get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)
```

描述

- 支持 2010-01-01 至今的商品期货tick数据，提供买一卖一数据。每0.5秒一条数据，盘后15:00更新，24:00校对完成入库。
- 如果要获取主力合约的tick数据，可以先使用get_dominant_future(underlying_symbol,dt)获取主力合约对应的标的，然后再用get_ticks()获取该合约的tick数据

- 用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com

商品期货Tick参数

- security: 期货代码,不支持传入多个标的
- start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'
- end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'
- count: 取出指定时间区间内前多少条的tick数据。
- fields: 选择要获取的行情数据字段，默认为None，返回结果如下：
- skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据
- df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray
- 自2020年1月1日起，交易所调整商品期货【成交量和持仓量和成交额】的统计、发布和报送口径由双边计算统一为单边计算。聚宽的数据处理规则与交易所保持一致，如考虑前后统计口径保持一尺，可将相关字段的数值除以二用于获得大致结果。

注意：

- 同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据

###### 商品期货Tick返回结果

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
#获取AU1812期货合约在“2018-07-03”前8个时间单位的tick数据,start_dt和count只能有一个不为None值
df=get_ticks('AU1812.XSGE',end_dt='2018-07-03',count=8)
print(df)
                     time  current    high    low   volume         money  \
0 2018-07-02 23:59:35.500   272.00  272.95  272.0  42922.0  1.170027e+10   
1 2018-07-02 23:59:37.000   272.05  272.95  272.0  42942.0  1.170571e+10   
2 2018-07-02 23:59:37.500   272.05  272.95  272.0  42966.0  1.171224e+10   
3 2018-07-02 23:59:38.000   272.05  272.95  272.0  42974.0  1.171442e+10   
4 2018-07-02 23:59:43.000   272.05  272.95  272.0  42978.0  1.171550e+10   
5 2018-07-02 23:59:45.500   272.05  272.95  272.0  42986.0  1.171768e+10   
6 2018-07-02 23:59:46.000   272.05  272.95  272.0  42994.0  1.171986e+10   
7 2018-07-02 23:59:59.000   272.05  272.95  272.0  42998.0  1.172094e+10   

   position    a1_p  a1_v    b1_p   b1_v  
0  361578.0  272.05  57.0  272.00  281.0  
1  361570.0  272.05  12.0  272.00  289.0  
2  361562.0  272.10  96.0  272.05   14.0  
3  361554.0  272.10  97.0  272.05   25.0  
4  361554.0  272.10  97.0  272.05   24.0  
5  361546.0  272.10  95.0  272.05   20.0  
6  361538.0  272.10  91.0  272.05   16.0  
7  361534.0  272.10  85.0  272.05   17.0
```
