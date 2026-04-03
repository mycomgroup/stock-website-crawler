# 基金公司信息API

## 简要描述

获取基金公司详细信息。

## 请求URL

```
https://open.lixinger.com/api/cn/fund-company
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 基金公司代码数组。<br>请参考基金信息API获取合法的stockCode。 |

## API试用示例

### 获取所有基金公司信息

```json
{}
```

### 获取指定基金公司信息

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
| name | String | 基金公司名称 |
| stockCode | String | 基金公司代码 |
| inceptionDate | Date | 成立日期 |
| fundsNum | Number | 基金数量 |
| assetScale | Number | 总资产规模 |
| fundCollectionType | String | 基金公司类型 基金公司 :fund_company 证券公司 :securities_company 证券公司资产管理子公司 :securities_company_amsc 保险资产管理公司 :insurance_am_company |
