---
id: "url-3649601d"
type: "website"
title: "聚宽特色指数成分股"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10763"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:48:32.343Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10763"
  headings:
    - {"level":3,"text":"聚宽特色指数成分股","id":""}
  paragraphs:
    - "描述"
    - "示例"
  lists:
    - {"type":"ul","items":["历史范围：2010年至今；更新时间：每天8:00检查更新"]}
    - {"type":"ul","items":["获取聚宽特色系列指数成分股列表"]}
    - {"type":"ul","items":["index_symbol: 指数代码","date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None,"]}
    - {"type":"ul","items":["返回聚宽特色系列指数代码的list"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_index_stocks(index_symbol, date=None)"}
    - {"language":"python","code":"JQ= get_index_stocks('JQ0001.SPI')\nprint(JQ[:5])\n\n['000001.XSHE', '000002.XSHE', '000004.XSHE', '000006.XSHE', '000007.XSHE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"聚宽特色指数成分股"}
    - {"type":"list","listType":"ul","items":["历史范围：2010年至今；更新时间：每天8:00检查更新"]}
    - {"type":"codeblock","language":"python","content":"get_index_stocks(index_symbol, date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取聚宽特色系列指数成分股列表"]}
    - {"type":"list","listType":"ul","items":["index_symbol: 指数代码","date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None,"]}
    - {"type":"list","listType":"ul","items":["返回聚宽特色系列指数代码的list"]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"JQ= get_index_stocks('JQ0001.SPI')\nprint(JQ[:5])\n\n['000001.XSHE', '000002.XSHE', '000004.XSHE', '000006.XSHE', '000007.XSHE']"}
  suggestedFilename: "doc_JQDatadoc_10763_overview_聚宽特色指数成分股"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10763"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 聚宽特色指数成分股

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10763

## 描述

描述

## 内容

#### 聚宽特色指数成分股

- 历史范围：2010年至今；更新时间：每天8:00检查更新

```python
get_index_stocks(index_symbol, date=None)
```

描述

- 获取聚宽特色系列指数成分股列表

- index_symbol: 指数代码
- date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None,

- 返回聚宽特色系列指数代码的list

示例

```python
JQ= get_index_stocks('JQ0001.SPI')
print(JQ[:5])

['000001.XSHE', '000002.XSHE', '000004.XSHE', '000006.XSHE', '000007.XSHE']
```
