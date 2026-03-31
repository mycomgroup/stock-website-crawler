---
id: "url-3649605c"
type: "website"
title: "期货持仓量"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10742"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:50:18.359Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10742"
  headings:
    - {"level":3,"text":"期货持仓量","id":""}
  paragraphs:
    - "描述"
    - "跳转"
  lists:
    - {"type":"ul","items":["get_pirce中fields 参数中指定 open_trest 字段"]}
    - {"type":"ul","items":["使用 get_price 接口时，在 fields 参数中指定 open_trest 字段以获取持仓量信息。"]}
    - {"type":"ul","items":["获取商品期货持仓量get_pirce中fields 参数中指定 open_interest字段","获取金融期货持仓量get_pirce中fields 参数中指定 open_interest字段"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_price(security, start_date=None, end_date=None, frequency='daily', fields=['open_interest'], skip_paused=False, fq='pre', count=None)"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"期货持仓量"}
    - {"type":"list","listType":"ul","items":["get_pirce中fields 参数中指定 open_trest 字段"]}
    - {"type":"codeblock","language":"python","content":"get_price(security, start_date=None, end_date=None, frequency='daily', fields=['open_interest'], skip_paused=False, fq='pre', count=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["使用 get_price 接口时，在 fields 参数中指定 open_trest 字段以获取持仓量信息。"]}
    - {"type":"paragraph","content":"跳转"}
    - {"type":"list","listType":"ul","items":["获取商品期货持仓量get_pirce中fields 参数中指定 open_interest字段","获取金融期货持仓量get_pirce中fields 参数中指定 open_interest字段"]}
  suggestedFilename: "doc_JQDatadoc_10742_overview_期货持仓量"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10742"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 期货持仓量

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10742

## 描述

描述

## 内容

#### 期货持仓量

- get_pirce中fields 参数中指定 open_trest 字段

```python
get_price(security, start_date=None, end_date=None, frequency='daily', fields=['open_interest'], skip_paused=False, fq='pre', count=None)
```

描述

- 使用 get_price 接口时，在 fields 参数中指定 open_trest 字段以获取持仓量信息。

跳转

- 获取商品期货持仓量get_pirce中fields 参数中指定 open_interest字段
- 获取金融期货持仓量get_pirce中fields 参数中指定 open_interest字段
