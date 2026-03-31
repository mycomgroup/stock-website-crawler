---
id: "url-7a226e3b"
type: "website"
title: "期货主力合约"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9909"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:19:44.826Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9909"
  headings:
    - {"level":3,"text":"期货主力合约","id":""}
    - {"level":5,"text":"示例：","id":"-1"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：19:00更新下一交易日"]}
    - {"type":"ul","items":["获取主力合约对应的标的"]}
    - {"type":"ul","items":["underlying_symbol: 期货合约品种，如 'AG'(白银)","date:指定日期参数，获取历史上该日期的主力期货合约 ,如未指定end_date时返回date当天的主力合约(字符串格式), 默认为当前时间; 该参数可指定分时秒，因期货夜盘的存在，date参数的分时秒指定为19:00:00(含)之后返回为下一交易日的主力","end_date:可选参数，如指定则返回date当天(忽略分时秒)到end_date这一个时间区间的主力合约序列(Series)"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_dominant_future(underlying_symbol,date , end_date )"}
    - {"language":"python","code":"# 获取某一天的主力合约对应的期货合约代码，指定日期为'2018-05-06'\nget_dominant_future('AU','2018-05-06')\n>>> 'AU1812.XSGE'"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"期货主力合约"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：19:00更新下一交易日"]}
    - {"type":"codeblock","language":"python","content":"get_dominant_future(underlying_symbol,date , end_date )"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取主力合约对应的标的"]}
    - {"type":"list","listType":"ul","items":["underlying_symbol: 期货合约品种，如 'AG'(白银)","date:指定日期参数，获取历史上该日期的主力期货合约 ,如未指定end_date时返回date当天的主力合约(字符串格式), 默认为当前时间; 该参数可指定分时秒，因期货夜盘的存在，date参数的分时秒指定为19:00:00(含)之后返回为下一交易日的主力","end_date:可选参数，如指定则返回date当天(忽略分时秒)到end_date这一个时间区间的主力合约序列(Series)"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 获取某一天的主力合约对应的期货合约代码，指定日期为'2018-05-06'\nget_dominant_future('AU','2018-05-06')\n>>> 'AU1812.XSGE'"}
  suggestedFilename: "doc_JQDatadoc_9909_overview_期货主力合约"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9909"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 期货主力合约

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9909

## 描述

描述

## 内容

#### 期货主力合约

- 历史范围：2005年至今；更新时间：19:00更新下一交易日

```python
get_dominant_future(underlying_symbol,date , end_date )
```

描述

- 获取主力合约对应的标的

- underlying_symbol: 期货合约品种，如 'AG'(白银)
- date:指定日期参数，获取历史上该日期的主力期货合约 ,如未指定end_date时返回date当天的主力合约(字符串格式), 默认为当前时间; 该参数可指定分时秒，因期货夜盘的存在，date参数的分时秒指定为19:00:00(含)之后返回为下一交易日的主力
- end_date:可选参数，如指定则返回date当天(忽略分时秒)到end_date这一个时间区间的主力合约序列(Series)

###### 示例：

```python
# 获取某一天的主力合约对应的期货合约代码，指定日期为'2018-05-06'
get_dominant_future('AU','2018-05-06')
>>> 'AU1812.XSGE'
```
