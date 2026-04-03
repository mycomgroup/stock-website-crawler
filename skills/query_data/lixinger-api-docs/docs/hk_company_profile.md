# 公司概况API

## 简要描述

获取公司概况数据

## 请求URL

```
https://open.lixinger.com/api/hk/company/profile
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。stockCodes长度>=1且<=100，格式如下：["00700"]。<br>请参考股票信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "00700"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 股票代码 |
| listingDate | Date | 上市日期 |
| chairman | String | 董事长 |
| classAdescription | String | A股 |
| classBdescription | String | B股 |
| capitalStructureClassA | Number | A股股本结构 |
| capitalStructureClassB | Number | B股股本结构 |
| fiscalYearEnd | Date | 财政年度结算日期 |
| summary | String | 公司概况 |
| listingCategory | String | 上市类型 |
| registrar | String | 过户处 |
| website | String | 公司网址 |
| registeredAddress | String | 注册地址 |
| officeAddress | String | 办公地址 |
