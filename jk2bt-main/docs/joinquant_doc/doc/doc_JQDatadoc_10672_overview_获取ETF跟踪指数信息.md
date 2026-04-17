---
id: "url-364963c0"
type: "website"
title: "获取ETF跟踪指数信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10672"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:48:04.953Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10672"
  headings:
    - {"level":3,"text":"获取ETF跟踪指数信息","id":""}
    - {"level":5,"text":"参数","id":""}
  paragraphs:
    - "描述"
    - "获取etf跟踪指数信息"
    - "示例："
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：24点更新"]}
    - {"type":"ul","items":["获取etf跟踪指数信息"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.FUND_INVEST_TARGET)表示从finance.FUND_INVEST_TARGET这张表中查询etf跟踪指数信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_INVEST_TARGET：收录了ETF基金跟踪的指数信息，表结构和字段信息如下：","filter(finance.FUND_INVEST_TARGET.code==code)：指定筛选条件，通过finance.FUND_INVEST_TARGET.code==code可以指定你想要查询的基金标的；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段名","类型","描述"],"rows":[["code","varchar(12)","基金代码"],["name","varchar(50)","基金简称"],["pub_date","DATE","公告日期"],["start_date","DATE","生效日期"],["end_date","DATE","失效日期（未失效则为空）"],["traced_index_name","varchar(100)","跟踪指数名称"],["traced_index_code","varchar(12)","跟踪指数代码（不支持的指数填充为空）"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import *\nfinance.run_query(query(finance.FUND_INVEST_TARGET).filter(finance.FUND_INVEST_TARGET.code== '510190.XSHG'))"}
    - {"language":"python","code":"# 查询510190追踪的指数信息\nq = query(finance.FUND_INVEST_TARGET).filter(finance.FUND_INVEST_TARGET.code== '510190.XSHG')\ndf = finance.run_query(q)\nprint(df)\n>>>\n\n    id         code   name    pub_date  start_date    end_date traced_index_name traced_index_code\n0  930  510190.XSHG  上证50基  2010-10-20  2010-10-25  2023-02-23      上证龙头(000065)       000065.XSHG\n1  742  510190.XSHG  上证50基  2023-02-23  2023-02-23        None      上证50(000016)       000016.XSHG"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取ETF跟踪指数信息"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：24点更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\nfinance.run_query(query(finance.FUND_INVEST_TARGET).filter(finance.FUND_INVEST_TARGET.code== '510190.XSHG'))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取etf跟踪指数信息"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"获取etf跟踪指数信息"}
    - {"type":"list","listType":"ul","items":["query(finance.FUND_INVEST_TARGET)表示从finance.FUND_INVEST_TARGET这张表中查询etf跟踪指数信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_INVEST_TARGET：收录了ETF基金跟踪的指数信息，表结构和字段信息如下：","filter(finance.FUND_INVEST_TARGET.code==code)：指定筛选条件，通过finance.FUND_INVEST_TARGET.code==code可以指定你想要查询的基金标的；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["字段名","类型","描述"],"rows":[["code","varchar(12)","基金代码"],["name","varchar(50)","基金简称"],["pub_date","DATE","公告日期"],["start_date","DATE","生效日期"],["end_date","DATE","失效日期（未失效则为空）"],["traced_index_name","varchar(100)","跟踪指数名称"],["traced_index_code","varchar(12)","跟踪指数代码（不支持的指数填充为空）"]]}
    - {"type":"paragraph","content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 查询510190追踪的指数信息\nq = query(finance.FUND_INVEST_TARGET).filter(finance.FUND_INVEST_TARGET.code== '510190.XSHG')\ndf = finance.run_query(q)\nprint(df)\n>>>\n\n    id         code   name    pub_date  start_date    end_date traced_index_name traced_index_code\n0  930  510190.XSHG  上证50基  2010-10-20  2010-10-25  2023-02-23      上证龙头(000065)       000065.XSHG\n1  742  510190.XSHG  上证50基  2023-02-23  2023-02-23        None      上证50(000016)       000016.XSHG"}
  suggestedFilename: "doc_JQDatadoc_10672_overview_获取ETF跟踪指数信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10672"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取ETF跟踪指数信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10672

## 描述

描述

## 内容

#### 获取ETF跟踪指数信息

- 历史范围：上市至今；更新时间：24点更新

```python
from jqdatasdk import *
finance.run_query(query(finance.FUND_INVEST_TARGET).filter(finance.FUND_INVEST_TARGET.code== '510190.XSHG'))
```

描述

- 获取etf跟踪指数信息

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

获取etf跟踪指数信息

- query(finance.FUND_INVEST_TARGET)表示从finance.FUND_INVEST_TARGET这张表中查询etf跟踪指数信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- finance.FUND_INVEST_TARGET：收录了ETF基金跟踪的指数信息，表结构和字段信息如下：
- filter(finance.FUND_INVEST_TARGET.code==code)：指定筛选条件，通过finance.FUND_INVEST_TARGET.code==code可以指定你想要查询的基金标的；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 参数

| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| code | varchar(12) | 基金代码 |
| name | varchar(50) | 基金简称 |
| pub_date | DATE | 公告日期 |
| start_date | DATE | 生效日期 |
| end_date | DATE | 失效日期（未失效则为空） |
| traced_index_name | varchar(100) | 跟踪指数名称 |
| traced_index_code | varchar(12) | 跟踪指数代码（不支持的指数填充为空） |

示例：

```python
# 查询510190追踪的指数信息
q = query(finance.FUND_INVEST_TARGET).filter(finance.FUND_INVEST_TARGET.code== '510190.XSHG')
df = finance.run_query(q)
print(df)
>>>

    id         code   name    pub_date  start_date    end_date traced_index_name traced_index_code
0  930  510190.XSHG  上证50基  2010-10-20  2010-10-25  2023-02-23      上证龙头(000065)       000065.XSHG
1  742  510190.XSHG  上证50基  2023-02-23  2023-02-23        None      上证50(000016)       000016.XSHG
```
