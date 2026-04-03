# 最新股东API

## 简要描述

获取最新股东数据。

## 请求URL

```
https://open.lixinger.com/api/hk/company/latest-shareholders
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 股票代码请参考股票信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCode": "00700"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 最后申报有关通知之日期 |
| name | String | 姓名 |
| numOfSharesInterestedList | Array | 持有权益的股份数目 子字段: 数额: value: (Number) 股份类型: sharesType: (String) |
| percentageOfIssuedVotingShares | Array | 占已发行的有投票权股份百分比 子字段: 数额: value: (Number) 股份类型: sharesType: (String) |
