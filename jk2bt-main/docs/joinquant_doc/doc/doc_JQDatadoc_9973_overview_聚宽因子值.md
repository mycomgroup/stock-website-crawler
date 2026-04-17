---
id: "url-7a226f0e"
type: "website"
title: "聚宽因子值"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9973"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T09:08:22.450Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9973"
  headings:
    - {"level":3,"text":"聚宽因子值","id":""}
    - {"level":5,"text":"示例：","id":"-1"}
  paragraphs:
    - "描述"
    - "参数"
  lists:
    - {"type":"ul","items":["获取聚宽因子库值","聚宽因子"]}
    - {"type":"ul","items":["为保证数据的连续性，所有数据基于后复权计算","为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个"]}
    - {"type":"ul","items":["用户如有需要使用聚宽因子的，请联系我们的运营同事。个人用户咨询微信号15815705123，机构服务咨询添加微信号JQData02"]}
    - {"type":"ul","items":["securities:股票池，单只股票（字符串）或一个股票列表","factors: 因子名称，单个因子（字符串）或一个因子列表","start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一","end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一"]}
    - {"type":"ul","items":["一个 dict： key 是因子名称， value 是 pandas.dataframe。","dataframe 的 index 是日期， column 是股票代码， value 是因子值"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import get_factor_values\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import get_factor_values\n\n# 获取因子Skewness60(个股收益的60日偏度)从 2017-01-01 至 2017-03-04 的因子值\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['Skewness60','DEGM','quick_ratio'], start_date='2017-01-01', end_date='2017-03-04')\n# 查看因子值\nprint(factor_data['Skewness60'][:5])\n\n            000001.XSHE\n2017-01-03    -0.002081\n2017-01-04     0.021962\n2017-01-05    -0.003263\n2017-01-06    -0.007545\n2017-01-09    -0.007441"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"聚宽因子值"}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import get_factor_values\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取聚宽因子库值","聚宽因子"]}
    - {"type":"list","listType":"ul","items":["为保证数据的连续性，所有数据基于后复权计算","为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个"]}
    - {"type":"list","listType":"ul","items":["用户如有需要使用聚宽因子的，请联系我们的运营同事。个人用户咨询微信号15815705123，机构服务咨询添加微信号JQData02"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["securities:股票池，单只股票（字符串）或一个股票列表","factors: 因子名称，单个因子（字符串）或一个因子列表","start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一","end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一"]}
    - {"type":"list","listType":"ul","items":["一个 dict： key 是因子名称， value 是 pandas.dataframe。","dataframe 的 index 是日期， column 是股票代码， value 是因子值"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import get_factor_values\n\n# 获取因子Skewness60(个股收益的60日偏度)从 2017-01-01 至 2017-03-04 的因子值\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['Skewness60','DEGM','quick_ratio'], start_date='2017-01-01', end_date='2017-03-04')\n# 查看因子值\nprint(factor_data['Skewness60'][:5])\n\n            000001.XSHE\n2017-01-03    -0.002081\n2017-01-04     0.021962\n2017-01-05    -0.003263\n2017-01-06    -0.007545\n2017-01-09    -0.007441"}
  suggestedFilename: "doc_JQDatadoc_9973_overview_聚宽因子值"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9973"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 聚宽因子值

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9973

## 描述

描述

## 内容

#### 聚宽因子值

```python
# 导入函数库
from jqdatasdk import get_factor_values
# 取值函数
get_factor_values(securities, factors, start_date, end_date, count)
```

描述

- 获取聚宽因子库值

- 为保证数据的连续性，所有数据基于后复权计算
- 为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个

- 用户如有需要使用聚宽因子的，请联系我们的运营同事。个人用户咨询微信号15815705123，机构服务咨询添加微信号JQData02

参数

- securities:股票池，单只股票（字符串）或一个股票列表
- factors: 因子名称，单个因子（字符串）或一个因子列表
- start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一
- end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用
- count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一

- 一个 dict： key 是因子名称， value 是 pandas.dataframe。
- dataframe 的 index 是日期， column 是股票代码， value 是因子值

###### 示例：

```python
# 导入函数库
from jqdatasdk import get_factor_values

# 获取因子Skewness60(个股收益的60日偏度)从 2017-01-01 至 2017-03-04 的因子值
factor_data = get_factor_values(securities=['000001.XSHE'], factors=['Skewness60','DEGM','quick_ratio'], start_date='2017-01-01', end_date='2017-03-04')
# 查看因子值
print(factor_data['Skewness60'][:5])

            000001.XSHE
2017-01-03    -0.002081
2017-01-04     0.021962
2017-01-05    -0.003263
2017-01-06    -0.007545
2017-01-09    -0.007441
```
