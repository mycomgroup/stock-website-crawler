---
id: "url-3649731f"
type: "website"
title: "获取单支标的信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10244"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:48:48.030Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10244"
  headings:
    - {"level":3,"text":"获取单支标的信息","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["code: 证券代码","使用方式:接口+.属性，具体属性说明如下图"]}
    - {"type":"ul","items":["使用get_all_securities方法，即可获取完整的证券交易列表代码"]}
    - {"type":"ul","items":["获取中文名称"]}
  tables:
    - {"caption":"","headers":["属性","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期","[datetime.date] 类型"],["end_date","退市日期","[datetime.date] 类型, 如果没有退市则为2200-01-01)"],["type","类型","stock(股票),index(交易所指数) ,options(期权) , conbond(可转债),futures（期货) etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）,’bond_fund（债券基金）, stock_fund（股票型基金）QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）,mixture_fund（混合型基金）,"]]}
  codeBlocks:
    - {"language":"python","code":"get_security_info(code,date=None)"}
    - {"language":"python","code":"# 获取000001.XSHE某一日期的中文名称\ndisplay_name = get_security_info('000001.XSHE',date='2017-08-31’).display_name\nprint(display_name)\n>>>平安银行\n\n#获取000001.XSHE的上市时间\nstart_date = get_security_info('000001.XSHE').start_date\nprint(start_date)\n>>>1991-04-03"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取单支标的信息"}
    - {"type":"codeblock","language":"python","content":"get_security_info(code,date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["code: 证券代码","使用方式:接口+.属性，具体属性说明如下图"]}
    - {"type":"list","listType":"ul","items":["使用get_all_securities方法，即可获取完整的证券交易列表代码"]}
    - {"type":"table","headers":["属性","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期","[datetime.date] 类型"],["end_date","退市日期","[datetime.date] 类型, 如果没有退市则为2200-01-01)"],["type","类型","stock(股票),index(交易所指数) ,options(期权) , conbond(可转债),futures（期货) etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）,’bond_fund（债券基金）, stock_fund（股票型基金）QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）,mixture_fund（混合型基金）,"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获取中文名称"]}
    - {"type":"codeblock","language":"python","content":"# 获取000001.XSHE某一日期的中文名称\ndisplay_name = get_security_info('000001.XSHE',date='2017-08-31’).display_name\nprint(display_name)\n>>>平安银行\n\n#获取000001.XSHE的上市时间\nstart_date = get_security_info('000001.XSHE').start_date\nprint(start_date)\n>>>1991-04-03"}
  suggestedFilename: "doc_JQDatadoc_10244_overview_获取单支标的信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10244"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取单支标的信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10244

## 描述

描述

## 内容

#### 获取单支标的信息

```python
get_security_info(code,date=None)
```

描述

- code: 证券代码
- 使用方式:接口+.属性，具体属性说明如下图

- 使用get_all_securities方法，即可获取完整的证券交易列表代码

| 属性 | 名称 | 备注 |
| --- | --- | --- |
| display_name | 中文名称 |  |
| name | 缩写简称 |  |
| start_date | 上市日期 | [datetime.date] 类型 |
| end_date | 退市日期 | [datetime.date] 类型, 如果没有退市则为2200-01-01) |
| type | 类型 | stock(股票),index(交易所指数) ,options(期权) , conbond(可转债),futures（期货) etf(ETF基金)，fja（分级A），fjb（分级B），fjm（分级母基金），mmf（场内交易的货币基金）open_fund（开放式基金）,’bond_fund（债券基金）, stock_fund（股票型基金）QDII_fund（QDII 基金）, money_market_fund（场外交易的货币基金）,mixture_fund（混合型基金）, |

###### 示例

- 获取中文名称

```python
# 获取000001.XSHE某一日期的中文名称
display_name = get_security_info('000001.XSHE',date='2017-08-31’).display_name
print(display_name)
>>>平安银行

#获取000001.XSHE的上市时间
start_date = get_security_info('000001.XSHE').start_date
print(start_date)
>>>1991-04-03
```
