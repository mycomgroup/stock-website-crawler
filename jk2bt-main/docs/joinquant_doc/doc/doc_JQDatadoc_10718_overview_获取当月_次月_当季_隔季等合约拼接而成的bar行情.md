---
id: "url-364960b3"
type: "website"
title: "获取当月/次月/当季/隔季等合约拼接而成的bar行情"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10718"
description: "历史范围：2005年至今;"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:15.449Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10718"
  headings:
    - {"level":3,"text":"获取当月/次月/当季/隔季等合约拼接而成的bar行情","id":""}
    - {"level":5,"text":"示例：","id":""}
  paragraphs:
    - "历史范围：2005年至今;"
    - "描述"
    - "参数"
  lists:
    - {"type":"ul","items":["get_order_future_bar 获取当月/次月/当季/隔季等合约拼接而成的bar数据"]}
    - {"type":"ul","items":["symbol：品种代码,如 'AG'","future_type：合约类型，按当前可交易的合约顺序推算，0为当月，1为次月，也可以按季度，'0q'为当季(最近一个季月) 、'1q'为次季....如该品种最多可交易的合约仅有12个自然月的合约，此时参数指定为大于等于12或大于等于4q时，【即对应的第13个月份及第五个季月的合约)，则仅按照当前可交易的最后一个合约（或季月）拼接。","start_dt：开始时间","end_dt：结束时间","unit：bar频率，只支持 (x)m 或者1d , 划分方式同 get_bars , 不支持1w和1M","fields：获取字段,同get_bars , 可额外指定\"code\" 字段, 表示当前bar的行情是使用的哪个合约拼接的","include_now：是否包含当前bar"]}
    - {"type":"ul","items":["返回dataframe"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"get_order_future_bar(symbol, future_type, start_dt, end_dt, unit='1d', fields=('code','date', 'open', 'high', 'low', 'close', 'volume', 'money', 'open_interest'))"}
    - {"language":"python","code":"df=get_order_future_bar(symbol='AG', future_type='4q',start_dt='2024-04-05', end_dt='2024-05-05', unit='5m', \n                     fields=('code','date','open','high','low','close','volume','money','open_interest'))\nprint(df[:2])\n\n          code                date    open    high     low   close  volume  \\\n0  AG2503.XSGE 2024-04-08 09:05:00  6888.0  6888.0  6805.0  6837.0   308.0   \n1  AG2503.XSGE 2024-04-08 09:10:00  6839.0  6893.0  6835.0  6878.0   146.0   \n\n        money  open_interest  \n0  31585680.0         1357.0  \n1  15032670.0         1389.0"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取当月/次月/当季/隔季等合约拼接而成的bar行情"}
    - {"type":"paragraph","content":"历史范围：2005年至今;"}
    - {"type":"codeblock","language":"python","content":"get_order_future_bar(symbol, future_type, start_dt, end_dt, unit='1d', fields=('code','date', 'open', 'high', 'low', 'close', 'volume', 'money', 'open_interest'))"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["get_order_future_bar 获取当月/次月/当季/隔季等合约拼接而成的bar数据"]}
    - {"type":"paragraph","content":"参数"}
    - {"type":"list","listType":"ul","items":["symbol：品种代码,如 'AG'","future_type：合约类型，按当前可交易的合约顺序推算，0为当月，1为次月，也可以按季度，'0q'为当季(最近一个季月) 、'1q'为次季....如该品种最多可交易的合约仅有12个自然月的合约，此时参数指定为大于等于12或大于等于4q时，【即对应的第13个月份及第五个季月的合约)，则仅按照当前可交易的最后一个合约（或季月）拼接。","start_dt：开始时间","end_dt：结束时间","unit：bar频率，只支持 (x)m 或者1d , 划分方式同 get_bars , 不支持1w和1M","fields：获取字段,同get_bars , 可额外指定\"code\" 字段, 表示当前bar的行情是使用的哪个合约拼接的","include_now：是否包含当前bar"]}
    - {"type":"heading","level":5,"content":"示例："}
    - {"type":"list","listType":"ul","items":["返回dataframe"]}
    - {"type":"codeblock","language":"python","content":"df=get_order_future_bar(symbol='AG', future_type='4q',start_dt='2024-04-05', end_dt='2024-05-05', unit='5m', \n                     fields=('code','date','open','high','low','close','volume','money','open_interest'))\nprint(df[:2])\n\n          code                date    open    high     low   close  volume  \\\n0  AG2503.XSGE 2024-04-08 09:05:00  6888.0  6888.0  6805.0  6837.0   308.0   \n1  AG2503.XSGE 2024-04-08 09:10:00  6839.0  6893.0  6835.0  6878.0   146.0   \n\n        money  open_interest  \n0  31585680.0         1357.0  \n1  15032670.0         1389.0"}
  suggestedFilename: "doc_JQDatadoc_10718_overview_获取当月_次月_当季_隔季等合约拼接而成的bar行情"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10718"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取当月/次月/当季/隔季等合约拼接而成的bar行情

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10718

## 描述

历史范围：2005年至今;

## 内容

#### 获取当月/次月/当季/隔季等合约拼接而成的bar行情

历史范围：2005年至今;

```python
get_order_future_bar(symbol, future_type, start_dt, end_dt, unit='1d', fields=('code','date', 'open', 'high', 'low', 'close', 'volume', 'money', 'open_interest'))
```

描述

- get_order_future_bar 获取当月/次月/当季/隔季等合约拼接而成的bar数据

参数

- symbol：品种代码,如 'AG'
- future_type：合约类型，按当前可交易的合约顺序推算，0为当月，1为次月，也可以按季度，'0q'为当季(最近一个季月) 、'1q'为次季....如该品种最多可交易的合约仅有12个自然月的合约，此时参数指定为大于等于12或大于等于4q时，【即对应的第13个月份及第五个季月的合约)，则仅按照当前可交易的最后一个合约（或季月）拼接。
- start_dt：开始时间
- end_dt：结束时间
- unit：bar频率，只支持 (x)m 或者1d , 划分方式同 get_bars , 不支持1w和1M
- fields：获取字段,同get_bars , 可额外指定"code" 字段, 表示当前bar的行情是使用的哪个合约拼接的
- include_now：是否包含当前bar

###### 示例：

- 返回dataframe

```python
df=get_order_future_bar(symbol='AG', future_type='4q',start_dt='2024-04-05', end_dt='2024-05-05', unit='5m', 
                     fields=('code','date','open','high','low','close','volume','money','open_interest'))
print(df[:2])

          code                date    open    high     low   close  volume  \
0  AG2503.XSGE 2024-04-08 09:05:00  6888.0  6888.0  6805.0  6837.0   308.0   
1  AG2503.XSGE 2024-04-08 09:10:00  6839.0  6893.0  6835.0  6878.0   146.0   

        money  open_interest  
0  31585680.0         1357.0  
1  15032670.0         1389.0
```
