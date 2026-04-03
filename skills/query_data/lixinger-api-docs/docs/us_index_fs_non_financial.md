# 财报数据API

## 简要描述

获取财务数据，如营业收入、ROE等。 说明: 指标计算请参考指数财务数据计算

## 请求URL

```
https://open.lixinger.com/api/us/index/fs/non_financial
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。stockCodes长度>=1且<=100，格式如下：[".INX"]。<br>请参考指数信息API获取合法的stockCode。<br>需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest | YYYY-MM-DD(北京时间) | 信息日期。用于获取指定日期数据。<br>由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。<br>其中，传入latest会得到最近1.1年内的最新财报数据。<br>需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年<br>需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。<br>需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。<br>需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。<br>当前支持:<br>granularity<br>年 :y<br>半年 :hy<br>季度 :q<br>expressionCalculateType<br>资产负债表:<br>年(y):<br>当期 :t<br>当期同比 :t_y2y<br>TTM环比 :ttm_c2c<br>半年(hy):<br>当期 :t<br>当期原始值 :t_o<br>当期同比 :t_y2y<br>当期环比 :t_c2c<br>半年 :c<br>半年原始值 :c_o<br>半年同比 :c_y2y<br>半年环比 :c_c2c<br>季度(q):<br>当期 :t<br>当期原始值 :t_o<br>当期同比 :t_y2y<br>当期环比 :t_c2c<br>单季 :c<br>单季原始值 :c_o<br>单季同比 :c_y2y<br>单季环比 :c_c2c<br>利润表:<br>年(y):<br>累积 :t<br>累积原始值 :t_o<br>累积同比 :t_y2y<br>半年(hy):<br>累积 :t<br>累积原始值 :t_o<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>半年 :c<br>半年原始值 :c_o<br>半年同比 :c_y2y<br>半年环比 :c_c2c<br>半年年比 :c_2y<br>TTM :ttm<br>TTM原始值 :ttm_o<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>季度(q):<br>累积 :t<br>累积原始值 :t_o<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>单季 :c<br>单季原始值 :c_o<br>单季同比 :c_y2y<br>单季环比 :c_c2c<br>单季年比 :c_2y<br>TTM :ttm<br>TTM原始值 :ttm_o<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>现金流量表:<br>年(y):<br>累积 :t<br>累积原始值 :t_o<br>累积同比 :t_y2y<br>半年(hy):<br>累积 :t<br>累积原始值 :t_o<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>半年 :c<br>半年原始值 :c_o<br>半年同比 :c_y2y<br>半年环比 :c_c2c<br>半年年比 :c_2y<br>TTM :ttm<br>TTM原始值 :ttm_o<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>季度(q):<br>累积 :t<br>累积原始值 :t_o<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>单季 :c<br>单季原始值 :c_o<br>单季同比 :c_y2y<br>单季环比 :c_c2c<br>单季年比 :c_2y<br>TTM :ttm<br>TTM原始值 :ttm_o<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>tableName.fieldName<br>资产负债表<br>利润表<br>一、营业总收入 : ps.toi<br>营业收入 : ps.oi<br>营业成本 : ps.oc<br>毛利率(GM) : ps.gp_m<br>销售及行政开支 : ps.sgnae<br>研发费用 : ps.rade<br>研发费用率 : ps.rade_r<br>利息费用 : ps.ieife<br>二、利润总额 : ps.tp<br>所得税费用 : ps.ite<br>有效税率 : ps.ite_tp_r<br>研发费占利润总额比值 : ps.rade_tp_r<br>三、净利润 : ps.np<br>净利润率 : ps.np_s_r<br>归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc<br>归属于母公司普通股股东的净利润 : ps.npatoshopc<br>少数股东损益 : ps.npatmsh<br>五、分红及涨跌幅<br>分红金额 : ps.da<br>现金流量表<br>财务指标 |

## API试用示例

```json
{
  "date": "2023-12-31",
  "stockCodes": [
    ".INX"
  ],
  "metricsList": [
    "q.ps.toi.t"
  ]
}
```
