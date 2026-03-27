---
id: "url-364972fe"
type: "website"
title: "获取期货可交易合约列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10256"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:11.552Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10256"
  headings:
    - {"level":3,"text":"获取期货可交易合约列表","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回"
    - "示例"
  lists:
    - {"type":"ul","items":["获取某期货品种在指定日期下的可交易合约标的列表"]}
    - {"type":"ul","items":["underlying_symbol : 期货合约品种，如 'AU'(白银)","date：指定日期，默认为None，不指定时返回当前日期下可交易的合约标的列表"]}
    - {"type":"ul","items":["某一期货品种在指定日期下的可交易合约标的列表"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_future_contracts(underlying_symbol, date)"}
    - {"language":"python","code":"# 获取某期货品种在指定日期下的可交易合约标的列表\nget_future_contracts('AU','2017-01-05')\n\n# 输出\n['AU1701.XSGE', 'AU1702.XSGE', 'AU1703.XSGE', 'AU1704.XSGE', 'AU1706.XSGE', 'AU1708.XSGE', 'AU1710.XSGE', 'AU1712.XSGE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取期货可交易合约列表"}
    - {"type":"codeblock","language":"python","content":"get_future_contracts(underlying_symbol, date)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取某期货品种在指定日期下的可交易合约标的列表"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["underlying_symbol : 期货合约品种，如 'AU'(白银)","date：指定日期，默认为None，不指定时返回当前日期下可交易的合约标的列表"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["某一期货品种在指定日期下的可交易合约标的列表"]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 获取某期货品种在指定日期下的可交易合约标的列表\nget_future_contracts('AU','2017-01-05')\n\n# 输出\n['AU1701.XSGE', 'AU1702.XSGE', 'AU1703.XSGE', 'AU1704.XSGE', 'AU1706.XSGE', 'AU1708.XSGE', 'AU1710.XSGE', 'AU1712.XSGE']"}
  suggestedFilename: "doc_JQDatadoc_10256_overview_获取期货可交易合约列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10256"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取期货可交易合约列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10256

## 描述

描述

## 内容

#### 获取期货可交易合约列表

```python
get_future_contracts(underlying_symbol, date)
```

描述

- 获取某期货品种在指定日期下的可交易合约标的列表

参数

- underlying_symbol : 期货合约品种，如 'AU'(白银)
- date：指定日期，默认为None，不指定时返回当前日期下可交易的合约标的列表

返回

- 某一期货品种在指定日期下的可交易合约标的列表

示例

```python
# 获取某期货品种在指定日期下的可交易合约标的列表
get_future_contracts('AU','2017-01-05')

# 输出
['AU1701.XSGE', 'AU1702.XSGE', 'AU1703.XSGE', 'AU1704.XSGE', 'AU1706.XSGE', 'AU1708.XSGE', 'AU1710.XSGE', 'AU1712.XSGE']
```
