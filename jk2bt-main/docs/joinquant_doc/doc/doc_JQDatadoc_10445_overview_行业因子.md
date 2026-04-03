---
id: "url-36496b9c"
type: "website"
title: "行业因子"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10445"
description: "可以获取以下行业的分类因子，股票属于这个行业则为赋值为1，否则赋值为0 1.证监会行业 2.聚宽行业(一二级) 3.申万行业(一二三级)"
source: ""
tags: []
crawl_time: "2026-03-27T07:46:46.064Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10445"
  headings:
    - {"level":3,"text":"行业因子","id":""}
  paragraphs:
    - "可以获取以下行业的分类因子，股票属于这个行业则为赋值为1，否则赋值为0 1.证监会行业 2.聚宽行业(一二级) 3.申万行业(一二三级)"
  lists: []
  tables: []
  codeBlocks:
    - {"language":"python","code":">>> df_dic = get_factor_values('000001.XSHE',['A01','HY007','801780','801723'] ,end_date='2023-02-23',count=1)\nprint(df_dic)\n>>>  {'A01':             000001.XSHE\n    2023-02-23            0, \n'HY007':             000001.XSHE\n    2023-02-23            1, \n'801780':             000001.XSHE\n    2023-02-23            1, \n'801723':             000001.XSHE\n    2023-02-23            0}"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"行业因子"}
    - {"type":"paragraph","content":"可以获取以下行业的分类因子，股票属于这个行业则为赋值为1，否则赋值为0 1.证监会行业 2.聚宽行业(一二级) 3.申万行业(一二三级)"}
    - {"type":"codeblock","language":"python","content":">>> df_dic = get_factor_values('000001.XSHE',['A01','HY007','801780','801723'] ,end_date='2023-02-23',count=1)\nprint(df_dic)\n>>>  {'A01':             000001.XSHE\n    2023-02-23            0, \n'HY007':             000001.XSHE\n    2023-02-23            1, \n'801780':             000001.XSHE\n    2023-02-23            1, \n'801723':             000001.XSHE\n    2023-02-23            0}"}
  suggestedFilename: "doc_JQDatadoc_10445_overview_行业因子"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10445"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 行业因子

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10445

## 描述

可以获取以下行业的分类因子，股票属于这个行业则为赋值为1，否则赋值为0 1.证监会行业 2.聚宽行业(一二级) 3.申万行业(一二三级)

## 内容

#### 行业因子

可以获取以下行业的分类因子，股票属于这个行业则为赋值为1，否则赋值为0 1.证监会行业 2.聚宽行业(一二级) 3.申万行业(一二三级)

```python
>>> df_dic = get_factor_values('000001.XSHE',['A01','HY007','801780','801723'] ,end_date='2023-02-23',count=1)
print(df_dic)
>>>  {'A01':             000001.XSHE
    2023-02-23            0, 
'HY007':             000001.XSHE
    2023-02-23            1, 
'801780':             000001.XSHE
    2023-02-23            1, 
'801723':             000001.XSHE
    2023-02-23            0}
```
