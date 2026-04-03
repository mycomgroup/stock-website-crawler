# 问询函API

## 简要描述

获取问询函信息。

## 请求URL

```
https://open.lixinger.com/api/cn/company/inquiry
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考股票信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

## API试用示例

```json
{
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "stockCode": "600866"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 公告日期 |
| type | String | 种类 问询函 :il 定期报告审核意见函 :olo_prpa 重大资产重组预案审核意见函 :olo_romarp |
| displayTypeText | String | 显示类型文本 |
| linkText | String | 链接文本 |
| linkUrl | String | 链接地址 |
| linkType | String | 链接类型 |
