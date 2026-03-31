---
id: "url-7a226b4b"
type: "website"
title: "市场通十大成交活跃股"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9871"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:18:09.255Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9871"
  headings:
    - {"level":3,"text":"市场通十大成交活跃股","id":""}
    - {"level":5,"text":"表字段信息","id":""}
    - {"level":5,"text":"市场通编码","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：交易日20:30-06:30更新"]}
    - {"type":"ul","items":["统计沪港通、深港通和港股通前十大交易活跃股的交易状况。"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.STK_EL_TOP_ACTIVATE)：表示从finance.STK_EL_TOP_ACTIVATE这张表中查询沪港通、深港通和港股通前十大交易活跃股的交易状况，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_EL_TOP_ACTIVATE：代表市场通十大成交活跃股数据表，统计沪港通、深港通和港股通前十大交易活跃股的交易状况，包括买入金额，卖出金额等，表结构和字段信息如下:","filter(finance.STK_EL_TOP_ACTIVATE.code==code)：指定筛选条件，通过finance.STK_EL_TOP_ACTIVATE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_EL_TOP_ACTIVATE.day>='2015-01-01'，表示筛选日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段","名称","类型","非空","交易所","备注/示例"],"rows":[["day","日期","date","Y","",""],["link_id","市场通编码","int","Y","",""],["link_name","市场通名称","varchar(32)","Y","包括以下四个名称：沪股通， 深股通， 港股通(沪)，港股通(深)",""],["rank","排名","int","Y","",""],["code","股票代码","varchar(12)","Y","",""],["name","股票名称","varchar(100)","Y","",""],["exchange","交易所名称","varchar(12)","Y","",""],["buy","买入金额(元)","decimal(20, 4)","Y","(北向自2024-08-18之后不再披露)",""],["sell","卖出金额(元)","decimal(20, 4)","Y","(北向自2024-08-18之后不再披露)",""],["total","买入及卖出金额(元)","decimal(20, 4)","Y","",""]]}
    - {"caption":"","headers":["市场通编码","市场通名称"],"rows":[["310001","沪股通"],["310002","深股通"],["310003","港股通（沪）"],["310004","港股通（深）"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance finance.run_query(query(finance.STK_EL_TOP_ACTIVATE).filter(finance.STK_EL_TOP_ACTIVATE.code==code).limit(n))"}
    - {"language":"python","code":"q=query(finance.STK_EL_TOP_ACTIVATE).filter(finance.STK_EL_TOP_ACTIVATE.code=='000002.XSHE').limit(10)\ndf=finance.run_query(q)\nprint(df)\n\n       id         day  link_id link_name  rank         code name exchange  \\\n0  323010  2018-01-15   310002       深股通     2  000002.XSHE  万科Ａ      深交所   \n1  323050  2018-01-16   310002       深股通     2  000002.XSHE  万科Ａ      深交所   \n2  323089  2018-01-17   310002       深股通     1  000002.XSHE  万科Ａ      深交所   \n3  323132  2018-01-18   310002       深股通     4  000002.XSHE  万科Ａ      深交所   \n4  323213  2018-01-23   310002       深股通     6  000002.XSHE  万科Ａ      深交所   \n5  323254  2018-01-24   310002       深股通     7  000002.XSHE  万科Ａ      深交所   \n6  341170  2018-01-25   310002       深股通     7  000002.XSHE  万科Ａ      深交所   \n7  341209  2018-01-26   310002       深股通     6  000002.XSHE  万科Ａ      深交所   \n8  341248  2018-01-29   310002       深股通     5  000002.XSHE  万科Ａ      深交所   \n9  341444  2018-01-30   310002       深股通     5  000002.XSHE  万科Ａ      深交所   \n\n           buy         sell        total  \n0  124497968.0  326656496.0  451154464.0  \n1  127460061.0  465933921.0  593393982.0  \n2  157676630.0  542617116.0  700293746.0  \n3  203996076.0  105819761.0  309815837.0  \n4  141515523.0  190282952.0  331798475.0  \n5  110052973.0  163321615.0  273374588.0  \n6  179785644.0  120157651.0  299943295.0  \n7  166750550.0   78471253.0  245221803.0  \n8  157899558.0  170790111.0  328689669.0  \n9  201547219.0  165714289.0  367261508.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"市场通十大成交活跃股"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：交易日20:30-06:30更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance finance.run_query(query(finance.STK_EL_TOP_ACTIVATE).filter(finance.STK_EL_TOP_ACTIVATE.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["统计沪港通、深港通和港股通前十大交易活跃股的交易状况。"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["query(finance.STK_EL_TOP_ACTIVATE)：表示从finance.STK_EL_TOP_ACTIVATE这张表中查询沪港通、深港通和港股通前十大交易活跃股的交易状况，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]","finance.STK_EL_TOP_ACTIVATE：代表市场通十大成交活跃股数据表，统计沪港通、深港通和港股通前十大交易活跃股的交易状况，包括买入金额，卖出金额等，表结构和字段信息如下:","filter(finance.STK_EL_TOP_ACTIVATE.code==code)：指定筛选条件，通过finance.STK_EL_TOP_ACTIVATE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_EL_TOP_ACTIVATE.day>='2015-01-01'，表示筛选日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"heading","level":5,"content":"表字段信息"}
    - {"type":"table","headers":["字段","名称","类型","非空","交易所","备注/示例"],"rows":[["day","日期","date","Y","",""],["link_id","市场通编码","int","Y","",""],["link_name","市场通名称","varchar(32)","Y","包括以下四个名称：沪股通， 深股通， 港股通(沪)，港股通(深)",""],["rank","排名","int","Y","",""],["code","股票代码","varchar(12)","Y","",""],["name","股票名称","varchar(100)","Y","",""],["exchange","交易所名称","varchar(12)","Y","",""],["buy","买入金额(元)","decimal(20, 4)","Y","(北向自2024-08-18之后不再披露)",""],["sell","卖出金额(元)","decimal(20, 4)","Y","(北向自2024-08-18之后不再披露)",""],["total","买入及卖出金额(元)","decimal(20, 4)","Y","",""]]}
    - {"type":"heading","level":5,"content":"市场通编码"}
    - {"type":"table","headers":["市场通编码","市场通名称"],"rows":[["310001","沪股通"],["310002","深股通"],["310003","港股通（沪）"],["310004","港股通（深）"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"q=query(finance.STK_EL_TOP_ACTIVATE).filter(finance.STK_EL_TOP_ACTIVATE.code=='000002.XSHE').limit(10)\ndf=finance.run_query(q)\nprint(df)\n\n       id         day  link_id link_name  rank         code name exchange  \\\n0  323010  2018-01-15   310002       深股通     2  000002.XSHE  万科Ａ      深交所   \n1  323050  2018-01-16   310002       深股通     2  000002.XSHE  万科Ａ      深交所   \n2  323089  2018-01-17   310002       深股通     1  000002.XSHE  万科Ａ      深交所   \n3  323132  2018-01-18   310002       深股通     4  000002.XSHE  万科Ａ      深交所   \n4  323213  2018-01-23   310002       深股通     6  000002.XSHE  万科Ａ      深交所   \n5  323254  2018-01-24   310002       深股通     7  000002.XSHE  万科Ａ      深交所   \n6  341170  2018-01-25   310002       深股通     7  000002.XSHE  万科Ａ      深交所   \n7  341209  2018-01-26   310002       深股通     6  000002.XSHE  万科Ａ      深交所   \n8  341248  2018-01-29   310002       深股通     5  000002.XSHE  万科Ａ      深交所   \n9  341444  2018-01-30   310002       深股通     5  000002.XSHE  万科Ａ      深交所   \n\n           buy         sell        total  \n0  124497968.0  326656496.0  451154464.0  \n1  127460061.0  465933921.0  593393982.0  \n2  157676630.0  542617116.0  700293746.0  \n3  203996076.0  105819761.0  309815837.0  \n4  141515523.0  190282952.0  331798475.0  \n5  110052973.0  163321615.0  273374588.0  \n6  179785644.0  120157651.0  299943295.0  \n7  166750550.0   78471253.0  245221803.0  \n8  157899558.0  170790111.0  328689669.0  \n9  201547219.0  165714289.0  367261508.0"}
  suggestedFilename: "doc_JQDatadoc_9871_overview_市场通十大成交活跃股"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9871"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 市场通十大成交活跃股

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9871

## 描述

描述

## 内容

#### 市场通十大成交活跃股

- 历史范围：上市至今；更新时间：交易日20:30-06:30更新

```python
from jqdatasdk import finance finance.run_query(query(finance.STK_EL_TOP_ACTIVATE).filter(finance.STK_EL_TOP_ACTIVATE.code==code).limit(n))
```

描述

- 统计沪港通、深港通和港股通前十大交易活跃股的交易状况。

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

参数

- query(finance.STK_EL_TOP_ACTIVATE)：表示从finance.STK_EL_TOP_ACTIVATE这张表中查询沪港通、深港通和港股通前十大交易活跃股的交易状况，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用英文逗号进行分隔；query函数的更多用法详见：[query简易教程]
- finance.STK_EL_TOP_ACTIVATE：代表市场通十大成交活跃股数据表，统计沪港通、深港通和港股通前十大交易活跃股的交易状况，包括买入金额，卖出金额等，表结构和字段信息如下:
- filter(finance.STK_EL_TOP_ACTIVATE.code==code)：指定筛选条件，通过finance.STK_EL_TOP_ACTIVATE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_EL_TOP_ACTIVATE.day>='2015-01-01'，表示筛选日期大于等于2015年1月1日之后的数据；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

###### 表字段信息

| 字段 | 名称 | 类型 | 非空 | 交易所 | 备注/示例 |
| --- | --- | --- | --- | --- | --- |
| day | 日期 | date | Y |  |  |
| link_id | 市场通编码 | int | Y |  |  |
| link_name | 市场通名称 | varchar(32) | Y | 包括以下四个名称：沪股通， 深股通， 港股通(沪)，港股通(深) |  |
| rank | 排名 | int | Y |  |  |
| code | 股票代码 | varchar(12) | Y |  |  |
| name | 股票名称 | varchar(100) | Y |  |  |
| exchange | 交易所名称 | varchar(12) | Y |  |  |
| buy | 买入金额(元) | decimal(20, 4) | Y | (北向自2024-08-18之后不再披露) |  |
| sell | 卖出金额(元) | decimal(20, 4) | Y | (北向自2024-08-18之后不再披露) |  |
| total | 买入及卖出金额(元) | decimal(20, 4) | Y |  |  |

###### 市场通编码

| 市场通编码 | 市场通名称 |
| --- | --- |
| 310001 | 沪股通 |
| 310002 | 深股通 |
| 310003 | 港股通（沪） |
| 310004 | 港股通（深） |

###### 示例

```python
q=query(finance.STK_EL_TOP_ACTIVATE).filter(finance.STK_EL_TOP_ACTIVATE.code=='000002.XSHE').limit(10)
df=finance.run_query(q)
print(df)

       id         day  link_id link_name  rank         code name exchange  \
0  323010  2018-01-15   310002       深股通     2  000002.XSHE  万科Ａ      深交所   
1  323050  2018-01-16   310002       深股通     2  000002.XSHE  万科Ａ      深交所   
2  323089  2018-01-17   310002       深股通     1  000002.XSHE  万科Ａ      深交所   
3  323132  2018-01-18   310002       深股通     4  000002.XSHE  万科Ａ      深交所   
4  323213  2018-01-23   310002       深股通     6  000002.XSHE  万科Ａ      深交所   
5  323254  2018-01-24   310002       深股通     7  000002.XSHE  万科Ａ      深交所   
6  341170  2018-01-25   310002       深股通     7  000002.XSHE  万科Ａ      深交所   
7  341209  2018-01-26   310002       深股通     6  000002.XSHE  万科Ａ      深交所   
8  341248  2018-01-29   310002       深股通     5  000002.XSHE  万科Ａ      深交所   
9  341444  2018-01-30   310002       深股通     5  000002.XSHE  万科Ａ      深交所   

           buy         sell        total  
0  124497968.0  326656496.0  451154464.0  
1  127460061.0  465933921.0  593393982.0  
2  157676630.0  542617116.0  700293746.0  
3  203996076.0  105819761.0  309815837.0  
4  141515523.0  190282952.0  331798475.0  
5  110052973.0  163321615.0  273374588.0  
6  179785644.0  120157651.0  299943295.0  
7  166750550.0   78471253.0  245221803.0  
8  157899558.0  170790111.0  328689669.0  
9  201547219.0  165714289.0  367261508.0
```
