---
id: "url-36497ade"
type: "website"
title: "上市信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10025"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:45:23.270Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10025"
  headings:
    - {"level":3,"text":"上市信息","id":""}
    - {"level":5,"text":"表字段信息","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "上市信息参数"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"ul","items":["获取沪深A股的上市信息，包含上市日期、交易所、发行价格、初始上市数量等"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.finance.STK_LIST)：表示从STK_LIST这张表中查询沪深A股的上市信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_LIST：代表上市公司基本信息表，收录了上市公司最新公布的基本信息，表结构和字段信息如下：","filter(finance.STK_LIST.code==code)：指定筛选条件，通过finance.STK_LIST.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_LIST.start_date>='2015-01-01'，表示筛选上市日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型","备注/示例"],"rows":[["code","证券代码","varchar(12)",""],["name","证券简称","varchar(40)",""],["short_name","拼音简称","varchar(20)",""],["category","证券类别","varchar(4)","A/B"],["exchange","交易所","varchar(12)","XSHG/XSHE"],["start_date","上市日期","date",""],["end_date","终止上市日期","date",""],["company_id","公司ID","int",""],["company_name","公司名称","varchar(100)",""],["ipo_shares","初始上市数量","decimal(20,2)","股"],["book_price","发行价格","decimal(20,4)","元"],["par_value","面值","decimal(20,4)","元"],["state_id","上市状态编码","int",""],["state","上市状态","varchar(32)",""]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_LIST).filter(finance.STK_LIST.code==code).limit(n))"}
    - {"language":"python","code":"# 指定查询对象为格力电器（000651.XSHG)的上市信息\nq=query(finance.STK_LIST).filter(finance.STK_LIST.code=='000651.XSHE')\ndf=finance.run_query(q)\nprint(df)\n\n     id         code  name short_name category exchange  start_date end_date  \\\n0  1789  000651.XSHE  格力电器       GLDQ        A     XSHE  1996-11-18     None   \n\n   company_id  company_name  ipo_shares  book_price  par_value  state_id state  \n0   430000651  珠海格力电器股份有限公司  21000000.0         2.5        1.0    301001  正常上市"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"上市信息"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_LIST).filter(finance.STK_LIST.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取沪深A股的上市信息，包含上市日期、交易所、发行价格、初始上市数量等"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"上市信息参数"}
    - {"type":"list","listType":"ul","items":["query(finance.finance.STK_LIST)：表示从STK_LIST这张表中查询沪深A股的上市信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_LIST：代表上市公司基本信息表，收录了上市公司最新公布的基本信息，表结构和字段信息如下：","filter(finance.STK_LIST.code==code)：指定筛选条件，通过finance.STK_LIST.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_LIST.start_date>='2015-01-01'，表示筛选上市日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"表字段信息"}
    - {"type":"table","headers":["字段名称","中文名称","字段类型","备注/示例"],"rows":[["code","证券代码","varchar(12)",""],["name","证券简称","varchar(40)",""],["short_name","拼音简称","varchar(20)",""],["category","证券类别","varchar(4)","A/B"],["exchange","交易所","varchar(12)","XSHG/XSHE"],["start_date","上市日期","date",""],["end_date","终止上市日期","date",""],["company_id","公司ID","int",""],["company_name","公司名称","varchar(100)",""],["ipo_shares","初始上市数量","decimal(20,2)","股"],["book_price","发行价格","decimal(20,4)","元"],["par_value","面值","decimal(20,4)","元"],["state_id","上市状态编码","int",""],["state","上市状态","varchar(32)",""]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 指定查询对象为格力电器（000651.XSHG)的上市信息\nq=query(finance.STK_LIST).filter(finance.STK_LIST.code=='000651.XSHE')\ndf=finance.run_query(q)\nprint(df)\n\n     id         code  name short_name category exchange  start_date end_date  \\\n0  1789  000651.XSHE  格力电器       GLDQ        A     XSHE  1996-11-18     None   \n\n   company_id  company_name  ipo_shares  book_price  par_value  state_id state  \n0   430000651  珠海格力电器股份有限公司  21000000.0         2.5        1.0    301001  正常上市"}
  suggestedFilename: "doc_JQDatadoc_10025_overview_上市信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10025"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 上市信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10025

## 描述

描述

## 内容

#### 上市信息

- 历史范围：2005年至今；更新时间：交易日24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.STK_LIST).filter(finance.STK_LIST.code==code).limit(n))
```

描述

- 获取沪深A股的上市信息，包含上市日期、交易所、发行价格、初始上市数量等

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

上市信息参数

- query(finance.finance.STK_LIST)：表示从STK_LIST这张表中查询沪深A股的上市信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]
- finance.STK_LIST：代表上市公司基本信息表，收录了上市公司最新公布的基本信息，表结构和字段信息如下：
- filter(finance.STK_LIST.code==code)：指定筛选条件，通过finance.STK_LIST.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_LIST.start_date>='2015-01-01'，表示筛选上市日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 表字段信息

| 字段名称 | 中文名称 | 字段类型 | 备注/示例 |
| --- | --- | --- | --- |
| code | 证券代码 | varchar(12) |  |
| name | 证券简称 | varchar(40) |  |
| short_name | 拼音简称 | varchar(20) |  |
| category | 证券类别 | varchar(4) | A/B |
| exchange | 交易所 | varchar(12) | XSHG/XSHE |
| start_date | 上市日期 | date |  |
| end_date | 终止上市日期 | date |  |
| company_id | 公司ID | int |  |
| company_name | 公司名称 | varchar(100) |  |
| ipo_shares | 初始上市数量 | decimal(20,2) | 股 |
| book_price | 发行价格 | decimal(20,4) | 元 |
| par_value | 面值 | decimal(20,4) | 元 |
| state_id | 上市状态编码 | int |  |
| state | 上市状态 | varchar(32) |  |

###### 示例

```python
# 指定查询对象为格力电器（000651.XSHG)的上市信息
q=query(finance.STK_LIST).filter(finance.STK_LIST.code=='000651.XSHE')
df=finance.run_query(q)
print(df)

     id         code  name short_name category exchange  start_date end_date  \
0  1789  000651.XSHE  格力电器       GLDQ        A     XSHE  1996-11-18     None   

   company_id  company_name  ipo_shares  book_price  par_value  state_id state  
0   430000651  珠海格力电器股份有限公司  21000000.0         2.5        1.0    301001  正常上市
```
