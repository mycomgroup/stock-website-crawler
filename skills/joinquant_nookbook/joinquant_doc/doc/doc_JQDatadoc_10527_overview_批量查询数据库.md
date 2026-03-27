---
id: "url-36496817"
type: "website"
title: "批量查询数据库"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10527"
description: "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
source: ""
tags: []
crawl_time: "2026-03-27T09:08:42.668Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10527"
  headings:
    - {"level":3,"text":"批量查询数据库","id":""}
  paragraphs:
    - "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
    - "run_offset_query分页查询数据库数据，返回最多20万条数据，注意区分数据库，接收Query对象,query对象的教程见Query的简单教程"
    - "注意"
    - "示例"
  lists:
    - {"type":"ul","items":["因为run_query 有单次调取最大返回5000条的限制，此函数利用MySql的offset方法循环获取数据，便于提取超过5000条的数据集","因为随着offset值的增大，查询性能是递减的 ,因此此方法仍然设置了查询上限, 最多返回20万条数据，如查询超过此上限返回数据可能不完整，请注意控制查询范围，可利用数据的日期,标的代码等字段限制查询范围, 分批查询","因为该方法是通过指定limit和offset来实现分页查询的，因此用户自己给Query对象中传递的limit及offset参数将不生效","查询时尽量根据id,日期,或者标的代码(一般地这些字段都会被设置为索引)进行filter,查询如果命中索引返回就会较快"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"finance.run_offset_query(query_object) #分页查询股票/期货/基金数据库\nopt.run_offset_query(query_object) #分页查询期权数据库\nbond.run_offset_query(query_object) #分页查询债券数据库\nmacro.run_offset_query(query_object) #分页查询宏观数据库"}
    - {"language":"python","code":"# 查询finance库，报告期利润表2022年报和2023年报,数据量约1.6万条\nfrom jqdatasdk import query,finance\n# 或from jqdatasdk import *\nq = query(finance.STK_INCOME_STATEMENT).filter(finance.STK_INCOME_STATEMENT.end_date.in_(['2022-12-31','2021-12-31']))\ndf = finance.run_offset_query(q)"}
    - {"language":"python","code":"# 查询bond库, 国债逆回购日行情2019年到2021年的数据,数据量约1.3万条\nfrom jqdatasdk import query,bond\n# 或from jqdatasdk import *\nq = query(bond.REPO_DAILY_PRICE).filter(bond.REPO_DAILY_PRICE.date>'2019-01-01',\n                                                   bond.REPO_DAILY_PRICE.date<='2021-12-31'\n                                                   )\ndf = jq.bond.run_offset_query(q)"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"批量查询数据库"}
    - {"type":"paragraph","content":"试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"}
    - {"type":"codeblock","language":"python","content":"finance.run_offset_query(query_object) #分页查询股票/期货/基金数据库\nopt.run_offset_query(query_object) #分页查询期权数据库\nbond.run_offset_query(query_object) #分页查询债券数据库\nmacro.run_offset_query(query_object) #分页查询宏观数据库"}
    - {"type":"paragraph","content":"run_offset_query分页查询数据库数据，返回最多20万条数据，注意区分数据库，接收Query对象,query对象的教程见Query的简单教程"}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["因为run_query 有单次调取最大返回5000条的限制，此函数利用MySql的offset方法循环获取数据，便于提取超过5000条的数据集","因为随着offset值的增大，查询性能是递减的 ,因此此方法仍然设置了查询上限, 最多返回20万条数据，如查询超过此上限返回数据可能不完整，请注意控制查询范围，可利用数据的日期,标的代码等字段限制查询范围, 分批查询","因为该方法是通过指定limit和offset来实现分页查询的，因此用户自己给Query对象中传递的limit及offset参数将不生效","查询时尽量根据id,日期,或者标的代码(一般地这些字段都会被设置为索引)进行filter,查询如果命中索引返回就会较快"]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 查询finance库，报告期利润表2022年报和2023年报,数据量约1.6万条\nfrom jqdatasdk import query,finance\n# 或from jqdatasdk import *\nq = query(finance.STK_INCOME_STATEMENT).filter(finance.STK_INCOME_STATEMENT.end_date.in_(['2022-12-31','2021-12-31']))\ndf = finance.run_offset_query(q)"}
    - {"type":"codeblock","language":"python","content":"# 查询bond库, 国债逆回购日行情2019年到2021年的数据,数据量约1.3万条\nfrom jqdatasdk import query,bond\n# 或from jqdatasdk import *\nq = query(bond.REPO_DAILY_PRICE).filter(bond.REPO_DAILY_PRICE.date>'2019-01-01',\n                                                   bond.REPO_DAILY_PRICE.date<='2021-12-31'\n                                                   )\ndf = jq.bond.run_offset_query(q)"}
  suggestedFilename: "doc_JQDatadoc_10527_overview_批量查询数据库"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10527"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 批量查询数据库

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10527

## 描述

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

## 内容

#### 批量查询数据库

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

```python
finance.run_offset_query(query_object) #分页查询股票/期货/基金数据库
opt.run_offset_query(query_object) #分页查询期权数据库
bond.run_offset_query(query_object) #分页查询债券数据库
macro.run_offset_query(query_object) #分页查询宏观数据库
```

run_offset_query分页查询数据库数据，返回最多20万条数据，注意区分数据库，接收Query对象,query对象的教程见Query的简单教程

注意

- 因为run_query 有单次调取最大返回5000条的限制，此函数利用MySql的offset方法循环获取数据，便于提取超过5000条的数据集
- 因为随着offset值的增大，查询性能是递减的 ,因此此方法仍然设置了查询上限, 最多返回20万条数据，如查询超过此上限返回数据可能不完整，请注意控制查询范围，可利用数据的日期,标的代码等字段限制查询范围, 分批查询
- 因为该方法是通过指定limit和offset来实现分页查询的，因此用户自己给Query对象中传递的limit及offset参数将不生效
- 查询时尽量根据id,日期,或者标的代码(一般地这些字段都会被设置为索引)进行filter,查询如果命中索引返回就会较快

示例

```python
# 查询finance库，报告期利润表2022年报和2023年报,数据量约1.6万条
from jqdatasdk import query,finance
# 或from jqdatasdk import *
q = query(finance.STK_INCOME_STATEMENT).filter(finance.STK_INCOME_STATEMENT.end_date.in_(['2022-12-31','2021-12-31']))
df = finance.run_offset_query(q)
```

```python
# 查询bond库, 国债逆回购日行情2019年到2021年的数据,数据量约1.3万条
from jqdatasdk import query,bond
# 或from jqdatasdk import *
q = query(bond.REPO_DAILY_PRICE).filter(bond.REPO_DAILY_PRICE.date>'2019-01-01',
                                                   bond.REPO_DAILY_PRICE.date<='2021-12-31'
                                                   )
df = jq.bond.run_offset_query(q)
```
