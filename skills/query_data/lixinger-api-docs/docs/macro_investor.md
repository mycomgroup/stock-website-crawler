# 投资者API

## 简要描述

获取投资者数据，如自然人等。

## 请求URL

```
https://open.lixinger.com/api/macro/investor
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
| granularity | Yes | String | 数据统计维度<br>当前支持:<br>月度数据: m。 该数据只有在2015年3月后有数据。<br>周数据: w。 该数据只在2020年4月之间有数据。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。<br>当前支持:<br>大陆: cn |
| metricsList | Yes | Array | 指标数组。如['ni']。<br>新增自然人 :nni<br>新增非自然人 :n_non_ni<br>自然人 :ni<br>A股自然人 :nia<br>B股自然人 :nib<br>非自然人 :non_ni<br>A股非自然人 :non_nia<br>B股非自然人 :non_nib |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "granularity": "m",
  "metricsList": [
    "ni"
  ]
}
```
