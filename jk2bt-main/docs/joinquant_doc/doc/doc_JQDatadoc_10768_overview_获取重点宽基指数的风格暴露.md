---
id: "url-36496018"
type: "website"
title: "获取重点宽基指数的风格暴露"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10768"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:48:36.267Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10768"
  headings:
    - {"level":3,"text":"获取重点宽基指数的风格暴露","id":""}
    - {"level":5,"text":"参数","id":""}
    - {"level":5,"text":"代码示例","id":""}
  paragraphs:
    - "描述"
    - "返回"
    - "注意"
  lists:
    - {"type":"ul","items":["历史范围：提供2011-08-31至今的数据，9点更新前一交易日"]}
    - {"type":"ul","items":["获取重点宽基指数的风格暴露,提供2011-08-31至今的数据 index : 指数代码,可选 ['000300.XSHG', '000905.XSHG', '000906.XSHG', '000852.XSHG', '000985.XSHG'] 中的一个"]}
    - {"type":"ul","items":["DataFrame,宽基指数的风格暴露值"]}
    - {"type":"ul","items":["算法：指数中的个股每日权重与其对应的因子暴露值相乘并求和"]}
    - {"type":"ul","items":["获取沪深300指数的风格暴露"]}
  tables:
    - {"caption":"","headers":["参数","中文名称","备注"],"rows":[["index","指数代码","可选值为 ['000300.XSHG', '000905.XSHG', '000906.XSHG', '000852.XSHG', '000985.XSHG'] 中的一个"],["factors","因子名称","单个因子（字符串）或一个因子列表，支持风格因子如 \"size\"，支持申万 / 聚宽一级行业如 \"801010\" 和 \"HY001\"，注意：为避免混淆，风格因子仅支持传递 style 和 style_pro 中的一类，也可指定因子分类 ('style' 或'style_pro') 表示分类下的所有风格因子"],["start_date","开始日期","字符串或 datetime 对象"],["end_date","结束日期","字符串或 datetime 对象，可以与 start_date 或 count 配合使用"],["count","表示 截止 end_date 之前交易日的数量（含 end_date 当日）","与start_date参数二选一"]]}
  codeBlocks:
    - {"language":"python","code":"get_index_style_exposure(index, factors=None,start_date=None, end_date=None, count=None)"}
    - {"language":"python","code":"get_index_style_exposure('000300.XSHG', factors='size',start_date='2025-01-01', end_date='2025-01-31')\n\n                size\n2025-01-02    0.852575\n2025-01-03    0.838789\n2025-01-06    0.836143\n2025-01-07    0.845130\n2025-01-08    0.844728\n2025-01-09    0.849589\n2025-01-10    0.841113\n2025-01-13    0.844195\n2025-01-14    0.855145\n2025-01-15    0.856006\n2025-01-16    0.858106\n2025-01-17    0.856345\n2025-01-20    0.860688\n2025-01-21    0.859198"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取重点宽基指数的风格暴露"}
    - {"type":"list","listType":"ul","items":["历史范围：提供2011-08-31至今的数据，9点更新前一交易日"]}
    - {"type":"codeblock","language":"python","content":"get_index_style_exposure(index, factors=None,start_date=None, end_date=None, count=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取重点宽基指数的风格暴露,提供2011-08-31至今的数据 index : 指数代码,可选 ['000300.XSHG', '000905.XSHG', '000906.XSHG', '000852.XSHG', '000985.XSHG'] 中的一个"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["DataFrame,宽基指数的风格暴露值"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["算法：指数中的个股每日权重与其对应的因子暴露值相乘并求和"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["参数","中文名称","备注"],"rows":[["index","指数代码","可选值为 ['000300.XSHG', '000905.XSHG', '000906.XSHG', '000852.XSHG', '000985.XSHG'] 中的一个"],["factors","因子名称","单个因子（字符串）或一个因子列表，支持风格因子如 \"size\"，支持申万 / 聚宽一级行业如 \"801010\" 和 \"HY001\"，注意：为避免混淆，风格因子仅支持传递 style 和 style_pro 中的一类，也可指定因子分类 ('style' 或'style_pro') 表示分类下的所有风格因子"],["start_date","开始日期","字符串或 datetime 对象"],["end_date","结束日期","字符串或 datetime 对象，可以与 start_date 或 count 配合使用"],["count","表示 截止 end_date 之前交易日的数量（含 end_date 当日）","与start_date参数二选一"]]}
    - {"type":"heading","level":5,"content":"代码示例"}
    - {"type":"list","listType":"ul","items":["获取沪深300指数的风格暴露"]}
    - {"type":"codeblock","language":"python","content":"get_index_style_exposure('000300.XSHG', factors='size',start_date='2025-01-01', end_date='2025-01-31')\n\n                size\n2025-01-02    0.852575\n2025-01-03    0.838789\n2025-01-06    0.836143\n2025-01-07    0.845130\n2025-01-08    0.844728\n2025-01-09    0.849589\n2025-01-10    0.841113\n2025-01-13    0.844195\n2025-01-14    0.855145\n2025-01-15    0.856006\n2025-01-16    0.858106\n2025-01-17    0.856345\n2025-01-20    0.860688\n2025-01-21    0.859198"}
  suggestedFilename: "doc_JQDatadoc_10768_overview_获取重点宽基指数的风格暴露"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10768"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取重点宽基指数的风格暴露

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10768

## 描述

描述

## 内容

#### 获取重点宽基指数的风格暴露

- 历史范围：提供2011-08-31至今的数据，9点更新前一交易日

```python
get_index_style_exposure(index, factors=None,start_date=None, end_date=None, count=None)
```

描述

- 获取重点宽基指数的风格暴露,提供2011-08-31至今的数据 index : 指数代码,可选 ['000300.XSHG', '000905.XSHG', '000906.XSHG', '000852.XSHG', '000985.XSHG'] 中的一个

返回

- DataFrame,宽基指数的风格暴露值

注意

- 算法：指数中的个股每日权重与其对应的因子暴露值相乘并求和

###### 参数

| 参数 | 中文名称 | 备注 |
| --- | --- | --- |
| index | 指数代码 | 可选值为 ['000300.XSHG', '000905.XSHG', '000906.XSHG', '000852.XSHG', '000985.XSHG'] 中的一个 |
| factors | 因子名称 | 单个因子（字符串）或一个因子列表，支持风格因子如 "size"，支持申万 / 聚宽一级行业如 "801010" 和 "HY001"，注意：为避免混淆，风格因子仅支持传递 style 和 style_pro 中的一类，也可指定因子分类 ('style' 或'style_pro') 表示分类下的所有风格因子 |
| start_date | 开始日期 | 字符串或 datetime 对象 |
| end_date | 结束日期 | 字符串或 datetime 对象，可以与 start_date 或 count 配合使用 |
| count | 表示 截止 end_date 之前交易日的数量（含 end_date 当日） | 与start_date参数二选一 |

###### 代码示例

- 获取沪深300指数的风格暴露

```python
get_index_style_exposure('000300.XSHG', factors='size',start_date='2025-01-01', end_date='2025-01-31')

                size
2025-01-02    0.852575
2025-01-03    0.838789
2025-01-06    0.836143
2025-01-07    0.845130
2025-01-08    0.844728
2025-01-09    0.849589
2025-01-10    0.841113
2025-01-13    0.844195
2025-01-14    0.855145
2025-01-15    0.856006
2025-01-16    0.858106
2025-01-17    0.856345
2025-01-20    0.860688
2025-01-21    0.859198
```
