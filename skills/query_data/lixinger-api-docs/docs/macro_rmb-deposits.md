# 人民币存款

## 简要描述

获取人民币贷款数据，如人民币存款等。

## 请求URL

```
https://open.lixinger.com/api/macro/rmb-deposits
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
| metricsList | Yes | Array | 指标数组。如['rmb_d']。<br>人民币存款 :rmb_d<br>m(月):<br>t(累积)<br>境内存款 :rmb_d_d<br>m(月):<br>t(累积)<br>境外存款 :rmb_o_d<br>m(月):<br>t(累积)<br>住户存款 :rmb_h_d<br>m(月):<br>t(累积)<br>非金融企业存款 :rmb_nfe_d<br>m(月):<br>t(累积)<br>机关团体存款 :rmb_gdo_d<br>m(月):<br>t(累积)<br>财政性存款 :rmb_f_d<br>m(月):<br>t(累积)<br>非银行业金融机构存款 :rmb_nbfi_d<br>m(月):<br>t(累积)<br>住户活期存款 :rmb_h_d_d<br>m(月):<br>t(累积)<br>住户定期及其他存款 :rmb_h_to_d<br>m(月):<br>t(累积)<br>非金融企业活期存款 :rmb_nfe_d_d<br>m(月):<br>t(累积)<br>非金融企业定期及其他存款 :rmb_nfe_to_d<br>m(月):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.rmb_d.t"
  ]
}
```
