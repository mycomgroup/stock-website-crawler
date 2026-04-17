---
id: "url-7a226eb2"
type: "website"
title: "基金累计净值/基金单位净值/场外基金的复权净值"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9944"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:21:11.637Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9944"
  headings:
    - {"level":3,"text":"基金累计净值/基金单位净值/场外基金的复权净值","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "基金净值参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：盘后17点到下一交易日9点"]}
    - {"type":"ul","items":["获取基金累计净值/基金单位净值/场外基金的复权净值"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["info[ 'acc_net_value', 'unit_net_value', 'adj_net_value'] 中的一个","security_list：基金列表","start_date/end_date：开始结束日期, 同 [get_price]。","df：返回[pandas.DataFrame]对象还是一个dict","count：与 start_date 二选一, 不可同时使用, 必须大于 0. 表示取 end_date 往前的 count 个交易日的数据"]}
  tables:
    - {"caption":"","headers":["指定info字段","返回信息"],"rows":[["acc_net_value","基金累计净值"],["unit_net_value","基金单位净值"],["adj_net_value","场外基金的复权净值"]]}
  codeBlocks:
    - {"language":"python","code":"get_extras(info, security_list, start_date='2015-01-01', end_date='2015-12-31', df=True, count=None)"}
    - {"language":"python","code":"# 获取基金累计净值\n# df=True,返回[pandas.DataFrame]对象\ndf=get_extras('acc_net_value', ['510300.XSHG', '510050.XSHG'], start_date='2015-12-01', end_date='2015-12-03',df=True)\nprint(df)\n\n            510300.XSHG  510050.XSHG\n2015-12-01       1.3950        3.119\n2015-12-02       1.4432        3.251\n2015-12-03       1.4535        3.254"}
    - {"language":"python","code":"# 获取基金单位净值\n# df=False,返回一个dict, key是基金代号, value是[numpy.ndarray]\nget_extras('unit_net_value', ['510300.XSHG', '510050.XSHG'], start_date='2015-12-01', end_date='2015-12-03',df=False)\n#返回\n{'510300.XSHG': array([3.6446, 3.7746, 3.8023]),\n '510050.XSHG': array([2.344, 2.455, 2.458])}"}
    - {"language":"python","code":"# 获取场外基金的复权净值\ndf=get_extras('adj_net_value','398051.OF')\nprint(df[:4])\n            398051.OF\n2015-01-05      1.087\n2015-01-06      1.073\n2015-01-07      1.086\n2015-01-08      1.054"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"基金累计净值/基金单位净值/场外基金的复权净值"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：盘后17点到下一交易日9点"]}
    - {"type":"codeblock","language":"python","content":"get_extras(info, security_list, start_date='2015-01-01', end_date='2015-12-31', df=True, count=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取基金累计净值/基金单位净值/场外基金的复权净值"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"基金净值参数"}
    - {"type":"list","listType":"ul","items":["info[ 'acc_net_value', 'unit_net_value', 'adj_net_value'] 中的一个","security_list：基金列表","start_date/end_date：开始结束日期, 同 [get_price]。","df：返回[pandas.DataFrame]对象还是一个dict","count：与 start_date 二选一, 不可同时使用, 必须大于 0. 表示取 end_date 往前的 count 个交易日的数据"]}
    - {"type":"table","headers":["指定info字段","返回信息"],"rows":[["acc_net_value","基金累计净值"],["unit_net_value","基金单位净值"],["adj_net_value","场外基金的复权净值"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 获取基金累计净值\n# df=True,返回[pandas.DataFrame]对象\ndf=get_extras('acc_net_value', ['510300.XSHG', '510050.XSHG'], start_date='2015-12-01', end_date='2015-12-03',df=True)\nprint(df)\n\n            510300.XSHG  510050.XSHG\n2015-12-01       1.3950        3.119\n2015-12-02       1.4432        3.251\n2015-12-03       1.4535        3.254"}
    - {"type":"codeblock","language":"python","content":"# 获取基金单位净值\n# df=False,返回一个dict, key是基金代号, value是[numpy.ndarray]\nget_extras('unit_net_value', ['510300.XSHG', '510050.XSHG'], start_date='2015-12-01', end_date='2015-12-03',df=False)\n#返回\n{'510300.XSHG': array([3.6446, 3.7746, 3.8023]),\n '510050.XSHG': array([2.344, 2.455, 2.458])}"}
    - {"type":"codeblock","language":"python","content":"# 获取场外基金的复权净值\ndf=get_extras('adj_net_value','398051.OF')\nprint(df[:4])\n            398051.OF\n2015-01-05      1.087\n2015-01-06      1.073\n2015-01-07      1.086\n2015-01-08      1.054"}
  suggestedFilename: "doc_JQDatadoc_9944_overview_基金累计净值_基金单位净值_场外基金的复权净值"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9944"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 基金累计净值/基金单位净值/场外基金的复权净值

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9944

## 描述

描述

## 内容

#### 基金累计净值/基金单位净值/场外基金的复权净值

- 历史范围：上市至今；更新时间：盘后17点到下一交易日9点

```python
get_extras(info, security_list, start_date='2015-01-01', end_date='2015-12-31', df=True, count=None)
```

描述

- 获取基金累计净值/基金单位净值/场外基金的复权净值

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

基金净值参数

- info[ 'acc_net_value', 'unit_net_value', 'adj_net_value'] 中的一个
- security_list：基金列表
- start_date/end_date：开始结束日期, 同 [get_price]。
- df：返回[pandas.DataFrame]对象还是一个dict
- count：与 start_date 二选一, 不可同时使用, 必须大于 0. 表示取 end_date 往前的 count 个交易日的数据

| 指定info字段 | 返回信息 |
| --- | --- |
| acc_net_value | 基金累计净值 |
| unit_net_value | 基金单位净值 |
| adj_net_value | 场外基金的复权净值 |

###### 示例：

```python
# 获取基金累计净值
# df=True,返回[pandas.DataFrame]对象
df=get_extras('acc_net_value', ['510300.XSHG', '510050.XSHG'], start_date='2015-12-01', end_date='2015-12-03',df=True)
print(df)

            510300.XSHG  510050.XSHG
2015-12-01       1.3950        3.119
2015-12-02       1.4432        3.251
2015-12-03       1.4535        3.254
```

```python
# 获取基金单位净值
# df=False,返回一个dict, key是基金代号, value是[numpy.ndarray]
get_extras('unit_net_value', ['510300.XSHG', '510050.XSHG'], start_date='2015-12-01', end_date='2015-12-03',df=False)
#返回
{'510300.XSHG': array([3.6446, 3.7746, 3.8023]),
 '510050.XSHG': array([2.344, 2.455, 2.458])}
```

```python
# 获取场外基金的复权净值
df=get_extras('adj_net_value','398051.OF')
print(df[:4])
            398051.OF
2015-01-05      1.087
2015-01-06      1.073
2015-01-07      1.086
2015-01-08      1.054
```
