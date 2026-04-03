# 股票所属指数信息API

## 简要描述

获取股票所属指数信息。

## 请求URL

```
https://open.lixinger.com/api/cn/company/indices
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 股票代码请参考股票信息API获取合法的stockCode。 |
| date | No | String: YYYY-MM-DD(北京时间) | 信息时间。默认值是当前最新时间。 |

## API试用示例

### 获取最新时间股票所属指数信息

```json
{
  "stockCode": "300750"
}
```

### 获取指定日期股票所属指数信息

```json
{
  "date": "2026-02-23",
  "stockCode": "300750"
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| name | String | 指数名称 |
| areaCode | String | 地区代码 |
| stockCode | String | 指数代码 |
| source | String | 指数来源 中证 :csi 国证 :cni 恒生 :hsi 美指 :usi 理杏仁 :lxri |
