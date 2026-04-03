---
id: "url-36497ae0"
type: "website"
title: "上市公司状态变动"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10023"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:45:15.378Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10023"
  headings:
    - {"level":3,"text":"上市公司状态变动","id":""}
    - {"level":5,"text":"表字段信息","id":""}
    - {"level":5,"text":"报表来源编码","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "公司状态变动参数"
    - "母公司利润表参数"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"ul","items":["获取上市公司已发行未上市、正常上市、实行ST、*ST、暂停上市、终止上市的变动情况等"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.finance.STK_STATUS_CHANGE)：表示从finance.STK_STATUS_CHANGE这张表中查询上市公司的状态变动信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：:[query简易教程]","finance.STK_STATUS_CHANGE：代表上市公司状态变动表，收录了上市公司已发行未上市、正常上市、实行ST、*ST、暂停上市、终止上市的变动情况等，**表结构和字段信息如下**：","filter(finance.STK_INCOME_STATEMENT_PARENT.code==code)：指定筛选条件，通过finance.STK_INCOME_STATEMENT.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_INCOME_STATEMENT.pub_date>='2015-01-01'，表示公告日期大于2015年1月1日上市公司公布的合并利润表信息；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"ul","items":["query(finance.STK_STATUS_CHANGE)：表示从finance.STK_STATUS_CHANGE这张表中查询上市公司的状态变动信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","STK_INCOME_STATEMENT_PARENT：代表上市公司母公司利润表，收录了上市公司母公司的利润信息，表结构和字段信息如下：","filter(finance.STK_STATUS_CHANGE.code==code)：指定筛选条件，通过finance.STK_STATUS_CHANGE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_STATUS_CHANGE.pub_date>='2015-01-01'，表示筛选公告日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"ul","items":["获取上市公司状态变动"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型","备注/示例"],"rows":[["company_id","机构ID","int",""],["code","股票代码","varchar(12)",""],["name","股票名称","varchar(40)",""],["pub_date","公告日期","date",""],["change_date","变更日期（实际）","date",""],["public_status_id","上市状态编码","int","如下上市状态编码"],["public_status","上市状态","varchar(32)",""],["change_reason","变更原因","varchar(500)",""],["change_type_id","变更类型编码","int","如下变更类型编码"],["change_type","变更类型","varchar(60)",""],["comments","备注","varchar(255)",""]]}
    - {"caption":"","headers":["上市状态编码","上市状态"],"rows":[["301001","正常上市"],["301002","ST"],["301003","*ST"],["301004","暂停上市"],["301005","进入退市整理期"],["301006","终止上市"],["301007","已发行未上市"],["301008","预披露"],["301009","未过会"],["301010","发行失败"],["301011","暂缓发行"],["301012","暂缓上市"],["301013","停止转让"],["301014","正常转让"],["301015","实行投资者适当性管理表示"],["301099","其他"]]}
    - {"caption":"","headers":["变更类型编码","变更类型"],"rows":[["303001","恢复上市"],["303002","摘星"],["303003","摘帽"],["303004","摘星摘帽"],["303005","披星"],["303006","戴帽"],["303007","戴帽披星"],["303008","拟上市"],["303009","新股上市"],["303010","发行失败"],["303011","暂停上市"],["303012","终止上市"],["303013","退市整理"],["303014","暂缓发行"],["303015","暂缓上市"],["303016","实行投资者适当性管理标识"],["303017","未过会"],["303018","预披露"],["303019","正常转让"],["303020","停止转让"],["303021","重新上市"],["303099","其他"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_STATUS_CHANGE).filter(finance.STK_STATUS_CHANGE.code==code).limit(n))"}
    - {"language":"python","code":"# 指定查询对象为恒瑞医药（600276.XSHG)的上市公司状态变动\nq=query(finance.STK_STATUS_CHANGE).filter(finance.STK_STATUS_CHANGE.code=='600276.XSHG').limit(10)\ndf=finance.run_query(q)\nprint(df)\n\n     id   company_id         code     name   pub_date    public_status_id  \\\n0  2840    420600276  600276.XSHG  恒瑞医药  2000-10-18             301001\n\n  public_status   change_date  change_reason  change_type_id   change_type  comments\n0       正常上市    2000-10-18            NaN           303009      新股上市      NaN"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"上市公司状态变动"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_STATUS_CHANGE).filter(finance.STK_STATUS_CHANGE.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取上市公司已发行未上市、正常上市、实行ST、*ST、暂停上市、终止上市的变动情况等"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"公司状态变动参数"}
    - {"type":"list","listType":"ul","items":["query(finance.finance.STK_STATUS_CHANGE)：表示从finance.STK_STATUS_CHANGE这张表中查询上市公司的状态变动信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：:[query简易教程]","finance.STK_STATUS_CHANGE：代表上市公司状态变动表，收录了上市公司已发行未上市、正常上市、实行ST、*ST、暂停上市、终止上市的变动情况等，**表结构和字段信息如下**：","filter(finance.STK_INCOME_STATEMENT_PARENT.code==code)：指定筛选条件，通过finance.STK_INCOME_STATEMENT.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_INCOME_STATEMENT.pub_date>='2015-01-01'，表示公告日期大于2015年1月1日上市公司公布的合并利润表信息；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"paragraph","content":"母公司利润表参数"}
    - {"type":"list","listType":"ul","items":["query(finance.STK_STATUS_CHANGE)：表示从finance.STK_STATUS_CHANGE这张表中查询上市公司的状态变动信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","STK_INCOME_STATEMENT_PARENT：代表上市公司母公司利润表，收录了上市公司母公司的利润信息，表结构和字段信息如下：","filter(finance.STK_STATUS_CHANGE.code==code)：指定筛选条件，通过finance.STK_STATUS_CHANGE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_STATUS_CHANGE.pub_date>='2015-01-01'，表示筛选公告日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"表字段信息"}
    - {"type":"table","headers":["字段名称","中文名称","字段类型","备注/示例"],"rows":[["company_id","机构ID","int",""],["code","股票代码","varchar(12)",""],["name","股票名称","varchar(40)",""],["pub_date","公告日期","date",""],["change_date","变更日期（实际）","date",""],["public_status_id","上市状态编码","int","如下上市状态编码"],["public_status","上市状态","varchar(32)",""],["change_reason","变更原因","varchar(500)",""],["change_type_id","变更类型编码","int","如下变更类型编码"],["change_type","变更类型","varchar(60)",""],["comments","备注","varchar(255)",""]]}
    - {"type":"heading","level":5,"content":"报表来源编码"}
    - {"type":"table","headers":["上市状态编码","上市状态"],"rows":[["301001","正常上市"],["301002","ST"],["301003","*ST"],["301004","暂停上市"],["301005","进入退市整理期"],["301006","终止上市"],["301007","已发行未上市"],["301008","预披露"],["301009","未过会"],["301010","发行失败"],["301011","暂缓发行"],["301012","暂缓上市"],["301013","停止转让"],["301014","正常转让"],["301015","实行投资者适当性管理表示"],["301099","其他"]]}
    - {"type":"table","headers":["变更类型编码","变更类型"],"rows":[["303001","恢复上市"],["303002","摘星"],["303003","摘帽"],["303004","摘星摘帽"],["303005","披星"],["303006","戴帽"],["303007","戴帽披星"],["303008","拟上市"],["303009","新股上市"],["303010","发行失败"],["303011","暂停上市"],["303012","终止上市"],["303013","退市整理"],["303014","暂缓发行"],["303015","暂缓上市"],["303016","实行投资者适当性管理标识"],["303017","未过会"],["303018","预披露"],["303019","正常转让"],["303020","停止转让"],["303021","重新上市"],["303099","其他"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获取上市公司状态变动"]}
    - {"type":"codeblock","language":"python","content":"# 指定查询对象为恒瑞医药（600276.XSHG)的上市公司状态变动\nq=query(finance.STK_STATUS_CHANGE).filter(finance.STK_STATUS_CHANGE.code=='600276.XSHG').limit(10)\ndf=finance.run_query(q)\nprint(df)\n\n     id   company_id         code     name   pub_date    public_status_id  \\\n0  2840    420600276  600276.XSHG  恒瑞医药  2000-10-18             301001\n\n  public_status   change_date  change_reason  change_type_id   change_type  comments\n0       正常上市    2000-10-18            NaN           303009      新股上市      NaN"}
  suggestedFilename: "doc_JQDatadoc_10023_overview_上市公司状态变动"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10023"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 上市公司状态变动

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10023

## 描述

描述

## 内容

#### 上市公司状态变动

- 历史范围：2005年至今；更新时间：交易日24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.STK_STATUS_CHANGE).filter(finance.STK_STATUS_CHANGE.code==code).limit(n))
```

描述

- 获取上市公司已发行未上市、正常上市、实行ST、*ST、暂停上市、终止上市的变动情况等

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

公司状态变动参数

- query(finance.finance.STK_STATUS_CHANGE)：表示从finance.STK_STATUS_CHANGE这张表中查询上市公司的状态变动信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：:[query简易教程]
- finance.STK_STATUS_CHANGE：代表上市公司状态变动表，收录了上市公司已发行未上市、正常上市、实行ST、*ST、暂停上市、终止上市的变动情况等，**表结构和字段信息如下**：
- filter(finance.STK_INCOME_STATEMENT_PARENT.code==code)：指定筛选条件，通过finance.STK_INCOME_STATEMENT.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_INCOME_STATEMENT.pub_date>='2015-01-01'，表示公告日期大于2015年1月1日上市公司公布的合并利润表信息；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

母公司利润表参数

- query(finance.STK_STATUS_CHANGE)：表示从finance.STK_STATUS_CHANGE这张表中查询上市公司的状态变动信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]
- STK_INCOME_STATEMENT_PARENT：代表上市公司母公司利润表，收录了上市公司母公司的利润信息，表结构和字段信息如下：
- filter(finance.STK_STATUS_CHANGE.code==code)：指定筛选条件，通过finance.STK_STATUS_CHANGE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_STATUS_CHANGE.pub_date>='2015-01-01'，表示筛选公告日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 表字段信息

| 字段名称 | 中文名称 | 字段类型 | 备注/示例 |
| --- | --- | --- | --- |
| company_id | 机构ID | int |  |
| code | 股票代码 | varchar(12) |  |
| name | 股票名称 | varchar(40) |  |
| pub_date | 公告日期 | date |  |
| change_date | 变更日期（实际） | date |  |
| public_status_id | 上市状态编码 | int | 如下上市状态编码 |
| public_status | 上市状态 | varchar(32) |  |
| change_reason | 变更原因 | varchar(500) |  |
| change_type_id | 变更类型编码 | int | 如下变更类型编码 |
| change_type | 变更类型 | varchar(60) |  |
| comments | 备注 | varchar(255) |  |

###### 报表来源编码

| 上市状态编码 | 上市状态 |
| --- | --- |
| 301001 | 正常上市 |
| 301002 | ST |
| 301003 | *ST |
| 301004 | 暂停上市 |
| 301005 | 进入退市整理期 |
| 301006 | 终止上市 |
| 301007 | 已发行未上市 |
| 301008 | 预披露 |
| 301009 | 未过会 |
| 301010 | 发行失败 |
| 301011 | 暂缓发行 |
| 301012 | 暂缓上市 |
| 301013 | 停止转让 |
| 301014 | 正常转让 |
| 301015 | 实行投资者适当性管理表示 |
| 301099 | 其他 |

| 变更类型编码 | 变更类型 |
| --- | --- |
| 303001 | 恢复上市 |
| 303002 | 摘星 |
| 303003 | 摘帽 |
| 303004 | 摘星摘帽 |
| 303005 | 披星 |
| 303006 | 戴帽 |
| 303007 | 戴帽披星 |
| 303008 | 拟上市 |
| 303009 | 新股上市 |
| 303010 | 发行失败 |
| 303011 | 暂停上市 |
| 303012 | 终止上市 |
| 303013 | 退市整理 |
| 303014 | 暂缓发行 |
| 303015 | 暂缓上市 |
| 303016 | 实行投资者适当性管理标识 |
| 303017 | 未过会 |
| 303018 | 预披露 |
| 303019 | 正常转让 |
| 303020 | 停止转让 |
| 303021 | 重新上市 |
| 303099 | 其他 |

###### 示例

- 获取上市公司状态变动

```python
# 指定查询对象为恒瑞医药（600276.XSHG)的上市公司状态变动
q=query(finance.STK_STATUS_CHANGE).filter(finance.STK_STATUS_CHANGE.code=='600276.XSHG').limit(10)
df=finance.run_query(q)
print(df)

     id   company_id         code     name   pub_date    public_status_id  \
0  2840    420600276  600276.XSHG  恒瑞医药  2000-10-18             301001

  public_status   change_date  change_reason  change_type_id   change_type  comments
0       正常上市    2000-10-18            NaN           303009      新股上市      NaN
```
