---
id: "url-7a226b2e"
type: "website"
title: "获取行业列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9863"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:37.711Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9863"
  headings:
    - {"level":3,"text":"获取行业列表","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "描述"
    - "参数"
    - "返回值"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"ul","items":["获取行业列表","行业列表"]}
    - {"type":"ul","items":["\"sw_l1\": 申万一级行业","\"sw_l2\": 申万二级行业","\"sw_l3\": 申万三级行业","\"jq_l1\": 聚宽一级行业","\"jq_l2\": 聚宽二级行业","\"zjw\": 证监会行业"]}
    - {"type":"ul","items":["index: 行业代码","name: 行业名称","start_date: 开始日期"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_industries(name='zjw', date=None)"}
    - {"language":"python","code":"# 获取2020-05-07当天证监会行业行业列表\ndf=get_industries(name='zjw', date=\"2022-05-07\")[:5]\nprint(df)\n\n      name start_date\nL72  商务服务业 1996-08-29\nL71    租赁业 1997-01-30\nG53  铁路运输业 1998-05-11\nG57  管道运输业 1996-11-04\nG56  航空运输业 1997-11-05"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取行业列表"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_industries(name='zjw', date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取行业列表","行业列表"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["\"sw_l1\": 申万一级行业","\"sw_l2\": 申万二级行业","\"sw_l3\": 申万三级行业","\"jq_l1\": 聚宽一级行业","\"jq_l2\": 聚宽二级行业","\"zjw\": 证监会行业"]}
    - {"type":"paragraph","content":"返回值"}
    - {"type":"list","listType":"ul","items":["index: 行业代码","name: 行业名称","start_date: 开始日期"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 获取2020-05-07当天证监会行业行业列表\ndf=get_industries(name='zjw', date=\"2022-05-07\")[:5]\nprint(df)\n\n      name start_date\nL72  商务服务业 1996-08-29\nL71    租赁业 1997-01-30\nG53  铁路运输业 1998-05-11\nG57  管道运输业 1996-11-04\nG56  航空运输业 1997-11-05"}
  suggestedFilename: "doc_JQDatadoc_9863_overview_获取行业列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9863"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取行业列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9863

## 描述

描述

## 内容

#### 获取行业列表

- 历史范围：2005年至今；更新时间：8:00更新

```python
get_industries(name='zjw', date=None)
```

描述

- 获取行业列表

参数

- "sw_l1": 申万一级行业
- "sw_l2": 申万二级行业
- "sw_l3": 申万三级行业
- "jq_l1": 聚宽一级行业
- "jq_l2": 聚宽二级行业
- "zjw": 证监会行业

返回值

- index: 行业代码
- name: 行业名称
- start_date: 开始日期

###### 示例

```python
# 获取2020-05-07当天证监会行业行业列表
df=get_industries(name='zjw', date="2022-05-07")[:5]
print(df)

      name start_date
L72  商务服务业 1996-08-29
L71    租赁业 1997-01-30
G53  铁路运输业 1998-05-11
G57  管道运输业 1996-11-04
G56  航空运输业 1997-11-05
```
