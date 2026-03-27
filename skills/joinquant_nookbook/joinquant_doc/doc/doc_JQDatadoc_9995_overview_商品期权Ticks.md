---
id: "url-7a226f4e"
type: "website"
title: "商品期权Ticks"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9995"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:24:33.485Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9995"
  headings:
    - {"level":3,"text":"商品期权Ticks","id":"ticks"}
    - {"level":5,"text":"期权tick返回结果","id":"tick"}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "购买"
    - "商品期权参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今"]}
    - {"type":"ul","items":["支持商品期权tick数据，每0.5s一条数据，盘后15:00更新，24:00校对完成入。"]}
    - {"type":"ul","items":["用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"ul","items":["security: 期权代码；如security='10001979.XSHG' security='CU2001C42000.XSGE'#铜期权，上海期货交易所； security='SR003C5600.XZCE' #白糖期权，郑州商品交易所； security='M2005-P-2400.XDCE' #豆粕期权，大连商品交易所；","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（手）","float"],["money","累计成交额","float"],["position","持仓量","float"],["a1_v","一档卖量","float"],["a1_p","一档卖价","float"],["b1_v","一档买量","float"],["b1_p","一档买价","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"language":"python","code":"#获取PG2204-C-4300.XDCE期权合约在“2022-03-07”前8个时间单位的tick数据,start_dt和count只能有一个不为None值\ndf=get_ticks('PG2204-C-4300.XDCE',end_dt='2022-03-07',count=8)\nprint(df)\n\n                     time  current   high    low  volume    money  position  \\\n0 2021-07-09 13:38:43.228    649.8  649.8  627.6     2.0  25548.0       1.0   \n1 2021-07-16 13:52:32.956    583.2  583.2  583.2     1.0  11664.0       1.0   \n2 2021-08-12 13:37:10.824    699.8  699.8  699.8     1.0  13996.0       2.0   \n3 2021-08-24 13:35:48.156    550.6  550.6  550.6     1.0  11012.0       2.0   \n4 2021-12-22 14:23:37.476    411.8  411.8  411.8     1.0   8236.0       1.0   \n\n    a1_p  a1_v   b1_p  b1_v  \n0  682.8   2.0  645.4   1.0  \n1  603.2   1.0  570.4   2.0  \n2  702.2   1.0  660.4   1.0  \n3  587.8   1.0  556.4   1.0  \n4  431.2   1.0  411.2   1.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"商品期权Ticks"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今"]}
    - {"type":"codeblock","language":"python","content":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["支持商品期权tick数据，每0.5s一条数据，盘后15:00更新，24:00校对完成入。"]}
    - {"type":"paragraph","content":"购买"}
    - {"type":"list","listType":"ul","items":["用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"paragraph","content":"商品期权参数"}
    - {"type":"list","listType":"ul","items":["security: 期权代码；如security='10001979.XSHG' security='CU2001C42000.XSGE'#铜期权，上海期货交易所； security='SR003C5600.XZCE' #白糖期权，郑州商品交易所； security='M2005-P-2400.XDCE' #豆粕期权，大连商品交易所；","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"list","listType":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
    - {"type":"heading","level":5,"content":"期权tick返回结果"}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（手）","float"],["money","累计成交额","float"],["position","持仓量","float"],["a1_v","一档卖量","float"],["a1_p","一档卖价","float"],["b1_v","一档买量","float"],["b1_p","一档买价","float"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#获取PG2204-C-4300.XDCE期权合约在“2022-03-07”前8个时间单位的tick数据,start_dt和count只能有一个不为None值\ndf=get_ticks('PG2204-C-4300.XDCE',end_dt='2022-03-07',count=8)\nprint(df)\n\n                     time  current   high    low  volume    money  position  \\\n0 2021-07-09 13:38:43.228    649.8  649.8  627.6     2.0  25548.0       1.0   \n1 2021-07-16 13:52:32.956    583.2  583.2  583.2     1.0  11664.0       1.0   \n2 2021-08-12 13:37:10.824    699.8  699.8  699.8     1.0  13996.0       2.0   \n3 2021-08-24 13:35:48.156    550.6  550.6  550.6     1.0  11012.0       2.0   \n4 2021-12-22 14:23:37.476    411.8  411.8  411.8     1.0   8236.0       1.0   \n\n    a1_p  a1_v   b1_p  b1_v  \n0  682.8   2.0  645.4   1.0  \n1  603.2   1.0  570.4   2.0  \n2  702.2   1.0  660.4   1.0  \n3  587.8   1.0  556.4   1.0  \n4  431.2   1.0  411.2   1.0"}
  suggestedFilename: "doc_JQDatadoc_9995_overview_商品期权Ticks"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9995"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 商品期权Ticks

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9995

## 描述

描述

## 内容

#### 商品期权Ticks

- 历史范围：上市至今

```python
get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)
```

描述

- 支持商品期权tick数据，每0.5s一条数据，盘后15:00更新，24:00校对完成入。

购买

- 用户如有需要使用tick数据的，可添加**微信号JQData02**申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com

商品期权参数

- security: 期权代码；如security='10001979.XSHG' security='CU2001C42000.XSGE'#铜期权，上海期货交易所； security='SR003C5600.XZCE' #白糖期权，郑州商品交易所； security='M2005-P-2400.XDCE' #豆粕期权，大连商品交易所；
- start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'
- end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'
- count: 取出指定时间区间内前多少条的tick数据。
- fields: 选择要获取的行情数据字段，默认为None，返回结果如下：
- skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据
- df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray

- 同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据

###### 期权tick返回结果

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
#获取PG2204-C-4300.XDCE期权合约在“2022-03-07”前8个时间单位的tick数据,start_dt和count只能有一个不为None值
df=get_ticks('PG2204-C-4300.XDCE',end_dt='2022-03-07',count=8)
print(df)

                     time  current   high    low  volume    money  position  \
0 2021-07-09 13:38:43.228    649.8  649.8  627.6     2.0  25548.0       1.0   
1 2021-07-16 13:52:32.956    583.2  583.2  583.2     1.0  11664.0       1.0   
2 2021-08-12 13:37:10.824    699.8  699.8  699.8     1.0  13996.0       2.0   
3 2021-08-24 13:35:48.156    550.6  550.6  550.6     1.0  11012.0       2.0   
4 2021-12-22 14:23:37.476    411.8  411.8  411.8     1.0   8236.0       1.0   

    a1_p  a1_v   b1_p  b1_v  
0  682.8   2.0  645.4   1.0  
1  603.2   1.0  570.4   2.0  
2  702.2   1.0  660.4   1.0  
3  587.8   1.0  556.4   1.0  
4  431.2   1.0  411.2   1.0
```
