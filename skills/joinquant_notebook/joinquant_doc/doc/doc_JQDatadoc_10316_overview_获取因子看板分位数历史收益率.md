---
id: "url-36496fb9"
type: "website"
title: "获取因子看板分位数历史收益率"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10316"
description: "参数"
source: ""
tags: []
crawl_time: "2026-03-27T07:45:54.734Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10316"
  headings:
    - {"level":3,"text":"获取因子看板分位数历史收益率","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "参数"
    - "返回"
  lists:
    - {"type":"ul","items":["factor_names :因子名称，单个因子（字符串）或一个因子列表，支持的因子见聚宽因子库","universe_type : 股票池包括以下五种( 默认为'hs300')： 'hs300': 沪深300 'zz500': 中证500 'zz800': 中证800 'zz1000': 中证1000 'zzqz': 中证全指","start_date : 开始日期，字符串或 datetime 对象","end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日）","skip_paused : 是否跳过停牌，bool，默认为False","commision_fee : 手续费，float，0.0/0.0008/0.0018, 默认为0.0"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_factor_stats(factor_names=None, universe_type='hs300',\n                     start_date=None, end_date=None, count=None,\n                     skip_paused=False, commision_fee=0.0)"}
    - {"language":"python","code":"from jqdatasdk import *\ndata = get_factor_stats(factor_names=['PEG','VSTD20'] , end_date ='2022-09-20',count=5  )\nprint(data['PEG'])\n>>> {'PEG':                    1         2         3         4         5\n 2022-09-14  3.070544  2.847542  2.390142  1.978835  1.331841\n 2022-09-15  2.994605  2.796805  2.310998  1.938225  1.309742\n 2022-09-16  2.999703  2.814595  2.308664  1.940463  1.307399\n 2022-09-19  3.015146  2.813510  2.310971  1.942719  1.310100\n 2022-09-20  3.010017  2.810997  2.294774  1.920928  1.298267,\n 'VSTD20':                    1         2         3         4         5\n 2022-09-14  3.963227  2.854103  2.774518  2.034258  1.146730\n 2022-09-15  3.885976  2.795398  2.719512  1.977875  1.112380\n 2022-09-16  3.885621  2.785908  2.721697  1.985330  1.110787\n 2022-09-19  3.886508  2.801825  2.710205  1.986811  1.112331\n 2022-09-20  3.853822  2.763628  2.694442  1.985192  1.112072}"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取因子看板分位数历史收益率"}
    - {"type":"codeblock","language":"python","content":"get_factor_stats(factor_names=None, universe_type='hs300',\n                     start_date=None, end_date=None, count=None,\n                     skip_paused=False, commision_fee=0.0)"}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["factor_names :因子名称，单个因子（字符串）或一个因子列表，支持的因子见聚宽因子库","universe_type : 股票池包括以下五种( 默认为'hs300')： 'hs300': 沪深300 'zz500': 中证500 'zz800': 中证800 'zz1000': 中证1000 'zzqz': 中证全指","start_date : 开始日期，字符串或 datetime 对象","end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用","count: 截止 end_date 之前交易日的数量（含 end_date 当日）","skip_paused : 是否跳过停牌，bool，默认为False","commision_fee : 手续费，float，0.0/0.0008/0.0018, 默认为0.0"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\ndata = get_factor_stats(factor_names=['PEG','VSTD20'] , end_date ='2022-09-20',count=5  )\nprint(data['PEG'])\n>>> {'PEG':                    1         2         3         4         5\n 2022-09-14  3.070544  2.847542  2.390142  1.978835  1.331841\n 2022-09-15  2.994605  2.796805  2.310998  1.938225  1.309742\n 2022-09-16  2.999703  2.814595  2.308664  1.940463  1.307399\n 2022-09-19  3.015146  2.813510  2.310971  1.942719  1.310100\n 2022-09-20  3.010017  2.810997  2.294774  1.920928  1.298267,\n 'VSTD20':                    1         2         3         4         5\n 2022-09-14  3.963227  2.854103  2.774518  2.034258  1.146730\n 2022-09-15  3.885976  2.795398  2.719512  1.977875  1.112380\n 2022-09-16  3.885621  2.785908  2.721697  1.985330  1.110787\n 2022-09-19  3.886508  2.801825  2.710205  1.986811  1.112331\n 2022-09-20  3.853822  2.763628  2.694442  1.985192  1.112072}"}
  suggestedFilename: "doc_JQDatadoc_10316_overview_获取因子看板分位数历史收益率"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10316"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取因子看板分位数历史收益率

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10316

## 描述

参数

## 内容

#### 获取因子看板分位数历史收益率

```python
get_factor_stats(factor_names=None, universe_type='hs300',
                     start_date=None, end_date=None, count=None,
                     skip_paused=False, commision_fee=0.0)
```

参数

- factor_names :因子名称，单个因子（字符串）或一个因子列表，支持的因子见聚宽因子库
- universe_type : 股票池包括以下五种( 默认为'hs300')： 'hs300': 沪深300 'zz500': 中证500 'zz800': 中证800 'zz1000': 中证1000 'zzqz': 中证全指
- start_date : 开始日期，字符串或 datetime 对象
- end_date : 结束日期，字符串或 datetime 对象，可以与 start_date 或 count 配合使用
- count: 截止 end_date 之前交易日的数量（含 end_date 当日）
- skip_paused : 是否跳过停牌，bool，默认为False
- commision_fee : 手续费，float，0.0/0.0008/0.0018, 默认为0.0

返回

###### 示例

```python
from jqdatasdk import *
data = get_factor_stats(factor_names=['PEG','VSTD20'] , end_date ='2022-09-20',count=5  )
print(data['PEG'])
>>> {'PEG':                    1         2         3         4         5
 2022-09-14  3.070544  2.847542  2.390142  1.978835  1.331841
 2022-09-15  2.994605  2.796805  2.310998  1.938225  1.309742
 2022-09-16  2.999703  2.814595  2.308664  1.940463  1.307399
 2022-09-19  3.015146  2.813510  2.310971  1.942719  1.310100
 2022-09-20  3.010017  2.810997  2.294774  1.920928  1.298267,
 'VSTD20':                    1         2         3         4         5
 2022-09-14  3.963227  2.854103  2.774518  2.034258  1.146730
 2022-09-15  3.885976  2.795398  2.719512  1.977875  1.112380
 2022-09-16  3.885621  2.785908  2.721697  1.985330  1.110787
 2022-09-19  3.886508  2.801825  2.710205  1.986811  1.112331
 2022-09-20  3.853822  2.763628  2.694442  1.985192  1.112072}
```
