---
id: "url-36496f62"
type: "website"
title: "获取所有可转债标的信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10340"
description: "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
source: ""
tags: []
crawl_time: "2026-03-27T07:43:25.184Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10340"
  headings:
    - {"level":3,"text":"获取所有可转债标的信息","id":""}
    - {"level":5,"text":"参数","id":"-1"}
    - {"level":5,"text":"返回结果","id":"-2"}
  paragraphs:
    - "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
    - "描述"
    - "示例"
  lists:
    - {"type":"ul","items":["获取平台支持的所有可转债等信息"]}
  tables:
    - {"caption":"","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'conbond'"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的可转债信息. 默认值为 None, 表示获取所有日期的可转债信息"]]}
    - {"caption":"","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","conbond(可转债)"]]}
  codeBlocks:
    - {"language":"python","code":"get_all_securities(types=[], date=None)"}
    - {"language":"python","code":"#获得所有可转债列表\ndf=get_all_securities(\"conbond\")\ndf[:5]\n\n            display_name  name start_date   end_date     type\n110001.XSHG         邯钢转债  HGZZ 2003-12-11 2007-03-16  conbond\n110002.XSHG         南山转债  NSZZ 2008-05-13 2009-09-24  conbond\n110003.XSHG         新钢转债  XGZZ 2008-09-05 2013-08-27  conbond\n110004.XSHG         厦工转债  SGZZ 2009-09-11 2010-09-30  conbond\n110005.XSHG         西洋转债  XYZZ 2009-09-21 2010-05-19  conbond"}
    - {"language":"python","code":"#获得2023年02月01日还在上市的所有可转债列表\ndf=get_all_securities(\"conbond\",date='2023-02-01')\nprint(df[:5])\n\n            display_name  name start_date   end_date     type\n110001.XSHG         邯钢转债  HGZZ 2003-12-11 2007-03-16  conbond\n110002.XSHG         南山转债  NSZZ 2008-05-13 2009-09-24  conbond\n110003.XSHG         新钢转债  XGZZ 2008-09-05 2013-08-27  conbond\n110004.XSHG         厦工转债  SGZZ 2009-09-11 2010-09-30  conbond\n110005.XSHG         西洋转债  XYZZ 2009-09-21 2010-05-19  conbond"}
    - {"language":"python","code":"#将所有可转债列表转换成数组\nconbond = list(get_all_securities(['conbond']).index)\nconbond[:5]\n>>>['110001.XSHG', '110002.XSHG', '110003.XSHG', '110004.XSHG', '110005.XSHG']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取所有可转债标的信息"}
    - {"type":"paragraph","content":"试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"}
    - {"type":"codeblock","language":"python","content":"get_all_securities(types=[], date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取平台支持的所有可转债等信息"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'conbond'"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的可转债信息. 默认值为 None, 表示获取所有日期的可转债信息"]]}
    - {"type":"heading","level":5,"content":"返回结果"}
    - {"type":"table","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","conbond(可转债)"]]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"#获得所有可转债列表\ndf=get_all_securities(\"conbond\")\ndf[:5]\n\n            display_name  name start_date   end_date     type\n110001.XSHG         邯钢转债  HGZZ 2003-12-11 2007-03-16  conbond\n110002.XSHG         南山转债  NSZZ 2008-05-13 2009-09-24  conbond\n110003.XSHG         新钢转债  XGZZ 2008-09-05 2013-08-27  conbond\n110004.XSHG         厦工转债  SGZZ 2009-09-11 2010-09-30  conbond\n110005.XSHG         西洋转债  XYZZ 2009-09-21 2010-05-19  conbond"}
    - {"type":"codeblock","language":"python","content":"#获得2023年02月01日还在上市的所有可转债列表\ndf=get_all_securities(\"conbond\",date='2023-02-01')\nprint(df[:5])\n\n            display_name  name start_date   end_date     type\n110001.XSHG         邯钢转债  HGZZ 2003-12-11 2007-03-16  conbond\n110002.XSHG         南山转债  NSZZ 2008-05-13 2009-09-24  conbond\n110003.XSHG         新钢转债  XGZZ 2008-09-05 2013-08-27  conbond\n110004.XSHG         厦工转债  SGZZ 2009-09-11 2010-09-30  conbond\n110005.XSHG         西洋转债  XYZZ 2009-09-21 2010-05-19  conbond"}
    - {"type":"codeblock","language":"python","content":"#将所有可转债列表转换成数组\nconbond = list(get_all_securities(['conbond']).index)\nconbond[:5]\n>>>['110001.XSHG', '110002.XSHG', '110003.XSHG', '110004.XSHG', '110005.XSHG']"}
  suggestedFilename: "doc_JQDatadoc_10340_overview_获取所有可转债标的信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10340"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取所有可转债标的信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10340

## 描述

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

## 内容

#### 获取所有可转债标的信息

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

```python
get_all_securities(types=[], date=None)
```

描述

- 获取平台支持的所有可转债等信息

###### 参数

| 属性 | 名称 | 字段类型 | 备注 |
| --- | --- | --- | --- |
| types | 类型 | 用list的形式过滤securities的类型, | list元素可选: 'conbond' |
| date | 日期 | 日期字符串或者 [datetime.datetime]/[datetime.date] 对象 | 用于获取某日期还在上市的可转债信息. 默认值为 None, 表示获取所有日期的可转债信息 |

###### 返回结果

| 字段 | 名称 | 备注 |
| --- | --- | --- |
| display_name | 中文名称 |  |
| name | 缩写简称 |  |
| start_date | 上市日期 |  |
| end_date | 退市日期 | 如果没有退市则为2200-01-01 |
| type | 类型 | conbond(可转债) |

示例

```python
#获得所有可转债列表
df=get_all_securities("conbond")
df[:5]

            display_name  name start_date   end_date     type
110001.XSHG         邯钢转债  HGZZ 2003-12-11 2007-03-16  conbond
110002.XSHG         南山转债  NSZZ 2008-05-13 2009-09-24  conbond
110003.XSHG         新钢转债  XGZZ 2008-09-05 2013-08-27  conbond
110004.XSHG         厦工转债  SGZZ 2009-09-11 2010-09-30  conbond
110005.XSHG         西洋转债  XYZZ 2009-09-21 2010-05-19  conbond
```

```python
#获得2023年02月01日还在上市的所有可转债列表
df=get_all_securities("conbond",date='2023-02-01')
print(df[:5])

            display_name  name start_date   end_date     type
110001.XSHG         邯钢转债  HGZZ 2003-12-11 2007-03-16  conbond
110002.XSHG         南山转债  NSZZ 2008-05-13 2009-09-24  conbond
110003.XSHG         新钢转债  XGZZ 2008-09-05 2013-08-27  conbond
110004.XSHG         厦工转债  SGZZ 2009-09-11 2010-09-30  conbond
110005.XSHG         西洋转债  XYZZ 2009-09-21 2010-05-19  conbond
```

```python
#将所有可转债列表转换成数组
conbond = list(get_all_securities(['conbond']).index)
conbond[:5]
>>>['110001.XSHG', '110002.XSHG', '110003.XSHG', '110004.XSHG', '110005.XSHG']
```
