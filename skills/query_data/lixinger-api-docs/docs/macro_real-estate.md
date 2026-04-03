# 房地产API

## 简要描述

获取房地产数据，如房地产投资额等。

## 请求URL

```
https://open.lixinger.com/api/macro/real-estate
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.rei.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>房地产投资额 :rei<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>房地产施工面积 :re_ca<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>房地产新开工施工面积 :nsca_i_re<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>房地产竣工面积 :ca_o_re<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>购置土地面积 :l_pa<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>土地成交价款 :l_tr<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>商品房销售面积 :sa_o_ch<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>商品房销售额 :st_o_ch<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>商品住宅房销售面积 :sa_o_crb<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>商品住宅房销售额 :st_o_crb<br>m(月):<br>t(累积)<br>t_y2y(累积同比) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.rei.t"
  ]
}
```
