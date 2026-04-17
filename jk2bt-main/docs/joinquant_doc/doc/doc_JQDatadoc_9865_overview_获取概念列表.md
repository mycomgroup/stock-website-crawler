---
id: "url-7a226b30"
type: "website"
title: "获取概念列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9865"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:45.572Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9865"
  headings:
    - {"level":3,"text":"获取概念列表","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "返回值"
  lists:
    - {"type":"ul","items":["历史范围：2016年至今；更新时间：8:00更新"]}
    - {"type":"ul","items":["获取概念板块列表"]}
    - {"type":"ul","items":["index: 概念代码","name: 概念名称","start_date: 开始日期"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_concepts()"}
    - {"language":"python","code":"df=get_concepts()[:5]\nprint(df)\n\n       name start_date\nSC0001    石墨烯 2016-07-31\nSC0002    阿里  2016-07-31\nSC0003    腾讯  2017-12-26\nSC0004    百度  2018-06-11\nSC0005    华为  2018-12-24"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取概念列表"}
    - {"type":"list","listType":"ul","items":["历史范围：2016年至今；更新时间：8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_concepts()"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取概念板块列表"]}
    - {"type":"paragraph","content":"返回值"}
    - {"type":"list","listType":"ul","items":["index: 概念代码","name: 概念名称","start_date: 开始日期"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"df=get_concepts()[:5]\nprint(df)\n\n       name start_date\nSC0001    石墨烯 2016-07-31\nSC0002    阿里  2016-07-31\nSC0003    腾讯  2017-12-26\nSC0004    百度  2018-06-11\nSC0005    华为  2018-12-24"}
  suggestedFilename: "doc_JQDatadoc_9865_overview_获取概念列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9865"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取概念列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9865

## 描述

描述

## 内容

#### 获取概念列表

- 历史范围：2016年至今；更新时间：8:00更新

```python
get_concepts()
```

描述

- 获取概念板块列表

返回值

- index: 概念代码
- name: 概念名称
- start_date: 开始日期

###### 示例

```python
df=get_concepts()[:5]
print(df)

       name start_date
SC0001    石墨烯 2016-07-31
SC0002    阿里  2016-07-31
SC0003    腾讯  2017-12-26
SC0004    百度  2018-06-11
SC0005    华为  2018-12-24
```
