# 社会融资API

## 简要描述

获取社会融资数据，如社会融资等。

## 请求URL

```
https://open.lixinger.com/api/macro/social-financing
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
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['m.sf.t']<br>指标参数示例:<br>指标名 :metricsName<br>granularity(时间粒度):<br>expressionCalculateType(数据统计方式):<br>大陆支持:<br>社会融资 :sf<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>人民币贷款 :sf_rmbl<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>外币贷款 :sf_fl<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>委托贷款 :sf_el<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>信托贷款 :sf_tl<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>未贴现银行承兑汇票 :sf_ubc<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>企业债券 :sf_nf_cb<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>政府债券 :sf_gb<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>非金融企业境内股票 :sf_nfef_dsm<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>存款类金融机构资产支持证券 :sf_abs_dfi<br>m(月):<br>t(累积)<br>t_y2y(累积同比)<br>贷款核销 :sf_lwo<br>m(月):<br>t(累积)<br>t_y2y(累积同比) |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "m.sf.t"
  ]
}
```
