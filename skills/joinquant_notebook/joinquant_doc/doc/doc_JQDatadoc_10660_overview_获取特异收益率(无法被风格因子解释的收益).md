---
id: "url-364963e1"
type: "website"
title: "获取特异收益率(无法被风格因子解释的收益)"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10660"
description: "参数"
source: ""
tags: []
crawl_time: "2026-03-27T07:47:53.175Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10660"
  headings:
    - {"level":3,"text":"获取特异收益率(无法被风格因子解释的收益)","id":""}
    - {"level":4,"text":"示例：","id":"-1"}
  paragraphs:
    - "参数"
    - "注意:"
    - "返回"
  lists:
    - {"type":"ul","items":["security : 股票代码, 或者股票代码组成的list","start_date : 开始日期，字符串或 datetime 对象","end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日）","category : 风格因子分类, 可选 'style' 和 'style_pro', 默认 'style'","universe : 市场范围,默认为None代表全市场, 可选 : 'hs300': 沪深300 ; 'zz500': 中证500'; zz800': 中证800; 'zz1000':中证1000; 'zz2000':中证2000; 'zzqz':中证全指","industry : 行业选取, 默认为 'sw_l1',可选 : 'sw_l1':申万一级, 'jq_l1':聚宽一级; 为了避免混淆, factors 中的行业因子仅返回 industy 下的行业"]}
    - {"type":"ul","items":["当指定universe时，回归所用的风格因子有根据市场范围进行标准化等重新计算"]}
    - {"type":"ul","items":["个股被风格因子无法解释的那部分收益，即特质收益率"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_factor_specific_returns(security, start_date=None, end_date=None, count=None, category=\"style\",universe=None, industry='sw_l1')"}
    - {"language":"python","code":"from jqdatasdk import *\ndf = get_factor_specific_returns(['000001.XSHE','600000.XSHG'],end_date='2022-09-01',count=5,category='style_pro')\nprint(df)\n>>>         000001.XSHE  600000.XSHG\n2022-08-26     0.005033     0.003910\n2022-08-29    -0.004840    -0.003806\n2022-08-30    -0.002171    -0.002390\n2022-08-31     0.007849    -0.009216\n2022-09-01    -0.001498    -0.001936"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取特异收益率(无法被风格因子解释的收益)"}
    - {"type":"codeblock","language":"python","content":"get_factor_specific_returns(security, start_date=None, end_date=None, count=None, category=\"style\",universe=None, industry='sw_l1')"}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["security : 股票代码, 或者股票代码组成的list","start_date : 开始日期，字符串或 datetime 对象","end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日）","category : 风格因子分类, 可选 'style' 和 'style_pro', 默认 'style'","universe : 市场范围,默认为None代表全市场, 可选 : 'hs300': 沪深300 ; 'zz500': 中证500'; zz800': 中证800; 'zz1000':中证1000; 'zz2000':中证2000; 'zzqz':中证全指","industry : 行业选取, 默认为 'sw_l1',可选 : 'sw_l1':申万一级, 'jq_l1':聚宽一级; 为了避免混淆, factors 中的行业因子仅返回 industy 下的行业"]}
    - {"type":"paragraph","content":"注意:"}
    - {"type":"list","listType":"ul","items":["当指定universe时，回归所用的风格因子有根据市场范围进行标准化等重新计算"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["个股被风格因子无法解释的那部分收益，即特质收益率"]}
    - {"type":"heading","level":4,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\ndf = get_factor_specific_returns(['000001.XSHE','600000.XSHG'],end_date='2022-09-01',count=5,category='style_pro')\nprint(df)\n>>>         000001.XSHE  600000.XSHG\n2022-08-26     0.005033     0.003910\n2022-08-29    -0.004840    -0.003806\n2022-08-30    -0.002171    -0.002390\n2022-08-31     0.007849    -0.009216\n2022-09-01    -0.001498    -0.001936"}
  suggestedFilename: "doc_JQDatadoc_10660_overview_获取特异收益率(无法被风格因子解释的收益)"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10660"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取特异收益率(无法被风格因子解释的收益)

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10660

## 描述

参数

## 内容

#### 获取特异收益率(无法被风格因子解释的收益)

```python
get_factor_specific_returns(security, start_date=None, end_date=None, count=None, category="style",universe=None, industry='sw_l1')
```

参数

- security : 股票代码, 或者股票代码组成的list
- start_date : 开始日期，字符串或 datetime 对象
- end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用
- count: 截止 end_date 之前交易日的数量（含 end_date 当日）
- category : 风格因子分类, 可选 'style' 和 'style_pro', 默认 'style'
- universe : 市场范围,默认为None代表全市场, 可选 : 'hs300': 沪深300 ; 'zz500': 中证500'; zz800': 中证800; 'zz1000':中证1000; 'zz2000':中证2000; 'zzqz':中证全指
- industry : 行业选取, 默认为 'sw_l1',可选 : 'sw_l1':申万一级, 'jq_l1':聚宽一级; 为了避免混淆, factors 中的行业因子仅返回 industy 下的行业

注意:

- 当指定universe时，回归所用的风格因子有根据市场范围进行标准化等重新计算

返回

- 个股被风格因子无法解释的那部分收益，即特质收益率

##### 示例：

```python
from jqdatasdk import *
df = get_factor_specific_returns(['000001.XSHE','600000.XSHG'],end_date='2022-09-01',count=5,category='style_pro')
print(df)
>>>         000001.XSHE  600000.XSHG
2022-08-26     0.005033     0.003910
2022-08-29    -0.004840    -0.003806
2022-08-30    -0.002171    -0.002390
2022-08-31     0.007849    -0.009216
2022-09-01    -0.001498    -0.001936
```
