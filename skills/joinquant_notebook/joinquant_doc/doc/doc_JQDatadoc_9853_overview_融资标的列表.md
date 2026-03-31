---
id: "url-7a226b0f"
type: "website"
title: "融资标的列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9853"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:10.082Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9853"
  headings:
    - {"level":3,"text":"融资标的列表","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "描述"
    - "参数"
    - "返回结果"
  lists:
    - {"type":"ul","items":["历史范围：2010年至今；更新时间：每天21:00更新下一交易日"]}
    - {"type":"ul","items":["获取指定日期的融资标的列表"]}
    - {"type":"ul","items":["date:默认为None,不指定时返回上交所、深交所最近一次披露的的可融资标的列表的list。"]}
    - {"type":"ul","items":["返回指定日期上交所、深交所披露的的可融资标的列表的list。"]}
    - {"type":"ul","items":["获取某一天的融资标的列表"]}
    - {"type":"ul","items":["判断某只股票是否在融资列表内"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_margincash_stocks(date)"}
    - {"language":"python","code":"# 获取融资标的列表，并赋值给 margincash_stocks\nmargincash_stocks = get_margincash_stocks(date='2018-07-02')\nmargincash_stocks[:3]\n>>>['000001.XSHE', '000002.XSHE', '000006.XSHE']"}
    - {"language":"python","code":"# 判断平安银行是否在可融资列表\n'000001.XSHE' in get_margincash_stocks(date='2018-07-02')\n>>> True"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"融资标的列表"}
    - {"type":"list","listType":"ul","items":["历史范围：2010年至今；更新时间：每天21:00更新下一交易日"]}
    - {"type":"codeblock","language":"python","content":"get_margincash_stocks(date)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取指定日期的融资标的列表"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["date:默认为None,不指定时返回上交所、深交所最近一次披露的的可融资标的列表的list。"]}
    - {"type":"paragraph","content":"返回结果"}
    - {"type":"list","listType":"ul","items":["返回指定日期上交所、深交所披露的的可融资标的列表的list。"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获取某一天的融资标的列表"]}
    - {"type":"codeblock","language":"python","content":"# 获取融资标的列表，并赋值给 margincash_stocks\nmargincash_stocks = get_margincash_stocks(date='2018-07-02')\nmargincash_stocks[:3]\n>>>['000001.XSHE', '000002.XSHE', '000006.XSHE']"}
    - {"type":"list","listType":"ul","items":["判断某只股票是否在融资列表内"]}
    - {"type":"codeblock","language":"python","content":"# 判断平安银行是否在可融资列表\n'000001.XSHE' in get_margincash_stocks(date='2018-07-02')\n>>> True"}
  suggestedFilename: "doc_JQDatadoc_9853_overview_融资标的列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9853"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 融资标的列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9853

## 描述

描述

## 内容

#### 融资标的列表

- 历史范围：2010年至今；更新时间：每天21:00更新下一交易日

```python
get_margincash_stocks(date)
```

描述

- 获取指定日期的融资标的列表

参数

- date:默认为None,不指定时返回上交所、深交所最近一次披露的的可融资标的列表的list。

返回结果

- 返回指定日期上交所、深交所披露的的可融资标的列表的list。

###### 示例

- 获取某一天的融资标的列表

```python
# 获取融资标的列表，并赋值给 margincash_stocks
margincash_stocks = get_margincash_stocks(date='2018-07-02')
margincash_stocks[:3]
>>>['000001.XSHE', '000002.XSHE', '000006.XSHE']
```

- 判断某只股票是否在融资列表内

```python
# 判断平安银行是否在可融资列表
'000001.XSHE' in get_margincash_stocks(date='2018-07-02')
>>> True
```
