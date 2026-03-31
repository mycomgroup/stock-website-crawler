---
id: "url-36496bba"
type: "website"
title: "成长类因子"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10436"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:46:22.456Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10436"
  headings:
    - {"level":3,"text":"成长类因子","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "示例"
  lists:
    - {"type":"ul","items":["获取成长类因子值"]}
    - {"type":"ul","items":["为保证数据的连续性，所有数据基于后复权计算","为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个"]}
    - {"type":"ul","items":["securities:股票池，单只股票（字符串）或一个股票列表","factors: 因子名称，单个因子（字符串）或一个因子列表","start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一","end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一"]}
    - {"type":"ul","items":["一个 dict： key 是因子名称， value 是 pandas.dataframe。","dataframe 的 index 是日期， column 是股票代码， value 是因子值"]}
  tables:
    - {"caption":"","headers":["因子 code","因子名称","计算方法"],"rows":[["operating_revenue_growth_rate","营业收入增长率","营业收入增长率=（今年营业收入（TTM）/去年营业收入（TTM））-1"],["total_asset_growth_rate","总资产增长率","总资产 / 总资产_4 -1"],["net_operate_cashflow_growth_rate","经营活动产生的现金流量净额增长率","(今年经营活动产生的现金流量净额（TTM）/去年经营活动产生的现金流量净额（TTM）)-1"],["total_profit_growth_rate","利润总额增长率","利润总额增长率=(今年利润总额（TTM）/去年利润总额（TTM）)-1"],["np_parent_company_owners_growth_rate","归属母公司股东的净利润增长率","(今年归属于母公司所有者的净利润（TTM）/去年归属于母公司所有者的净利润（TTM）)-1"],["financing_cash_growth_rate","筹资活动产生的现金流量净额增长率","过去12个月的筹资现金流量净额 / 4季度前的12个月的筹资现金流量净额 - 1"],["net_profit_growth_rate","净利润增长率","净利润增长率=(今年净利润（TTM）/去年净利润（TTM）)-1"],["net_asset_growth_rate","净资产增长率","（当季的股东权益/三季度前的股东权益）-1"],["PEG","市盈率相对盈利增长比率","PEG = PE / (归母公司净利润(TTM)增长率 * 100) # 如果 PE 或 增长率为负，则为 nan"]]}
  codeBlocks:
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import *\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"language":"python","code":"from jqdatasdk import get_factor_values\n\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['operating_revenue_growth_rate','total_asset_growth_rate','net_operate_cashflow_growth_rate'], \n                                start_date='2022-01-01', end_date='2022-01-10')\n# 查看因子值\nprint(factor_data['net_operate_cashflow_growth_rate'])"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"成长类因子"}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import *\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取成长类因子值"]}
    - {"type":"list","listType":"ul","items":["为保证数据的连续性，所有数据基于后复权计算","为了防止单次返回数据时间过长，每次调用 api 请求的因子值不能超过 200000 个"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["securities:股票池，单只股票（字符串）或一个股票列表","factors: 因子名称，单个因子（字符串）或一个因子列表","start_date:开始日期，字符串或 datetime 对象，与 coun t参数二选一","end_date: 结束日期， 字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日），与 start_date 参数二选一"]}
    - {"type":"list","listType":"ul","items":["一个 dict： key 是因子名称， value 是 pandas.dataframe。","dataframe 的 index 是日期， column 是股票代码， value 是因子值"]}
    - {"type":"table","headers":["因子 code","因子名称","计算方法"],"rows":[["operating_revenue_growth_rate","营业收入增长率","营业收入增长率=（今年营业收入（TTM）/去年营业收入（TTM））-1"],["total_asset_growth_rate","总资产增长率","总资产 / 总资产_4 -1"],["net_operate_cashflow_growth_rate","经营活动产生的现金流量净额增长率","(今年经营活动产生的现金流量净额（TTM）/去年经营活动产生的现金流量净额（TTM）)-1"],["total_profit_growth_rate","利润总额增长率","利润总额增长率=(今年利润总额（TTM）/去年利润总额（TTM）)-1"],["np_parent_company_owners_growth_rate","归属母公司股东的净利润增长率","(今年归属于母公司所有者的净利润（TTM）/去年归属于母公司所有者的净利润（TTM）)-1"],["financing_cash_growth_rate","筹资活动产生的现金流量净额增长率","过去12个月的筹资现金流量净额 / 4季度前的12个月的筹资现金流量净额 - 1"],["net_profit_growth_rate","净利润增长率","净利润增长率=(今年净利润（TTM）/去年净利润（TTM）)-1"],["net_asset_growth_rate","净资产增长率","（当季的股东权益/三季度前的股东权益）-1"],["PEG","市盈率相对盈利增长比率","PEG = PE / (归母公司净利润(TTM)增长率 * 100) # 如果 PE 或 增长率为负，则为 nan"]]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import get_factor_values\n\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['operating_revenue_growth_rate','total_asset_growth_rate','net_operate_cashflow_growth_rate'], \n                                start_date='2022-01-01', end_date='2022-01-10')\n# 查看因子值\nprint(factor_data['net_operate_cashflow_growth_rate'])"}
  suggestedFilename: "doc_JQDatadoc_10436_overview_成长类因子"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10436"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 成长类因子

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10436

## 描述

描述

## 内容

#### 成长类因子

```python
# 导入函数库
from jqdatasdk import *
# 取值函数
get_factor_values(securities, factors, start_date, end_date, count)
```

描述

- 获取成长类因子值

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
| operating_revenue_growth_rate | 营业收入增长率 | 营业收入增长率=（今年营业收入（TTM）/去年营业收入（TTM））-1 |
| total_asset_growth_rate | 总资产增长率 | 总资产 / 总资产_4 -1 |
| net_operate_cashflow_growth_rate | 经营活动产生的现金流量净额增长率 | (今年经营活动产生的现金流量净额（TTM）/去年经营活动产生的现金流量净额（TTM）)-1 |
| total_profit_growth_rate | 利润总额增长率 | 利润总额增长率=(今年利润总额（TTM）/去年利润总额（TTM）)-1 |
| np_parent_company_owners_growth_rate | 归属母公司股东的净利润增长率 | (今年归属于母公司所有者的净利润（TTM）/去年归属于母公司所有者的净利润（TTM）)-1 |
| financing_cash_growth_rate | 筹资活动产生的现金流量净额增长率 | 过去12个月的筹资现金流量净额 / 4季度前的12个月的筹资现金流量净额 - 1 |
| net_profit_growth_rate | 净利润增长率 | 净利润增长率=(今年净利润（TTM）/去年净利润（TTM）)-1 |
| net_asset_growth_rate | 净资产增长率 | （当季的股东权益/三季度前的股东权益）-1 |
| PEG | 市盈率相对盈利增长比率 | PEG = PE / (归母公司净利润(TTM)增长率 * 100) # 如果 PE 或 增长率为负，则为 nan |

示例

```python
from jqdatasdk import get_factor_values

factor_data = get_factor_values(securities=['000001.XSHE'], factors=['operating_revenue_growth_rate','total_asset_growth_rate','net_operate_cashflow_growth_rate'], 
                                start_date='2022-01-01', end_date='2022-01-10')
# 查看因子值
print(factor_data['net_operate_cashflow_growth_rate'])
```
