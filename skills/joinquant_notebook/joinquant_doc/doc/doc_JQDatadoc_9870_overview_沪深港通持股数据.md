---
id: "url-7a226b4a"
type: "website"
title: "沪深港通持股数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9870"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:18:05.326Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9870"
  headings:
    - {"level":3,"text":"沪深港通持股数据","id":""}
    - {"level":5,"text":"表字段信息","id":""}
    - {"level":5,"text":"市场通编码","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：交易日20:30-06:30更新"]}
    - {"type":"ul","items":["记录了北向资金（沪股通、深股通）和南向资金港股通的持股数量和持股比例"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.STK_HK_HOLD_INFO)：表示从finance.STK_HK_HOLD_INFO这张表中查询沪深港通的持股数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号分隔进行提取；如query(finance.STK_HK_HOLD_INFO.code)。query函数的更多用法详见：[query简易教程]","finance.STK_HK_HOLD_INFO：收录了沪深港通每日的持股数量和持股比例数据，表结构和字段信息如下:","filter(finance.STK_HK_HOLD_INFO.link_id==310001)：指定筛选条件，通过finance.STK_HK_HOLD_INFO.link_id==310001可以指定查询沪股通的持股数据；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_HK_HOLD_INFO.day=='2019-03-01'，指定获取2019年3月1日的沪深港通持股数据。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型","能否为空","注释"],"rows":[["day","日期","date","N","(北向自2024-08-18之后按季度披露)"],["link_id","市场通编码","int","N","三种类型：310001-沪股通，310002-深股通，310005-港股通"],["link_name","市场通名称","varchar(32)","N","三种类型：沪股通，深股通，港股通"],["code","股票代码","varchar(12)","N",""],["name","股票名称","varchar(100)","N",""],["share_number","持股数量","int","单位：股，于中央结算系统的持股量",""],["share_ratio","持股比例","decimal(10,4)","单位：％，沪股通：占于上交所上市及交易的A股总数的百分比；深股通：占于深交所上市及交易的A股总数的百分比；港股通：占已发行股份百分比",""]]}
    - {"caption":"","headers":["市场通编码","市场通名称"],"rows":[["310001","沪股通"],["310002","深股通"],["310005","港股通"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\ndf=finance.run_query(query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.link_id==310001))\nprint(df)"}
    - {"language":"python","code":"#获取北向资金沪股通的持股数据\ndf=finance.run_query(query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.link_id==310001).order_by(finance.STK_HK_HOLD_INFO.day.desc()))\nprint(df[:4])\n\n        id         day  link_id link_name         code  name  share_number  \\\n0  3070982  2021-03-20   310001       沪股通  605222.XSHG  起帆电缆        161022   \n1  3070981  2021-03-20   310001       沪股通  605199.XSHG   葫芦娃         66103   \n2  3070980  2021-03-20   310001       沪股通  605198.XSHG  德利股份         90174   \n3  3070979  2021-03-20   310001       沪股通  605168.XSHG   三人行        269393   \n\n   share_ratio  \n0         0.32  \n1         0.16  \n2         0.45  \n3         1.56"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"沪深港通持股数据"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：交易日20:30-06:30更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\ndf=finance.run_query(query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.link_id==310001))\nprint(df)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["记录了北向资金（沪股通、深股通）和南向资金港股通的持股数量和持股比例"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["query(finance.STK_HK_HOLD_INFO)：表示从finance.STK_HK_HOLD_INFO这张表中查询沪深港通的持股数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号分隔进行提取；如query(finance.STK_HK_HOLD_INFO.code)。query函数的更多用法详见：[query简易教程]","finance.STK_HK_HOLD_INFO：收录了沪深港通每日的持股数量和持股比例数据，表结构和字段信息如下:","filter(finance.STK_HK_HOLD_INFO.link_id==310001)：指定筛选条件，通过finance.STK_HK_HOLD_INFO.link_id==310001可以指定查询沪股通的持股数据；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_HK_HOLD_INFO.day=='2019-03-01'，指定获取2019年3月1日的沪深港通持股数据。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"表字段信息"}
    - {"type":"table","headers":["字段名称","中文名称","字段类型","能否为空","注释"],"rows":[["day","日期","date","N","(北向自2024-08-18之后按季度披露)"],["link_id","市场通编码","int","N","三种类型：310001-沪股通，310002-深股通，310005-港股通"],["link_name","市场通名称","varchar(32)","N","三种类型：沪股通，深股通，港股通"],["code","股票代码","varchar(12)","N",""],["name","股票名称","varchar(100)","N",""],["share_number","持股数量","int","单位：股，于中央结算系统的持股量",""],["share_ratio","持股比例","decimal(10,4)","单位：％，沪股通：占于上交所上市及交易的A股总数的百分比；深股通：占于深交所上市及交易的A股总数的百分比；港股通：占已发行股份百分比",""]]}
    - {"type":"heading","level":5,"content":"市场通编码"}
    - {"type":"table","headers":["市场通编码","市场通名称"],"rows":[["310001","沪股通"],["310002","深股通"],["310005","港股通"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"#获取北向资金沪股通的持股数据\ndf=finance.run_query(query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.link_id==310001).order_by(finance.STK_HK_HOLD_INFO.day.desc()))\nprint(df[:4])\n\n        id         day  link_id link_name         code  name  share_number  \\\n0  3070982  2021-03-20   310001       沪股通  605222.XSHG  起帆电缆        161022   \n1  3070981  2021-03-20   310001       沪股通  605199.XSHG   葫芦娃         66103   \n2  3070980  2021-03-20   310001       沪股通  605198.XSHG  德利股份         90174   \n3  3070979  2021-03-20   310001       沪股通  605168.XSHG   三人行        269393   \n\n   share_ratio  \n0         0.32  \n1         0.16  \n2         0.45  \n3         1.56"}
  suggestedFilename: "doc_JQDatadoc_9870_overview_沪深港通持股数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9870"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 沪深港通持股数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9870

## 描述

描述

## 内容

#### 沪深港通持股数据

- 历史范围：上市至今；更新时间：交易日20:30-06:30更新

```python
from jqdatasdk import finance
df=finance.run_query(query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.link_id==310001))
print(df)
```

描述

- 记录了北向资金（沪股通、深股通）和南向资金港股通的持股数量和持股比例

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

参数

- query(finance.STK_HK_HOLD_INFO)：表示从finance.STK_HK_HOLD_INFO这张表中查询沪深港通的持股数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号分隔进行提取；如query(finance.STK_HK_HOLD_INFO.code)。query函数的更多用法详见：[query简易教程]
- finance.STK_HK_HOLD_INFO：收录了沪深港通每日的持股数量和持股比例数据，表结构和字段信息如下:
- filter(finance.STK_HK_HOLD_INFO.link_id==310001)：指定筛选条件，通过finance.STK_HK_HOLD_INFO.link_id==310001可以指定查询沪股通的持股数据；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_HK_HOLD_INFO.day=='2019-03-01'，指定获取2019年3月1日的沪深港通持股数据。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 表字段信息

| 字段名称 | 中文名称 | 字段类型 | 能否为空 | 注释 |
| --- | --- | --- | --- | --- |
| day | 日期 | date | N | (北向自2024-08-18之后按季度披露) |
| link_id | 市场通编码 | int | N | 三种类型：310001-沪股通，310002-深股通，310005-港股通 |
| link_name | 市场通名称 | varchar(32) | N | 三种类型：沪股通，深股通，港股通 |
| code | 股票代码 | varchar(12) | N |  |
| name | 股票名称 | varchar(100) | N |  |
| share_number | 持股数量 | int | 单位：股，于中央结算系统的持股量 |  |
| share_ratio | 持股比例 | decimal(10,4) | 单位：％，沪股通：占于上交所上市及交易的A股总数的百分比；深股通：占于深交所上市及交易的A股总数的百分比；港股通：占已发行股份百分比 |  |

###### 市场通编码

| 市场通编码 | 市场通名称 |
| --- | --- |
| 310001 | 沪股通 |
| 310002 | 深股通 |
| 310005 | 港股通 |

###### 示例

```python
#获取北向资金沪股通的持股数据
df=finance.run_query(query(finance.STK_HK_HOLD_INFO).filter(finance.STK_HK_HOLD_INFO.link_id==310001).order_by(finance.STK_HK_HOLD_INFO.day.desc()))
print(df[:4])

        id         day  link_id link_name         code  name  share_number  \
0  3070982  2021-03-20   310001       沪股通  605222.XSHG  起帆电缆        161022   
1  3070981  2021-03-20   310001       沪股通  605199.XSHG   葫芦娃         66103   
2  3070980  2021-03-20   310001       沪股通  605198.XSHG  德利股份         90174   
3  3070979  2021-03-20   310001       沪股通  605168.XSHG   三人行        269393   

   share_ratio  
0         0.32  
1         0.16  
2         0.45  
3         1.56
```
