# 最新收盘价溢价率信息API

## 简要描述

获取最新收盘价溢价率信息数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund/hot/f_nlacan
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
| stockCode | String | 股票代码 |
| f_c_d | Date | 价格时间 |
| f_c_c | Number | 收盘价格 |
| f_c_cr | Number | 收盘价涨跌幅 |
| f_c_a | Number | 成交金额 |
| f_nv_eicpd | Date | 净值估算日期 |
| f_nv_esnv | Number | 净值估算前值 |
| f_nv_esvd | Date | 净值估算前值时间 |
| f_nv_eicpcr | Number | 净值估算对应的指数涨跌幅 |
| f_nv_env | Number | 净值估算值 |
| f_nv_d | Date | 净值日期 |
| f_nv | Number | 基金净值 |
| f_nv_cr | Number | 净值涨跌幅 |
| f_pnv_pr | Number | 收盘价溢价率 |
| f_pnv_pr_avg_d5 | Number | 最近5个交易日平均溢价率 |
| f_pnv_pr_avg_d10 | Number | 最近10个交易日平均溢价率 |
| f_pnv_pr_avg_d20 | Number | 最近20个交易日平均溢价率 |
