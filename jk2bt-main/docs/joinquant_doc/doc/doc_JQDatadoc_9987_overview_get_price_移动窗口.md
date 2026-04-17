---
id: "url-7a226f31"
type: "website"
title: "get_price 移动窗口"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9987"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:24:17.744Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9987"
  headings:
    - {"level":3,"text":"get_price 移动窗口","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "描述"
    - "注意"
    - "常见问题"
    - "get_price 参数说明"
    - "get_price参数补充说明"
    - "fields字段说明"
  lists:
    - {"type":"ul","items":["历史范围：2019/12/2至今","学习材料：JQData 日分钟API清洗与处理规则"]}
    - {"type":"ul","items":["当可以获取指定标的一天或一分钟行情数据，返回标的的开盘价、收盘价、最高价、最低价，成交的数量,时段中成交的金额、复权因子、时间段中的涨停价、时段中跌停价、时段中平均价，是否停牌，前一天收盘价等，同时也可以利用date数据查看所返回的数据是什么时刻的。","panel=True时且pandas<0.25时返回[pandas.Panel]对象 , panel= False 或 pandas>=0.25时返回[pandas.DataFrame]对象","获取一支或者多只标的的行情"]}
    - {"type":"ul","items":["当天 09:00 ~ 15:00 的行情在 15:00 之后可以获取 ,当end_date指定为当天尚未结束的交易时间时，会自动填充为上一个交易日的盘后15点时间","获取一支或者多只标的1天或者1分钟行情；","frequency为非一天或者一分钟，请使用get_bars;","标识时间为09:32:00的1分钟k线，其数据时间为09:31:00至09:31:59；"]}
    - {"type":"ul","items":["security支持的标的种类为【股票，基金，指数，可转债，期货，期权】","start_date 不可与‘count’同时存在；当start_date没有指定时分秒的时间戳时，时分秒的默认值为00:00:00； 注：当frequency不为1d/1m时，将从start_date开始,从前向后将每X个的(1m/1d)的数据合并成一条,一直到取到end_date为止","end_date 当end_date没有指定时分秒的时间戳，时分秒的默认值为00:00:00，所以此时返回的数据不包括 end_date这天； 当end_date指定为当天尚未结束的交易时间时，会自动填充为上一个交易日的盘后时间。 注：当frequency不为1d/1m时，可与‘count’与‘start_date’分开搭配获得不同的使用效果","count 只与‘end_date’搭配使用； 注：当指定了count 时，从end_date开始, 从后向前将每X个的(1m/1d)的数据合并成一条,一直到取到足够的数量","frequency 支持[ 'Xm'(X分钟) , 'Xd'(X天) , 'Daily'(即1天,等于1d) , '1m'(即1分钟，等于1m)]， 可指定任意数量长度，即'X'可为任一大于0的自然数 ，例如'5d','3m','10m'等 注：指定单位为分钟时，会跨交易日合并分钟bar数据","skip_paused 如果不跳过, 停牌时会使用停牌前的数据填充(如fill_paused=True)，上市前或者退市后数据都为 nan。","fill_paused True 表示用pre_close价格填充; False 表示使用NAN填充停牌的股票价格。","fq 'pre'：前复权 'none'：不复权, 返回实际价格 'post'：后复权 注：fq:复权选项(仅对股票/基金品种生效，生效的fields（字段）包括['open','close','high','low','volume','factor','high_limit','low_limit','avg','pre_close']","panel 当本地pandas版本小于0.25时，指定panel=True 表示让数据可以返回panel格式； 当本地pandas版本>0.25 或 指定panel = False时，数据将返回dataframe格式；"]}
    - {"type":"ul","items":["获取一只期权"]}
    - {"type":"ul","items":["获取多只期权"]}
    - {"type":"ul","items":["获取夜盘"]}
  tables:
    - {"caption":"","headers":["参数名称","参数说明","默认值"],"rows":[["security","指定标的，获取多个标的时需传入List","无默认值，必填项"],["start_date","开始时间","2015/1/1 0:00:00"],["end_date","结束时间","2015/12/31 0:00:00"],["count","表示获取 end_date 之前几个 frequency 的数据","无默认值，必填项"],["frequency","单位时间长度，即指定获取的时间频率","无默认值，必填项"],["fields","所获取数据的字段名称，即表头","['open','close','high','low','volume','money']"],["skip_paused","是否跳过不交易日期(含：停牌/未上市/退市后的日期)","True"],["fill_paused","对于停牌股票的价格处理","True"],["fq","复权选项","pre"],["panel","当本地pandas版本小于0.25时，指定返回的数据格式是否为panel","True"]]}
    - {"caption":"","headers":["字段名称","中文名称","注释（特殊说明）"],"rows":[["open","时间段开始时价格",""],["close","时间段结束时价格",""],["low","时间段中的最低价",""],["high","时间段中的最高价",""],["volume","时间段中的成交的标的数量",""],["money","时间段中的成交的金额",""],["factor","复权因子","复权选项仅针对股票和基金品种有效，对于期权而言，复权因子被固定设置为1"],["high_limit","指定交易日的当日涨停价",""],["low_limit","指定交易日的当日跌停价",""],["avg","时间段中的平均价","成交额除以成交量；"],["pre_close","前一个单位时间结束时的价格,按天则是前一天的收盘价","前一个单位时间结束时的价格。注：按天来获取的话，股票、指数、基金、可转债的是前一天的收盘价。（新股上市为IPO发行价，股票出现分红，则pre close是指昨天收盘价带分红拆股调整后的价格）;期货/期权是前一天的结算价；"],["paused","bool值,股票是否停牌;","当paused=1，即停牌时 open/close/low/high/pre_close 都等于停牌前的收盘价, volume=money=0"],["open_interest","持仓量","期货/期权品种的持仓量"]]}
  codeBlocks:
    - {"language":"python","code":"get_price(security, start_date=None, end_date=None, frequency='daily', fields=['open','close','low','high','volume','money','factor',\n        'high_limit','low_limit','avg','pre_close','paused'], skip_paused=False, fq='pre', count=None)"}
    - {"language":"python","code":"#获取'ZC107C740.XZCE'指定时间周期为5m的期权行情数据\ndf =get_price('ZC107C740.XZCE', start_date= '2021-04-01 09:00:00',end_date='2021-04-05 14:00:00', \n              frequency='1d', fields=['open','close','low','high','volume','money','open_interest','pre_close'])\n\nprint(df[:4])\n            open  close   low  high  volume     money  open_interest  \\\n2021-04-01  26.0   25.8  25.8  26.2    24.0   62400.0          370.0   \n2021-04-02  27.6   26.5  26.2  27.6    79.0  215900.0          428.0   \n\n            pre_close  \n2021-04-01       26.3  \n2021-04-02       25.8"}
    - {"language":"python","code":"# panel=True时且pandas<0.25时返回[pandas.Panel]对象 , panel= False 或 pandas>=0.25时返回panel=get_price(['ZC107C740.XZCE','ZC107C750.XZCE'] ,count=2, panel=True,end_date='2021-04-05')\n#返回[pandas.DataFrame]对象,行索引是[datetime.datetime]对象, 列索引是股票代号\ndf=panel['open']\nprint(df)\n\n            ZC107C740.XZCE  ZC107C750.XZCE\n2021-04-01            26.0            23.1\n2021-04-02            27.6            22.6"}
    - {"language":"python","code":"df =get_price('ZC107C740.XZCE', start_date= '2021-04-01 09:00:00',end_date='2021-04-05 14:00:00', \n              frequency='60m', fields=['open','close','low','high','volume','money'])\n\nall_trade_days = pd.to_datetime(get_all_trade_days())\ndf['trade_date'] = df.index\ndf.loc[df.index.time > pd.to_datetime('16:00').time(),'trade_date'] += datetime.timedelta(days=1) #夜盘的+1天\ndf['trade_date'] = all_trade_days [ np.searchsorted( all_trade_days , df.trade_date.dt.date.values , side='left') ]\ndf"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"get_price 移动窗口"}
    - {"type":"list","listType":"ul","items":["历史范围：2019/12/2至今","学习材料：JQData 日分钟API清洗与处理规则"]}
    - {"type":"codeblock","language":"python","content":"get_price(security, start_date=None, end_date=None, frequency='daily', fields=['open','close','low','high','volume','money','factor',\n        'high_limit','low_limit','avg','pre_close','paused'], skip_paused=False, fq='pre', count=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["当可以获取指定标的一天或一分钟行情数据，返回标的的开盘价、收盘价、最高价、最低价，成交的数量,时段中成交的金额、复权因子、时间段中的涨停价、时段中跌停价、时段中平均价，是否停牌，前一天收盘价等，同时也可以利用date数据查看所返回的数据是什么时刻的。","panel=True时且pandas<0.25时返回[pandas.Panel]对象 , panel= False 或 pandas>=0.25时返回[pandas.DataFrame]对象","获取一支或者多只标的的行情"]}
    - {"type":"paragraph","content":"注意"}
    - {"type":"list","listType":"ul","items":["当天 09:00 ~ 15:00 的行情在 15:00 之后可以获取 ,当end_date指定为当天尚未结束的交易时间时，会自动填充为上一个交易日的盘后15点时间","获取一支或者多只标的1天或者1分钟行情；","frequency为非一天或者一分钟，请使用get_bars;","标识时间为09:32:00的1分钟k线，其数据时间为09:31:00至09:31:59；"]}
    - {"type":"paragraph","content":"常见问题"}
    - {"type":"paragraph","content":"get_price 参数说明"}
    - {"type":"table","headers":["参数名称","参数说明","默认值"],"rows":[["security","指定标的，获取多个标的时需传入List","无默认值，必填项"],["start_date","开始时间","2015/1/1 0:00:00"],["end_date","结束时间","2015/12/31 0:00:00"],["count","表示获取 end_date 之前几个 frequency 的数据","无默认值，必填项"],["frequency","单位时间长度，即指定获取的时间频率","无默认值，必填项"],["fields","所获取数据的字段名称，即表头","['open','close','high','low','volume','money']"],["skip_paused","是否跳过不交易日期(含：停牌/未上市/退市后的日期)","True"],["fill_paused","对于停牌股票的价格处理","True"],["fq","复权选项","pre"],["panel","当本地pandas版本小于0.25时，指定返回的数据格式是否为panel","True"]]}
    - {"type":"paragraph","content":"get_price参数补充说明"}
    - {"type":"list","listType":"ul","items":["security支持的标的种类为【股票，基金，指数，可转债，期货，期权】","start_date 不可与‘count’同时存在；当start_date没有指定时分秒的时间戳时，时分秒的默认值为00:00:00； 注：当frequency不为1d/1m时，将从start_date开始,从前向后将每X个的(1m/1d)的数据合并成一条,一直到取到end_date为止","end_date 当end_date没有指定时分秒的时间戳，时分秒的默认值为00:00:00，所以此时返回的数据不包括 end_date这天； 当end_date指定为当天尚未结束的交易时间时，会自动填充为上一个交易日的盘后时间。 注：当frequency不为1d/1m时，可与‘count’与‘start_date’分开搭配获得不同的使用效果","count 只与‘end_date’搭配使用； 注：当指定了count 时，从end_date开始, 从后向前将每X个的(1m/1d)的数据合并成一条,一直到取到足够的数量","frequency 支持[ 'Xm'(X分钟) , 'Xd'(X天) , 'Daily'(即1天,等于1d) , '1m'(即1分钟，等于1m)]， 可指定任意数量长度，即'X'可为任一大于0的自然数 ，例如'5d','3m','10m'等 注：指定单位为分钟时，会跨交易日合并分钟bar数据","skip_paused 如果不跳过, 停牌时会使用停牌前的数据填充(如fill_paused=True)，上市前或者退市后数据都为 nan。","fill_paused True 表示用pre_close价格填充; False 表示使用NAN填充停牌的股票价格。","fq 'pre'：前复权 'none'：不复权, 返回实际价格 'post'：后复权 注：fq:复权选项(仅对股票/基金品种生效，生效的fields（字段）包括['open','close','high','low','volume','factor','high_limit','low_limit','avg','pre_close']","panel 当本地pandas版本小于0.25时，指定panel=True 表示让数据可以返回panel格式； 当本地pandas版本>0.25 或 指定panel = False时，数据将返回dataframe格式；"]}
    - {"type":"paragraph","content":"fields字段说明"}
    - {"type":"table","headers":["字段名称","中文名称","注释（特殊说明）"],"rows":[["open","时间段开始时价格",""],["close","时间段结束时价格",""],["low","时间段中的最低价",""],["high","时间段中的最高价",""],["volume","时间段中的成交的标的数量",""],["money","时间段中的成交的金额",""],["factor","复权因子","复权选项仅针对股票和基金品种有效，对于期权而言，复权因子被固定设置为1"],["high_limit","指定交易日的当日涨停价",""],["low_limit","指定交易日的当日跌停价",""],["avg","时间段中的平均价","成交额除以成交量；"],["pre_close","前一个单位时间结束时的价格,按天则是前一天的收盘价","前一个单位时间结束时的价格。注：按天来获取的话，股票、指数、基金、可转债的是前一天的收盘价。（新股上市为IPO发行价，股票出现分红，则pre close是指昨天收盘价带分红拆股调整后的价格）;期货/期权是前一天的结算价；"],["paused","bool值,股票是否停牌;","当paused=1，即停牌时 open/close/low/high/pre_close 都等于停牌前的收盘价, volume=money=0"],["open_interest","持仓量","期货/期权品种的持仓量"]]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"list","listType":"ul","items":["获取一只期权"]}
    - {"type":"codeblock","language":"python","content":"#获取'ZC107C740.XZCE'指定时间周期为5m的期权行情数据\ndf =get_price('ZC107C740.XZCE', start_date= '2021-04-01 09:00:00',end_date='2021-04-05 14:00:00', \n              frequency='1d', fields=['open','close','low','high','volume','money','open_interest','pre_close'])\n\nprint(df[:4])\n            open  close   low  high  volume     money  open_interest  \\\n2021-04-01  26.0   25.8  25.8  26.2    24.0   62400.0          370.0   \n2021-04-02  27.6   26.5  26.2  27.6    79.0  215900.0          428.0   \n\n            pre_close  \n2021-04-01       26.3  \n2021-04-02       25.8"}
    - {"type":"list","listType":"ul","items":["获取多只期权"]}
    - {"type":"codeblock","language":"python","content":"# panel=True时且pandas<0.25时返回[pandas.Panel]对象 , panel= False 或 pandas>=0.25时返回panel=get_price(['ZC107C740.XZCE','ZC107C750.XZCE'] ,count=2, panel=True,end_date='2021-04-05')\n#返回[pandas.DataFrame]对象,行索引是[datetime.datetime]对象, 列索引是股票代号\ndf=panel['open']\nprint(df)\n\n            ZC107C740.XZCE  ZC107C750.XZCE\n2021-04-01            26.0            23.1\n2021-04-02            27.6            22.6"}
    - {"type":"list","listType":"ul","items":["获取夜盘"]}
    - {"type":"codeblock","language":"python","content":"df =get_price('ZC107C740.XZCE', start_date= '2021-04-01 09:00:00',end_date='2021-04-05 14:00:00', \n              frequency='60m', fields=['open','close','low','high','volume','money'])\n\nall_trade_days = pd.to_datetime(get_all_trade_days())\ndf['trade_date'] = df.index\ndf.loc[df.index.time > pd.to_datetime('16:00').time(),'trade_date'] += datetime.timedelta(days=1) #夜盘的+1天\ndf['trade_date'] = all_trade_days [ np.searchsorted( all_trade_days , df.trade_date.dt.date.values , side='left') ]\ndf"}
  suggestedFilename: "doc_JQDatadoc_9987_overview_get_price_移动窗口"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "9987"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# get_price 移动窗口

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9987

## 描述

描述

## 内容

#### get_price 移动窗口

- 历史范围：2019/12/2至今
- 学习材料：JQData 日分钟API清洗与处理规则

```python
get_price(security, start_date=None, end_date=None, frequency='daily', fields=['open','close','low','high','volume','money','factor',
        'high_limit','low_limit','avg','pre_close','paused'], skip_paused=False, fq='pre', count=None)
```

描述

- 当可以获取指定标的一天或一分钟行情数据，返回标的的开盘价、收盘价、最高价、最低价，成交的数量,时段中成交的金额、复权因子、时间段中的涨停价、时段中跌停价、时段中平均价，是否停牌，前一天收盘价等，同时也可以利用date数据查看所返回的数据是什么时刻的。
- panel=True时且pandas<0.25时返回[pandas.Panel]对象 , panel= False 或 pandas>=0.25时返回[pandas.DataFrame]对象
- 获取一支或者多只标的的行情

注意

- 当天 09:00 ~ 15:00 的行情在 15:00 之后可以获取 ,当end_date指定为当天尚未结束的交易时间时，会自动填充为上一个交易日的盘后15点时间
- 获取一支或者多只标的1天或者1分钟行情；
- frequency为非一天或者一分钟，请使用get_bars;
- 标识时间为09:32:00的1分钟k线，其数据时间为09:31:00至09:31:59；

常见问题

get_price 参数说明

| 参数名称 | 参数说明 | 默认值 |
| --- | --- | --- |
| security | 指定标的，获取多个标的时需传入List | 无默认值，必填项 |
| start_date | 开始时间 | 2015/1/1 0:00:00 |
| end_date | 结束时间 | 2015/12/31 0:00:00 |
| count | 表示获取 end_date 之前几个 frequency 的数据 | 无默认值，必填项 |
| frequency | 单位时间长度，即指定获取的时间频率 | 无默认值，必填项 |
| fields | 所获取数据的字段名称，即表头 | ['open','close','high','low','volume','money'] |
| skip_paused | 是否跳过不交易日期(含：停牌/未上市/退市后的日期) | True |
| fill_paused | 对于停牌股票的价格处理 | True |
| fq | 复权选项 | pre |
| panel | 当本地pandas版本小于0.25时，指定返回的数据格式是否为panel | True |

get_price参数补充说明

- security支持的标的种类为【股票，基金，指数，可转债，期货，期权】
- start_date 不可与‘count’同时存在；当start_date没有指定时分秒的时间戳时，时分秒的默认值为00:00:00； 注：当frequency不为1d/1m时，将从start_date开始,从前向后将每X个的(1m/1d)的数据合并成一条,一直到取到end_date为止
- end_date 当end_date没有指定时分秒的时间戳，时分秒的默认值为00:00:00，所以此时返回的数据不包括 end_date这天； 当end_date指定为当天尚未结束的交易时间时，会自动填充为上一个交易日的盘后时间。 注：当frequency不为1d/1m时，可与‘count’与‘start_date’分开搭配获得不同的使用效果
- count 只与‘end_date’搭配使用； 注：当指定了count 时，从end_date开始, 从后向前将每X个的(1m/1d)的数据合并成一条,一直到取到足够的数量
- frequency 支持[ 'Xm'(X分钟) , 'Xd'(X天) , 'Daily'(即1天,等于1d) , '1m'(即1分钟，等于1m)]， 可指定任意数量长度，即'X'可为任一大于0的自然数 ，例如'5d','3m','10m'等 注：指定单位为分钟时，会跨交易日合并分钟bar数据
- skip_paused 如果不跳过, 停牌时会使用停牌前的数据填充(如fill_paused=True)，上市前或者退市后数据都为 nan。
- fill_paused True 表示用pre_close价格填充; False 表示使用NAN填充停牌的股票价格。
- fq 'pre'：前复权 'none'：不复权, 返回实际价格 'post'：后复权 注：fq:复权选项(仅对股票/基金品种生效，生效的fields（字段）包括['open','close','high','low','volume','factor','high_limit','low_limit','avg','pre_close']
- panel 当本地pandas版本小于0.25时，指定panel=True 表示让数据可以返回panel格式； 当本地pandas版本>0.25 或 指定panel = False时，数据将返回dataframe格式；

fields字段说明

| 字段名称 | 中文名称 | 注释（特殊说明） |
| --- | --- | --- |
| open | 时间段开始时价格 |  |
| close | 时间段结束时价格 |  |
| low | 时间段中的最低价 |  |
| high | 时间段中的最高价 |  |
| volume | 时间段中的成交的标的数量 |  |
| money | 时间段中的成交的金额 |  |
| factor | 复权因子 | 复权选项仅针对股票和基金品种有效，对于期权而言，复权因子被固定设置为1 |
| high_limit | 指定交易日的当日涨停价 |  |
| low_limit | 指定交易日的当日跌停价 |  |
| avg | 时间段中的平均价 | 成交额除以成交量； |
| pre_close | 前一个单位时间结束时的价格,按天则是前一天的收盘价 | 前一个单位时间结束时的价格。注：按天来获取的话，股票、指数、基金、可转债的是前一天的收盘价。（新股上市为IPO发行价，股票出现分红，则pre close是指昨天收盘价带分红拆股调整后的价格）;期货/期权是前一天的结算价； |
| paused | bool值,股票是否停牌; | 当paused=1，即停牌时 open/close/low/high/pre_close 都等于停牌前的收盘价, volume=money=0 |
| open_interest | 持仓量 | 期货/期权品种的持仓量 |

###### 示例：

- 获取一只期权

```python
#获取'ZC107C740.XZCE'指定时间周期为5m的期权行情数据
df =get_price('ZC107C740.XZCE', start_date= '2021-04-01 09:00:00',end_date='2021-04-05 14:00:00', 
              frequency='1d', fields=['open','close','low','high','volume','money','open_interest','pre_close'])

print(df[:4])
            open  close   low  high  volume     money  open_interest  \
2021-04-01  26.0   25.8  25.8  26.2    24.0   62400.0          370.0   
2021-04-02  27.6   26.5  26.2  27.6    79.0  215900.0          428.0   

            pre_close  
2021-04-01       26.3  
2021-04-02       25.8
```

- 获取多只期权

```python
# panel=True时且pandas<0.25时返回[pandas.Panel]对象 , panel= False 或 pandas>=0.25时返回panel=get_price(['ZC107C740.XZCE','ZC107C750.XZCE'] ,count=2, panel=True,end_date='2021-04-05')
#返回[pandas.DataFrame]对象,行索引是[datetime.datetime]对象, 列索引是股票代号
df=panel['open']
print(df)

            ZC107C740.XZCE  ZC107C750.XZCE
2021-04-01            26.0            23.1
2021-04-02            27.6            22.6
```

```python
df =get_price('ZC107C740.XZCE', start_date= '2021-04-01 09:00:00',end_date='2021-04-05 14:00:00', 
              frequency='60m', fields=['open','close','low','high','volume','money'])

all_trade_days = pd.to_datetime(get_all_trade_days())
df['trade_date'] = df.index
df.loc[df.index.time > pd.to_datetime('16:00').time(),'trade_date'] += datetime.timedelta(days=1) #夜盘的+1天
df['trade_date'] = all_trade_days [ np.searchsorted( all_trade_days , df.trade_date.dt.date.values , side='left') ]
df
```
