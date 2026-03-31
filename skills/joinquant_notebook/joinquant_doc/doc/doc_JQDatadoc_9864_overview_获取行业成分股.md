---
id: "url-7a226b2f"
type: "website"
title: "获取行业成分股"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9864"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:41.634Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9864"
  headings:
    - {"level":3,"text":"获取行业成分股","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "描述"
    - "行业分类列表"
    - "参数"
    - "返回"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"ul","items":["获取行业列表。"]}
    - {"type":"ul","items":["获取在给定日期一个行业的所有股票，行业分类列表见数据页面 [行业概念数据]"]}
    - {"type":"ul","items":["industry_code：行业编码","date：查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None."]}
    - {"type":"ul","items":["返回股票代码的list"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_industry_stocks(industry_code, date=None)"}
    - {"language":"python","code":"# 获取计算机/互联网行业的成分股\nstocks = get_industry_stocks('I64')\nprint(stocks[:5])\n\n# 输出\n['000503.XSHE', '000606.XSHE', '000676.XSHE', '000835.XSHE', '002072.XSHE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取行业成分股"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_industry_stocks(industry_code, date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取行业列表。"]}
    - {"type":"paragraph","content":"行业分类列表"}
    - {"type":"list","listType":"ul","items":["获取在给定日期一个行业的所有股票，行业分类列表见数据页面 [行业概念数据]"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["industry_code：行业编码","date：查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None."]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["返回股票代码的list"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"# 获取计算机/互联网行业的成分股\nstocks = get_industry_stocks('I64')\nprint(stocks[:5])\n\n# 输出\n['000503.XSHE', '000606.XSHE', '000676.XSHE', '000835.XSHE', '002072.XSHE']"}
  suggestedFilename: "doc_JQDatadoc_9864_overview_获取行业成分股"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9864"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取行业成分股

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9864

## 描述

描述

## 内容

#### 获取行业成分股

- 历史范围：2005年至今；更新时间：8:00更新

```python
get_industry_stocks(industry_code, date=None)
```

描述

- 获取行业列表。

行业分类列表

- 获取在给定日期一个行业的所有股票，行业分类列表见数据页面 [行业概念数据]

参数

- industry_code：行业编码
- date：查询日期, 一个字符串(格式类似'2015-10-15')或者[datetime.date]/[datetime.datetime]对象, 可以是None.

返回

- 返回股票代码的list

###### 示例

```python
# 获取计算机/互联网行业的成分股
stocks = get_industry_stocks('I64')
print(stocks[:5])

# 输出
['000503.XSHE', '000606.XSHE', '000676.XSHE', '000835.XSHE', '002072.XSHE']
```
