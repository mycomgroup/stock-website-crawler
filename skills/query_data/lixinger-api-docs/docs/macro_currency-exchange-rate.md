# 汇率API

## 简要描述

获取汇率数据。

## 请求URL

```
https://open.lixinger.com/api/macro/currency-exchange-rate
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。开始和结束的时间间隔不超过10年 |
| endDate | Yes | String: YYYY-MM-DD(北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |
| fromCurrency | Yes | String | 当前支持:<br>元 :CNY<br>港币 :HKD<br>美元 :USD |
| toCurrency | Yes | String | 当前支持:<br>元 :CNY<br>支持兑换的货币:<br>HKD(港币)<br>USD(美元)<br>EUR(欧元)<br>JPY(日元)<br>港币 :HKD<br>支持兑换的货币:<br>CNY(元)<br>USD(美元)<br>JPY(日元)<br>EUR(欧元)<br>GBP(英镑)<br>SGD(新加坡元)<br>CAD(加拿大元)<br>MYR(马来西亚林吉特)<br>MOP(澳门元)<br>TWD(台湾元)<br>AUD(澳币)<br>THB(泰铢)<br>BRL(巴西雷亚尔)<br>美元 :USD<br>支持兑换的货币:<br>ARS(阿根廷比索)<br>AUD(澳币)<br>BRL(巴西雷亚尔)<br>CAD(加拿大元)<br>CHF(瑞士法郎)<br>CLP(智利比索)<br>CNY(元)<br>COP(哥伦比亚比索)<br>DKK(克朗)<br>EUR(欧元)<br>GBP(英镑)<br>HKD(港币)<br>MOP(澳门元)<br>IDR(印尼盾)<br>ILS(以色列谢克尔)<br>INR(印度卢比)<br>JPY(日元)<br>KRW(韩元)<br>MXN(墨西哥比索)<br>MYR(马来西亚林吉特)<br>NOK(挪威克朗)<br>PEN(秘鲁索尔)<br>PHP(菲律宾比索)<br>PLN(波兰兹罗提)<br>RUB(俄国卢布)<br>SEK(瑞典克朗)<br>TRY(土耳其里拉)<br>TWD(台湾元)<br>ZAR(南非兰特) |

## API试用示例

```json
{
  "startDate": "2026-02-16",
  "endDate": "2026-02-23",
  "fromCurrency": "USD",
  "toCurrency": "CNY"
}
```
