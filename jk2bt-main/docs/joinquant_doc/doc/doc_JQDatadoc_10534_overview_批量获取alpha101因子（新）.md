---
id: "url-364967fb"
type: "website"
title: "批量获取alpha101因子（新）"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10534"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:43:48.826Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10534"
  headings:
    - {"level":3,"text":"批量获取alpha101因子（新）","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回"
  lists:
    - {"type":"ul","items":["获取alpha101中所有的code和因子名称"]}
    - {"type":"ul","items":["date 日期","code 标的 code 字符串列表或者单个标的字符串, 默认为date日已上市未退市的全部标的","alpha 因子列表,如['alpha_001','alpha_002'.....] 默认为全部"]}
    - {"type":"ul","items":["返回 DataFrame ,index是标的名称, colume是因子名称"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import get_all_alpha_101\nget_all_alpha_101(date, code=None, alpha=None)"}
    - {"language":"python","code":"import pandas as pd\npd.set_option('display.max_rows', None)  \npd.set_option('display.max_columns', None)\n\nget_all_alpha_101(code=None,date='2023-07-20',alpha=None)[:5]\n\n             alpha_001  alpha_002  alpha_003  alpha_004  alpha_005  alpha_006  \\\n000001.XSHE  -0.397467  -0.547174  -0.441010  -0.888889  -0.372487  -0.348236   \n000002.XSHE   0.232496  -0.895346   0.008940  -0.888889  -0.370538  -0.129153   \n000004.XSHE  -0.004089   0.451901   0.242697  -0.666667  -0.335587  -0.298457   \n000005.XSHE   0.232496   0.356102  -0.409565  -0.444444  -0.408287  -0.344957   \n000006.XSHE   0.423200  -0.681307  -0.016132  -1.000000  -0.505174  -0.244237   \n\n             alpha_007  alpha_008  alpha_009  alpha_010  alpha_011  alpha_012  \\\n000001.XSHE  -1.000000  -0.528328      -0.01   0.285572   0.076890      -0.01   \n000002.XSHE  -0.033333  -0.791792       0.02   0.353422   0.644826      -0.02   \n000004.XSHE  -0.950000  -0.959560      -0.48   0.079625   1.852289       0.48   \n000005.XSHE   0.150000  -0.705506       0.00   0.304131   0.524998       0.00   \n000006.XSHE  -0.350000  -0.725125      -0.03   0.243963   0.428006      -0.03   \n....\n...."}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"批量获取alpha101因子（新）"}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import get_all_alpha_101\nget_all_alpha_101(date, code=None, alpha=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取alpha101中所有的code和因子名称"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["date 日期","code 标的 code 字符串列表或者单个标的字符串, 默认为date日已上市未退市的全部标的","alpha 因子列表,如['alpha_001','alpha_002'.....] 默认为全部"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["返回 DataFrame ,index是标的名称, colume是因子名称"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"import pandas as pd\npd.set_option('display.max_rows', None)  \npd.set_option('display.max_columns', None)\n\nget_all_alpha_101(code=None,date='2023-07-20',alpha=None)[:5]\n\n             alpha_001  alpha_002  alpha_003  alpha_004  alpha_005  alpha_006  \\\n000001.XSHE  -0.397467  -0.547174  -0.441010  -0.888889  -0.372487  -0.348236   \n000002.XSHE   0.232496  -0.895346   0.008940  -0.888889  -0.370538  -0.129153   \n000004.XSHE  -0.004089   0.451901   0.242697  -0.666667  -0.335587  -0.298457   \n000005.XSHE   0.232496   0.356102  -0.409565  -0.444444  -0.408287  -0.344957   \n000006.XSHE   0.423200  -0.681307  -0.016132  -1.000000  -0.505174  -0.244237   \n\n             alpha_007  alpha_008  alpha_009  alpha_010  alpha_011  alpha_012  \\\n000001.XSHE  -1.000000  -0.528328      -0.01   0.285572   0.076890      -0.01   \n000002.XSHE  -0.033333  -0.791792       0.02   0.353422   0.644826      -0.02   \n000004.XSHE  -0.950000  -0.959560      -0.48   0.079625   1.852289       0.48   \n000005.XSHE   0.150000  -0.705506       0.00   0.304131   0.524998       0.00   \n000006.XSHE  -0.350000  -0.725125      -0.03   0.243963   0.428006      -0.03   \n....\n...."}
  suggestedFilename: "doc_JQDatadoc_10534_overview_批量获取alpha101因子（新）"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10534"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 批量获取alpha101因子（新）

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10534

## 描述

描述

## 内容

#### 批量获取alpha101因子（新）

```python
# 导入函数库
from jqdatasdk import get_all_alpha_101
get_all_alpha_101(date, code=None, alpha=None)
```

描述

- 获取alpha101中所有的code和因子名称

参数

- date 日期
- code 标的 code 字符串列表或者单个标的字符串, 默认为date日已上市未退市的全部标的
- alpha 因子列表,如['alpha_001','alpha_002'.....] 默认为全部

返回

- 返回 DataFrame ,index是标的名称, colume是因子名称

###### 示例：

```python
import pandas as pd
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)

get_all_alpha_101(code=None,date='2023-07-20',alpha=None)[:5]

             alpha_001  alpha_002  alpha_003  alpha_004  alpha_005  alpha_006  \
000001.XSHE  -0.397467  -0.547174  -0.441010  -0.888889  -0.372487  -0.348236   
000002.XSHE   0.232496  -0.895346   0.008940  -0.888889  -0.370538  -0.129153   
000004.XSHE  -0.004089   0.451901   0.242697  -0.666667  -0.335587  -0.298457   
000005.XSHE   0.232496   0.356102  -0.409565  -0.444444  -0.408287  -0.344957   
000006.XSHE   0.423200  -0.681307  -0.016132  -1.000000  -0.505174  -0.244237   

             alpha_007  alpha_008  alpha_009  alpha_010  alpha_011  alpha_012  \
000001.XSHE  -1.000000  -0.528328      -0.01   0.285572   0.076890      -0.01   
000002.XSHE  -0.033333  -0.791792       0.02   0.353422   0.644826      -0.02   
000004.XSHE  -0.950000  -0.959560      -0.48   0.079625   1.852289       0.48   
000005.XSHE   0.150000  -0.705506       0.00   0.304131   0.524998       0.00   
000006.XSHE  -0.350000  -0.725125      -0.03   0.243963   0.428006      -0.03   
....
....
```
