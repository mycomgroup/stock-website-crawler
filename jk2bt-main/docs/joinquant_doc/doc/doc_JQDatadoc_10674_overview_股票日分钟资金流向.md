---
id: "url-364963be"
type: "website"
title: "股票日分钟资金流向"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10674"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:48:08.863Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10674"
  headings:
    - {"level":3,"text":"股票日分钟资金流向","id":""}
    - {"level":5,"text":"field参数","id":""}
  paragraphs:
    - "描述"
    - "注意"
    - "</body> </html>"
    - "示例："
  lists:
    - {"type":"ul","items":["历史范围：2015年至今；更新时间：分钟级别因子每日15:00更新，日级别每日19:00更新","注意：分钟级别资金流向为聚宽特色数据；需单独采购"]}
    - {"type":"ul","items":["security_list : 一只股票代码或者一个股票代码的 list","start_date, count 二选一，start_date和end_date获取分钟数据时可以精确到分钟 ,count代表end_date往前推的交易日/分钟个数","提供2015年至今的数据，支持分钟和天级别 , 相比于旧版资金流向算法有优化，所以和旧版数据上可能存在差异。","frequency : 只支持 minutes/1m 或 daily/1d ;数据按天储存,建议按天进行获取","fields : 支持的字段: [ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s', 'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s'] ,字段含义详见下图","data_type : 统计字段,默认为money成交额 , money、volume、deal三选一; 返回： dataframe,columns是time ,code以及对应的fields；字段含义详见下图"]}
    - {"type":"ul","items":["单次数据返回条数小于200万条(获取分钟数据时，单次获取的数据区间不可超过30个交易日)","停牌时无数据 , 传递count时会按照交易时间计算取数范围 , 不考虑停牌","资金流向天级别的数据在19:00可获取 , 数据产生之前查询不会返回","当日的分钟资金流向数据固定时间计算生成,一般在每分钟的第30秒完成计算, 所以建议在T分钟的30s之后再去获取T分钟的前的数据 ,如果个别标的在获取的时候恰好未生成, 对应的行填充为nan","默认情况下，fildes参数设为None，仅返回资金流入和流入字段，而不包括资金净流入字段。若您希望获取完整的内容，请将fields参数设置为所需字段的完整列表。如需返回完整内容，fields直接传入[ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s', 'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s']"]}
  tables:
    - {"caption":"","headers":["字段","名称"],"rows":[["money","统计成交额"],["volume","统计成交量"],["deal","统计成交笔数"]]}
    - {"caption":"","headers":["类型","字段","前缀","后缀","描述"],"rows":[["资金流入"],["超大单","inflow_xl","inflow","xl","超大单流入（大于等于50万股或100万元的成交单）"],["大单","inflow_l","inflow","l","大单流入（大于等于10万股或20万元且小于50万股或100万元的成交单）"],["中单","inflow_m","inflow","m","中单流入（大于等于2万股或4万元且小于10万股或20万元的成交单）"],["小单","inflow_s","inflow","s","小单流入（小于2万股或4万元的成交单）"],["资金流出"],["超大单","outflow_xl","outflow","xl","超大单流出（大于等于50万股或100万元的成交单）"],["大单","outflow_l","outflow","l","大单流出（大于等于10万股或20万元且小于50万股或100万元的成交单）"],["中单","outflow_m","outflow","m","中单流出（大于等于2万股或4万元且小于10万股或20万元的成交单）"],["小单","outflow_s","outflow","s","小单流出（小于2万股或4万元的成交单）"],["资金净流入"],["超大单","netflow_xl","netflow","xl","超大单净流入（inflow_xl - outflow_xl）"],["大单","netflow_l","netflow","l","大单净流入（inflow_l - outflow_l）"],["中单","netflow_m","netflow","m","中单净流入（inflow_m - outflow_m）"],["小单","netflow_s","netflow","s","小单净流入（inflow_s - outflow_s）"]]}
  codeBlocks:
    - {"language":"python","code":"get_money_flow_pro(security_list,start_date=None, end_date=None,\n frequency='daily',fields=None,count=None, data_type='money')"}
    - {"language":"python","code":"# 获取000001.XSHE在2024-02-28 14:55:00往前推240条分钟的分钟级资金流向数据\ndf = get_money_flow_pro(\"000001.XSHE\",end_date='2024-02-28 14:55:00',\n                        count=240,frequency='1m',\n                        fields=[ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s',\n                               'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl',\n                               'netflow_l', 'netflow_m', 'netflow_s'])\nprint(df.head(10))\n>>>\n                 time         code    inflow_l    inflow_m    inflow_s  \\\n0 2024-02-27 14:56:00  000001.XSHE   7795323.0  10198617.0   5580355.0   \n1 2024-02-27 14:57:00  000001.XSHE  10093650.0   7018003.0   4808979.0   \n2 2024-02-27 14:58:00  000001.XSHE         0.0         0.0         0.0   \n3 2024-02-27 14:59:00  000001.XSHE         0.0         0.0         0.0   \n4 2024-02-27 15:00:00  000001.XSHE         0.0         0.0         0.0   \n5 2024-02-28 09:31:00  000001.XSHE  20712683.0  18633030.0  10438000.0   \n6 2024-02-28 09:32:00  000001.XSHE  10876648.0   5826687.0   3165221.0   \n7 2024-02-28 09:33:00  000001.XSHE   6292688.0   5076045.0   2240633.0   \n8 2024-02-28 09:34:00  000001.XSHE   8219759.0   4739779.0   3445819.0   \n9 2024-02-28 09:35:00  000001.XSHE  13489408.0  12084201.0  10398338.0   \n\n    inflow_xl   outflow_l   outflow_m   outflow_s  outflow_xl  netflow_xl  \\\n0  10606647.0   3331029.0  1084035.00  1537411.00  28228467.0 -17621820.0   \n1  31102831.0   2062556.0  1702601.00  1306774.00  47951532.0 -16848701.0   \n2         0.0         0.0        0.00        0.00         0.0         0.0   \n3         0.0         0.0        0.00        0.00         0.0         0.0   \n4         0.0         0.0        0.00        0.00         0.0         0.0   \n5  15242588.0  17926255.0  9793870.29  5222146.71  32084029.0 -16841441.0   \n6   3679661.0  10121116.0  7237059.00  2524108.00   3665934.0     13727.0   \n7  13968043.0   8555154.0  5548937.00  2870119.00  10603199.0   3364844.0   \n8  16300908.0   6344863.0  4852270.00  4408176.00  17100956.0   -800048.0   \n9  16285511.0   9562841.0  5200105.00  3586663.00  33907849.0 -17622338.0   \n\n   netflow_l   netflow_m   netflow_s  \n0  4464294.0  9114582.00  4042944.00  \n1  8031094.0  5315402.00  3502205.00  \n2        0.0        0.00        0.00  \n3        0.0        0.00        0.00  \n4        0.0        0.00        0.00  \n5  2786428.0  8839159.71  5215853.29  \n6   755532.0 -1410372.00   641113.00  \n7 -2262466.0  -472892.00  -629486.00  \n8  1874896.0  -112491.00  -962357.00  \n9  3926567.0  6884096.00  6811675.00"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"股票日分钟资金流向"}
    - {"type":"list","listType":"ul","items":["历史范围：2015年至今；更新时间：分钟级别因子每日15:00更新，日级别每日19:00更新","注意：分钟级别资金流向为聚宽特色数据；需单独采购"]}
    - {"type":"codeblock","language":"python","content":"get_money_flow_pro(security_list,start_date=None, end_date=None,\n frequency='daily',fields=None,count=None, data_type='money')"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["security_list : 一只股票代码或者一个股票代码的 list","start_date, count 二选一，start_date和end_date获取分钟数据时可以精确到分钟 ,count代表end_date往前推的交易日/分钟个数","提供2015年至今的数据，支持分钟和天级别 , 相比于旧版资金流向算法有优化，所以和旧版数据上可能存在差异。","frequency : 只支持 minutes/1m 或 daily/1d ;数据按天储存,建议按天进行获取","fields : 支持的字段: [ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s', 'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s'] ,字段含义详见下图","data_type : 统计字段,默认为money成交额 , money、volume、deal三选一; 返回： dataframe,columns是time ,code以及对应的fields；字段含义详见下图"]}
    - {"type":"table","headers":["字段","名称"],"rows":[["money","统计成交额"],["volume","统计成交量"],["deal","统计成交笔数"]]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["单次数据返回条数小于200万条(获取分钟数据时，单次获取的数据区间不可超过30个交易日)","停牌时无数据 , 传递count时会按照交易时间计算取数范围 , 不考虑停牌","资金流向天级别的数据在19:00可获取 , 数据产生之前查询不会返回","当日的分钟资金流向数据固定时间计算生成,一般在每分钟的第30秒完成计算, 所以建议在T分钟的30s之后再去获取T分钟的前的数据 ,如果个别标的在获取的时候恰好未生成, 对应的行填充为nan","默认情况下，fildes参数设为None，仅返回资金流入和流入字段，而不包括资金净流入字段。若您希望获取完整的内容，请将fields参数设置为所需字段的完整列表。如需返回完整内容，fields直接传入[ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s', 'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s']"]}
    - {"type":"heading","level":5,"content":"field参数"}
    - {"type":"table","headers":["类型","字段","前缀","后缀","描述"],"rows":[["资金流入"],["超大单","inflow_xl","inflow","xl","超大单流入（大于等于50万股或100万元的成交单）"],["大单","inflow_l","inflow","l","大单流入（大于等于10万股或20万元且小于50万股或100万元的成交单）"],["中单","inflow_m","inflow","m","中单流入（大于等于2万股或4万元且小于10万股或20万元的成交单）"],["小单","inflow_s","inflow","s","小单流入（小于2万股或4万元的成交单）"],["资金流出"],["超大单","outflow_xl","outflow","xl","超大单流出（大于等于50万股或100万元的成交单）"],["大单","outflow_l","outflow","l","大单流出（大于等于10万股或20万元且小于50万股或100万元的成交单）"],["中单","outflow_m","outflow","m","中单流出（大于等于2万股或4万元且小于10万股或20万元的成交单）"],["小单","outflow_s","outflow","s","小单流出（小于2万股或4万元的成交单）"],["资金净流入"],["超大单","netflow_xl","netflow","xl","超大单净流入（inflow_xl - outflow_xl）"],["大单","netflow_l","netflow","l","大单净流入（inflow_l - outflow_l）"],["中单","netflow_m","netflow","m","中单净流入（inflow_m - outflow_m）"],["小单","netflow_s","netflow","s","小单净流入（inflow_s - outflow_s）"]]}
    - {"type":"paragraph","content":"</body> </html>"}
    - {"type":"paragraph","content":"示例："}
    - {"type":"codeblock","language":"python","content":"# 获取000001.XSHE在2024-02-28 14:55:00往前推240条分钟的分钟级资金流向数据\ndf = get_money_flow_pro(\"000001.XSHE\",end_date='2024-02-28 14:55:00',\n                        count=240,frequency='1m',\n                        fields=[ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s',\n                               'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl',\n                               'netflow_l', 'netflow_m', 'netflow_s'])\nprint(df.head(10))\n>>>\n                 time         code    inflow_l    inflow_m    inflow_s  \\\n0 2024-02-27 14:56:00  000001.XSHE   7795323.0  10198617.0   5580355.0   \n1 2024-02-27 14:57:00  000001.XSHE  10093650.0   7018003.0   4808979.0   \n2 2024-02-27 14:58:00  000001.XSHE         0.0         0.0         0.0   \n3 2024-02-27 14:59:00  000001.XSHE         0.0         0.0         0.0   \n4 2024-02-27 15:00:00  000001.XSHE         0.0         0.0         0.0   \n5 2024-02-28 09:31:00  000001.XSHE  20712683.0  18633030.0  10438000.0   \n6 2024-02-28 09:32:00  000001.XSHE  10876648.0   5826687.0   3165221.0   \n7 2024-02-28 09:33:00  000001.XSHE   6292688.0   5076045.0   2240633.0   \n8 2024-02-28 09:34:00  000001.XSHE   8219759.0   4739779.0   3445819.0   \n9 2024-02-28 09:35:00  000001.XSHE  13489408.0  12084201.0  10398338.0   \n\n    inflow_xl   outflow_l   outflow_m   outflow_s  outflow_xl  netflow_xl  \\\n0  10606647.0   3331029.0  1084035.00  1537411.00  28228467.0 -17621820.0   \n1  31102831.0   2062556.0  1702601.00  1306774.00  47951532.0 -16848701.0   \n2         0.0         0.0        0.00        0.00         0.0         0.0   \n3         0.0         0.0        0.00        0.00         0.0         0.0   \n4         0.0         0.0        0.00        0.00         0.0         0.0   \n5  15242588.0  17926255.0  9793870.29  5222146.71  32084029.0 -16841441.0   \n6   3679661.0  10121116.0  7237059.00  2524108.00   3665934.0     13727.0   \n7  13968043.0   8555154.0  5548937.00  2870119.00  10603199.0   3364844.0   \n8  16300908.0   6344863.0  4852270.00  4408176.00  17100956.0   -800048.0   \n9  16285511.0   9562841.0  5200105.00  3586663.00  33907849.0 -17622338.0   \n\n   netflow_l   netflow_m   netflow_s  \n0  4464294.0  9114582.00  4042944.00  \n1  8031094.0  5315402.00  3502205.00  \n2        0.0        0.00        0.00  \n3        0.0        0.00        0.00  \n4        0.0        0.00        0.00  \n5  2786428.0  8839159.71  5215853.29  \n6   755532.0 -1410372.00   641113.00  \n7 -2262466.0  -472892.00  -629486.00  \n8  1874896.0  -112491.00  -962357.00  \n9  3926567.0  6884096.00  6811675.00"}
  suggestedFilename: "doc_JQDatadoc_10674_overview_股票日分钟资金流向"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10674"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 股票日分钟资金流向

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10674

