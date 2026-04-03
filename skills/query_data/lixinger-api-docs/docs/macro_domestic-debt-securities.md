# 国内各类债券API

## 简要描述

获取国内各类债券数据，如政府债券发行金额等。

## 请求URL

```
https://open.lixinger.com/api/macro/domestic-debt-securities
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.gs_i.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>政府债券发行金额 :gs_i<br>m(月):<br>c(当期)<br>金融债券发行金额 :fb_i<br>m(月):<br>c(当期)<br>公司信用类债券发行金额 :cdb_i<br>m(月):<br>c(当期)<br>国际机构债券发行金额 :iib_i<br>m(月):<br>c(当期)<br>政府债券累积余额 :gs_o<br>m(月):<br>t(累积)<br>金融债券累积余额 :fb_o<br>m(月):<br>t(累积)<br>公司信用类债券累积余额 :cdb_o<br>m(月):<br>t(累积)<br>国际机构债券累积余额 :iib_o<br>m(月):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.gs_i.t"
  ]
}
```
