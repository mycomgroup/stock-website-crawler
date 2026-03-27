---
id: "url-7a226eaf"
type: "website"
title: "货币基金收益日报"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9941"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:20:59.816Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9941"
  headings:
    - {"level":3,"text":"货币基金收益日报","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "货币基金收益日报信息"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"ul","items":["货币基金收益日报"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.FUND_MF_DAILY_PROFIT)表示从finance.FUND_MF_DAILY_PROFIT这张表中查询货币基金收益日报数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_MF_DAILY_PROFIT：收录了货币基金收益日报数据，表结构和字段信息如下：","filter(finance.FUND_MF_DAILY_PROFIT.code==code)：指定筛选条件，通过finance.FUND_MF_DAILY_PROFIT.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段","名称","类型"],"rows":[["code","基金代码","varchar(12)"],["name","基金名称","varchar(80)"],["end_date","收益日期","date"],["weekly_yield","7日年化收益率(%)","decimal(10,4)"],["daily_profit","每万份基金单位当日收益(元)","decimal(10,4)"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_MF_DAILY_PROFIT).filter(finance.FUND_MF_DAILY_PROFIT.code==code).limit(n))"}
    - {"language":"python","code":"#查询汇添富现金宝(\"000330\")货币基金收益日报数据，只显示5条信息。\nfrom jqdatasdk import finance\ndf=finance.run_query(query(finance.FUND_MF_DAILY_PROFIT).filter(finance.FUND_MF_DAILY_PROFIT.code=='000330').order_by(finance.FUND_MF_DAILY_PROFIT.end_date.desc()).limit(5))\nprint(df)\n\n        id    code            name    end_date  weekly_yield  daily_profit\n0  1742123  000330  汇添富现金宝货币市场基金A类  2021-03-17         2.165        0.5857\n1  1741454  000330  汇添富现金宝货币市场基金A类  2021-03-16         2.172        0.5863\n2  1740404  000330  汇添富现金宝货币市场基金A类  2021-03-15         2.168        0.6136\n3  1740100  000330  汇添富现金宝货币市场基金A类  2021-03-14         2.155        0.5785\n4  1739586  000330  汇添富现金宝货币市场基金A类  2021-03-13         2.155        0.5812"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"货币基金收益日报"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_MF_DAILY_PROFIT).filter(finance.FUND_MF_DAILY_PROFIT.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["货币基金收益日报"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"货币基金收益日报信息"}
    - {"type":"list","listType":"ul","items":["query(finance.FUND_MF_DAILY_PROFIT)表示从finance.FUND_MF_DAILY_PROFIT这张表中查询货币基金收益日报数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_MF_DAILY_PROFIT：收录了货币基金收益日报数据，表结构和字段信息如下：","filter(finance.FUND_MF_DAILY_PROFIT.code==code)：指定筛选条件，通过finance.FUND_MF_DAILY_PROFIT.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"table","headers":["字段","名称","类型"],"rows":[["code","基金代码","varchar(12)"],["name","基金名称","varchar(80)"],["end_date","收益日期","date"],["weekly_yield","7日年化收益率(%)","decimal(10,4)"],["daily_profit","每万份基金单位当日收益(元)","decimal(10,4)"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#查询汇添富现金宝(\"000330\")货币基金收益日报数据，只显示5条信息。\nfrom jqdatasdk import finance\ndf=finance.run_query(query(finance.FUND_MF_DAILY_PROFIT).filter(finance.FUND_MF_DAILY_PROFIT.code=='000330').order_by(finance.FUND_MF_DAILY_PROFIT.end_date.desc()).limit(5))\nprint(df)\n\n        id    code            name    end_date  weekly_yield  daily_profit\n0  1742123  000330  汇添富现金宝货币市场基金A类  2021-03-17         2.165        0.5857\n1  1741454  000330  汇添富现金宝货币市场基金A类  2021-03-16         2.172        0.5863\n2  1740404  000330  汇添富现金宝货币市场基金A类  2021-03-15         2.168        0.6136\n3  1740100  000330  汇添富现金宝货币市场基金A类  2021-03-14         2.155        0.5785\n4  1739586  000330  汇添富现金宝货币市场基金A类  2021-03-13         2.155        0.5812"}
  suggestedFilename: "doc_JQDatadoc_9941_overview_货币基金收益日报"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9941"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 货币基金收益日报

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9941

## 描述

描述

## 内容

#### 货币基金收益日报

- 历史范围：上市至今；更新时间：盘后24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.FUND_MF_DAILY_PROFIT).filter(finance.FUND_MF_DAILY_PROFIT.code==code).limit(n))
```

描述

- 货币基金收益日报

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

货币基金收益日报信息

- query(finance.FUND_MF_DAILY_PROFIT)表示从finance.FUND_MF_DAILY_PROFIT这张表中查询货币基金收益日报数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- finance.FUND_MF_DAILY_PROFIT：收录了货币基金收益日报数据，表结构和字段信息如下：
- filter(finance.FUND_MF_DAILY_PROFIT.code==code)：指定筛选条件，通过finance.FUND_MF_DAILY_PROFIT.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

| 字段 | 名称 | 类型 |
| --- | --- | --- |
| code | 基金代码 | varchar(12) |
| name | 基金名称 | varchar(80) |
| end_date | 收益日期 | date |
| weekly_yield | 7日年化收益率(%) | decimal(10,4) |
| daily_profit | 每万份基金单位当日收益(元) | decimal(10,4) |

###### 示例：

```python
#查询汇添富现金宝("000330")货币基金收益日报数据，只显示5条信息。
from jqdatasdk import finance
df=finance.run_query(query(finance.FUND_MF_DAILY_PROFIT).filter(finance.FUND_MF_DAILY_PROFIT.code=='000330').order_by(finance.FUND_MF_DAILY_PROFIT.end_date.desc()).limit(5))
print(df)

        id    code            name    end_date  weekly_yield  daily_profit
0  1742123  000330  汇添富现金宝货币市场基金A类  2021-03-17         2.165        0.5857
1  1741454  000330  汇添富现金宝货币市场基金A类  2021-03-16         2.172        0.5863
2  1740404  000330  汇添富现金宝货币市场基金A类  2021-03-15         2.168        0.6136
3  1740100  000330  汇添富现金宝货币市场基金A类  2021-03-14         2.155        0.5785
4  1739586  000330  汇添富现金宝货币市场基金A类  2021-03-13         2.155        0.5812
```
