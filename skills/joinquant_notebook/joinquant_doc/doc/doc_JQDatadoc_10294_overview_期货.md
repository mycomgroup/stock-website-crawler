---
id: "url-36497284"
type: "website"
title: "期货"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10294"
description: "A: 2020年后期货成交量是单边计算的,因为多空成交相同,而持仓机构的成交量指的是他自身的成交量,比如；某个会员机构多头成交2手，空头成交1手，它必须要与别的会员成交，只能记3手。 可以和交易所官网数据进行对比,比如中金所: http://www.cffex.com.cn/ccpm/"
source: ""
tags: []
crawl_time: "2026-03-27T07:29:36.572Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10294"
  headings:
    - {"level":3,"text":"期货","id":""}
    - {"level":5,"text":"常见数据问题>>>","id":"httpsdocsqqcomdocdrwjyevdovfpmafpb"}
  paragraphs:
    - "A: 2020年后期货成交量是单边计算的,因为多空成交相同,而持仓机构的成交量指的是他自身的成交量,比如；某个会员机构多头成交2手，空头成交1手，它必须要与别的会员成交，只能记3手。 可以和交易所官网数据进行对比,比如中金所: http://www.cffex.com.cn/ccpm/"
    - "4.郑商所成交额有负值出现，数据不准确？ A：郑商所没有直接披露tick数据累计成交额，但实际上，CTP成交额通过计算【日成交均价与日累计成交量的乘积】得出的。 由于CTP日成交均价精度的原因，可能出现tick计算的累计成交额不准确甚至出现由大变小的情况 分钟数据是由tick数据合成的，【成交额字段含义为时间段中的成交的金额 】，因此可能不准确甚至出现负数"
  lists:
    - {"type":"ol","items":["为什么某期货合约日行情数据的总成交量会小于中金所披露的持仓会员前20名的成交量?"]}
    - {"type":"ol","items":["为什么郑商所ticks数据不是每0.5秒更新？ A：交易所之间的规则不一样，郑商所只有秒"]}
    - {"type":"ol","items":["有关tick数据--tick 时间戳重复 A：这种情况一般出现在郑商所，是正常的。见下方截图"]}
  tables: []
  codeBlocks: []
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"期货"}
    - {"type":"heading","level":5,"content":"常见数据问题>>>"}
    - {"type":"list","listType":"ol","items":["为什么某期货合约日行情数据的总成交量会小于中金所披露的持仓会员前20名的成交量?"]}
    - {"type":"paragraph","content":"A: 2020年后期货成交量是单边计算的,因为多空成交相同,而持仓机构的成交量指的是他自身的成交量,比如；某个会员机构多头成交2手，空头成交1手，它必须要与别的会员成交，只能记3手。 可以和交易所官网数据进行对比,比如中金所: http://www.cffex.com.cn/ccpm/"}
    - {"type":"hr"}
    - {"type":"list","listType":"ol","items":["为什么郑商所ticks数据不是每0.5秒更新？ A：交易所之间的规则不一样，郑商所只有秒"]}
    - {"type":"hr"}
    - {"type":"list","listType":"ol","items":["有关tick数据--tick 时间戳重复 A：这种情况一般出现在郑商所，是正常的。见下方截图"]}
    - {"type":"paragraph","content":"4.郑商所成交额有负值出现，数据不准确？ A：郑商所没有直接披露tick数据累计成交额，但实际上，CTP成交额通过计算【日成交均价与日累计成交量的乘积】得出的。 由于CTP日成交均价精度的原因，可能出现tick计算的累计成交额不准确甚至出现由大变小的情况 分钟数据是由tick数据合成的，【成交额字段含义为时间段中的成交的金额 】，因此可能不准确甚至出现负数"}
    - {"type":"hr"}
  suggestedFilename: "doc_JQDatadoc_10294_overview_期货"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10294"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 期货

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10294

## 描述

A: 2020年后期货成交量是单边计算的,因为多空成交相同,而持仓机构的成交量指的是他自身的成交量,比如；某个会员机构多头成交2手，空头成交1手，它必须要与别的会员成交，只能记3手。 可以和交易所官网数据进行对比,比如中金所: http://www.cffex.com.cn/ccpm/

## 内容

#### 期货

###### 常见数据问题>>>

1. 为什么某期货合约日行情数据的总成交量会小于中金所披露的持仓会员前20名的成交量?

A: 2020年后期货成交量是单边计算的,因为多空成交相同,而持仓机构的成交量指的是他自身的成交量,比如；某个会员机构多头成交2手，空头成交1手，它必须要与别的会员成交，只能记3手。 可以和交易所官网数据进行对比,比如中金所: http://www.cffex.com.cn/ccpm/

---

1. 为什么郑商所ticks数据不是每0.5秒更新？ A：交易所之间的规则不一样，郑商所只有秒

---

1. 有关tick数据--tick 时间戳重复 A：这种情况一般出现在郑商所，是正常的。见下方截图

4.郑商所成交额有负值出现，数据不准确？ A：郑商所没有直接披露tick数据累计成交额，但实际上，CTP成交额通过计算【日成交均价与日累计成交量的乘积】得出的。 由于CTP日成交均价精度的原因，可能出现tick计算的累计成交额不准确甚至出现由大变小的情况 分钟数据是由tick数据合成的，【成交额字段含义为时间段中的成交的金额 】，因此可能不准确甚至出现负数

---
