---
id: "url-7a226e93"
type: "website"
title: "基金持股信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9934"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:20:40.123Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9934"
  headings:
    - {"level":3,"text":"基金持股信息","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "基金持股信息参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"ul","items":["统计基金季度报表、半年度报表和年度报表披露的股票持仓数据"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.FUND_PORTFOLIO_STOCK)：表示从finance.FUND_PORTFOLIO_STOCK这张表中查询基金持仓股票组合数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_PORTFOLIO_STOCK：收录了基金持仓股票组合数据，表结构和字段信息如下：","filter(finance.FUND_PORTFOLIO_STOCK.code==code)：指定筛选条件，通过finance.FUND_PORTFOLIO_STOCK.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型"],"rows":[["code","基金代码","varchar(12)"],["period_start","开始日期","date"],["period_end","报告期","date"],["pub_date","公告日期","date"],["report_type_id","报告类型编码","int"],["report_type","报告类型","varchar(32)"],["rank","持仓排名","int"],["symbol","股票代码","varchar(32)"],["name","股票名称","varchar(100)"],["shares","持有股票","decimal(20,4)"],["market_cap","持有股票的市值","decimal(20,4)"],["proportion","占净值比例","decimal(10,4)"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code==code).limit(n))"}
    - {"language":"python","code":"#查询合润A基金(\"150016\")最近一个季度的基金持仓股票组合前5只股票\nq=query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code==\"150016\").order_by(finance.FUND_PORTFOLIO_STOCK.pub_date.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n         id    code period_start  period_end    pub_date  report_type_id  \\\n0  16178727  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n1  16178726  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n2  16178725  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n3  16178724  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n4  16178723  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n\n  report_type  rank  symbol  name      shares    market_cap  proportion  \n0        第四季度    10  601012  隆基股份   6707249.0  5.835850e+08        2.83  \n1        第四季度     9  688099  晶晨股份   7575165.0  5.887965e+08        2.86  \n2        第四季度     8  000895  双汇发展  13913806.0  6.439926e+08        3.13  \n3        第四季度     7  300413  芒果超媒   9394546.0  6.811046e+08        3.31  \n4        第四季度     6  002594   比亚迪   3581370.0  6.958602e+08        3.38"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"基金持股信息"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["统计基金季度报表、半年度报表和年度报表披露的股票持仓数据"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"基金持股信息参数"}
    - {"type":"list","listType":"ul","items":["query(finance.FUND_PORTFOLIO_STOCK)：表示从finance.FUND_PORTFOLIO_STOCK这张表中查询基金持仓股票组合数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_PORTFOLIO_STOCK：收录了基金持仓股票组合数据，表结构和字段信息如下：","filter(finance.FUND_PORTFOLIO_STOCK.code==code)：指定筛选条件，通过finance.FUND_PORTFOLIO_STOCK.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"table","headers":["字段名称","中文名称","字段类型"],"rows":[["code","基金代码","varchar(12)"],["period_start","开始日期","date"],["period_end","报告期","date"],["pub_date","公告日期","date"],["report_type_id","报告类型编码","int"],["report_type","报告类型","varchar(32)"],["rank","持仓排名","int"],["symbol","股票代码","varchar(32)"],["name","股票名称","varchar(100)"],["shares","持有股票","decimal(20,4)"],["market_cap","持有股票的市值","decimal(20,4)"],["proportion","占净值比例","decimal(10,4)"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#查询合润A基金(\"150016\")最近一个季度的基金持仓股票组合前5只股票\nq=query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code==\"150016\").order_by(finance.FUND_PORTFOLIO_STOCK.pub_date.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n         id    code period_start  period_end    pub_date  report_type_id  \\\n0  16178727  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n1  16178726  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n2  16178725  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n3  16178724  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n4  16178723  150016   2020-10-01  2020-12-31  2021-01-22          403004   \n\n  report_type  rank  symbol  name      shares    market_cap  proportion  \n0        第四季度    10  601012  隆基股份   6707249.0  5.835850e+08        2.83  \n1        第四季度     9  688099  晶晨股份   7575165.0  5.887965e+08        2.86  \n2        第四季度     8  000895  双汇发展  13913806.0  6.439926e+08        3.13  \n3        第四季度     7  300413  芒果超媒   9394546.0  6.811046e+08        3.31  \n4        第四季度     6  002594   比亚迪   3581370.0  6.958602e+08        3.38"}
  suggestedFilename: "doc_JQDatadoc_9934_overview_基金持股信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9934"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 基金持股信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9934

## 描述

描述

## 内容

#### 基金持股信息

- 历史范围：上市至今；更新时间：盘后24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code==code).limit(n))
```

描述

- 统计基金季度报表、半年度报表和年度报表披露的股票持仓数据

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

基金持股信息参数

- query(finance.FUND_PORTFOLIO_STOCK)：表示从finance.FUND_PORTFOLIO_STOCK这张表中查询基金持仓股票组合数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- finance.FUND_PORTFOLIO_STOCK：收录了基金持仓股票组合数据，表结构和字段信息如下：
- filter(finance.FUND_PORTFOLIO_STOCK.code==code)：指定筛选条件，通过finance.FUND_PORTFOLIO_STOCK.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

| 字段名称 | 中文名称 | 字段类型 |
| --- | --- | --- |
| code | 基金代码 | varchar(12) |
| period_start | 开始日期 | date |
| period_end | 报告期 | date |
| pub_date | 公告日期 | date |
| report_type_id | 报告类型编码 | int |
| report_type | 报告类型 | varchar(32) |
| rank | 持仓排名 | int |
| symbol | 股票代码 | varchar(32) |
| name | 股票名称 | varchar(100) |
| shares | 持有股票 | decimal(20,4) |
| market_cap | 持有股票的市值 | decimal(20,4) |
| proportion | 占净值比例 | decimal(10,4) |

###### 示例：

```python
#查询合润A基金("150016")最近一个季度的基金持仓股票组合前5只股票
q=query(finance.FUND_PORTFOLIO_STOCK).filter(finance.FUND_PORTFOLIO_STOCK.code=="150016").order_by(finance.FUND_PORTFOLIO_STOCK.pub_date.desc()).limit(5)
df=finance.run_query(q)
print(df)

         id    code period_start  period_end    pub_date  report_type_id  \
0  16178727  150016   2020-10-01  2020-12-31  2021-01-22          403004   
1  16178726  150016   2020-10-01  2020-12-31  2021-01-22          403004   
2  16178725  150016   2020-10-01  2020-12-31  2021-01-22          403004   
3  16178724  150016   2020-10-01  2020-12-31  2021-01-22          403004   
4  16178723  150016   2020-10-01  2020-12-31  2021-01-22          403004   

  report_type  rank  symbol  name      shares    market_cap  proportion  
0        第四季度    10  601012  隆基股份   6707249.0  5.835850e+08        2.83  
1        第四季度     9  688099  晶晨股份   7575165.0  5.887965e+08        2.86  
2        第四季度     8  000895  双汇发展  13913806.0  6.439926e+08        3.13  
3        第四季度     7  300413  芒果超媒   9394546.0  6.811046e+08        3.31  
4        第四季度     6  002594   比亚迪   3581370.0  6.958602e+08        3.38
```
