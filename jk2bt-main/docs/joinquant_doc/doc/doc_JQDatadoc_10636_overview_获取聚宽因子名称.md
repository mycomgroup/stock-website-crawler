---
id: "url-36496438"
type: "website"
title: "获取聚宽因子名称"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10636"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T09:09:06.682Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10636"
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
    - {"language":"python","code":"from jqdatasdk import *\ndf=get_all_factors()\nprint(df[df.category.str.contains('style_pro')])\n\n                 factor factor_intro   category category_intro\n244                btop        市净率因子  style_pro   风险因子 - 新风格因子\n245             divyild         分红因子  style_pro   风险因子 - 新风格因子\n246            earnqlty       盈利质量因子  style_pro   风险因子 - 新风格因子\n247             earnvar      盈利变动率因子  style_pro   风险因子 - 新风格因子\n248            earnyild         收益因子  style_pro   风险因子 - 新风格因子\n249  financial_leverage       财务杠杆因子  style_pro   风险因子 - 新风格因子\n250            invsqlty       投资能力因子  style_pro   风险因子 - 新风格因子\n251            liquidty        流动性因子  style_pro   风险因子 - 新风格因子\n252         long_growth       长期成长因子  style_pro   风险因子 - 新风格因子\n253            ltrevrsl       长期反转因子  style_pro   风险因子 - 新风格因子\n254         market_beta      市场波动率因子  style_pro   风险因子 - 新风格因子\n255         market_size       市值规模因子  style_pro   风险因子 - 新风格因子\n256              midcap       中等市值因子  style_pro   风险因子 - 新风格因子\n257              profit       盈利能力因子  style_pro   风险因子 - 新风格因子\n258   relative_momentum       相对动量因子  style_pro   风险因子 - 新风格因子\n259              resvol      残余波动率因子  style_pro   风险因子 - 新风格因子"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取聚宽因子名称"}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import *\nget_all_factors()"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取聚宽因子库中所有的因子code和因子名称","详细介绍:函数计算公式、API 调用方法，输入输出值详情请见:数据字典 - 聚宽因子","【风险因子-新风格因子】目前正在调试中，未正式上线，敬请期待"]}
    - {"type":"list","listType":"ul","items":["无"]}
    - {"type":"list","listType":"ul","items":["pandas.DataFrame","factor:因子code","factor_intro:因子说明","category:因子分类名称","category_intro:因子分类说明"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\ndf=get_all_factors()\nprint(df[df.category.str.contains('style_pro')])\n\n                 factor factor_intro   category category_intro\n244                btop        市净率因子  style_pro   风险因子 - 新风格因子\n245             divyild         分红因子  style_pro   风险因子 - 新风格因子\n246            earnqlty       盈利质量因子  style_pro   风险因子 - 新风格因子\n247             earnvar      盈利变动率因子  style_pro   风险因子 - 新风格因子\n248            earnyild         收益因子  style_pro   风险因子 - 新风格因子\n249  financial_leverage       财务杠杆因子  style_pro   风险因子 - 新风格因子\n250            invsqlty       投资能力因子  style_pro   风险因子 - 新风格因子\n251            liquidty        流动性因子  style_pro   风险因子 - 新风格因子\n252         long_growth       长期成长因子  style_pro   风险因子 - 新风格因子\n253            ltrevrsl       长期反转因子  style_pro   风险因子 - 新风格因子\n254         market_beta      市场波动率因子  style_pro   风险因子 - 新风格因子\n255         market_size       市值规模因子  style_pro   风险因子 - 新风格因子\n256              midcap       中等市值因子  style_pro   风险因子 - 新风格因子\n257              profit       盈利能力因子  style_pro   风险因子 - 新风格因子\n258   relative_momentum       相对动量因子  style_pro   风险因子 - 新风格因子\n259              resvol      残余波动率因子  style_pro   风险因子 - 新风格因子"}
  suggestedFilename: "doc_JQDatadoc_10636_overview_获取聚宽因子名称"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10636"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取聚宽因子名称

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10636

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
df=get_all_factors()
print(df[df.category.str.contains('style_pro')])

                 factor factor_intro   category category_intro
244                btop        市净率因子  style_pro   风险因子 - 新风格因子
245             divyild         分红因子  style_pro   风险因子 - 新风格因子
246            earnqlty       盈利质量因子  style_pro   风险因子 - 新风格因子
247             earnvar      盈利变动率因子  style_pro   风险因子 - 新风格因子
248            earnyild         收益因子  style_pro   风险因子 - 新风格因子
249  financial_leverage       财务杠杆因子  style_pro   风险因子 - 新风格因子
250            invsqlty       投资能力因子  style_pro   风险因子 - 新风格因子
251            liquidty        流动性因子  style_pro   风险因子 - 新风格因子
252         long_growth       长期成长因子  style_pro   风险因子 - 新风格因子
253            ltrevrsl       长期反转因子  style_pro   风险因子 - 新风格因子
254         market_beta      市场波动率因子  style_pro   风险因子 - 新风格因子
255         market_size       市值规模因子  style_pro   风险因子 - 新风格因子
256              midcap       中等市值因子  style_pro   风险因子 - 新风格因子
257              profit       盈利能力因子  style_pro   风险因子 - 新风格因子
258   relative_momentum       相对动量因子  style_pro   风险因子 - 新风格因子
259              resvol      残余波动率因子  style_pro   风险因子 - 新风格因子
```
