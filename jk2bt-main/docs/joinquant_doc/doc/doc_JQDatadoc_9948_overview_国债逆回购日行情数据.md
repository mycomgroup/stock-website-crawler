---
id: "url-7a226eb6"
type: "website"
title: "国债逆回购日行情数据"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9948"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:21:27.406Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9948"
  headings:
    - {"level":3,"text":"国债逆回购日行情数据","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "国债逆回购日行情参数"
    - "示例"
  lists:
    - {"type":"ul","items":["历史范围：上市至今；更新时间：每日19：00、22:00更新"]}
    - {"type":"ul","items":["获取国债逆回购日行情数据"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"ul","items":["query(bond.REPO_DAILY_PRICE)：表示从bond.REPO_DAILY_PRICE这张表中查询国债逆回购日行情数据，其中bond是库名，REPO_DAILY_PRICE是表名。bond库中的表都可以使用run_query方法调用,在查询表数据时还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2，多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","bond.REPO_DAILY_PRICE：获取国债逆回购日行情数据，表结构和字段信息如下：","filter(bond.REPO_DAILY_PRICE.code==code)：指定筛选条件，通过bond.REPO_DAILY_PRICE.code == '131801' 可以指定债券代码来获取国债逆回购日行情数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
  tables:
    - {"caption":"","headers":["名称","类型","描述"],"rows":[["date","date","交易日期"],["code","varchar(12)","回购代码，如 '204001.XSHG'"],["name","varchar(20)","回购简称，如 'GC001'"],["exchange_code","varchar(12)","证券市场编码。XSHG-上海证券交易所；XSHE-深圳证券交易所"],["pre_close","decimal(10,4)","前收盘利率(%)"],["open","decimal(10,4)","开盘利率(%)"],["high","decimal(10,4)","最高利率(%)"],["low","decimal(10,4)","最低利率(%)"],["close","decimal(10,4)","收盘利率(%)"],["volume","bigint","成交量（手）"],["money","decimal（20,2）","成交额（元）"],["deal_number","int","成交笔数（笔）"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import *\ndf=bond.run_query(query(bond.REPO_DAILY_PRICE).limit(n))"}
    - {"language":"python","code":"from jqdatasdk import *\ndf=bond.run_query(query(bond.REPO_DAILY_PRICE))\nprint(df.sort_values(by='deal_number',ascending=False)[:5])\n\n        id        date         code   name exchange_code  pre_close  open  \\\n2842  2843  2018-04-24  204001.XSHG  GC001          XSHG       8.87   9.5   \n2709  2710  2017-10-09  204001.XSHG  GC001          XSHG      16.63   5.0   \n2769  2770  2018-01-02  204001.XSHG  GC001          XSHG      14.53   3.9   \n2843  2844  2018-04-25  204001.XSHG  GC001          XSHG       8.93   6.0   \n2767  2768  2017-12-28  204001.XSHG  GC001          XSHG      12.57  13.0   \n\n       high     low   close     volume         money  deal_number  \n2842  12.20   6.500   8.930  915840200  9.158402e+11     728989.0  \n2709  12.00   5.000   8.745  961308900  9.613089e+11     723141.0  \n2769  10.10   3.900   6.010  828761600  8.287616e+11     703459.0  \n2843  10.01   5.555   8.795  875500800  8.755008e+11     696009.0  \n2767  24.00  13.000  17.695  703348000  7.033480e+11     669847.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"国债逆回购日行情数据"}
    - {"type":"list","listType":"ul","items":["历史范围：上市至今；更新时间：每日19：00、22:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\ndf=bond.run_query(query(bond.REPO_DAILY_PRICE).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取国债逆回购日行情数据"]}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"paragraph","content":"国债逆回购日行情参数"}
    - {"type":"list","listType":"ul","items":["query(bond.REPO_DAILY_PRICE)：表示从bond.REPO_DAILY_PRICE这张表中查询国债逆回购日行情数据，其中bond是库名，REPO_DAILY_PRICE是表名。bond库中的表都可以使用run_query方法调用,在查询表数据时还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2，多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]","bond.REPO_DAILY_PRICE：获取国债逆回购日行情数据，表结构和字段信息如下：","filter(bond.REPO_DAILY_PRICE.code==code)：指定筛选条件，通过bond.REPO_DAILY_PRICE.code == '131801' 可以指定债券代码来获取国债逆回购日行情数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"table","headers":["名称","类型","描述"],"rows":[["date","date","交易日期"],["code","varchar(12)","回购代码，如 '204001.XSHG'"],["name","varchar(20)","回购简称，如 'GC001'"],["exchange_code","varchar(12)","证券市场编码。XSHG-上海证券交易所；XSHE-深圳证券交易所"],["pre_close","decimal(10,4)","前收盘利率(%)"],["open","decimal(10,4)","开盘利率(%)"],["high","decimal(10,4)","最高利率(%)"],["low","decimal(10,4)","最低利率(%)"],["close","decimal(10,4)","收盘利率(%)"],["volume","bigint","成交量（手）"],["money","decimal（20,2）","成交额（元）"],["deal_number","int","成交笔数（笔）"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\ndf=bond.run_query(query(bond.REPO_DAILY_PRICE))\nprint(df.sort_values(by='deal_number',ascending=False)[:5])\n\n        id        date         code   name exchange_code  pre_close  open  \\\n2842  2843  2018-04-24  204001.XSHG  GC001          XSHG       8.87   9.5   \n2709  2710  2017-10-09  204001.XSHG  GC001          XSHG      16.63   5.0   \n2769  2770  2018-01-02  204001.XSHG  GC001          XSHG      14.53   3.9   \n2843  2844  2018-04-25  204001.XSHG  GC001          XSHG       8.93   6.0   \n2767  2768  2017-12-28  204001.XSHG  GC001          XSHG      12.57  13.0   \n\n       high     low   close     volume         money  deal_number  \n2842  12.20   6.500   8.930  915840200  9.158402e+11     728989.0  \n2709  12.00   5.000   8.745  961308900  9.613089e+11     723141.0  \n2769  10.10   3.900   6.010  828761600  8.287616e+11     703459.0  \n2843  10.01   5.555   8.795  875500800  8.755008e+11     696009.0  \n2767  24.00  13.000  17.695  703348000  7.033480e+11     669847.0"}
  suggestedFilename: "doc_JQDatadoc_9948_overview_国债逆回购日行情数据"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9948"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 国债逆回购日行情数据

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9948

## 描述

描述

## 内容

#### 国债逆回购日行情数据

- 历史范围：上市至今；更新时间：每日19：00、22:00更新

```python
from jqdatasdk import *
df=bond.run_query(query(bond.REPO_DAILY_PRICE).limit(n))
```

描述

- 获取国债逆回购日行情数据

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

- query函数的更多用法详见：query简易教程

国债逆回购日行情参数

- query(bond.REPO_DAILY_PRICE)：表示从bond.REPO_DAILY_PRICE这张表中查询国债逆回购日行情数据，其中bond是库名，REPO_DAILY_PRICE是表名。bond库中的表都可以使用run_query方法调用,在查询表数据时还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2，多个字段用逗号分隔进行提取；query函数的更多用法详见：[query简易教程]
- bond.REPO_DAILY_PRICE：获取国债逆回购日行情数据，表结构和字段信息如下：
- filter(bond.REPO_DAILY_PRICE.code==code)：指定筛选条件，通过bond.REPO_DAILY_PRICE.code == '131801' 可以指定债券代码来获取国债逆回购日行情数据；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| date | date | 交易日期 |
| code | varchar(12) | 回购代码，如 '204001.XSHG' |
| name | varchar(20) | 回购简称，如 'GC001' |
| exchange_code | varchar(12) | 证券市场编码。XSHG-上海证券交易所；XSHE-深圳证券交易所 |
| pre_close | decimal(10,4) | 前收盘利率(%) |
| open | decimal(10,4) | 开盘利率(%) |
| high | decimal(10,4) | 最高利率(%) |
| low | decimal(10,4) | 最低利率(%) |
| close | decimal(10,4) | 收盘利率(%) |
| volume | bigint | 成交量（手） |
| money | decimal（20,2） | 成交额（元） |
| deal_number | int | 成交笔数（笔） |

###### 示例：

示例

```python
from jqdatasdk import *
df=bond.run_query(query(bond.REPO_DAILY_PRICE))
print(df.sort_values(by='deal_number',ascending=False)[:5])

        id        date         code   name exchange_code  pre_close  open  \
2842  2843  2018-04-24  204001.XSHG  GC001          XSHG       8.87   9.5   
2709  2710  2017-10-09  204001.XSHG  GC001          XSHG      16.63   5.0   
2769  2770  2018-01-02  204001.XSHG  GC001          XSHG      14.53   3.9   
2843  2844  2018-04-25  204001.XSHG  GC001          XSHG       8.93   6.0   
2767  2768  2017-12-28  204001.XSHG  GC001          XSHG      12.57  13.0   

       high     low   close     volume         money  deal_number  
2842  12.20   6.500   8.930  915840200  9.158402e+11     728989.0  
2709  12.00   5.000   8.745  961308900  9.613089e+11     723141.0  
2769  10.10   3.900   6.010  828761600  8.287616e+11     703459.0  
2843  10.01   5.555   8.795  875500800  8.755008e+11     696009.0  
2767  24.00  13.000  17.695  703348000  7.033480e+11     669847.0
```
