# 样本信息API

## 简要描述

获取样本信息。

## 请求URL

```
https://open.lixinger.com/api/cn/index/constituents
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：["000016"]。<br>请参考指数信息API获取合法的stockCode。 |
| date | Yes | String: latest | YYYY-MM-DD(北京时间) | 信息日期。 |

## API试用示例

```json
{
  "date": "latest",
  "stockCodes": [
    "000016"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 指数代码 |
| constituents.$.stockCode | String | 样本股票代码 |
| constituents.$.areaCode | String | 地区代码 |
| constituents.$.market | String | 市场 |
