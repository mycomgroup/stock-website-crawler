# 公司概况API

## 简要描述

获取公司概况数据

## 请求URL

```
https://open.lixinger.com/api/cn/company/profile
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。stockCodes长度>=1且<=100，格式如下：["300750","600519","600157"]。<br>请参考股票信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "300750",
    "600519",
    "600157"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 股票代码 |
| companyName | String | 公司名称 |
| historyStockNames | Array | 历史名称 新名称 :newName 老名称 :oldName |
| province | String | 省份 |
| city | String | 城市 |
| actualControllerTypes | Array | 实际控制人类型 自然人 :natural_person 集体 :collective 外企 :foreign_company 国有 :state_owned |
| actualControllerName | String | 实际控制人 |
