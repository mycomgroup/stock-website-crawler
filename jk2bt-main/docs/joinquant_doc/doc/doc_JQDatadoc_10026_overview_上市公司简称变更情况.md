---
id: "url-36497add"
type: "website"
title: "上市公司简称变更情况"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10026"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:45:27.207Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10026"
  headings:
    - {"level":3,"text":"上市公司简称变更情况","id":""}
    - {"level":5,"text":"表字段信息","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "上市公司简称变更情况参数"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"ul","items":["获取在A股市场和B股市场上市的股票简称的变更情况"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.STK_NAME_HISTORY)：表示从finance.STK_NAME_HISTORY这张表中查询股票简称的变更情况，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_NAME_HISTORY：代表股票简称变更表，收录了在A股市场和B股市场上市的股票简称的变更情况，表结构和字段信息如下：","filter(finance.STK_NAME_HISTORY.code==code)：指定筛选条件，通过finance.STK_NAME_HISTORY.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_NAME_HISTORY.pub_date>='2015-01-01'，表示筛选公告日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型","备注/示例"],"rows":[["code","股票代码","varchar(12)",""],["company_id","公司ID","int",""],["new_name","新股票简称","varchar(40)",""],["new_spelling","新英文简称","varchar(40)",""],["org_name","原证券简称","varchar(40)",""],["org_spelling","原证券英文简称","varchar(40)",""],["start_date","开始日期","date",""],["pub_date","公告日期","date",""],["reason","变更原因","varchar(255)",""]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_NAME_HISTORY).filter(finance.STK_NAME_HISTORY.code==code).limit(n))"}
    - {"language":"python","code":"# 指定查询对象为恒瑞医药（600276.XSHG)的股票简称变更信息\nq=query(finance.STK_NAME_HISTORY).filter(finance.STK_NAME_HISTORY.code=='600276.XSHG')\ndf=finance.run_query(q)\nprint(df)\n\n     id         code company_id     new_name   new_spelling org_name org_spelling  \\\n0  1459  600276.XSHG  420600276     恒瑞医药         HRYY      NaN          NaN\n1  3588  600276.XSHG  420600276      Ｇ恒瑞          ＧHR      NaN          NaN\n2  4007  600276.XSHG  420600276     恒瑞医药         HRYY      NaN          NaN\n\n   start_date    pub_date  reason\n0  2000-10-18  2000-10-18    NaN\n1  2006-06-20  2006-06-15    NaN\n2  2006-10-09  2006-09-28    NaN"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"上市公司简称变更情况"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_NAME_HISTORY).filter(finance.STK_NAME_HISTORY.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取在A股市场和B股市场上市的股票简称的变更情况"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"上市公司简称变更情况参数"}
    - {"type":"list","listType":"ul","items":["query(finance.STK_NAME_HISTORY)：表示从finance.STK_NAME_HISTORY这张表中查询股票简称的变更情况，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_NAME_HISTORY：代表股票简称变更表，收录了在A股市场和B股市场上市的股票简称的变更情况，表结构和字段信息如下：","filter(finance.STK_NAME_HISTORY.code==code)：指定筛选条件，通过finance.STK_NAME_HISTORY.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_NAME_HISTORY.pub_date>='2015-01-01'，表示筛选公告日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"表字段信息"}
    - {"type":"table","headers":["字段名称","中文名称","字段类型","备注/示例"],"rows":[["code","股票代码","varchar(12)",""],["company_id","公司ID","int",""],["new_name","新股票简称","varchar(40)",""],["new_spelling","新英文简称","varchar(40)",""],["org_name","原证券简称","varchar(40)",""],["org_spelling","原证券英文简称","varchar(40)",""],["start_date","开始日期","date",""],["pub_date","公告日期","date",""],["reason","变更原因","varchar(255)",""]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 指定查询对象为恒瑞医药（600276.XSHG)的股票简称变更信息\nq=query(finance.STK_NAME_HISTORY).filter(finance.STK_NAME_HISTORY.code=='600276.XSHG')\ndf=finance.run_query(q)\nprint(df)\n\n     id         code company_id     new_name   new_spelling org_name org_spelling  \\\n0  1459  600276.XSHG  420600276     恒瑞医药         HRYY      NaN          NaN\n1  3588  600276.XSHG  420600276      Ｇ恒瑞          ＧHR      NaN          NaN\n2  4007  600276.XSHG  420600276     恒瑞医药         HRYY      NaN          NaN\n\n   start_date    pub_date  reason\n0  2000-10-18  2000-10-18    NaN\n1  2006-06-20  2006-06-15    NaN\n2  2006-10-09  2006-09-28    NaN"}
  suggestedFilename: "doc_JQDatadoc_10026_overview_上市公司简称变更情况"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10026"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 上市公司简称变更情况

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10026

## 描述

描述

## 内容

#### 上市公司简称变更情况

- 历史范围：2005年至今；更新时间：交易日24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.STK_NAME_HISTORY).filter(finance.STK_NAME_HISTORY.code==code).limit(n))
```

描述

- 获取在A股市场和B股市场上市的股票简称的变更情况

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

上市公司简称变更情况参数

- query(finance.STK_NAME_HISTORY)：表示从finance.STK_NAME_HISTORY这张表中查询股票简称的变更情况，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]
- finance.STK_NAME_HISTORY：代表股票简称变更表，收录了在A股市场和B股市场上市的股票简称的变更情况，表结构和字段信息如下：
- filter(finance.STK_NAME_HISTORY.code==code)：指定筛选条件，通过finance.STK_NAME_HISTORY.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_NAME_HISTORY.pub_date>='2015-01-01'，表示筛选公告日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 表字段信息

| 字段名称 | 中文名称 | 字段类型 | 备注/示例 |
| --- | --- | --- | --- |
| code | 股票代码 | varchar(12) |  |
| company_id | 公司ID | int |  |
| new_name | 新股票简称 | varchar(40) |  |
| new_spelling | 新英文简称 | varchar(40) |  |
| org_name | 原证券简称 | varchar(40) |  |
| org_spelling | 原证券英文简称 | varchar(40) |  |
| start_date | 开始日期 | date |  |
| pub_date | 公告日期 | date |  |
| reason | 变更原因 | varchar(255) |  |

###### 示例

```python
# 指定查询对象为恒瑞医药（600276.XSHG)的股票简称变更信息
q=query(finance.STK_NAME_HISTORY).filter(finance.STK_NAME_HISTORY.code=='600276.XSHG')
df=finance.run_query(q)
print(df)

     id         code company_id     new_name   new_spelling org_name org_spelling  \
0  1459  600276.XSHG  420600276     恒瑞医药         HRYY      NaN          NaN
1  3588  600276.XSHG  420600276      Ｇ恒瑞          ＧHR      NaN          NaN
2  4007  600276.XSHG  420600276     恒瑞医药         HRYY      NaN          NaN

   start_date    pub_date  reason
0  2000-10-18  2000-10-18    NaN
1  2006-06-20  2006-06-15    NaN
2  2006-10-09  2006-09-28    NaN
```
