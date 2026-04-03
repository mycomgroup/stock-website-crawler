# 美元指数API

## 简要描述

获取美元指数数据

## 请求URL

```
https://open.lixinger.com/api/macro/usdx
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

## API试用示例

```json
{
  "startDate": "2026-02-16",
  "endDate": "2026-02-23"
}
```
