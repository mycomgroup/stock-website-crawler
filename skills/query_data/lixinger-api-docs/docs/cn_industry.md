# 股票信息API

## 简要描述

获取股票详细信息。

## 请求URL

```
https://open.lixinger.com/api/cn/industry
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | No | Array | 行业代码数组。默认值为所有行业的股票代码。格式如下：["490000"]。<br>请参考行业信息API获取合法的stockCode。 |
| source | Yes | String | 行业来源，例如：{source}。<br>当前支持:<br>申万: sw<br>申万2021版: sw_2021<br>国证: cni |
| level | No | String | 行业分类级别，例如：'one'。<br>当前支持:<br>一级: one<br>二级: two<br>三级: three |

## API试用示例

### 获取指定行业信息

```json
{
  "stockCodes": [
    "490000"
  ],
  "source": "sw"
}
```

### 获取指定分类级别的所有行业信息

```json
{
  "source": "sw",
  "level": "one"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| stockCode | String | 行业代码 |
| name | String | 行业名称 |
| launchDate | Date | 发布时间 |
| areaCode | String | 地区代码 |
| market | String | 市场 |
| fsTableType | String | 财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid |
| level | String | 行业分类等级 |
| source | String | 行业来源 国证 :cni 申万 :sw 申万2021版 :sw_2021 |
| currency | String | 货币 |
