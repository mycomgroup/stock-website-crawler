# 人民币贷款

## 简要描述

获取人民币贷款数据，如人民币贷款等。

## 请求URL

```
https://open.lixinger.com/api/macro/rmb-loans
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
| metricsList | Yes | Array | 指标数组。如['rmb_l']。<br>人民币贷款 :rmb_l<br>m(月):<br>t(累积)<br>境内贷款 :rmb_d_l<br>m(月):<br>t(累积)<br>海外贷款 :rmb_o_l<br>m(月):<br>t(累积)<br>住户贷款 :rmb_h_l<br>m(月):<br>t(累积)<br>住户短期贷款 :rmb_h_s_l<br>m(月):<br>t(累积)<br>住户中长期贷款 :rmb_h_ml_l<br>m(月):<br>t(累积)<br>企（事）业单位贷款 :rmb_nfeg_l<br>m(月):<br>t(累积)<br>企（事）业单位短期贷款 :rmb_nfeg_s_l<br>m(月):<br>t(累积)<br>企（事）业单位中长期贷款 :rmb_nfeg_ml_l<br>m(月):<br>t(累积)<br>企（事）业单位票据融资 :rmb_nfeg_p_f<br>m(月):<br>t(累积)<br>企（事）业单位融资租赁 :rmb_nfeg_f_l<br>m(月):<br>t(累积)<br>企（事）业单位各项垫款 :rmb_nfeg_ta_l<br>m(月):<br>t(累积)<br>非银行业金融机构贷款 :rmb_nbfo_l<br>m(月):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.rmb_l.t"
  ]
}
```
