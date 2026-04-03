# Gdp API

## 简要描述

获取GDP数据，如GDP等。

## 请求URL

```
https://open.lixinger.com/api/macro/gdp
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['q.gdp.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>GDP :gdp<br>q(季度):<br>t(累积)<br>t_y2y(累积同比)<br>c(当期)<br>c_c2c(当期环比)<br>不变价GDP :gdp_cp<br>q(季度):<br>t(累积)<br>c(当期)<br>人均GDP :per_gdp<br>q(季度):<br>t(累积)<br>t_y2y(累积同比)<br>第一产业GDP :pi_gdp<br>q(季度):<br>t(累积)<br>t_y2y(累积同比)<br>c(当期)<br>c_c2c(当期环比)<br>第二产业GDP :si_gdp<br>q(季度):<br>t(累积)<br>t_y2y(累积同比)<br>c(当期)<br>c_c2c(当期环比)<br>第三产业GDP :ti_gdp<br>q(季度):<br>t(累积)<br>t_y2y(累积同比)<br>c(当期)<br>c_c2c(当期环比)<br>第一产业对GDP贡献率 :pi_gdp_c_r<br>q(季度):<br>t(累积)<br>c(当期)<br>第二产业对GDP贡献率 :si_gdp_c_r<br>q(季度):<br>t(累积)<br>c(当期)<br>第三产业对GDP贡献率 :ti_gdp_c_r<br>q(季度):<br>t(累积)<br>q(季度):<br>t(累积)<br>c(当期)<br>GNI :gni<br>q(季度):<br>t(累积)<br>t_y2y(累积同比)<br>美国支持:<br>GDP :gdp<br>q(季度):<br>t(累积)<br>t_c2c(累积环比)<br>t_y2y(累积同比) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "q.gdp.t"
  ]
}
```
