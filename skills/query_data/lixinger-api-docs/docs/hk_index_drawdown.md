# 指数回撤API

## 简要描述

获取指数回撤数据。

## 请求URL

```
https://open.lixinger.com/api/hk/index/drawdown
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考指数信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| granularity | Yes | String | 回撤周期，例如：“y”。<br>当前支持:<br>月: m<br>季度: q<br>半年: hy<br>1年: y1<br>3年: y3<br>5年: y5<br>10年: y10<br>上市以来: fs |

## API试用示例

```json
{
  "startDate": "2023-02-23",
  "endDate": "2026-02-23",
  "granularity": "y",
  "stockCode": "HSI"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 数据时间 |
| value | Number | 回撤 |
