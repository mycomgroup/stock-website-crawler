# 股权质押API

## 简要描述

获取股权质押数据。

## 请求URL

```
https://open.lixinger.com/api/cn/company/pledge
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
  "stockCode": "300750"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 数据时间 |
| pledgor | String | 出质人 |
| pledgee | String | 质权人 |
| pledgeMatters | String | 质押事项 |
| pledgeSharesNature | String | 质押股份性质 |
| pledgeAmount | Number | 质押数量 |
| pledgePercentageOfTotalEquity | Number | 占总股比例 |
| pledgeStartDate | Date | 质押起始日 |
| pledgeEndDate | Date | 质押终止日 |
| pledgeDischargeDate | Date | 质押解除日 |
| pledgeDischargeExplanation | String | 质押解除解释 |
| pledgeDischargeAmount | Number | 质押解除数量 |
| isPledgeRepurchaseTransactions | Boolean | 是否质押式回购交易 |
| accumulatedPledgePercentageOfTotalEquity | Number | 累计质押占总股比例 |
