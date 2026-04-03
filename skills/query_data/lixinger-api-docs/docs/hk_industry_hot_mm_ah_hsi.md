# 互联互通API

## 简要描述

获取互联互通数据。

## 请求URL

```
https://open.lixinger.com/api/hk/industry/hot/mm_ah/hsi
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 行业代码数组。stockCodes长度>=1且<=100，格式如下：["H50","H5010"]。<br>请参考行业信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "H50",
    "H5010"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| mm_sha | Number | 港股通持仓金额 |
| mm_sha_mc_r | Number | 港股通持仓金额占市值比例 |
| mm_sh_nba_d1 | Number | 港股通过去1个交易日净买入金额 |
| mm_sh_nba_d5 | Number | 港股通过去5个交易日净买入金额 |
| mm_sh_nba_d20 | Number | 港股通过去20个交易日净买入金额 |
| mm_sh_nba_d60 | Number | 港股通过去60个交易日净买入金额 |
| mm_sh_nba_d120 | Number | 港股通过去120个交易日净买入金额 |
| mm_sh_nba_d240 | Number | 港股通过去240个交易日净买入金额 |
| mm_sh_nba_ys | Number | 港股通今年以来净买入金额 |
| mm_sha_mc_rc_d1 | Number | 港股通过去1个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d5 | Number | 港股通过去5个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d20 | Number | 港股通过去20个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d60 | Number | 港股通过去60个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d120 | Number | 港股通过去120个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_d240 | Number | 港股通过去240个交易日持股金额占市值变化比例 |
| mm_sha_mc_rc_ys | Number | 港股通今年以來持股金额占市值变化比例 |
