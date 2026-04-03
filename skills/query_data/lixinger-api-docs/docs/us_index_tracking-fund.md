# 指数跟踪基金信息API

## 简要描述

获取指数跟踪基金数据。

## 请求URL

```
https://open.lixinger.com/api/us/index/tracking-fund
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 股票代码请参考指数信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCode": ".INX"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| name | String | 基金名称 |
| stockCode | String | 基金代码 |
| shortName | String | 简称 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| exchange | String | 交易所 |
