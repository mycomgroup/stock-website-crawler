---
id: "url-36497302"
type: "website"
title: "获取期权交易列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10252"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:45:39.001Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10252"
  headings:
    - {"level":3,"text":"获取期权交易列表","id":""}
    - {"level":5,"text":"参数","id":""}
    - {"level":5,"text":"返回结果","id":""}
  paragraphs:
    - "描述"
    - "示例"
  lists:
    - {"type":"ul","items":["历史范围：2019/12/2至今；更新频率：交易日08:00更新"]}
    - {"type":"ul","items":["获取平台支持的所有股票、基金、指数、期货、期权等信息"]}
  tables:
    - {"caption":"","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'stock', 'fund', 'index', 'futures', 'etf','lof', 'fja', 'fjb','open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'types为空时返回所有股票, 不包括基金,指数和期货"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息"]]}
    - {"caption":"","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","stock(股票)，index(交易所指数))etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权) , conbond(可转债)"]]}
  codeBlocks:
    - {"language":"python","code":"get_all_securities(types=[], date=None)"}
    - {"language":"python","code":"#获得所有期权列表\ndf=get_all_securities(types=['options'])\nprint(df[:2])\n\n                display_name           name start_date   end_date     type\n10000001.XSHG  10000001.XSHG  10000001.XSHG 2015-02-09 2015-03-25  options\n10000002.XSHG  10000002.XSHG  10000002.XSHG 2015-02-09 2015-03-25  options"}
    - {"language":"python","code":"#获得2020年10月10日还在上市的所有期权列表\ndf=get_all_securities(types=['options'],date='2020-10-10')\nprint(df[:5])\n\n                display_name           name start_date   end_date     type\n10002477.XSHG  10002477.XSHG  10002477.XSHG 2020-04-23 2020-12-23  options\n10002478.XSHG  10002478.XSHG  10002478.XSHG 2020-04-23 2020-12-23  options\n10002479.XSHG  10002479.XSHG  10002479.XSHG 2020-04-23 2020-12-23  options\n10002480.XSHG  10002480.XSHG  10002480.XSHG 2020-04-23 2020-12-23  options\n10002481.XSHG  10002481.XSHG  10002481.XSHG 2020-04-23 2020-12-23  options"}
    - {"language":"python","code":"#将所有期权列表转换成数组\noptions= list(get_all_securities(['options']).index)\noptions[:5]\n>>>['10000001.XSHG', '10000002.XSHG','10000003.XSHG','10000004.XSHG','10000005.XSHG']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取期权交易列表"}
    - {"type":"list","listType":"ul","items":["历史范围：2019/12/2至今；更新频率：交易日08:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_all_securities(types=[], date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取平台支持的所有股票、基金、指数、期货、期权等信息"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'stock', 'fund', 'index', 'futures', 'etf','lof', 'fja', 'fjb','open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'types为空时返回所有股票, 不包括基金,指数和期货"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息"]]}
    - {"type":"heading","level":5,"content":"返回结果"}
    - {"type":"table","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","stock(股票)，index(交易所指数))etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权) , conbond(可转债)"]]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"#获得所有期权列表\ndf=get_all_securities(types=['options'])\nprint(df[:2])\n\n                display_name           name start_date   end_date     type\n10000001.XSHG  10000001.XSHG  10000001.XSHG 2015-02-09 2015-03-25  options\n10000002.XSHG  10000002.XSHG  10000002.XSHG 2015-02-09 2015-03-25  options"}
    - {"type":"codeblock","language":"python","content":"#获得2020年10月10日还在上市的所有期权列表\ndf=get_all_securities(types=['options'],date='2020-10-10')\nprint(df[:5])\n\n                display_name           name start_date   end_date     type\n10002477.XSHG  10002477.XSHG  10002477.XSHG 2020-04-23 2020-12-23  options\n10002478.XSHG  10002478.XSHG  10002478.XSHG 2020-04-23 2020-12-23  options\n10002479.XSHG  10002479.XSHG  10002479.XSHG 2020-04-23 2020-12-23  options\n10002480.XSHG  10002480.XSHG  10002480.XSHG 2020-04-23 2020-12-23  options\n10002481.XSHG  10002481.XSHG  10002481.XSHG 2020-04-23 2020-12-23  options"}
    - {"type":"codeblock","language":"python","content":"#将所有期权列表转换成数组\noptions= list(get_all_securities(['options']).index)\noptions[:5]\n>>>['10000001.XSHG', '10000002.XSHG','10000003.XSHG','10000004.XSHG','10000005.XSHG']"}
  suggestedFilename: "doc_JQDatadoc_10252_overview_获取期权交易列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10252"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取期权交易列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10252

## 描述

描述

## 内容

#### 获取期权交易列表

- 历史范围：2019/12/2至今；更新频率：交易日08:00更新

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
| type | 类型 | stock(股票)，index(交易所指数))etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权) , conbond(可转债) |

示例

```python
#获得所有期权列表
df=get_all_securities(types=['options'])
print(df[:2])

                display_name           name start_date   end_date     type
10000001.XSHG  10000001.XSHG  10000001.XSHG 2015-02-09 2015-03-25  options
10000002.XSHG  10000002.XSHG  10000002.XSHG 2015-02-09 2015-03-25  options
```

```python
#获得2020年10月10日还在上市的所有期权列表
df=get_all_securities(types=['options'],date='2020-10-10')
print(df[:5])

                display_name           name start_date   end_date     type
10002477.XSHG  10002477.XSHG  10002477.XSHG 2020-04-23 2020-12-23  options
10002478.XSHG  10002478.XSHG  10002478.XSHG 2020-04-23 2020-12-23  options
10002479.XSHG  10002479.XSHG  10002479.XSHG 2020-04-23 2020-12-23  options
10002480.XSHG  10002480.XSHG  10002480.XSHG 2020-04-23 2020-12-23  options
10002481.XSHG  10002481.XSHG  10002481.XSHG 2020-04-23 2020-12-23  options
```

```python
#将所有期权列表转换成数组
options= list(get_all_securities(['options']).index)
options[:5]
>>>['10000001.XSHG', '10000002.XSHG','10000003.XSHG','10000004.XSHG','10000005.XSHG']
```
