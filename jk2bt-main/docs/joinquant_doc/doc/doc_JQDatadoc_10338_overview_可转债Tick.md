---
id: "url-36496f79"
type: "website"
title: "可转债Tick"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10338"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:45:58.672Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10338"
  headings:
    - {"level":3,"text":"可转债Tick","id":""}
    - {"level":5,"text":"可转债tick返回结果","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "可转债tick参数"
  lists:
    - {"type":"ul","items":["历史范围：2019年至今；更新时间：盘后15点"]}
    - {"type":"ul","items":["可转债部分， 支持2019年至今的tick数据，提供买五卖五数据，。每3秒一条数据，盘后15:00更新，24:00校对完成入库"]}
    - {"type":"ul","items":["用户如有需要使用tick数据的，可添加微信号JQData02申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"ul","items":["security: 标的代码,如 110043.XSHE","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（股）","float"],["money","累计成交额","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"language":"python","code":"# start_dt和count只能有一个不为None值\nd = get_ticks(\"110043.XSHG\",start_dt=None, end_dt=\"2023-02-03 10:43:00\", count=5)\nprint(d)\n\n#输出\n                     time  current     high     low   volume      money  \\\n0 2023-02-03 10:42:30.408  116.680  117.687  116.43  66290.0  7740472.0   \n1 2023-02-03 10:42:36.412  116.680  117.687  116.43  66330.0  7745139.0   \n2 2023-02-03 10:42:39.416  116.695  117.687  116.43  66340.0  7746306.0   \n3 2023-02-03 10:42:45.408  116.696  117.687  116.43  66500.0  7764977.0   \n4 2023-02-03 10:42:48.408  116.705  117.687  116.43  66510.0  7766144.0   \n\n      a1_p  a1_v     a2_p  a2_v     a3_p  a3_v     a4_p    a4_v     a5_p  \\\n0  116.680  30.0  116.695  10.0  116.705  10.0  116.739    20.0  116.740   \n1  116.705  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   \n2  116.696  60.0  116.705  10.0  116.739  20.0  116.740    10.0  116.744   \n3  116.705  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   \n4  116.706  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   \n\n     a5_v     b1_p   b1_v     b2_p   b2_v     b3_p  b3_v    b4_p  b4_v  \\\n0    10.0  116.662  110.0  116.658   10.0  116.640  10.0  116.61  10.0   \n1    10.0  116.695  160.0  116.662  260.0  116.658  10.0  116.64  10.0   \n2  1960.0  116.695  300.0  116.662  110.0  116.658  10.0  116.64  10.0   \n3    10.0  116.695  200.0  116.662  110.0  116.658  10.0  116.64  10.0   \n4    10.0  116.695  200.0  116.662  110.0  116.658  10.0  116.64  10.0   \n\n     b5_p   b5_v  \n0  116.60  310.0  \n1  116.61   10.0  \n2  116.61   10.0  \n3  116.61   10.0  \n4  116.61   10.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"可转债Tick"}
    - {"type":"list","listType":"ul","items":["历史范围：2019年至今；更新时间：盘后15点"]}
    - {"type":"codeblock","language":"python","content":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["可转债部分， 支持2019年至今的tick数据，提供买五卖五数据，。每3秒一条数据，盘后15:00更新，24:00校对完成入库"]}
    - {"type":"list","listType":"ul","items":["用户如有需要使用tick数据的，可添加微信号JQData02申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"paragraph","content":"可转债tick参数"}
    - {"type":"list","listType":"ul","items":["security: 标的代码,如 110043.XSHE","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"list","listType":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
    - {"type":"heading","level":5,"content":"可转债tick返回结果"}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（股）","float"],["money","累计成交额","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# start_dt和count只能有一个不为None值\nd = get_ticks(\"110043.XSHG\",start_dt=None, end_dt=\"2023-02-03 10:43:00\", count=5)\nprint(d)\n\n#输出\n                     time  current     high     low   volume      money  \\\n0 2023-02-03 10:42:30.408  116.680  117.687  116.43  66290.0  7740472.0   \n1 2023-02-03 10:42:36.412  116.680  117.687  116.43  66330.0  7745139.0   \n2 2023-02-03 10:42:39.416  116.695  117.687  116.43  66340.0  7746306.0   \n3 2023-02-03 10:42:45.408  116.696  117.687  116.43  66500.0  7764977.0   \n4 2023-02-03 10:42:48.408  116.705  117.687  116.43  66510.0  7766144.0   \n\n      a1_p  a1_v     a2_p  a2_v     a3_p  a3_v     a4_p    a4_v     a5_p  \\\n0  116.680  30.0  116.695  10.0  116.705  10.0  116.739    20.0  116.740   \n1  116.705  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   \n2  116.696  60.0  116.705  10.0  116.739  20.0  116.740    10.0  116.744   \n3  116.705  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   \n4  116.706  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   \n\n     a5_v     b1_p   b1_v     b2_p   b2_v     b3_p  b3_v    b4_p  b4_v  \\\n0    10.0  116.662  110.0  116.658   10.0  116.640  10.0  116.61  10.0   \n1    10.0  116.695  160.0  116.662  260.0  116.658  10.0  116.64  10.0   \n2  1960.0  116.695  300.0  116.662  110.0  116.658  10.0  116.64  10.0   \n3    10.0  116.695  200.0  116.662  110.0  116.658  10.0  116.64  10.0   \n4    10.0  116.695  200.0  116.662  110.0  116.658  10.0  116.64  10.0   \n\n     b5_p   b5_v  \n0  116.60  310.0  \n1  116.61   10.0  \n2  116.61   10.0  \n3  116.61   10.0  \n4  116.61   10.0"}
  suggestedFilename: "doc_JQDatadoc_10338_overview_可转债Tick"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10338"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 可转债Tick

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10338

## 描述

描述

## 内容

#### 可转债Tick

- 历史范围：2019年至今；更新时间：盘后15点

```python
get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)
```

描述

- 可转债部分， 支持2019年至今的tick数据，提供买五卖五数据，。每3秒一条数据，盘后15:00更新，24:00校对完成入库

- 用户如有需要使用tick数据的，可添加微信号JQData02申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com

可转债tick参数

- security: 标的代码,如 110043.XSHE
- start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'
- end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'
- count: 取出指定时间区间内前多少条的tick数据。
- fields: 选择要获取的行情数据字段，默认为None，返回结果如下：
- skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据
- df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray

- 同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据

###### 可转债tick返回结果

| 字段名 | 说明 | 字段类型 |
| --- | --- | --- |
| time | 时间 | datetime |
| current | 当前价 | float |
| high | 当日最高价 | float |
| low | 当日最低价 | float |
| volume | 累计成交量（股） | float |
| money | 累计成交额 | float |
| a1_v~a5_v | 五档卖量 | float |
| a1_p~a5_p | 五档卖价 | float |
| b1_v~b5_v | 五档买量 | float |
| b1_p~b5_p | 五档买价 | float |

###### 示例：

```python
# start_dt和count只能有一个不为None值
d = get_ticks("110043.XSHG",start_dt=None, end_dt="2023-02-03 10:43:00", count=5)
print(d)

#输出
                     time  current     high     low   volume      money  \
0 2023-02-03 10:42:30.408  116.680  117.687  116.43  66290.0  7740472.0   
1 2023-02-03 10:42:36.412  116.680  117.687  116.43  66330.0  7745139.0   
2 2023-02-03 10:42:39.416  116.695  117.687  116.43  66340.0  7746306.0   
3 2023-02-03 10:42:45.408  116.696  117.687  116.43  66500.0  7764977.0   
4 2023-02-03 10:42:48.408  116.705  117.687  116.43  66510.0  7766144.0   

      a1_p  a1_v     a2_p  a2_v     a3_p  a3_v     a4_p    a4_v     a5_p  \
0  116.680  30.0  116.695  10.0  116.705  10.0  116.739    20.0  116.740   
1  116.705  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   
2  116.696  60.0  116.705  10.0  116.739  20.0  116.740    10.0  116.744   
3  116.705  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   
4  116.706  10.0  116.739  20.0  116.740  10.0  116.744  1960.0  116.750   

     a5_v     b1_p   b1_v     b2_p   b2_v     b3_p  b3_v    b4_p  b4_v  \
0    10.0  116.662  110.0  116.658   10.0  116.640  10.0  116.61  10.0   
1    10.0  116.695  160.0  116.662  260.0  116.658  10.0  116.64  10.0   
2  1960.0  116.695  300.0  116.662  110.0  116.658  10.0  116.64  10.0   
3    10.0  116.695  200.0  116.662  110.0  116.658  10.0  116.64  10.0   
4    10.0  116.695  200.0  116.662  110.0  116.658  10.0  116.64  10.0   

     b5_p   b5_v  
0  116.60  310.0  
1  116.61   10.0  
2  116.61   10.0  
3  116.61   10.0  
4  116.61   10.0
```
