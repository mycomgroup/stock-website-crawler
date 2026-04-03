# 全社会固定资产投资API

## 简要描述

获取全社会固定资产投资数据，如固定资产投资(不含农户)等。

## 请求URL

```
https://open.lixinger.com/api/macro/investment-in-fixed-assets
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.fai_ef.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>固定资产投资(不含农户) :fai_ef<br>m(月):<br>t(累积)<br>固定资产投资额累计增长(不含农户) :cg_o_fai_ef<br>m(月):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.fai_ef.t"
  ]
}
```
