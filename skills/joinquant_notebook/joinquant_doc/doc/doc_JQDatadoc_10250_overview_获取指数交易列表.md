---
id: "url-36497304"
type: "website"
title: "获取指数交易列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10250"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:35.081Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10250"
  headings:
    - {"level":3,"text":"获取指数交易列表","id":""}
    - {"level":5,"text":"参数","id":"-1"}
    - {"level":5,"text":"返回结果","id":"-2"}
  paragraphs:
    - "描述"
    - "示例"
  lists:
    - {"type":"ul","items":["获取平台支持的所有股票、基金、指数、期货、期权等信息"]}
  tables:
    - {"caption":"","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'stock', 'fund', 'index', 'futures', 'etf','lof', 'fja', 'fjb','open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'types为空时返回所有股票, 不包括基金,指数和期货"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息"]]}
    - {"caption":"","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","stock(股票)，index(指数)，etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权)"]]}
  codeBlocks:
    - {"language":"python","code":"get_all_securities(types=[], date=None)"}
    - {"language":"python","code":"#获得所有指数列表\ndf=get_all_securities(types=['index'])\nprint(df[:2])\n\n            display_name  name start_date   end_date   type\n000001.XSHG         上证指数  SZZS 1991-07-15 2200-01-01  index\n000002.XSHG         A股指数  AGZS 1992-02-21 2200-01-01  index"}
    - {"language":"python","code":"#获得2020年10月10日还在上市的所有指数列表\ndf=get_all_securities(types=['index'],date='2020-10-10')\nprint(df[:5])\n            display_name  name start_date   end_date   type\n000001.XSHG         上证指数  SZZS 1991-07-15 2200-01-01  index\n000002.XSHG         A股指数  AGZS 1992-02-21 2200-01-01  index\n000003.XSHG         B股指数  BGZS 1992-02-21 2200-01-01  index\n000004.XSHG         工业指数  GYZS 1993-05-03 2200-01-01  index\n000005.XSHG         商业指数  SYZS 1993-05-03 2200-01-01  index"}
    - {"language":"python","code":"#将所有指数列表转换成数组\nindex = list(get_all_securities(['index']).index)\nindex[:5]\n>>>['000001.XSHG', '000002.XSHG', '000003.XSHG', '000004.XSHG', '000005.XSHG']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取指数交易列表"}
    - {"type":"codeblock","language":"python","content":"get_all_securities(types=[], date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取平台支持的所有股票、基金、指数、期货、期权等信息"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'stock', 'fund', 'index', 'futures', 'etf','lof', 'fja', 'fjb','open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'types为空时返回所有股票, 不包括基金,指数和期货"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息"]]}
    - {"type":"heading","level":5,"content":"返回结果"}
    - {"type":"table","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","stock(股票)，index(指数)，etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权)"]]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"#获得所有指数列表\ndf=get_all_securities(types=['index'])\nprint(df[:2])\n\n            display_name  name start_date   end_date   type\n000001.XSHG         上证指数  SZZS 1991-07-15 2200-01-01  index\n000002.XSHG         A股指数  AGZS 1992-02-21 2200-01-01  index"}
    - {"type":"codeblock","language":"python","content":"#获得2020年10月10日还在上市的所有指数列表\ndf=get_all_securities(types=['index'],date='2020-10-10')\nprint(df[:5])\n            display_name  name start_date   end_date   type\n000001.XSHG         上证指数  SZZS 1991-07-15 2200-01-01  index\n000002.XSHG         A股指数  AGZS 1992-02-21 2200-01-01  index\n000003.XSHG         B股指数  BGZS 1992-02-21 2200-01-01  index\n000004.XSHG         工业指数  GYZS 1993-05-03 2200-01-01  index\n000005.XSHG         商业指数  SYZS 1993-05-03 2200-01-01  index"}
    - {"type":"codeblock","language":"python","content":"#将所有指数列表转换成数组\nindex = list(get_all_securities(['index']).index)\nindex[:5]\n>>>['000001.XSHG', '000002.XSHG', '000003.XSHG', '000004.XSHG', '000005.XSHG']"}
  suggestedFilename: "doc_JQDatadoc_10250_overview_获取指数交易列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10250"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取指数交易列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10250

## 描述

描述

## 内容

#### 获取指数交易列表

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
| type | 类型 | stock(股票)，index(指数)，etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）, bond_fund（债券基金）, stock_fund（股票型基金）, QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）, mixture_fund（混合型基金）, options(期权) |

示例

```python
#获得所有指数列表
df=get_all_securities(types=['index'])
print(df[:2])

            display_name  name start_date   end_date   type
000001.XSHG         上证指数  SZZS 1991-07-15 2200-01-01  index
000002.XSHG         A股指数  AGZS 1992-02-21 2200-01-01  index
```

```python
#获得2020年10月10日还在上市的所有指数列表
df=get_all_securities(types=['index'],date='2020-10-10')
print(df[:5])
            display_name  name start_date   end_date   type
000001.XSHG         上证指数  SZZS 1991-07-15 2200-01-01  index
000002.XSHG         A股指数  AGZS 1992-02-21 2200-01-01  index
000003.XSHG         B股指数  BGZS 1992-02-21 2200-01-01  index
000004.XSHG         工业指数  GYZS 1993-05-03 2200-01-01  index
000005.XSHG         商业指数  SYZS 1993-05-03 2200-01-01  index
```

```python
#将所有指数列表转换成数组
index = list(get_all_securities(['index']).index)
index[:5]
>>>['000001.XSHG', '000002.XSHG', '000003.XSHG', '000004.XSHG', '000005.XSHG']
```
