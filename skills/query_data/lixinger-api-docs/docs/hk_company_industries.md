# 股票所属行业信息API

## 简要描述

获取股票所属行业信息。

## 请求URL

```
https://open.lixinger.com/api/hk/company/industries
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 股票代码请参考股票信息API获取合法的stockCode。 |
| date | No | String: YYYY-MM-DD(北京时间) | 信息时间。默认值是当前最新时间。 |

## API试用示例

### 获取最新时间股票所属行业信息

```json
{
  "stockCode": "00700"
}
```

### 获取指定日期股票所属行业信息

```json
{
  "date": "2026-02-23",
  "stockCode": "00700"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| name | String | 行业名称 |
| areaCode | String | 地区代码 |
| stockCode | String | 行业代码 |
| source | String | 行业来源 申万 :sw 申万2021版 :sw_2021 国证 :cni |
