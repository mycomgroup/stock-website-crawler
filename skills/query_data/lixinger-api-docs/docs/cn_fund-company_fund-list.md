# 基金列表API

## 简要描述

获取基金列表详细信息。

## 请求URL

```
https://open.lixinger.com/api/cn/fund-company/fund-list
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金公司代码数组。stockCodes长度>=1且<=100，格式如下：["50110000","50030000"]。<br>请参考基金信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "50110000",
    "50030000"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| fundCodes | Array | 基金代码数组。 |
