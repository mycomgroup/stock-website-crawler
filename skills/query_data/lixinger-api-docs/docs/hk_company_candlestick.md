# K线数据API

## 简要描述

获取K线数据。 说明: 复权计算仅对所选时间段的价格进行复权 成交量不进行复权计算

## 请求URL

```
https://open.lixinger.com/api/hk/company/candlestick
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。stockCode仅在请求数据为date range的情况下生效。 |
| type | No | String | 除复权类型， 例如， “lxr_fc_rights”。<br>当前支持:<br>不复权: ex_rights<br>理杏仁前复权: lxr_fc_rights<br>前复权: fc_rights<br>后复权: bc_rights |
| date | No | String: YYYY-MM-DD(北京时间) | 信息日期。用于获取指定日期数据。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| adjustForwardDate | No | String: YYYY-MM-DD(北京时间) | 前复权指定起始时间点。<br>需要注意的是，请与endDate一起使用且大于或等于endDate。 获取复权类型数据时要传入，不传时默认值是endDate。 |
| adjustBackwardDate | No | String: YYYY-MM-DD(北京时间) | 后复权指定起始时间点。<br>需要注意的是，请与startDate一起使用且小于或等于startDate。 获取复权类型数据时要传入，不传时默认值是startDate。 |
| limit | No | Number | 返回最近数据的数量。 |

## API试用示例

```json
{
  "type": "lxr_fc_rights",
  "startDate": "2025-02-23",
  "endDate": "2026-02-23",
  "stockCode": "00700"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 数据时间 |
| stockCode | String | 股票代码 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| volume | Number | 成交量 |
| amount | Number | 金额 |
| change | Number | 涨跌幅 |
| to_r | Number | 换手率 |
