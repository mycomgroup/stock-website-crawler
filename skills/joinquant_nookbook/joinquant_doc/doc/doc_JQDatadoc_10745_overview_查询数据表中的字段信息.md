---
id: "url-36496059"
type: "website"
title: "查询数据表中的字段信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10745"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:58.663Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10745"
  headings:
    - {"level":3,"text":"查询数据表中的字段信息","id":""}
    - {"level":5,"text":"参数","id":"-1"}
    - {"level":5,"text":"代码示例","id":"-2"}
  paragraphs:
    - "描述"
    - "返回"
  lists:
    - {"type":"ul","items":["查询数据表中的字段信息","范围：涵盖各数据表：finance 库（股票、期货库中的统计表），opt 库（期权的各种表）、bond 库（债券及可转债的表）和macro 库（宏观经济指标表)"]}
    - {"type":"ul","items":["DataFrame : index 为标的列表, columns 为字段名"]}
    - {"type":"ul","items":["返回中文名称的表字段信息"]}
  tables:
    - {"caption":"","headers":["参数","备注"],"rows":[["table","数据表, 可以是表名字符串或者 ORM 对象 返回"],["DataFrame","包含各字段的中英文名称以及类型等信息"]]}
  codeBlocks:
    - {"language":"python","code":"get_table_info(table)"}
    - {"language":"python","code":"# 获取单季度某张表中的字段信息\nget_table_info(valuation)\n# 获取finance库某张表中的字段信息\nget_table_info(finance.STK_XR_XD)\n# 获取opt库某张表中的字段信息\nget_table_info(opt.OPT_ADJUSTMENT)\n# 获取bond库某张表中的字段信息\nget_table_info(bond.CONBOND_CONVERT_PRICE_ADJUST)\n# 获取macro库某张表中的字段信息\nget_table_info(macro.MAC_LEND_RATE)"}
    - {"language":"python","code":"# 获取期权合约调整记录表的字段信息\ntable=get_table_info(opt.OPT_ADJUSTMENT)\n# 对 OPT_ADJUSTMENT 表的name_en列建立索引，并清理该表中name_zh列的所有空值记录。\ncolumns = jq.get_table_info(jq.opt.OPT_ADJUSTMENT).set_index(\"name_en\").name_zh.dropna()\n# 获取期权合约调整记录表\ndf  = jq.opt.run_query(jq.query(jq.opt.OPT_ADJUSTMENT ).limit(20))\n# 重命名DataFrame中的列名为中文\ndf.rename(columns=columns)"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"查询数据表中的字段信息"}
    - {"type":"codeblock","language":"python","content":"get_table_info(table)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["查询数据表中的字段信息","范围：涵盖各数据表：finance 库（股票、期货库中的统计表），opt 库（期权的各种表）、bond 库（债券及可转债的表）和macro 库（宏观经济指标表)"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["DataFrame : index 为标的列表, columns 为字段名"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["参数","备注"],"rows":[["table","数据表, 可以是表名字符串或者 ORM 对象 返回"],["DataFrame","包含各字段的中英文名称以及类型等信息"]]}
    - {"type":"heading","level":5,"content":"代码示例"}
    - {"type":"codeblock","language":"python","content":"# 获取单季度某张表中的字段信息\nget_table_info(valuation)\n# 获取finance库某张表中的字段信息\nget_table_info(finance.STK_XR_XD)\n# 获取opt库某张表中的字段信息\nget_table_info(opt.OPT_ADJUSTMENT)\n# 获取bond库某张表中的字段信息\nget_table_info(bond.CONBOND_CONVERT_PRICE_ADJUST)\n# 获取macro库某张表中的字段信息\nget_table_info(macro.MAC_LEND_RATE)"}
    - {"type":"list","listType":"ul","items":["返回中文名称的表字段信息"]}
    - {"type":"codeblock","language":"python","content":"# 获取期权合约调整记录表的字段信息\ntable=get_table_info(opt.OPT_ADJUSTMENT)\n# 对 OPT_ADJUSTMENT 表的name_en列建立索引，并清理该表中name_zh列的所有空值记录。\ncolumns = jq.get_table_info(jq.opt.OPT_ADJUSTMENT).set_index(\"name_en\").name_zh.dropna()\n# 获取期权合约调整记录表\ndf  = jq.opt.run_query(jq.query(jq.opt.OPT_ADJUSTMENT ).limit(20))\n# 重命名DataFrame中的列名为中文\ndf.rename(columns=columns)"}
  suggestedFilename: "doc_JQDatadoc_10745_overview_查询数据表中的字段信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10745"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 查询数据表中的字段信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10745

## 描述

描述

## 内容

#### 查询数据表中的字段信息

```python
get_table_info(table)
```

描述

- 查询数据表中的字段信息
- 范围：涵盖各数据表：finance 库（股票、期货库中的统计表），opt 库（期权的各种表）、bond 库（债券及可转债的表）和macro 库（宏观经济指标表)

返回

- DataFrame : index 为标的列表, columns 为字段名

###### 参数

| 参数 | 备注 |
| --- | --- |
| table | 数据表, 可以是表名字符串或者 ORM 对象 返回 |
| DataFrame | 包含各字段的中英文名称以及类型等信息 |

###### 代码示例

```python
# 获取单季度某张表中的字段信息
get_table_info(valuation)
# 获取finance库某张表中的字段信息
get_table_info(finance.STK_XR_XD)
# 获取opt库某张表中的字段信息
get_table_info(opt.OPT_ADJUSTMENT)
# 获取bond库某张表中的字段信息
get_table_info(bond.CONBOND_CONVERT_PRICE_ADJUST)
# 获取macro库某张表中的字段信息
get_table_info(macro.MAC_LEND_RATE)
```

- 返回中文名称的表字段信息

```python
# 获取期权合约调整记录表的字段信息
table=get_table_info(opt.OPT_ADJUSTMENT)
# 对 OPT_ADJUSTMENT 表的name_en列建立索引，并清理该表中name_zh列的所有空值记录。
columns = jq.get_table_info(jq.opt.OPT_ADJUSTMENT).set_index("name_en").name_zh.dropna()
# 获取期权合约调整记录表
df  = jq.opt.run_query(jq.query(jq.opt.OPT_ADJUSTMENT ).limit(20))
# 重命名DataFrame中的列名为中文
df.rename(columns=columns)
```
