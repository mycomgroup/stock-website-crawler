# 央行资产负债表API

## 简要描述

获取央行资产负债表数据，如总资产等。

## 请求URL

```
https://open.lixinger.com/api/macro/central-bank-balance-sheet
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。开始和结束的时间间隔不超过10年 |
| endDate | Yes | String: YYYY-MM-DD(北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。<br>当前支持:<br>大陆: cn |
| metricsList | Yes | Array | 指标数组。如['t_a']。<br>总资产 :t_a<br>m(月):<br>t(累积)<br>国外资产 :f_a<br>m(月):<br>t(累积)<br>对政府债权 :c_o_g<br>m(月):<br>t(累积)<br>对其他存款性公司债权 :c_o_odc<br>m(月):<br>t(累积)<br>对其他金融性公司债权 :c_o_ofc<br>m(月):<br>t(累积)<br>对非金融性公司债权 :c_o_onfc<br>m(月):<br>t(累积)<br>其他资产 :o_a<br>m(月):<br>t(累积)<br>储备货币 :r_m<br>m(月):<br>t(累积)<br>不计入储备货币的金融性公司存款 :d_o_fc_ef_rm<br>m(月):<br>t(累积)<br>发行债券 :b_i<br>m(月):<br>t(累积)<br>国外负债 :f_l<br>m(月):<br>t(累积)<br>政府存款 :d_o_g<br>m(月):<br>t(累积)<br>自有资金 :o_c<br>m(月):<br>t(累积)<br>其他负债 :o_lia<br>m(月):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.t_a.t"
  ]
}
```
