---
id: "url-36496bbf"
type: "website"
title: "获取聚宽因子名称"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10431"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:46:10.640Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10431"
  headings:
    - {"level":3,"text":"获取聚宽因子名称","id":""}
    - {"level":5,"text":"示例：","id":"-1"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["获取聚宽因子库中所有的因子code和因子名称","详细介绍:函数计算公式、API 调用方法，输入输出值详情请见:数据字典 - 聚宽因子","【风险因子-新风格因子】目前正在调试中，未正式上线，敬请期待"]}
    - {"type":"ul","items":["无"]}
    - {"type":"ul","items":["pandas.DataFrame","factor:因子code","factor_intro:因子说明","category:因子分类名称","category_intro:因子分类说明"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import *\nget_all_factors()"}
    - {"language":"python","code":"from jqdatasdk import *\n#获取聚宽因子库所有因子\ndf = get_all_factors()\nprint(df) \n\n\n                         factor factor_intro   category category_intro\n0    administration_expense_ttm      管理费用TTM     basics     基础科目及衍生类因子\n1     asset_impairment_loss_ttm    资产减值损失TTM     basics     基础科目及衍生类因子\n2      cash_flow_to_price_ratio       现金流市值比     basics     基础科目及衍生类因子\n3        circulating_market_cap         流通市值     basics     基础科目及衍生类因子\n4                          EBIT        息税前利润     basics     基础科目及衍生类因子\n..                          ...          ...        ...            ...\n255                        MAC5       5日移动均线  technical         技术指标因子\n256                       MAC60      60日移动均线  technical         技术指标因子\n257                       MACDC    平滑异同移动平均线  technical         技术指标因子\n258                       MFI14       资金流量指标  technical         技术指标因子\n259                 price_no_fq      不复权价格因子  technical         技术指标因子\n\n[260 rows x 4 columns]"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取聚宽因子名称"}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import *\nget_all_factors()"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取聚宽因子库中所有的因子code和因子名称","详细介绍:函数计算公式、API 调用方法，输入输出值详情请见:数据字典 - 聚宽因子","【风险因子-新风格因子】目前正在调试中，未正式上线，敬请期待"]}
    - {"type":"list","listType":"ul","items":["无"]}
    - {"type":"list","listType":"ul","items":["pandas.DataFrame","factor:因子code","factor_intro:因子说明","category:因子分类名称","category_intro:因子分类说明"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\n#获取聚宽因子库所有因子\ndf = get_all_factors()\nprint(df) \n\n\n                         factor factor_intro   category category_intro\n0    administration_expense_ttm      管理费用TTM     basics     基础科目及衍生类因子\n1     asset_impairment_loss_ttm    资产减值损失TTM     basics     基础科目及衍生类因子\n2      cash_flow_to_price_ratio       现金流市值比     basics     基础科目及衍生类因子\n3        circulating_market_cap         流通市值     basics     基础科目及衍生类因子\n4                          EBIT        息税前利润     basics     基础科目及衍生类因子\n..                          ...          ...        ...            ...\n255                        MAC5       5日移动均线  technical         技术指标因子\n256                       MAC60      60日移动均线  technical         技术指标因子\n257                       MACDC    平滑异同移动平均线  technical         技术指标因子\n258                       MFI14       资金流量指标  technical         技术指标因子\n259                 price_no_fq      不复权价格因子  technical         技术指标因子\n\n[260 rows x 4 columns]"}
  suggestedFilename: "doc_JQDatadoc_10431_overview_获取聚宽因子名称"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10431"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取聚宽因子名称

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10431

## 描述

描述

## 内容

#### 获取聚宽因子名称

```python
# 导入函数库
from jqdatasdk import *
get_all_factors()
```

描述

- 获取聚宽因子库中所有的因子code和因子名称
- 详细介绍:函数计算公式、API 调用方法，输入输出值详情请见:数据字典 - 聚宽因子
- 【风险因子-新风格因子】目前正在调试中，未正式上线，敬请期待

- pandas.DataFrame
- factor:因子code
- factor_intro:因子说明
- category:因子分类名称
- category_intro:因子分类说明

###### 示例：

```python
from jqdatasdk import *
#获取聚宽因子库所有因子
df = get_all_factors()
print(df) 

                         factor factor_intro   category category_intro
0    administration_expense_ttm      管理费用TTM     basics     基础科目及衍生类因子
1     asset_impairment_loss_ttm    资产减值损失TTM     basics     基础科目及衍生类因子
2      cash_flow_to_price_ratio       现金流市值比     basics     基础科目及衍生类因子
3        circulating_market_cap         流通市值     basics     基础科目及衍生类因子
4                          EBIT        息税前利润     basics     基础科目及衍生类因子
..                          ...          ...        ...            ...
255                        MAC5       5日移动均线  technical         技术指标因子
256                       MAC60      60日移动均线  technical         技术指标因子
257                       MACDC    平滑异同移动平均线  technical         技术指标因子
258                       MFI14       资金流量指标  technical         技术指标因子
259                 price_no_fq      不复权价格因子  technical         技术指标因子

[260 rows x 4 columns]
```
