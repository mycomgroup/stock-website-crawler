# K线数据API

## 简要描述

获取K线数据。 说明: 中证指数全收益率2016年以前没有数据。

## 请求URL

```
https://open.lixinger.com/api/us/index/candlestick
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考指数信息API获取合法的stockCode。stockCode仅在请求数据为date range的情况下生效。 |
| type | Yes | String | 收盘点位类型，例如，“normal”。<br>当前支持:<br>正常点位: normal<br>全收益率点位: total_return |
| date | No | String: YYYY-MM-DD(北京时间) | 信息日期。用于获取指定日期数据。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

## API试用示例

```json
{
  "type": "normal",
  "startDate": "2025-02-23",
  "endDate": "2026-02-23",
  "stockCode": ".INX"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 数据时间 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| volume | Number | 成交量 |
| amount | Number | 金额 |
| change | Number | 涨跌幅 |
