---
id: "url-7a226b34"
type: "website"
title: "市场通合格证券变动记录"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9869"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:18:01.277Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9869"
  headings:
    - {"level":3,"text":"市场通合格证券变动记录","id":""}
    - {"level":5,"text":"表字段信息","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：交易日20:30-06:30更新"]}
    - {"type":"ul","items":["记录沪港通、深港通和港股通的成分股的变动情况。"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.STK_EL_CONST_CHANGE)：表示从finance.STK_EL_CONST_CHANGE这张表中查询沪港通、深港通和港股通成分股的变动记录，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_EL_CONST_CHANGE：代表合资格证券变动表，记录沪港通、深港通和港股通成分股的变动情况，包括交易类型，变更日期，变更方向等，表结构和字段信息如下:","filter(finance.STK_EL_CONST_CHANGE.code==code)：指定筛选条件，通过finance.STK_EL_CONST_CHANGE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_EL_CONST_CHANGE.change_date>='2015-01-01'，表示筛选变更日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","order_by(finance.STK_EL_CONST_CHANGE.change_date)：将返回结果按变更日期排序。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段","名称","类型","非空","备注/示例"],"rows":[["link_id","交易类型编码","int","Y","同市场通编码"],["link_name","交易类型名称","varchar(12)","Y",""],["code","证券代码","varchar(12)","Y",""],["name_ch","中文简称","varchar(30)","",""],["name_en","英文简称","varchar(120)","",""],["exchange","该股票所在的交易所","varchar(12)","Y","上海市场:XSHG/深圳市场:XSHE/香港市场:XHKG"],["change_date","变更日期","date","Y",""],["direction","变更方向","varchar(6)","Y","IN/OUT（分别为纳入和剔除）"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\n\nfinance.run_query(query(finance.STK_EL_CONST_CHANGE).filter(finance.STK_EL_CONST_CHANGE.code==code).limit(n))"}
    - {"language":"python","code":"q=query(finance.STK_EL_CONST_CHANGE).filter(finance.STK_EL_CONST_CHANGE.link_id==310001).order_by(finance.STK_EL_CONST_CHANGE.change_date).limit(4)\ndf=finance.run_query(q)\nprint(df)\n\n    id  link_id link_name         code name_ch name_en exchange change_date  \\\n0  536   310001       沪股通  600000.XSHG    浦发银行    None     XSHG  2014-11-17   \n1  537   310001       沪股通  600004.XSHG    白云机场    None     XSHG  2014-11-17   \n2  539   310001       沪股通  600007.XSHG    中国国贸    None     XSHG  2014-11-17   \n3  540   310001       沪股通  600008.XSHG    首创股份    None     XSHG  2014-11-17   \n\n  direction  \n0        IN  \n1        IN  \n2        IN  \n3        IN"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"市场通合格证券变动记录"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：交易日20:30-06:30更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\n\nfinance.run_query(query(finance.STK_EL_CONST_CHANGE).filter(finance.STK_EL_CONST_CHANGE.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["记录沪港通、深港通和港股通的成分股的变动情况。"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["query(finance.STK_EL_CONST_CHANGE)：表示从finance.STK_EL_CONST_CHANGE这张表中查询沪港通、深港通和港股通成分股的变动记录，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_EL_CONST_CHANGE：代表合资格证券变动表，记录沪港通、深港通和港股通成分股的变动情况，包括交易类型，变更日期，变更方向等，表结构和字段信息如下:","filter(finance.STK_EL_CONST_CHANGE.code==code)：指定筛选条件，通过finance.STK_EL_CONST_CHANGE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_EL_CONST_CHANGE.change_date>='2015-01-01'，表示筛选变更日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","order_by(finance.STK_EL_CONST_CHANGE.change_date)：将返回结果按变更日期排序。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"表字段信息"}
    - {"type":"table","headers":["字段","名称","类型","非空","备注/示例"],"rows":[["link_id","交易类型编码","int","Y","同市场通编码"],["link_name","交易类型名称","varchar(12)","Y",""],["code","证券代码","varchar(12)","Y",""],["name_ch","中文简称","varchar(30)","",""],["name_en","英文简称","varchar(120)","",""],["exchange","该股票所在的交易所","varchar(12)","Y","上海市场:XSHG/深圳市场:XSHE/香港市场:XHKG"],["change_date","变更日期","date","Y",""],["direction","变更方向","varchar(6)","Y","IN/OUT（分别为纳入和剔除）"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"q=query(finance.STK_EL_CONST_CHANGE).filter(finance.STK_EL_CONST_CHANGE.link_id==310001).order_by(finance.STK_EL_CONST_CHANGE.change_date).limit(4)\ndf=finance.run_query(q)\nprint(df)\n\n    id  link_id link_name         code name_ch name_en exchange change_date  \\\n0  536   310001       沪股通  600000.XSHG    浦发银行    None     XSHG  2014-11-17   \n1  537   310001       沪股通  600004.XSHG    白云机场    None     XSHG  2014-11-17   \n2  539   310001       沪股通  600007.XSHG    中国国贸    None     XSHG  2014-11-17   \n3  540   310001       沪股通  600008.XSHG    首创股份    None     XSHG  2014-11-17   \n\n  direction  \n0        IN  \n1        IN  \n2        IN  \n3        IN"}
  suggestedFilename: "doc_JQDatadoc_9869_overview_市场通合格证券变动记录"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9869"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 市场通合格证券变动记录

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9869

## 描述

描述

## 内容

#### 市场通合格证券变动记录

- 历史范围：上市至今；更新时间：交易日20:30-06:30更新

```python
from jqdatasdk import finance

finance.run_query(query(finance.STK_EL_CONST_CHANGE).filter(finance.STK_EL_CONST_CHANGE.code==code).limit(n))
```

描述

- 记录沪港通、深港通和港股通的成分股的变动情况。

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

参数

- query(finance.STK_EL_CONST_CHANGE)：表示从finance.STK_EL_CONST_CHANGE这张表中查询沪港通、深港通和港股通成分股的变动记录，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]
- finance.STK_EL_CONST_CHANGE：代表合资格证券变动表，记录沪港通、深港通和港股通成分股的变动情况，包括交易类型，变更日期，变更方向等，表结构和字段信息如下:
- filter(finance.STK_EL_CONST_CHANGE.code==code)：指定筛选条件，通过finance.STK_EL_CONST_CHANGE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_EL_CONST_CHANGE.change_date>='2015-01-01'，表示筛选变更日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。
- order_by(finance.STK_EL_CONST_CHANGE.change_date)：将返回结果按变更日期排序。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 表字段信息

| 字段 | 名称 | 类型 | 非空 | 备注/示例 |
| --- | --- | --- | --- | --- |
| link_id | 交易类型编码 | int | Y | 同市场通编码 |
| link_name | 交易类型名称 | varchar(12) | Y |  |
| code | 证券代码 | varchar(12) | Y |  |
| name_ch | 中文简称 | varchar(30) |  |  |
| name_en | 英文简称 | varchar(120) |  |  |
| exchange | 该股票所在的交易所 | varchar(12) | Y | 上海市场:XSHG/深圳市场:XSHE/香港市场:XHKG |
| change_date | 变更日期 | date | Y |  |
| direction | 变更方向 | varchar(6) | Y | IN/OUT（分别为纳入和剔除） |

###### 示例

```python
q=query(finance.STK_EL_CONST_CHANGE).filter(finance.STK_EL_CONST_CHANGE.link_id==310001).order_by(finance.STK_EL_CONST_CHANGE.change_date).limit(4)
df=finance.run_query(q)
print(df)

    id  link_id link_name         code name_ch name_en exchange change_date  \
0  536   310001       沪股通  600000.XSHG    浦发银行    None     XSHG  2014-11-17   
1  537   310001       沪股通  600004.XSHG    白云机场    None     XSHG  2014-11-17   
2  539   310001       沪股通  600007.XSHG    中国国贸    None     XSHG  2014-11-17   
3  540   310001       沪股通  600008.XSHG    首创股份    None     XSHG  2014-11-17   

  direction  
0        IN  
1        IN  
2        IN  
3        IN
```
