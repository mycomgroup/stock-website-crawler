---
id: "url-364972ff"
type: "website"
title: "获取单支标的信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10255"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:31.168Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10255"
  headings:
    - {"level":3,"text":"获取单支标的信息","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；"]}
    - {"type":"ul","items":["code: 证券代码","使用方式:接口+.属性，具体属性说明如下图"]}
    - {"type":"ul","items":["获取中文名称"]}
  tables:
    - {"caption":"","headers":["属性","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期","[datetime.date] 类型"],["end_date","退市日期","[datetime.date] 类型, 如果没有退市则为2200-01-01)"],["type","类型","stock(股票)，index(指数)，etf(ETF基金)，fja（分级A），fjb（分级B）"],["parent","分级基金的母基金代码",""]]}
  codeBlocks:
    - {"language":"python","code":"get_security_info(code)"}
    - {"language":"python","code":"# 获取518860.XSHG的中文名称\ndisplay_name = get_security_info('518860.XSHG').display_name\nprint(display_name)\n>>>上海金E\n\n\n-获取上市时间\n# 获取518860.XSHG的上市时间\nstart_date = get_security_info('518860.XSHG').start_date\nprint(start_date)\n>>>2020-09-07"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取单支标的信息"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；"]}
    - {"type":"codeblock","language":"python","content":"get_security_info(code)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["code: 证券代码","使用方式:接口+.属性，具体属性说明如下图"]}
    - {"type":"table","headers":["属性","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期","[datetime.date] 类型"],["end_date","退市日期","[datetime.date] 类型, 如果没有退市则为2200-01-01)"],["type","类型","stock(股票)，index(指数)，etf(ETF基金)，fja（分级A），fjb（分级B）"],["parent","分级基金的母基金代码",""]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获取中文名称"]}
    - {"type":"codeblock","language":"python","content":"# 获取518860.XSHG的中文名称\ndisplay_name = get_security_info('518860.XSHG').display_name\nprint(display_name)\n>>>上海金E\n\n\n-获取上市时间\n# 获取518860.XSHG的上市时间\nstart_date = get_security_info('518860.XSHG').start_date\nprint(start_date)\n>>>2020-09-07"}
  suggestedFilename: "doc_JQDatadoc_10255_overview_获取单支标的信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10255"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取单支标的信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10255

## 描述

描述

## 内容

#### 获取单支标的信息

- 历史范围：2005年至今；

```python
get_security_info(code)
```

描述

- code: 证券代码
- 使用方式:接口+.属性，具体属性说明如下图

| 属性 | 名称 | 备注 |
| --- | --- | --- |
| display_name | 中文名称 |  |
| name | 缩写简称 |  |
| start_date | 上市日期 | [datetime.date] 类型 |
| end_date | 退市日期 | [datetime.date] 类型, 如果没有退市则为2200-01-01) |
| type | 类型 | stock(股票)，index(指数)，etf(ETF基金)，fja（分级A），fjb（分级B） |
| parent | 分级基金的母基金代码 |  |

###### 示例

- 获取中文名称

```python
# 获取518860.XSHG的中文名称
display_name = get_security_info('518860.XSHG').display_name
print(display_name)
>>>上海金E

-获取上市时间
# 获取518860.XSHG的上市时间
start_date = get_security_info('518860.XSHG').start_date
print(start_date)
>>>2020-09-07
```
