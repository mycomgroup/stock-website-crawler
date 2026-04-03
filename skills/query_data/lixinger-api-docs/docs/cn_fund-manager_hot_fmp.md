# 基金经理收益率API

## 简要描述

获取基金经理收益率数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund-manager/hot/fmp
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金经理代码数组。stockCodes长度>=1且<=100，格式如下：["8801388323","8801372475"]。<br>请参考基金信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "8801388323",
    "8801372475"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 股票代码 |
| fm_p_r_d | Date | 最新收益率时间 |
| fm_p_r_fys | Number | 今年以来收益率 |
| fm_p_r_m1 | Number | 一个月收益率 |
| fm_p_r_m3 | Number | 三个月收益率 |
| fm_p_r_m6 | Number | 六个月收益率 |
| fm_p_r_y1 | Number | 一年收益率 |
| fm_p_r_y3 | Number | 三年收益率 |
| fm_p_r_y5 | Number | 五年收益率 |
| fm_p_r_y10 | Number | 十年收益率 |
| fm_cagr_p_r_fs | Number | 管理基金以来年化收益率 |
| fm_p_r_fys_rp | Number | 相同基金经理类型今年以来收益率排名 |
| fm_p_r_m1_rp | Number | 相同基金经理类型一个月收益率排名 |
| fm_p_r_m3_rp | Number | 相同基金经理类型三个月收益率排名 |
| fm_p_r_m6_rp | Number | 相同基金经理类型六个月收益率排名 |
| fm_p_r_y1_rp | Number | 相同基金经理类型一年收益率排名 |
| fm_p_r_y3_rp | Number | 相同基金经理类型三年收益率排名 |
| fm_p_r_y5_rp | Number | 相同基金经理类型五年收益率排名 |
| fm_p_r_y10_rp | Number | 相同基金经理类型十年收益率排名 |
| fm_cagr_p_r_fs_rp | Number | 相同基金经理类型管理基金以来年化收益率排名 |
