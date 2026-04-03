# 回购API

## 简要描述

获取回购数据。 说明: 计算股本为总H股

## 请求URL

```
https://open.lixinger.com/api/hk/company/repurchase
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

## API试用示例

```json
{
  "startDate": "2025-02-23",
  "endDate": "2026-02-23",
  "stockCode": "00700"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| methodOfRepurchase | String | 回购方式 |
| highestPrice | Number | 最高价 |
| lowestPrice | Number | 最低价 |
| avgPrice | Number | 成交均价 |
| num | Number | 回购股数 |
| totalPaid | Number | 总金额 |
| numPurchasedInYearSinceResolution | Number | 本年内至今（自决议案通过以来）在交易所购回的股数 |
| ratioPurchasedSinceResolution | Number | 自决议通过以来回购股数占通过决议时股本百分比 |
