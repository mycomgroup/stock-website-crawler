---
id: "url-7a226eb1"
type: "website"
title: "获取场内基金集合竞价"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9943"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:21:07.702Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9943"
  headings:
    - {"level":3,"text":"获取场内基金集合竞价","id":""}
    - {"level":5,"text":"返回值：","id":""}
  paragraphs:
    - "描述"
    - "基金集合竞价"
  lists:
    - {"type":"ul","items":["历史范围：2017-01-01至今；"]}
    - {"type":"ul","items":["支持场内基金（2019年至今）的集合竞价，当日的集合竞价数据于盘后15点返回。","为了防止返回数据量过大, 我们每次最多返回10000行。"]}
    - {"type":"ul","items":["security: 场内基金（2019年至今）","start_date: 开始日期，YYYY-MM-DD格式","end_date: 结束日期，YYYY-MM-DD格式","fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。"]}
    - {"type":"ul","items":["返回指定时间区间标的集合竞价tick数据，返回字段结果如下："]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价（不复权）","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_call_auction(security, start_date, end_date, fields=None)"}
    - {"language":"python","code":"#获取159003.XSHE招商快线2019-3-05至2019-3-06期间的集合竞价数据\ndf=get_call_auction('159003.XSHE','2019-3-05','2019-3-06')\nprint(df)\n\n          code                time  current   volume      money   a1_p  \\\n0  159003.XSHE 2019-03-05 09:25:03    100.0  16300.0  1629951.1  100.0   \n1  159003.XSHE 2019-03-06 09:25:03    100.0  29300.0  2929941.4  100.0   \n\n      a1_v   a2_p     a2_v   a3_p   ...     b1_p    b1_v    b2_p    b2_v  \\\n0  19412.0  100.0  21915.0  100.0   ...    100.0  1500.0   99.99  5300.0   \n1   9199.0  100.0  49813.0  100.0   ...    100.0   300.0  100.00   500.0   \n\n     b3_p    b3_v   b4_p    b4_v   b5_p    b5_v  \n0   99.99   900.0  99.99  3000.0  99.99  1000.0  \n1  100.00  1200.0  99.99  6500.0  99.99  9400.0  \n\n[2 rows x 25 columns]"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取场内基金集合竞价"}
    - {"type":"list","listType":"ul","items":["历史范围：2017-01-01至今；"]}
    - {"type":"codeblock","language":"python","content":"get_call_auction(security, start_date, end_date, fields=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["支持场内基金（2019年至今）的集合竞价，当日的集合竞价数据于盘后15点返回。","为了防止返回数据量过大, 我们每次最多返回10000行。"]}
    - {"type":"paragraph","content":"基金集合竞价"}
    - {"type":"list","listType":"ul","items":["security: 场内基金（2019年至今）","start_date: 开始日期，YYYY-MM-DD格式","end_date: 结束日期，YYYY-MM-DD格式","fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。"]}
    - {"type":"heading","level":5,"content":"返回值："}
    - {"type":"list","listType":"ul","items":["返回指定时间区间标的集合竞价tick数据，返回字段结果如下："]}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价（不复权）","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
    - {"type":"codeblock","language":"python","content":"#获取159003.XSHE招商快线2019-3-05至2019-3-06期间的集合竞价数据\ndf=get_call_auction('159003.XSHE','2019-3-05','2019-3-06')\nprint(df)\n\n          code                time  current   volume      money   a1_p  \\\n0  159003.XSHE 2019-03-05 09:25:03    100.0  16300.0  1629951.1  100.0   \n1  159003.XSHE 2019-03-06 09:25:03    100.0  29300.0  2929941.4  100.0   \n\n      a1_v   a2_p     a2_v   a3_p   ...     b1_p    b1_v    b2_p    b2_v  \\\n0  19412.0  100.0  21915.0  100.0   ...    100.0  1500.0   99.99  5300.0   \n1   9199.0  100.0  49813.0  100.0   ...    100.0   300.0  100.00   500.0   \n\n     b3_p    b3_v   b4_p    b4_v   b5_p    b5_v  \n0   99.99   900.0  99.99  3000.0  99.99  1000.0  \n1  100.00  1200.0  99.99  6500.0  99.99  9400.0  \n\n[2 rows x 25 columns]"}
  suggestedFilename: "doc_JQDatadoc_9943_overview_获取场内基金集合竞价"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9943"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取场内基金集合竞价

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9943

## 描述

描述

## 内容

#### 获取场内基金集合竞价

- 历史范围：2017-01-01至今；

```python
get_call_auction(security, start_date, end_date, fields=None)
```

描述

- 支持场内基金（2019年至今）的集合竞价，当日的集合竞价数据于盘后15点返回。
- 为了防止返回数据量过大, 我们每次最多返回10000行。

基金集合竞价

- security: 场内基金（2019年至今）
- start_date: 开始日期，YYYY-MM-DD格式
- end_date: 结束日期，YYYY-MM-DD格式
- fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。

###### 返回值：

- 返回指定时间区间标的集合竞价tick数据，返回字段结果如下：

| 字段名 | 说明 | 字段类型 |
| --- | --- | --- |
| time | 时间 | datetime |
| current | 当前价（不复权） | float |
| volume | 累计成交量（股） | float |
| money | 累计成交额（元） | float |
| a1_v~a5_v | 五档卖量 | float |
| a1_p~a5_p | 五档卖价 | float |
| b1_v~b5_v | 五档买量 | float |
| b1_p~b5_p | 五档买价 | float |

```python
#获取159003.XSHE招商快线2019-3-05至2019-3-06期间的集合竞价数据
df=get_call_auction('159003.XSHE','2019-3-05','2019-3-06')
print(df)

          code                time  current   volume      money   a1_p  \
0  159003.XSHE 2019-03-05 09:25:03    100.0  16300.0  1629951.1  100.0   
1  159003.XSHE 2019-03-06 09:25:03    100.0  29300.0  2929941.4  100.0   

      a1_v   a2_p     a2_v   a3_p   ...     b1_p    b1_v    b2_p    b2_v  \
0  19412.0  100.0  21915.0  100.0   ...    100.0  1500.0   99.99  5300.0   
1   9199.0  100.0  49813.0  100.0   ...    100.0   300.0  100.00   500.0   

     b3_p    b3_v   b4_p    b4_v   b5_p    b5_v  
0   99.99   900.0  99.99  3000.0  99.99  1000.0  
1  100.00  1200.0  99.99  6500.0  99.99  9400.0  

[2 rows x 25 columns]
```
