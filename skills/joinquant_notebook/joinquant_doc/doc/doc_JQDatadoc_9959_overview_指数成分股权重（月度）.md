---
id: "url-7a226ed6"
type: "website"
title: "指数成分股权重（月度）"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9959"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:21:51.873Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9959"
  headings:
    - {"level":3,"text":"指数成分股权重（月度）","id":""}
    - {"level":5,"text":"示例：","id":"-1"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"ul","items":["指数成本股权重披露时间不固定，但此接口每日都会检查更新。注：中证指数公司一般只在月末/月初披露。请点击[指数列表]查看指数信息"]}
    - {"type":"ul","items":["index_id: 代表指数的标准形式代码， 形式：指数代码.交易所代码，例如\"000001.XSHG\"。","date: 查询权重信息的日期，形式：\"%Y-%m-%d\"，例如\"2018-05-03\"；"]}
    - {"type":"ul","items":["查询到对应日期，且有权重数据，返回 pandas.DataFrame， code(股票代码)，display_name(股票名称), date(日期), weight(权重)；","查询到对应日期，且无权重数据， 返回距离查询日期最近日期的权重信息；","找不到对应日期的权重信息， 返回距离查询日期最近日期的权重信息；"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_index_weights(index_id, date=None)"}
    - {"language":"python","code":"#获取2018年5月9日这天的上证指数的成份股权重\ndf = get_index_weights(index_id=\"000001.XSHG\", date=\"2018-05-09\")\nprint(df)\n\n＃输出\n                   date  weight display_name\n603648.XSHG  2018-04-27   0.023         畅联股份\n603139.XSHG  2018-04-27   0.007         康惠制药\n603138.XSHG  2018-04-27   0.015         海量数据\n603136.XSHG  2018-04-27   0.009          天目湖\n603131.XSHG  2018-04-27   0.011         上海沪工\n...                 ...     ...          ...\n603005.XSHG  2018-04-27   0.023         晶方科技\n603007.XSHG  2018-04-27   0.013         ST花王\n603006.XSHG  2018-04-27   0.008         联明股份\n603009.XSHG  2018-04-27   0.014         北特科技\n603008.XSHG  2018-04-27   0.022          喜临门"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"指数成分股权重（月度）"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_index_weights(index_id, date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["指数成本股权重披露时间不固定，但此接口每日都会检查更新。注：中证指数公司一般只在月末/月初披露。请点击[指数列表]查看指数信息"]}
    - {"type":"list","listType":"ul","items":["index_id: 代表指数的标准形式代码， 形式：指数代码.交易所代码，例如\"000001.XSHG\"。","date: 查询权重信息的日期，形式：\"%Y-%m-%d\"，例如\"2018-05-03\"；"]}
    - {"type":"list","listType":"ul","items":["查询到对应日期，且有权重数据，返回 pandas.DataFrame， code(股票代码)，display_name(股票名称), date(日期), weight(权重)；","查询到对应日期，且无权重数据， 返回距离查询日期最近日期的权重信息；","找不到对应日期的权重信息， 返回距离查询日期最近日期的权重信息；"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#获取2018年5月9日这天的上证指数的成份股权重\ndf = get_index_weights(index_id=\"000001.XSHG\", date=\"2018-05-09\")\nprint(df)\n\n＃输出\n                   date  weight display_name\n603648.XSHG  2018-04-27   0.023         畅联股份\n603139.XSHG  2018-04-27   0.007         康惠制药\n603138.XSHG  2018-04-27   0.015         海量数据\n603136.XSHG  2018-04-27   0.009          天目湖\n603131.XSHG  2018-04-27   0.011         上海沪工\n...                 ...     ...          ...\n603005.XSHG  2018-04-27   0.023         晶方科技\n603007.XSHG  2018-04-27   0.013         ST花王\n603006.XSHG  2018-04-27   0.008         联明股份\n603009.XSHG  2018-04-27   0.014         北特科技\n603008.XSHG  2018-04-27   0.022          喜临门"}
  suggestedFilename: "doc_JQDatadoc_9959_overview_指数成分股权重（月度）"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9959"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 指数成分股权重（月度）

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9959

## 描述

描述

## 内容

#### 指数成分股权重（月度）

- 历史范围：2005年至今；更新时间：8:00更新

```python
get_index_weights(index_id, date=None)
```

描述

- 指数成本股权重披露时间不固定，但此接口每日都会检查更新。注：中证指数公司一般只在月末/月初披露。请点击[指数列表]查看指数信息

- index_id: 代表指数的标准形式代码， 形式：指数代码.交易所代码，例如"000001.XSHG"。
- date: 查询权重信息的日期，形式："%Y-%m-%d"，例如"2018-05-03"；

- 查询到对应日期，且有权重数据，返回 pandas.DataFrame， code(股票代码)，display_name(股票名称), date(日期), weight(权重)；
- 查询到对应日期，且无权重数据， 返回距离查询日期最近日期的权重信息；
- 找不到对应日期的权重信息， 返回距离查询日期最近日期的权重信息；

###### 示例：

```python
#获取2018年5月9日这天的上证指数的成份股权重
df = get_index_weights(index_id="000001.XSHG", date="2018-05-09")
print(df)

＃输出
                   date  weight display_name
603648.XSHG  2018-04-27   0.023         畅联股份
603139.XSHG  2018-04-27   0.007         康惠制药
603138.XSHG  2018-04-27   0.015         海量数据
603136.XSHG  2018-04-27   0.009          天目湖
603131.XSHG  2018-04-27   0.011         上海沪工
...                 ...     ...          ...
603005.XSHG  2018-04-27   0.023         晶方科技
603007.XSHG  2018-04-27   0.013         ST花王
603006.XSHG  2018-04-27   0.008         联明股份
603009.XSHG  2018-04-27   0.014         北特科技
603008.XSHG  2018-04-27   0.022          喜临门
```
