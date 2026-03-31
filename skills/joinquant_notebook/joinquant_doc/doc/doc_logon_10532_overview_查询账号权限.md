---
id: "url-94b85e7"
type: "website"
title: "查询账号权限"
url: "https://www.joinquant.com/help/api/doc?name=logon&id=10532"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:14:38.192Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=logon&id=10532"
  headings:
    - {"level":3,"text":"查询账号权限","id":""}
    - {"level":5,"text":"返回","id":"-1"}
  paragraphs:
    - "描述"
    - "一个dict，字段说明如下"
    - "示例"
  lists:
    - {"type":"ul","items":["查看当前账号信息。"]}
  tables:
    - {"caption":"","headers":["字段名","说明"],"rows":[["license","账号最多可以同时使用的链接数(默认1条)"],["date_range_start","可调用的数据起始日期,为*时代表无限制"],["date_range_end","可调用的数据终止日期,为*时代表无限制"],["query_count_limit","账号流量(不含临时流量)"],["expire_time","账号失效时间"],["mob","账号"]]}
  codeBlocks:
    - {"language":"python","code":"get_account_info()"}
    - {"language":"python","code":"pip install jqdatasdk -U"}
    - {"language":"python","code":"#查询账号信息\ninfos = get_account_info()\nprint(infos)\n\n>>>{'license': 1,\n 'date_range_start': '2022-04-22 00:00:00',\n 'query_count_limit': 500000,\n 'date_range_end': '*',\n 'expire_time': '2023-04-22 00:00:00',\n 'mob': '199XXXXXXXX'}"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"查询账号权限"}
    - {"type":"codeblock","language":"python","content":"get_account_info()"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["查看当前账号信息。"]}
    - {"type":"codeblock","language":"python","content":"pip install jqdatasdk -U"}
    - {"type":"heading","level":5,"content":"返回"}
    - {"type":"paragraph","content":"一个dict，字段说明如下"}
    - {"type":"table","headers":["字段名","说明"],"rows":[["license","账号最多可以同时使用的链接数(默认1条)"],["date_range_start","可调用的数据起始日期,为*时代表无限制"],["date_range_end","可调用的数据终止日期,为*时代表无限制"],["query_count_limit","账号流量(不含临时流量)"],["expire_time","账号失效时间"],["mob","账号"]]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"#查询账号信息\ninfos = get_account_info()\nprint(infos)\n\n>>>{'license': 1,\n 'date_range_start': '2022-04-22 00:00:00',\n 'query_count_limit': 500000,\n 'date_range_end': '*',\n 'expire_time': '2023-04-22 00:00:00',\n 'mob': '199XXXXXXXX'}"}
  suggestedFilename: "doc_logon_10532_overview_查询账号权限"
  pageKind: "doc"
  pageName: "logon"
  pageId: "10532"
  sectionHash: ""
  sourceTitle: "试用和购买说明"
  treeRootTitle: ""
---

# 查询账号权限

## 源URL

https://www.joinquant.com/help/api/doc?name=logon&id=10532

## 描述

描述

## 内容

#### 查询账号权限

```python
get_account_info()
```

描述

- 查看当前账号信息。

```python
pip install jqdatasdk -U
```

###### 返回

一个dict，字段说明如下

| 字段名 | 说明 |
| --- | --- |
| license | 账号最多可以同时使用的链接数(默认1条) |
| date_range_start | 可调用的数据起始日期,为*时代表无限制 |
| date_range_end | 可调用的数据终止日期,为*时代表无限制 |
| query_count_limit | 账号流量(不含临时流量) |
| expire_time | 账号失效时间 |
| mob | 账号 |

示例

```python
#查询账号信息
infos = get_account_info()
print(infos)

>>>{'license': 1,
 'date_range_start': '2022-04-22 00:00:00',
 'query_count_limit': 500000,
 'date_range_end': '*',
 'expire_time': '2023-04-22 00:00:00',
 'mob': '199XXXXXXXX'}
```
