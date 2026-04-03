# 客户API

## 简要描述

获取客户信息。

## 请求URL

```
https://open.lixinger.com/api/cn/company/customers
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
  "startDate": "2024-02-23",
  "endDate": "2026-02-23",
  "stockCode": "300750"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 数据时间 |
| declarationDate | Date | 公告日期 |
| dataList.$.ratio | Number | 比例 |
| dataList.$.tradeAmount | Number | 成交金额 |
| dataList.$.trader | String | 交易商 |
| top5Customer.$.tradeAmount | Number | 前五大成交金额 |
| top5Customer.$.ratio | Number | 前五大占比 |
