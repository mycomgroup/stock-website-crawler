---
id: "url-3649681b"
type: "website"
title: "查询数据库数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10523"
description: "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
source: ""
tags: []
crawl_time: "2026-03-27T07:47:05.739Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10523"
  headings:
    - {"level":3,"text":"查询数据库数据","id":""}
  paragraphs:
    - "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
    - "run_query查询数据库数据，注意区分数据库，接收Query对象,query对象的教程见Query的简单教程"
    - "注意"
    - "示例"
  lists:
    - {"type":"ul","items":["单次返回最多5000条，如查询数据量超出请限制查询范围或者使用run_offset_query","查询时尽量根据id,日期,或者标的代码(一般地这些字段都会被设置为索引)进行filter,查询如果命中索引返回就会较快"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"finance.run_query(query_object) #查询股票/期货/基金数据库\nopt.run_query(query_object) #查询期权数据库\nbond.run_query(query_object) #查询债券数据库\nmacro.run_query(query_object) #查询宏观数据库"}
    - {"language":"python","code":"# 查询finance库，万科 AH 股价格的前10条数据\nfrom jqdatasdk import query,finance\n# 或from jqdatasdk import *\nq=query(finance.STK_AH_PRICE_COMP\n  ).filter(\n        finance.STK_AH_PRICE_COMP.a_code=='000002.XSHE'\n  ).order_by(\n        finance.STK_AH_PRICE_COMP.day\n  ).limit(10)\ndf=finance.run_query(q)"}
    - {"language":"python","code":"# 查询opt库，当前可交易的50ETF期权合约信息\nfrom jqdatasdk import query,opt\n# 或from jqdatasdk import *\nfrom datetime import datetime\nopt.run_query(query(opt.OPT_CONTRACT_INFO).filter((opt.OPT_CONTRACT_INFO.underlying_symbol == \"510050.XSHG\") & (opt.OPT_CONTRACT_INFO.last_trade_date > datetime.now())))"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"查询数据库数据"}
    - {"type":"paragraph","content":"试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"}
    - {"type":"codeblock","language":"python","content":"finance.run_query(query_object) #查询股票/期货/基金数据库\nopt.run_query(query_object) #查询期权数据库\nbond.run_query(query_object) #查询债券数据库\nmacro.run_query(query_object) #查询宏观数据库"}
    - {"type":"paragraph","content":"run_query查询数据库数据，注意区分数据库，接收Query对象,query对象的教程见Query的简单教程"}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["单次返回最多5000条，如查询数据量超出请限制查询范围或者使用run_offset_query","查询时尽量根据id,日期,或者标的代码(一般地这些字段都会被设置为索引)进行filter,查询如果命中索引返回就会较快"]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 查询finance库，万科 AH 股价格的前10条数据\nfrom jqdatasdk import query,finance\n# 或from jqdatasdk import *\nq=query(finance.STK_AH_PRICE_COMP\n  ).filter(\n        finance.STK_AH_PRICE_COMP.a_code=='000002.XSHE'\n  ).order_by(\n        finance.STK_AH_PRICE_COMP.day\n  ).limit(10)\ndf=finance.run_query(q)"}
    - {"type":"codeblock","language":"python","content":"# 查询opt库，当前可交易的50ETF期权合约信息\nfrom jqdatasdk import query,opt\n# 或from jqdatasdk import *\nfrom datetime import datetime\nopt.run_query(query(opt.OPT_CONTRACT_INFO).filter((opt.OPT_CONTRACT_INFO.underlying_symbol == \"510050.XSHG\") & (opt.OPT_CONTRACT_INFO.last_trade_date > datetime.now())))"}
  suggestedFilename: "doc_JQDatadoc_10523_overview_查询数据库数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10523"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 查询数据库数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10523

## 描述

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

## 内容

#### 查询数据库数据

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

```python
finance.run_query(query_object) #查询股票/期货/基金数据库
opt.run_query(query_object) #查询期权数据库
bond.run_query(query_object) #查询债券数据库
macro.run_query(query_object) #查询宏观数据库
```

run_query查询数据库数据，注意区分数据库，接收Query对象,query对象的教程见Query的简单教程

注意

- 单次返回最多5000条，如查询数据量超出请限制查询范围或者使用run_offset_query
- 查询时尽量根据id,日期,或者标的代码(一般地这些字段都会被设置为索引)进行filter,查询如果命中索引返回就会较快

示例

```python
# 查询finance库，万科 AH 股价格的前10条数据
from jqdatasdk import query,finance
# 或from jqdatasdk import *
q=query(finance.STK_AH_PRICE_COMP
  ).filter(
        finance.STK_AH_PRICE_COMP.a_code=='000002.XSHE'
  ).order_by(
        finance.STK_AH_PRICE_COMP.day
  ).limit(10)
df=finance.run_query(q)
```

```python
# 查询opt库，当前可交易的50ETF期权合约信息
from jqdatasdk import query,opt
# 或from jqdatasdk import *
from datetime import datetime
opt.run_query(query(opt.OPT_CONTRACT_INFO).filter((opt.OPT_CONTRACT_INFO.underlying_symbol == "510050.XSHG") & (opt.OPT_CONTRACT_INFO.last_trade_date > datetime.now())))
```
