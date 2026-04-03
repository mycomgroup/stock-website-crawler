# 对外贸易API

## 简要描述

获取对外贸易数据，如进出口总额(人民币)等。

## 请求URL

```
https://open.lixinger.com/api/macro/foreign-trade
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
| areaCode | Yes | String | 区域编码，如{areaCode}。<br>当前支持:<br>大陆: cn |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.tiae_rmb.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>进出口总额(人民币) :tiae_rmb<br>m(月):<br>t(累积)<br>进口差额(人民币) :iaeb_rmb<br>m(月):<br>t(累积)<br>出口总额(人民币) :te_rmb<br>m(月):<br>t(累积)<br>进口总额(人民币) :ti_rmb<br>m(月):<br>t(累积)<br>进出口总额(美元) :tiae_usd<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>c(当期)<br>c_c2c(当期环比)<br>进口差额(美元) :iaeb_usd<br>m(月):<br>t(累积)<br>c(当期)<br>出口总额(美元) :te_usd<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>c(当期)<br>c_c2c(当期环比)<br>进口总额(美元) :ti_usd<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>c(当期)<br>c_c2c(当期环比) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.tiae_rmb.t"
  ]
}
```
