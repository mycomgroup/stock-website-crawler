---
id: "url-3649731c"
type: "website"
title: "获取期货交易列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10247"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:03.708Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10247"
  headings:
    - {"level":3,"text":"获取期货交易列表","id":""}
    - {"level":5,"text":"参数","id":""}
    - {"level":5,"text":"返回结果","id":""}
  paragraphs:
    - "描述"
    - "示例"
  lists:
    - {"type":"ul","items":["获取平台支持的所有股票、基金、指数、期货、期权等信息"]}
  tables:
    - {"caption":"","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'stock', 'fund', 'index', 'futures', 'etf','lof', 'fja', 'fjb','open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'types为空时返回所有股票, 不包括基金,指数和期货"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息"]]}
    - {"caption":"","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","stock(股票)，index(交易所指数)etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权) , conbond(可转债)"]]}
  codeBlocks:
    - {"language":"python","code":"get_all_securities(types=[], date=None)"}
    - {"language":"python","code":"#获得所有期货列表\ndf=get_all_securities(types=['futures'])\nprint(df[:2])\n\n           display_name   name start_date   end_date     type\nA0501.XDCE       豆一0501  a0501 2003-07-15 2005-01-17  futures\nA0503.XDCE       豆一0503  a0503 2003-09-15 2005-03-14  futures"}
    - {"language":"python","code":"#获得2020年10月10日还在上市的所有期货列表\ndf=get_all_securities(types=['futures'],date='2020-10-10')\nprint(df[:5])\n           display_name   name start_date   end_date     type\nA2011.XDCE       豆一2011  a2011 2019-11-15 2020-11-13  futures\nA2101.XDCE       豆一2101  a2101 2020-01-16 2021-01-15  futures\nA2103.XDCE       豆一2103  a2103 2020-03-16 2021-03-12  futures\nA2105.XDCE       豆一2105  a2105 2020-05-20 2021-05-19  futures\nA2107.XDCE       豆一2107  a2107 2020-07-15 2021-07-14  futures"}
    - {"language":"python","code":"#将所有期货列表转换成数组\nfutures = list(get_all_securities(['futures']).index)\nfutures[:5]\n>>>['A0501.XDCE', 'A0503.XDCE', 'A0505.XDCE', 'A0507.XDCE', 'A0509.XDCE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取期货交易列表"}
    - {"type":"codeblock","language":"python","content":"get_all_securities(types=[], date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取平台支持的所有股票、基金、指数、期货、期权等信息"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'stock', 'fund', 'index', 'futures', 'etf','lof', 'fja', 'fjb','open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'types为空时返回所有股票, 不包括基金,指数和期货"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息"]]}
    - {"type":"heading","level":5,"content":"返回结果"}
    - {"type":"table","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","stock(股票)，index(交易所指数)etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权) , conbond(可转债)"]]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"#获得所有期货列表\ndf=get_all_securities(types=['futures'])\nprint(df[:2])\n\n           display_name   name start_date   end_date     type\nA0501.XDCE       豆一0501  a0501 2003-07-15 2005-01-17  futures\nA0503.XDCE       豆一0503  a0503 2003-09-15 2005-03-14  futures"}
    - {"type":"codeblock","language":"python","content":"#获得2020年10月10日还在上市的所有期货列表\ndf=get_all_securities(types=['futures'],date='2020-10-10')\nprint(df[:5])\n           display_name   name start_date   end_date     type\nA2011.XDCE       豆一2011  a2011 2019-11-15 2020-11-13  futures\nA2101.XDCE       豆一2101  a2101 2020-01-16 2021-01-15  futures\nA2103.XDCE       豆一2103  a2103 2020-03-16 2021-03-12  futures\nA2105.XDCE       豆一2105  a2105 2020-05-20 2021-05-19  futures\nA2107.XDCE       豆一2107  a2107 2020-07-15 2021-07-14  futures"}
    - {"type":"codeblock","language":"python","content":"#将所有期货列表转换成数组\nfutures = list(get_all_securities(['futures']).index)\nfutures[:5]\n>>>['A0501.XDCE', 'A0503.XDCE', 'A0505.XDCE', 'A0507.XDCE', 'A0509.XDCE']"}
  suggestedFilename: "doc_JQDatadoc_10247_overview_获取期货交易列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10247"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取期货交易列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10247

## 描述

描述

## 内容

#### 获取期货交易列表

```python
get_all_securities(types=[], date=None)
```

描述

- 获取平台支持的所有股票、基金、指数、期货、期权等信息

###### 参数

| 属性 | 名称 | 字段类型 | 备注 |
| --- | --- | --- | --- |
| types | 类型 | 用list的形式过滤securities的类型, | list元素可选: 'stock', 'fund', 'index', 'futures', 'etf','lof', 'fja', 'fjb','open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'types为空时返回所有股票, 不包括基金,指数和期货 |
| date | 日期 | 日期字符串或者 [datetime.datetime]/[datetime.date] 对象 | 用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息 |

###### 返回结果

| 字段 | 名称 | 备注 |
| --- | --- | --- |
| display_name | 中文名称 |  |
| name | 缩写简称 |  |
| start_date | 上市日期 |  |
| end_date | 退市日期 | 如果没有退市则为2200-01-01 |
| type | 类型 | stock(股票)，index(交易所指数)etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权) , conbond(可转债) |

示例

```python
#获得所有期货列表
df=get_all_securities(types=['futures'])
print(df[:2])

           display_name   name start_date   end_date     type
A0501.XDCE       豆一0501  a0501 2003-07-15 2005-01-17  futures
A0503.XDCE       豆一0503  a0503 2003-09-15 2005-03-14  futures
```

```python
#获得2020年10月10日还在上市的所有期货列表
df=get_all_securities(types=['futures'],date='2020-10-10')
print(df[:5])
           display_name   name start_date   end_date     type
A2011.XDCE       豆一2011  a2011 2019-11-15 2020-11-13  futures
A2101.XDCE       豆一2101  a2101 2020-01-16 2021-01-15  futures
A2103.XDCE       豆一2103  a2103 2020-03-16 2021-03-12  futures
A2105.XDCE       豆一2105  a2105 2020-05-20 2021-05-19  futures
A2107.XDCE       豆一2107  a2107 2020-07-15 2021-07-14  futures
```

```python
#将所有期货列表转换成数组
futures = list(get_all_securities(['futures']).index)
futures[:5]
>>>['A0501.XDCE', 'A0503.XDCE', 'A0505.XDCE', 'A0507.XDCE', 'A0509.XDCE']
```
