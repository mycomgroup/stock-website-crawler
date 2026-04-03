# 基本面数据API

## 简要描述

获取基本面数据，如PE、PB等。

## 请求URL

```
https://open.lixinger.com/api/hk/company/fundamental/non_financial
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。stockCodes长度>=1且<=100，格式如下：["00700"]。<br>请参考股票信息API获取合法的stockCode。<br>需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: YYYY-MM-DD(北京时间) | 指定日期。<br>需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年<br>需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。<br>需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组。格式如下：['mc', 'pe_ttm', 'pb', 'dyr']。<br>需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取36 个指标。<br>当前支持:<br>估值指标:<br>PE-TTM :pe_ttm<br>PB :pb<br>PS-TTM :ps_ttm<br>股息率 :dyr<br>PCF-TTM :pcf_ttm<br>股价 :sp<br>涨跌幅 :spc<br>股价振幅 :spa<br>成交量 :tv<br>成交金额 :ta<br>换手率 :to_r<br>市值 :mc<br>H股市值 :mc_om<br>港股通持仓股数 :ah_sh<br>港股通持仓金额 :ah_shm<br>港股通净买入金额 :mm_nba<br>每手股数 :sharesPerLot<br>估值统计指标:<br>指标格式为[metricsName].[granularity].[statisticsDataType]。<br>metricsName<br>PE-TTM :pe_ttm<br>PB :pb<br>PS-TTM :ps_ttm<br>股息率 :dyr<br>granularity<br>上市以来 :fs<br>20年 :y20<br>10年 :y10<br>5年 :y5<br>3年 :y3<br>1年 :y1<br>statisticsDataType<br>分位点% :cvpos<br>20%分位点值 :q2v<br>50%分位点值 :q5v<br>80%分位点值 :q8v<br>最小值 :minv<br>最大值 :maxv<br>最大正值 :maxpv<br>平均值 :avgv |

## API试用示例

```json
{
  "date": "2026-02-17",
  "stockCodes": [
    "00700"
  ],
  "metricsList": [
    "pe_ttm",
    "mc",
    "pe_ttm.y3.cvpos"
  ]
}
```
