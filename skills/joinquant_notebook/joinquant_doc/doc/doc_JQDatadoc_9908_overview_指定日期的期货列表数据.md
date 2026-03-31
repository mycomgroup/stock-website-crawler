---
id: "url-7a226e3a"
type: "website"
title: "指定日期的期货列表数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9908"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:19:40.905Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9908"
  headings:
    - {"level":3,"text":"指定日期的期货列表数据","id":""}
    - {"level":5,"text":"示例：","id":"-1"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["获取某期货品种在指定日期下的可交易合约标的列表"]}
    - {"type":"ul","items":["underlying_symbol: 期货合约品种，如 'AU'(白银)","date：指定日期，默认为None，不指定时返回当前日期下可交易的合约标的列表"]}
    - {"type":"ul","items":["某一期货品种在指定日期下的可交易合约标的列表"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_future_contracts(underlying_symbol, date)"}
    - {"language":"python","code":"# 获取某期货品种在指定日期下的可交易合约标的列表\nget_future_contracts('AU','2017-01-05')\n\n# 输出\n['AU1701.XSGE', 'AU1702.XSGE', 'AU1703.XSGE', 'AU1704.XSGE', 'AU1706.XSGE', 'AU1708.XSGE', 'AU1710.XSGE', 'AU1712.XSGE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"指定日期的期货列表数据"}
    - {"type":"codeblock","language":"python","content":"get_future_contracts(underlying_symbol, date)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取某期货品种在指定日期下的可交易合约标的列表"]}
    - {"type":"list","listType":"ul","items":["underlying_symbol: 期货合约品种，如 'AU'(白银)","date：指定日期，默认为None，不指定时返回当前日期下可交易的合约标的列表"]}
    - {"type":"list","listType":"ul","items":["某一期货品种在指定日期下的可交易合约标的列表"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 获取某期货品种在指定日期下的可交易合约标的列表\nget_future_contracts('AU','2017-01-05')\n\n# 输出\n['AU1701.XSGE', 'AU1702.XSGE', 'AU1703.XSGE', 'AU1704.XSGE', 'AU1706.XSGE', 'AU1708.XSGE', 'AU1710.XSGE', 'AU1712.XSGE']"}
  suggestedFilename: "doc_JQDatadoc_9908_overview_指定日期的期货列表数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9908"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 指定日期的期货列表数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9908

## 描述

描述

## 内容

#### 指定日期的期货列表数据

```python
get_future_contracts(underlying_symbol, date)
```

描述

- 获取某期货品种在指定日期下的可交易合约标的列表

- underlying_symbol: 期货合约品种，如 'AU'(白银)
- date：指定日期，默认为None，不指定时返回当前日期下可交易的合约标的列表

- 某一期货品种在指定日期下的可交易合约标的列表

###### 示例：

```python
# 获取某期货品种在指定日期下的可交易合约标的列表
get_future_contracts('AU','2017-01-05')

# 输出
['AU1701.XSGE', 'AU1702.XSGE', 'AU1703.XSGE', 'AU1704.XSGE', 'AU1706.XSGE', 'AU1708.XSGE', 'AU1710.XSGE', 'AU1712.XSGE']
```
