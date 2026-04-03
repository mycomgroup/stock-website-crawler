# 分红再投入收益率API

## 简要描述

获取分红再投入收益率数据。 说明: 理杏仁采用分红再投入策略计算投资收益率

## 请求URL

```
https://open.lixinger.com/api/cn/company/hot/tr_dri
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
| last_data_date | Date | 数据时间 |
| p_r | Number | 指定时间段投资收益率 |
| cagr_p_r_fys | Number | 今年以来投资收益率 |
| cagr_p_r_d7 | Number | 近7日投资收益率 |
| cagr_p_r_d14 | Number | 近14日投资收益率 |
| cagr_p_r_d30 | Number | 近30日投资收益率 |
| cagr_p_r_d60 | Number | 近60日投资收益率 |
| cagr_p_r_d90 | Number | 近90日投资收益率 |
| cagr_p_r_y1 | Number | 近一年投资收益率 |
| cagr_p_r_y3 | Number | 近三年年化投资收益率 |
| cagr_p_r_y5 | Number | 近五年年化投资收益率 |
| cagr_p_r_y10 | Number | 近十年年化投资收益率 |
| cagr_p_r_y20 | Number | 近二十年年化投资收益率 |
| cagr_p_r_fs | Number | 上市至今年化投资收益率 |
| p_r_fs | Number | 上市以来总投资收益率 |
| period_date | Date | 投资收益率计算起始日期 |
