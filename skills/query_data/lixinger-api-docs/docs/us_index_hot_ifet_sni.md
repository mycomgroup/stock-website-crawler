# 场内基金认购净流入API

## 简要描述

获取场内基金认购净流入数据。

## 请求URL

```
https://open.lixinger.com/api/us/index/hot/ifet_sni
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：[".INX"]。<br>请参考指数信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    ".INX"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| cpc | Number | 涨跌幅 |
| ifet_as | Number | 场内基金资产规模 |
| ifet_sni_ytd | Number | 过去1天场内基金认购净流入 |
| ifet_sni_w1 | Number | 过去1周场内基金认购净流入 |
| ifet_sni_w2 | Number | 过去2周场内基金认购净流入 |
| ifet_ssni_m1 | Number | 过去1个月场内基金认购净流入 |
| ifet_sni_m3 | Number | 过去3个月场内基金认购净流入 |
| ifet_sni_m6 | Number | 过去6个月场内基金认购净流入 |
| ifet_sni_y1 | Number | 过去1年场内基金认购净流入 |
| ifet_sni_y2 | Number | 过去2年场内基金认购净流入 |
| ifet_sni_fys | Number | 今年以来场内基金认购净流入 |
