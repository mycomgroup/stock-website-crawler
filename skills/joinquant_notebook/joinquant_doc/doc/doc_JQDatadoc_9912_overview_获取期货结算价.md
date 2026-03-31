---
id: "url-7a226e53"
type: "website"
title: "获取期货结算价"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9912"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:19:56.567Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9912"
  headings:
    - {"level":3,"text":"获取期货结算价","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：盘后17:00更新"]}
    - {"type":"ul","items":["获取期货结算价"]}
    - {"type":"ul","items":["info: [futures_sett_price]期货结算价;","security_list: 期货列表：","start_date/end_date:开始/结束日期, 同 [get_price]","df: 返回[pandas.DataFrame]对象还是一个dict","count: 数量, 与 start_date 二选一, 不可同时使用, 必须大于 0. 表示取 end_date 往前的 count 个交易日的数据"]}
    - {"type":"ul","items":["df=True: 返回[pandas.DataFrame]对象, 列索引是期货代号, 行索引是[datetime.datetime]"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_extras(info, security_list, start_date='2005-01-01', end_date =None, df=True, count=None)"}
    - {"language":"python","code":"获取期货结算价：futures_sett_price\n\nget_extras('futures_sett_price', ['A0603.XDCE','A0605.XDCE'],start_date='2005-01-18').head()\n\n            A0603.XDCE  A0605.XDCE\n2005-01-18      2510.0      2537.0\n2005-01-19      2512.0      2537.0\n2005-01-20      2512.0      2529.0\n2005-01-21      2500.0      2528.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取期货结算价"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：盘后17:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_extras(info, security_list, start_date='2005-01-01', end_date =None, df=True, count=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取期货结算价"]}
    - {"type":"list","listType":"ul","items":["info: [futures_sett_price]期货结算价;","security_list: 期货列表：","start_date/end_date:开始/结束日期, 同 [get_price]","df: 返回[pandas.DataFrame]对象还是一个dict","count: 数量, 与 start_date 二选一, 不可同时使用, 必须大于 0. 表示取 end_date 往前的 count 个交易日的数据"]}
    - {"type":"list","listType":"ul","items":["df=True: 返回[pandas.DataFrame]对象, 列索引是期货代号, 行索引是[datetime.datetime]"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"获取期货结算价：futures_sett_price\n\nget_extras('futures_sett_price', ['A0603.XDCE','A0605.XDCE'],start_date='2005-01-18').head()\n\n            A0603.XDCE  A0605.XDCE\n2005-01-18      2510.0      2537.0\n2005-01-19      2512.0      2537.0\n2005-01-20      2512.0      2529.0\n2005-01-21      2500.0      2528.0"}
  suggestedFilename: "doc_JQDatadoc_9912_overview_获取期货结算价"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9912"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取期货结算价

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9912

## 描述

描述

## 内容

#### 获取期货结算价

- 历史范围：2005年至今；更新时间：盘后17:00更新

```python
get_extras(info, security_list, start_date='2005-01-01', end_date =None, df=True, count=None)
```

描述

- 获取期货结算价

- info: [futures_sett_price]期货结算价;
- security_list: 期货列表：
- start_date/end_date:开始/结束日期, 同 [get_price]
- df: 返回[pandas.DataFrame]对象还是一个dict
- count: 数量, 与 start_date 二选一, 不可同时使用, 必须大于 0. 表示取 end_date 往前的 count 个交易日的数据

- df=True: 返回[pandas.DataFrame]对象, 列索引是期货代号, 行索引是[datetime.datetime]

###### 示例：

```python
获取期货结算价：futures_sett_price

get_extras('futures_sett_price', ['A0603.XDCE','A0605.XDCE'],start_date='2005-01-18').head()

            A0603.XDCE  A0605.XDCE
2005-01-18      2510.0      2537.0
2005-01-19      2512.0      2537.0
2005-01-20      2512.0      2529.0
2005-01-21      2500.0      2528.0
```
