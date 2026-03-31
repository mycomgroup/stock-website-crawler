---
id: "url-7a226e70"
type: "website"
title: "期权风险指标（查表）"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9920"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:20:08.464Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9920"
  headings:
    - {"level":3,"text":"期权风险指标（查表）","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "期权日行情参数"
  lists:
    - {"type":"ul","items":["历史范围：2019/12/2至今；更新频率：下一交易日盘前8:05更新"]}
    - {"type":"ul","items":["描述：统计各期权合约每日的风险指标，帮助用户更科学的衡量期权合约的价值变动"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(opt.OPT_RISK_INDICATOR)：表示从opt.OPT_RISK_INDICATOR这张表中查询期权风险指标数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","opt.OPT_RISK_INDICATOR：收录了期权风险指标数据，表结构和字段信息如下：","filter(opt.OPT_RISK_INDICATOR.code==code)：指定筛选条件，通过opt.OPT_RISK_INDICATOR.code==code可以指定你想要查询的合约代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["名称","类型","描述","示例","备注"],"rows":[["code","str","合约代码","10001313.XSHG；CU1901C46000.XSGE；SR903C4700.XZCE；M1707-C-2400.XDCE","合约代码使用大写字母"],["exchange_code","str","证券市场编码","XSHG",""],["date","str","交易日期","2018-10-19",""],["delta","float","DELTA","0.906","Delta=期权价格变化/期货变化"],["theta","float","THETA","-0.249","Theta＝期权价格的变化／距离到期日时间的变化"],["gamma","float","GAMMA","0.669","Gamma=delta的变化／期货价格的变化"],["vega","float","VEGA","0.138","Vega=期权价格变化/波动率的变化"],["rho","float","RHO","0.213","Rho=期权价格的变化／无风险利率的变化"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import opt\nopt.run_query(query(opt.OPT_RISK_INDICATOR).filter(opt.OPT_RISK_INDICATOR.code==code).limit(n))"}
    - {"language":"python","code":"#查询上证50ETF期权（'10001313.XSHG')最新的期权风险指标数据。\nfrom jqdatasdk import *\nq=query(opt.OPT_RISK_INDICATOR).filter(opt.OPT_RISK_INDICATOR.code=='10001313.XSHG').order_by(opt.OPT_RISK_INDICATOR.date.desc()).limit(10)\ndf=opt.run_query(q)\nprint(df)\n\n       id           code exchange_code        date  delta  theta  gamma  \\\n0  320797  10001313.XSHG          XSHG  2018-12-05  0.609 -0.488  2.875   \n1   83541  10001313.XSHG          XSHG  2018-12-04  0.638 -0.471  2.730   \n2   83540  10001313.XSHG          XSHG  2018-12-03  0.610 -0.490  2.607   \n3   83539  10001313.XSHG          XSHG  2018-11-30  0.467 -0.519  2.278   \n4   83538  10001313.XSHG          XSHG  2018-11-29  0.419 -0.484  2.266   \n5   83537  10001313.XSHG          XSHG  2018-11-28  0.447 -0.466  2.341   \n6   83536  10001313.XSHG          XSHG  2018-11-27  0.391 -0.449  2.198   \n7   83535  10001313.XSHG          XSHG  2018-11-26  0.422 -0.470  2.108   \n8   83534  10001313.XSHG          XSHG  2018-11-23  0.418 -0.468  1.917   \n9   83533  10001313.XSHG          XSHG  2018-11-22  0.497 -0.477  1.929   \n\n    vega    rho  \n0  0.228  0.083  \n1  0.229  0.091  \n2  0.239  0.090  \n3  0.263  0.078  \n4  0.261  0.072  \n5  0.270  0.080  \n6  0.264  0.072  \n7  0.275  0.080  \n8  0.287  0.087  \n9  0.302  0.108"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"期权风险指标（查表）"}
    - {"type":"list","listType":"ul","items":["历史范围：2019/12/2至今；更新频率：下一交易日盘前8:05更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import opt\nopt.run_query(query(opt.OPT_RISK_INDICATOR).filter(opt.OPT_RISK_INDICATOR.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["描述：统计各期权合约每日的风险指标，帮助用户更科学的衡量期权合约的价值变动"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"期权日行情参数"}
    - {"type":"list","listType":"ul","items":["query(opt.OPT_RISK_INDICATOR)：表示从opt.OPT_RISK_INDICATOR这张表中查询期权风险指标数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","opt.OPT_RISK_INDICATOR：收录了期权风险指标数据，表结构和字段信息如下：","filter(opt.OPT_RISK_INDICATOR.code==code)：指定筛选条件，通过opt.OPT_RISK_INDICATOR.code==code可以指定你想要查询的合约代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"table","headers":["名称","类型","描述","示例","备注"],"rows":[["code","str","合约代码","10001313.XSHG；CU1901C46000.XSGE；SR903C4700.XZCE；M1707-C-2400.XDCE","合约代码使用大写字母"],["exchange_code","str","证券市场编码","XSHG",""],["date","str","交易日期","2018-10-19",""],["delta","float","DELTA","0.906","Delta=期权价格变化/期货变化"],["theta","float","THETA","-0.249","Theta＝期权价格的变化／距离到期日时间的变化"],["gamma","float","GAMMA","0.669","Gamma=delta的变化／期货价格的变化"],["vega","float","VEGA","0.138","Vega=期权价格变化/波动率的变化"],["rho","float","RHO","0.213","Rho=期权价格的变化／无风险利率的变化"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#查询上证50ETF期权（'10001313.XSHG')最新的期权风险指标数据。\nfrom jqdatasdk import *\nq=query(opt.OPT_RISK_INDICATOR).filter(opt.OPT_RISK_INDICATOR.code=='10001313.XSHG').order_by(opt.OPT_RISK_INDICATOR.date.desc()).limit(10)\ndf=opt.run_query(q)\nprint(df)\n\n       id           code exchange_code        date  delta  theta  gamma  \\\n0  320797  10001313.XSHG          XSHG  2018-12-05  0.609 -0.488  2.875   \n1   83541  10001313.XSHG          XSHG  2018-12-04  0.638 -0.471  2.730   \n2   83540  10001313.XSHG          XSHG  2018-12-03  0.610 -0.490  2.607   \n3   83539  10001313.XSHG          XSHG  2018-11-30  0.467 -0.519  2.278   \n4   83538  10001313.XSHG          XSHG  2018-11-29  0.419 -0.484  2.266   \n5   83537  10001313.XSHG          XSHG  2018-11-28  0.447 -0.466  2.341   \n6   83536  10001313.XSHG          XSHG  2018-11-27  0.391 -0.449  2.198   \n7   83535  10001313.XSHG          XSHG  2018-11-26  0.422 -0.470  2.108   \n8   83534  10001313.XSHG          XSHG  2018-11-23  0.418 -0.468  1.917   \n9   83533  10001313.XSHG          XSHG  2018-11-22  0.497 -0.477  1.929   \n\n    vega    rho  \n0  0.228  0.083  \n1  0.229  0.091  \n2  0.239  0.090  \n3  0.263  0.078  \n4  0.261  0.072  \n5  0.270  0.080  \n6  0.264  0.072  \n7  0.275  0.080  \n8  0.287  0.087  \n9  0.302  0.108"}
  suggestedFilename: "doc_JQDatadoc_9920_overview_期权风险指标（查表）"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9920"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 期权风险指标（查表）

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9920

## 描述

描述

## 内容

#### 期权风险指标（查表）

- 历史范围：2019/12/2至今；更新频率：下一交易日盘前8:05更新

```python
from jqdatasdk import opt
opt.run_query(query(opt.OPT_RISK_INDICATOR).filter(opt.OPT_RISK_INDICATOR.code==code).limit(n))
```

描述

- 描述：统计各期权合约每日的风险指标，帮助用户更科学的衡量期权合约的价值变动

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

期权日行情参数

- query(opt.OPT_RISK_INDICATOR)：表示从opt.OPT_RISK_INDICATOR这张表中查询期权风险指标数据，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- opt.OPT_RISK_INDICATOR：收录了期权风险指标数据，表结构和字段信息如下：
- filter(opt.OPT_RISK_INDICATOR.code==code)：指定筛选条件，通过opt.OPT_RISK_INDICATOR.code==code可以指定你想要查询的合约代码；除此之外，还可以对表中其他字段指定筛选条件；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

| 名称 | 类型 | 描述 | 示例 | 备注 |
| --- | --- | --- | --- | --- |
| code | str | 合约代码 | 10001313.XSHG；CU1901C46000.XSGE；SR903C4700.XZCE；M1707-C-2400.XDCE | 合约代码使用大写字母 |
| exchange_code | str | 证券市场编码 | XSHG |  |
| date | str | 交易日期 | 2018-10-19 |  |
| delta | float | DELTA | 0.906 | Delta=期权价格变化/期货变化 |
| theta | float | THETA | -0.249 | Theta＝期权价格的变化／距离到期日时间的变化 |
| gamma | float | GAMMA | 0.669 | Gamma=delta的变化／期货价格的变化 |
| vega | float | VEGA | 0.138 | Vega=期权价格变化/波动率的变化 |
| rho | float | RHO | 0.213 | Rho=期权价格的变化／无风险利率的变化 |

###### 示例：

```python
#查询上证50ETF期权（'10001313.XSHG')最新的期权风险指标数据。
from jqdatasdk import *
q=query(opt.OPT_RISK_INDICATOR).filter(opt.OPT_RISK_INDICATOR.code=='10001313.XSHG').order_by(opt.OPT_RISK_INDICATOR.date.desc()).limit(10)
df=opt.run_query(q)
print(df)

       id           code exchange_code        date  delta  theta  gamma  \
0  320797  10001313.XSHG          XSHG  2018-12-05  0.609 -0.488  2.875   
1   83541  10001313.XSHG          XSHG  2018-12-04  0.638 -0.471  2.730   
2   83540  10001313.XSHG          XSHG  2018-12-03  0.610 -0.490  2.607   
3   83539  10001313.XSHG          XSHG  2018-11-30  0.467 -0.519  2.278   
4   83538  10001313.XSHG          XSHG  2018-11-29  0.419 -0.484  2.266   
5   83537  10001313.XSHG          XSHG  2018-11-28  0.447 -0.466  2.341   
6   83536  10001313.XSHG          XSHG  2018-11-27  0.391 -0.449  2.198   
7   83535  10001313.XSHG          XSHG  2018-11-26  0.422 -0.470  2.108   
8   83534  10001313.XSHG          XSHG  2018-11-23  0.418 -0.468  1.917   
9   83533  10001313.XSHG          XSHG  2018-11-22  0.497 -0.477  1.929   

    vega    rho  
0  0.228  0.083  
1  0.229  0.091  
2  0.239  0.090  
3  0.263  0.078  
4  0.261  0.072  
5  0.270  0.080  
6  0.264  0.072  
7  0.275  0.080  
8  0.287  0.087  
9  0.302  0.108
```
