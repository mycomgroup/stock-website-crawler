# 价格指数API

## 简要描述

获取价格指数数据，如居民消费价格指数(CPI)等。

## 请求URL

```
https://open.lixinger.com/api/macro/price-index
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。开始和结束的时间间隔不超过10年 |
| endDate | Yes | String: YYYY-MM-DD(北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。<br>当前支持:<br>大陆: cn<br>美国: us |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.cpi.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>居民消费价格指数(CPI) :cpi<br>m(月):<br>t(累积)<br>核心居民消费价格指数(CCPI) :ccpi<br>m(月):<br>t(累积)<br>城市居民消费价格指数 :ucpi<br>m(月):<br>t(累积)<br>农村居民消费价格指数 :rcpi<br>m(月):<br>t(累积)<br>居民消费水平 :hci<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>农村居民消费水平 :rrci<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>城镇居民消费水平 :urci<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>工业品出厂价格指数(PPI) :ppi<br>m(月):<br>t(累积)<br>工业生产者购进价格指数(PPPI) :pppi<br>m(月):<br>t(累积)<br>制造业采购经理指数 :mi_pmi<br>m(月):<br>t(累积)<br>非制造业采购经理指数 :n_mi_pmi<br>m(月):<br>t(累积)<br>综合采购经理指数 :c_pmi<br>m(月):<br>t(累积)<br>美国支持:<br>美国-所有城市消费者的消费物价指数：美国城市平均所有项目（季调） :cpiaucsl<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>t_c2c(累积环比)<br>生产者价格指数按商品分类：最终需求 :ppifis<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>制造业采购经理指数 :mi_pmi<br>m(月):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.cpi.t"
  ]
}
```
