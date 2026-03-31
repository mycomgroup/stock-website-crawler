---
id: "url-7a226ed5"
type: "website"
title: "指数成分股数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9958"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:21:47.942Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9958"
  headings:
    - {"level":3,"text":"指数成分股数据","id":""}
    - {"level":5,"text":"示例：","id":"-1"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：每天8:00检查更新"]}
    - {"type":"ul","items":["获取一个指数给定日期在平台可交易的成分股列表，请点击[指数列表](/indexData)查看指数信息"]}
    - {"type":"ul","items":["index_symbol: 指数代码","date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None,"]}
    - {"type":"ul","items":["返回股票代码的list"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_index_stocks(index_symbol, date=None)"}
    - {"language":"python","code":"# 获取所有沪深300的股票\nstocks = get_index_stocks('000300.XSHG')\nprint(stocks[:5])\n\n# 输出\n['000001.XSHE', '000002.XSHE', '000063.XSHE', '000066.XSHE', '000069.XSHE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"指数成分股数据"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：每天8:00检查更新"]}
    - {"type":"codeblock","language":"python","content":"get_index_stocks(index_symbol, date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取一个指数给定日期在平台可交易的成分股列表，请点击[指数列表](/indexData)查看指数信息"]}
    - {"type":"list","listType":"ul","items":["index_symbol: 指数代码","date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None,"]}
    - {"type":"list","listType":"ul","items":["返回股票代码的list"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 获取所有沪深300的股票\nstocks = get_index_stocks('000300.XSHG')\nprint(stocks[:5])\n\n# 输出\n['000001.XSHE', '000002.XSHE', '000063.XSHE', '000066.XSHE', '000069.XSHE']"}
  suggestedFilename: "doc_JQDatadoc_9958_overview_指数成分股数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9958"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 指数成分股数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9958

## 描述

描述

## 内容

#### 指数成分股数据

- 历史范围：2005年至今；更新时间：每天8:00检查更新

```python
get_index_stocks(index_symbol, date=None)
```

描述

- 获取一个指数给定日期在平台可交易的成分股列表，请点击[指数列表](/indexData)查看指数信息

- index_symbol: 指数代码
- date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None,

- 返回股票代码的list

###### 示例：

```python
# 获取所有沪深300的股票
stocks = get_index_stocks('000300.XSHG')
print(stocks[:5])

# 输出
['000001.XSHE', '000002.XSHE', '000063.XSHE', '000066.XSHE', '000069.XSHE']
```
