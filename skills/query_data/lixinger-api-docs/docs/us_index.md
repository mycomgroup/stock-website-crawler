# 指数信息API

## 简要描述

获取指数详细信息。

## 请求URL

```
https://open.lixinger.com/api/us/index
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 指数代码数组。默认值为所有指数的股票代码。格式如下：[".INX"]。<br>请参考指数信息API获取合法的stockCode。 |

## API试用示例

### 获取所有指数信息

```json
{}
```

### 获取指定指数信息

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
| name | String | 指数名称 |
| stockCode | String | 指数代码 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| fsTableType | String | 财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid |
| source | String | 指数来源 美指 :usi |
| currency | String | 货币 |
| series | String | 类型 规模 :size 综合 :composite 行业 :sector 风格 :style 主题 :thematic 策略 :strategy |
| launchDate | Date | 发布时间 |
| rebalancingFrequency | String | 调样频率 年度 :annually 半年 :semi-annually 季度 :quarterly 月度 :monthly 不定期 :irregularly 定期 :aperiodically |
| caculationMethod | String | 计算方式 派氏加权 :paasche 分级靠档加权 :grading_weighted 股息率加权 :dividend_grading 等权 :equal 自由流通市值加权 :free_float_cap 修正资本化加权 :modified_cap_weighted 流通市值加权 :negotiable_mc_weighted 债券成分券流通金额加权 :circulation_amount_of_constituent_bonds |
