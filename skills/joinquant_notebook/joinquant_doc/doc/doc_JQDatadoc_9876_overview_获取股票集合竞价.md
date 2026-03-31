---
id: "url-7a226b50"
type: "website"
title: "获取股票集合竞价"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9876"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:18:24.978Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9876"
  headings:
    - {"level":3,"text":"获取股票集合竞价","id":""}
    - {"level":5,"text":"fields字段说明","id":""}
  paragraphs:
    - "描述"
    - "股票集合竞价字段"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：盘后15点,24:00校对完成入库"]}
    - {"type":"ul","items":["支持股票（2010年至今）的集合竞价，当日的集合竞价数据于盘后15点返回。","为了防止返回数据量过大, 我们每次最多返回10000行。"]}
    - {"type":"ul","items":["security: 股票（2010年至今）","start_date: 开始日期，YYYY-MM-DD格式","end_date: 结束日期，YYYY-MM-DD格式","fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。"]}
    - {"type":"ul","items":["返回指定时间区间标的集合竞价tick数据，返回字段结果如下："]}
  tables:
    - {"caption":"","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价（不复权）","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
  codeBlocks:
    - {"language":"python","code":"get_call_auction(security, start_date, end_date, fields=None)"}
    - {"language":"python","code":"#获取平安银行2019-09-02至2019-09-05期间的集合竞价数据\ndf=get_call_auction('000001.XSHE','2022-09-02','2022-09-05')\nprint(df)\n\n          code                time  current    volume      money   a1_p  \\\n0  000001.XSHE 2022-09-02 09:25:00    12.62  369458.0  4662559.0  12.63   \n1  000001.XSHE 2022-09-05 09:25:00    12.46  394700.0  4917962.0  12.46   \n\n     a1_v   a2_p     a2_v   a3_p     a3_v   a4_p    a4_v   a5_p     a5_v  \\\n0  8200.0  12.64   5000.0  12.65  12900.0  12.66  4500.0  12.67   4900.0   \n1  9355.0  12.47  28000.0  12.48  58100.0  12.49  4600.0  12.50  13400.0   \n\n    b1_p      b1_v   b2_p     b2_v   b3_p     b3_v   b4_p     b4_v   b5_p  \\\n0  12.62   95142.0  12.61  26200.0  12.60  83500.0  12.59  15500.0  12.58   \n1  12.45  638300.0  12.44  95900.0  12.43  66000.0  12.42  59000.0  12.41   \n\n       b5_v  \n0  107600.0  \n1  217500.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取股票集合竞价"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：盘后15点,24:00校对完成入库"]}
    - {"type":"codeblock","language":"python","content":"get_call_auction(security, start_date, end_date, fields=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["支持股票（2010年至今）的集合竞价，当日的集合竞价数据于盘后15点返回。","为了防止返回数据量过大, 我们每次最多返回10000行。"]}
    - {"type":"paragraph","content":"股票集合竞价字段"}
    - {"type":"list","listType":"ul","items":["security: 股票（2010年至今）","start_date: 开始日期，YYYY-MM-DD格式","end_date: 结束日期，YYYY-MM-DD格式","fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。"]}
    - {"type":"heading","level":5,"content":"fields字段说明"}
    - {"type":"list","listType":"ul","items":["返回指定时间区间标的集合竞价tick数据，返回字段结果如下："]}
    - {"type":"table","headers":["字段名","说明","字段类型"],"rows":[["time","时间","datetime"],["current","当前价（不复权）","float"],["volume","累计成交量（股）","float"],["money","累计成交额（元）","float"],["a1_v~a5_v","五档卖量","float"],["a1_p~a5_p","五档卖价","float"],["b1_v~b5_v","五档买量","float"],["b1_p~b5_p","五档买价","float"]]}
    - {"type":"codeblock","language":"python","content":"#获取平安银行2019-09-02至2019-09-05期间的集合竞价数据\ndf=get_call_auction('000001.XSHE','2022-09-02','2022-09-05')\nprint(df)\n\n          code                time  current    volume      money   a1_p  \\\n0  000001.XSHE 2022-09-02 09:25:00    12.62  369458.0  4662559.0  12.63   \n1  000001.XSHE 2022-09-05 09:25:00    12.46  394700.0  4917962.0  12.46   \n\n     a1_v   a2_p     a2_v   a3_p     a3_v   a4_p    a4_v   a5_p     a5_v  \\\n0  8200.0  12.64   5000.0  12.65  12900.0  12.66  4500.0  12.67   4900.0   \n1  9355.0  12.47  28000.0  12.48  58100.0  12.49  4600.0  12.50  13400.0   \n\n    b1_p      b1_v   b2_p     b2_v   b3_p     b3_v   b4_p     b4_v   b5_p  \\\n0  12.62   95142.0  12.61  26200.0  12.60  83500.0  12.59  15500.0  12.58   \n1  12.45  638300.0  12.44  95900.0  12.43  66000.0  12.42  59000.0  12.41   \n\n       b5_v  \n0  107600.0  \n1  217500.0"}
  suggestedFilename: "doc_JQDatadoc_9876_overview_获取股票集合竞价"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9876"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取股票集合竞价

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9876

## 描述

描述

## 内容

#### 获取股票集合竞价

- 历史范围：2005年至今；更新时间：盘后15点,24:00校对完成入库

```python
get_call_auction(security, start_date, end_date, fields=None)
```

描述

- 支持股票（2010年至今）的集合竞价，当日的集合竞价数据于盘后15点返回。
- 为了防止返回数据量过大, 我们每次最多返回10000行。

股票集合竞价字段

- security: 股票（2010年至今）
- start_date: 开始日期，YYYY-MM-DD格式
- end_date: 结束日期，YYYY-MM-DD格式
- fields: 选择要获取的行情数据字段，参数为list格式，默认为None，返回全部字段。

###### fields字段说明

- 返回指定时间区间标的集合竞价tick数据，返回字段结果如下：

| 字段名 | 说明 | 字段类型 |
| --- | --- | --- |
| time | 时间 | datetime |
| current | 当前价（不复权） | float |
| volume | 累计成交量（股） | float |
| money | 累计成交额（元） | float |
| a1_v~a5_v | 五档卖量 | float |
| a1_p~a5_p | 五档卖价 | float |
| b1_v~b5_v | 五档买量 | float |
| b1_p~b5_p | 五档买价 | float |

```python
#获取平安银行2019-09-02至2019-09-05期间的集合竞价数据
df=get_call_auction('000001.XSHE','2022-09-02','2022-09-05')
print(df)

          code                time  current    volume      money   a1_p  \
0  000001.XSHE 2022-09-02 09:25:00    12.62  369458.0  4662559.0  12.63   
1  000001.XSHE 2022-09-05 09:25:00    12.46  394700.0  4917962.0  12.46   

     a1_v   a2_p     a2_v   a3_p     a3_v   a4_p    a4_v   a5_p     a5_v  \
0  8200.0  12.64   5000.0  12.65  12900.0  12.66  4500.0  12.67   4900.0   
1  9355.0  12.47  28000.0  12.48  58100.0  12.49  4600.0  12.50  13400.0   

    b1_p      b1_v   b2_p     b2_v   b3_p     b3_v   b4_p     b4_v   b5_p  \
0  12.62   95142.0  12.61  26200.0  12.60  83500.0  12.59  15500.0  12.58   
1  12.45  638300.0  12.44  95900.0  12.43  66000.0  12.42  59000.0  12.41   

       b5_v  
0  107600.0  
1  217500.0
```
