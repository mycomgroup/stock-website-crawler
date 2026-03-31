---
id: "url-7a226e95"
type: "website"
title: "基金资产组合概况"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9936"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:20:47.995Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9936"
  headings:
    - {"level":3,"text":"基金资产组合概况","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "基金持股信息参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"ul","items":["基金资产组合概况"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.FUND_PORTFOLIO)表示从finance.FUND_PORTFOLIO这张表中查询基金资产组合概况数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_PORTFOLIO：收录了基金资产组合概况数据，表结构和字段信息如下：","finance.FUND_PORTFOLIO.code==code：指定筛选条件，通过finance.FUND_PORTFOLIO.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"ul","items":["场内基金"]}
    - {"type":"ul","items":["场外基金"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型"],"rows":[["code","基金代码","varchar(12)"],["name","基金名称","varchar(80)"],["period_start","开始日期","date"],["period_end","报告期","date"],["pub_date","公告日期","date"],["report_type_id","报告类型编码","int"],["report_type","报告类型","varchar(32)"],["equity_value","权益类投资金额","decimal(20,4)"],["equity_rate","权益类投资占比","decimal(10,4)"],["stock_value","股票投资金额","decimal(20,4)"],["stock_rate","股票投资占比","decimal(10,4)"],["fixed_income_value","固定收益投资金额","decimal(20,4)"],["fixed_income_rate","固定收益投资占比","decimal(10,4)"],["precious_metal_value","贵金属投资金额","decimal(20,4)"],["precious_metal_rate","贵金属投资占比","decimal(10,4)"],["derivative_value","金融衍生品投资金额","decimal(20,4)"],["derivative_rate","金融衍生品投资占比","decimal(10,4)"],["buying_back_value","买入返售金融资产金额","decimal(20,4)"],["buying_back_rate","买入返售金融资产占比","decimal(10,4)"],["deposit_value","银行存款和结算备付金合计","decimal(20,4)"],["deposit_rate","银行存款和结算备付金合计占比","decimal(10,4)"],["others_value","其他资产","decimal(20,4)"],["others_rate","其他资产占比","decimal(10,4)"],["total_asset","总资产合计","decimal(20,4)"],["CDR_value","存托凭证","decimal(10,4)"],["CDR_rate","存托凭证占总值比例","decimal(10,5)"],["fund_value","基金投资","decimal(10,6)"],["fund_rate","基金投资占总值比例","decimal(10,7)"],["mm_inst_value","货币市场工具","decimal(10,8)"],["mm_inst_rate","货币市场工具占总值比例","decimal(10,9)"],["REIT_value","房地产信托","decimal(10,10)"],["REIT_rate","房地产信托占总值比例","decimal(10,13)"],["preferred_value","优先股","decimal(10,11)"],["preferred_rate","优先股占总值比例","decimal(10,14)"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_PORTFOLIO).filter(finance.FUND_PORTFOLIO.code==code).limit(n))"}
    - {"language":"python","code":"#查询深成指B基金(\"150023\")基金资产组合概况数据，传入的基金代码无需后缀\nfrom jqdatasdk import finance\nq=query(finance.FUND_PORTFOLIO.code,\n                  finance.FUND_PORTFOLIO.name,\n                  finance.FUND_PORTFOLIO.pub_date,\n                  finance.FUND_PORTFOLIO.stock_rate,\n                  finance.FUND_PORTFOLIO.fixed_income_rate,\nfinance.FUND_PORTFOLIO.total_asset).filter(finance.FUND_PORTFOLIO.code==\"150023\").order_by(finance.FUND_PORTFOLIO.pub_date.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n     code                    name    pub_date  stock_rate  fixed_income_rate  \\\n0  150023  申万菱信深证成指分级证券投资基金申万进取份额  2021-01-22       84.92                0.0   \n1  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-10-28       93.66                0.0   \n2  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-07-21       93.18                NaN   \n3  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-04-22       92.68                NaN   \n4  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-01-20       93.35                NaN   \n\n    total_asset  \n0  2.499121e+09  \n1  3.503815e+09  \n2  3.314002e+09  \n3  2.794784e+09  \n4  2.960295e+09"}
    - {"language":"python","code":"#查询开元证券投资基金(\"184688\")基金资产组合概况数据，传入的基金代码无需后缀\nfrom jqdatasdk import finance\nq=query(finance.FUND_PORTFOLIO.code,\n                  finance.FUND_PORTFOLIO.name,\n                  finance.FUND_PORTFOLIO.pub_date,\n                  finance.FUND_PORTFOLIO.stock_rate,\n                  finance.FUND_PORTFOLIO.fixed_income_rate,\nfinance.FUND_PORTFOLIO.total_asset).filter(finance.FUND_PORTFOLIO.code==\"184688\").order_by(finance.FUND_PORTFOLIO.pub_date.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n     code      name    pub_date  stock_rate  fixed_income_rate   total_asset\n0  184688  开元证券投资基金  2013-01-21       76.08              23.14  1.755376e+09\n1  184688  开元证券投资基金  2012-10-26       73.16              25.00  1.710568e+09\n2  184688  开元证券投资基金  2012-07-18       73.93              24.76  1.733814e+09\n3  184688  开元证券投资基金  2012-04-23       76.62              21.86  1.726419e+09\n4  184688  开元证券投资基金  2012-01-20       73.83              24.41  1.625162e+09"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"基金资产组合概况"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_PORTFOLIO).filter(finance.FUND_PORTFOLIO.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["基金资产组合概况"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"基金持股信息参数"}
    - {"type":"list","listType":"ul","items":["query(finance.FUND_PORTFOLIO)表示从finance.FUND_PORTFOLIO这张表中查询基金资产组合概况数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_PORTFOLIO：收录了基金资产组合概况数据，表结构和字段信息如下：","finance.FUND_PORTFOLIO.code==code：指定筛选条件，通过finance.FUND_PORTFOLIO.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"table","headers":["字段名称","中文名称","字段类型"],"rows":[["code","基金代码","varchar(12)"],["name","基金名称","varchar(80)"],["period_start","开始日期","date"],["period_end","报告期","date"],["pub_date","公告日期","date"],["report_type_id","报告类型编码","int"],["report_type","报告类型","varchar(32)"],["equity_value","权益类投资金额","decimal(20,4)"],["equity_rate","权益类投资占比","decimal(10,4)"],["stock_value","股票投资金额","decimal(20,4)"],["stock_rate","股票投资占比","decimal(10,4)"],["fixed_income_value","固定收益投资金额","decimal(20,4)"],["fixed_income_rate","固定收益投资占比","decimal(10,4)"],["precious_metal_value","贵金属投资金额","decimal(20,4)"],["precious_metal_rate","贵金属投资占比","decimal(10,4)"],["derivative_value","金融衍生品投资金额","decimal(20,4)"],["derivative_rate","金融衍生品投资占比","decimal(10,4)"],["buying_back_value","买入返售金融资产金额","decimal(20,4)"],["buying_back_rate","买入返售金融资产占比","decimal(10,4)"],["deposit_value","银行存款和结算备付金合计","decimal(20,4)"],["deposit_rate","银行存款和结算备付金合计占比","decimal(10,4)"],["others_value","其他资产","decimal(20,4)"],["others_rate","其他资产占比","decimal(10,4)"],["total_asset","总资产合计","decimal(20,4)"],["CDR_value","存托凭证","decimal(10,4)"],["CDR_rate","存托凭证占总值比例","decimal(10,5)"],["fund_value","基金投资","decimal(10,6)"],["fund_rate","基金投资占总值比例","decimal(10,7)"],["mm_inst_value","货币市场工具","decimal(10,8)"],["mm_inst_rate","货币市场工具占总值比例","decimal(10,9)"],["REIT_value","房地产信托","decimal(10,10)"],["REIT_rate","房地产信托占总值比例","decimal(10,13)"],["preferred_value","优先股","decimal(10,11)"],["preferred_rate","优先股占总值比例","decimal(10,14)"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"list","listType":"ul","items":["场内基金"]}
    - {"type":"codeblock","language":"python","content":"#查询深成指B基金(\"150023\")基金资产组合概况数据，传入的基金代码无需后缀\nfrom jqdatasdk import finance\nq=query(finance.FUND_PORTFOLIO.code,\n                  finance.FUND_PORTFOLIO.name,\n                  finance.FUND_PORTFOLIO.pub_date,\n                  finance.FUND_PORTFOLIO.stock_rate,\n                  finance.FUND_PORTFOLIO.fixed_income_rate,\nfinance.FUND_PORTFOLIO.total_asset).filter(finance.FUND_PORTFOLIO.code==\"150023\").order_by(finance.FUND_PORTFOLIO.pub_date.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n     code                    name    pub_date  stock_rate  fixed_income_rate  \\\n0  150023  申万菱信深证成指分级证券投资基金申万进取份额  2021-01-22       84.92                0.0   \n1  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-10-28       93.66                0.0   \n2  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-07-21       93.18                NaN   \n3  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-04-22       92.68                NaN   \n4  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-01-20       93.35                NaN   \n\n    total_asset  \n0  2.499121e+09  \n1  3.503815e+09  \n2  3.314002e+09  \n3  2.794784e+09  \n4  2.960295e+09"}
    - {"type":"list","listType":"ul","items":["场外基金"]}
    - {"type":"codeblock","language":"python","content":"#查询开元证券投资基金(\"184688\")基金资产组合概况数据，传入的基金代码无需后缀\nfrom jqdatasdk import finance\nq=query(finance.FUND_PORTFOLIO.code,\n                  finance.FUND_PORTFOLIO.name,\n                  finance.FUND_PORTFOLIO.pub_date,\n                  finance.FUND_PORTFOLIO.stock_rate,\n                  finance.FUND_PORTFOLIO.fixed_income_rate,\nfinance.FUND_PORTFOLIO.total_asset).filter(finance.FUND_PORTFOLIO.code==\"184688\").order_by(finance.FUND_PORTFOLIO.pub_date.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n     code      name    pub_date  stock_rate  fixed_income_rate   total_asset\n0  184688  开元证券投资基金  2013-01-21       76.08              23.14  1.755376e+09\n1  184688  开元证券投资基金  2012-10-26       73.16              25.00  1.710568e+09\n2  184688  开元证券投资基金  2012-07-18       73.93              24.76  1.733814e+09\n3  184688  开元证券投资基金  2012-04-23       76.62              21.86  1.726419e+09\n4  184688  开元证券投资基金  2012-01-20       73.83              24.41  1.625162e+09"}
  suggestedFilename: "doc_JQDatadoc_9936_overview_基金资产组合概况"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9936"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 基金资产组合概况

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9936

## 描述

描述

## 内容

#### 基金资产组合概况

- 历史范围：上市至今；更新时间：盘后24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.FUND_PORTFOLIO).filter(finance.FUND_PORTFOLIO.code==code).limit(n))
```

描述

- 基金资产组合概况

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

基金持股信息参数

- query(finance.FUND_PORTFOLIO)表示从finance.FUND_PORTFOLIO这张表中查询基金资产组合概况数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- finance.FUND_PORTFOLIO：收录了基金资产组合概况数据，表结构和字段信息如下：
- finance.FUND_PORTFOLIO.code==code：指定筛选条件，通过finance.FUND_PORTFOLIO.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

| 字段名称 | 中文名称 | 字段类型 |
| --- | --- | --- |
| code | 基金代码 | varchar(12) |
| name | 基金名称 | varchar(80) |
| period_start | 开始日期 | date |
| period_end | 报告期 | date |
| pub_date | 公告日期 | date |
| report_type_id | 报告类型编码 | int |
| report_type | 报告类型 | varchar(32) |
| equity_value | 权益类投资金额 | decimal(20,4) |
| equity_rate | 权益类投资占比 | decimal(10,4) |
| stock_value | 股票投资金额 | decimal(20,4) |
| stock_rate | 股票投资占比 | decimal(10,4) |
| fixed_income_value | 固定收益投资金额 | decimal(20,4) |
| fixed_income_rate | 固定收益投资占比 | decimal(10,4) |
| precious_metal_value | 贵金属投资金额 | decimal(20,4) |
| precious_metal_rate | 贵金属投资占比 | decimal(10,4) |
| derivative_value | 金融衍生品投资金额 | decimal(20,4) |
| derivative_rate | 金融衍生品投资占比 | decimal(10,4) |
| buying_back_value | 买入返售金融资产金额 | decimal(20,4) |
| buying_back_rate | 买入返售金融资产占比 | decimal(10,4) |
| deposit_value | 银行存款和结算备付金合计 | decimal(20,4) |
| deposit_rate | 银行存款和结算备付金合计占比 | decimal(10,4) |
| others_value | 其他资产 | decimal(20,4) |
| others_rate | 其他资产占比 | decimal(10,4) |
| total_asset | 总资产合计 | decimal(20,4) |
| CDR_value | 存托凭证 | decimal(10,4) |
| CDR_rate | 存托凭证占总值比例 | decimal(10,5) |
| fund_value | 基金投资 | decimal(10,6) |
| fund_rate | 基金投资占总值比例 | decimal(10,7) |
| mm_inst_value | 货币市场工具 | decimal(10,8) |
| mm_inst_rate | 货币市场工具占总值比例 | decimal(10,9) |
| REIT_value | 房地产信托 | decimal(10,10) |
| REIT_rate | 房地产信托占总值比例 | decimal(10,13) |
| preferred_value | 优先股 | decimal(10,11) |
| preferred_rate | 优先股占总值比例 | decimal(10,14) |

###### 示例：

```python
#查询深成指B基金("150023")基金资产组合概况数据，传入的基金代码无需后缀
from jqdatasdk import finance
q=query(finance.FUND_PORTFOLIO.code,
                  finance.FUND_PORTFOLIO.name,
                  finance.FUND_PORTFOLIO.pub_date,
                  finance.FUND_PORTFOLIO.stock_rate,
                  finance.FUND_PORTFOLIO.fixed_income_rate,
finance.FUND_PORTFOLIO.total_asset).filter(finance.FUND_PORTFOLIO.code=="150023").order_by(finance.FUND_PORTFOLIO.pub_date.desc()).limit(5)
df=finance.run_query(q)
print(df)

     code                    name    pub_date  stock_rate  fixed_income_rate  \
0  150023  申万菱信深证成指分级证券投资基金申万进取份额  2021-01-22       84.92                0.0   
1  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-10-28       93.66                0.0   
2  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-07-21       93.18                NaN   
3  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-04-22       92.68                NaN   
4  150023  申万菱信深证成指分级证券投资基金申万进取份额  2020-01-20       93.35                NaN   

    total_asset  
0  2.499121e+09  
1  3.503815e+09  
2  3.314002e+09  
3  2.794784e+09  
4  2.960295e+09
```

```python
#查询开元证券投资基金("184688")基金资产组合概况数据，传入的基金代码无需后缀
from jqdatasdk import finance
q=query(finance.FUND_PORTFOLIO.code,
                  finance.FUND_PORTFOLIO.name,
                  finance.FUND_PORTFOLIO.pub_date,
                  finance.FUND_PORTFOLIO.stock_rate,
                  finance.FUND_PORTFOLIO.fixed_income_rate,
finance.FUND_PORTFOLIO.total_asset).filter(finance.FUND_PORTFOLIO.code=="184688").order_by(finance.FUND_PORTFOLIO.pub_date.desc()).limit(5)
df=finance.run_query(q)
print(df)

     code      name    pub_date  stock_rate  fixed_income_rate   total_asset
0  184688  开元证券投资基金  2013-01-21       76.08              23.14  1.755376e+09
1  184688  开元证券投资基金  2012-10-26       73.16              25.00  1.710568e+09
2  184688  开元证券投资基金  2012-07-18       73.93              24.76  1.733814e+09
3  184688  开元证券投资基金  2012-04-23       76.62              21.86  1.726419e+09
4  184688  开元证券投资基金  2012-01-20       73.83              24.41  1.625162e+09
```
