---
id: "url-7a226b13"
type: "website"
title: "龙虎榜数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9857"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:21.874Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9857"
  headings:
    - {"level":3,"text":"龙虎榜数据","id":""}
    - {"level":5,"text":"参数","id":"-1"}
    - {"level":5,"text":"返回值","id":"-2"}
    - {"level":5,"text":"示例","id":"-3"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2010年至今；更新时间：盘后20:00和22:00更新"]}
    - {"type":"ul","items":["获取指定日期区间内的龙虎榜数据"]}
    - {"type":"ul","items":["abnormal_code异常波动类型说明"]}
  tables:
    - {"caption":"","headers":["参数","名称","注释"],"rows":[["stock_list","股票列表","一个股票代码的 list。 当值为 None 时， 返回指定日期的所有股票。"],["start_date","开始日期","一个字符串或者 [datetime.datetime]/[datetime.date] 对象"],["end_date","结束日期","一个字符串或者 [datetime.date]/[datetime.datetime] 对象"],["count","数量","交易日数量， 可以与 end_date 同时使用， 表示获取 end_date 前 count 个交易日的数据(含 end_date 当日)"]]}
    - {"caption":"","headers":["参数","名称"],"rows":[["code","股票代码"],["day","日期"],["direction","ALL 表示『汇总』，SELL 表示『卖』，BUY 表示『买』"],["abnormal_code","异常波动类型"],["abnormal_name","异常波动名称"],["sales_depart_name","营业部名称"],["rank","0 表示汇总， 1~5 对应买入金额或卖出金额排名第一到第五"],["buy_value","买入金额"],["buy_rate","买入金额占比(买入金额/市场总成交额)"],["sell_value","卖出金额"],["sell_rate","卖出金额占比(卖出金额/市场总成交额)"],["net_value","净额(买入金额 - 卖出金额)"],["amount","市场总成交额"]]}
    - {"caption":"","headers":["参数编码","参数名称"],"rows":[["106001","涨幅偏离值达7%的证券"],["106002","跌幅偏离值达7%的证券"],["106003","日价格振幅达到15%的证券"],["106004","换手率达20%的证券"],["106005","无价格涨跌幅限制的证券"],["106006","连续三个交易日内收盘价格涨幅偏离值累计达到20%的证券"],["106007","连续三个交易日内收盘价格跌幅偏离值累计达到20%的证券"],["106008","连续三个交易日内收盘价格涨幅偏离值累计达到15%的证券"],["106009","连续三个交易日内收盘价格跌幅偏离值累计达到15%的证券"],["106010","连续三个交易日内涨幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券"],["106011","连续三个交易日内跌幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券"],["106012","连续三个交易日的日均换手率与前五个交易日日均换手率的比值到达30倍"],["106013","单只标的证券的当日融资买入数量达到当日该证券总交易量的50％以上的证券"],["106014","单只标的证券的当日融券卖出数量达到当日该证券总交易量的50％以上的证券"],["106015","日价格涨幅达到20%的证券"],["106016","日价格跌幅达到-15%的证券"],["106017","严重异常期间日收盘价格涨幅偏离值累计达到108%的证券"],["106018","严重异常期间日收盘价格跌幅偏离值累计达到-50%的证券"],["106099","其它异常波动的证券"]]}
  codeBlocks:
    - {"language":"python","code":"get_billboard_list(stock_list, start_date, end_date, count)"}
    - {"language":"python","code":"# 获取2018-08-01的龙虎榜数据,count表示交易日数量\ndf=get_billboard_list(stock_list=None, end_date = '2022-08-01', count =1)\nprint(df[:3])\n\n          code         day direction  rank  abnormal_code  \\\n0  688786.XSHG  2022-08-01      SELL     1         106019   \n1  688786.XSHG  2022-08-01      SELL     3         106019   \n2  688786.XSHG  2022-08-01      SELL     4         106019   \n\n                 abnormal_name         sales_depart_name  buy_value  buy_rate  \\\n0  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券  招商证券股份有限公司深圳深南大道车公庙证券营业部        NaN       NaN   \n1  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券      华泰证券股份有限公司苏州人民路证券营业部        NaN       NaN   \n2  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券                      机构专用        NaN       NaN   \n\n   sell_value  sell_rate  total_value  net_value    amount  \n0      731.35     3.7839       731.35    -731.35  19328.09  \n1      655.67     3.3923       655.67    -655.67  19328.09  \n2      630.45     3.2618       630.45    -630.45  19328.09"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"龙虎榜数据"}
    - {"type":"list","listType":"ul","items":["历史范围：2010年至今；更新时间：盘后20:00和22:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_billboard_list(stock_list, start_date, end_date, count)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取指定日期区间内的龙虎榜数据"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["参数","名称","注释"],"rows":[["stock_list","股票列表","一个股票代码的 list。 当值为 None 时， 返回指定日期的所有股票。"],["start_date","开始日期","一个字符串或者 [datetime.datetime]/[datetime.date] 对象"],["end_date","结束日期","一个字符串或者 [datetime.date]/[datetime.datetime] 对象"],["count","数量","交易日数量， 可以与 end_date 同时使用， 表示获取 end_date 前 count 个交易日的数据(含 end_date 当日)"]]}
    - {"type":"heading","level":5,"content":"返回值"}
    - {"type":"table","headers":["参数","名称"],"rows":[["code","股票代码"],["day","日期"],["direction","ALL 表示『汇总』，SELL 表示『卖』，BUY 表示『买』"],["abnormal_code","异常波动类型"],["abnormal_name","异常波动名称"],["sales_depart_name","营业部名称"],["rank","0 表示汇总， 1~5 对应买入金额或卖出金额排名第一到第五"],["buy_value","买入金额"],["buy_rate","买入金额占比(买入金额/市场总成交额)"],["sell_value","卖出金额"],["sell_rate","卖出金额占比(卖出金额/市场总成交额)"],["net_value","净额(买入金额 - 卖出金额)"],["amount","市场总成交额"]]}
    - {"type":"list","listType":"ul","items":["abnormal_code异常波动类型说明"]}
    - {"type":"table","headers":["参数编码","参数名称"],"rows":[["106001","涨幅偏离值达7%的证券"],["106002","跌幅偏离值达7%的证券"],["106003","日价格振幅达到15%的证券"],["106004","换手率达20%的证券"],["106005","无价格涨跌幅限制的证券"],["106006","连续三个交易日内收盘价格涨幅偏离值累计达到20%的证券"],["106007","连续三个交易日内收盘价格跌幅偏离值累计达到20%的证券"],["106008","连续三个交易日内收盘价格涨幅偏离值累计达到15%的证券"],["106009","连续三个交易日内收盘价格跌幅偏离值累计达到15%的证券"],["106010","连续三个交易日内涨幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券"],["106011","连续三个交易日内跌幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券"],["106012","连续三个交易日的日均换手率与前五个交易日日均换手率的比值到达30倍"],["106013","单只标的证券的当日融资买入数量达到当日该证券总交易量的50％以上的证券"],["106014","单只标的证券的当日融券卖出数量达到当日该证券总交易量的50％以上的证券"],["106015","日价格涨幅达到20%的证券"],["106016","日价格跌幅达到-15%的证券"],["106017","严重异常期间日收盘价格涨幅偏离值累计达到108%的证券"],["106018","严重异常期间日收盘价格跌幅偏离值累计达到-50%的证券"],["106099","其它异常波动的证券"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 获取2018-08-01的龙虎榜数据,count表示交易日数量\ndf=get_billboard_list(stock_list=None, end_date = '2022-08-01', count =1)\nprint(df[:3])\n\n          code         day direction  rank  abnormal_code  \\\n0  688786.XSHG  2022-08-01      SELL     1         106019   \n1  688786.XSHG  2022-08-01      SELL     3         106019   \n2  688786.XSHG  2022-08-01      SELL     4         106019   \n\n                 abnormal_name         sales_depart_name  buy_value  buy_rate  \\\n0  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券  招商证券股份有限公司深圳深南大道车公庙证券营业部        NaN       NaN   \n1  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券      华泰证券股份有限公司苏州人民路证券营业部        NaN       NaN   \n2  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券                      机构专用        NaN       NaN   \n\n   sell_value  sell_rate  total_value  net_value    amount  \n0      731.35     3.7839       731.35    -731.35  19328.09  \n1      655.67     3.3923       655.67    -655.67  19328.09  \n2      630.45     3.2618       630.45    -630.45  19328.09"}
  suggestedFilename: "doc_JQDatadoc_9857_overview_龙虎榜数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9857"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 龙虎榜数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9857

## 描述

描述

## 内容

#### 龙虎榜数据

- 历史范围：2010年至今；更新时间：盘后20:00和22:00更新

```python
get_billboard_list(stock_list, start_date, end_date, count)
```

描述

- 获取指定日期区间内的龙虎榜数据

###### 参数

| 参数 | 名称 | 注释 |
| --- | --- | --- |
| stock_list | 股票列表 | 一个股票代码的 list。 当值为 None 时， 返回指定日期的所有股票。 |
| start_date | 开始日期 | 一个字符串或者 [datetime.datetime]/[datetime.date] 对象 |
| end_date | 结束日期 | 一个字符串或者 [datetime.date]/[datetime.datetime] 对象 |
| count | 数量 | 交易日数量， 可以与 end_date 同时使用， 表示获取 end_date 前 count 个交易日的数据(含 end_date 当日) |

###### 返回值

| 参数 | 名称 |
| --- | --- |
| code | 股票代码 |
| day | 日期 |
| direction | ALL 表示『汇总』，SELL 表示『卖』，BUY 表示『买』 |
| abnormal_code | 异常波动类型 |
| abnormal_name | 异常波动名称 |
| sales_depart_name | 营业部名称 |
| rank | 0 表示汇总， 1~5 对应买入金额或卖出金额排名第一到第五 |
| buy_value | 买入金额 |
| buy_rate | 买入金额占比(买入金额/市场总成交额) |
| sell_value | 卖出金额 |
| sell_rate | 卖出金额占比(卖出金额/市场总成交额) |
| net_value | 净额(买入金额 - 卖出金额) |
| amount | 市场总成交额 |

- abnormal_code异常波动类型说明

| 参数编码 | 参数名称 |
| --- | --- |
| 106001 | 涨幅偏离值达7%的证券 |
| 106002 | 跌幅偏离值达7%的证券 |
| 106003 | 日价格振幅达到15%的证券 |
| 106004 | 换手率达20%的证券 |
| 106005 | 无价格涨跌幅限制的证券 |
| 106006 | 连续三个交易日内收盘价格涨幅偏离值累计达到20%的证券 |
| 106007 | 连续三个交易日内收盘价格跌幅偏离值累计达到20%的证券 |
| 106008 | 连续三个交易日内收盘价格涨幅偏离值累计达到15%的证券 |
| 106009 | 连续三个交易日内收盘价格跌幅偏离值累计达到15%的证券 |
| 106010 | 连续三个交易日内涨幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券 |
| 106011 | 连续三个交易日内跌幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券 |
| 106012 | 连续三个交易日的日均换手率与前五个交易日日均换手率的比值到达30倍 |
| 106013 | 单只标的证券的当日融资买入数量达到当日该证券总交易量的50％以上的证券 |
| 106014 | 单只标的证券的当日融券卖出数量达到当日该证券总交易量的50％以上的证券 |
| 106015 | 日价格涨幅达到20%的证券 |
| 106016 | 日价格跌幅达到-15%的证券 |
| 106017 | 严重异常期间日收盘价格涨幅偏离值累计达到108%的证券 |
| 106018 | 严重异常期间日收盘价格跌幅偏离值累计达到-50%的证券 |
| 106099 | 其它异常波动的证券 |

###### 示例

```python
# 获取2018-08-01的龙虎榜数据,count表示交易日数量
df=get_billboard_list(stock_list=None, end_date = '2022-08-01', count =1)
print(df[:3])

          code         day direction  rank  abnormal_code  \
0  688786.XSHG  2022-08-01      SELL     1         106019   
1  688786.XSHG  2022-08-01      SELL     3         106019   
2  688786.XSHG  2022-08-01      SELL     4         106019   

                 abnormal_name         sales_depart_name  buy_value  buy_rate  \
0  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券  招商证券股份有限公司深圳深南大道车公庙证券营业部        NaN       NaN   
1  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券      华泰证券股份有限公司苏州人民路证券营业部        NaN       NaN   
2  有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券                      机构专用        NaN       NaN   

   sell_value  sell_rate  total_value  net_value    amount  
0      731.35     3.7839       731.35    -731.35  19328.09  
1      655.67     3.3923       655.67    -655.67  19328.09  
2      630.45     3.2618       630.45    -630.45  19328.09
```
