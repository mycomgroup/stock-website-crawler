# 铂金API

## 简要描述

获取铂金数据，如伦敦铂金价格等。

## 请求URL

```
https://open.lixinger.com/api/macro/platinum-price
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
| metricsList | Yes | Array | 指标数组。如['pl_usd']。<br>伦敦铂金价格 :pl_usd |

## API试用示例

```json
{
  "areaCode": "us",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "pl_usd"
  ]
}
```
