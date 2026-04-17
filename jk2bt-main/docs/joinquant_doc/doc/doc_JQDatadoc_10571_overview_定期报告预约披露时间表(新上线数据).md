---
id: "url-36496782"
type: "website"
title: "定期报告预约披露时间表(新上线数据)"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10571"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:47:33.235Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10571"
  headings:
    - {"level":3,"text":"定期报告预约披露时间表(新上线数据)","id":""}
    - {"level":5,"text":"示例","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回结果"
    - "注意"
    - "query函数的使用技巧"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"ul","items":["获取上市公司定期报告预约披露及实际披露日期"]}
    - {"type":"ul","items":["query(finance.STK_REPORT_DISCLOSURE)：表示从finance.STK_REPORT_DISCLOSURE这张表中查询所有字段信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：sqlalchemy.orm.query.Query对象","finance.STK_REPORT_DISCLOSURE：收录了上市公司定期报告预约披露及实际披露日期，表结构和字段信息如下：","filter(finance.STK_REPORT_DISCLOSURE.code==code)：指定筛选条件，通过finance.STK_REPORT_DISCLOSURE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_REPORT_DISCLOSURE.pub_date>='2015-01-01'，表示公告日期在2015年1月1日之后发布的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"ul","items":["query函数的更多用法详见：query简易教程"]}
  tables:
    - {"caption":"","headers":["字段","名称","类型","注释"],"rows":[["code","公司代码","VARCHAR(12)",""],["end_date","截止日期","DATE",""],["appoint_date","预约披露日","DATE",""],["first_date","首次变更日","DATE",""],["second_date","二次变更日","DATE",""],["third_date","三次变更日","DATE",""],["pub_date","实际披露日","DATE",""]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_REPORT_DISCLOSURE).filter(finance.STK_REPORT_DISCLOSURE.code==code).limit(n))"}
    - {"language":"python","code":"#查询贵州茅台2019年之后的数据，限定返回条数为10条\nfrom jqdatasdk import finance \nq=query(finance.STK_REPORT_DISCLOSURE).filter(finance.STK_REPORT_DISCLOSURE.code=='600519.XSHG',\n                                              finance.STK_REPORT_DISCLOSURE.end_date>='2019-01-01').limit(10)\ndf=finance.run_query(q)\nprint(df)\n\n       id         code    end_date appoint_date  first_date second_date  \\\n0  143825  600519.XSHG  2019-03-31   2019-04-25        None        None   \n1  140169  600519.XSHG  2019-06-30   2019-08-08  2019-07-18        None   \n2  136468  600519.XSHG  2019-09-30   2019-10-16        None        None   \n3  132661  600519.XSHG  2019-12-31   2020-03-25  2020-04-22        None   \n4  159688  600519.XSHG  2020-03-31   2020-04-28        None        None   \n5  155757  600519.XSHG  2020-06-30   2020-07-29        None        None   \n6  151704  600519.XSHG  2020-09-30   2020-10-26        None        None   \n7  147459  600519.XSHG  2020-12-31   2021-03-31        None        None   \n8  177187  600519.XSHG  2021-03-31   2021-04-28        None        None   \n9  172783  600519.XSHG  2021-06-30   2021-07-31        None        None   \n\n  third_date    pub_date  \n0       None  2019-04-25  \n1       None  2019-07-18  \n2       None  2019-10-16  \n3       None  2020-04-22  \n4       None  2020-04-28  \n5       None  2020-07-29  \n6       None  2020-10-26  \n7       None  2021-03-31  \n8       None  2021-04-28  \n9       None  2021-07-31"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"定期报告预约披露时间表(新上线数据)"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：交易日24:00更新"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import finance\nfinance.run_query(query(finance.STK_REPORT_DISCLOSURE).filter(finance.STK_REPORT_DISCLOSURE.code==code).limit(n))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取上市公司定期报告预约披露及实际披露日期"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["query(finance.STK_REPORT_DISCLOSURE)：表示从finance.STK_REPORT_DISCLOSURE这张表中查询所有字段信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：sqlalchemy.orm.query.Query对象","finance.STK_REPORT_DISCLOSURE：收录了上市公司定期报告预约披露及实际披露日期，表结构和字段信息如下：","filter(finance.STK_REPORT_DISCLOSURE.code==code)：指定筛选条件，通过finance.STK_REPORT_DISCLOSURE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_REPORT_DISCLOSURE.pub_date>='2015-01-01'，表示公告日期在2015年1月1日之后发布的数据；多个筛选条件用英文逗号分隔。","limit(n)：限制返回的数据条数，n指定返回条数。"]}
    - {"type":"paragraph","content":"返回结果"}
    - {"type":"list","listType":"ul","items":["返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["为了防止返回数据量过大, 我们每次最多返回5000行","不能进行连表查询，即同时查询多张表的数据","新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条","新增 get_table_info(table) 方法，支持查询数据表中的字段信息"]}
    - {"type":"paragraph","content":"query函数的使用技巧"}
    - {"type":"list","listType":"ul","items":["query函数的更多用法详见：query简易教程"]}
    - {"type":"table","headers":["字段","名称","类型","注释"],"rows":[["code","公司代码","VARCHAR(12)",""],["end_date","截止日期","DATE",""],["appoint_date","预约披露日","DATE",""],["first_date","首次变更日","DATE",""],["second_date","二次变更日","DATE",""],["third_date","三次变更日","DATE",""],["pub_date","实际披露日","DATE",""]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"#查询贵州茅台2019年之后的数据，限定返回条数为10条\nfrom jqdatasdk import finance \nq=query(finance.STK_REPORT_DISCLOSURE).filter(finance.STK_REPORT_DISCLOSURE.code=='600519.XSHG',\n                                              finance.STK_REPORT_DISCLOSURE.end_date>='2019-01-01').limit(10)\ndf=finance.run_query(q)\nprint(df)\n\n       id         code    end_date appoint_date  first_date second_date  \\\n0  143825  600519.XSHG  2019-03-31   2019-04-25        None        None   \n1  140169  600519.XSHG  2019-06-30   2019-08-08  2019-07-18        None   \n2  136468  600519.XSHG  2019-09-30   2019-10-16        None        None   \n3  132661  600519.XSHG  2019-12-31   2020-03-25  2020-04-22        None   \n4  159688  600519.XSHG  2020-03-31   2020-04-28        None        None   \n5  155757  600519.XSHG  2020-06-30   2020-07-29        None        None   \n6  151704  600519.XSHG  2020-09-30   2020-10-26        None        None   \n7  147459  600519.XSHG  2020-12-31   2021-03-31        None        None   \n8  177187  600519.XSHG  2021-03-31   2021-04-28        None        None   \n9  172783  600519.XSHG  2021-06-30   2021-07-31        None        None   \n\n  third_date    pub_date  \n0       None  2019-04-25  \n1       None  2019-07-18  \n2       None  2019-10-16  \n3       None  2020-04-22  \n4       None  2020-04-28  \n5       None  2020-07-29  \n6       None  2020-10-26  \n7       None  2021-03-31  \n8       None  2021-04-28  \n9       None  2021-07-31"}
  suggestedFilename: "doc_JQDatadoc_10571_overview_定期报告预约披露时间表(新上线数据)"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10571"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 定期报告预约披露时间表(新上线数据)

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10571

## 描述

描述

## 内容

#### 定期报告预约披露时间表(新上线数据)

- 历史范围：2005年至今；更新时间：交易日24:00更新

```python
from jqdatasdk import finance
finance.run_query(query(finance.STK_REPORT_DISCLOSURE).filter(finance.STK_REPORT_DISCLOSURE.code==code).limit(n))
```

描述

- 获取上市公司定期报告预约披露及实际披露日期

参数

- query(finance.STK_REPORT_DISCLOSURE)：表示从finance.STK_REPORT_DISCLOSURE这张表中查询所有字段信息，还可以指定所要查询的字段名，格式如下：query(库名.表名.字段名1，库名.表名.字段名2），多个字段用逗号分隔进行提取；query函数的更多用法详见：sqlalchemy.orm.query.Query对象
- finance.STK_REPORT_DISCLOSURE：收录了上市公司定期报告预约披露及实际披露日期，表结构和字段信息如下：
- filter(finance.STK_REPORT_DISCLOSURE.code==code)：指定筛选条件，通过finance.STK_REPORT_DISCLOSURE.code==code可以指定你想要查询的股票代码；除此之外，还可以对表中其他字段指定筛选条件，如finance.STK_REPORT_DISCLOSURE.pub_date>='2015-01-01'，表示公告日期在2015年1月1日之后发布的数据；多个筛选条件用英文逗号分隔。
- limit(n)：限制返回的数据条数，n指定返回条数。

返回结果

- 返回一个 dataframe，每一行对应数据表中的一条数据， 列索引是您所查询的字段名称

注意

- 为了防止返回数据量过大, 我们每次最多返回5000行
- 不能进行连表查询，即同时查询多张表的数据
- 新增 run_offset_query方法，支持分批从数据库提取超5000条的数据，上限20万条
- 新增 get_table_info(table) 方法，支持查询数据表中的字段信息

query函数的使用技巧

- query函数的更多用法详见：query简易教程

| 字段 | 名称 | 类型 | 注释 |
| --- | --- | --- | --- |
| code | 公司代码 | VARCHAR(12) |  |
| end_date | 截止日期 | DATE |  |
| appoint_date | 预约披露日 | DATE |  |
| first_date | 首次变更日 | DATE |  |
| second_date | 二次变更日 | DATE |  |
| third_date | 三次变更日 | DATE |  |
| pub_date | 实际披露日 | DATE |  |

###### 示例

```python
#查询贵州茅台2019年之后的数据，限定返回条数为10条
from jqdatasdk import finance 
q=query(finance.STK_REPORT_DISCLOSURE).filter(finance.STK_REPORT_DISCLOSURE.code=='600519.XSHG',
                                              finance.STK_REPORT_DISCLOSURE.end_date>='2019-01-01').limit(10)
df=finance.run_query(q)
print(df)

       id         code    end_date appoint_date  first_date second_date  \
0  143825  600519.XSHG  2019-03-31   2019-04-25        None        None   
1  140169  600519.XSHG  2019-06-30   2019-08-08  2019-07-18        None   
2  136468  600519.XSHG  2019-09-30   2019-10-16        None        None   
3  132661  600519.XSHG  2019-12-31   2020-03-25  2020-04-22        None   
4  159688  600519.XSHG  2020-03-31   2020-04-28        None        None   
5  155757  600519.XSHG  2020-06-30   2020-07-29        None        None   
6  151704  600519.XSHG  2020-09-30   2020-10-26        None        None   
7  147459  600519.XSHG  2020-12-31   2021-03-31        None        None   
8  177187  600519.XSHG  2021-03-31   2021-04-28        None        None   
9  172783  600519.XSHG  2021-06-30   2021-07-31        None        None   

  third_date    pub_date  
0       None  2019-04-25  
1       None  2019-07-18  
2       None  2019-10-16  
3       None  2020-04-22  
4       None  2020-04-28  
5       None  2020-07-29  
6       None  2020-10-26  
7       None  2021-03-31  
8       None  2021-04-28  
9       None  2021-07-31
```
