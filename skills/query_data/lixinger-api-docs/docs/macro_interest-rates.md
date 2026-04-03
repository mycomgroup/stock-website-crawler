# 利率API

## 简要描述

获取利率数据，如活期存款等。

## 请求URL

```
https://open.lixinger.com/api/macro/interest-rates
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
| areaCode | Yes | String | 区域编码，如{areaCode}。<br>当前支持:<br>大陆: cn<br>香港: hk<br>美国: us |
| metricsList | Yes | Array | 指标数组。如['rmb_bdirofi_d']。<br>大陆支持:<br>活期存款 :rmb_bdirofi_d<br>定期存款（三个月） :rmb_bdirofi_m3<br>定期存款（半年） :rmb_bdirofi_hy<br>定期存款（一年） :rmb_bdirofi_y1<br>定期存款（两年） :rmb_bdirofi_y2<br>定期存款（三年） :rmb_bdirofi_y3<br>定期存款（五年） :rmb_bdirofi_y5<br>贷款：六个月以内（含六个月） :rmb_blrofi_wm6<br>贷款：一年以内（含一年） :rmb_blrofi_wy1<br>贷款：六个月至一年（含一年） :rmb_blrofi_m6ty1<br>贷款：一至三年（含三年） :rmb_blrofi_y1ty3<br>贷款：三至五年（含五年） :rmb_blrofi_y3ty5<br>贷款：一至五年（含五年） :rmb_blrofi_y1ty5<br>贷款：五年以上 :rmb_blrofi_mty5<br>一年期LRP :lpr_y1<br>五年及以上LPR :lpr_y5<br>三个月期MLF利率 :mlf_m3_r<br>六个月期MLF利率 :mlf_m6_r<br>一年期MLF利率 :mlf_y1_r<br>1个周Shibor :shibor_w1<br>2个周Shibor :shibor_w2<br>1个月Shibor :shibor_m1<br>3个月Shibor :shibor_m3<br>6个月Shibor :shibor_m6<br>9个月Shibor :shibor_m9<br>1年Shibor :shibor_y1<br>隔夜Shibor :shibor_on<br>中债商业银行同业存单(AAA)隔夜收益率 :cdnaaa_d1<br>中债商业银行同业存单(AAA)1周收益率 :cdnaaa_w1<br>中债商业银行同业存单(AAA)1个月收益率 :cdnaaa_m1<br>中债商业银行同业存单(AAA)6个月收益率 :cdnaaa_m6<br>中债商业银行同业存单(AAA)1年收益率 :cdnaaa_y1<br>隔夜回购定盘利率(FR001) :fr_d1<br>七天回购定盘利率(FR007) :fr_d7<br>十四天回购定盘利率(FR014) :fr_d14<br>银银间隔夜回购定盘利率(FDR001) :fdr_d1<br>银银间七天回购定盘利率(FDR007) :fdr_d7<br>银银间十四天回购定盘利率(FDR014) :fdr_d14<br>美国支持:<br>联邦基金（有效） :eff<br>金融商业票据：1个月 :fcp_m1<br>金融商业票据：2个月 :fcp_m2<br>金融商业票据：3个月 :fcp_m3<br>非金融商业票据：1个月 :nfcp_m1<br>非金融商业票据：2个月 :nfcp_m2<br>非金融商业票据：3个月 :nfcp_m3<br>银行优惠贷款 :bpl<br>贴现窗主要信贷 :dwpc<br>国库券（二级市场）：4周 :smtb_w4<br>国库券（二级市场）：3个月 :smtb_m3<br>国库券（二级市场）：6个月 :smtb_m6<br>国库券（二级市场）：1年 :smtb_y1<br>通货膨胀指数：5年 :ii_y5<br>通货膨胀指数：7年 :ii_y7<br>通货膨胀指数：10年 :ii_y10<br>通货膨胀指数：20年 :ii_y20<br>通货膨胀指数：30年 :ii_y30<br>通货膨胀指数长期平均值 :ltavg<br>香港支持:<br>1周Hibor :hibor_w1<br>2周Hibor :hibor_w2<br>1个月Hibor :hibor_m1<br>3个月Hibor :hibor_m3<br>6个月Hibor :hibor_m6<br>9个月Hibor :hibor_m9<br>1年Hibor :hibor_y1<br>隔夜Hibor :hibor_on |

## API试用示例

```json
{
  "areaCode": "cn",
  "startDate": "2016-02-23",
  "endDate": "2026-02-23",
  "metricsList": [
    "rmb_bdirofi_d"
  ]
}
```
