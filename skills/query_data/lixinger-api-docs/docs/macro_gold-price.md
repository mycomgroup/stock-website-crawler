# 黄金API

## 简要描述

获取黄金数据，如上海金价格等。

## 请求URL

```
https://open.lixinger.com/api/macro/gold-price
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
| metricsList | Yes | Array | 指标数组。如['sge_pm_cny']。<br>大陆支持:<br>上海金价格 :sge_pm_cny<br>美国支持:<br>伦敦金价格 :lbma_pm_usd |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "sge_pm_cny"
  ]
}
```
