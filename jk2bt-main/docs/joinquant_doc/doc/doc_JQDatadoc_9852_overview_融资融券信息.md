---
id: "url-7a226b0e"
type: "website"
title: "融资融券信息"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9852"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:17:06.158Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9852"
  headings:
    - {"level":3,"text":"融资融券信息","id":""}
    - {"level":5,"text":"示例","id":"-1"}
  paragraphs:
    - "描述"
    - "返回"
  lists:
    - {"type":"ul","items":["历史范围：2010年至今；更新时间：下一个交易日9点之前更新"]}
    - {"type":"ul","items":["获取一只或者多只股票在一个时间段内的融资融券信息"]}
    - {"type":"ul","items":["返回一个 [pandas.DataFrame] 对象，默认的列索引为取得的全部字段. 如果给定了 fields 参数, 则列索引与给定的 fields 对应"]}
    - {"type":"ul","items":["获取一只股票"]}
    - {"type":"ul","items":["获取多只股票的"]}
  tables:
    - {"caption":"","headers":["参数","名称","注释"],"rows":[["security_list","股票代码","一只股票代码或者一个股票代码的 list"],["start_date","开始日期","与 count 二选一, 不可同时使用； 一个字符串或者 [datetime.datetime]/[datetime.date] 对象, 默认为平台提供的数据的最早日期"],["end_date","结束日期","一个字符串或者 [datetime.date]/[datetime.datetime] 对象, 默认为 datetime.date.today()"],["count","数量","与 start_date 二选一，不可同时使用**, 必须大于 0. 表示返回 end_date 之前 count 个交易日的数据, 包含 end_date"],["fields","内涵不同字段，具体含义如下","字段名或者 list, 可选. 默认为 None, 表示取全部字段,"]]}
    - {"caption":"","headers":["字段名","含义"],"rows":[["date","日期"],["sec_code","股票代码"],["fin_value","融资余额(元）"],["fin_buy_value","融资买入额（元）"],["fin_refund_value","融资偿还额（元）"],["sec_value","融券余量（股）"],["sec_sell_value","融券卖出量（股）"],["sec_refund_value","融券偿还量（股）"],["fin_sec_value","融资融券余额（元）"]]}
  codeBlocks:
    - {"language":"python","code":"get_mtss(security_list, start_date=None, end_date=None, fields=None, count=None)"}
    - {"language":"python","code":"# 获取平安银行在2016-01-01和2016-04-01的融资融券信息\ndf=get_mtss('000001.XSHE','2016-01-01','2016-04-01',fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])\nprint(df[:5])\n\n        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \\\n0 2016-01-04  000001.XSHE  3.472612e+09    152129217.0       169414153.0   \n1 2016-01-05  000001.XSHE  3.439317e+09    143615276.0       176910198.0   \n2 2016-01-06  000001.XSHE  3.424639e+09    110246569.0       124924119.0   \n3 2016-01-07  000001.XSHE  3.431689e+09     35093634.0        28044375.0   \n4 2016-01-08  000001.XSHE  3.369931e+09    136799561.0       198556950.0   \n\n   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  \n0   594640.0        184100.0          317900.0   3.479349e+09  \n1   584540.0         20800.0           30900.0   3.445981e+09  \n2   403040.0           900.0          182400.0   3.429286e+09  \n3   395140.0             0.0            7900.0   3.436011e+09  \n4   362440.0          2400.0           35100.0   3.373962e+09"}
    - {"language":"python","code":"# 获取股票 000001.XSHE 在日期 2016-06-30 往前 5 个交易日的融资融券信息\ndf=get_mtss('000001.XSHE', end_date=\"2016-06-30\", count=5,fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])\nprint(df)\n        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \\\n0 2016-06-24  000001.XSHE  2.855885e+09     71503613.0        53903693.0   \n1 2016-06-27  000001.XSHE  2.869486e+09     47309234.0        33707430.0   \n2 2016-06-28  000001.XSHE  2.889199e+09     55438177.0        35725201.0   \n3 2016-06-29  000001.XSHE  2.897613e+09     72215294.0        63801533.0   \n4 2016-06-30  000001.XSHE  2.859810e+09     41895702.0        79699182.0   \n\n   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  \n0  2210681.0         14100.0         1666940.0   2.874830e+09  \n1  3846536.0       1660755.0           24900.0   2.902605e+09  \n2  3920836.0         91700.0           17400.0   2.923036e+09  \n3  4024356.0        161500.0           57980.0   2.932585e+09  \n4  3921356.0         45700.0          148700.0   2.893925e+09"}
    - {"language":"python","code":"# 获取平万科A、中信海直、深振业A股票的融资融券信息\ndf=get_mtss(['000002.XSHE','000099.XSHE','000006.XSHE'],'2016-01-24','2016-01-25',fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])\nprint(df[:5])\n\n        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \\\n0 2016-01-25  000006.XSHE  1.502571e+09     14822257.0        24633824.0   \n1 2016-01-25  000002.XSHE  1.779932e+09            0.0         5976580.0   \n2 2016-01-25  000099.XSHE  7.126432e+08     14776171.0        13732025.0   \n\n   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  \n0      100.0             0.0               0.0   1.502572e+09  \n1  1449450.0             0.0               0.0   1.815342e+09  \n2     3400.0             0.0               0.0   7.126829e+08"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"融资融券信息"}
    - {"type":"list","listType":"ul","items":["历史范围：2010年至今；更新时间：下一个交易日9点之前更新"]}
    - {"type":"codeblock","language":"python","content":"get_mtss(security_list, start_date=None, end_date=None, fields=None, count=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取一只或者多只股票在一个时间段内的融资融券信息"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["返回一个 [pandas.DataFrame] 对象，默认的列索引为取得的全部字段. 如果给定了 fields 参数, 则列索引与给定的 fields 对应"]}
    - {"type":"table","headers":["参数","名称","注释"],"rows":[["security_list","股票代码","一只股票代码或者一个股票代码的 list"],["start_date","开始日期","与 count 二选一, 不可同时使用； 一个字符串或者 [datetime.datetime]/[datetime.date] 对象, 默认为平台提供的数据的最早日期"],["end_date","结束日期","一个字符串或者 [datetime.date]/[datetime.datetime] 对象, 默认为 datetime.date.today()"],["count","数量","与 start_date 二选一，不可同时使用**, 必须大于 0. 表示返回 end_date 之前 count 个交易日的数据, 包含 end_date"],["fields","内涵不同字段，具体含义如下","字段名或者 list, 可选. 默认为 None, 表示取全部字段,"]]}
    - {"type":"table","headers":["字段名","含义"],"rows":[["date","日期"],["sec_code","股票代码"],["fin_value","融资余额(元）"],["fin_buy_value","融资买入额（元）"],["fin_refund_value","融资偿还额（元）"],["sec_value","融券余量（股）"],["sec_sell_value","融券卖出量（股）"],["sec_refund_value","融券偿还量（股）"],["fin_sec_value","融资融券余额（元）"]]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获取一只股票"]}
    - {"type":"codeblock","language":"python","content":"# 获取平安银行在2016-01-01和2016-04-01的融资融券信息\ndf=get_mtss('000001.XSHE','2016-01-01','2016-04-01',fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])\nprint(df[:5])\n\n        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \\\n0 2016-01-04  000001.XSHE  3.472612e+09    152129217.0       169414153.0   \n1 2016-01-05  000001.XSHE  3.439317e+09    143615276.0       176910198.0   \n2 2016-01-06  000001.XSHE  3.424639e+09    110246569.0       124924119.0   \n3 2016-01-07  000001.XSHE  3.431689e+09     35093634.0        28044375.0   \n4 2016-01-08  000001.XSHE  3.369931e+09    136799561.0       198556950.0   \n\n   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  \n0   594640.0        184100.0          317900.0   3.479349e+09  \n1   584540.0         20800.0           30900.0   3.445981e+09  \n2   403040.0           900.0          182400.0   3.429286e+09  \n3   395140.0             0.0            7900.0   3.436011e+09  \n4   362440.0          2400.0           35100.0   3.373962e+09"}
    - {"type":"codeblock","language":"python","content":"# 获取股票 000001.XSHE 在日期 2016-06-30 往前 5 个交易日的融资融券信息\ndf=get_mtss('000001.XSHE', end_date=\"2016-06-30\", count=5,fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])\nprint(df)\n        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \\\n0 2016-06-24  000001.XSHE  2.855885e+09     71503613.0        53903693.0   \n1 2016-06-27  000001.XSHE  2.869486e+09     47309234.0        33707430.0   \n2 2016-06-28  000001.XSHE  2.889199e+09     55438177.0        35725201.0   \n3 2016-06-29  000001.XSHE  2.897613e+09     72215294.0        63801533.0   \n4 2016-06-30  000001.XSHE  2.859810e+09     41895702.0        79699182.0   \n\n   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  \n0  2210681.0         14100.0         1666940.0   2.874830e+09  \n1  3846536.0       1660755.0           24900.0   2.902605e+09  \n2  3920836.0         91700.0           17400.0   2.923036e+09  \n3  4024356.0        161500.0           57980.0   2.932585e+09  \n4  3921356.0         45700.0          148700.0   2.893925e+09"}
    - {"type":"list","listType":"ul","items":["获取多只股票的"]}
    - {"type":"codeblock","language":"python","content":"# 获取平万科A、中信海直、深振业A股票的融资融券信息\ndf=get_mtss(['000002.XSHE','000099.XSHE','000006.XSHE'],'2016-01-24','2016-01-25',fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])\nprint(df[:5])\n\n        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \\\n0 2016-01-25  000006.XSHE  1.502571e+09     14822257.0        24633824.0   \n1 2016-01-25  000002.XSHE  1.779932e+09            0.0         5976580.0   \n2 2016-01-25  000099.XSHE  7.126432e+08     14776171.0        13732025.0   \n\n   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  \n0      100.0             0.0               0.0   1.502572e+09  \n1  1449450.0             0.0               0.0   1.815342e+09  \n2     3400.0             0.0               0.0   7.126829e+08"}
  suggestedFilename: "doc_JQDatadoc_9852_overview_融资融券信息"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9852"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 融资融券信息

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9852

## 描述

描述

## 内容

#### 融资融券信息

- 历史范围：2010年至今；更新时间：下一个交易日9点之前更新

```python
get_mtss(security_list, start_date=None, end_date=None, fields=None, count=None)
```

描述

- 获取一只或者多只股票在一个时间段内的融资融券信息

返回

- 返回一个 [pandas.DataFrame] 对象，默认的列索引为取得的全部字段. 如果给定了 fields 参数, 则列索引与给定的 fields 对应

| 参数 | 名称 | 注释 |
| --- | --- | --- |
| security_list | 股票代码 | 一只股票代码或者一个股票代码的 list |
| start_date | 开始日期 | 与 count 二选一, 不可同时使用； 一个字符串或者 [datetime.datetime]/[datetime.date] 对象, 默认为平台提供的数据的最早日期 |
| end_date | 结束日期 | 一个字符串或者 [datetime.date]/[datetime.datetime] 对象, 默认为 datetime.date.today() |
| count | 数量 | 与 start_date 二选一，不可同时使用**, 必须大于 0. 表示返回 end_date 之前 count 个交易日的数据, 包含 end_date |
| fields | 内涵不同字段，具体含义如下 | 字段名或者 list, 可选. 默认为 None, 表示取全部字段, |

| 字段名 | 含义 |
| --- | --- |
| date | 日期 |
| sec_code | 股票代码 |
| fin_value | 融资余额(元） |
| fin_buy_value | 融资买入额（元） |
| fin_refund_value | 融资偿还额（元） |
| sec_value | 融券余量（股） |
| sec_sell_value | 融券卖出量（股） |
| sec_refund_value | 融券偿还量（股） |
| fin_sec_value | 融资融券余额（元） |

###### 示例

- 获取一只股票

```python
# 获取平安银行在2016-01-01和2016-04-01的融资融券信息
df=get_mtss('000001.XSHE','2016-01-01','2016-04-01',fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])
print(df[:5])

        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \
0 2016-01-04  000001.XSHE  3.472612e+09    152129217.0       169414153.0   
1 2016-01-05  000001.XSHE  3.439317e+09    143615276.0       176910198.0   
2 2016-01-06  000001.XSHE  3.424639e+09    110246569.0       124924119.0   
3 2016-01-07  000001.XSHE  3.431689e+09     35093634.0        28044375.0   
4 2016-01-08  000001.XSHE  3.369931e+09    136799561.0       198556950.0   

   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  
0   594640.0        184100.0          317900.0   3.479349e+09  
1   584540.0         20800.0           30900.0   3.445981e+09  
2   403040.0           900.0          182400.0   3.429286e+09  
3   395140.0             0.0            7900.0   3.436011e+09  
4   362440.0          2400.0           35100.0   3.373962e+09
```

```python
# 获取股票 000001.XSHE 在日期 2016-06-30 往前 5 个交易日的融资融券信息
df=get_mtss('000001.XSHE', end_date="2016-06-30", count=5,fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])
print(df)
        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \
0 2016-06-24  000001.XSHE  2.855885e+09     71503613.0        53903693.0   
1 2016-06-27  000001.XSHE  2.869486e+09     47309234.0        33707430.0   
2 2016-06-28  000001.XSHE  2.889199e+09     55438177.0        35725201.0   
3 2016-06-29  000001.XSHE  2.897613e+09     72215294.0        63801533.0   
4 2016-06-30  000001.XSHE  2.859810e+09     41895702.0        79699182.0   

   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  
0  2210681.0         14100.0         1666940.0   2.874830e+09  
1  3846536.0       1660755.0           24900.0   2.902605e+09  
2  3920836.0         91700.0           17400.0   2.923036e+09  
3  4024356.0        161500.0           57980.0   2.932585e+09  
4  3921356.0         45700.0          148700.0   2.893925e+09
```

- 获取多只股票的

```python
# 获取平万科A、中信海直、深振业A股票的融资融券信息
df=get_mtss(['000002.XSHE','000099.XSHE','000006.XSHE'],'2016-01-24','2016-01-25',fields=['date','sec_code','fin_value','fin_buy_value','fin_refund_value','sec_value','sec_sell_value','sec_refund_value','fin_sec_value'])
print(df[:5])

        date     sec_code     fin_value  fin_buy_value  fin_refund_value  \
0 2016-01-25  000006.XSHE  1.502571e+09     14822257.0        24633824.0   
1 2016-01-25  000002.XSHE  1.779932e+09            0.0         5976580.0   
2 2016-01-25  000099.XSHE  7.126432e+08     14776171.0        13732025.0   

   sec_value  sec_sell_value  sec_refund_value  fin_sec_value  
0      100.0             0.0               0.0   1.502572e+09  
1  1449450.0             0.0               0.0   1.815342e+09  
2     3400.0             0.0               0.0   7.126829e+08
```
