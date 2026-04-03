# 杠杆率API

## 简要描述

获取杠杆率数据

## 请求URL

```
https://open.lixinger.com/api/macro/leverage-ratio
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
| metricsList | Yes | Array | 指标数组。如['lr_h']。<br>居民杠杆率 :lr_h<br>非金融企业部门杠杆率 :lr_nfc<br>政府杠杆率 :lr_gg<br>实体经济部门杠杆率 :lr_nfs<br>中央政府杠杆率 :lr_cg<br>地方政府杠杆率 :lr_lg<br>金融部门资产方杠杆率 :lr_fsas<br>金融部门负债方杠杆率 :lr_fsls |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "lr_h"
  ]
}
```
