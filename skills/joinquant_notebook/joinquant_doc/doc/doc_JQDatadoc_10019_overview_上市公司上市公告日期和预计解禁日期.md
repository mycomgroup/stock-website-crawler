---
id: "url-36497af9"
type: "website"
title: "上市公司上市公告日期和预计解禁日期"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10019"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:44:59.622Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10019"
  headings:
    - {"level":3,"text":"上市公司上市公告日期和预计解禁日期","id":""}
    - {"level":5,"text":"表字段信息","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "上市公司上市公告日期和预计解禁日期参数"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"ul","items":["获取上市公司受限股份上市公告日期和预计解禁日期。"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.STK_LIMITED_SHARES_LIST)：表示从finance.STK_LIMITED_SHARES_LIST这张表中查询上市公司受限股份上市公告和预计解禁的日期，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_LIMITED_SHARES_LIST：代表受限股份上市公告日期表，收录了上市公司受限股份上市公告和预计解禁的日期。表结构和字段信息如下：","filter(finance.STK_LIMITED_SHARES_LIST.code==code)：指定筛选条件，通过finance.STK_LIMITED_SHARES_LIST.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_LIMITED_SHARES_LIST.pub_date>='2015-01-01'，表示筛选公布日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型","含义"],"rows":[["company_id","公司ID","int",""],["company_name","公司名称","varchar(100)",""],["code","股票代码","varchar(12)",""],["pub_date","公告日期","date","上市流通方案公布日期"],["shareholder_name","股东名称","varchar(100)",""],["expected_unlimited_date","预计解除限售日期","date",""],["expected_unlimited_number","预计解除限售数量","int","单位：股"],["expected_unlimited_ratio","预计解除限售比例","decimal(10,4)","单位：％；预计解除限售数量占总股本比例"],["actual_unlimited_date","实际解除限售日期","date",""],["actual_unlimited_number","实际解除限售数量","int","单位：股"],["actual_unlimited_ratio","实际解除限售比例","decimal(10,4)","单位：％；实际解除限售数量占总股本比例"],["limited_reason_id","限售原因编码","int","如下 限售原因编码"],["limited_reason","限售原因","varchar(60)","用户选择：股改限售；发行限售"],["trade_condition","上市交易条件","varchar(500)","股份上市交易的条件限制"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_LIMITED_SHARES_LIST).filter(finance.STK_LIMITED_SHARES_LIST.code==code).limit(n))"}
    - {"language":"python","code":"#指定查询对象为华泰证券（601688.XSHG)的受限股份上市公告日期\nq=query(finance.STK_LIMITED_SHARES_LIST).filter(finance.STK_LIMITED_SHARES_LIST.code=='601688.XSHG',finance.STK_LIMITED_SHARES_LIST.pub_date>'2018-01-01')\ndf=finance.run_query(q)\nprint(df)\n\n      id  company_id company_name         code    pub_date   shareholder_name  \\\n0  34395   460000161   华泰证券股份有限公司  601688.XSHG  2018-08-04  阿里巴巴（中国）网络技术有限公司等\n\n  expected_unlimited_date  expected_unlimited_number expected_unlimited_ratio  \\\n0              2019-08-02               1.088731e+09                     None\n\n  actual_unlimited_date actual_unlimited_number actual_unlimited_ratio  \\\n0                  None                    None                   None\n\n   limited_reason_id limited_reason trade_condition\n0             309008        非公开发行限售            None"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"上市公司上市公告日期和预计解禁日期"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_LIMITED_SHARES_LIST).filter(finance.STK_LIMITED_SHARES_LIST.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取上市公司受限股份上市公告日期和预计解禁日期。"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"上市公司上市公告日期和预计解禁日期参数"}
    - {"type":"list","listType":"ul","items":["query(finance.STK_LIMITED_SHARES_LIST)：表示从finance.STK_LIMITED_SHARES_LIST这张表中查询上市公司受限股份上市公告和预计解禁的日期，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_LIMITED_SHARES_LIST：代表受限股份上市公告日期表，收录了上市公司受限股份上市公告和预计解禁的日期。表结构和字段信息如下：","filter(finance.STK_LIMITED_SHARES_LIST.code==code)：指定筛选条件，通过finance.STK_LIMITED_SHARES_LIST.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_LIMITED_SHARES_LIST.pub_date>='2015-01-01'，表示筛选公布日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"表字段信息"}
    - {"type":"table","headers":["字段名称","中文名称","字段类型","含义"],"rows":[["company_id","公司ID","int",""],["company_name","公司名称","varchar(100)",""],["code","股票代码","varchar(12)",""],["pub_date","公告日期","date","上市流通方案公布日期"],["shareholder_name","股东名称","varchar(100)",""],["expected_unlimited_date","预计解除限售日期","date",""],["expected_unlimited_number","预计解除限售数量","int","单位：股"],["expected_unlimited_ratio","预计解除限售比例","decimal(10,4)","单位：％；预计解除限售数量占总股本比例"],["actual_unlimited_date","实际解除限售日期","date",""],["actual_unlimited_number","实际解除限售数量","int","单位：股"],["actual_unlimited_ratio","实际解除限售比例","decimal(10,4)","单位：％；实际解除限售数量占总股本比例"],["limited_reason_id","限售原因编码","int","如下 限售原因编码"],["limited_reason","限售原因","varchar(60)","用户选择：股改限售；发行限售"],["trade_condition","上市交易条件","varchar(500)","股份上市交易的条件限制"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"#指定查询对象为华泰证券（601688.XSHG)的受限股份上市公告日期\nq=query(finance.STK_LIMITED_SHARES_LIST).filter(finance.STK_LIMITED_SHARES_LIST.code=='601688.XSHG',finance.STK_LIMITED_SHARES_LIST.pub_date>'2018-01-01')\ndf=finance.run_query(q)\nprint(df)\n\n      id  company_id company_name         code    pub_date   shareholder_name  \\\n0  34395   460000161   华泰证券股份有限公司  601688.XSHG  2018-08-04  阿里巴巴（中国）网络技术有限公司等\n\n  expected_unlimited_date  expected_unlimited_number expected_unlimited_ratio  \\\n0              2019-08-02               1.088731e+09                     None\n\n  actual_unlimited_date actual_unlimited_number actual_unlimited_ratio  \\\n0                  None                    None                   None\n\n   limited_reason_id limited_reason trade_condition\n0             309008        非公开发行限售            None"}
  suggestedFilename: "doc_JQDatadoc_10019_overview_上市公司上市公告日期和预计解禁日期"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10019"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 上市公司上市公告日期和预计解禁日期

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10019

## 描述

描述

## 内容

#### 上市公司上市公告日期和预计解禁日期

- 历史范围：2005年至今；更新时间：交易日24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.STK_LIMITED_SHARES_LIST).filter(finance.STK_LIMITED_SHARES_LIST.code==code).limit(n))
```

描述

- 获取上市公司受限股份上市公告日期和预计解禁日期。

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

上市公司上市公告日期和预计解禁日期参数

- query(finance.STK_LIMITED_SHARES_LIST)：表示从finance.STK_LIMITED_SHARES_LIST这张表中查询上市公司受限股份上市公告和预计解禁的日期，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]
- finance.STK_LIMITED_SHARES_LIST：代表受限股份上市公告日期表，收录了上市公司受限股份上市公告和预计解禁的日期。表结构和字段信息如下：
- filter(finance.STK_LIMITED_SHARES_LIST.code==code)：指定筛选条件，通过finance.STK_LIMITED_SHARES_LIST.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_LIMITED_SHARES_LIST.pub_date>='2015-01-01'，表示筛选公布日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 表字段信息

| 字段名称 | 中文名称 | 字段类型 | 含义 |
| --- | --- | --- | --- |
| company_id | 公司ID | int |  |
| company_name | 公司名称 | varchar(100) |  |
| code | 股票代码 | varchar(12) |  |
| pub_date | 公告日期 | date | 上市流通方案公布日期 |
| shareholder_name | 股东名称 | varchar(100) |  |
| expected_unlimited_date | 预计解除限售日期 | date |  |
| expected_unlimited_number | 预计解除限售数量 | int | 单位：股 |
| expected_unlimited_ratio | 预计解除限售比例 | decimal(10,4) | 单位：％；预计解除限售数量占总股本比例 |
| actual_unlimited_date | 实际解除限售日期 | date |  |
| actual_unlimited_number | 实际解除限售数量 | int | 单位：股 |
| actual_unlimited_ratio | 实际解除限售比例 | decimal(10,4) | 单位：％；实际解除限售数量占总股本比例 |
| limited_reason_id | 限售原因编码 | int | 如下 限售原因编码 |
| limited_reason | 限售原因 | varchar(60) | 用户选择：股改限售；发行限售 |
| trade_condition | 上市交易条件 | varchar(500) | 股份上市交易的条件限制 |

###### 示例

```python
#指定查询对象为华泰证券（601688.XSHG)的受限股份上市公告日期
q=query(finance.STK_LIMITED_SHARES_LIST).filter(finance.STK_LIMITED_SHARES_LIST.code=='601688.XSHG',finance.STK_LIMITED_SHARES_LIST.pub_date>'2018-01-01')
df=finance.run_query(q)
print(df)

      id  company_id company_name         code    pub_date   shareholder_name  \
0  34395   460000161   华泰证券股份有限公司  601688.XSHG  2018-08-04  阿里巴巴（中国）网络技术有限公司等

  expected_unlimited_date  expected_unlimited_number expected_unlimited_ratio  \
0              2019-08-02               1.088731e+09                     None

  actual_unlimited_date actual_unlimited_number actual_unlimited_ratio  \
0                  None                    None                   None

   limited_reason_id limited_reason trade_condition
0             309008        非公开发行限售            None
```
