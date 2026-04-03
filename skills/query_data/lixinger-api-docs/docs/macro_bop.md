# 国际收支平衡API

## 简要描述

获取国际收支平衡数据，如资本账户差额等。

## 请求URL

```
https://open.lixinger.com/api/macro/bop
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.bop_ca.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>经常账户差额 :bop_cura<br>q(季度):<br>c(当期)<br>t(累积)<br>货物于服务差额 :bop_gas<br>q(季度):<br>c(当期)<br>t(累积)<br>货物差额 :bop_g<br>q(季度):<br>c(当期)<br>t(累积)<br>服务差额 :bop_s<br>q(季度):<br>c(当期)<br>t(累积)<br>初次收入差额 :bop_firi<br>q(季度):<br>c(当期)<br>t(累积)<br>二次收入差额 :bop_seci<br>q(季度):<br>c(当期)<br>t(累积)<br>资本与金融账户差额 :bop_cafa<br>q(季度):<br>c(当期)<br>t(累积)<br>资本账户差额 :bop_ca<br>q(季度):<br>c(当期)<br>t(累积)<br>金融账户差额 :bop_fa<br>q(季度):<br>c(当期)<br>t(累积)<br>非储备性质金融账户差额 :bop_nsfa<br>q(季度):<br>c(当期)<br>t(累积)<br>直接投资差额 :bop_di<br>q(季度):<br>c(当期)<br>t(累积)<br>证券投资差额 :bop_si<br>q(季度):<br>c(当期)<br>t(累积)<br>金融衍生工具差额 :bop_nsfa_fd<br>q(季度):<br>c(当期)<br>t(累积)<br>其他投资差额 :bop_nsfa_oi<br>q(季度):<br>c(当期)<br>t(累积)<br>储备资产差额 :bop_ra<br>q(季度):<br>c(当期)<br>t(累积)<br>净误差与遗漏差额 :bop_eao<br>q(季度):<br>c(当期)<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.bop_ca.t"
  ]
}
```
