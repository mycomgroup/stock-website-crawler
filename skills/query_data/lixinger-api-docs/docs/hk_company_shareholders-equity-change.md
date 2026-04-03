# 股东权益变动API

## 简要描述

获取股东权益变动数据。

## 请求URL

```
https://open.lixinger.com/api/hk/company/shareholders-equity-change
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | No | String | 请参考股票信息API获取合法的stockCode。stockCode仅在请求数据为date range的情况下生效。 |
| date | No | String: YYYY-MM-DD(北京时间) | 信息日期。用于获取指定日期数据。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

## API试用示例

```json
{
  "date": "2026-02-17"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 日期 |
| name | String | 姓名 |
| numOfSharesInvolvedList | Array | 持有权益的股份数量 子字段: 数额: value: (Number) 股份类型: sharesType: (String) |
| numOfSharesInterestedList | Array | 持有权益的股份数目 子字段: 数额: value: (Number) 股份类型: sharesType: (String) |
| percentageOfIssuedVotingShares | Array | 占已发行的有投票权股份百分比 子字段: 数额: value: (Number) 股份类型: sharesType: (String) |
