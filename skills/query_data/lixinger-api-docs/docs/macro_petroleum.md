# 石油API

## 简要描述

获取石油数据，如世界石油和其他液体库存等。

## 请求URL

```
https://open.lixinger.com/api/macro/petroleum
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
| areaCode | Yes | String | 区域编码，如{areaCode}。<br>当前支持:<br>美国: us |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['y.w_petaol_sto.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>美国支持:<br>世界石油和其他液体库存 :w_petaol_sto<br>y(年):<br>t(累积)<br>世界石油和其他液体产量 :w_petaol_pro<br>y(年):<br>t(累积)<br>m(月):<br>c(当期)<br>世界石油和其他液体消耗 :w_petaol_con<br>y(年):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "us",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "y.w_petaol_sto.t"
  ]
}
```
