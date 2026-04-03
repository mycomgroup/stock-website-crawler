# 官方储备资产

## 简要描述

获取官方储备资产数据，如官方储备资产-合计等。

## 请求URL

```
https://open.lixinger.com/api/macro/official-reserve-assets
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
| metricsList | Yes | Array | 指标数组。如['ora']。<br>官方储备资产-合计 :ora<br>m(月):<br>t(累积)<br>外汇储备 :ora_fc<br>m(月):<br>t(累积)<br>黄金储量资产 :ora_g_usd<br>m(月):<br>t(累积)<br>黄金储量 :ora_g_o<br>m(月):<br>t(累积)<br>基金组织储备头寸 :ora_imf_rp<br>m(月):<br>t(累积)<br>特别提款权 :ora_sdr_s<br>m(月):<br>t(累积)<br>其他储备资产 :ora_o<br>m(月):<br>t(累积) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.ora.t"
  ]
}
```
