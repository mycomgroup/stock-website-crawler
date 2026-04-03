# 财报数据API

## 简要描述

获取财务数据，如营业收入、ROE等。

## 请求URL

```
https://open.lixinger.com/api/cn/company/fs/non_financial
```

## 请求方式

POST

## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| token | Yes | String | 我的Token页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。stockCodes长度>=1且<=100，格式如下：["300750","600519","600157"]。<br>请参考股票信息API获取合法的stockCode。<br>需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest | YYYY-MM-DD(北京时间) | 信息日期。用于获取指定日期数据。<br>由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。<br>其中，传入latest会得到最近1.1年内的最新财报数据。<br>需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年<br>需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。<br>需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。<br>需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。<br>当前支持:<br>granularity<br>年 :y<br>半年 :hy<br>季度 :q<br>expressionCalculateType<br>资产负债表:<br>年(y):<br>当期 :t<br>当期回溯值 :t_r<br>当期同比 :t_y2y<br>当期环比 :t_c2c<br>半年(hy):<br>当期 :t<br>当期回溯值 :t_r<br>当期同比 :t_y2y<br>当期环比 :t_c2c<br>半年 :c<br>半年回溯值 :c_r<br>半年同比 :c_y2y<br>半年环比 :c_c2c<br>季度(q):<br>当期 :t<br>当期回溯值 :t_r<br>当期同比 :t_y2y<br>当期环比 :t_c2c<br>单季 :c<br>单季回溯值 :c_r<br>单季同比 :c_y2y<br>单季环比 :c_c2c<br>利润表:<br>年(y):<br>累积 :t<br>累积回溯值 :t_r<br>累积同比 :t_y2y<br>半年(hy):<br>累积 :t<br>累积回溯值 :t_r<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>半年 :c<br>半年回溯值 :c_r<br>半年同比 :c_y2y<br>半年环比 :c_c2c<br>半年年比 :c_2y<br>TTM :ttm<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>季度(q):<br>累积 :t<br>累积回溯值 :t_r<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>单季 :c<br>单季回溯值 :c_r<br>单季同比 :c_y2y<br>单季环比 :c_c2c<br>单季年比 :c_2y<br>TTM :ttm<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>现金流量表:<br>年(y):<br>累积 :t<br>累积回溯值 :t_r<br>累积同比 :t_y2y<br>半年(hy):<br>累积 :t<br>累积回溯值 :t_r<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>半年 :c<br>半年回溯值 :c_r<br>半年同比 :c_y2y<br>半年环比 :c_c2c<br>半年年比 :c_2y<br>TTM :ttm<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>季度(q):<br>累积 :t<br>累积回溯值 :t_r<br>累积同比 :t_y2y<br>累积环比 :t_c2c<br>单季 :c<br>单季回溯值 :c_r<br>单季同比 :c_y2y<br>单季环比 :c_c2c<br>单季年比 :c_2y<br>TTM :ttm<br>TTM同比 :ttm_y2y<br>TTM环比 :ttm_c2c<br>tableName.fieldName<br>资产负债表<br>利润表<br>一、营业总收入 : ps.toi<br>营业收入 : ps.oi<br>利息收入 : ps.ii<br>已赚保费 : ps.ep<br>手续费及佣金收入 : ps.faci<br>其他业务收入 : ps.ooi<br>二、营业总成本 : ps.toc<br>营业成本 : ps.oc<br>毛利率(GM) : ps.gp_m<br>利息支出 : ps.ie<br>手续费及佣金支出 : ps.face<br>退保金 : ps.s<br>保险合同赔付支出 : ps.ce<br>提取保险责任准备金净额 : ps.iiicr<br>保单红利支出 : ps.phdrfpip<br>分保费用 : ps.rie<br>税金及附加 : ps.tas<br>销售费用 : ps.se<br>管理费用 : ps.ae<br>研发费用 : ps.rade<br>(备注)资本化研发支出 : ps.crade<br>(备注)资本化研发支出占比 : ps.crade_r<br>财务费用 : ps.fe<br>(其中)利息费用 : ps.ieife<br>(其中)利息收入 : ps.iiife<br>销售费用率 : ps.se_r<br>管理费用率 : ps.ae_r<br>研发费用率 : ps.rade_r<br>财务费用率 : ps.fe_r<br>营业费用率 : ps.oe_r<br>四项费用率 : ps.foe_r<br>加：其他收益 : ps.oic<br>投资收益 : ps.ivi<br>(其中)对联营企业及合营企业的投资收益 : ps.iifaajv<br>(其中)以摊余成本计量的金融资产终止确认产生的投资收益 : ps.iftdofamaac<br>汇兑收益 : ps.ei<br>净敞口套期收益 : ps.nehb<br>公允价值变动收益 : ps.ciofv<br>信用减值损失 : ps.cilor<br>资产减值损失 : ps.ailor<br>其他资产减值损失 : ps.oail<br>资产处置收益 : ps.adi<br>其他业务成本 : ps.ooe<br>核心利润 : ps.cp<br>核心利润率 : ps.cp_r<br>三、营业利润 : ps.op<br>营业利润率 : ps.op_s_r<br>其他营业利润率 : ps.op_op_r<br>加：营业外收入 : ps.noi<br>(其中)非流动资产毁损报废利得 : ps.ncadarg<br>减：营业外支出 : ps.noe<br>(其中)非流动资产毁损报废损失 : ps.ncadarl<br>四、利润总额 : ps.tp<br>研发费占利润总额比值 : ps.rade_tp_r<br>息税前净利润(EBIT) : ps.ebit<br>息税折旧及摊销前盈利(EBITDA) : ps.ebitda<br>减：所得税费用 : ps.ite<br>有效税率 : ps.ite_tp_r<br>五、净利润 : ps.np<br>净利润率 : ps.np_s_r<br>(一)持续经营净利润 : ps.npfco<br>(二)终止经营净利润 : ps.npfdco<br>归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc<br>归属于母公司普通股股东的净利润 : ps.npatoshopc<br>少数股东损益 : ps.npatmsh<br>归属于母公司普通股股东的扣除非经常性损益的净利润 : ps.npadnrpatoshaopc<br>扣非净利润占比 : ps.npadnrpatoshaopc_npatoshopc_r<br>归属于母公司普通股股东的加权ROE : ps.wroe<br>归属于母公司普通股股东的扣非加权ROE : ps.wdroe<br>六、基本每股收益 : ps.beps<br>稀释每股收益 : ps.deps<br>七、综合收益总额 : ps.tci<br>归属于母公司股东及其他权益持有者的综合收益总额 : ps.tciatshaoehopc<br>归属于母公司普通股股东的综合收益总额 : ps.tciatoshopc<br>归属于少数股东的综合收益总额 : ps.tciatmsh<br>其他综合收益的税后净额 : ps.natooci<br>八、区域收入<br>境内收入 : ps.d_oi<br>境内营业成本 : ps.d_oc<br>境内收入占比 : ps.d_oi_r<br>境内毛利率 : ps.d_gp_m<br>海外收入 : ps.o_oi<br>海外营业成本 : ps.o_oc<br>海外收入占比 : ps.o_oi_r<br>海外毛利率 : ps.o_gp_m<br>九、分红、融资及涨跌幅<br>分红金额 : ps.da<br>分红率 : ps.d_np_r<br>A股分红金额 : ps.da_om<br>A股融资金额 : ps.fa_om<br>年度涨跌幅 : ps.spc_a<br>十、客户及供应商<br>前五大客户收入占比 : ps.tfci_r<br>前五大供应商采购占比 : ps.tfsp_r<br>现金流量表<br>财务指标 |

## API试用示例

```json
{
  "date": "2025-09-30",
  "stockCodes": [
    "300750",
    "600519",
    "600157"
  ],
  "metricsList": [
    "q.ps.toi.t"
  ]
}
```

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
| -------- | -------- | ---- |
| date | Date | 财报日期 |
| reportDate | Date | 公告时间 |
| standardDate | Date | 标准财年时间（不同公司的财年不一样，有的年报12月结束，有的却是3月结束，还有的7月结束。例如2017-01-01到2017-06-30结束的年报，调整到2016-Q4，其余的季报和中报都相应的做类似调整。调整后具有通用性。） |
| stockCode | String | 股票代码 |
| reportType | String | 财报类型 |
| currency | String | 货币类型 |
| auditOpinionType | String | 审计意见 无保留意见 :unqualified_opinion 保留意见 :qualified_opinion 保留意见与解释性说明 :qualified_opinion_with_explanatory_notes 否定意见 :adverse_opinion 拒绝表示意见 :disclaimer_of_opinion 解释性说明 :explanatory_statement 无法表示意见 :unable_to_express_an_opinion 带强调事项段的无保留意见 :unqualified_opinion_with_highlighted_matter_paragraph |
