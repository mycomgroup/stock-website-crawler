---
id: "url-7a226b31"
type: "website"
title: "获取概念成分股"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9866"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:49.492Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9866"
  headings:
    - {"level":3,"text":"获取概念成分股","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回"
  lists:
    - {"type":"ul","items":["历史范围：2016年至今；更新时间：8:00更新"]}
    - {"type":"ul","items":["获取在给定日期一个概念板块的所有股票，概念板块分类列表见数据页面[行业概念数据]"]}
    - {"type":"ul","items":["concept_code: 概念板块编码","date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None"]}
    - {"type":"ul","items":["返回股票代码的list"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_concept_stocks(concept_code, date=None)"}
    - {"language":"python","code":"# 获取风力发电概念板块的成分股\nstocks = get_concept_stocks('SC0084')\nprint(stocks[:5])\n#输出\n['000027.XSHE', '000039.XSHE', '000065.XSHE', '000099.XSHE', '000155.XSHE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取概念成分股"}
    - {"type":"list","listType":"ul","items":["历史范围：2016年至今；更新时间：8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_concept_stocks(concept_code, date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取在给定日期一个概念板块的所有股票，概念板块分类列表见数据页面[行业概念数据]"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["concept_code: 概念板块编码","date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["返回股票代码的list"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 获取风力发电概念板块的成分股\nstocks = get_concept_stocks('SC0084')\nprint(stocks[:5])\n#输出\n['000027.XSHE', '000039.XSHE', '000065.XSHE', '000099.XSHE', '000155.XSHE']"}
  suggestedFilename: "doc_JQDatadoc_9866_overview_获取概念成分股"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9866"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取概念成分股

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9866

## 描述

描述

## 内容

#### 获取概念成分股

- 历史范围：2016年至今；更新时间：8:00更新

```python
get_concept_stocks(concept_code, date=None)
```

描述

- 获取在给定日期一个概念板块的所有股票，概念板块分类列表见数据页面[行业概念数据]

参数

- concept_code: 概念板块编码
- date: 查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None

返回

- 返回股票代码的list

###### 示例

```python
# 获取风力发电概念板块的成分股
stocks = get_concept_stocks('SC0084')
print(stocks[:5])
#输出
['000027.XSHE', '000039.XSHE', '000065.XSHE', '000099.XSHE', '000155.XSHE']
```
