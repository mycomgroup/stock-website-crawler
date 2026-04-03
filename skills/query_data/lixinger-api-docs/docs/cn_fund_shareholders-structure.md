# 持有人结构API

## 简要描述

获取基金持有人结构数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund/shareholders-structure
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考基金信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

## API试用示例

```json
{
  "startDate": "2025-02-23",
  "endDate": "2026-02-23",
  "stockCode": "161725"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 数据时间 |
| h_a | Number | 持有人户数 |
| h_s_a | Number | 持有人平均份额 |
| ins_h_s | Number | 机构持有份额 |
| ins_h_s_r | Number | 机构投资占比 |
| ind_h_s | Number | 个人持有份额 |
| ind_h_s_r | Number | 个人持有份额占比 |
| f_f_s | Number | 联接基金份额 |
| f_f_s_r | Number | 联接基金份额占比 |
