---
id: "url-7a226e94"
type: "website"
title: "基金持有的债券信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9935"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:20:44.059Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9935"
  headings:
    - {"level":3,"text":"基金持有的债券信息","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "基金持有的债券信息参数"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"ul","items":["记录公募基金按季度公布的债券组合，为债券投资者提供一些参照"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.FUND_PORTFOLIO_BOND)：表示从finance.FUND_PORTFOLIO_BOND这张表中查询基金持仓债券组合数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_PORTFOLIO_BOND：收录了基金持仓债券组合数据，表结构和字段信息如下：","filter(finance.FUND_PORTFOLIO_BOND.code==code)：指定筛选条件，通过finance.FUND_PORTFOLIO_BOND.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"ul","items":["场内基金"]}
    - {"type":"ul","items":["场外基金"]}
  tables:
    - {"caption":"","headers":["字段名称","中文名称","字段类型"],"rows":[["code","基金代码","varchar(12)"],["period_start","开始日期","date"],["period_end","报告期","date"],["pub_date","公告日期","date"],["report_type_id","报告类型编码","int"],["report_type","报告类型","varchar(32)"],["rank","持仓排名","int"],["symbol","债券代码","varchar(32)"],["name","债券名称","varchar(100)"],["shares","持有债券数量","decimal(20,4)"],["market_cap","持有债券的市值","decimal(20,4)"],["proportion","占净值比例","decimal(10,4)"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code==code).limit(n))"}
    - {"language":"python","code":"#查询银华锐进基金(\"150019\")基金持有的债券组合数据\ndf=finance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code=='150019').order_by(finance.FUND_PORTFOLIO_BOND.pub_date.desc()).limit(5))\nprint(df)\n\n       id    code period_start  period_end    pub_date  report_type_id  \\\n0  727440  150019   2019-04-01  2019-06-30  2019-07-19          403002   \n1  697207  150019   2019-01-01  2019-03-31  2019-04-18          403001   \n2  697208  150019   2019-01-01  2019-03-31  2019-04-18          403001   \n3  697209  150019   2019-01-01  2019-03-31  2019-04-18          403001   \n\n  report_type  rank  symbol    name    shares  market_cap  proportion  \n0        第二季度     1  108603  国开1804   90000.0   9005400.0        0.14  \n1        第一季度     1  018005  国开1701  380000.0  38003800.0        0.57  \n2        第一季度     2  108603  国开1804   80000.0   8040000.0        0.12  \n3        第一季度     3  019537  16国债09   66810.0   6681000.0        0.10"}
    - {"language":"python","code":"#查询中海环保新能源主题灵活配置混合型证券投资基金(\"398051\")基金持有的债券组合数据\ndf=finance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code=='398051').order_by(finance.FUND_PORTFOLIO_BOND.pub_date.desc()).limit(5))\nprint(df)\n\n       id    code period_start  period_end    pub_date  report_type_id  \\\n0  929557  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n1  929556  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n2  929555  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n3  929554  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n4  929558  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n\n  report_type  rank  symbol    name    shares   market_cap  proportion  \n0        第四季度     4  113040    星宇转债  110000.0  15744300.00        1.14  \n1        第四季度     3  019640  20国债10  235200.0  23489424.00        1.69  \n2        第四季度     2  123070    鹏辉转债  269372.0  37356508.96        2.70  \n3        第四季度     1  019645  20国债15  380000.0  38136800.00        2.75  \n4        第四季度     5  113586    上机转债   37130.0  15395583.20        1.11"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"基金持有的债券信息"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：盘后24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["记录公募基金按季度公布的债券组合，为债券投资者提供一些参照"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"基金持有的债券信息参数"}
    - {"type":"list","listType":"ul","items":["query(finance.FUND_PORTFOLIO_BOND)：表示从finance.FUND_PORTFOLIO_BOND这张表中查询基金持仓债券组合数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_PORTFOLIO_BOND：收录了基金持仓债券组合数据，表结构和字段信息如下：","filter(finance.FUND_PORTFOLIO_BOND.code==code)：指定筛选条件，通过finance.FUND_PORTFOLIO_BOND.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"table","headers":["字段名称","中文名称","字段类型"],"rows":[["code","基金代码","varchar(12)"],["period_start","开始日期","date"],["period_end","报告期","date"],["pub_date","公告日期","date"],["report_type_id","报告类型编码","int"],["report_type","报告类型","varchar(32)"],["rank","持仓排名","int"],["symbol","债券代码","varchar(32)"],["name","债券名称","varchar(100)"],["shares","持有债券数量","decimal(20,4)"],["market_cap","持有债券的市值","decimal(20,4)"],["proportion","占净值比例","decimal(10,4)"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"list","listType":"ul","items":["场内基金"]}
    - {"type":"codeblock","language":"python","content":"#查询银华锐进基金(\"150019\")基金持有的债券组合数据\ndf=finance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code=='150019').order_by(finance.FUND_PORTFOLIO_BOND.pub_date.desc()).limit(5))\nprint(df)\n\n       id    code period_start  period_end    pub_date  report_type_id  \\\n0  727440  150019   2019-04-01  2019-06-30  2019-07-19          403002   \n1  697207  150019   2019-01-01  2019-03-31  2019-04-18          403001   \n2  697208  150019   2019-01-01  2019-03-31  2019-04-18          403001   \n3  697209  150019   2019-01-01  2019-03-31  2019-04-18          403001   \n\n  report_type  rank  symbol    name    shares  market_cap  proportion  \n0        第二季度     1  108603  国开1804   90000.0   9005400.0        0.14  \n1        第一季度     1  018005  国开1701  380000.0  38003800.0        0.57  \n2        第一季度     2  108603  国开1804   80000.0   8040000.0        0.12  \n3        第一季度     3  019537  16国债09   66810.0   6681000.0        0.10"}
    - {"type":"list","listType":"ul","items":["场外基金"]}
    - {"type":"codeblock","language":"python","content":"#查询中海环保新能源主题灵活配置混合型证券投资基金(\"398051\")基金持有的债券组合数据\ndf=finance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code=='398051').order_by(finance.FUND_PORTFOLIO_BOND.pub_date.desc()).limit(5))\nprint(df)\n\n       id    code period_start  period_end    pub_date  report_type_id  \\\n0  929557  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n1  929556  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n2  929555  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n3  929554  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n4  929558  398051   2020-10-01  2020-12-31  2021-01-22          403004   \n\n  report_type  rank  symbol    name    shares   market_cap  proportion  \n0        第四季度     4  113040    星宇转债  110000.0  15744300.00        1.14  \n1        第四季度     3  019640  20国债10  235200.0  23489424.00        1.69  \n2        第四季度     2  123070    鹏辉转债  269372.0  37356508.96        2.70  \n3        第四季度     1  019645  20国债15  380000.0  38136800.00        2.75  \n4        第四季度     5  113586    上机转债   37130.0  15395583.20        1.11"}
  suggestedFilename: "doc_JQDatadoc_9935_overview_基金持有的债券信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9935"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 基金持有的债券信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9935

## 描述

描述

## 内容

#### 基金持有的债券信息

- 历史范围：上市至今；更新时间：盘后24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code==code).limit(n))
```

描述

- 记录公募基金按季度公布的债券组合，为债券投资者提供一些参照

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

基金持有的债券信息参数

- query(finance.FUND_PORTFOLIO_BOND)：表示从finance.FUND_PORTFOLIO_BOND这张表中查询基金持仓债券组合数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- finance.FUND_PORTFOLIO_BOND：收录了基金持仓债券组合数据，表结构和字段信息如下：
- filter(finance.FUND_PORTFOLIO_BOND.code==code)：指定筛选条件，通过finance.FUND_PORTFOLIO_BOND.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
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
| symbol | 债券代码 | varchar(32) |
| name | 债券名称 | varchar(100) |
| shares | 持有债券数量 | decimal(20,4) |
| market_cap | 持有债券的市值 | decimal(20,4) |
| proportion | 占净值比例 | decimal(10,4) |

###### 示例：

```python
#查询银华锐进基金("150019")基金持有的债券组合数据
df=finance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code=='150019').order_by(finance.FUND_PORTFOLIO_BOND.pub_date.desc()).limit(5))
print(df)

       id    code period_start  period_end    pub_date  report_type_id  \
0  727440  150019   2019-04-01  2019-06-30  2019-07-19          403002   
1  697207  150019   2019-01-01  2019-03-31  2019-04-18          403001   
2  697208  150019   2019-01-01  2019-03-31  2019-04-18          403001   
3  697209  150019   2019-01-01  2019-03-31  2019-04-18          403001   

  report_type  rank  symbol    name    shares  market_cap  proportion  
0        第二季度     1  108603  国开1804   90000.0   9005400.0        0.14  
1        第一季度     1  018005  国开1701  380000.0  38003800.0        0.57  
2        第一季度     2  108603  国开1804   80000.0   8040000.0        0.12  
3        第一季度     3  019537  16国债09   66810.0   6681000.0        0.10
```

```python
#查询中海环保新能源主题灵活配置混合型证券投资基金("398051")基金持有的债券组合数据
df=finance.run_query(query(finance.FUND_PORTFOLIO_BOND).filter(finance.FUND_PORTFOLIO_BOND.code=='398051').order_by(finance.FUND_PORTFOLIO_BOND.pub_date.desc()).limit(5))
print(df)

       id    code period_start  period_end    pub_date  report_type_id  \
0  929557  398051   2020-10-01  2020-12-31  2021-01-22          403004   
1  929556  398051   2020-10-01  2020-12-31  2021-01-22          403004   
2  929555  398051   2020-10-01  2020-12-31  2021-01-22          403004   
3  929554  398051   2020-10-01  2020-12-31  2021-01-22          403004   
4  929558  398051   2020-10-01  2020-12-31  2021-01-22          403004   

  report_type  rank  symbol    name    shares   market_cap  proportion  
0        第四季度     4  113040    星宇转债  110000.0  15744300.00        1.14  
1        第四季度     3  019640  20国债10  235200.0  23489424.00        1.69  
2        第四季度     2  123070    鹏辉转债  269372.0  37356508.96        2.70  
3        第四季度     1  019645  20国债15  380000.0  38136800.00        2.75  
4        第四季度     5  113586    上机转债   37130.0  15395583.20        1.11
```
