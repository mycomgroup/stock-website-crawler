---
id: "url-36497300"
type: "website"
title: "将标的代码转化成聚宽标准格式"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10254"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:27.215Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10254"
  headings:
    - {"level":3,"text":"将标的代码转化成聚宽标准格式","id":""}
  paragraphs:
    - "描述"
    - "注意"
    - "以场内基金为例"
  lists:
    - {"type":"ul","items":["将标的代码转化成聚宽标准格式","适用于A股市场股票、期货以及场内基金代码,支持传入单只标的或一个标的list<、li>"]}
    - {"type":"ul","items":["由于同一代码可能代表不同的交易品种，JQData给每个交易品种后面都添加了该市场特定的代码后缀，用户在调用API时，需要将参数security传入带有该市场后缀的证券代码，如security='600519.XSHG'，以便于区分实际调用的交易品种。以下列出了每个交易市场的代码后缀和示例代码。"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"normalize_code(code)"}
    - {"language":"python","code":"#输入\nnormalize_code(['150008','561130'])\n#输出\n['150008.XSHE', '561130.XSHG']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"将标的代码转化成聚宽标准格式"}
    - {"type":"codeblock","language":"python","content":"normalize_code(code)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["将标的代码转化成聚宽标准格式","适用于A股市场股票、期货以及场内基金代码,支持传入单只标的或一个标的list<、li>"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["由于同一代码可能代表不同的交易品种，JQData给每个交易品种后面都添加了该市场特定的代码后缀，用户在调用API时，需要将参数security传入带有该市场后缀的证券代码，如security='600519.XSHG'，以便于区分实际调用的交易品种。以下列出了每个交易市场的代码后缀和示例代码。"]}
    - {"type":"paragraph","content":"以场内基金为例"}
    - {"type":"codeblock","language":"python","content":"#输入\nnormalize_code(['150008','561130'])\n#输出\n['150008.XSHE', '561130.XSHG']"}
  suggestedFilename: "doc_JQDatadoc_10254_overview_将标的代码转化成聚宽标准格式"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10254"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 将标的代码转化成聚宽标准格式

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10254

## 描述

描述

## 内容

#### 将标的代码转化成聚宽标准格式

```python
normalize_code(code)
```

描述

- 将标的代码转化成聚宽标准格式
- 适用于A股市场股票、期货以及场内基金代码,支持传入单只标的或一个标的list<、li>

注意

- 由于同一代码可能代表不同的交易品种，JQData给每个交易品种后面都添加了该市场特定的代码后缀，用户在调用API时，需要将参数security传入带有该市场后缀的证券代码，如security='600519.XSHG'，以便于区分实际调用的交易品种。以下列出了每个交易市场的代码后缀和示例代码。

以场内基金为例

```python
#输入
normalize_code(['150008','561130'])
#输出
['150008.XSHE', '561130.XSHG']
```
