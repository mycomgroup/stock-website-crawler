# 基金经理信息API

## 简要描述

获取基金经理详细信息。

## 请求URL

```
https://open.lixinger.com/api/cn/fund-manager
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 基金经理代码数组。<br>请参考基金信息API获取合法的stockCode。 |

## API试用示例

### 获取所有基金经理信息

```json
{}
```

### 获取指定基金经理信息

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
| name | String | 基金经理姓名 |
| birthYear | Number | 出生年份 |
| resume | String | 履历 |
| stockCode | String | 基金经理代码 |
| gender | String | 性别 |
