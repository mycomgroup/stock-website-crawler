---
id: "url-7a226b2c"
type: "website"
title: "查询股票所属行业"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9861"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:29.756Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9861"
  headings:
    - {"level":3,"text":"查询股票所属行业","id":""}
    - {"level":5,"text":"参数","id":"-1"}
    - {"level":5,"text":"示例","id":"-2"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"ul","items":["查询股票所属行业"]}
    - {"type":"ul","items":["返回结果是一个dict，key是传入的股票代码"]}
    - {"type":"ul","items":["获取一只股票所属行业"]}
    - {"type":"ul","items":["同时获取多只股票的所属行业信息;返回dataframe"]}
  tables:
    - {"caption":"","headers":["参数","含义","注释"],"rows":[["security","标的代码","类型为字符串，形式如\"000001.XSHE\"；或为包含标的代码字符串的列表，形如[\"000001.XSHE\", \"000002.XSHE\"]"],["date","查询的日期","默认为None，指定查询当天数据。类型为字符串，形如\"2018-06-01\"或\"2018-06-01 09:00:00\"；或为datetime.datetime对象和datetime.date。注意传入对象的时分秒将被忽略。"],["df","是否以DataFrame 形式返回(jqdatasdk>=1.9.0新增参数)","默认为False,返回dict格式的数据"]]}
  codeBlocks:
    - {"language":"python","code":"get_industry(security, date=None)"}
    - {"language":"python","code":"#获取贵州茅台(\"600519.XSHG\")的所属行业数据\nd = get_industry(\"600519.XSHG\",date=\"2018-06-01\")\nprint(d)\n\n# 输出\n{'600519.XSHG': {'sw_l1': {'industry_code': '801120', 'industry_name': '食品饮料I'}, 'sw_l2': {'industry_code': '801123', 'industry_name': '饮料制造II'}, 'sw_l3': {'industry_code': '851231', 'industry_name': '白酒III'}, 'zjw': {'industry_code': 'C15', 'industry_name': '酒、饮料和精制茶制造业'}, 'jq_l2': {'industry_code': 'HY478', 'industry_name': '白酒与葡萄酒指数'}, 'jq_l1': {'industry_code': 'HY005', 'industry_name': '日常消费指数'}}}"}
    - {"language":"python","code":"d = get_industry(security= ['000001.XSHE','000002.XSHE'], date=\"2022-06-01\",df=True)\nd[d.type=='zjw']\n\n# 输出\n\n           code type industry_code industry_name\n1   000002.XSHE  zjw           K70          房地产业\n11  000001.XSHE  zjw           J66        货币金融服务"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"查询股票所属行业"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_industry(security, date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["查询股票所属行业"]}
    - {"type":"list","listType":"ul","items":["返回结果是一个dict，key是传入的股票代码"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["参数","含义","注释"],"rows":[["security","标的代码","类型为字符串，形式如\"000001.XSHE\"；或为包含标的代码字符串的列表，形如[\"000001.XSHE\", \"000002.XSHE\"]"],["date","查询的日期","默认为None，指定查询当天数据。类型为字符串，形如\"2018-06-01\"或\"2018-06-01 09:00:00\"；或为datetime.datetime对象和datetime.date。注意传入对象的时分秒将被忽略。"],["df","是否以DataFrame 形式返回(jqdatasdk>=1.9.0新增参数)","默认为False,返回dict格式的数据"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获取一只股票所属行业"]}
    - {"type":"codeblock","language":"python","content":"#获取贵州茅台(\"600519.XSHG\")的所属行业数据\nd = get_industry(\"600519.XSHG\",date=\"2018-06-01\")\nprint(d)\n\n# 输出\n{'600519.XSHG': {'sw_l1': {'industry_code': '801120', 'industry_name': '食品饮料I'}, 'sw_l2': {'industry_code': '801123', 'industry_name': '饮料制造II'}, 'sw_l3': {'industry_code': '851231', 'industry_name': '白酒III'}, 'zjw': {'industry_code': 'C15', 'industry_name': '酒、饮料和精制茶制造业'}, 'jq_l2': {'industry_code': 'HY478', 'industry_name': '白酒与葡萄酒指数'}, 'jq_l1': {'industry_code': 'HY005', 'industry_name': '日常消费指数'}}}"}
    - {"type":"list","listType":"ul","items":["同时获取多只股票的所属行业信息;返回dataframe"]}
    - {"type":"codeblock","language":"python","content":"d = get_industry(security= ['000001.XSHE','000002.XSHE'], date=\"2022-06-01\",df=True)\nd[d.type=='zjw']\n\n# 输出\n\n           code type industry_code industry_name\n1   000002.XSHE  zjw           K70          房地产业\n11  000001.XSHE  zjw           J66        货币金融服务"}
  suggestedFilename: "doc_JQDatadoc_9861_overview_查询股票所属行业"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9861"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 查询股票所属行业

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9861

## 描述

描述

## 内容

#### 查询股票所属行业

- 历史范围：2005年至今；更新时间：8:00更新

```python
get_industry(security, date=None)
```

描述

- 查询股票所属行业

- 返回结果是一个dict，key是传入的股票代码

###### 参数

| 参数 | 含义 | 注释 |
| --- | --- | --- |
| security | 标的代码 | 类型为字符串，形式如"000001.XSHE"；或为包含标的代码字符串的列表，形如["000001.XSHE", "000002.XSHE"] |
| date | 查询的日期 | 默认为None，指定查询当天数据。类型为字符串，形如"2018-06-01"或"2018-06-01 09:00:00"；或为datetime.datetime对象和datetime.date。注意传入对象的时分秒将被忽略。 |
| df | 是否以DataFrame 形式返回(jqdatasdk>=1.9.0新增参数) | 默认为False,返回dict格式的数据 |

###### 示例

- 获取一只股票所属行业

```python
#获取贵州茅台("600519.XSHG")的所属行业数据
d = get_industry("600519.XSHG",date="2018-06-01")
print(d)

# 输出
{'600519.XSHG': {'sw_l1': {'industry_code': '801120', 'industry_name': '食品饮料I'}, 'sw_l2': {'industry_code': '801123', 'industry_name': '饮料制造II'}, 'sw_l3': {'industry_code': '851231', 'industry_name': '白酒III'}, 'zjw': {'industry_code': 'C15', 'industry_name': '酒、饮料和精制茶制造业'}, 'jq_l2': {'industry_code': 'HY478', 'industry_name': '白酒与葡萄酒指数'}, 'jq_l1': {'industry_code': 'HY005', 'industry_name': '日常消费指数'}}}
```

- 同时获取多只股票的所属行业信息;返回dataframe

```python
d = get_industry(security= ['000001.XSHE','000002.XSHE'], date="2022-06-01",df=True)
d[d.type=='zjw']

# 输出

           code type industry_code industry_name
1   000002.XSHE  zjw           K70          房地产业
11  000001.XSHE  zjw           J66        货币金融服务
```
