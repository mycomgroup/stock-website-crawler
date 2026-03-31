---
id: "url-36496f61"
type: "website"
title: "获取单支可转债标的信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10341"
description: "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:38.996Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10341"
  headings:
    - {"level":3,"text":"获取单支可转债标的信息","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
    - "描述"
  lists:
    - {"type":"ul","items":["code: 证券代码","使用方式:接口+.属性，具体属性说明如下图"]}
    - {"type":"ul","items":["获取中文名称"]}
  tables:
    - {"caption":"","headers":["属性","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期","[datetime.date] 类型"],["end_date","退市日期","[datetime.date] 类型, 如果没有退市则为2200-01-01)"],["type","类型","conbond(可转债)"]]}
  codeBlocks:
    - {"language":"python","code":"get_security_info(code)"}
    - {"language":"python","code":"# 获取110043.XSHG的中文名称\ndisplay_name = get_security_info('110043.XSHG').display_name\nprint(display_name)\n>>>无锡转债\n\n-获取上市时间\n# 获取000001.XSHE的上市时间\nstart_date = get_security_info('110043.XSHG').start_date\nprint(start_date)\n>>>2018-03-14"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取单支可转债标的信息"}
    - {"type":"paragraph","content":"试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"}
    - {"type":"codeblock","language":"python","content":"get_security_info(code)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["code: 证券代码","使用方式:接口+.属性，具体属性说明如下图"]}
    - {"type":"table","headers":["属性","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期","[datetime.date] 类型"],["end_date","退市日期","[datetime.date] 类型, 如果没有退市则为2200-01-01)"],["type","类型","conbond(可转债)"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获取中文名称"]}
    - {"type":"codeblock","language":"python","content":"# 获取110043.XSHG的中文名称\ndisplay_name = get_security_info('110043.XSHG').display_name\nprint(display_name)\n>>>无锡转债\n\n-获取上市时间\n# 获取000001.XSHE的上市时间\nstart_date = get_security_info('110043.XSHG').start_date\nprint(start_date)\n>>>2018-03-14"}
  suggestedFilename: "doc_JQDatadoc_10341_overview_获取单支可转债标的信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10341"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取单支可转债标的信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10341

## 描述

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

## 内容

#### 获取单支可转债标的信息

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

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
| type | 类型 | conbond(可转债) |

###### 示例

- 获取中文名称

```python
# 获取110043.XSHG的中文名称
display_name = get_security_info('110043.XSHG').display_name
print(display_name)
>>>无锡转债

-获取上市时间
# 获取000001.XSHE的上市时间
start_date = get_security_info('110043.XSHG').start_date
print(start_date)
>>>2018-03-14
```
