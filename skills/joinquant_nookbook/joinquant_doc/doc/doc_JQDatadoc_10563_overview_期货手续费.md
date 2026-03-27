---
id: "url-3649679f"
type: "website"
title: "期货手续费"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10563"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:47:25.399Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10563"
  headings:
    - {"level":3,"text":"期货手续费","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回结果"
    - "注意"
    - "query函数的使用技巧"
    - "字段设计"
    - "示例："
  lists:
    - {"type":"ul","items":["历史范围：2013-01-01 至今；更新时间：17:00 按实际披露更新当天, 20:30按公告推算填充下一交易日"]}
    - {"type":"ul","items":["描述：获取期货手续费。注意这是结算参数，正常是盘后更新，但是盘前也可以根据公告推导,因此盘前(含夜盘)是推算得到的，准确的结算参数需要在盘后 17:00 之后获取"]}
    - {"type":"ul","items":["query(finance.FUT_CHARGE)：表示从finance.FUT_CHARGE这张表中查询期货手续费数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：sqlalchemy.orm.query.Query对象","finance.FUT_CHARGE：收录了期货手续费数据，表结构和字段信息如下：","filter(finance.FUT_CHARGE.code==code)：指定筛选条件，通过finance.FUT_CHARGE.code==code可以指定你想要查询的标的；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称/li>"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型","注释"],"rows":[["day","日期","date",""],["code","标的代码","varchar(12)",""],["exchange","交易所编码","varchar(10)","英文编码"],["exchange_name","交易所名称","varchar(30)",""],["unit","计量单位","varchar(10)","'元/手' 或者 '‱'"],["clearance_charge","平仓手续费","DECIMAL(19, 4)","上期所/能源中心,郑商所,中金所为交易手续费"],["opening_charge","开仓手续费","DECIMAL(19, 4)","上期所//能源中心,郑商所,中金所不支持 , (大商所和广期所一般等于平仓手续费)"],["short_clearance_charge","短平手续费","DECIMAL(19, 4)","大商所和广期所是短平手续费,郑商所为平今,上期货//能源中心和中金所根据折扣率换算"],["short_opening_charge","短开手续费","DECIMAL(19, 4)","仅大商所(一般等于短平)和广期所支持"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUT_CHARGE).filter(finance.FUT_CHARGE.day==date).limit(n))"}
    - {"language":"python","code":"#查询SI2312的2022年12月22日的手续费数据\nfrom jqdatasdk import finance\ndf = finance.run_query(query(finance.FUT_CHARGE).filter(finance.FUT_CHARGE.day == '2022-12-22',\n                                                  finance.FUT_CHARGE.code == \"SI2312.GFEX\"\n                                                  ))\nprint(df)\n\n        id        date  ... short_clearance_charge short_opening_charge\n0  1389520  2022-12-22  ...                    1.0                  1.0\n\n[1 rows x 10 columns]"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"期货手续费"}
    - {"type":"list","listType":"ul","items":["历史范围：2013-01-01 至今；更新时间：17:00 按实际披露更新当天, 20:30按公告推算填充下一交易日"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUT_CHARGE).filter(finance.FUT_CHARGE.day==date).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["描述：获取期货手续费。注意这是结算参数，正常是盘后更新，但是盘前也可以根据公告推导,因此盘前(含夜盘)是推算得到的，准确的结算参数需要在盘后 17:00 之后获取"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["query(finance.FUT_CHARGE)：表示从finance.FUT_CHARGE这张表中查询期货手续费数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：sqlalchemy.orm.query.Query对象","finance.FUT_CHARGE：收录了期货手续费数据，表结构和字段信息如下：","filter(finance.FUT_CHARGE.code==code)：指定筛选条件，通过finance.FUT_CHARGE.code==code可以指定你想要查询的标的；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"paragraph","content":"返回结果"}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称/li>"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"paragraph","content":"query函数的使用技巧"}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"字段设计"}
    - {"type":"table","headers":["字段名称","中文名称","字段类型","注释"],"rows":[["day","日期","date",""],["code","标的代码","varchar(12)",""],["exchange","交易所编码","varchar(10)","英文编码"],["exchange_name","交易所名称","varchar(30)",""],["unit","计量单位","varchar(10)","'元/手' 或者 '‱'"],["clearance_charge","平仓手续费","DECIMAL(19, 4)","上期所/能源中心,郑商所,中金所为交易手续费"],["opening_charge","开仓手续费","DECIMAL(19, 4)","上期所//能源中心,郑商所,中金所不支持 , (大商所和广期所一般等于平仓手续费)"],["short_clearance_charge","短平手续费","DECIMAL(19, 4)","大商所和广期所是短平手续费,郑商所为平今,上期货//能源中心和中金所根据折扣率换算"],["short_opening_charge","短开手续费","DECIMAL(19, 4)","仅大商所(一般等于短平)和广期所支持"]]}
    - {"type":"paragraph","content":"示例："}
    - {"type":"codeblock","language":"python","content":"#查询SI2312的2022年12月22日的手续费数据\nfrom jqdatasdk import finance\ndf = finance.run_query(query(finance.FUT_CHARGE).filter(finance.FUT_CHARGE.day == '2022-12-22',\n                                                  finance.FUT_CHARGE.code == \"SI2312.GFEX\"\n                                                  ))\nprint(df)\n\n        id        date  ... short_clearance_charge short_opening_charge\n0  1389520  2022-12-22  ...                    1.0                  1.0\n\n[1 rows x 10 columns]"}
  suggestedFilename: "doc_JQDatadoc_10563_overview_期货手续费"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10563"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 期货手续费

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10563

## 描述

描述

## 内容

#### 期货手续费

- 历史范围：2013-01-01 至今；更新时间：17:00 按实际披露更新当天, 20:30按公告推算填充下一交易日

```python
from jqdatasdk import finance
finance.run_query(query(finance.FUT_CHARGE).filter(finance.FUT_CHARGE.day==date).limit(n))
```

描述

- 描述：获取期货手续费。注意这是结算参数，正常是盘后更新，但是盘前也可以根据公告推导,因此盘前(含夜盘)是推算得到的，准确的结算参数需要在盘后 17:00 之后获取

参数

- query(finance.FUT_CHARGE)：表示从finance.FUT_CHARGE这张表中查询期货手续费数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：sqlalchemy.orm.query.Query对象
- finance.FUT_CHARGE：收录了期货手续费数据，表结构和字段信息如下：
- filter(finance.FUT_CHARGE.code==code)：指定筛选条件，通过finance.FUT_CHARGE.code==code可以指定你想要查询的标的；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

返回结果

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称/li>

注意

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

query函数的使用技巧

- query函数的更多用法详见：query简易教程

字段设计

| 字段名称 | 中文名称 | 字段类型 | 注释 |
| --- | --- | --- | --- |
| day | 日期 | date |  |
| code | 标的代码 | varchar(12) |  |
| exchange | 交易所编码 | varchar(10) | 英文编码 |
| exchange_name | 交易所名称 | varchar(30) |  |
| unit | 计量单位 | varchar(10) | '元/手' 或者 '‱' |
| clearance_charge | 平仓手续费 | DECIMAL(19, 4) | 上期所/能源中心,郑商所,中金所为交易手续费 |
| opening_charge | 开仓手续费 | DECIMAL(19, 4) | 上期所//能源中心,郑商所,中金所不支持 , (大商所和广期所一般等于平仓手续费) |
| short_clearance_charge | 短平手续费 | DECIMAL(19, 4) | 大商所和广期所是短平手续费,郑商所为平今,上期货//能源中心和中金所根据折扣率换算 |
| short_opening_charge | 短开手续费 | DECIMAL(19, 4) | 仅大商所(一般等于短平)和广期所支持 |

示例：

```python
#查询SI2312的2022年12月22日的手续费数据
from jqdatasdk import finance
df = finance.run_query(query(finance.FUT_CHARGE).filter(finance.FUT_CHARGE.day == '2022-12-22',
                                                  finance.FUT_CHARGE.code == "SI2312.GFEX"
                                                  ))
print(df)

        id        date  ... short_clearance_charge short_opening_charge
0  1389520  2022-12-22  ...                    1.0                  1.0

[1 rows x 10 columns]
```
