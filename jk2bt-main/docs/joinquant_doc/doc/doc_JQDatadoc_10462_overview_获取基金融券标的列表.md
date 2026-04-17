---
id: "url-36496b61"
type: "website"
title: "获取基金融券标的列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10462"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:47:01.832Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10462"
  headings:
    - {"level":3,"text":"获取基金融券标的列表","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回结果"
    - "示例"
  lists:
    - {"type":"ul","items":["历史范围：2010年至今；更新时间：下一个交易日9点之前更新"]}
    - {"type":"ul","items":["获取基金融资标的列表"]}
    - {"type":"ul","items":["date:默认为None,不指定时返回上交所、深交所最近一次披露的的可融券标的列表的list。"]}
    - {"type":"ul","items":["返回指定日期上交所、深交所披露的的可融券标的列表的list。"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_marginsec_stocks(date)"}
    - {"language":"python","code":"# 判断新经济ETF是否在可融券列表\n'159822.XSHE' in get_marginsec_stocks(date='2021-03-02')\n>>> True"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取基金融券标的列表"}
    - {"type":"list","listType":"ul","items":["历史范围：2010年至今；更新时间：下一个交易日9点之前更新"]}
    - {"type":"codeblock","language":"python","content":"get_marginsec_stocks(date)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取基金融资标的列表"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["date:默认为None,不指定时返回上交所、深交所最近一次披露的的可融券标的列表的list。"]}
    - {"type":"paragraph","content":"返回结果"}
    - {"type":"list","listType":"ul","items":["返回指定日期上交所、深交所披露的的可融券标的列表的list。"]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 判断新经济ETF是否在可融券列表\n'159822.XSHE' in get_marginsec_stocks(date='2021-03-02')\n>>> True"}
  suggestedFilename: "doc_JQDatadoc_10462_overview_获取基金融券标的列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10462"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取基金融券标的列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10462

## 描述

描述

## 内容

#### 获取基金融券标的列表

- 历史范围：2010年至今；更新时间：下一个交易日9点之前更新

```python
get_marginsec_stocks(date)
```

描述

- 获取基金融资标的列表

参数

- date:默认为None,不指定时返回上交所、深交所最近一次披露的的可融券标的列表的list。

返回结果

- 返回指定日期上交所、深交所披露的的可融券标的列表的list。

示例

```python
# 判断新经济ETF是否在可融券列表
'159822.XSHE' in get_marginsec_stocks(date='2021-03-02')
>>> True
```