## 描述

描述

## 内容

#### 股票日分钟资金流向

- 历史范围：2015年至今；更新时间：分钟级别因子每日15:00更新，日级别每日19:00更新
- 注意：分钟级别资金流向为聚宽特色数据；需单独采购

```python
get_money_flow_pro(security_list,start_date=None, end_date=None,
 frequency='daily',fields=None,count=None, data_type='money')
```

描述

- security_list : 一只股票代码或者一个股票代码的 list
- start_date, count 二选一，start_date和end_date获取分钟数据时可以精确到分钟 ,count代表end_date往前推的交易日/分钟个数
- 提供2015年至今的数据，支持分钟和天级别 , 相比于旧版资金流向算法有优化，所以和旧版数据上可能存在差异。
- frequency : 只支持 minutes/1m 或 daily/1d ;数据按天储存,建议按天进行获取
- fields : 支持的字段: [ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s', 'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s'] ,字段含义详见下图
- data_type : 统计字段,默认为money成交额 , money、volume、deal三选一; 返回： dataframe,columns是time ,code以及对应的fields；字段含义详见下图

| 字段 | 名称 |
| --- | --- |
| money | 统计成交额 |
| volume | 统计成交量 |
| deal | 统计成交笔数 |

注意

- 单次数据返回条数小于200万条(获取分钟数据时，单次获取的数据区间不可超过30个交易日)
- 停牌时无数据 , 传递count时会按照交易时间计算取数范围 , 不考虑停牌
- 资金流向天级别的数据在19:00可获取 , 数据产生之前查询不会返回
- 当日的分钟资金流向数据固定时间计算生成,一般在每分钟的第30秒完成计算, 所以建议在T分钟的30s之后再去获取T分钟的前的数据 ,如果个别标的在获取的时候恰好未生成, 对应的行填充为nan
- 默认情况下，fildes参数设为None，仅返回资金流入和流入字段，而不包括资金净流入字段。若您希望获取完整的内容，请将fields参数设置为所需字段的完整列表。如需返回完整内容，fields直接传入[ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s', 'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl', 'netflow_l', 'netflow_m', 'netflow_s']

###### field参数

| 类型 | 字段 | 前缀 | 后缀 | 描述 |
| --- | --- | --- | --- | --- |
| 资金流入 |
| 超大单 | inflow_xl | inflow | xl | 超大单流入（大于等于50万股或100万元的成交单） |
| 大单 | inflow_l | inflow | l | 大单流入（大于等于10万股或20万元且小于50万股或100万元的成交单） |
| 中单 | inflow_m | inflow | m | 中单流入（大于等于2万股或4万元且小于10万股或20万元的成交单） |
| 小单 | inflow_s | inflow | s | 小单流入（小于2万股或4万元的成交单） |
| 资金流出 |
| 超大单 | outflow_xl | outflow | xl | 超大单流出（大于等于50万股或100万元的成交单） |
| 大单 | outflow_l | outflow | l | 大单流出（大于等于10万股或20万元且小于50万股或100万元的成交单） |
| 中单 | outflow_m | outflow | m | 中单流出（大于等于2万股或4万元且小于10万股或20万元的成交单） |
| 小单 | outflow_s | outflow | s | 小单流出（小于2万股或4万元的成交单） |
| 资金净流入 |
| 超大单 | netflow_xl | netflow | xl | 超大单净流入（inflow_xl - outflow_xl） |
| 大单 | netflow_l | netflow | l | 大单净流入（inflow_l - outflow_l） |
| 中单 | netflow_m | netflow | m | 中单净流入（inflow_m - outflow_m） |
| 小单 | netflow_s | netflow | s | 小单净流入（inflow_s - outflow_s） |

</body> </html>

示例：

```python
# 获取000001.XSHE在2024-02-28 14:55:00往前推240条分钟的分钟级资金流向数据
df = get_money_flow_pro("000001.XSHE",end_date='2024-02-28 14:55:00',
                        count=240,frequency='1m',
                        fields=[ 'inflow_xl', 'inflow_l', 'inflow_m', 'inflow_s',
                               'outflow_xl', 'outflow_l', 'outflow_m', 'outflow_s', 'netflow_xl',
                               'netflow_l', 'netflow_m', 'netflow_s'])
print(df.head(10))
>>>
                 time         code    inflow_l    inflow_m    inflow_s  \
0 2024-02-27 14:56:00  000001.XSHE   7795323.0  10198617.0   5580355.0   
1 2024-02-27 14:57:00  000001.XSHE  10093650.0   7018003.0   4808979.0   
2 2024-02-27 14:58:00  000001.XSHE         0.0         0.0         0.0   
3 2024-02-27 14:59:00  000001.XSHE         0.0         0.0         0.0   
4 2024-02-27 15:00:00  000001.XSHE         0.0         0.0         0.0   
5 2024-02-28 09:31:00  000001.XSHE  20712683.0  18633030.0  10438000.0   
6 2024-02-28 09:32:00  000001.XSHE  10876648.0   5826687.0   3165221.0   
7 2024-02-28 09:33:00  000001.XSHE   6292688.0   5076045.0   2240633.0   
8 2024-02-28 09:34:00  000001.XSHE   8219759.0   4739779.0   3445819.0   
9 2024-02-28 09:35:00  000001.XSHE  13489408.0  12084201.0  10398338.0   

    inflow_xl   outflow_l   outflow_m   outflow_s  outflow_xl  netflow_xl  \
0  10606647.0   3331029.0  1084035.00  1537411.00  28228467.0 -17621820.0   
1  31102831.0   2062556.0  1702601.00  1306774.00  47951532.0 -16848701.0   
2         0.0         0.0        0.00        0.00         0.0         0.0   
3         0.0         0.0        0.00        0.00         0.0         0.0   
4         0.0         0.0        0.00        0.00         0.0         0.0   
5  15242588.0  17926255.0  9793870.29  5222146.71  32084029.0 -16841441.0   
6   3679661.0  10121116.0  7237059.00  2524108.00   3665934.0     13727.0   
7  13968043.0   8555154.0  5548937.00  2870119.00  10603199.0   3364844.0   
8  16300908.0   6344863.0  4852270.00  4408176.00  17100956.0   -800048.0   
9  16285511.0   9562841.0  5200105.00  3586663.00  33907849.0 -17622338.0   

   netflow_l   netflow_m   netflow_s  
0  4464294.0  9114582.00  4042944.00  
1  8031094.0  5315402.00  3502205.00  
2        0.0        0.00        0.00  
3        0.0        0.00        0.00  
4        0.0        0.00        0.00  
5  2786428.0  8839159.71  5215853.29  
6   755532.0 -1410372.00   641113.00  
7 -2262466.0  -472892.00  -629486.00  
8  1874896.0  -112491.00  -962357.00  
9  3926567.0  6884096.00  6811675.00
```
