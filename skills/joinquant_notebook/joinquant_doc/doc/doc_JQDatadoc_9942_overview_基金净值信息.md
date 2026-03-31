---
id: "url-7a226eb0"
type: "website"
title: "基金净值信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9942"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:21:03.767Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9942"
  headings:
    - {"level":3,"text":"基金净值信息","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "基金净值信息"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：盘前09:00更新"]}
    - {"type":"ul","items":["基金净值信息"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(finance.FUND_NET_VALUE)表示从finance.FUND_NET_VALUE这张表中查询基金净值数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_NET_VALUE：收录了基金净值数据，表结构和字段信息如下：","filter(finance.FUND_NET_VALUE.code==code)：指定筛选条件，通过finance.FUND_NET_VALUE.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"ul","items":["场内基金"]}
    - {"type":"ul","items":["场外基金"]}
  tables:
    - {"caption":"","headers":["字段","名称","类型","注释"],"rows":[["code","基金代码","varchar(12)",""],["day","交易日","date",""],["net_value","单位净值","decimal(20,6)","基金单位净值=（基金资产总值－基金负债）÷ 基金总份额"],["sum_value","累计净值","decimal(20,6)","累计单位净值＝单位净值＋成立以来每份累计分红派息的金额"],["factor","复权因子","decimal(20,6)","交易日最近一次分红拆分送股的复权因子"],["acc_factor","累计复权因子","decimal(20,6)","基金从上市至今累计分红拆分送股的复权因子"],["refactor_net_value","累计复权净值","decimal(20,6)","复权单位净值＝单计净值＋成立以来每份累计分红派息的金额（1+涨跌幅）"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code).limit(n))"}
    - {"language":"python","code":"#查询瑞和小康(\"150008)基金净值数据，传入的基金代码无需添加后缀\nfrom jqdatasdk import finance\nq=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==\"150008\").order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n         id    code         day  net_value  sum_value  factor  acc_factor  \\\n0  23506832  150008  2020-08-27      1.227      1.613     1.0    1.314668   \n1  23506831  150008  2020-08-26      1.228      1.614     1.0    1.314668   \n2  23506830  150008  2020-08-25      1.234      1.622     1.0    1.314668   \n3  23425100  150008  2020-08-24      1.234      1.622     1.0    1.314668   \n4  23414948  150008  2020-08-21      1.229      1.616     1.0    1.314668   \n\n   refactor_net_value  \n0            1.613098  \n1            1.614412  \n2            1.622300  \n3            1.622300  \n4            1.615727"}
    - {"language":"python","code":"#查询华夏成长证券投资基金(\"000001\")基金净值数据，传入的基金代码无需添加后缀\nq=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==\"000001\").order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n         id    code         day  net_value  sum_value  factor  acc_factor  \\\n0  27902258  000001  2021-03-05      1.284      3.795     1.0    6.062503   \n1  27897919  000001  2021-03-04      1.281      3.792     1.0    6.062503   \n2  27884693  000001  2021-03-03      1.330      3.841     1.0    6.062503   \n3  27871106  000001  2021-03-02      1.315      3.826     1.0    6.062503   \n4  27864300  000001  2021-03-01      1.336      3.847     1.0    6.062503   \n\n   refactor_net_value  \n0            7.784254  \n1            7.766066  \n2            8.063129  \n3            7.972191  \n4            8.099504"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"基金净值信息"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：盘前09:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["基金净值信息"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"基金净值信息"}
    - {"type":"list","listType":"ul","items":["query(finance.FUND_NET_VALUE)表示从finance.FUND_NET_VALUE这张表中查询基金净值数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","finance.FUND_NET_VALUE：收录了基金净值数据，表结构和字段信息如下：","filter(finance.FUND_NET_VALUE.code==code)：指定筛选条件，通过finance.FUND_NET_VALUE.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"table","headers":["字段","名称","类型","注释"],"rows":[["code","基金代码","varchar(12)",""],["day","交易日","date",""],["net_value","单位净值","decimal(20,6)","基金单位净值=（基金资产总值－基金负债）÷ 基金总份额"],["sum_value","累计净值","decimal(20,6)","累计单位净值＝单位净值＋成立以来每份累计分红派息的金额"],["factor","复权因子","decimal(20,6)","交易日最近一次分红拆分送股的复权因子"],["acc_factor","累计复权因子","decimal(20,6)","基金从上市至今累计分红拆分送股的复权因子"],["refactor_net_value","累计复权净值","decimal(20,6)","复权单位净值＝单计净值＋成立以来每份累计分红派息的金额（1+涨跌幅）"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"list","listType":"ul","items":["场内基金"]}
    - {"type":"codeblock","language":"python","content":"#查询瑞和小康(\"150008)基金净值数据，传入的基金代码无需添加后缀\nfrom jqdatasdk import finance\nq=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==\"150008\").order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n         id    code         day  net_value  sum_value  factor  acc_factor  \\\n0  23506832  150008  2020-08-27      1.227      1.613     1.0    1.314668   \n1  23506831  150008  2020-08-26      1.228      1.614     1.0    1.314668   \n2  23506830  150008  2020-08-25      1.234      1.622     1.0    1.314668   \n3  23425100  150008  2020-08-24      1.234      1.622     1.0    1.314668   \n4  23414948  150008  2020-08-21      1.229      1.616     1.0    1.314668   \n\n   refactor_net_value  \n0            1.613098  \n1            1.614412  \n2            1.622300  \n3            1.622300  \n4            1.615727"}
    - {"type":"list","listType":"ul","items":["场外基金"]}
    - {"type":"codeblock","language":"python","content":"#查询华夏成长证券投资基金(\"000001\")基金净值数据，传入的基金代码无需添加后缀\nq=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==\"000001\").order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)\ndf=finance.run_query(q)\nprint(df)\n\n         id    code         day  net_value  sum_value  factor  acc_factor  \\\n0  27902258  000001  2021-03-05      1.284      3.795     1.0    6.062503   \n1  27897919  000001  2021-03-04      1.281      3.792     1.0    6.062503   \n2  27884693  000001  2021-03-03      1.330      3.841     1.0    6.062503   \n3  27871106  000001  2021-03-02      1.315      3.826     1.0    6.062503   \n4  27864300  000001  2021-03-01      1.336      3.847     1.0    6.062503   \n\n   refactor_net_value  \n0            7.784254  \n1            7.766066  \n2            8.063129  \n3            7.972191  \n4            8.099504"}
  suggestedFilename: "doc_JQDatadoc_9942_overview_基金净值信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9942"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 基金净值信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9942

## 描述

描述

## 内容

#### 基金净值信息

- 历史范围：上市至今；更新时间：盘前09:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code).limit(n))
```

描述

- 基金净值信息

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

基金净值信息

- query(finance.FUND_NET_VALUE)表示从finance.FUND_NET_VALUE这张表中查询基金净值数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- finance.FUND_NET_VALUE：收录了基金净值数据，表结构和字段信息如下：
- filter(finance.FUND_NET_VALUE.code==code)：指定筛选条件，通过finance.FUND_NET_VALUE.code==code可以指定你想要查询的基金代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

| 字段 | 名称 | 类型 | 注释 |
| --- | --- | --- | --- |
| code | 基金代码 | varchar(12) |  |
| day | 交易日 | date |  |
| net_value | 单位净值 | decimal(20,6) | 基金单位净值=（基金资产总值－基金负债）÷ 基金总份额 |
| sum_value | 累计净值 | decimal(20,6) | 累计单位净值＝单位净值＋成立以来每份累计分红派息的金额 |
| factor | 复权因子 | decimal(20,6) | 交易日最近一次分红拆分送股的复权因子 |
| acc_factor | 累计复权因子 | decimal(20,6) | 基金从上市至今累计分红拆分送股的复权因子 |
| refactor_net_value | 累计复权净值 | decimal(20,6) | 复权单位净值＝单计净值＋成立以来每份累计分红派息的金额（1+涨跌幅） |

###### 示例：

```python
#查询瑞和小康("150008)基金净值数据，传入的基金代码无需添加后缀
from jqdatasdk import finance
q=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code=="150008").order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)
df=finance.run_query(q)
print(df)
         id    code         day  net_value  sum_value  factor  acc_factor  \
0  23506832  150008  2020-08-27      1.227      1.613     1.0    1.314668   
1  23506831  150008  2020-08-26      1.228      1.614     1.0    1.314668   
2  23506830  150008  2020-08-25      1.234      1.622     1.0    1.314668   
3  23425100  150008  2020-08-24      1.234      1.622     1.0    1.314668   
4  23414948  150008  2020-08-21      1.229      1.616     1.0    1.314668   

   refactor_net_value  
0            1.613098  
1            1.614412  
2            1.622300  
3            1.622300  
4            1.615727
```

```python
#查询华夏成长证券投资基金("000001")基金净值数据，传入的基金代码无需添加后缀
q=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code=="000001").order_by(finance.FUND_NET_VALUE.day.desc()).limit(5)
df=finance.run_query(q)
print(df)

         id    code         day  net_value  sum_value  factor  acc_factor  \
0  27902258  000001  2021-03-05      1.284      3.795     1.0    6.062503   
1  27897919  000001  2021-03-04      1.281      3.792     1.0    6.062503   
2  27884693  000001  2021-03-03      1.330      3.841     1.0    6.062503   
3  27871106  000001  2021-03-02      1.315      3.826     1.0    6.062503   
4  27864300  000001  2021-03-01      1.336      3.847     1.0    6.062503   

   refactor_net_value  
0            7.784254  
1            7.766066  
2            8.063129  
3            7.972191  
4            8.099504
```
