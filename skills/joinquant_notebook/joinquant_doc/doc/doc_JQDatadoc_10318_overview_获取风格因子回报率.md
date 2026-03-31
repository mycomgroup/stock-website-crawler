---
id: "url-36496fb7"
type: "website"
title: "获取风格因子回报率"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10318"
description: "参数"
source: ""
tags: []
crawl_time: "2026-03-27T07:29:40.524Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10318"
  headings:
    - {"level":3,"text":"获取风格因子回报率","id":""}
    - {"level":4,"text":"示例：","id":""}
  paragraphs:
    - "参数"
    - "注意:"
    - "返回"
  lists:
    - {"type":"ul","items":["factors : 因子名称，单个因子（字符串）或一个因子列表。 支持风格因子如\"size\" 支持申万/聚宽一级行业如 \"801010\"和\"HY001\", 以及国家因子 \"country\", 注意为了避免混淆, 风格因子仅支持传递 style 和 style_pro 中的一类，也可以指定因子分类('style'或'style_pro') 表示分类下的所有风格因子","start_date : 开始日期，字符串或 datetime 对象","end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日）","universe : 市场范围,默认为None代表全市场, 可选 : 'hs300': 沪深300 ; 'zz500': 中证500'; zz800': 中证800; 'zz1000':中证1000; 'zz2000':中证2000; 'zzqz':中证全指","industry : 行业选取, 默认为 'sw_l1',可选 : 'sw_l1':申万一级, 'jq_l1':聚宽一级; 为了避免混淆, factors 中的行业因子仅返回 industy 下的行业"]}
    - {"type":"ul","items":["当指定universe时，回归所用的风格因子有根据市场范围进行标准化等重新计算"]}
    - {"type":"ul","items":["一个 DataFrame, index 是日期, columns为因子名, 值为因子暴露收益率"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_factor_style_returns(factors=None, start_date=None,\n                             end_date=None, count=None,\n                             universe=None, industry='sw_l1')"}
    - {"language":"python","code":"#返回市值、贝塔、动量和申万行业中电器设备Ⅰ的风格暴露收益率\nfrom jqdatasdk import *\ndf = get_factor_style_returns(['size','beta','momentum','801730'] , end_date='2022-09-01',count=2)\nprint(df)\n>>>            momentum      size      beta\n2022-08-31 -0.006386  0.005105 -0.004319\n2022-09-01  0.001502 -0.002413 -0.002344"}
    - {"language":"python","code":"#返回各风格因子和行业的风格暴露收益率\nfactors=['size','beta','momentum']\nindustry=get_industries(name='sw_l1', date=\"2024-03-04\").index.tolist()\nfactors+=industry\ndf = get_factor_style_returns(factors , end_date='2024-03-04',count=2)\nprint(df)\n                size      beta  momentum    801740    801110    801160  \\\n2024-03-01 -0.000049  0.007306  0.001623  0.004321  0.005648 -0.005210   \n2024-03-04  0.001993  0.002615  0.006406 -0.003117  0.010871  0.010889   \n\n              801770    801010    801120    801750    801050    801890  \\\n2024-03-01  0.007611 -0.014258 -0.005887  0.013469 -0.001397  0.003204   \n2024-03-04  0.004516 -0.004206 -0.005126 -0.000859  0.003369  0.000285   \n\n              801950    801980    801970    801170    801710    801780  \\\n2024-03-01  0.011792 -0.011260  0.001416 -0.009285 -0.000874  0.002390   \n2024-03-04  0.009799  0.001316 -0.001012 -0.000165 -0.006680 -0.008169   \n\n              801960    801130    801180    801760    801200    801230  \\\n2024-03-01 -0.002266 -0.001771 -0.007426  0.006103 -0.000325 -0.002224   \n2024-03-04  0.016863  0.003803 -0.017994  0.001779 -0.003024 -0.006256   \n\n              801880    801140    801720    801080    801790    801030  \\\n2024-03-01 -0.004408 -0.007582 -0.005680  0.009736 -0.006065 -0.001757   \n2024-03-04 -0.012024 -0.004254 -0.006216  0.005643 -0.016220 -0.003845   \n\n              801210    801150    801730    801040  \n2024-03-01 -0.005916 -0.007509  0.002144 -0.004160  \n2024-03-04 -0.003953  0.014519  0.002164 -0.004327"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取风格因子回报率"}
    - {"type":"codeblock","language":"python","content":"get_factor_style_returns(factors=None, start_date=None,\n                             end_date=None, count=None,\n                             universe=None, industry='sw_l1')"}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["factors : 因子名称，单个因子（字符串）或一个因子列表。 支持风格因子如\"size\" 支持申万/聚宽一级行业如 \"801010\"和\"HY001\", 以及国家因子 \"country\", 注意为了避免混淆, 风格因子仅支持传递 style 和 style_pro 中的一类，也可以指定因子分类('style'或'style_pro') 表示分类下的所有风格因子","start_date : 开始日期，字符串或 datetime 对象","end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日）","universe : 市场范围,默认为None代表全市场, 可选 : 'hs300': 沪深300 ; 'zz500': 中证500'; zz800': 中证800; 'zz1000':中证1000; 'zz2000':中证2000; 'zzqz':中证全指","industry : 行业选取, 默认为 'sw_l1',可选 : 'sw_l1':申万一级, 'jq_l1':聚宽一级; 为了避免混淆, factors 中的行业因子仅返回 industy 下的行业"]}
    - {"type":"paragraph","content":"注意:"}
    - {"type":"list","listType":"ul","items":["当指定universe时，回归所用的风格因子有根据市场范围进行标准化等重新计算"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["一个 DataFrame, index 是日期, columns为因子名, 值为因子暴露收益率"]}
    - {"type":"heading","level":4,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"#返回市值、贝塔、动量和申万行业中电器设备Ⅰ的风格暴露收益率\nfrom jqdatasdk import *\ndf = get_factor_style_returns(['size','beta','momentum','801730'] , end_date='2022-09-01',count=2)\nprint(df)\n>>>            momentum      size      beta\n2022-08-31 -0.006386  0.005105 -0.004319\n2022-09-01  0.001502 -0.002413 -0.002344"}
    - {"type":"codeblock","language":"python","content":"#返回各风格因子和行业的风格暴露收益率\nfactors=['size','beta','momentum']\nindustry=get_industries(name='sw_l1', date=\"2024-03-04\").index.tolist()\nfactors+=industry\ndf = get_factor_style_returns(factors , end_date='2024-03-04',count=2)\nprint(df)\n                size      beta  momentum    801740    801110    801160  \\\n2024-03-01 -0.000049  0.007306  0.001623  0.004321  0.005648 -0.005210   \n2024-03-04  0.001993  0.002615  0.006406 -0.003117  0.010871  0.010889   \n\n              801770    801010    801120    801750    801050    801890  \\\n2024-03-01  0.007611 -0.014258 -0.005887  0.013469 -0.001397  0.003204   \n2024-03-04  0.004516 -0.004206 -0.005126 -0.000859  0.003369  0.000285   \n\n              801950    801980    801970    801170    801710    801780  \\\n2024-03-01  0.011792 -0.011260  0.001416 -0.009285 -0.000874  0.002390   \n2024-03-04  0.009799  0.001316 -0.001012 -0.000165 -0.006680 -0.008169   \n\n              801960    801130    801180    801760    801200    801230  \\\n2024-03-01 -0.002266 -0.001771 -0.007426  0.006103 -0.000325 -0.002224   \n2024-03-04  0.016863  0.003803 -0.017994  0.001779 -0.003024 -0.006256   \n\n              801880    801140    801720    801080    801790    801030  \\\n2024-03-01 -0.004408 -0.007582 -0.005680  0.009736 -0.006065 -0.001757   \n2024-03-04 -0.012024 -0.004254 -0.006216  0.005643 -0.016220 -0.003845   \n\n              801210    801150    801730    801040  \n2024-03-01 -0.005916 -0.007509  0.002144 -0.004160  \n2024-03-04 -0.003953  0.014519  0.002164 -0.004327"}
  suggestedFilename: "doc_JQDatadoc_10318_overview_获取风格因子回报率"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10318"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取风格因子回报率

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10318

## 描述

参数

## 内容

#### 获取风格因子回报率

```python
get_factor_style_returns(factors=None, start_date=None,
                             end_date=None, count=None,
                             universe=None, industry='sw_l1')
```

参数

- factors : 因子名称，单个因子（字符串）或一个因子列表。 支持风格因子如"size" 支持申万/聚宽一级行业如 "801010"和"HY001", 以及国家因子 "country", 注意为了避免混淆, 风格因子仅支持传递 style 和 style_pro 中的一类，也可以指定因子分类('style'或'style_pro') 表示分类下的所有风格因子
- start_date : 开始日期，字符串或 datetime 对象
- end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用
- count: 截止 end_date 之前交易日的数量（含 end_date 当日）
- universe : 市场范围,默认为None代表全市场, 可选 : 'hs300': 沪深300 ; 'zz500': 中证500'; zz800': 中证800; 'zz1000':中证1000; 'zz2000':中证2000; 'zzqz':中证全指
- industry : 行业选取, 默认为 'sw_l1',可选 : 'sw_l1':申万一级, 'jq_l1':聚宽一级; 为了避免混淆, factors 中的行业因子仅返回 industy 下的行业

注意:

- 当指定universe时，回归所用的风格因子有根据市场范围进行标准化等重新计算

返回

- 一个 DataFrame, index 是日期, columns为因子名, 值为因子暴露收益率

##### 示例：

```python
#返回市值、贝塔、动量和申万行业中电器设备Ⅰ的风格暴露收益率
from jqdatasdk import *
df = get_factor_style_returns(['size','beta','momentum','801730'] , end_date='2022-09-01',count=2)
print(df)
>>>            momentum      size      beta
2022-08-31 -0.006386  0.005105 -0.004319
2022-09-01  0.001502 -0.002413 -0.002344
```

```python
#返回各风格因子和行业的风格暴露收益率
factors=['size','beta','momentum']
industry=get_industries(name='sw_l1', date="2024-03-04").index.tolist()
factors+=industry
df = get_factor_style_returns(factors , end_date='2024-03-04',count=2)
print(df)
                size      beta  momentum    801740    801110    801160  \
2024-03-01 -0.000049  0.007306  0.001623  0.004321  0.005648 -0.005210   
2024-03-04  0.001993  0.002615  0.006406 -0.003117  0.010871  0.010889   

              801770    801010    801120    801750    801050    801890  \
2024-03-01  0.007611 -0.014258 -0.005887  0.013469 -0.001397  0.003204   
2024-03-04  0.004516 -0.004206 -0.005126 -0.000859  0.003369  0.000285   

              801950    801980    801970    801170    801710    801780  \
2024-03-01  0.011792 -0.011260  0.001416 -0.009285 -0.000874  0.002390   
2024-03-04  0.009799  0.001316 -0.001012 -0.000165 -0.006680 -0.008169   

              801960    801130    801180    801760    801200    801230  \
2024-03-01 -0.002266 -0.001771 -0.007426  0.006103 -0.000325 -0.002224   
2024-03-04  0.016863  0.003803 -0.017994  0.001779 -0.003024 -0.006256   

              801880    801140    801720    801080    801790    801030  \
2024-03-01 -0.004408 -0.007582 -0.005680  0.009736 -0.006065 -0.001757   
2024-03-04 -0.012024 -0.004254 -0.006216  0.005643 -0.016220 -0.003845   

              801210    801150    801730    801040  
2024-03-01 -0.005916 -0.007509  0.002144 -0.004160  
2024-03-04 -0.003953  0.014519  0.002164 -0.004327
```
