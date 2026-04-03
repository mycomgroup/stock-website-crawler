# 互联互通API

## 简要描述

获取互联互通数据。

## 请求URL

```
https://open.lixinger.com/api/cn/index/hot/mm_ha
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：["000016"]。<br>请参考指数信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "000016"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| cpc | Number | 涨跌幅 |
| mm_sha | Number | 陆股通持仓金额 |
| mm_sha_mc_r | Number | 陆股通持仓金额占市值比例 |
| mm_sh_nba_q1 | Number | 陆股通过去1个季度净买入金额 |
| mm_sh_nba_q2 | Number | 陆股通过去2个季度净买入金额 |
| mm_sh_nba_q3 | Number | 陆股通过去3个季度净买入金额 |
| mm_sh_nba_q4 | Number | 陆股通过去4个季度净买入金额 |
| mm_sha_mc_rc_q1 | Number | 陆股通过去1个季度持股金额占市值变化比例 |
| mm_sha_mc_rc_q2 | Number | 陆股通过去2个季度持股金额占市值变化比例 |
| mm_sha_mc_rc_q3 | Number | 陆股通过去3个季度持股金额占市值变化比例 |
| mm_sha_mc_rc_q4 | Number | 陆股通过去4个季度持股金额占市值变化比例 |
