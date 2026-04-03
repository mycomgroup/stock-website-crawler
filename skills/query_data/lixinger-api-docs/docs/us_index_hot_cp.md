# 收盘点位API

## 简要描述

获取收盘点位数据。

## 请求URL

```
https://open.lixinger.com/api/us/index/hot/cp
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：[".INX"]。<br>请参考指数信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    ".INX"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| cpc | Number | 涨跌幅 |
| cpc_fys | Number | 今年以来涨跌幅 |
| cpc_w1 | Number | 近一周涨跌幅 |
| cpc_w2 | Number | 近二周涨跌幅 |
| cpc_m1 | Number | 近一月涨跌幅 |
| cpc_m3 | Number | 近三月涨跌幅 |
| cpc_m6 | Number | 近六月涨跌幅 |
| cpc_y1 | Number | 近一年涨跌幅 |
| cp_cac_y2 | Number | 近二年年化涨跌幅 |
| cp_cac_y3 | Number | 近三年年化涨跌幅 |
| cp_cac_y5 | Number | 近五年年化涨跌幅 |
| cp_cac_y10 | Number | 近十年年化涨跌幅 |
| cp_cac_fs | Number | 发布以来年化涨跌幅 |
