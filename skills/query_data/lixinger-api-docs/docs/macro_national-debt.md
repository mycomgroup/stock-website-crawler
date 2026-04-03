# 国债API

## 简要描述

获取国债数据，如十年期收益率等。

## 请求URL

```
https://open.lixinger.com/api/macro/national-debt
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
| areaCode | Yes | String | 区域编码，如{areaCode}。<br>当前支持:<br>大陆: cn<br>美国: us |
| metricsList | Yes | Array | 指标数组。如['tcm_y10']。<br>大陆支持:<br>三月期收益率 :tcm_m3<br>六月期收益率 :tcm_m6<br>一年期收益率 :tcm_y1<br>二年期收益率 :tcm_y2<br>三年期收益率 :tcm_y3<br>五年期收益率 :tcm_y5<br>七年期收益率 :tcm_y7<br>十年期收益率 :tcm_y10<br>二十年期收益率 :tcm_y20<br>三十年期收益率 :tcm_y30<br>美国支持:<br>三月期收益率 :tcm_m3<br>六月期收益率 :tcm_m6<br>一年期收益率 :tcm_y1<br>二年期收益率 :tcm_y2<br>三年期收益率 :tcm_y3<br>五年期收益率 :tcm_y5<br>七年期收益率 :tcm_y7<br>十年期收益率 :tcm_y10<br>二十年期收益率 :tcm_y20<br>三十年期收益率 :tcm_y30 |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "tcm_y10"
  ]
}
```
