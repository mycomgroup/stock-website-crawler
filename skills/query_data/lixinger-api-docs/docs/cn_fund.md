# 基金信息API

## 简要描述

获取基金详细信息。 说明: 场内基金的exchange是 sz 或 sh。

## 请求URL

```
https://open.lixinger.com/api/cn/fund
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 基金代码数组。默认值为所有基金的基金代码。格式如下：["161725","005827"]。<br>请参考基金信息API获取合法的stockCode。 |
| pageIndex | Yes | Number | 页面索引。 默认值是0。 |

## API试用示例

### 获取所有基金信息

```json
{
  "pageIndex": 0
}
```

### 获取指定基金信息

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
| total | Number | 基金总数 |
| name | String | 基金名称 |
| stockCode | String | 基金代码 |
| fundFirstLevel | String | 基金一级类型，目前只有商品基金有这个类型。 互认基金 :mutual_recognition |
| fundSecondLevel | String | 基金类型 股票型 :company 混合型 :hybrid 债券型 :bond QDII :QDII REIT :reit FOF :fof 商品基金 :commodity |
| shortName | String | 简称 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| exchange | String | 交易所 |
| inceptionDate | Date | 合同生效日 |
| delistedDate | Date | 退市时间 |
