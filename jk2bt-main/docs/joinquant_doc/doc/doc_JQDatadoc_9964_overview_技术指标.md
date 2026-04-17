---
id: "url-7a226ef0"
type: "website"
title: "技术指标"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9964"
description: "更新方式"
source: ""
tags: []
crawl_time: "2026-03-27T07:16:34.668Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9964"
  headings:
    - {"level":3,"text":"技术指标","id":""}
    - {"level":5,"text":"技术指标汇总","id":"-1"}
    - {"level":5,"text":"示例：","id":"-2"}
  paragraphs:
    - "更新方式"
  lists:
    - {"type":"ul","items":["技术指标 —— 2005至今,支持设置复权基准日（fq_ref_date 参数），实时计算","详细介绍：函数计算公式、API 调用方法，用法注释， 输入输出值详情请见:[数据 - 技术分析指标]"]}
  tables:
    - {"caption":"","headers":["类型","指标","类型","指标","类型","指标","类型","指标"],"rows":[["超买超卖型","ACCER-幅度涨速ADTM-动态买卖气指标ATR-真实波幅BIAS-乖离率BIAS_QL-乖离率_传统版BIAS_36-三六乖离CCI-商品路径指标CYF-市场能量DKX-多空线KD-随机指标KDKDJ-随机指标SKDJ-慢速随机指标MFI-资金流量指标MTM-动量线ROC-变动率指标RSI-相对强弱指标MARSI-相对强弱平均线OSC-变动速率线UDL-引力线WR-威廉指标LWR-LWR威廉指标TAPI-加权指数成交值FSL-分水岭","趋势型","CHO-佳庆指标CYE-市场趋势DBQR-对比强弱DMA-平均差DMI - 趋向指标DPO-区间震荡线EMV-简易波动指标GDX-鬼道线JLHB-绝路航标JS-加速线MACD-平滑异同平均QACD-快速异同平均QR-强弱指标TRIX-终极指标UOS-终极指标VMACD-量平滑移动平均VPT-量价曲线WVAD-威廉变异离散量","能量型","BRAR-情绪指标CR-带状能量线CYR-市场强弱MASS-梅斯线PCNT-幅度比PSY-心理线VR-成交量变异率","成交量型","AMO-成交金额CCL-持仓量（适用于期货）DBLB-对比量比DBQRV-对比强弱量OBV-累积能量线VOL-成交量VRSI-相对强弱量LB-量比"],["均线型","AMV-成本价均线ALLIGAT-鳄鱼线BBI-多空均线EXPMA-指数平均线BBIBOLL-多空布林线MA-均线HMA-高价平均线LMA-低价平均线 VMA-变异平均线","路径型","BOLL-布林线ENE-轨道线MIKE-麦克支撑压力PBX-瀑布线XS-薛斯通道XS2-薛斯通道2","其他型","EMA-指数移动平均SMA-移动平均BDZX-波段之星CDP-STD-逆势操作CJDX-超级短线CYHT-财运亨通JAX-济安线JFZX-飓风智能中线JYJL-交易参考均量LHXJ-猎狐先觉LYJH-猎鹰歼狐TBP-STD-趋势平衡点ZBCD-准备抄底","特色型","AROON-阿隆指标CFJT-财富阶梯ZSDB-指数对比"],["神系","SG-SMX-生命线SG-LB-量比SG-PF-强势股评分XDT-心电图","龙系","ZLMM-主力买卖RAD-威力雷达SHT-龙系短线","鬼系","CYW-主力控盘CYS-市场盈亏","图表型","ZX-重心线PUCU-逆时钟曲线"]]}
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk.technical_analysis import *"}
    - {"language":"python","code":"# 导入技术分析指标库\nfrom jqdatasdk import *\nfrom jqdatasdk.technical_analysis import *\n\n\n# 定义股票池列表\nsecurity_list1 = '000001.XSHE'\nsecurity_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']\n\n\n# 计算并输出 security_list1 的 GDX 值，分别返回：济安线、压力线和支撑线的值。\ngdx_jax, gdx_ylx, gdx_zcx = GDX(security_list1,check_date='2017-01-04', N = 30, M = 9)\nprint (gdx_jax[security_list1])\nprint (gdx_ylx[security_list1])\nprint (gdx_zcx[security_list1])\n\n# 输出 security_list2 的 GDX 值\ngdx_jax, gdx_ylx, gdx_zcx = GDX(security_list2,check_date='2017-01-04', N = 30, M = 9)\nfor stock in security_list2:\n    print (gdx_jax[stock])\n    print (gdx_ylx[stock])\n    print (gdx_zcx[stock])\n\n8.29159727600139\n9.037841030841516\n7.545353521161265\n8.29159727600139\n9.037841030841516\n7.545353521161265\n15.528491778666732\n16.92605603874674\n14.130927518586727\n15.359770622508778\n16.74214997853457\n13.977391266482988\nnan\nnan\nnan"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"技术指标"}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk.technical_analysis import *"}
    - {"type":"paragraph","content":"更新方式"}
    - {"type":"list","listType":"ul","items":["技术指标 —— 2005至今,支持设置复权基准日（fq_ref_date 参数），实时计算","详细介绍：函数计算公式、API 调用方法，用法注释， 输入输出值详情请见:[数据 - 技术分析指标]"]}
    - {"type":"heading","level":5,"content":"技术指标汇总"}
    - {"type":"table","headers":["类型","指标","类型","指标","类型","指标","类型","指标"],"rows":[["超买超卖型","ACCER-幅度涨速ADTM-动态买卖气指标ATR-真实波幅BIAS-乖离率BIAS_QL-乖离率_传统版BIAS_36-三六乖离CCI-商品路径指标CYF-市场能量DKX-多空线KD-随机指标KDKDJ-随机指标SKDJ-慢速随机指标MFI-资金流量指标MTM-动量线ROC-变动率指标RSI-相对强弱指标MARSI-相对强弱平均线OSC-变动速率线UDL-引力线WR-威廉指标LWR-LWR威廉指标TAPI-加权指数成交值FSL-分水岭","趋势型","CHO-佳庆指标CYE-市场趋势DBQR-对比强弱DMA-平均差DMI - 趋向指标DPO-区间震荡线EMV-简易波动指标GDX-鬼道线JLHB-绝路航标JS-加速线MACD-平滑异同平均QACD-快速异同平均QR-强弱指标TRIX-终极指标UOS-终极指标VMACD-量平滑移动平均VPT-量价曲线WVAD-威廉变异离散量","能量型","BRAR-情绪指标CR-带状能量线CYR-市场强弱MASS-梅斯线PCNT-幅度比PSY-心理线VR-成交量变异率","成交量型","AMO-成交金额CCL-持仓量（适用于期货）DBLB-对比量比DBQRV-对比强弱量OBV-累积能量线VOL-成交量VRSI-相对强弱量LB-量比"],["均线型","AMV-成本价均线ALLIGAT-鳄鱼线BBI-多空均线EXPMA-指数平均线BBIBOLL-多空布林线MA-均线HMA-高价平均线LMA-低价平均线 VMA-变异平均线","路径型","BOLL-布林线ENE-轨道线MIKE-麦克支撑压力PBX-瀑布线XS-薛斯通道XS2-薛斯通道2","其他型","EMA-指数移动平均SMA-移动平均BDZX-波段之星CDP-STD-逆势操作CJDX-超级短线CYHT-财运亨通JAX-济安线JFZX-飓风智能中线JYJL-交易参考均量LHXJ-猎狐先觉LYJH-猎鹰歼狐TBP-STD-趋势平衡点ZBCD-准备抄底","特色型","AROON-阿隆指标CFJT-财富阶梯ZSDB-指数对比"],["神系","SG-SMX-生命线SG-LB-量比SG-PF-强势股评分XDT-心电图","龙系","ZLMM-主力买卖RAD-威力雷达SHT-龙系短线","鬼系","CYW-主力控盘CYS-市场盈亏","图表型","ZX-重心线PUCU-逆时钟曲线"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 导入技术分析指标库\nfrom jqdatasdk import *\nfrom jqdatasdk.technical_analysis import *\n\n\n# 定义股票池列表\nsecurity_list1 = '000001.XSHE'\nsecurity_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']\n\n\n# 计算并输出 security_list1 的 GDX 值，分别返回：济安线、压力线和支撑线的值。\ngdx_jax, gdx_ylx, gdx_zcx = GDX(security_list1,check_date='2017-01-04', N = 30, M = 9)\nprint (gdx_jax[security_list1])\nprint (gdx_ylx[security_list1])\nprint (gdx_zcx[security_list1])\n\n# 输出 security_list2 的 GDX 值\ngdx_jax, gdx_ylx, gdx_zcx = GDX(security_list2,check_date='2017-01-04', N = 30, M = 9)\nfor stock in security_list2:\n    print (gdx_jax[stock])\n    print (gdx_ylx[stock])\n    print (gdx_zcx[stock])\n\n8.29159727600139\n9.037841030841516\n7.545353521161265\n8.29159727600139\n9.037841030841516\n7.545353521161265\n15.528491778666732\n16.92605603874674\n14.130927518586727\n15.359770622508778\n16.74214997853457\n13.977391266482988\nnan\nnan\nnan"}
  suggestedFilename: "doc_JQDatadoc_9964_overview_技术指标"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9964"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 技术指标

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9964

## 描述

更新方式

## 内容

#### 技术指标

```python
from jqdatasdk.technical_analysis import *
```

更新方式

- 技术指标 —— 2005至今,支持设置复权基准日（fq_ref_date 参数），实时计算
- 详细介绍：函数计算公式、API 调用方法，用法注释， 输入输出值详情请见:[数据 - 技术分析指标]

###### 技术指标汇总

| 类型 | 指标 | 类型 | 指标 | 类型 | 指标 | 类型 | 指标 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 超买超卖型 | ACCER-幅度涨速ADTM-动态买卖气指标ATR-真实波幅BIAS-乖离率BIAS_QL-乖离率_传统版BIAS_36-三六乖离CCI-商品路径指标CYF-市场能量DKX-多空线KD-随机指标KDKDJ-随机指标SKDJ-慢速随机指标MFI-资金流量指标MTM-动量线ROC-变动率指标RSI-相对强弱指标MARSI-相对强弱平均线OSC-变动速率线UDL-引力线WR-威廉指标LWR-LWR威廉指标TAPI-加权指数成交值FSL-分水岭 | 趋势型 | CHO-佳庆指标CYE-市场趋势DBQR-对比强弱DMA-平均差DMI - 趋向指标DPO-区间震荡线EMV-简易波动指标GDX-鬼道线JLHB-绝路航标JS-加速线MACD-平滑异同平均QACD-快速异同平均QR-强弱指标TRIX-终极指标UOS-终极指标VMACD-量平滑移动平均VPT-量价曲线WVAD-威廉变异离散量 | 能量型 | BRAR-情绪指标CR-带状能量线CYR-市场强弱MASS-梅斯线PCNT-幅度比PSY-心理线VR-成交量变异率 | 成交量型 | AMO-成交金额CCL-持仓量（适用于期货）DBLB-对比量比DBQRV-对比强弱量OBV-累积能量线VOL-成交量VRSI-相对强弱量LB-量比 |
| 均线型 | AMV-成本价均线ALLIGAT-鳄鱼线BBI-多空均线EXPMA-指数平均线BBIBOLL-多空布林线MA-均线HMA-高价平均线LMA-低价平均线 VMA-变异平均线 | 路径型 | BOLL-布林线ENE-轨道线MIKE-麦克支撑压力PBX-瀑布线XS-薛斯通道XS2-薛斯通道2 | 其他型 | EMA-指数移动平均SMA-移动平均BDZX-波段之星CDP-STD-逆势操作CJDX-超级短线CYHT-财运亨通JAX-济安线JFZX-飓风智能中线JYJL-交易参考均量LHXJ-猎狐先觉LYJH-猎鹰歼狐TBP-STD-趋势平衡点ZBCD-准备抄底 | 特色型 | AROON-阿隆指标CFJT-财富阶梯ZSDB-指数对比 |
| 神系 | SG-SMX-生命线SG-LB-量比SG-PF-强势股评分XDT-心电图 | 龙系 | ZLMM-主力买卖RAD-威力雷达SHT-龙系短线 | 鬼系 | CYW-主力控盘CYS-市场盈亏 | 图表型 | ZX-重心线PUCU-逆时钟曲线 |

###### 示例：

```python
# 导入技术分析指标库
from jqdatasdk import *
from jqdatasdk.technical_analysis import *

# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 GDX 值，分别返回：济安线、压力线和支撑线的值。
gdx_jax, gdx_ylx, gdx_zcx = GDX(security_list1,check_date='2017-01-04', N = 30, M = 9)
print (gdx_jax[security_list1])
print (gdx_ylx[security_list1])
print (gdx_zcx[security_list1])

# 输出 security_list2 的 GDX 值
gdx_jax, gdx_ylx, gdx_zcx = GDX(security_list2,check_date='2017-01-04', N = 30, M = 9)
for stock in security_list2:
    print (gdx_jax[stock])
    print (gdx_ylx[stock])
    print (gdx_zcx[stock])

8.29159727600139
9.037841030841516
7.545353521161265
8.29159727600139
9.037841030841516
7.545353521161265
15.528491778666732
16.92605603874674
14.130927518586727
15.359770622508778
16.74214997853457
13.977391266482988
nan
nan
nan
```
