# 基金概况API

## 简要描述

获取基金概况数据。比如，投资目标、投资策略、子基金等。 说明: 主基金代码和子基金代码获取相同的数据。

## 请求URL

```
https://open.lixinger.com/api/cn/fund/profile
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金代码数组。stockCodes长度>=1且<=100，格式如下：["161725","005827"]。<br>请参考基金信息API获取合法的stockCode。 |

## API试用示例

```json
{
  "stockCodes": [
    "161725",
    "005827"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 财报日期 |
| c_name | String | 基金托管人 |
| e_t_short_name | String | 场内简称 |
| f_c_name | String | 基金公司 |
| inception_date | Date | 合同生效日 |
| op_mode | String | 运作方式 |
| m_stock_code | String | 基金主代码 |
| investment_o | String | 投资目标 |
| investment_s | String | 投资策略 |
| p_c_benchmark | Array | 业绩比较基准 |
| risk_r_c | String | 风险收益特征 |
| ipo_date | Date | 上市日期 |
| s_f_stock_codes | Array | 子基金代码 |
| feeder_funds | Array | 联接基金 |
