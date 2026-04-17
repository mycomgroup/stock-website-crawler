---
id: "url-36497ae2"
type: "website"
title: "限售解禁数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10021"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:45:07.475Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10021"
  headings:
    - {"level":3,"text":"限售解禁数据","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"ul","items":["获取指定日期区间内的限售解禁数据"]}
    - {"type":"ul","items":["stock_list: 一个股票代码的 list","start_date: 开始日期","end_date: 结束日期","forward_count: 交易日数量， 可以与 start_date 同时使用， 表示获取 start_date 到 forward_count 个交易日区间的数据"]}
    - {"type":"ul","items":["pandas.DataFrame， 各 column 的含义如下:","day: 解禁日期","code: 股票代码","num: 解禁股数","rate1: 解禁股数/总股本","rate2: 解禁股数/总流通股本"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_locked_shares(stock_list, start_date, end_date, forward_count)"}
    - {"language":"python","code":"# 在策略中获取个股未来500天的解禁情况\ndf=get_locked_shares(stock_list=['002345.XSHE', '603025.XSHG'], start_date='2020-07-20', forward_count=500)\nprint(df)\n          day         code         num   rate1   rate2\n0  2020-07-20  002345.XSHE  12060300.0  0.0083  0.0086\n1  2020-12-28  603025.XSHG   3561107.0  0.0038  0.0039\n2  2021-11-04  603025.XSHG   1263300.0  0.0014  0.0014"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"限售解禁数据"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_locked_shares(stock_list, start_date, end_date, forward_count)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取指定日期区间内的限售解禁数据"]}
    - {"type":"list","listType":"ul","items":["stock_list: 一个股票代码的 list","start_date: 开始日期","end_date: 结束日期","forward_count: 交易日数量， 可以与 start_date 同时使用， 表示获取 start_date 到 forward_count 个交易日区间的数据"]}
    - {"type":"list","listType":"ul","items":["pandas.DataFrame， 各 column 的含义如下:","day: 解禁日期","code: 股票代码","num: 解禁股数","rate1: 解禁股数/总股本","rate2: 解禁股数/总流通股本"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 在策略中获取个股未来500天的解禁情况\ndf=get_locked_shares(stock_list=['002345.XSHE', '603025.XSHG'], start_date='2020-07-20', forward_count=500)\nprint(df)\n          day         code         num   rate1   rate2\n0  2020-07-20  002345.XSHE  12060300.0  0.0083  0.0086\n1  2020-12-28  603025.XSHG   3561107.0  0.0038  0.0039\n2  2021-11-04  603025.XSHG   1263300.0  0.0014  0.0014"}
  suggestedFilename: "doc_JQDatadoc_10021_overview_限售解禁数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10021"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 限售解禁数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10021

## 描述

描述

## 内容

#### 限售解禁数据

- 历史范围：2005年至今；更新时间：交易日24:00更新

```python
get_locked_shares(stock_list, start_date, end_date, forward_count)
```

描述

- 获取指定日期区间内的限售解禁数据

- stock_list: 一个股票代码的 list
- start_date: 开始日期
- end_date: 结束日期
- forward_count: 交易日数量， 可以与 start_date 同时使用， 表示获取 start_date 到 forward_count 个交易日区间的数据

- pandas.DataFrame， 各 column 的含义如下:
- day: 解禁日期
- code: 股票代码
- num: 解禁股数
- rate1: 解禁股数/总股本
- rate2: 解禁股数/总流通股本

###### 示例

```python
# 在策略中获取个股未来500天的解禁情况
df=get_locked_shares(stock_list=['002345.XSHE', '603025.XSHG'], start_date='2020-07-20', forward_count=500)
print(df)
          day         code         num   rate1   rate2
0  2020-07-20  002345.XSHE  12060300.0  0.0083  0.0086
1  2020-12-28  603025.XSHG   3561107.0  0.0038  0.0039
2  2021-11-04  603025.XSHG   1263300.0  0.0014  0.0014
```
