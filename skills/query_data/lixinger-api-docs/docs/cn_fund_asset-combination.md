# 资产组合API

## 简要描述

获取资产组合信息 说明: 主基金代码和子基金代码获取相同的数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund/asset-combination
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考基金信息API获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

## API试用示例

```json
{
  "startDate": "2025-02-23",
  "endDate": "2026-02-23",
  "stockCode": "161725"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 财报日期 |
| ac | Object | 资产组合 子字段: 权益类投资: ei: (Number) (其中)股票: ei_c: (Number) (其中)优先股: ei_ps: (Number) (其中)存托凭证: ei_dr: (Number) (其中)房地产信托: ei_ret: (Number) 权益类投资占比: ei_r: (Number) 基金投资: fi: (Number) 基金投资占比: fi_r: (Number) 固定收益投资: fii: (Number) (其中)债券: fii_b: (Number) (其中)资产支持证券: fii_abs: (Number) 固定收益投资占比: fii_r: (Number) 贵金属投资: pmi: (Number) 贵金属投资占比: pmi_r: (Number) 金融衍生品投资: fdi: (Number) (其中)远期: fdi_fd: (Number) (其中)期货: fdi_fs: (Number) (其中)期权: fdi_o: (Number) (其中)权证: fdi_W: (Number) 金融衍生品投资占比: fdi_r: (Number) 返售型金融资产: rfa: (Number) (其中)买断式: rfa_br: (Number) 返售型金融资产占比: rfa_r: (Number) 银行存款及结算备付金: bs_a_sr: (Number) 银行存款及结算备付金占比: bs_a_sr_r: (Number) 货币市场工具: mmt: (Number) 货币市场工具占比: mmt_r: (Number) 其他资产: oa: (Number) 其他资产占比: oa_r: (Number) |
