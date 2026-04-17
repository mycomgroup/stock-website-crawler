---
id: "url-364967fa"
type: "website"
title: "批量获取alpha191因子（新）"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10535"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:43:52.746Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10535"
  headings:
    - {"level":3,"text":"批量获取alpha191因子（新）","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "参数"
    - "返回"
  lists:
    - {"type":"ul","items":["获取alpha191中所有的code和因子名称"]}
    - {"type":"ul","items":["date 日期","code 标的 code 字符串列表或者单个标的字符串, 默认为date日已上市未退市的全部标的","alpha 因子列表,如['alpha_001','alpha_002'.....] 默认为全部"]}
    - {"type":"ul","items":["返回 DataFrame ,index是标的名称, colume是因子名称"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"# 导入函数库\nfrom jqdatasdk import get_all_alpha_191\nget_all_alpha_191(date, code=None, alpha=None)"}
    - {"language":"python","code":"import pandas as pd\npd.set_option('display.max_rows', None)  \npd.set_option('display.max_columns', None)\n\nget_all_alpha_191(code=None,date='2023-07-20',alpha=None)[:5]\n\n\n             alpha_001  alpha_002  alpha_003  alpha_004  alpha_005  alpha_006  \\\n000004.XSHE   0.001883  -0.885735       5.52        1.0  -0.204124  -0.772038   \n000010.XSHE  -0.592623   0.522727       0.34       -1.0  -0.218218  -0.772038   \n000011.XSHE  -0.881874   1.384615       0.41       -1.0  -0.716115  -0.772038   \n000012.XSHE  -0.781107   1.000000       0.03       -1.0  -0.878070  -0.772038   \n000007.XSHE  -0.433969  -0.619048      -0.28       -1.0  -0.834280  -0.269446   \n\n             alpha_007  alpha_008     alpha_009  alpha_010     alpha_011  \\\n000004.XSHE   1.129669   0.025380 -1.000000e-08   0.663978 -4.746199e+07   \n000010.XSHE   0.547911   0.208633  0.000000e+00   0.035444  2.068642e+07   \n000011.XSHE   0.500772   0.187450  0.000000e+00   0.352847  3.789074e+06   \n000012.XSHE   0.638117   0.307554  0.000000e+00   0.193748 -3.648076e+06   \n000007.XSHE   0.363683   0.313549  0.000000e+00   0.153524 -1.354658e+06   \n\n\n....\n...."}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"批量获取alpha191因子（新）"}
    - {"type":"codeblock","language":"python","content":"# 导入函数库\nfrom jqdatasdk import get_all_alpha_191\nget_all_alpha_191(date, code=None, alpha=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取alpha191中所有的code和因子名称"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["date 日期","code 标的 code 字符串列表或者单个标的字符串, 默认为date日已上市未退市的全部标的","alpha 因子列表,如['alpha_001','alpha_002'.....] 默认为全部"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["返回 DataFrame ,index是标的名称, colume是因子名称"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"import pandas as pd\npd.set_option('display.max_rows', None)  \npd.set_option('display.max_columns', None)\n\nget_all_alpha_191(code=None,date='2023-07-20',alpha=None)[:5]\n\n\n             alpha_001  alpha_002  alpha_003  alpha_004  alpha_005  alpha_006  \\\n000004.XSHE   0.001883  -0.885735       5.52        1.0  -0.204124  -0.772038   \n000010.XSHE  -0.592623   0.522727       0.34       -1.0  -0.218218  -0.772038   \n000011.XSHE  -0.881874   1.384615       0.41       -1.0  -0.716115  -0.772038   \n000012.XSHE  -0.781107   1.000000       0.03       -1.0  -0.878070  -0.772038   \n000007.XSHE  -0.433969  -0.619048      -0.28       -1.0  -0.834280  -0.269446   \n\n             alpha_007  alpha_008     alpha_009  alpha_010     alpha_011  \\\n000004.XSHE   1.129669   0.025380 -1.000000e-08   0.663978 -4.746199e+07   \n000010.XSHE   0.547911   0.208633  0.000000e+00   0.035444  2.068642e+07   \n000011.XSHE   0.500772   0.187450  0.000000e+00   0.352847  3.789074e+06   \n000012.XSHE   0.638117   0.307554  0.000000e+00   0.193748 -3.648076e+06   \n000007.XSHE   0.363683   0.313549  0.000000e+00   0.153524 -1.354658e+06   \n\n\n....\n...."}
  suggestedFilename: "doc_JQDatadoc_10535_overview_批量获取alpha191因子（新）"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10535"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 批量获取alpha191因子（新）

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10535

## 描述

描述

## 内容

#### 批量获取alpha191因子（新）

```python
# 导入函数库
from jqdatasdk import get_all_alpha_191
get_all_alpha_191(date, code=None, alpha=None)
```

描述

- 获取alpha191中所有的code和因子名称

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

get_all_alpha_191(code=None,date='2023-07-20',alpha=None)[:5]

             alpha_001  alpha_002  alpha_003  alpha_004  alpha_005  alpha_006  \
000004.XSHE   0.001883  -0.885735       5.52        1.0  -0.204124  -0.772038   
000010.XSHE  -0.592623   0.522727       0.34       -1.0  -0.218218  -0.772038   
000011.XSHE  -0.881874   1.384615       0.41       -1.0  -0.716115  -0.772038   
000012.XSHE  -0.781107   1.000000       0.03       -1.0  -0.878070  -0.772038   
000007.XSHE  -0.433969  -0.619048      -0.28       -1.0  -0.834280  -0.269446   

             alpha_007  alpha_008     alpha_009  alpha_010     alpha_011  \
000004.XSHE   1.129669   0.025380 -1.000000e-08   0.663978 -4.746199e+07   
000010.XSHE   0.547911   0.208633  0.000000e+00   0.035444  2.068642e+07   
000011.XSHE   0.500772   0.187450  0.000000e+00   0.352847  3.789074e+06   
000012.XSHE   0.638117   0.307554  0.000000e+00   0.193748 -3.648076e+06   
000007.XSHE   0.363683   0.313549  0.000000e+00   0.153524 -1.354658e+06   

....
....
```
