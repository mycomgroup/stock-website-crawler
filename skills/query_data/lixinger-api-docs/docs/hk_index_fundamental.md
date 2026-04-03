# 基本面数据API

## 简要描述

获取基本面数据，如PE、PB等。 说明: 指标计算请参考指数估值计算

## 请求URL

```
https://open.lixinger.com/api/hk/index/fundamental
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：["HSI"]。<br>请参考指数信息API获取合法的stockCode。<br>需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: YYYY-MM-DD(北京时间) | 指定日期。<br>需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年<br>需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。<br>需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标列表。例如：['mc', 'pe_ttm.ew', 'pe_ttm.y10.ew.cvpos’]。<br>需要注意的是，共有三种形式的指标格式：<br>[metricsName].[granularity].[metricsType].[statisticsDataType]: 支持指标有 pe_ttm, pb, ps_ttm, dyr(股息率)<br>[metricsName].[metricsType]: 支持指标有 dyr(股息率), pe_ttm, pb, ps_ttm<br>[metricsName] : 被剩余的指标支持，如 , mc(市值), tv(成交量), ta(成交金额) , cp(收盘点位) , cpc(涨跌幅)<br>当前支持:<br>metricsName<br>PE-TTM :pe_ttm<br>PB :pb<br>PS-TTM :ps_ttm<br>股息率 :dyr<br>成交量 :tv<br>成交金额 :ta<br>收盘点位 :cp<br>涨跌幅 :cpc<br>指数点位振幅 :cpa<br>市值 :mc<br>H股市值 :mc_om<br>港股通持仓金额 :ah_shm<br>港股通净买入金额 :mm_nba<br>A股场内基金资产规模 :fet_as_ma<br>A股场内基金认购净流入 :fet_snif_ma<br>发布时间 :launchDate<br>granularity<br>上市以来 :fs<br>20年 :y20<br>10年 :y10<br>5年 :y5<br>3年 :y3<br>1年 :y1<br>metricsType<br>市值加权 :mcw<br>等权 :ew<br>正数等权 :ewpvo<br>平均值 :avg<br>中位数 :median<br>statisticsDataType<br>当前值 :cv<br>分位点% :cvpos<br>最小值 :minv<br>最大值 :maxv<br>最大正值 :maxpv<br>50%分位点值 :q5v<br>80%分位点值 :q8v<br>20%分位点值 :q2v<br>平均值 :avgv |

## API试用示例

```json
{
  "date": "2026-02-17",
  "stockCodes": [
    "HSI"
  ],
  "metricsList": [
    "pe_ttm.y10.mcw.cvpos",
    "pe_ttm.mcw",
    "mc"
  ]
}
```
