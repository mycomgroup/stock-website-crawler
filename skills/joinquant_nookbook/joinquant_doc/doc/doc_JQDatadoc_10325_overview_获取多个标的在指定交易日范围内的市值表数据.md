---
id: "url-36496f9b"
type: "website"
title: "获取多个标的在指定交易日范围内的市值表数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10325"
description: "参数"
source: ""
tags: []
crawl_time: "2026-03-27T07:29:52.401Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10325"
  headings:
    - {"level":3,"text":"获取多个标的在指定交易日范围内的市值表数据","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "参数"
    - "返回值"
    - "注意"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；","更新时间：每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空；每天盘后(16:00)更新全部指标"]}
    - {"type":"ul","items":["security_list：标的code字符串列表或者单个标的字符串","end_date: 查询结束时间","start_date: 查询开始时间，不能与count共用","count: 表示往前查询每一个标的count个交易日的数据，如果期间标的停牌，则该标的返回的市值数据数量小于count","fields: 财务数据中市值表的字段，返回结果中总会包含code、day字段，可用字段如下："]}
    - {"type":"ul","items":["返回一个dataframe，索引默认是pandas的整数索引，返回的结果中总会包含code、day字段。"]}
    - {"type":"ul","items":["每次最多返回10000条数据，更多数据需要根据标的或者时间分多次获取"]}
  tables:
    - {"caption":"","headers":["列名","列的含义","解释","公式"],"rows":[["code","股票代码","带后缀.XSHE/.XSHG",""],["day","日期","取数据的日期",""],["capitalization","总股本(万股)","公司已发行的普通股股份总数(包含A股，B股和H股的总股本)",""],["circulating_cap","流通股本(万股)","公司已发行的境内上市流通、以人民币兑换的股份总数(A股市场的流通股本)",""],["market_cap","总市值(亿元)","A股收盘价*已发行股票总股本（A股+B股+H股）",""],["circulating_market_cap","流通市值(亿元)","流通市值指在某特定时间内当时可交易的流通股股数乘以当时股价得出的流通股票总价值。","A股市场的收盘价*A股市场的流通股数"],["turnover_ratio","换手率(%)","指在一定时间内市场中股票转手买卖的频率，是反映股票流通性强弱的指标之一。","换手率=[指定交易日成交量(手)*100/截至该日股票的流通股本(股)]*100%"],["pe_ratio","市盈率(PE, TTM)","每股市价为每股收益的倍数，反映投资人对每元净利润所愿支付的价格，用来估计股票的投资报酬和风险","市盈率（PE，TTM）=（股票在指定交易日期的收盘价* 截止当日公司总股本）/归属于母公司股东的净利润TTM"],["pe_ratio_lyr","市盈率(PE)","以上一年度每股盈利计算的静态市盈率. 股价/最近年度报告EPS","市盈率（PE）=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/归属母公司股东的净利润"],["pb_ratio","市净率(PB)","每股股价与每股净资产的比率","市净率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/(归属母公司股东的权益 MRQ-其他权益工具)"],["ps_ratio","市销率(PS, TTM)","市销率为股票价格与每股销售收入之比，市销率越小，通常被认为投资价值越高。","市销率TTM=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/营业总收入TTM"],["pcf_ratio","市现率(PCF, 现金净流量TTM)","每股市价为每股现金净流量的倍数","市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/现金及现金等价物净增加额TTM"],["pcf_ratio2","市现率(PCF,经营活动现金流TTM)","每股市价为每股经营活动现金净流量的倍数(jqdtasdk1.9.5新增)","市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/经营活动现金及经营活动现金等价物净增加额TTM"],["dividend_ratio","股息率(TTM) %","使用除权除息日进行统计(jqdtasdk1.9.5新增)","(近12个月派现合计/总市值)/100"],["free_cap","自由流通股本(万股)","流通股本-其他扣除数(如高管限售25%)(jqdtasdk1.9.5新增)",""],["free_market_cap","自由流通市值(亿元)","A股收盘价*自由流通股本(jqdtasdk1.9.5新增)",""],["a_cap","A股总股本(万股)","公司已发行的普通股股份A股总数(jqdtasdk1.9.5新增)",""],["a_market_cap","A股总市值(亿元)","A股收盘价*A股总股本(jqdtasdk1.9.5新增)",""]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import *\nget_valuation(security_list, start_date=None, end_date=None, fields=None, count=None)"}
    - {"language":"python","code":"from jqdatasdk import *\n# 传入单个标的\ndf1 = get_valuation('000001.XSHE', end_date=\"2019-11-18\", count=3)\nprint(df1)\n\n# 传入多个标的\ndf2 = get_valuation(['000001.XSHE', '000002.XSHE'], end_date=\"2019-11-18\", count=3)\nprint(df2)"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取多个标的在指定交易日范围内的市值表数据"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；","更新时间：每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空；每天盘后(16:00)更新全部指标"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\nget_valuation(security_list, start_date=None, end_date=None, fields=None, count=None)"}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["security_list：标的code字符串列表或者单个标的字符串","end_date: 查询结束时间","start_date: 查询开始时间，不能与count共用","count: 表示往前查询每一个标的count个交易日的数据，如果期间标的停牌，则该标的返回的市值数据数量小于count","fields: 财务数据中市值表的字段，返回结果中总会包含code、day字段，可用字段如下："]}
    - {"type":"table","headers":["列名","列的含义","解释","公式"],"rows":[["code","股票代码","带后缀.XSHE/.XSHG",""],["day","日期","取数据的日期",""],["capitalization","总股本(万股)","公司已发行的普通股股份总数(包含A股，B股和H股的总股本)",""],["circulating_cap","流通股本(万股)","公司已发行的境内上市流通、以人民币兑换的股份总数(A股市场的流通股本)",""],["market_cap","总市值(亿元)","A股收盘价*已发行股票总股本（A股+B股+H股）",""],["circulating_market_cap","流通市值(亿元)","流通市值指在某特定时间内当时可交易的流通股股数乘以当时股价得出的流通股票总价值。","A股市场的收盘价*A股市场的流通股数"],["turnover_ratio","换手率(%)","指在一定时间内市场中股票转手买卖的频率，是反映股票流通性强弱的指标之一。","换手率=[指定交易日成交量(手)*100/截至该日股票的流通股本(股)]*100%"],["pe_ratio","市盈率(PE, TTM)","每股市价为每股收益的倍数，反映投资人对每元净利润所愿支付的价格，用来估计股票的投资报酬和风险","市盈率（PE，TTM）=（股票在指定交易日期的收盘价* 截止当日公司总股本）/归属于母公司股东的净利润TTM"],["pe_ratio_lyr","市盈率(PE)","以上一年度每股盈利计算的静态市盈率. 股价/最近年度报告EPS","市盈率（PE）=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/归属母公司股东的净利润"],["pb_ratio","市净率(PB)","每股股价与每股净资产的比率","市净率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/(归属母公司股东的权益 MRQ-其他权益工具)"],["ps_ratio","市销率(PS, TTM)","市销率为股票价格与每股销售收入之比，市销率越小，通常被认为投资价值越高。","市销率TTM=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/营业总收入TTM"],["pcf_ratio","市现率(PCF, 现金净流量TTM)","每股市价为每股现金净流量的倍数","市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/现金及现金等价物净增加额TTM"],["pcf_ratio2","市现率(PCF,经营活动现金流TTM)","每股市价为每股经营活动现金净流量的倍数(jqdtasdk1.9.5新增)","市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/经营活动现金及经营活动现金等价物净增加额TTM"],["dividend_ratio","股息率(TTM) %","使用除权除息日进行统计(jqdtasdk1.9.5新增)","(近12个月派现合计/总市值)/100"],["free_cap","自由流通股本(万股)","流通股本-其他扣除数(如高管限售25%)(jqdtasdk1.9.5新增)",""],["free_market_cap","自由流通市值(亿元)","A股收盘价*自由流通股本(jqdtasdk1.9.5新增)",""],["a_cap","A股总股本(万股)","公司已发行的普通股股份A股总数(jqdtasdk1.9.5新增)",""],["a_market_cap","A股总市值(亿元)","A股收盘价*A股总股本(jqdtasdk1.9.5新增)",""]]}
    - {"type":"paragraph","content":"返回值"}
    - {"type":"list","listType":"ul","items":["返回一个dataframe，索引默认是pandas的整数索引，返回的结果中总会包含code、day字段。"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["每次最多返回10000条数据，更多数据需要根据标的或者时间分多次获取"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\n# 传入单个标的\ndf1 = get_valuation('000001.XSHE', end_date=\"2019-11-18\", count=3)\nprint(df1)\n\n# 传入多个标的\ndf2 = get_valuation(['000001.XSHE', '000002.XSHE'], end_date=\"2019-11-18\", count=3)\nprint(df2)"}
  suggestedFilename: "doc_JQDatadoc_10325_overview_获取多个标的在指定交易日范围内的市值表数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10325"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取多个标的在指定交易日范围内的市值表数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10325

## 描述

参数

## 内容

#### 获取多个标的在指定交易日范围内的市值表数据

- 历史范围：2005年至今；
- 更新时间：每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空；每天盘后(16:00)更新全部指标

```python
from jqdatasdk import *
get_valuation(security_list, start_date=None, end_date=None, fields=None, count=None)
```

参数

- security_list：标的code字符串列表或者单个标的字符串
- end_date: 查询结束时间
- start_date: 查询开始时间，不能与count共用
- count: 表示往前查询每一个标的count个交易日的数据，如果期间标的停牌，则该标的返回的市值数据数量小于count
- fields: 财务数据中市值表的字段，返回结果中总会包含code、day字段，可用字段如下：

| 列名 | 列的含义 | 解释 | 公式 |
| --- | --- | --- | --- |
| code | 股票代码 | 带后缀.XSHE/.XSHG |  |
| day | 日期 | 取数据的日期 |  |
| capitalization | 总股本(万股) | 公司已发行的普通股股份总数(包含A股，B股和H股的总股本) |  |
| circulating_cap | 流通股本(万股) | 公司已发行的境内上市流通、以人民币兑换的股份总数(A股市场的流通股本) |  |
| market_cap | 总市值(亿元) | A股收盘价*已发行股票总股本（A股+B股+H股） |  |
| circulating_market_cap | 流通市值(亿元) | 流通市值指在某特定时间内当时可交易的流通股股数乘以当时股价得出的流通股票总价值。 | A股市场的收盘价*A股市场的流通股数 |
| turnover_ratio | 换手率(%) | 指在一定时间内市场中股票转手买卖的频率，是反映股票流通性强弱的指标之一。 | 换手率=[指定交易日成交量(手)*100/截至该日股票的流通股本(股)]*100% |
| pe_ratio | 市盈率(PE, TTM) | 每股市价为每股收益的倍数，反映投资人对每元净利润所愿支付的价格，用来估计股票的投资报酬和风险 | 市盈率（PE，TTM）=（股票在指定交易日期的收盘价* 截止当日公司总股本）/归属于母公司股东的净利润TTM |
| pe_ratio_lyr | 市盈率(PE) | 以上一年度每股盈利计算的静态市盈率. 股价/最近年度报告EPS | 市盈率（PE）=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/归属母公司股东的净利润 |
| pb_ratio | 市净率(PB) | 每股股价与每股净资产的比率 | 市净率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/(归属母公司股东的权益 MRQ-其他权益工具) |
| ps_ratio | 市销率(PS, TTM) | 市销率为股票价格与每股销售收入之比，市销率越小，通常被认为投资价值越高。 | 市销率TTM=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/营业总收入TTM |
| pcf_ratio | 市现率(PCF, 现金净流量TTM) | 每股市价为每股现金净流量的倍数 | 市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/现金及现金等价物净增加额TTM |
| pcf_ratio2 | 市现率(PCF,经营活动现金流TTM) | 每股市价为每股经营活动现金净流量的倍数(jqdtasdk1.9.5新增) | 市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/经营活动现金及经营活动现金等价物净增加额TTM |
| dividend_ratio | 股息率(TTM) % | 使用除权除息日进行统计(jqdtasdk1.9.5新增) | (近12个月派现合计/总市值)/100 |
| free_cap | 自由流通股本(万股) | 流通股本-其他扣除数(如高管限售25%)(jqdtasdk1.9.5新增) |  |
| free_market_cap | 自由流通市值(亿元) | A股收盘价*自由流通股本(jqdtasdk1.9.5新增) |  |
| a_cap | A股总股本(万股) | 公司已发行的普通股股份A股总数(jqdtasdk1.9.5新增) |  |
| a_market_cap | A股总市值(亿元) | A股收盘价*A股总股本(jqdtasdk1.9.5新增) |  |

返回值

- 返回一个dataframe，索引默认是pandas的整数索引，返回的结果中总会包含code、day字段。

注意

- 每次最多返回10000条数据，更多数据需要根据标的或者时间分多次获取

###### 示例

```python
from jqdatasdk import *
# 传入单个标的
df1 = get_valuation('000001.XSHE', end_date="2019-11-18", count=3)
print(df1)

# 传入多个标的
df2 = get_valuation(['000001.XSHE', '000002.XSHE'], end_date="2019-11-18", count=3)
print(df2)
```
