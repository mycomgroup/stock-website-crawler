---
id: "url-36496439"
type: "website"
title: "风格因子pro"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10635"
description: "对描述因子和风格因子的数据分别进行正规化的处理，步骤如下："
source: ""
tags: []
crawl_time: "2026-03-27T09:09:02.734Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10635"
  headings:
    - {"level":2,"text":"风格因子pro","id":""}
  paragraphs:
    - "风格因子数据处理说明"
    - "对描述因子和风格因子的数据分别进行正规化的处理，步骤如下："
    - "风格因子pro在原有的风格因子基础上，对底层的因子进一步细分和扩充。目前仅jqdatasdk提供，如有需求可咨询运营开通"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；更新时间：下一自然日5点、8点"]}
    - {"type":"ul","items":["对描述因子分别进行去极值和标准化","对描述因子按照权重加权求和","对风格因子市值加权标准化","缺失值填充","对风格因子去极值，去极值方法同上面去极值描述"]}
  tables:
    - {"caption":"","headers":["因子 code","因子名称","简介"],"rows":[["btop","市净率因子","描述了股票估值高低不同而产生的收益差异, 即价值因子"],["divyild","分红因子","股票历史和预测的股息价格比的股票回报差异"],["earnqlty","盈利质量因子","股票收益因其收益的应计部分而产生的差异"],["earnvar","盈利变动率因子","解释由于收益、销售额和现金流的可变性而导致的股票回报差异，以及分析师预测的收益与价格之比。"],["earnyild","收益因子","描述了由盈利收益导致的收益差异"],["financial_leverage","财务杠杆因子","描述了高杠杆股票与低杠杆股票之间的收益差异"],["invsqlty","投资能力因子","衡量当股票价格过高/过低时，公司对资产扩张/紧缩的的倾向以及管理观点"],["liquidty","流动性因子","解释了由股票相对的交易活跃度不同而产生的收益率差异"],["long_growth","长期成长因子","描述了对销售或盈利增长预期不同而产生的收益差异"],["ltrevrsl","长期反转因子","解释与长期股票价格行为相关的常见回报变化"],["market_beta","市场波动率因子","表征股票相对于市场的波动敏感度"],["market_size","市值规模因子","捕捉大盘股和小盘股之间的收益差异"],["midcap","中等市值因子","捕捉中等市值股票与大盘股或者小盘股之间的收益差异"],["profit","盈利能力因子","表征公司运营的效率，盈利能力指标的组合"],["relative_momentum","相对动量因子","解释与最近（12个月，滞后1个月）股价行为相关的股票回报的常见变化"],["resvol","残余波动率因子","捕捉股票回报的相对波动性，这种波动性不能用股票对市场回报的敏感性差异来解释（市场波动率因子）"]]}
  codeBlocks:
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import *\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"language":"python","code":"from jqdatasdk import get_factor_values\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['btop','divyild','earnqlty'], \n                                start_date='2022-01-01', end_date='2022-01-10')\nprint(factor_data['btop'])\n\n            000001.XSHE\n2022-01-04     1.970804\n2022-01-05     1.840099\n2022-01-06     1.829950\n2022-01-07     1.800281\n2022-01-10     1.823760"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":2,"content":"风格因子pro"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；更新时间：下一自然日5点、8点"]}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import *\n# 取值函数\nget_factor_values(securities, factors, start_date, end_date, count)"}
    - {"type":"paragraph","content":"风格因子数据处理说明"}
    - {"type":"paragraph","content":"对描述因子和风格因子的数据分别进行正规化的处理，步骤如下："}
    - {"type":"list","listType":"ul","items":["对描述因子分别进行去极值和标准化","对描述因子按照权重加权求和","对风格因子市值加权标准化","缺失值填充","对风格因子去极值，去极值方法同上面去极值描述"]}
    - {"type":"paragraph","content":"风格因子pro在原有的风格因子基础上，对底层的因子进一步细分和扩充。目前仅jqdatasdk提供，如有需求可咨询运营开通"}
    - {"type":"table","headers":["因子 code","因子名称","简介"],"rows":[["btop","市净率因子","描述了股票估值高低不同而产生的收益差异, 即价值因子"],["divyild","分红因子","股票历史和预测的股息价格比的股票回报差异"],["earnqlty","盈利质量因子","股票收益因其收益的应计部分而产生的差异"],["earnvar","盈利变动率因子","解释由于收益、销售额和现金流的可变性而导致的股票回报差异，以及分析师预测的收益与价格之比。"],["earnyild","收益因子","描述了由盈利收益导致的收益差异"],["financial_leverage","财务杠杆因子","描述了高杠杆股票与低杠杆股票之间的收益差异"],["invsqlty","投资能力因子","衡量当股票价格过高/过低时，公司对资产扩张/紧缩的的倾向以及管理观点"],["liquidty","流动性因子","解释了由股票相对的交易活跃度不同而产生的收益率差异"],["long_growth","长期成长因子","描述了对销售或盈利增长预期不同而产生的收益差异"],["ltrevrsl","长期反转因子","解释与长期股票价格行为相关的常见回报变化"],["market_beta","市场波动率因子","表征股票相对于市场的波动敏感度"],["market_size","市值规模因子","捕捉大盘股和小盘股之间的收益差异"],["midcap","中等市值因子","捕捉中等市值股票与大盘股或者小盘股之间的收益差异"],["profit","盈利能力因子","表征公司运营的效率，盈利能力指标的组合"],["relative_momentum","相对动量因子","解释与最近（12个月，滞后1个月）股价行为相关的股票回报的常见变化"],["resvol","残余波动率因子","捕捉股票回报的相对波动性，这种波动性不能用股票对市场回报的敏感性差异来解释（市场波动率因子）"]]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import get_factor_values\nfactor_data = get_factor_values(securities=['000001.XSHE'], factors=['btop','divyild','earnqlty'], \n                                start_date='2022-01-01', end_date='2022-01-10')\nprint(factor_data['btop'])\n\n            000001.XSHE\n2022-01-04     1.970804\n2022-01-05     1.840099\n2022-01-06     1.829950\n2022-01-07     1.800281\n2022-01-10     1.823760"}
  suggestedFilename: "doc_JQDatadoc_10635_overview_风格因子pro"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10635"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 风格因子pro

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10635

## 描述

对描述因子和风格因子的数据分别进行正规化的处理，步骤如下：

## 内容

### 风格因子pro

- 历史范围：2005年至今；更新时间：下一自然日5点、8点

```python
# 导入函数库
from jqdatasdk import *
# 取值函数
get_factor_values(securities, factors, start_date, end_date, count)
```

风格因子数据处理说明

对描述因子和风格因子的数据分别进行正规化的处理，步骤如下：

- 对描述因子分别进行去极值和标准化
- 对描述因子按照权重加权求和
- 对风格因子市值加权标准化
- 缺失值填充
- 对风格因子去极值，去极值方法同上面去极值描述

风格因子pro在原有的风格因子基础上，对底层的因子进一步细分和扩充。目前仅jqdatasdk提供，如有需求可咨询运营开通

| 因子 code | 因子名称 | 简介 |
| --- | --- | --- |
| btop | 市净率因子 | 描述了股票估值高低不同而产生的收益差异, 即价值因子 |
| divyild | 分红因子 | 股票历史和预测的股息价格比的股票回报差异 |
| earnqlty | 盈利质量因子 | 股票收益因其收益的应计部分而产生的差异 |
| earnvar | 盈利变动率因子 | 解释由于收益、销售额和现金流的可变性而导致的股票回报差异，以及分析师预测的收益与价格之比。 |
| earnyild | 收益因子 | 描述了由盈利收益导致的收益差异 |
| financial_leverage | 财务杠杆因子 | 描述了高杠杆股票与低杠杆股票之间的收益差异 |
| invsqlty | 投资能力因子 | 衡量当股票价格过高/过低时，公司对资产扩张/紧缩的的倾向以及管理观点 |
| liquidty | 流动性因子 | 解释了由股票相对的交易活跃度不同而产生的收益率差异 |
| long_growth | 长期成长因子 | 描述了对销售或盈利增长预期不同而产生的收益差异 |
| ltrevrsl | 长期反转因子 | 解释与长期股票价格行为相关的常见回报变化 |
| market_beta | 市场波动率因子 | 表征股票相对于市场的波动敏感度 |
| market_size | 市值规模因子 | 捕捉大盘股和小盘股之间的收益差异 |
| midcap | 中等市值因子 | 捕捉中等市值股票与大盘股或者小盘股之间的收益差异 |
| profit | 盈利能力因子 | 表征公司运营的效率，盈利能力指标的组合 |
| relative_momentum | 相对动量因子 | 解释与最近（12个月，滞后1个月）股价行为相关的股票回报的常见变化 |
| resvol | 残余波动率因子 | 捕捉股票回报的相对波动性，这种波动性不能用股票对市场回报的敏感性差异来解释（市场波动率因子） |

```python
from jqdatasdk import get_factor_values
factor_data = get_factor_values(securities=['000001.XSHE'], factors=['btop','divyild','earnqlty'], 
                                start_date='2022-01-01', end_date='2022-01-10')
print(factor_data['btop'])

            000001.XSHE
2022-01-04     1.970804
2022-01-05     1.840099
2022-01-06     1.829950
2022-01-07     1.800281
2022-01-10     1.823760
```
