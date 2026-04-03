# 信用证券账户API

## 简要描述

获取信用证券账户数据，如新增信用证券账户等。

## 请求URL

```
https://open.lixinger.com/api/macro/credit-securities-account
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
| metricsList | Yes | Array | 指标数组。如['ncsa']。<br>新增信用证券账户 :ncsa<br>新增个人信用证券账户 :nisca<br>新增机构信用证券账户 :nosca<br>新销信用证券账户 :dcsa<br>新销个人信用证券账户 :disca<br>新销机构信用证券账户 :dosca<br>信用证券账户 :csa<br>个人信用证券账户 :isca<br>机构信用证券账户 :osca |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "ncsa"
  ]
}
```
