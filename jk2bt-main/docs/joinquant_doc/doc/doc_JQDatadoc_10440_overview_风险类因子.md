---
id: "url-36496ba1"
type: "website"
title: "风险类因子"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10440"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:46:34.270Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10440"
  headings:
    - {"level":3,"text":"风险类因子","id":""}
  paragraphs:
    - "描述"
    - "参数"
  lists:
    - {"type":"ul","items":["获取风险类因子值"]}
    - {"type":"ul","items":["为保证数据的连续性，所有数据基于后复权计算","为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个"]}
    - {"type":"ul","items":["securities:股票池，单只股票（字符串）或一个股票列表","factors: 因子名称，单个因子（字符串）或一个因子列表","start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一","end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一"]}
    - {"type":"ul","items":["一个 dict： key 是因子名称， value 是 pandas.dataframe。","dataframe 的 index 是日期， column 是股票代码， value 是因子值"]}
  tables:
    - {"caption":"","headers":["因子 code","因子名称","计算方法"],"rows":[["Variance20","20日年化收益方差","20日年化收益方差"],["Skewness20","个股收益的20日偏度","个股收益的20日偏度"],["Kurtosis20","个股收益的20日峰度","个股收益的20日峰度"],["sharpe_ratio_20","20日夏普比率","（Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差）"],["Variance60","60日年化收益方差","60日年化收益方差"],["Skewness60","个股收益的60日偏度","个股收益的60日偏度"],["Kurtosis60","个股收益的60日峰度","个股收益的60日峰度"],["sharpe_ratio_60","60日夏普比率","（Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差）"],["Variance120","120日年化收益方差","120日年化收益方差"],["Skewness120","个股收益的120日偏度","个股收益的120日偏度"],["Kurtosis120","个股收益的120日峰度","个股收益的120日峰度"],["sharpe_ratio_120","120日夏普比率","（Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差）"],["示例","",""]]}
  codeBlocks:
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import *\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"language":"python","code":"from jqdatasdk import get_factor_values\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['Variance20','Skewness20','Kurtosis20'],start_date='2022-01-01', end_date='2022-01-10')\n\n# 查看因子值\nprint(factor_data['Kurtosis20'])"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"风险类因子"}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import *\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取风险类因子值"]}
    - {"type":"list","listType":"ul","items":["为保证数据的连续性，所有数据基于后复权计算","为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["securities:股票池，单只股票（字符串）或一个股票列表","factors: 因子名称，单个因子（字符串）或一个因子列表","start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一","end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一"]}
    - {"type":"list","listType":"ul","items":["一个 dict： key 是因子名称， value 是 pandas.dataframe。","dataframe 的 index 是日期， column 是股票代码， value 是因子值"]}
    - {"type":"table","headers":["因子 code","因子名称","计算方法"],"rows":[["Variance20","20日年化收益方差","20日年化收益方差"],["Skewness20","个股收益的20日偏度","个股收益的20日偏度"],["Kurtosis20","个股收益的20日峰度","个股收益的20日峰度"],["sharpe_ratio_20","20日夏普比率","（Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差）"],["Variance60","60日年化收益方差","60日年化收益方差"],["Skewness60","个股收益的60日偏度","个股收益的60日偏度"],["Kurtosis60","个股收益的60日峰度","个股收益的60日峰度"],["sharpe_ratio_60","60日夏普比率","（Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差）"],["Variance120","120日年化收益方差","120日年化收益方差"],["Skewness120","个股收益的120日偏度","个股收益的120日偏度"],["Kurtosis120","个股收益的120日峰度","个股收益的120日峰度"],["sharpe_ratio_120","120日夏普比率","（Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差）"],["示例","",""]]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import get_factor_values\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['Variance20','Skewness20','Kurtosis20'],start_date='2022-01-01', end_date='2022-01-10')\n\n# 查看因子值\nprint(factor_data['Kurtosis20'])"}
  suggestedFilename: "doc_JQDatadoc_10440_overview_风险类因子"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10440"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 风险类因子

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10440

## 描述

描述

## 内容

#### 风险类因子

```python
# 导入函数库
from jqdatasdk import *
# 取值函数
get_factor_values(securities, factors, start_date, end_date, count)
```

描述

- 获取风险类因子值

- 为保证数据的连续性，所有数据基于后复权计算
- 为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个

参数

- securities:股票池，单只股票（字符串）或一个股票列表
- factors: 因子名称，单个因子（字符串）或一个因子列表
- start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一
- end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用
- count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一

- 一个 dict： key 是因子名称， value 是 pandas.dataframe。
- dataframe 的 index 是日期， column 是股票代码， value 是因子值

| 因子 code | 因子名称 | 计算方法 |
| --- | --- | --- |
| Variance20 | 20日年化收益方差 | 20日年化收益方差 |
| Skewness20 | 个股收益的20日偏度 | 个股收益的20日偏度 |
| Kurtosis20 | 个股收益的20日峰度 | 个股收益的20日峰度 |
| sharpe_ratio_20 | 20日夏普比率 | （Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差） |
| Variance60 | 60日年化收益方差 | 60日年化收益方差 |
| Skewness60 | 个股收益的60日偏度 | 个股收益的60日偏度 |
| Kurtosis60 | 个股收益的60日峰度 | 个股收益的60日峰度 |
| sharpe_ratio_60 | 60日夏普比率 | （Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差） |
| Variance120 | 120日年化收益方差 | 120日年化收益方差 |
| Skewness120 | 个股收益的120日偏度 | 个股收益的120日偏度 |
| Kurtosis120 | 个股收益的120日峰度 | 个股收益的120日峰度 |
| sharpe_ratio_120 | 120日夏普比率 | （Rp - Rf）/Sigma p 其中，Rp是个股的年化收益率，Rf是无风险利率（在这里设置为0.04），Sigma p是个股的收益波动率（标准差） |
| 示例 |  |  |

```python
from jqdatasdk import get_factor_values
factor_data = get_factor_values(securities=['000001.XSHE'], factors=['Variance20','Skewness20','Kurtosis20'],start_date='2022-01-01', end_date='2022-01-10')

# 查看因子值
print(factor_data['Kurtosis20'])
```
