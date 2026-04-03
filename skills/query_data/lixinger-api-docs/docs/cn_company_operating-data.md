# 经营数据API

## 简要描述

获取经营数据信息。

## 请求URL

```
https://open.lixinger.com/api/cn/company/operating-data
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
  "stockCode": "600157"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 数据时间 |
| declarationDate | Date | 公告日期 |
| startDate | Date | 开始日期 |
| dataList.$.itemName | String | 项目名称 |
| dataList.$.parentItemName | String | 父项名称 |
| dataList.$.unitText | String | 单位 |
| dataList.$.value | Number | 数额 |
