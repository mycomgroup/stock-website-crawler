# 基金公司资产规模API

## 简要描述

获取基金公司资产规模数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund-company/hot/fc_as
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
| stockCode | String | 股票代码 |
| fc_as_d | Date | 最新数据时间 |
| fc_as | Number | 总资产规模 |
| fc_nb_as | Number | 非债券基金资产规模 |
| fc_h_as | Number | 混合型资产规模 |
| fc_e_as | Number | 股票型资产规模 |
| fc_q_as | Number | QDII型资产规模 |
| fc_b_as | Number | 债券型资产规模 |
