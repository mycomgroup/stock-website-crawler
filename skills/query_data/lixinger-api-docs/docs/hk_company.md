# 股票信息API

## 简要描述

获取股票详细信息。

## 请求URL

```
https://open.lixinger.com/api/hk/company
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 股票代码数组。默认值为所有股票代码。格式如下：["00700"]。<br>请参考股票信息API获取合法的stockCode。 |
| fsTableType | No | String | 财报类型，比如，'bank'。<br>当前支持:<br>非金融: non_financial<br>银行: bank<br>证券: security<br>保险: insurance<br>房地产投资信托: reit<br>其他金融: other_financial |
| mutualMarkets | No | Array | 互联互通类型，比如：'[ah]'。<br>当前支持:<br>港股通: ah |
| includeDelisted | No | Boolean | 是否包含退市股。 默认值是false。 |
| pageIndex | Yes | Number | 页面索引。 默认值是0。 |

## API试用示例

### 获取所有股票信息

```json
{
  "pageIndex": 0
}
```

### 获取指定财报类型的所有股票信息

```json
{
  "fsTableType": "non_financial",
  "pageIndex": 0
}
```

### 获取指定股票信息

```json
{
  "stockCodes": [
    "00700"
  ]
}
```

### 获取港股通股票数据。

```json
{
  "mutualMarkets": [
    "ah"
  ],
  "pageIndex": 0
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| total | Number | 公司总数 |
| name | String | 公司名称 |
| stockCode | String | 股票代码 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| exchange | String | 交易所 |
| fsTableType | String | 财报类型 |
| mutualMarkets | String | 互联互通 |
| mutualMarketFlag | Boolean | 是否是互联互通标的 |
| ipoDate | Date | 上市时间 |
| delistedDate | Date | 退市时间 |
| sharesPerLot | Number | 每手股数 |
| stockCodeA | String | AH同时上市公司对应的A股代码 |
