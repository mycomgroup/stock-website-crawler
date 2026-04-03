# 人口API

## 简要描述

获取人口数据，如总人口等。

## 请求URL

```
https://open.lixinger.com/api/macro/population
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['y.tp.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>总人口 :tp<br>y(年):<br>t(累积)<br>男性总人口 :tmp<br>y(年):<br>t(累积)<br>女性总人口 :tfp<br>y(年):<br>t(累积)<br>人口增长率 :pb_r<br>y(年):<br>t(累积)<br>人口死亡率 :pm_r<br>y(年):<br>t(累积)<br>人口自然增长率 :png_r<br>y(年):<br>t(累积)<br>0至14岁总人口 :tp_a_0_14<br>y(年):<br>t(累积)<br>15至64岁总人口 :tp_a_15_64<br>y(年):<br>t(累积)<br>65岁以上总人口 :tp_a_65<br>y(年):<br>t(累积)<br>少儿抚养比 :cr_r<br>y(年):<br>t(累积)<br>老年抚养比 :or_r<br>y(年):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "y.tp.t"
  ]
}
```
