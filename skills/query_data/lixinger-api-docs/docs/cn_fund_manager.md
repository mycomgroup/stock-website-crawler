# 基金经理API

## 简要描述

获取该基金历史上所有的基金经理任职信息。 说明: 主基金代码和子基金代码获取相同的数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund/manager
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金代码数组。stockCodes长度>=1且<=100，格式如下：["161725","005827"]。<br>请参考基金信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "161725",
    "005827"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 基金代码 |
| managers | Array | 基金经理数组。 子字段: 基金经理姓名: name: (String) 基金经理代码: managerCode: (String) 任职日期: appointmentDate: (Date) 离任日期: departureDate: (Date) |
