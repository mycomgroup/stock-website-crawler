---
id: "url-36496f9a"
type: "website"
title: "获取多个季度/年度的历史财务数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10326"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:29:56.434Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10326"
  headings:
    - {"level":3,"text":"获取多个季度/年度的历史财务数据","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "query函数的使用技巧"
  lists:
    - {"type":"ul","items":["获取多个季度/年度的三大财务报表和财务指标数据. 可指定单季度数据, 也可以指定年度数据。可以指定观察日期, 也可以指定最后一个报告期的结束日期"]}
    - {"type":"ul","items":["security：股票代码或者股票代码列表。","fields：要查询的财务数据的列表, 季度数据和年度数据可选择的列不同。","watch_date：观察日期, 如果指定, 将返回 watch_date 日期前(包含该日期)发布的报表数据","stat_date：统计日期, 可以是 '2019'/'2019q1'/'2018q4' 格式, 如果指定, 将返回 stat_date 对应报告期及之前的历史报告期的报表数据","count：查询历史的多个报告期时, 指定的报告期数量. 如果股票历史报告期的数量小于 count, 则该股票返回的数据行数将小于 count","interval：查询多个报告期数据时, 指定报告期间隔, 可选值: '1q'/'1y', 表示间隔一季度或者一年, 举例说明:","stat_by_year：bool, 是否返回年度数据. 默认返回的按季度统计的数据(比如income表中只有单个季度的利润)."]}
    - {"type":"ul","items":["pandas.DataFrame, 数据库查询结果. 数据格式同 get_fundamentals. 每个股票每个报告期(一季度或者一年)的数据占用一行.","不支持valuation市值表","推荐用户对结果使用pandas的groupby方法来进行分组分析数据","为了防止返回数据量过大, 我们每次最多返回10000行","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_history_fundamentals(security, fields, watch_date=None, stat_date=None, count=1, interval='1q', stat_by_year=False)"}
    - {"language":"python","code":"from jqdatasdk import *\nsecurity = ['000001.XSHE', '600000.XSHG']\ndf = get_history_fundamentals(security, fields=[balance.cash_equivalents, \n        cash_flow.net_deposit_increase, income.total_operating_revenue], \n        watch_date=None, stat_date='2019q1', count=5, interval='1q', stat_by_year=False)\nprint(df)\nprint(df.groupby('code').mean())"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取多个季度/年度的历史财务数据"}
    - {"type":"codeblock","language":"python","content":"get_history_fundamentals(security, fields, watch_date=None, stat_date=None, count=1, interval='1q', stat_by_year=False)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取多个季度/年度的三大财务报表和财务指标数据. 可指定单季度数据, 也可以指定年度数据。可以指定观察日期, 也可以指定最后一个报告期的结束日期"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["security：股票代码或者股票代码列表。","fields：要查询的财务数据的列表, 季度数据和年度数据可选择的列不同。","watch_date：观察日期, 如果指定, 将返回 watch_date 日期前(包含该日期)发布的报表数据","stat_date：统计日期, 可以是 '2019'/'2019q1'/'2018q4' 格式, 如果指定, 将返回 stat_date 对应报告期及之前的历史报告期的报表数据","count：查询历史的多个报告期时, 指定的报告期数量. 如果股票历史报告期的数量小于 count, 则该股票返回的数据行数将小于 count","interval：查询多个报告期数据时, 指定报告期间隔, 可选值: '1q'/'1y', 表示间隔一季度或者一年, 举例说明:","stat_by_year：bool, 是否返回年度数据. 默认返回的按季度统计的数据(比如income表中只有单个季度的利润)."]}
    - {"type":"list","listType":"ul","items":["pandas.DataFrame, 数据库查询结果. 数据格式同 get_fundamentals. 每个股票每个报告期(一季度或者一年)的数据占用一行.","不支持valuation市值表","推荐用户对结果使用pandas的groupby方法来进行分组分析数据","为了防止返回数据量过大, 我们每次最多返回10000行","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"paragraph","content":"query函数的使用技巧"}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\nsecurity = ['000001.XSHE', '600000.XSHG']\ndf = get_history_fundamentals(security, fields=[balance.cash_equivalents, \n        cash_flow.net_deposit_increase, income.total_operating_revenue], \n        watch_date=None, stat_date='2019q1', count=5, interval='1q', stat_by_year=False)\nprint(df)\nprint(df.groupby('code').mean())"}
  suggestedFilename: "doc_JQDatadoc_10326_overview_获取多个季度_年度的历史财务数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10326"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取多个季度/年度的历史财务数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10326

## 描述

描述

## 内容

#### 获取多个季度/年度的历史财务数据

```python
get_history_fundamentals(security, fields, watch_date=None, stat_date=None, count=1, interval='1q', stat_by_year=False)
```

描述

- 获取多个季度/年度的三大财务报表和财务指标数据. 可指定单季度数据, 也可以指定年度数据。可以指定观察日期, 也可以指定最后一个报告期的结束日期

参数

- security：股票代码或者股票代码列表。
- fields：要查询的财务数据的列表, 季度数据和年度数据可选择的列不同。
- watch_date：观察日期, 如果指定, 将返回 watch_date 日期前(包含该日期)发布的报表数据
- stat_date：统计日期, 可以是 '2019'/'2019q1'/'2018q4' 格式, 如果指定, 将返回 stat_date 对应报告期及之前的历史报告期的报表数据
- count：查询历史的多个报告期时, 指定的报告期数量. 如果股票历史报告期的数量小于 count, 则该股票返回的数据行数将小于 count
- interval：查询多个报告期数据时, 指定报告期间隔, 可选值: '1q'/'1y', 表示间隔一季度或者一年, 举例说明:
- stat_by_year：bool, 是否返回年度数据. 默认返回的按季度统计的数据(比如income表中只有单个季度的利润).

- pandas.DataFrame, 数据库查询结果. 数据格式同 get_fundamentals. 每个股票每个报告期(一季度或者一年)的数据占用一行.
- 不支持valuation市值表
- 推荐用户对结果使用pandas的groupby方法来进行分组分析数据
- 为了防止返回数据量过大, 我们每次最多返回10000行
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

query函数的使用技巧

- query函数的更多用法详见：query简易教程

###### 示例

```python
from jqdatasdk import *
security = ['000001.XSHE', '600000.XSHG']
df = get_history_fundamentals(security, fields=[balance.cash_equivalents, 
        cash_flow.net_deposit_increase, income.total_operating_revenue], 
        watch_date=None, stat_date='2019q1', count=5, interval='1q', stat_by_year=False)
print(df)
print(df.groupby('code').mean())
```
