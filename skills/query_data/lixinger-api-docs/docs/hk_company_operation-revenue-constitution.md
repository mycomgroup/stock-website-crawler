# 营收构成API

## 简要描述

获取营收构成数据。

## 请求URL

```
https://open.lixinger.com/api/hk/company/operation-revenue-constitution
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
| date | Date | 数据时间 |
| declarationDate | Date | 公告日期 |
| currency | String | 货币 |
| dataList.$.itemName | String | 项目名称 |
| dataList.$.parentItemName | String | 父项名称 |
| dataList.$.revenue | Number | 收入 |
| dataList.$.costs | Number | 成本 |
| dataList.$.grossProfitMargin | Number | 毛利率 |
