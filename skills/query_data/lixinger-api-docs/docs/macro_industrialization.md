# 工业API

## 简要描述

获取工业数据，如工业企业利润总额等。

## 请求URL

```
https://open.lixinger.com/api/macro/industrialization
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.adsietp.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>工业企业利润总额 :adsietp<br>m(月):<br>t(累积)<br>工业企业营业收入 :ieop<br>m(月):<br>t(累积)<br>工业企业存货 :iei<br>m(月):<br>t(累积)<br>工业企业单位数 :ien<br>m(月):<br>t(累积)<br>工业企业平均用工人数 :ieaw<br>m(月):<br>t(累积)<br>工业企业产成品 :iep<br>y(年):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.adsietp.t"
  ]
}
```
