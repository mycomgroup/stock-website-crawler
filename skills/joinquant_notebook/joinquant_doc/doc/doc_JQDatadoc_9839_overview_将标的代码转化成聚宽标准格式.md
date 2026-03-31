---
id: "url-7a226ad7"
type: "website"
title: "将标的代码转化成聚宽标准格式"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9839"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:16:50.417Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9839"
  headings:
    - {"level":3,"text":"将标的代码转化成聚宽标准格式","id":""}
  paragraphs:
    - "描述"
    - "注意"
    - "以股票为例"
  lists:
    - {"type":"ul","items":["将标的代码转化成聚宽标准格式","适用于A股市场股票、期货以及场内基金代码,支持传入单只标的或一个标的list"]}
    - {"type":"ul","items":["由于同一代码可能代表不同的交易品种，JQData给每个交易品种后面都添加了该市场特定的代码后缀，用户在调用API时，需要将参数security传入带有该市场后缀的证券代码，如security='600519.XSHG'，以便于区分实际调用的交易品种。以下列出了每个交易市场的代码后缀和示例代码。"]}
  tables:
    - {"caption":"","headers":["交易市场","代码后缀","示例代码","证券简称"],"rows":[["上海证券交易所",".XSHG","600519.XSHG","贵州茅台"],["深圳证券交易所",".XSHE","000001.XSHE","平安银行"],["中金所",".CCFX","IC9999.CCFX","中证500主力合约"],["大商所",".XDCE","A9999.XDCE","豆一主力合约"],["上期所",".XSGE","AU9999.XSGE","黄金主力合约"],["郑商所",".XZCE","CY8888.XZCE","棉纱期货指数"],["上海国际能源期货交易所",".XINE","SC9999.XINE","原油主力合约"],["场外基金",".OF","398051.OF","中海环保新能源混合"]]}
  codeBlocks:
    - {"language":"python","code":"normalize_code(code)"}
    - {"language":"python","code":"#输入\nnormalize_code(['000001', 'SZ000001', '000001SZ', '000001.sz', '000001.XSHE'])\n#输出\n['000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE']"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"将标的代码转化成聚宽标准格式"}
    - {"type":"codeblock","language":"python","content":"normalize_code(code)"}
    - {"type":"table","headers":["交易市场","代码后缀","示例代码","证券简称"],"rows":[["上海证券交易所",".XSHG","600519.XSHG","贵州茅台"],["深圳证券交易所",".XSHE","000001.XSHE","平安银行"],["中金所",".CCFX","IC9999.CCFX","中证500主力合约"],["大商所",".XDCE","A9999.XDCE","豆一主力合约"],["上期所",".XSGE","AU9999.XSGE","黄金主力合约"],["郑商所",".XZCE","CY8888.XZCE","棉纱期货指数"],["上海国际能源期货交易所",".XINE","SC9999.XINE","原油主力合约"],["场外基金",".OF","398051.OF","中海环保新能源混合"]]}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["将标的代码转化成聚宽标准格式","适用于A股市场股票、期货以及场内基金代码,支持传入单只标的或一个标的list"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["由于同一代码可能代表不同的交易品种，JQData给每个交易品种后面都添加了该市场特定的代码后缀，用户在调用API时，需要将参数security传入带有该市场后缀的证券代码，如security='600519.XSHG'，以便于区分实际调用的交易品种。以下列出了每个交易市场的代码后缀和示例代码。"]}
    - {"type":"paragraph","content":"以股票为例"}
    - {"type":"codeblock","language":"python","content":"#输入\nnormalize_code(['000001', 'SZ000001', '000001SZ', '000001.sz', '000001.XSHE'])\n#输出\n['000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE']"}
  suggestedFilename: "doc_JQDatadoc_9839_overview_将标的代码转化成聚宽标准格式"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9839"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 将标的代码转化成聚宽标准格式

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9839

## 描述

描述

## 内容

#### 将标的代码转化成聚宽标准格式

```python
normalize_code(code)
```

| 交易市场 | 代码后缀 | 示例代码 | 证券简称 |
| --- | --- | --- | --- |
| 上海证券交易所 | .XSHG | 600519.XSHG | 贵州茅台 |
| 深圳证券交易所 | .XSHE | 000001.XSHE | 平安银行 |
| 中金所 | .CCFX | IC9999.CCFX | 中证500主力合约 |
| 大商所 | .XDCE | A9999.XDCE | 豆一主力合约 |
| 上期所 | .XSGE | AU9999.XSGE | 黄金主力合约 |
| 郑商所 | .XZCE | CY8888.XZCE | 棉纱期货指数 |
| 上海国际能源期货交易所 | .XINE | SC9999.XINE | 原油主力合约 |
| 场外基金 | .OF | 398051.OF | 中海环保新能源混合 |

描述

- 将标的代码转化成聚宽标准格式
- 适用于A股市场股票、期货以及场内基金代码,支持传入单只标的或一个标的list

注意

- 由于同一代码可能代表不同的交易品种，JQData给每个交易品种后面都添加了该市场特定的代码后缀，用户在调用API时，需要将参数security传入带有该市场后缀的证券代码，如security='600519.XSHG'，以便于区分实际调用的交易品种。以下列出了每个交易市场的代码后缀和示例代码。

以股票为例

```python
#输入
normalize_code(['000001', 'SZ000001', '000001SZ', '000001.sz', '000001.XSHE'])
#输出
['000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE', '000001.XSHE']
```
