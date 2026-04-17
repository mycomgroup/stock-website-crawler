---
id: "url-36496058"
type: "website"
title: "获取股票当日盘前交易信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10746"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:48:16.725Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10746"
  headings:
    - {"level":3,"text":"获取股票当日盘前交易信息","id":""}
    - {"level":5,"text":"参数","id":""}
    - {"level":5,"text":"代码示例","id":""}
  paragraphs:
    - "描述"
    - "返回"
    - "注意"
  lists:
    - {"type":"ul","items":["历史范围：当天；更新时间：盘前交易日 09:15 后可获取"]}
    - {"type":"ul","items":["获取股票当日盘前交易信息, 盘前交易日 09:15 后可获取到数据"]}
    - {"type":"ul","items":["DataFrame : index 为标的列表, columns 为字段名"]}
    - {"type":"ul","items":["在盘前更新中，聚宽单季度财务估值表于08:30更新当日最新的总股本与流通股本数据。"]}
  tables:
    - {"caption":"","headers":["参数","备注"],"rows":[["security","股票代码或者股票代码的 list"],["fields","请求字段, 默认为全部: paused(停牌标志), factor(后复权因子), high_limit(涨停价), low_limit(跌停价)"]]}
  codeBlocks:
    - {"language":"python","code":"get_preopen_infos(security, fields=(\"paused\", \"factor\", \"high_limit\", \"low_limit\"))"}
    - {"language":"python","code":"# 获取单季度某张表中的字段信息\nstocks = get_index_stocks('000300.XSHG')\nget_preopen_infos(stocks, fields=(\"paused\", \"factor\", \"high_limit\", \"low_limit\"))\n\n             paused      factor  high_limit  low_limit\n000001.XSHE     0.0  135.995625       11.01       9.01\n000002.XSHE     0.0  168.875961        7.57       6.19\n000063.XSHE     0.0   18.066363       28.11      23.00\n000100.XSHE     0.0    3.723823        4.04       3.30\n000157.XSHE     0.0   87.370424        7.12       5.82"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取股票当日盘前交易信息"}
    - {"type":"list","listType":"ul","items":["历史范围：当天；更新时间：盘前交易日 09:15 后可获取"]}
    - {"type":"codeblock","language":"python","content":"get_preopen_infos(security, fields=(\"paused\", \"factor\", \"high_limit\", \"low_limit\"))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取股票当日盘前交易信息, 盘前交易日 09:15 后可获取到数据"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["DataFrame : index 为标的列表, columns 为字段名"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["在盘前更新中，聚宽单季度财务估值表于08:30更新当日最新的总股本与流通股本数据。"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["参数","备注"],"rows":[["security","股票代码或者股票代码的 list"],["fields","请求字段, 默认为全部: paused(停牌标志), factor(后复权因子), high_limit(涨停价), low_limit(跌停价)"]]}
    - {"type":"heading","level":5,"content":"代码示例"}
    - {"type":"codeblock","language":"python","content":"# 获取单季度某张表中的字段信息\nstocks = get_index_stocks('000300.XSHG')\nget_preopen_infos(stocks, fields=(\"paused\", \"factor\", \"high_limit\", \"low_limit\"))\n\n             paused      factor  high_limit  low_limit\n000001.XSHE     0.0  135.995625       11.01       9.01\n000002.XSHE     0.0  168.875961        7.57       6.19\n000063.XSHE     0.0   18.066363       28.11      23.00\n000100.XSHE     0.0    3.723823        4.04       3.30\n000157.XSHE     0.0   87.370424        7.12       5.82"}
  suggestedFilename: "doc_JQDatadoc_10746_overview_获取股票当日盘前交易信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10746"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取股票当日盘前交易信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10746

## 描述

描述

## 内容

#### 获取股票当日盘前交易信息

- 历史范围：当天；更新时间：盘前交易日 09:15 后可获取

```python
get_preopen_infos(security, fields=("paused", "factor", "high_limit", "low_limit"))
```

描述

- 获取股票当日盘前交易信息, 盘前交易日 09:15 后可获取到数据

返回

- DataFrame : index 为标的列表, columns 为字段名

注意

- 在盘前更新中，聚宽单季度财务估值表于08:30更新当日最新的总股本与流通股本数据。

###### 参数

| 参数 | 备注 |
| --- | --- |
| security | 股票代码或者股票代码的 list |
| fields | 请求字段, 默认为全部: paused(停牌标志), factor(后复权因子), high_limit(涨停价), low_limit(跌停价) |

###### 代码示例

```python
# 获取单季度某张表中的字段信息
stocks = get_index_stocks('000300.XSHG')
get_preopen_infos(stocks, fields=("paused", "factor", "high_limit", "low_limit"))

             paused      factor  high_limit  low_limit
000001.XSHE     0.0  135.995625       11.01       9.01
000002.XSHE     0.0  168.875961        7.57       6.19
000063.XSHE     0.0   18.066363       28.11      23.00
000100.XSHE     0.0    3.723823        4.04       3.30
000157.XSHE     0.0   87.370424        7.12       5.82
```
