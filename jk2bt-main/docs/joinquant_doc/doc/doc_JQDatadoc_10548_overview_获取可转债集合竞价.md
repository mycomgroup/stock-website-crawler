---
id: "url-364967d8"
type: "website"
title: "获取可转债集合竞价"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10548"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:47:17.530Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10548"
  headings:
    - {"level":3,"text":"获取可转债集合竞价","id":""}
    - {"level":5,"text":"返回值：","id":"-1"}
  paragraphs:
    - "描述"
    - "可转债集合竞价"
  lists:
    - {"type":"ul","items":["历史范围：2019年至今；更新时间：盘后15点"]}
    - {"type":"ul","items":["支持可转债的集合竞价，当日的集合竞价数据于盘后15点返回。","为了防止返回数据量过大, 我们每次最多返回5000行。"]}
    - {"type":"ul","items":["security: 可转债","start_date: 开始日期，YYYY-MM-DD格式","end_date: 结束日期，YYYY-MM-DD格式","fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。"]}
    - {"type":"ul","items":["返回指定时间区间标的集合竞价tick数据，返回字段结果如下："]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_call_auction(security, start_date, end_date, fields=None)"}
    - {"language":"python","code":"#获取110043.XSHG可转债2023-08-08至2023-8-09期间的集合竞价数据\ndf=get_call_auction('110043.XSHG','2023-08-08','2023-08-09')\nprint(df)\n\n          code                time  current  volume    money    a1_p   a1_v  \\\n0  110043.XSHG 2023-08-08 09:25:02   112.81   120.0  13537.0  112.81  630.0   \n1  110043.XSHG 2023-08-09 09:25:01   112.20   130.0  14586.0  112.20  270.0   \n\n     a2_p   a2_v     a3_p  ...       b1_p  b1_v   b2_p  b2_v    b3_p  b3_v  \\\n0  113.09   10.0  113.188  ...    112.788  20.0  112.6  10.0  112.51  10.0   \n1  112.27  640.0  112.370  ...    111.988  20.0  111.9  90.0  111.89  10.0   \n\n      b4_p  b4_v   b5_p   b5_v  \n0  112.500  10.0  112.4  200.0  \n1  111.707  80.0  111.6   10.0  \n\n[2 rows x 25 columns]"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取可转债集合竞价"}
    - {"type":"list","listType":"ul","items":["历史范围：2019年至今；更新时间：盘后15点"]}
    - {"type":"codeblock","language":"python","content":"get_call_auction(security, start_date, end_date, fields=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["支持可转债的集合竞价，当日的集合竞价数据于盘后15点返回。","为了防止返回数据量过大, 我们每次最多返回5000行。"]}
    - {"type":"paragraph","content":"可转债集合竞价"}
    - {"type":"list","listType":"ul","items":["security: 可转债","start_date: 开始日期，YYYY-MM-DD格式","end_date: 结束日期，YYYY-MM-DD格式","fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。"]}
    - {"type":"heading","level":5,"content":"返回值："}
    - {"type":"list","listType":"ul","items":["返回指定时间区间标的集合竞价tick数据，返回字段结果如下："]}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
    - {"type":"codeblock","language":"python","content":"#获取110043.XSHG可转债2023-08-08至2023-8-09期间的集合竞价数据\ndf=get_call_auction('110043.XSHG','2023-08-08','2023-08-09')\nprint(df)\n\n          code                time  current  volume    money    a1_p   a1_v  \\\n0  110043.XSHG 2023-08-08 09:25:02   112.81   120.0  13537.0  112.81  630.0   \n1  110043.XSHG 2023-08-09 09:25:01   112.20   130.0  14586.0  112.20  270.0   \n\n     a2_p   a2_v     a3_p  ...       b1_p  b1_v   b2_p  b2_v    b3_p  b3_v  \\\n0  113.09   10.0  113.188  ...    112.788  20.0  112.6  10.0  112.51  10.0   \n1  112.27  640.0  112.370  ...    111.988  20.0  111.9  90.0  111.89  10.0   \n\n      b4_p  b4_v   b5_p   b5_v  \n0  112.500  10.0  112.4  200.0  \n1  111.707  80.0  111.6   10.0  \n\n[2 rows x 25 columns]"}
  suggestedFilename: "doc_JQDatadoc_10548_overview_获取可转债集合竞价"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10548"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取可转债集合竞价

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10548

## 描述

描述

## 内容

#### 获取可转债集合竞价

- 历史范围：2019年至今；更新时间：盘后15点

```python
get_call_auction(security, start_date, end_date, fields=None)
```

描述

- 支持可转债的集合竞价，当日的集合竞价数据于盘后15点返回。
- 为了防止返回数据量过大, 我们每次最多返回5000行。

可转债集合竞价

- security: 可转债
- start_date: 开始日期，YYYY-MM-DD格式
- end_date: 结束日期，YYYY-MM-DD格式
- fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。

###### 返回值：

- 返回指定时间区间标的集合竞价tick数据，返回字段结果如下：

| 字段名 | 说明 | 字段类型 |
| --- | --- | --- |
| time | 时间 | datetime |
| current | 当前价 | float |
| volume | 累计成交量（股） | float |
| money | 累计成交额（元） | float |
| a1_v~a5_v | 五档卖量 | float |
| a1_p~a5_p | 五档卖价 | float |
| b1_v~b5_v | 五档买量 | float |
| b1_p~b5_p | 五档买价 | float |

```python
#获取110043.XSHG可转债2023-08-08至2023-8-09期间的集合竞价数据
df=get_call_auction('110043.XSHG','2023-08-08','2023-08-09')
print(df)

          code                time  current  volume    money    a1_p   a1_v  \
0  110043.XSHG 2023-08-08 09:25:02   112.81   120.0  13537.0  112.81  630.0   
1  110043.XSHG 2023-08-09 09:25:01   112.20   130.0  14586.0  112.20  270.0   

     a2_p   a2_v     a3_p  ...       b1_p  b1_v   b2_p  b2_v    b3_p  b3_v  \
0  113.09   10.0  113.188  ...    112.788  20.0  112.6  10.0  112.51  10.0   
1  112.27  640.0  112.370  ...    111.988  20.0  111.9  90.0  111.89  10.0   

      b4_p  b4_v   b5_p   b5_v  
0  112.500  10.0  112.4  200.0  
1  111.707  80.0  111.6   10.0  

[2 rows x 25 columns]
```
