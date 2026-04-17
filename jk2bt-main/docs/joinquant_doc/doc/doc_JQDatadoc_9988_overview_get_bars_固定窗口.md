---
id: "url-7a226f32"
type: "website"
title: "get_bars 固定窗口"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9988"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:24:21.696Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9988"
  headings:
    - {"level":3,"text":"get_bars 固定窗口","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "get_bars 参数说明"
    - "get_bars参数补充说明"
    - "fileds字段说明"
  lists:
    - {"type":"ul","items":["历史范围：2019/12/2至今","学习材料：JQData 日分钟API清洗与处理规则"]}
    - {"type":"ul","items":["获取各种时间周期的bar数据，bar的分割方式与主流行情软件相同， 同时还支持返回当前时刻所在 bar 的数据。"]}
    - {"type":"ul","items":["返回一个pandas.dataframe对象，可以按任意周期返回标的的开盘价、收盘价、最高价、最低价，成交数量,时段中成交的金额、复权因子同时也可以利用date数据查看所返回的数据是什么时刻的。"]}
    - {"type":"ul","items":["当天 09:00 ~ 15:00 的行情在 15:00 之后可以获取 ,当end_dt指定为当天尚未结束的交易时间时，会自动填充为上一个交易日结束的时间"]}
    - {"type":"ul","items":["security支持的标的种类为【股票，基金，指数，可转债，期货，期权】","unit支持 ['Xm'(即X分钟),'1d'（1天）,'1w'（1周）,'1M'（1月） ]频率的数据，当频率单位为分钟（m）时，'X'可为任一大于0且小于240的自然数，以每天的开盘时间为起点,，不会跨交易日合并分钟bar数据。 指定单位为周或月时，周的起点固定为自然周内的第一个交易日，终点为自然周的最后一个交易日；月的起点为自然月内的第一个交易日，终点为自然月内的最后一个交易日。 例：比如股票交易时间为[09:30:00,11:30:00),[13:00:00,15:00:00),则每个交易日最多有240根1分钟bar用于分配撮合成Xm的数据；当240能被X整除时，每个交易日会固定划分出 ( 240 / unit) 根bar数据；当240不能被X整除时，每个交易日会固定划分出 (( 240 / unit) + 1 )根 bar数据； 注：商品期货等因为有特殊的早盘小休时间（10:15-10:30），所以有两种划分标准： 1）当指定的分钟bar为5m/15m/30m/60m/120m时，以自然时间来进行划分；举例如unit=30m来划分时，会将10:00-10:30的自然时间来进行划分为一个bar，但时间戳会以交易时间10:15来进行标记。 2）当指定的分钟bar为其他非标准频率时，以实际交易的分钟数来进行划分；","start_dt 不可与‘count’同时存在；当start_dt没有指定时分秒的时间戳时，时分秒的默认值为00:00:00；","end_dt","include_now 表示的是是否需要返回end_dt所在的bar。 例：比如'1m'，指定end_dt='20XX-XX-XX 15:00:00'时，若include_now=True，则会返回15:00:00为时间戳标记的bar，若include_now=False，则只会返回至14:59:00为时间戳标记的bar。","fq_ref_date 注：fq:复权选项(仅对股票/基金品种生效，生效的fields（字段）包括['open','close','high','low','volume','factor','high_limit','low_limit','avg','pre_close'] 当fq_ref_date =None时，返回不复权的数据； 当fq_ref_date 被指定时，返回基于fq_ref_date 的复权数据(定点复权)"]}
    - {"type":"ul","items":["获取一只期权"]}
    - {"type":"ul","items":["获取多支期权"]}
  tables:
    - {"caption":"","headers":["参数名称","参数说明","默认值"],"rows":[["security","指定标的，获取多个标的时需传入List","无默认值，必填项"],["start_dt","开始时间","无默认值，与count参数二选一"],["end_dt","结束时间","当前时间"],["count","表示获取 end_date 之前几个 unit 的数据","None,与start_dt参数二选一"],["unit","单位时间长度，即指定获取的时间频率","1d"],["fields","所获取数据的字段名称，即表头","默认['date', 'open', 'close', 'high', 'low'],还支持 'volume', 'money', 'open_interest'(持仓量，是期货和期权特有的字段), 'factor'(后复权因子)"],["include_now","表示是否包含end_dt所在的bar","默认最新的时间"],["fq_ref_date","复权基准日期","None,即返回不复权数据"],["df","指定返回的数据格式是否为dataframe格式","True"],["start_dt","查询的开始时间，当unit为天时传入的分时秒将被忽略(1.9.3新增参数)","None,与count参数二选一"],["skip_paused","是否跳过停牌(1.9.3新增参数)","True"]]}
    - {"caption":"","headers":["字段名称","中文名称","注释（特殊说明）"],"rows":[["date","日期",""],["open","时间段开始时价格",""],["close","时间段结束时价格",""],["low","时间段中的最低价",""],["high","时间段中的最高价",""],["volume","时间段中的成交的标的数量",""],["money","时间段中的成交的金额",""],["factor","复权因子","复权选项仅针对股票和基金品种有效，对于期权而言，复权因子被固定设置为1"],["open_interest","持仓量","期货/期权品种；反映当前时刻的持有数量"],["paused","是否停牌","0 正常；1 停牌 (限unit为1d时) (jqdatasdk1.9.5新增)"],["high_limit","当天涨停价","限unit为1d时 (jqdatasdk1.9.5新增)"],["low_limit","当天跌停价","限unit为1d时 (jqdatasdk1.9.5新增)"],["avg","当天均价","限unit为1d时 (jqdatasdk1.9.5新增)"],["pre_close","前收价","限unit为1d时 (jqdatasdk1.9.5新增)前天的收盘价。注：按天来获取的话，股票、指数、基金、可转债的是前一天的收盘价。（新股上市为IPO发行价，股票出现分红，则pre close是指昨天收盘价带分红拆股调整后的价格）;期货/期权是前一天的结算价；"]]}
  codeBlocks:
    - {"language":"python","code":"get_bars(security, count, unit='1d',\n         fields=['date', 'open', 'close', 'high', 'low', 'volume', 'money','factor'],\n         include_now=False, start_dt=None,end_dt=None, fq_ref_date=None,df=True)"}
    - {"language":"python","code":"#获取ZC107C740.XZCE期权合约在“2021-04-05”前5个时间单位的数据\n\ndf = get_bars('ZC107C740.XZCE', 5, unit='120m',fields=['open','close','low','high','volume','money','open_interest'],include_now=False,end_dt='2021-04-05')\nprint(df)\n                 date    open   close     low    high  volume      money  \\\n0 2006-03-13 11:30:00  2603.0  2603.0  2603.0  2603.0     0.0        0.0   \n1 2006-03-13 15:00:00  2603.0  2603.0  2603.0  2603.0     0.0        0.0   \n2 2006-03-14 11:00:00  2603.0  2581.0  2581.0  2603.0   210.0  5422000.0   \n3 2006-03-14 11:30:00  2581.0  2610.0  2581.0  2610.0    48.0  1252800.0   \n4 2006-03-14 15:00:00  2610.0  2595.0  2581.0  2610.0    30.0   774580.0   \n\n   open_interest  \n0         1526.0  \n1         1526.0  \n2         1736.0  \n3         1784.0  \n4         1812.0"}
    - {"language":"python","code":"df = get_bars(['ZC107C740.XZCE','ZC107C750.XZCE'], 5, unit='120m',fields=['open','close','low','high','volume','money','open_interest'],include_now=False,end_dt='2021-04-05')\nprint(df)\n\n                                date  open  close   low  high  volume  \\\nZC107C750.XZCE 0 2021-04-01 23:00:00  21.7   23.6  21.7  24.2    69.0   \n               1 2021-04-02 11:00:00  23.8   23.6  23.5  24.5   187.0   \n               2 2021-04-02 11:30:00  23.6   22.8  22.8  23.7     5.0   \n               3 2021-04-02 15:00:00  22.8   25.2  22.3  25.2   112.0   \n               4 2021-04-06 09:30:00  23.7   24.8  23.7  24.8     3.0   \nZC107C740.XZCE 0 2021-04-01 23:00:00  24.8   27.6  24.8  27.6    60.0   \n               1 2021-04-02 11:00:00  27.6   26.2  26.2  27.6     7.0   \n               2 2021-04-02 11:30:00  26.2   26.2  26.2  26.2     0.0   \n               3 2021-04-02 15:00:00  26.2   26.5  26.2  26.5    10.0   \n               4 2021-04-06 09:30:00  26.9   26.9  26.9  26.9     0.0   \n\n                     money  open_interest  \nZC107C750.XZCE 0  164220.0          451.0  \n               1  445060.0          536.0  \n               2   11900.0          537.0  \n               3  262830.0          564.0  \n               4    7440.0          555.0  \nZC107C740.XZCE 0  165600.0          420.0  \n               1   18650.0          420.0  \n               2       0.0          420.0  \n               3   25960.0          430.0  \n               4       0.0          428.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"get_bars 固定窗口"}
    - {"type":"list","listType":"ul","items":["历史范围：2019/12/2至今","学习材料：JQData 日分钟API清洗与处理规则"]}
    - {"type":"codeblock","language":"python","content":"get_bars(security, count, unit='1d',\n         fields=['date', 'open', 'close', 'high', 'low', 'volume', 'money','factor'],\n         include_now=False, start_dt=None,end_dt=None, fq_ref_date=None,df=True)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取各种时间周期的bar数据，bar的分割方式与主流行情软件相同， 同时还支持返回当前时刻所在 bar 的数据。"]}
    - {"type":"list","listType":"ul","items":["返回一个pandas.dataframe对象，可以按任意周期返回标的的开盘价、收盘价、最高价、最低价，成交数量,时段中成交的金额、复权因子同时也可以利用date数据查看所返回的数据是什么时刻的。"]}
    - {"type":"list","listType":"ul","items":["当天 09:00 ~ 15:00 的行情在 15:00 之后可以获取 ,当end_dt指定为当天尚未结束的交易时间时，会自动填充为上一个交易日结束的时间"]}
    - {"type":"paragraph","content":"get_bars 参数说明"}
    - {"type":"table","headers":["参数名称","参数说明","默认值"],"rows":[["security","指定标的，获取多个标的时需传入List","无默认值，必填项"],["start_dt","开始时间","无默认值，与count参数二选一"],["end_dt","结束时间","当前时间"],["count","表示获取 end_date 之前几个 unit 的数据","None,与start_dt参数二选一"],["unit","单位时间长度，即指定获取的时间频率","1d"],["fields","所获取数据的字段名称，即表头","默认['date', 'open', 'close', 'high', 'low'],还支持 'volume', 'money', 'open_interest'(持仓量，是期货和期权特有的字段), 'factor'(后复权因子)"],["include_now","表示是否包含end_dt所在的bar","默认最新的时间"],["fq_ref_date","复权基准日期","None,即返回不复权数据"],["df","指定返回的数据格式是否为dataframe格式","True"],["start_dt","查询的开始时间，当unit为天时传入的分时秒将被忽略(1.9.3新增参数)","None,与count参数二选一"],["skip_paused","是否跳过停牌(1.9.3新增参数)","True"]]}
    - {"type":"paragraph","content":"get_bars参数补充说明"}
    - {"type":"list","listType":"ul","items":["security支持的标的种类为【股票，基金，指数，可转债，期货，期权】","unit支持 ['Xm'(即X分钟),'1d'（1天）,'1w'（1周）,'1M'（1月） ]频率的数据，当频率单位为分钟（m）时，'X'可为任一大于0且小于240的自然数，以每天的开盘时间为起点,，不会跨交易日合并分钟bar数据。 指定单位为周或月时，周的起点固定为自然周内的第一个交易日，终点为自然周的最后一个交易日；月的起点为自然月内的第一个交易日，终点为自然月内的最后一个交易日。 例：比如股票交易时间为[09:30:00,11:30:00),[13:00:00,15:00:00),则每个交易日最多有240根1分钟bar用于分配撮合成Xm的数据；当240能被X整除时，每个交易日会固定划分出 ( 240 / unit) 根bar数据；当240不能被X整除时，每个交易日会固定划分出 (( 240 / unit) + 1 )根 bar数据； 注：商品期货等因为有特殊的早盘小休时间（10:15-10:30），所以有两种划分标准： 1）当指定的分钟bar为5m/15m/30m/60m/120m时，以自然时间来进行划分；举例如unit=30m来划分时，会将10:00-10:30的自然时间来进行划分为一个bar，但时间戳会以交易时间10:15来进行标记。 2）当指定的分钟bar为其他非标准频率时，以实际交易的分钟数来进行划分；","start_dt 不可与‘count’同时存在；当start_dt没有指定时分秒的时间戳时，时分秒的默认值为00:00:00；","end_dt","include_now 表示的是是否需要返回end_dt所在的bar。 例：比如'1m'，指定end_dt='20XX-XX-XX 15:00:00'时，若include_now=True，则会返回15:00:00为时间戳标记的bar，若include_now=False，则只会返回至14:59:00为时间戳标记的bar。","fq_ref_date 注：fq:复权选项(仅对股票/基金品种生效，生效的fields（字段）包括['open','close','high','low','volume','factor','high_limit','low_limit','avg','pre_close'] 当fq_ref_date =None时，返回不复权的数据； 当fq_ref_date 被指定时，返回基于fq_ref_date 的复权数据(定点复权)"]}
    - {"type":"paragraph","content":"fileds字段说明"}
    - {"type":"table","headers":["字段名称","中文名称","注释（特殊说明）"],"rows":[["date","日期",""],["open","时间段开始时价格",""],["close","时间段结束时价格",""],["low","时间段中的最低价",""],["high","时间段中的最高价",""],["volume","时间段中的成交的标的数量",""],["money","时间段中的成交的金额",""],["factor","复权因子","复权选项仅针对股票和基金品种有效，对于期权而言，复权因子被固定设置为1"],["open_interest","持仓量","期货/期权品种；反映当前时刻的持有数量"],["paused","是否停牌","0 正常；1 停牌 (限unit为1d时) (jqdatasdk1.9.5新增)"],["high_limit","当天涨停价","限unit为1d时 (jqdatasdk1.9.5新增)"],["low_limit","当天跌停价","限unit为1d时 (jqdatasdk1.9.5新增)"],["avg","当天均价","限unit为1d时 (jqdatasdk1.9.5新增)"],["pre_close","前收价","限unit为1d时 (jqdatasdk1.9.5新增)前天的收盘价。注：按天来获取的话，股票、指数、基金、可转债的是前一天的收盘价。（新股上市为IPO发行价，股票出现分红，则pre close是指昨天收盘价带分红拆股调整后的价格）;期货/期权是前一天的结算价；"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"list","listType":"ul","items":["获取一只期权"]}
    - {"type":"codeblock","language":"python","content":"#获取ZC107C740.XZCE期权合约在“2021-04-05”前5个时间单位的数据\n\ndf = get_bars('ZC107C740.XZCE', 5, unit='120m',fields=['open','close','low','high','volume','money','open_interest'],include_now=False,end_dt='2021-04-05')\nprint(df)\n                 date    open   close     low    high  volume      money  \\\n0 2006-03-13 11:30:00  2603.0  2603.0  2603.0  2603.0     0.0        0.0   \n1 2006-03-13 15:00:00  2603.0  2603.0  2603.0  2603.0     0.0        0.0   \n2 2006-03-14 11:00:00  2603.0  2581.0  2581.0  2603.0   210.0  5422000.0   \n3 2006-03-14 11:30:00  2581.0  2610.0  2581.0  2610.0    48.0  1252800.0   \n4 2006-03-14 15:00:00  2610.0  2595.0  2581.0  2610.0    30.0   774580.0   \n\n   open_interest  \n0         1526.0  \n1         1526.0  \n2         1736.0  \n3         1784.0  \n4         1812.0"}
    - {"type":"list","listType":"ul","items":["获取多支期权"]}
    - {"type":"codeblock","language":"python","content":"df = get_bars(['ZC107C740.XZCE','ZC107C750.XZCE'], 5, unit='120m',fields=['open','close','low','high','volume','money','open_interest'],include_now=False,end_dt='2021-04-05')\nprint(df)\n\n                                date  open  close   low  high  volume  \\\nZC107C750.XZCE 0 2021-04-01 23:00:00  21.7   23.6  21.7  24.2    69.0   \n               1 2021-04-02 11:00:00  23.8   23.6  23.5  24.5   187.0   \n               2 2021-04-02 11:30:00  23.6   22.8  22.8  23.7     5.0   \n               3 2021-04-02 15:00:00  22.8   25.2  22.3  25.2   112.0   \n               4 2021-04-06 09:30:00  23.7   24.8  23.7  24.8     3.0   \nZC107C740.XZCE 0 2021-04-01 23:00:00  24.8   27.6  24.8  27.6    60.0   \n               1 2021-04-02 11:00:00  27.6   26.2  26.2  27.6     7.0   \n               2 2021-04-02 11:30:00  26.2   26.2  26.2  26.2     0.0   \n               3 2021-04-02 15:00:00  26.2   26.5  26.2  26.5    10.0   \n               4 2021-04-06 09:30:00  26.9   26.9  26.9  26.9     0.0   \n\n                     money  open_interest  \nZC107C750.XZCE 0  164220.0          451.0  \n               1  445060.0          536.0  \n               2   11900.0          537.0  \n               3  262830.0          564.0  \n               4    7440.0          555.0  \nZC107C740.XZCE 0  165600.0          420.0  \n               1   18650.0          420.0  \n               2       0.0          420.0  \n               3   25960.0          430.0  \n               4       0.0          428.0"}
  suggestedFilename: "doc_JQDatadoc_9988_overview_get_bars_固定窗口"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9988"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# get_bars 固定窗口

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9988

## 描述

描述

## 内容

#### get_bars 固定窗口

- 历史范围：2019/12/2至今
- 学习材料：JQData 日分钟API清洗与处理规则

```python
get_bars(security, count, unit='1d',
         fields=['date', 'open', 'close', 'high', 'low', 'volume', 'money','factor'],
         include_now=False, start_dt=None,end_dt=None, fq_ref_date=None,df=True)
```

描述

- 获取各种时间周期的bar数据，bar的分割方式与主流行情软件相同， 同时还支持返回当前时刻所在 bar 的数据。

- 返回一个pandas.dataframe对象，可以按任意周期返回标的的开盘价、收盘价、最高价、最低价，成交数量,时段中成交的金额、复权因子同时也可以利用date数据查看所返回的数据是什么时刻的。

- 当天 09:00 ~ 15:00 的行情在 15:00 之后可以获取 ,当end_dt指定为当天尚未结束的交易时间时，会自动填充为上一个交易日结束的时间

get_bars 参数说明

| 参数名称 | 参数说明 | 默认值 |
| --- | --- | --- |
| security | 指定标的，获取多个标的时需传入List | 无默认值，必填项 |
| start_dt | 开始时间 | 无默认值，与count参数二选一 |
| end_dt | 结束时间 | 当前时间 |
| count | 表示获取 end_date 之前几个 unit 的数据 | None,与start_dt参数二选一 |
| unit | 单位时间长度，即指定获取的时间频率 | 1d |
| fields | 所获取数据的字段名称，即表头 | 默认['date', 'open', 'close', 'high', 'low'],还支持 'volume', 'money', 'open_interest'(持仓量，是期货和期权特有的字段), 'factor'(后复权因子) |
| include_now | 表示是否包含end_dt所在的bar | 默认最新的时间 |
| fq_ref_date | 复权基准日期 | None,即返回不复权数据 |
| df | 指定返回的数据格式是否为dataframe格式 | True |
| start_dt | 查询的开始时间，当unit为天时传入的分时秒将被忽略(1.9.3新增参数) | None,与count参数二选一 |
| skip_paused | 是否跳过停牌(1.9.3新增参数) | True |

get_bars参数补充说明

- security支持的标的种类为【股票，基金，指数，可转债，期货，期权】
- unit支持 ['Xm'(即X分钟),'1d'（1天）,'1w'（1周）,'1M'（1月） ]频率的数据，当频率单位为分钟（m）时，'X'可为任一大于0且小于240的自然数，以每天的开盘时间为起点,，不会跨交易日合并分钟bar数据。 指定单位为周或月时，周的起点固定为自然周内的第一个交易日，终点为自然周的最后一个交易日；月的起点为自然月内的第一个交易日，终点为自然月内的最后一个交易日。 例：比如股票交易时间为[09:30:00,11:30:00),[13:00:00,15:00:00),则每个交易日最多有240根1分钟bar用于分配撮合成Xm的数据；当240能被X整除时，每个交易日会固定划分出 ( 240 / unit) 根bar数据；当240不能被X整除时，每个交易日会固定划分出 (( 240 / unit) + 1 )根 bar数据； 注：商品期货等因为有特殊的早盘小休时间（10:15-10:30），所以有两种划分标准： 1）当指定的分钟bar为5m/15m/30m/60m/120m时，以自然时间来进行划分；举例如unit=30m来划分时，会将10:00-10:30的自然时间来进行划分为一个bar，但时间戳会以交易时间10:15来进行标记。 2）当指定的分钟bar为其他非标准频率时，以实际交易的分钟数来进行划分；
- start_dt 不可与‘count’同时存在；当start_dt没有指定时分秒的时间戳时，时分秒的默认值为00:00:00；
- end_dt
- include_now 表示的是是否需要返回end_dt所在的bar。 例：比如'1m'，指定end_dt='20XX-XX-XX 15:00:00'时，若include_now=True，则会返回15:00:00为时间戳标记的bar，若include_now=False，则只会返回至14:59:00为时间戳标记的bar。
- fq_ref_date 注：fq:复权选项(仅对股票/基金品种生效，生效的fields（字段）包括['open','close','high','low','volume','factor','high_limit','low_limit','avg','pre_close'] 当fq_ref_date =None时，返回不复权的数据； 当fq_ref_date 被指定时，返回基于fq_ref_date 的复权数据(定点复权)

fileds字段说明

| 字段名称 | 中文名称 | 注释（特殊说明） |
| --- | --- | --- |
| date | 日期 |  |
| open | 时间段开始时价格 |  |
| close | 时间段结束时价格 |  |
| low | 时间段中的最低价 |  |
| high | 时间段中的最高价 |  |
| volume | 时间段中的成交的标的数量 |  |
| money | 时间段中的成交的金额 |  |
| factor | 复权因子 | 复权选项仅针对股票和基金品种有效，对于期权而言，复权因子被固定设置为1 |
| open_interest | 持仓量 | 期货/期权品种；反映当前时刻的持有数量 |
| paused | 是否停牌 | 0 正常；1 停牌 (限unit为1d时) (jqdatasdk1.9.5新增) |
| high_limit | 当天涨停价 | 限unit为1d时 (jqdatasdk1.9.5新增) |
| low_limit | 当天跌停价 | 限unit为1d时 (jqdatasdk1.9.5新增) |
| avg | 当天均价 | 限unit为1d时 (jqdatasdk1.9.5新增) |
| pre_close | 前收价 | 限unit为1d时 (jqdatasdk1.9.5新增)前天的收盘价。注：按天来获取的话，股票、指数、基金、可转债的是前一天的收盘价。（新股上市为IPO发行价，股票出现分红，则pre close是指昨天收盘价带分红拆股调整后的价格）;期货/期权是前一天的结算价； |

###### 示例：

- 获取一只期权

```python
#获取ZC107C740.XZCE期权合约在“2021-04-05”前5个时间单位的数据

df = get_bars('ZC107C740.XZCE', 5, unit='120m',fields=['open','close','low','high','volume','money','open_interest'],include_now=False,end_dt='2021-04-05')
print(df)
                 date    open   close     low    high  volume      money  \
0 2006-03-13 11:30:00  2603.0  2603.0  2603.0  2603.0     0.0        0.0   
1 2006-03-13 15:00:00  2603.0  2603.0  2603.0  2603.0     0.0        0.0   
2 2006-03-14 11:00:00  2603.0  2581.0  2581.0  2603.0   210.0  5422000.0   
3 2006-03-14 11:30:00  2581.0  2610.0  2581.0  2610.0    48.0  1252800.0   
4 2006-03-14 15:00:00  2610.0  2595.0  2581.0  2610.0    30.0   774580.0   

   open_interest  
0         1526.0  
1         1526.0  
2         1736.0  
3         1784.0  
4         1812.0
```

- 获取多支期权

```python
df = get_bars(['ZC107C740.XZCE','ZC107C750.XZCE'], 5, unit='120m',fields=['open','close','low','high','volume','money','open_interest'],include_now=False,end_dt='2021-04-05')
print(df)

                                date  open  close   low  high  volume  \
ZC107C750.XZCE 0 2021-04-01 23:00:00  21.7   23.6  21.7  24.2    69.0   
               1 2021-04-02 11:00:00  23.8   23.6  23.5  24.5   187.0   
               2 2021-04-02 11:30:00  23.6   22.8  22.8  23.7     5.0   
               3 2021-04-02 15:00:00  22.8   25.2  22.3  25.2   112.0   
               4 2021-04-06 09:30:00  23.7   24.8  23.7  24.8     3.0   
ZC107C740.XZCE 0 2021-04-01 23:00:00  24.8   27.6  24.8  27.6    60.0   
               1 2021-04-02 11:00:00  27.6   26.2  26.2  27.6     7.0   
               2 2021-04-02 11:30:00  26.2   26.2  26.2  26.2     0.0   
               3 2021-04-02 15:00:00  26.2   26.5  26.2  26.5    10.0   
               4 2021-04-06 09:30:00  26.9   26.9  26.9  26.9     0.0   

                     money  open_interest  
ZC107C750.XZCE 0  164220.0          451.0  
               1  445060.0          536.0  
               2   11900.0          537.0  
               3  262830.0          564.0  
               4    7440.0          555.0  
ZC107C740.XZCE 0  165600.0          420.0  
               1   18650.0          420.0  
               2       0.0          420.0  
               3   25960.0          430.0  
               4       0.0          428.0
```
