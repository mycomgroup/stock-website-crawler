---
id: "url-36497b1f"
type: "website"
title: "指数Tick"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10002"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:44:28.132Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10002"
  headings:
    - {"level":3,"text":"指数Tick","id":"tick"}
    - {"level":5,"text":"测试：可联系微信号jqdata02，递交名片申请试用【具体权限可点击查看】","id":"jqdata02httpsdocsqqcomsheetdrvvxsnvaum9kvgzstabbb08j2"}
    - {"level":5,"text":"指数tick返回结果","id":"tick-1"}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "购买"
    - "指数tick参数"
  lists:
    - {"type":"ul","items":["历史范围：2017年至今；"]}
    - {"type":"ul","items":["指数部分,支持 2017-01-01 至今的tick数据。每3秒一条数据，盘后15:00更新，24:00校对完成入库 。"]}
    - {"type":"ul","items":["用户如有需要使用tick数据的，可添加微信号JQData02申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"ul","items":["security: 指数代码；","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"language":"python","code":"# 获取上证指数2019-11-19 10:00:00 到 2019-11-19 10:01:00的tick数据\ndf=get_ticks('000001.XSHG','2019-11-19 10:00:00','2019-11-19 10:01:00')\nprint(df)\n                      time    current       high       low        volume  \\\n0  2019-11-19 10:00:01.608  2913.4288  2914.6199  2902.855  2.795233e+09   \n1  2019-11-19 10:00:06.600  2913.1890  2914.6199  2902.855  2.800322e+09   \n2  2019-11-19 10:00:10.628  2913.0532  2914.6199  2902.855  2.807082e+09   \n3  2019-11-19 10:00:16.608  2913.3964  2914.6199  2902.855  2.814624e+09   \n4  2019-11-19 10:00:21.620  2913.2224  2914.6199  2902.855  2.818837e+09   \n5  2019-11-19 10:00:25.620  2913.6741  2914.6199  2902.855  2.824412e+09   \n6  2019-11-19 10:00:31.608  2912.6091  2914.6199  2902.855  2.830766e+09   \n7  2019-11-19 10:00:36.588  2913.6492  2914.6199  2902.855  2.835326e+09   \n8  2019-11-19 10:00:40.620  2913.5004  2914.6199  2902.855  2.840942e+09   \n9  2019-11-19 10:00:46.580  2913.7269  2914.6199  2902.855  2.846658e+09   \n10 2019-11-19 10:00:51.588  2913.7699  2914.6199  2902.855  2.850605e+09   \n11 2019-11-19 10:00:55.608  2913.9637  2914.6199  2902.855  2.856479e+09   \n\n           money  \n0   3.171538e+10  \n1   3.178079e+10  \n2   3.185376e+10  \n3   3.193569e+10  \n4   3.198723e+10  \n5   3.204712e+10  \n6   3.212560e+10  \n7   3.217697e+10  \n8   3.224518e+10  \n9   3.231385e+10  \n10  3.236239e+10  \n11  3.242965e+10  \n​"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"指数Tick"}
    - {"type":"list","listType":"ul","items":["历史范围：2017年至今；"]}
    - {"type":"heading","level":5,"content":"测试：可联系微信号jqdata02，递交名片申请试用【具体权限可点击查看】"}
    - {"type":"codeblock","language":"python","content":"get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["指数部分,支持 2017-01-01 至今的tick数据。每3秒一条数据，盘后15:00更新，24:00校对完成入库 。"]}
    - {"type":"paragraph","content":"购买"}
    - {"type":"list","listType":"ul","items":["用户如有需要使用tick数据的，可添加微信号JQData02申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com"]}
    - {"type":"paragraph","content":"指数tick参数"}
    - {"type":"list","listType":"ul","items":["security: 指数代码；","start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'","end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'","count: 取出指定时间区间内前多少条的tick数据。","fields: 选择要获取的行情数据字段，默认为None，返回结果如下：","skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据","df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray"]}
    - {"type":"list","listType":"ul","items":["同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据"]}
    - {"type":"heading","level":5,"content":"指数tick返回结果"}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["high","当日最高价","float"],["low","当日最低价","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 获取上证指数2019-11-19 10:00:00 到 2019-11-19 10:01:00的tick数据\ndf=get_ticks('000001.XSHG','2019-11-19 10:00:00','2019-11-19 10:01:00')\nprint(df)\n                      time    current       high       low        volume  \\\n0  2019-11-19 10:00:01.608  2913.4288  2914.6199  2902.855  2.795233e+09   \n1  2019-11-19 10:00:06.600  2913.1890  2914.6199  2902.855  2.800322e+09   \n2  2019-11-19 10:00:10.628  2913.0532  2914.6199  2902.855  2.807082e+09   \n3  2019-11-19 10:00:16.608  2913.3964  2914.6199  2902.855  2.814624e+09   \n4  2019-11-19 10:00:21.620  2913.2224  2914.6199  2902.855  2.818837e+09   \n5  2019-11-19 10:00:25.620  2913.6741  2914.6199  2902.855  2.824412e+09   \n6  2019-11-19 10:00:31.608  2912.6091  2914.6199  2902.855  2.830766e+09   \n7  2019-11-19 10:00:36.588  2913.6492  2914.6199  2902.855  2.835326e+09   \n8  2019-11-19 10:00:40.620  2913.5004  2914.6199  2902.855  2.840942e+09   \n9  2019-11-19 10:00:46.580  2913.7269  2914.6199  2902.855  2.846658e+09   \n10 2019-11-19 10:00:51.588  2913.7699  2914.6199  2902.855  2.850605e+09   \n11 2019-11-19 10:00:55.608  2913.9637  2914.6199  2902.855  2.856479e+09   \n\n           money  \n0   3.171538e+10  \n1   3.178079e+10  \n2   3.185376e+10  \n3   3.193569e+10  \n4   3.198723e+10  \n5   3.204712e+10  \n6   3.212560e+10  \n7   3.217697e+10  \n8   3.224518e+10  \n9   3.231385e+10  \n10  3.236239e+10  \n11  3.242965e+10  \n​"}
  suggestedFilename: "doc_JQDatadoc_10002_overview_指数Tick"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10002"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 指数Tick

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10002

## 描述

描述

## 内容

#### 指数Tick

- 历史范围：2017年至今；

###### 测试：可联系微信号jqdata02，递交名片申请试用【具体权限可点击查看】

```python
get_ticks(security, start_dt, end_dt, count, fields, skip=True,df=True)
```

描述

- 指数部分,支持 2017-01-01 至今的tick数据。每3秒一条数据，盘后15:00更新，24:00校对完成入库 。

购买

- 用户如有需要使用tick数据的，可添加微信号JQData02申请试用或咨询开通，或发送邮件至jqdatasdk@joinquant.com

指数tick参数

- security: 指数代码；
- start_dt: 开始日期，格式为'YYYY-MM-DD HH:MM:SS'
- end_dt: 结束日期，格式为'YYYY-MM-DD HH:MM:SS'
- count: 取出指定时间区间内前多少条的tick数据。
- fields: 选择要获取的行情数据字段，默认为None，返回结果如下：
- skip:默认为True，过滤掉无成交变化的tick数据；当指定skip=False时，返回的tick数据会保留无成交有盘口变化的tick数据
- df:指定返回的数据格式，默认为True，返回dataframe；df=False时返回一个np.ndarray

- 同时填入start_dt、end_dt和count参数的应用场景：比如取近1分钟30条数据

###### 指数tick返回结果

| 字段名 | 说明 | 字段类型 |
| --- | --- | --- |
| time | 时间 | datetime |
| current | 当前价 | float |
| high | 当日最高价 | float |
| low | 当日最低价 | float |
| volume | 累计成交量（股） | float |
| money | 累计成交额（元） | float |

###### 示例：

```python
# 获取上证指数2019-11-19 10:00:00 到 2019-11-19 10:01:00的tick数据
df=get_ticks('000001.XSHG','2019-11-19 10:00:00','2019-11-19 10:01:00')
print(df)
                      time    current       high       low        volume  \
0  2019-11-19 10:00:01.608  2913.4288  2914.6199  2902.855  2.795233e+09   
1  2019-11-19 10:00:06.600  2913.1890  2914.6199  2902.855  2.800322e+09   
2  2019-11-19 10:00:10.628  2913.0532  2914.6199  2902.855  2.807082e+09   
3  2019-11-19 10:00:16.608  2913.3964  2914.6199  2902.855  2.814624e+09   
4  2019-11-19 10:00:21.620  2913.2224  2914.6199  2902.855  2.818837e+09   
5  2019-11-19 10:00:25.620  2913.6741  2914.6199  2902.855  2.824412e+09   
6  2019-11-19 10:00:31.608  2912.6091  2914.6199  2902.855  2.830766e+09   
7  2019-11-19 10:00:36.588  2913.6492  2914.6199  2902.855  2.835326e+09   
8  2019-11-19 10:00:40.620  2913.5004  2914.6199  2902.855  2.840942e+09   
9  2019-11-19 10:00:46.580  2913.7269  2914.6199  2902.855  2.846658e+09   
10 2019-11-19 10:00:51.588  2913.7699  2914.6199  2902.855  2.850605e+09   
11 2019-11-19 10:00:55.608  2913.9637  2914.6199  2902.855  2.856479e+09   

           money  
0   3.171538e+10  
1   3.178079e+10  
2   3.185376e+10  
3   3.193569e+10  
4   3.198723e+10  
5   3.204712e+10  
6   3.212560e+10  
7   3.217697e+10  
8   3.224518e+10  
9   3.231385e+10  
10  3.236239e+10  
11  3.242965e+10  

```
