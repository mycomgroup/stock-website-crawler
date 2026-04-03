# 按行业分类的股票投资组合API

## 简要描述

获取按行业分类的股票投资组合的数据。 说明: 主基金代码和子基金代码获取相同的数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund/asset-industry-combination
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
  "stockCode": "005827"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 财报日期 |
| aic_cn | Array | 按行业分类的股票投资组合 子字段: 行业名称: name: (String) 公允价值: value: (Number) 比例: proportion: (Number) |
