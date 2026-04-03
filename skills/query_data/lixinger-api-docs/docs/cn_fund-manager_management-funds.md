# 管理的基金信息API

## 简要描述

获取管理的基金详细信息。

## 请求URL

```
https://open.lixinger.com/api/cn/fund-manager/management-funds
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金经理代码数组。stockCodes长度>=1且<=100，格式如下：["8801388323","8801372475"]。<br>请参考基金信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "8801388323",
    "8801372475"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| funds | Array | 基金数组。 子字段: 基金名称: name: (String) 基金代码: code: (String) 任职日期: appointmentDate: (Date) 离任日期: departureDate: (Date) |
