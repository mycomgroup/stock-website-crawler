---
id: "url-7a226b2d"
type: "website"
title: "查询股票所属板块概念"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9862"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:33.801Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9862"
  headings:
    - {"level":3,"text":"查询股票所属板块概念","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回"
    - "示例"
  lists:
    - {"type":"ul","items":["历史范围：2016年至今；更新时间：8:00更新"]}
    - {"type":"ul","items":["获取股票所属概念板块。返回一个dict，key为标的代码，value详见示例。"]}
    - {"type":"ul","items":["返回结果是一个dict，key是传入的股票代码"]}
    - {"type":"ul","items":["security：标的代码或包含标的代码的列表","query_dt：时刻,datetime或时刻形式的字符串,只传入日期代表日内时间为00:00:00.","security: 标的代码或标的列表","date: 要查询的日期，日期字符串/date对象/datetime对象，注意传入datetime对象时忽略日内时间；默认值为None，"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_concept(security, date=None)"}
    - {"language":"text","code":"# code是传入的股票代码；多个code返回嵌套的多个字典；\n# ‘jq_concept’代表聚宽概念；\n# XX是code所在的概念代码；\n# YY是code所在的概念名称；\n\n{code: { 'jq_concept':[\n            { 'concept_code': XX1; 'concept_name': YY1 },\n            { 'concept_code': XX2; 'concept_name': YY2 },\n            { 'concept_code': XX3; 'concept_name': YY3 }]\n        }\n}"}
    - {"language":"python","code":"dict1 = get_concept(['000001.XSHE', '000018.XSHE','000006.XSHE'], date='2019-07-15')\ndata = []  \nfor stock_code, info in dict1.items():  \n    for concept in info['jq_concept']:  \n        data.append({  \n            'stock_code': stock_code,  \n            'concept_name': concept['concept_name'],  \n            'concept_code': concept['concept_code']  \n        })  \ndf = pd.DataFrame(data)  \nprint(df)\n\n    stock_code concept_name concept_code\n0  000001.XSHE          深股通       SC0105\n1  000001.XSHE         融资融券       SC0181\n2  000001.XSHE         MSCI       SC0186\n3  000001.XSHE        转融券标的       SC0219\n4  000018.XSHE         民营医院       SC0113\n5  000006.XSHE       深圳国资改革       SC0098\n6  000006.XSHE          深股通       SC0105\n7  000006.XSHE         融资融券       SC0181\n8  000006.XSHE       粤港澳自贸区       SC0201\n9  000006.XSHE        转融券标的       SC0219"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"查询股票所属板块概念"}
    - {"type":"list","listType":"ul","items":["历史范围：2016年至今；更新时间：8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_concept(security, date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取股票所属概念板块。返回一个dict，key为标的代码，value详见示例。"]}
    - {"type":"list","listType":"ul","items":["返回结果是一个dict，key是传入的股票代码"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["security：标的代码或包含标的代码的列表","query_dt：时刻,datetime或时刻形式的字符串,只传入日期代表日内时间为00:00:00.","security: 标的代码或标的列表","date: 要查询的日期，日期字符串/date对象/datetime对象，注意传入datetime对象时忽略日内时间；默认值为None，"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"codeblock","language":"text","content":"# code是传入的股票代码；多个code返回嵌套的多个字典；\n# ‘jq_concept’代表聚宽概念；\n# XX是code所在的概念代码；\n# YY是code所在的概念名称；\n\n{code: { 'jq_concept':[\n            { 'concept_code': XX1; 'concept_name': YY1 },\n            { 'concept_code': XX2; 'concept_name': YY2 },\n            { 'concept_code': XX3; 'concept_name': YY3 }]\n        }\n}"}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"dict1 = get_concept(['000001.XSHE', '000018.XSHE','000006.XSHE'], date='2019-07-15')\ndata = []  \nfor stock_code, info in dict1.items():  \n    for concept in info['jq_concept']:  \n        data.append({  \n            'stock_code': stock_code,  \n            'concept_name': concept['concept_name'],  \n            'concept_code': concept['concept_code']  \n        })  \ndf = pd.DataFrame(data)  \nprint(df)\n\n    stock_code concept_name concept_code\n0  000001.XSHE          深股通       SC0105\n1  000001.XSHE         融资融券       SC0181\n2  000001.XSHE         MSCI       SC0186\n3  000001.XSHE        转融券标的       SC0219\n4  000018.XSHE         民营医院       SC0113\n5  000006.XSHE       深圳国资改革       SC0098\n6  000006.XSHE          深股通       SC0105\n7  000006.XSHE         融资融券       SC0181\n8  000006.XSHE       粤港澳自贸区       SC0201\n9  000006.XSHE        转融券标的       SC0219"}
  suggestedFilename: "doc_JQDatadoc_9862_overview_查询股票所属板块概念"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9862"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 查询股票所属板块概念

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9862

## 描述

描述

## 内容

#### 查询股票所属板块概念

- 历史范围：2016年至今；更新时间：8:00更新

```python
get_concept(security, date=None)
```

描述

- 获取股票所属概念板块。返回一个dict，key为标的代码，value详见示例。

- 返回结果是一个dict，key是传入的股票代码

参数

- security：标的代码或包含标的代码的列表
- query_dt：时刻,datetime或时刻形式的字符串,只传入日期代表日内时间为00:00:00.
- security: 标的代码或标的列表
- date: 要查询的日期，日期字符串/date对象/datetime对象，注意传入datetime对象时忽略日内时间；默认值为None，

返回

```text
# code是传入的股票代码；多个code返回嵌套的多个字典；
# ‘jq_concept’代表聚宽概念；
# XX是code所在的概念代码；
# YY是code所在的概念名称；

{code: { 'jq_concept':[
            { 'concept_code': XX1; 'concept_name': YY1 },
            { 'concept_code': XX2; 'concept_name': YY2 },
            { 'concept_code': XX3; 'concept_name': YY3 }]
        }
}
```

示例

```python
dict1 = get_concept(['000001.XSHE', '000018.XSHE','000006.XSHE'], date='2019-07-15')
data = []  
for stock_code, info in dict1.items():  
    for concept in info['jq_concept']:  
        data.append({  
            'stock_code': stock_code,  
            'concept_name': concept['concept_name'],  
            'concept_code': concept['concept_code']  
        })  
df = pd.DataFrame(data)  
print(df)

    stock_code concept_name concept_code
0  000001.XSHE          深股通       SC0105
1  000001.XSHE         融资融券       SC0181
2  000001.XSHE         MSCI       SC0186
3  000001.XSHE        转融券标的       SC0219
4  000018.XSHE         民营医院       SC0113
5  000006.XSHE       深圳国资改革       SC0098
6  000006.XSHE          深股通       SC0105
7  000006.XSHE         融资融券       SC0181
8  000006.XSHE       粤港澳自贸区       SC0201
9  000006.XSHE        转融券标的       SC0219
```
