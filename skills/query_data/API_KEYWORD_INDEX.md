# 理杏仁 API 中文关键词索引

快速查找：使用 `grep` 搜索中文关键词，找到对应的 API。

```bash
# 示例：查找分红相关 API
grep -i "分红\|股息\|dividend" API_KEYWORD_INDEX.md

# 示例：查找市盈率相关 API
grep -i "市盈率\|PE\|pe_ttm" API_KEYWORD_INDEX.md

# 示例：查找营收相关 API
grep -i "营业收入\|营收\|revenue\|toi" API_KEYWORD_INDEX.md

# 示例：查找 ROE 相关 API
grep -i "ROE\|净资产收益率\|roe" API_KEYWORD_INDEX.md
```

---

## A股公司

### 股票信息 | company

**API 路径**: `cn/company`

**说明**: 获取股票详细信息。

**返回字段**:

- **公司总数** (`total`)
- **公司名称** (`name`)
- **股票代码** (`stockCode`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **交易所** (`exchange`)
- **财报类型** (`fsTableType`)
- **互联互通** (`mutualMarkets`)
- **是否是互联互通标的** (`mutualMarketFlag`)
- **是否是融资融券标的** (`marginTradingAndSecuritiesLendingFlag`)
- **上市时间** (`ipoDate`)
- **退市时间** (`delistedDate`)

**文档**: `lixinger-api-docs/docs/cn_company.md`

<!-- 搜索关键词: name mutualMarketFlag exchange 公司总数 areaCode marginTradingAndSecuritiesLendingFlag 互联互通 地区代码 上市时间 是否是融资融券标的 财报类型 股票信息 market 退市时间 市场 mutualMarkets delistedDate fsTableType total company 公司名称 交易所 stockCode 是否是互联互通标的 ipoDate 股票代码 -->

---

### 配股 | allotment

**API 路径**: `cn/company/allotment`

**说明**: 获取配股信息。

**返回字段**:

- **公告日期** (`date`)
- **除权除息日** (`exDate`)
- **货币** (`currency`)
- **配股比例** (`allotmentRatio`)
- **配股价格** (`allotmentPrice`)
- **实际配股数量** (`allotmentShares`)

**文档**: `lixinger-api-docs/docs/cn_company_allotment.md`

<!-- 搜索关键词: allotmentPrice exDate date currency 公告日期 配股 配股比例 allotmentShares 除权除息日 配股价格 实际配股数量 allotmentRatio 货币 allotment -->

---

### 公告 | announcement

**API 路径**: `cn/company/announcement`

**说明**: 获取公告信息。

**返回字段**:

- **公告日期** (`date`)
- **链接文本** (`linkText`)
- **链接地址** (`linkUrl`)
- **链接类型** (`linkType`)
- **种类 全部 :all 财务报表 :fs 业绩预告 :fsfc 经营数据 :o_d 权益分派 :eac 董事会 :bm 监事会 :sm 股东大会 :shm 股权激励 :so 解禁 :ntsu 债券 :b 可转换债券 :c_b 股权变更 :eat 澄清及风险提示 :c_rp 投资者关系 :irs 问询函 :i_l 配股 :sa 增发 :spo 回购 :srp IPO :ipo 其它 :other** (`types`)

**文档**: `lixinger-api-docs/docs/cn_company_announcement.md`

<!-- 搜索关键词: 链接类型 date 公告日期 链接文本 链接地址 announcement types 种类 全部 :all 财务报表 :fs 业绩预告 :fsfc 经营数据 :o_d 权益分派 :eac 董事会 :bm 监事会 :sm 股东大会 :shm 股权激励 :so 解禁 :ntsu 债券 :b 可转换债券 :c_b 股权变更 :eat 澄清及风险提示 :c_rp 投资者关系 :irs 问询函 :i_l 配股 :sa 增发 :spo 回购 :srp IPO :ipo 其它 :other 公告 linkUrl linkType linkText -->

---

### 大宗交易 | block-deal

**API 路径**: `cn/company/block-deal`

**说明**: 获取大宗交易数据。

**返回字段**:

- **数据时间** (`date`)
- **股票代码** (`stockCode`)
- **成交价** (`tradingPrice`)
- **成交金额** (`tradingAmount`)
- **成交量** (`tradingVolume`)
- **买入营业部** (`buyBranch`)
- **卖出营业部** (`sellBranch`)
- **折价率** (`discountRate`)

**文档**: `lixinger-api-docs/docs/cn_company_block-deal.md`

<!-- 搜索关键词: tradingPrice 买入营业部 date tradingAmount 数据时间 stockCode 成交量 大宗交易 tradingVolume sellBranch discountRate 折价率 成交金额 buyBranch 卖出营业部 成交价 股票代码 block-deal -->

---

### K线数据 | candlestick

**API 路径**: `cn/company/candlestick`

**说明**: 获取K线数据。 说明: 复权计算仅对所选时间段的价格进行复权 成交量不进行复权计算

**返回字段**:

- **数据时间** (`date`)
- **股票代码** (`stockCode`)
- **开盘价** (`open`)
- **收盘价** (`close`)
- **最高价** (`high`)
- **最低价** (`low`)
- **成交量** (`volume`)
- **金额** (`amount`)
- **涨跌幅** (`change`)
- **换手率** (`to_r`)
- **复权因子** (`complexFactor`)

**文档**: `lixinger-api-docs/docs/cn_company_candlestick.md`

<!-- 搜索关键词: volume 复权因子 amount high change close 开盘价 数据时间 K线数据 涨跌幅 candlestick 换手率 open date 最高价 最低价 complexFactor stockCode 金额 low to_r 股票代码 成交量 收盘价 -->

---

### 客户 | customers

**API 路径**: `cn/company/customers`

**说明**: 获取客户信息。

**返回字段**:

- **数据时间** (`date`)
- **公告日期** (`declarationDate`)

**文档**: `lixinger-api-docs/docs/cn_company_customers.md`

<!-- 搜索关键词: date 数据时间 公告日期 客户 customers declarationDate -->

---

### 分红 | dividend

**API 路径**: `cn/company/dividend`

**说明**: 获取分红信息。

**返回字段**:

- **公告日期** (`date`)
- **内容** (`content`)
- **送股(股)** (`bonusSharesFromProfit`)
- **转增(股)** (`bonusSharesFromCapitalReserve`)
- **分红** (`dividend`)
- **货币** (`currency`)
- **分红金额** (`dividendAmount`)
- **年度净利润** (`annualNetProfit`)
- **年度净利润分红比例** (`annualNetProfitDividendRatio`)
- **股权登记日** (`registerDate`)
- **除权除息日** (`exDate`)
- **分红到账日** (`paymentDate`)
- **财报时间** (`fsEndDate`)

**文档**: `lixinger-api-docs/docs/cn_company_dividend.md`

<!-- 搜索关键词: exDate bonusSharesFromProfit annualNetProfit 股权登记日 currency annualNetProfitDividendRatio content 分红 分红到账日 dividendAmount 年度净利润分红比例 dividend 送股(股) date 分红金额 paymentDate 转增(股) 财报时间 内容 年度净利润 registerDate 公告日期 bonusSharesFromCapitalReserve 除权除息日 fsEndDate 货币 -->

---

### 股本变动 | equity-change

**API 路径**: `cn/company/equity-change`

**说明**: 获取股本变动数据。

**返回字段**:

- **变动日期** (`date`)
- **公告日期** (`declarationDate`)
- **变动原因** (`changeReason`)
- **总股本** (`capitalization`)
- **流通A股** (`outstandingSharesA`)
- **限售A股** (`limitedSharesA`)
- **流通H股** (`outstandingSharesH`)
- **总股本变动比例** (`capitalizationChangeRatio`)
- **流通A股变动比例** (`outstandingSharesAChangeRatio`)
- **限售A股变动比例** (`limitedSharesAChangeRatio`)
- **流通H股变动比例** (`outstandingSharesHChangeRatio`)

**文档**: `lixinger-api-docs/docs/cn_company_equity-change.md`

<!-- 搜索关键词: limitedSharesAChangeRatio 股本变动 outstandingSharesAChangeRatio 总股本变动比例 limitedSharesA capitalizationChangeRatio 流通H股变动比例 变动日期 流通A股 限售A股 date changeReason 流通A股变动比例 流通H股 变动原因 declarationDate capitalization 限售A股变动比例 总股本 公告日期 outstandingSharesA outstandingSharesH equity-change outstandingSharesHChangeRatio -->

---

### 财报数据 | non_financial

**API 路径**: `cn/company/fs/non_financial`

**说明**: 获取财务数据，如营业收入、ROE等。

**返回字段**:

- **财报日期** (`date`)
- **公告时间** (`reportDate`)
- **标准财年时间（不同公司的财年不一样，有的年报12月结束，有的却是3月结束，还有的7月结束。例如2017-01-01到2017-06-30结束的年报，调整到2016-Q4，其余的季报和中报都相应的做类似调整。调整后具有通用性。）** (`standardDate`)
- **股票代码** (`stockCode`)
- **财报类型** (`reportType`)
- **货币类型** (`currency`)
- **审计意见 无保留意见 :unqualified_opinion 保留意见 :qualified_opinion 保留意见与解释性说明 :qualified_opinion_with_explanatory_notes 否定意见 :adverse_opinion 拒绝表示意见 :disclaimer_of_opinion 解释性说明 :explanatory_statement 无法表示意见 :unable_to_express_an_opinion 带强调事项段的无保留意见 :unqualified_opinion_with_highlighted_matter_paragraph** (`auditOpinionType`)

**文档**: `lixinger-api-docs/docs/cn_company_fs_non_financial.md`

<!-- 搜索关键词: 财报类型 财报数据 date non_financial 审计意见 无保留意见 :unqualified_opinion 保留意见 :qualified_opinion 保留意见与解释性说明 :qualified_opinion_with_explanatory_notes 否定意见 :adverse_opinion 拒绝表示意见 :disclaimer_of_opinion 解释性说明 :explanatory_statement 无法表示意见 :unable_to_express_an_opinion 带强调事项段的无保留意见 :unqualified_opinion_with_highlighted_matter_paragraph currency auditOpinionType 公告时间 standardDate 标准财年时间（不同公司的财年不一样，有的年报12月结束，有的却是3月结束，还有的7月结束。例如2017-01-01到2017-06-30结束的年报，调整到2016-Q4，其余的季报和中报都相应的做类似调整。调整后具有通用性。） stockCode 货币类型 财报日期 reportDate reportType 股票代码 -->

---

### 基金公司持股 | fund-collection-shareholders

**API 路径**: `cn/company/fund-collection-shareholders`

**说明**: 获取基金公司持股信息。

**返回字段**:

- **公告日期** (`date`)
- **姓名** (`name`)
- **基金公司代码** (`fundCollectionCode`)
- **持仓** (`holdings`)
- **市值** (`marketCap`)
- **流通A股** (`outstandingSharesA`)
- **流通A股占比** (`proportionOfCapitalization`)

**文档**: `lixinger-api-docs/docs/cn_company_fund-collection-shareholders.md`

<!-- 搜索关键词: name 流通A股占比 date marketCap 公告日期 fund-collection-shareholders outstandingSharesA 基金公司代码 持仓 fundCollectionCode holdings 流通A股 市值 基金公司持股 proportionOfCapitalization 姓名 -->

---

### 公募基金持股 | fund-shareholders

**API 路径**: `cn/company/fund-shareholders`

**说明**: 获取公募基金持股信息。

**返回字段**:

- **数据时间** (`date`)
- **基金代码** (`fundCode`)
- **基金名称** (`name`)
- **持仓** (`holdings`)
- **市值** (`marketCap`)
- **当前股票所在基金持仓排名** (`marketCapRank`)
- **基金持仓占基金规模比例** (`netValueRatio`)
- **流通A股** (`outstandingSharesA`)
- **流通A股占比** (`proportionOfCapitalization`)

**文档**: `lixinger-api-docs/docs/cn_company_fund-shareholders.md`

<!-- 搜索关键词: name marketCap 基金代码 基金名称 当前股票所在基金持仓排名 netValueRatio 数据时间 流通A股 基金持仓占基金规模比例 持仓 date holdings 市值 marketCapRank 流通A股占比 公募基金持股 fundCode outstandingSharesA proportionOfCapitalization fund-shareholders -->

---

### 基本面数据 | non_financial

**API 路径**: `cn/company/fundamental/non_financial`

**说明**: 获取基本面数据，如PE、PB等。

**文档**: `lixinger-api-docs/docs/cn_company_fundamental_financial.md`

<!-- 搜索关键词: 基本面数据 non_financial -->

---

### 基本面数据 | non_financial

**API 路径**: `cn/company/fundamental/non_financial`

**说明**: 获取基本面数据，如PE、PB等。

**文档**: `lixinger-api-docs/docs/cn_company_fundamental_non_financial.md`

<!-- 搜索关键词: 基本面数据 non_financial -->

---

### 分红再投入收益率 | tr_dri

**API 路径**: `cn/company/hot/tr_dri`

**说明**: 获取分红再投入收益率数据。 说明: 理杏仁采用分红再投入策略计算投资收益率

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **指定时间段投资收益率** (`p_r`)
- **今年以来投资收益率** (`cagr_p_r_fys`)
- **近7日投资收益率** (`cagr_p_r_d7`)
- **近14日投资收益率** (`cagr_p_r_d14`)
- **近30日投资收益率** (`cagr_p_r_d30`)
- **近60日投资收益率** (`cagr_p_r_d60`)
- **近90日投资收益率** (`cagr_p_r_d90`)
- **近一年投资收益率** (`cagr_p_r_y1`)
- **近三年年化投资收益率** (`cagr_p_r_y3`)
- **近五年年化投资收益率** (`cagr_p_r_y5`)
- **近十年年化投资收益率** (`cagr_p_r_y10`)
- **近二十年年化投资收益率** (`cagr_p_r_y20`)
- **上市至今年化投资收益率** (`cagr_p_r_fs`)
- **上市以来总投资收益率** (`p_r_fs`)
- **投资收益率计算起始日期** (`period_date`)

**文档**: `lixinger-api-docs/docs/cn_company_hot_tr_dri.md`

<!-- 搜索关键词: 近二十年年化投资收益率 cagr_p_r_d7 cagr_p_r_d30 p_r cagr_p_r_y1 股票代码 今年以来投资收益率 近90日投资收益率 p_r_fs 数据时间 cagr_p_r_y20 cagr_p_r_d14 cagr_p_r_d90 近30日投资收益率 分红再投入收益率 上市以来总投资收益率 近60日投资收益率 cagr_p_r_fs 近7日投资收益率 投资收益率计算起始日期 cagr_p_r_fys 近五年年化投资收益率 上市至今年化投资收益率 近一年投资收益率 last_data_date tr_dri 近三年年化投资收益率 cagr_p_r_d60 stockCode 近十年年化投资收益率 period_date 近14日投资收益率 指定时间段投资收益率 cagr_p_r_y5 cagr_p_r_y3 cagr_p_r_y10 -->

---

### 股票所属指数信息 | indices

**API 路径**: `cn/company/indices`

**说明**: 获取股票所属指数信息。

**返回字段**:

- **指数名称** (`name`)
- **地区代码** (`areaCode`)
- **指数代码** (`stockCode`)
- **指数来源 中证 :csi 国证 :cni 恒生 :hsi 美指 :usi 理杏仁 :lxri** (`source`)

**文档**: `lixinger-api-docs/docs/cn_company_indices.md`

<!-- 搜索关键词: name indices 指数名称 指数来源 中证 :csi 国证 :cni 恒生 :hsi 美指 :usi 理杏仁 :lxri source stockCode areaCode 股票所属指数信息 地区代码 指数代码 -->

---

### 股票所属行业信息 | industries

**API 路径**: `cn/company/industries`

**说明**: 获取股票所属行业信息。

**返回字段**:

- **行业名称** (`name`)
- **地区代码** (`areaCode`)
- **行业代码** (`stockCode`)
- **行业来源 申万 :sw 申万2021版 :sw_2021 国证 :cni** (`source`)

**文档**: `lixinger-api-docs/docs/cn_company_industries.md`

<!-- 搜索关键词: name industries 行业代码 source 股票所属行业信息 stockCode areaCode 行业来源 申万 :sw 申万2021版 :sw_2021 国证 :cni 行业名称 地区代码 -->

---

### 问询函 | inquiry

**API 路径**: `cn/company/inquiry`

**说明**: 获取问询函信息。

**返回字段**:

- **公告日期** (`date`)
- **种类 问询函 :il 定期报告审核意见函 :olo_prpa 重大资产重组预案审核意见函 :olo_romarp** (`type`)
- **显示类型文本** (`displayTypeText`)
- **链接文本** (`linkText`)
- **链接地址** (`linkUrl`)
- **链接类型** (`linkType`)

**文档**: `lixinger-api-docs/docs/cn_company_inquiry.md`

<!-- 搜索关键词: 链接类型 date displayTypeText 种类 问询函 :il 定期报告审核意见函 :olo_prpa 重大资产重组预案审核意见函 :olo_romarp type 公告日期 问询函 链接文本 链接地址 显示类型文本 linkUrl linkType inquiry linkText -->

---

### 大股东增减持 | major-shareholders-shares-change

**API 路径**: `cn/company/major-shareholders-shares-change`

**说明**: 获取大股东增减持数据。

**返回字段**:

- **数据时间** (`date`)
- **股东名称** (`shareholderName`)
- **变动持股量** (`changeQuantity`)
- **变动数量占总股本比例** (`sharesChangeRatio`)
- **增(减)持价格下限** (`priceFloor`)
- **增(减)持价格上限** (`priceCeiling`)
- **增减持平均价格【如果没有价格上下限，我们会根据数据时间所在交易日的成交均价做计算】** (`avgPrice`)
- **变动后持股数量** (`quantityHeldAfterChange`)
- **变动后占比** (`sharesHeldAfterChange`)
- **增减持金额** (`sharesChangeAmount`)

**文档**: `lixinger-api-docs/docs/cn_company_major-shareholders-shares-change.md`

<!-- 搜索关键词: sharesChangeRatio 股东名称 增(减)持价格上限 变动后占比 sharesChangeAmount 数据时间 shareholderName 增(减)持价格下限 增减持平均价格【如果没有价格上下限，我们会根据数据时间所在交易日的成交均价做计算】 major-shareholders-shares-change date priceCeiling 增减持金额 priceFloor sharesHeldAfterChange 大股东增减持 变动持股量 quantityHeldAfterChange 变动后持股数量 avgPrice 变动数量占总股本比例 changeQuantity -->

---

### 前十大股东持股 | majority-shareholders

**API 路径**: `cn/company/majority-shareholders`

**说明**: 获取前十大股东持股信息。

**返回字段**:

- **数据时间** (`date`)
- **姓名** (`name`)
- **持仓** (`holdings`)
- **性质** (`property`)
- **总股本** (`capitalization`)
- **总股本占比** (`proportionOfCapitalization`)

**文档**: `lixinger-api-docs/docs/cn_company_majority-shareholders.md`

<!-- 搜索关键词: name 性质 date 总股本 capitalization 总股本占比 数据时间 前十大股东持股 majority-shareholders holdings property 持仓 proportionOfCapitalization 姓名 -->

---

### 融资融券 | margin-trading-and-securities-lending

**API 路径**: `cn/company/margin-trading-and-securities-lending`

**说明**: 获取融资融券数据。

**返回字段**:

- **公告日期** (`date`)
- **融资买入金额** (`financingPurchaseAmount`)
- **融资偿还金额** (`financingRepaymentAmount`)
- **融资余额** (`financingBalance`)
- **融券卖出量** (`securitiesSellVolume`)
- **融券偿还量** (`securitiesRepaymentVolume`)
- **融券卖出金额** (`securitiesSellAmount`)
- **融券偿还金额** (`securitiesRepaymentAmount`)
- **融券余额** (`securitiesBalance`)
- **融券余量** (`securitiesMargin`)
- **融资融券余额** (`financingSecuritiesBalance`)

**文档**: `lixinger-api-docs/docs/cn_company_margin-trading-and-securities-lending.md`

<!-- 搜索关键词: 融资偿还金额 融券余量 融券余额 securitiesRepaymentAmount securitiesRepaymentVolume 融券偿还量 securitiesSellVolume financingPurchaseAmount 融资融券余额 financingSecuritiesBalance 融资融券 融券卖出量 date 融券偿还金额 融资余额 securitiesBalance 融券卖出金额 financingBalance margin-trading-and-securities-lending securitiesSellAmount securitiesMargin 融资买入金额 公告日期 financingRepaymentAmount -->

---

### 监管措施 | measures

**API 路径**: `cn/company/measures`

**说明**: 获取监管措施信息。

**返回字段**:

- **公告日期** (`date`)
- **种类 监管警示 :sw 通报批评 :bc 公开谴责及认定 :pcar 监管工作函 :sl** (`type`)
- **显示类型文本** (`displayTypeText`)
- **链接文本** (`linkText`)
- **链接地址** (`linkUrl`)
- **链接类型** (`linkType`)
- **对象** (`referent`)

**文档**: `lixinger-api-docs/docs/cn_company_measures.md`

<!-- 搜索关键词: 链接类型 date displayTypeText type 公告日期 链接文本 链接地址 种类 监管警示 :sw 通报批评 :bc 公开谴责及认定 :pcar 监管工作函 :sl 显示类型文本 linkUrl linkType referent measures 对象 监管措施 linkText -->

---

### 互联互通 | mutual-market

**API 路径**: `cn/company/mutual-market`

**说明**: 获取互联互通数据。

**返回字段**:

- **数据时间** (`date`)
- **持股数量** (`shareholdings`)

**文档**: `lixinger-api-docs/docs/cn_company_mutual-market.md`

<!-- 搜索关键词: date shareholdings mutual-market 持股数量 数据时间 互联互通 -->

---

### 前十大流通股东持股 | nolimit-shareholders

**API 路径**: `cn/company/nolimit-shareholders`

**说明**: 获取前十大流通股东持股信息。

**返回字段**:

- **数据时间** (`date`)
- **姓名** (`name`)
- **持仓** (`holdings`)
- **性质** (`property`)
- **流通A股** (`outstandingSharesA`)
- **流通A股占比** (`proportionOfOutstandingSharesA`)

**文档**: `lixinger-api-docs/docs/cn_company_nolimit-shareholders.md`

<!-- 搜索关键词: name 性质 流通A股占比 date 流通A股 proportionOfOutstandingSharesA 数据时间 outstandingSharesA 持仓 holdings property nolimit-shareholders 前十大流通股东持股 姓名 -->

---

### 经营数据 | operating-data

**API 路径**: `cn/company/operating-data`

**说明**: 获取经营数据信息。

**返回字段**:

- **数据时间** (`date`)
- **公告日期** (`declarationDate`)
- **开始日期** (`startDate`)

**文档**: `lixinger-api-docs/docs/cn_company_operating-data.md`

<!-- 搜索关键词: date startDate operating-data 开始日期 数据时间 公告日期 declarationDate 经营数据 -->

---

### 营收构成 | operation-revenue-constitution

**API 路径**: `cn/company/operation-revenue-constitution`

**说明**: 获取营收构成数据。

**返回字段**:

- **数据时间** (`date`)
- **公告日期** (`declarationDate`)

**文档**: `lixinger-api-docs/docs/cn_company_operation-revenue-constitution.md`

<!-- 搜索关键词: date 数据时间 公告日期 营收构成 operation-revenue-constitution declarationDate -->

---

### 股权质押 | pledge

**API 路径**: `cn/company/pledge`

**说明**: 获取股权质押数据。

**返回字段**:

- **数据时间** (`date`)
- **出质人** (`pledgor`)
- **质权人** (`pledgee`)
- **质押事项** (`pledgeMatters`)
- **质押股份性质** (`pledgeSharesNature`)
- **质押数量** (`pledgeAmount`)
- **占总股比例** (`pledgePercentageOfTotalEquity`)
- **质押起始日** (`pledgeStartDate`)
- **质押终止日** (`pledgeEndDate`)
- **质押解除日** (`pledgeDischargeDate`)
- **质押解除解释** (`pledgeDischargeExplanation`)
- **质押解除数量** (`pledgeDischargeAmount`)
- **是否质押式回购交易** (`isPledgeRepurchaseTransactions`)
- **累计质押占总股比例** (`accumulatedPledgePercentageOfTotalEquity`)

**文档**: `lixinger-api-docs/docs/cn_company_pledge.md`

<!-- 搜索关键词: 占总股比例 pledgeMatters 质押解除解释 是否质押式回购交易 pledgeEndDate 数据时间 pledgor 质押股份性质 isPledgeRepurchaseTransactions pledgeDischargeDate 质押解除日 date accumulatedPledgePercentageOfTotalEquity 质权人 pledgeSharesNature pledgePercentageOfTotalEquity pledgeStartDate pledge pledgeDischargeAmount 质押事项 质押解除数量 股权质押 质押起始日 pledgeDischargeExplanation 出质人 pledgee 质押数量 累计质押占总股比例 pledgeAmount 质押终止日 -->

---

### 公司概况 | profile

**API 路径**: `cn/company/profile`

**说明**: 获取公司概况数据

**返回字段**:

- **股票代码** (`stockCode`)
- **公司名称** (`companyName`)
- **历史名称 新名称 :newName 老名称 :oldName** (`historyStockNames`)
- **省份** (`province`)
- **城市** (`city`)
- **实际控制人类型 自然人 :natural_person 集体 :collective 外企 :foreign_company 国有 :state_owned** (`actualControllerTypes`)
- **实际控制人** (`actualControllerName`)

**文档**: `lixinger-api-docs/docs/cn_company_profile.md`

<!-- 搜索关键词: city 历史名称 新名称 :newName 老名称 :oldName actualControllerName profile 公司名称 城市 stockCode companyName historyStockNames 省份 actualControllerTypes 实际控制人 province 实际控制人类型 自然人 :natural_person 集体 :collective 外企 :foreign_company 国有 :state_owned 股票代码 公司概况 -->

---

### 高管增减持 | senior-executive-shares-change

**API 路径**: `cn/company/senior-executive-shares-change`

**说明**: 获取高管增减持数据。

**返回字段**:

- **数据时间** (`date`)
- **股东名称** (`shareholderName`)
- **高管姓名** (`executiveName`)
- **职务** (`duty`)
- **持股人与高管关系** (`relationBetweenES`)
- **变动原因** (`changeReason`)
- **变动前持股量** (`beforeChangeShares`)
- **变动持股量** (`changedShares`)
- **变动后持股量** (`afterChangeShares`)
- **成交均价** (`avgPrice`)
- **增减持金额** (`sharesChangeAmount`)
- **增减持占总股本比例** (`changedSharesForCapitalizationProportion`)

**文档**: `lixinger-api-docs/docs/cn_company_senior-executive-shares-change.md`

<!-- 搜索关键词: 高管增减持 高管姓名 股东名称 sharesChangeAmount executiveName 成交均价 变动前持股量 changedSharesForCapitalizationProportion 数据时间 shareholderName 持股人与高管关系 relationBetweenES 变动后持股量 date 增减持金额 changeReason changedShares beforeChangeShares 变动原因 增减持占总股本比例 afterChangeShares 职务 变动持股量 avgPrice senior-executive-shares-change duty -->

---

### 股东人数 | shareholders-num

**API 路径**: `cn/company/shareholders-num`

**说明**: 获取股东人数数据。

**返回字段**:

- **数据时间** (`date`)
- **股东人数** (`total`)
- **股东人数变化比例** (`shareholdersNumberChangeRate`)
- **股价涨跌幅** (`spc`)

**文档**: `lixinger-api-docs/docs/cn_company_shareholders-num.md`

<!-- 搜索关键词: 股东人数变化比例 date shareholders-num shareholdersNumberChangeRate 数据时间 股价涨跌幅 股东人数 spc total -->

---

### 供应商 | suppliers

**API 路径**: `cn/company/suppliers`

**说明**: 获取供应商API

**返回字段**:

- **数据时间** (`date`)
- **公告日期** (`declarationDate`)

**文档**: `lixinger-api-docs/docs/cn_company_suppliers.md`

<!-- 搜索关键词: date 数据时间 suppliers 公告日期 供应商 declarationDate -->

---

### 龙虎榜 | trading-abnormal

**API 路径**: `cn/company/trading-abnormal`

**说明**: 获取龙虎榜信息。

**返回字段**:

- **数据时间** (`date`)
- **披露原因** (`reasonForDisclosure`)

**文档**: `lixinger-api-docs/docs/cn_company_trading-abnormal.md`

<!-- 搜索关键词: date 数据时间 trading-abnormal reasonForDisclosure 披露原因 龙虎榜 -->

---

## A股指数

### 指数信息 | index

**API 路径**: `cn/index`

**说明**: 获取指数详细信息。

**返回字段**:

- **指数名称** (`name`)
- **指数代码** (`stockCode`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid** (`fsTableType`)
- **指数来源 国证 :cni 中证 :csi 理杏仁 :lxri** (`source`)
- **货币** (`currency`)
- **类型 规模 :size 综合 :composite 行业 :sector 风格 :style 主题 :thematic 策略 :strategy** (`series`)
- **发布时间** (`launchDate`)
- **调样频率 年度 :annually 半年 :semi-annually 季度 :quarterly 月度 :monthly 不定期 :irregularly 定期 :aperiodically** (`rebalancingFrequency`)
- **计算方式 派氏加权 :paasche 分级靠档加权 :grading_weighted 股息率加权 :dividend_grading 等权 :equal 自由流通市值加权 :free_float_cap 修正资本化加权 :modified_cap_weighted 流通市值加权 :negotiable_mc_weighted 债券成分券流通金额加权 :circulation_amount_of_constituent_bonds** (`caculationMethod`)

**文档**: `lixinger-api-docs/docs/cn_index.md`

<!-- 搜索关键词: name 指数来源 国证 :cni 中证 :csi 理杏仁 :lxri areaCode 类型 规模 :size 综合 :composite 行业 :sector 风格 :style 主题 :thematic 策略 :strategy 计算方式 派氏加权 :paasche 分级靠档加权 :grading_weighted 股息率加权 :dividend_grading 等权 :equal 自由流通市值加权 :free_float_cap 修正资本化加权 :modified_cap_weighted 流通市值加权 :negotiable_mc_weighted 债券成分券流通金额加权 :circulation_amount_of_constituent_bonds series 地区代码 财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid caculationMethod market currency 发布时间 市场 launchDate 指数名称 调样频率 年度 :annually 半年 :semi-annually 季度 :quarterly 月度 :monthly 不定期 :irregularly 定期 :aperiodically index source rebalancingFrequency fsTableType 指数代码 stockCode 货币 指数信息 -->

---

### K线数据 | candlestick

**API 路径**: `cn/index/candlestick`

**说明**: 获取K线数据。 说明: 中证指数全收益率2016年以前没有数据。

**返回字段**:

- **数据时间** (`date`)
- **开盘价** (`open`)
- **收盘价** (`close`)
- **最高价** (`high`)
- **最低价** (`low`)
- **成交量** (`volume`)
- **金额** (`amount`)
- **涨跌幅** (`change`)

**文档**: `lixinger-api-docs/docs/cn_index_candlestick.md`

<!-- 搜索关键词: change volume date close 开盘价 数据时间 K线数据 金额 low amount 最高价 candlestick 最低价 涨跌幅 成交量 open 收盘价 high -->

---

### 指数样本权重 | constituent-weightings

**API 路径**: `cn/index/constituent-weightings`

**说明**: 获取指数样本权重信息。

**返回字段**:

- **数据时间** (`date`)
- **股票代码** (`stockCode`)
- **权重** (`weighting`)

**文档**: `lixinger-api-docs/docs/cn_index_constituent-weightings.md`

<!-- 搜索关键词: date constituent-weightings 数据时间 stockCode 指数样本权重 weighting 股票代码 权重 -->

---

### 样本信息 | constituents

**API 路径**: `cn/index/constituents`

**说明**: 获取样本信息。

**返回字段**:

- **指数代码** (`stockCode`)

**文档**: `lixinger-api-docs/docs/cn_index_constituents.md`

<!-- 搜索关键词: 指数代码 stockCode 样本信息 constituents -->

---

### 指数回撤 | drawdown

**API 路径**: `cn/index/drawdown`

**说明**: 获取指数回撤数据。

**返回字段**:

- **数据时间** (`date`)
- **回撤** (`value`)

**文档**: `lixinger-api-docs/docs/cn_index_drawdown.md`

<!-- 搜索关键词: date 回撤 数据时间 drawdown value 指数回撤 -->

---

### 财报数据 | hybrid

**API 路径**: `cn/index/fs/hybrid`

**说明**: 获取财务数据，如营业收入、ROE等。 说明: 指标计算请参考指数财务数据计算

**文档**: `lixinger-api-docs/docs/cn_index_fs_hybrid.md`

<!-- 搜索关键词: 财报数据 hybrid -->

---

### 基本面数据 | fundamental

**API 路径**: `cn/index/fundamental`

**说明**: 获取基本面数据，如PE、PB等。 说明: 指标计算请参考指数估值计算

**文档**: `lixinger-api-docs/docs/cn_index_fundamental.md`

<!-- 搜索关键词: 基本面数据 fundamental -->

---

### 互联互通 | mm_ha

**API 路径**: `cn/index/hot/mm_ha`

**说明**: 获取互联互通数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **涨跌幅** (`cpc`)
- **陆股通持仓金额** (`mm_sha`)
- **陆股通持仓金额占市值比例** (`mm_sha_mc_r`)
- **陆股通过去1个季度净买入金额** (`mm_sh_nba_q1`)
- **陆股通过去2个季度净买入金额** (`mm_sh_nba_q2`)
- **陆股通过去3个季度净买入金额** (`mm_sh_nba_q3`)
- **陆股通过去4个季度净买入金额** (`mm_sh_nba_q4`)
- **陆股通过去1个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q1`)
- **陆股通过去2个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q2`)
- **陆股通过去3个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q3`)
- **陆股通过去4个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q4`)

**文档**: `lixinger-api-docs/docs/cn_index_hot_mm_ha.md`

<!-- 搜索关键词: 陆股通过去3个季度净买入金额 陆股通过去2个季度持股金额占市值变化比例 mm_sha_mc_r 互联互通 陆股通过去1个季度持股金额占市值变化比例 mm_sha_mc_rc_q3 陆股通过去4个季度持股金额占市值变化比例 mm_sh_nba_q2 陆股通过去2个季度净买入金额 数据时间 涨跌幅 mm_sha_mc_rc_q1 mm_sha_mc_rc_q2 mm_sh_nba_q3 cpc mm_sha_mc_rc_q4 last_data_date mm_ha 陆股通持仓金额占市值比例 陆股通持仓金额 mm_sh_nba_q4 陆股通过去1个季度净买入金额 mm_sha stockCode 陆股通过去3个季度持股金额占市值变化比例 股票代码 mm_sh_nba_q1 陆股通过去4个季度净买入金额 -->

---

### 融资融券 | margin-trading-and-securities-lending

**API 路径**: `cn/index/margin-trading-and-securities-lending`

**说明**: 获取融资融券数据。

**返回字段**:

- **数据时间** (`date`)
- **融资余额** (`financingBalance`)
- **融券余额** (`securitiesBalance`)
- **融资余额占流通市值比例** (`financingBalanceToMarketCap`)
- **融券余额占流通市值比例** (`securitiesBalanceToMarketCap`)

**文档**: `lixinger-api-docs/docs/cn_index_margin-trading-and-securities-lending.md`

<!-- 搜索关键词: margin-trading-and-securities-lending date 融券余额占流通市值比例 financingBalanceToMarketCap 融资余额 数据时间 融资余额占流通市值比例 securitiesBalance 融券余额 融资融券 securitiesBalanceToMarketCap financingBalance -->

---

### 互联互通 | mutual-market

**API 路径**: `cn/index/mutual-market`

**说明**: 获取互联互通数据。

**返回字段**:

- **数据时间** (`date`)
- **持股金额** (`shareholdingsMoney`)
- **港资持仓金额占市值比例** (`shareholdingsMoneyToMarketCap`)

**文档**: `lixinger-api-docs/docs/cn_index_mutual-market.md`

<!-- 搜索关键词: date mutual-market 持股金额 数据时间 shareholdingsMoneyToMarketCap 互联互通 shareholdingsMoney 港资持仓金额占市值比例 -->

---

### 指数跟踪基金信息 | tracking-fund

**API 路径**: `cn/index/tracking-fund`

**说明**: 获取指数跟踪基金数据。

**返回字段**:

- **基金名称** (`name`)
- **基金代码** (`stockCode`)
- **简称** (`shortName`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **交易所** (`exchange`)

**文档**: `lixinger-api-docs/docs/cn_index_tracking-fund.md`

<!-- 搜索关键词: name market 基金代码 交易所 市场 指数跟踪基金信息 stockCode 基金名称 shortName exchange areaCode 地区代码 简称 tracking-fund -->

---

## A股行业

### 股票信息 | industry

**API 路径**: `cn/industry`

**说明**: 获取股票详细信息。

**返回字段**:

- **行业代码** (`stockCode`)
- **行业名称** (`name`)
- **发布时间** (`launchDate`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid** (`fsTableType`)
- **行业分类等级** (`level`)
- **行业来源 国证 :cni 申万 :sw 申万2021版 :sw_2021** (`source`)
- **货币** (`currency`)

**文档**: `lixinger-api-docs/docs/cn_industry.md`

<!-- 搜索关键词: name areaCode 行业名称 地区代码 财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid 股票信息 market currency 发布时间 市场 launchDate 行业代码 source level fsTableType 行业分类等级 stockCode 货币 行业来源 国证 :cni 申万 :sw 申万2021版 :sw_2021 industry -->

---

### 样本信息 | sw_2021

**API 路径**: `cn/industry/constituents/sw_2021`

**说明**: 获取样本信息。

**返回字段**:

- **指数代码** (`stockCode`)

**文档**: `lixinger-api-docs/docs/cn_industry_constituents_sw_2021.md`

<!-- 搜索关键词: 指数代码 stockCode 样本信息 sw_2021 -->

---

### 财报数据 | hybrid

**API 路径**: `cn/industry/fs/sw_2021/hybrid`

**说明**: 获取财务数据，如营业收入、ROE等。 说明: 指标计算请参考行业财务数据计算

**文档**: `lixinger-api-docs/docs/cn_industry_fs_sw_2021_hybrid.md`

<!-- 搜索关键词: 财报数据 hybrid -->

---

### 基本面数据 | sw_2021

**API 路径**: `cn/industry/fundamental/sw_2021`

**说明**: 获取基本面数据，如PE、PB等。 说明: 指标计算请参考行业估值计算

**文档**: `lixinger-api-docs/docs/cn_industry_fundamental_sw_2021.md`

<!-- 搜索关键词: 基本面数据 sw_2021 -->

---

### 互联互通 | sw_2021

**API 路径**: `cn/industry/hot/mm_ha/sw_2021`

**说明**: 获取互联互通数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **陆股通持仓金额** (`mm_sha`)
- **陆股通持仓金额占市值比例** (`mm_sha_mc_r`)
- **陆股通过去1个季度净买入金额** (`mm_sh_nba_q1`)
- **陆股通过去2个季度净买入金额** (`mm_sh_nba_q2`)
- **陆股通过去3个季度净买入金额** (`mm_sh_nba_q3`)
- **陆股通过去4个季度净买入金额** (`mm_sh_nba_q4`)
- **陆股通过去1个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q1`)
- **陆股通过去2个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q2`)
- **陆股通过去3个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q3`)
- **陆股通过去4个季度持股金额占市值变化比例** (`mm_sha_mc_rc_q4`)

**文档**: `lixinger-api-docs/docs/cn_industry_hot_mm_ha_sw_2021.md`

<!-- 搜索关键词: 陆股通过去3个季度净买入金额 陆股通过去2个季度持股金额占市值变化比例 mm_sha_mc_r 互联互通 陆股通过去1个季度持股金额占市值变化比例 mm_sha_mc_rc_q3 陆股通过去4个季度持股金额占市值变化比例 mm_sh_nba_q2 陆股通过去2个季度净买入金额 数据时间 sw_2021 mm_sha_mc_rc_q1 mm_sha_mc_rc_q2 mm_sh_nba_q3 mm_sha_mc_rc_q4 last_data_date 陆股通持仓金额占市值比例 陆股通持仓金额 mm_sh_nba_q4 陆股通过去1个季度净买入金额 mm_sha stockCode 陆股通过去3个季度持股金额占市值变化比例 股票代码 mm_sh_nba_q1 陆股通过去4个季度净买入金额 -->

---

### 融资融券 | sw_2021

**API 路径**: `cn/industry/margin-trading-and-securities-lending/sw_2021`

**说明**: 获取融资融券数据。

**返回字段**:

- **数据时间** (`date`)
- **融资余额** (`financingBalance`)
- **融券余额** (`securitiesBalance`)
- **融资余额占流通市值比例** (`financingBalanceToMarketCap`)
- **融券余额占流通市值比例** (`securitiesBalanceToMarketCap`)

**文档**: `lixinger-api-docs/docs/cn_industry_margin-trading-and-securities-lending_sw_2021.md`

<!-- 搜索关键词: date 融券余额占流通市值比例 financingBalanceToMarketCap 融资余额 数据时间 融资余额占流通市值比例 sw_2021 securitiesBalance 融券余额 融资融券 securitiesBalanceToMarketCap financingBalance -->

---

### 互联互通 | sw_2021

**API 路径**: `cn/industry/mutual-market/sw_2021`

**说明**: 获取互联互通数据。

**返回字段**:

- **数据时间** (`date`)
- **持股金额** (`shareholdingsMoney`)
- **港资持仓金额占市值比例** (`shareholdingsMoneyToMarketCap`)

**文档**: `lixinger-api-docs/docs/cn_industry_mutual-market_sw_2021.md`

<!-- 搜索关键词: date 持股金额 数据时间 shareholdingsMoneyToMarketCap 互联互通 shareholdingsMoney 港资持仓金额占市值比例 sw_2021 -->

---

## A股基金

### 基金公司信息 | fund-company

**API 路径**: `cn/fund-company`

**说明**: 获取基金公司详细信息。

**返回字段**:

- **基金公司名称** (`name`)
- **基金公司代码** (`stockCode`)
- **成立日期** (`inceptionDate`)
- **基金数量** (`fundsNum`)
- **总资产规模** (`assetScale`)
- **基金公司类型 基金公司 :fund_company 证券公司 :securities_company 证券公司资产管理子公司 :securities_company_amsc 保险资产管理公司 :insurance_am_company** (`fundCollectionType`)

**文档**: `lixinger-api-docs/docs/cn_fund-company.md`

<!-- 搜索关键词: name 基金公司类型 基金公司 :fund_company 证券公司 :securities_company 证券公司资产管理子公司 :securities_company_amsc 保险资产管理公司 :insurance_am_company 基金公司信息 总资产规模 assetScale 基金数量 stockCode inceptionDate fund-company 基金公司代码 基金公司名称 fundCollectionType 成立日期 fundsNum -->

---

### 资产规模 | asset-scale

**API 路径**: `cn/fund-company/asset-scale`

**说明**: 获取资产规模详细信息。

**返回字段**:

- **日期** (`date`)
- **股票型资产规模** (`equityAssetScale`)
- **混合型资产规模** (`hybridAssetScale`)
- **QDII型资产规模** (`qdiiAssetScale`)
- **债券型资产规模** (`bondAssetScale`)

**文档**: `lixinger-api-docs/docs/cn_fund-company_asset-scale.md`

<!-- 搜索关键词: date asset-scale 债券型资产规模 hybridAssetScale 资产规模 日期 混合型资产规模 qdiiAssetScale 股票型资产规模 QDII型资产规模 bondAssetScale equityAssetScale -->

---

### 基金列表 | fund-list

**API 路径**: `cn/fund-company/fund-list`

**说明**: 获取基金列表详细信息。

**返回字段**:

- **基金代码数组。** (`fundCodes`)

**文档**: `lixinger-api-docs/docs/cn_fund-company_fund-list.md`

<!-- 搜索关键词: fund-list 基金列表 fundCodes 基金代码数组。 -->

---

### 基金经理列表 | fund-manager-list

**API 路径**: `cn/fund-company/fund-manager-list`

**说明**: 获取基金经理列表详情。

**返回字段**:

- **基金经理代码数组** (`fundManagerCodes`)

**文档**: `lixinger-api-docs/docs/cn_fund-company_fund-manager-list.md`

<!-- 搜索关键词: 基金经理列表 fundManagerCodes fund-manager-list 基金经理代码数组 -->

---

### 基金公司资产规模 | fc_as

**API 路径**: `cn/fund-company/hot/fc_as`

**说明**: 获取基金公司资产规模数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **最新数据时间** (`fc_as_d`)
- **总资产规模** (`fc_as`)
- **非债券基金资产规模** (`fc_nb_as`)
- **混合型资产规模** (`fc_h_as`)
- **股票型资产规模** (`fc_e_as`)
- **QDII型资产规模** (`fc_q_as`)
- **债券型资产规模** (`fc_b_as`)

**文档**: `lixinger-api-docs/docs/cn_fund-company_hot_fc_as.md`

<!-- 搜索关键词: 基金公司资产规模 非债券基金资产规模 债券型资产规模 总资产规模 fc_nb_as stockCode fc_as_d 混合型资产规模 股票型资产规模 fc_e_as QDII型资产规模 最新数据时间 fc_b_as 股票代码 fc_as fc_h_as fc_q_as -->

---

### 持股 | shareholdings

**API 路径**: `cn/fund-company/shareholdings`

**说明**: 获取持仓详细信息。

**返回字段**:

- **日期** (`date`)
- **持仓股数** (`holdings`)
- **持仓市值** (`marketCap`)
- **股票代码** (`stockCode`)

**文档**: `lixinger-api-docs/docs/cn_fund-company_shareholdings.md`

<!-- 搜索关键词: 持仓股数 date shareholdings marketCap 日期 stockCode 持仓市值 持股 holdings 股票代码 -->

---

### 基金经理信息 | fund-manager

**API 路径**: `cn/fund-manager`

**说明**: 获取基金经理详细信息。

**返回字段**:

- **基金经理姓名** (`name`)
- **出生年份** (`birthYear`)
- **履历** (`resume`)
- **基金经理代码** (`stockCode`)
- **性别** (`gender`)

**文档**: `lixinger-api-docs/docs/cn_fund-manager.md`

<!-- 搜索关键词: name resume 性别 birthYear 基金经理信息 stockCode 履历 基金经理代码 gender 基金经理姓名 出生年份 fund-manager -->

---

### 基金经理收益率 | fmp

**API 路径**: `cn/fund-manager/hot/fmp`

**说明**: 获取基金经理收益率数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **最新收益率时间** (`fm_p_r_d`)
- **今年以来收益率** (`fm_p_r_fys`)
- **一个月收益率** (`fm_p_r_m1`)
- **三个月收益率** (`fm_p_r_m3`)
- **六个月收益率** (`fm_p_r_m6`)
- **一年收益率** (`fm_p_r_y1`)
- **三年收益率** (`fm_p_r_y3`)
- **五年收益率** (`fm_p_r_y5`)
- **十年收益率** (`fm_p_r_y10`)
- **管理基金以来年化收益率** (`fm_cagr_p_r_fs`)
- **相同基金经理类型今年以来收益率排名** (`fm_p_r_fys_rp`)
- **相同基金经理类型一个月收益率排名** (`fm_p_r_m1_rp`)
- **相同基金经理类型三个月收益率排名** (`fm_p_r_m3_rp`)
- **相同基金经理类型六个月收益率排名** (`fm_p_r_m6_rp`)
- **相同基金经理类型一年收益率排名** (`fm_p_r_y1_rp`)
- **相同基金经理类型三年收益率排名** (`fm_p_r_y3_rp`)
- **相同基金经理类型五年收益率排名** (`fm_p_r_y5_rp`)
- **相同基金经理类型十年收益率排名** (`fm_p_r_y10_rp`)
- **相同基金经理类型管理基金以来年化收益率排名** (`fm_cagr_p_r_fs_rp`)

**文档**: `lixinger-api-docs/docs/cn_fund-manager_hot_fmp.md`

<!-- 搜索关键词: fm_p_r_y10 fm_p_r_fys_rp fm_p_r_m6 最新收益率时间 相同基金经理类型六个月收益率排名 fm_p_r_y1_rp fm_p_r_y3_rp fm_p_r_y10_rp 相同基金经理类型管理基金以来年化收益率排名 fm_p_r_fys fm_p_r_m6_rp 今年以来收益率 相同基金经理类型三个月收益率排名 fm_p_r_y1 一年收益率 相同基金经理类型今年以来收益率排名 fmp 管理基金以来年化收益率 fm_cagr_p_r_fs fm_p_r_y5 六个月收益率 相同基金经理类型一个月收益率排名 基金经理收益率 相同基金经理类型三年收益率排名 相同基金经理类型五年收益率排名 fm_p_r_y3 fm_p_r_m3_rp 三个月收益率 相同基金经理类型十年收益率排名 fm_cagr_p_r_fs_rp fm_p_r_m3 一个月收益率 fm_p_r_m1 十年收益率 fm_p_r_m1_rp stockCode 相同基金经理类型一年收益率排名 五年收益率 股票代码 fm_p_r_y5_rp fm_p_r_d 三年收益率 -->

---

### 管理的基金信息 | management-funds

**API 路径**: `cn/fund-manager/management-funds`

**说明**: 获取管理的基金详细信息。

**返回字段**:

- **基金数组。 子字段: 基金名称: name: (String) 基金代码: code: (String) 任职日期: appointmentDate: (Date) 离任日期: departureDate: (Date)** (`funds`)

**文档**: `lixinger-api-docs/docs/cn_fund-manager_management-funds.md`

<!-- 搜索关键词: funds 基金数组。 子字段: 基金名称: name: (String) 基金代码: code: (String) 任职日期: appointmentDate: (Date) 离任日期: departureDate: (Date) management-funds 管理的基金信息 -->

---

### 利润率 | profit-ratio

**API 路径**: `cn/fund-manager/profit-ratio`

**说明**: 获取利润率信息。

**返回字段**:

- **公告日期** (`date`)
- **计算起始日期** (`startDate`)
- **数额** (`value`)

**文档**: `lixinger-api-docs/docs/cn_fund-manager_profit-ratio.md`

<!-- 搜索关键词: date startDate profit-ratio 利润率 公告日期 数额 计算起始日期 value -->

---

### 基金经理持仓 | shareholdings

**API 路径**: `cn/fund-manager/shareholdings`

**说明**: 获取基金经理持仓信息。

**返回字段**:

- **公告日期** (`date`)
- **市值** (`marketCap`)
- **持仓** (`holdings`)
- **持股占流通股比例** (`holdingsToCcRatio`)
- **股票代码** (`stockCode`)

**文档**: `lixinger-api-docs/docs/cn_fund-manager_shareholdings.md`

<!-- 搜索关键词: date shareholdings marketCap 公告日期 holdingsToCcRatio stockCode 持股占流通股比例 持仓 基金经理持仓 holdings 股票代码 市值 -->

---

### 基金信息 | fund

**API 路径**: `cn/fund`

**说明**: 获取基金详细信息。 说明: 场内基金的exchange是 sz 或 sh。

**返回字段**:

- **基金总数** (`total`)
- **基金名称** (`name`)
- **基金代码** (`stockCode`)
- **基金一级类型，目前只有商品基金有这个类型。 互认基金 :mutual_recognition** (`fundFirstLevel`)
- **基金类型 股票型 :company 混合型 :hybrid 债券型 :bond QDII :QDII REIT :reit FOF :fof 商品基金 :commodity** (`fundSecondLevel`)
- **简称** (`shortName`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **交易所** (`exchange`)
- **合同生效日** (`inceptionDate`)
- **退市时间** (`delistedDate`)

**文档**: `lixinger-api-docs/docs/cn_fund.md`

<!-- 搜索关键词: name 基金代码 基金名称 fundSecondLevel exchange areaCode 地区代码 简称 market 退市时间 市场 基金信息 fund 基金类型 股票型 :company 混合型 :hybrid 债券型 :bond QDII :QDII REIT :reit FOF :fof 商品基金 :commodity delistedDate inceptionDate shortName 基金一级类型，目前只有商品基金有这个类型。 互认基金 :mutual_recognition 基金总数 total 交易所 stockCode 合同生效日 fundFirstLevel -->

---

### 公告 | announcement

**API 路径**: `cn/fund/announcement`

**说明**: 获取公告信息。

**返回字段**:

- **公告日期** (`date`)
- **语言** (`lang`)
- **链接文本** (`linkText`)
- **链接地址** (`linkUrl`)
- **链接类型** (`linkType`)
- **种类 全部 :all 财务报表 :fs 招募设立 :s_u 分红 :dividend 拆分折算 :split 其它 :other** (`types`)

**文档**: `lixinger-api-docs/docs/cn_fund_announcement.md`

<!-- 搜索关键词: 链接类型 date 种类 全部 :all 财务报表 :fs 招募设立 :s_u 分红 :dividend 拆分折算 :split 其它 :other 公告日期 lang 语言 announcement 链接文本 链接地址 types 公告 linkUrl linkType linkText -->

---

### 资产组合 | asset-combination

**API 路径**: `cn/fund/asset-combination`

**说明**: 获取资产组合信息 说明: 主基金代码和子基金代码获取相同的数据。

**返回字段**:

- **财报日期** (`date`)
- **资产组合 子字段: 权益类投资: ei: (Number) (其中)股票: ei_c: (Number) (其中)优先股: ei_ps: (Number) (其中)存托凭证: ei_dr: (Number) (其中)房地产信托: ei_ret: (Number) 权益类投资占比: ei_r: (Number) 基金投资: fi: (Number) 基金投资占比: fi_r: (Number) 固定收益投资: fii: (Number) (其中)债券: fii_b: (Number) (其中)资产支持证券: fii_abs: (Number) 固定收益投资占比: fii_r: (Number) 贵金属投资: pmi: (Number) 贵金属投资占比: pmi_r: (Number) 金融衍生品投资: fdi: (Number) (其中)远期: fdi_fd: (Number) (其中)期货: fdi_fs: (Number) (其中)期权: fdi_o: (Number) (其中)权证: fdi_W: (Number) 金融衍生品投资占比: fdi_r: (Number) 返售型金融资产: rfa: (Number) (其中)买断式: rfa_br: (Number) 返售型金融资产占比: rfa_r: (Number) 银行存款及结算备付金: bs_a_sr: (Number) 银行存款及结算备付金占比: bs_a_sr_r: (Number) 货币市场工具: mmt: (Number) 货币市场工具占比: mmt_r: (Number) 其他资产: oa: (Number) 其他资产占比: oa_r: (Number)** (`ac`)

**文档**: `lixinger-api-docs/docs/cn_fund_asset-combination.md`

<!-- 搜索关键词: date asset-combination 资产组合 子字段: 权益类投资: ei: (Number) (其中)股票: ei_c: (Number) (其中)优先股: ei_ps: (Number) (其中)存托凭证: ei_dr: (Number) (其中)房地产信托: ei_ret: (Number) 权益类投资占比: ei_r: (Number) 基金投资: fi: (Number) 基金投资占比: fi_r: (Number) 固定收益投资: fii: (Number) (其中)债券: fii_b: (Number) (其中)资产支持证券: fii_abs: (Number) 固定收益投资占比: fii_r: (Number) 贵金属投资: pmi: (Number) 贵金属投资占比: pmi_r: (Number) 金融衍生品投资: fdi: (Number) (其中)远期: fdi_fd: (Number) (其中)期货: fdi_fs: (Number) (其中)期权: fdi_o: (Number) (其中)权证: fdi_W: (Number) 金融衍生品投资占比: fdi_r: (Number) 返售型金融资产: rfa: (Number) (其中)买断式: rfa_br: (Number) 返售型金融资产占比: rfa_r: (Number) 银行存款及结算备付金: bs_a_sr: (Number) 银行存款及结算备付金占比: bs_a_sr_r: (Number) 货币市场工具: mmt: (Number) 货币市场工具占比: mmt_r: (Number) 其他资产: oa: (Number) 其他资产占比: oa_r: (Number) ac 财报日期 资产组合 -->

---

### 按行业分类的股票投资组合 | asset-industry-combination

**API 路径**: `cn/fund/asset-industry-combination`

**说明**: 获取按行业分类的股票投资组合的数据。 说明: 主基金代码和子基金代码获取相同的数据。

**返回字段**:

- **财报日期** (`date`)
- **按行业分类的股票投资组合 子字段: 行业名称: name: (String) 公允价值: value: (Number) 比例: proportion: (Number)** (`aic_cn`)

**文档**: `lixinger-api-docs/docs/cn_fund_asset-industry-combination.md`

<!-- 搜索关键词: date asset-industry-combination 财报日期 按行业分类的股票投资组合 按行业分类的股票投资组合 子字段: 行业名称: name: (String) 公允价值: value: (Number) 比例: proportion: (Number) aic_cn -->

---

### K线数据 | candlestick

**API 路径**: `cn/fund/candlestick`

**说明**: 获取K线数据。

**返回字段**:

- **数据时间** (`date`)
- **开盘价** (`open`)
- **收盘价** (`close`)
- **最高价** (`high`)
- **最低价** (`low`)
- **成交量** (`volume`)
- **金额** (`amount`)
- **涨跌幅** (`change`)
- **复权因子** (`complexFactor`)

**文档**: `lixinger-api-docs/docs/cn_fund_candlestick.md`

<!-- 搜索关键词: volume 复权因子 amount high change close 开盘价 数据时间 K线数据 涨跌幅 candlestick open date 最高价 最低价 complexFactor 金额 low 成交量 收盘价 -->

---

### 分红 | dividend

**API 路径**: `cn/fund/dividend`

**说明**: 获取分红信息。

**返回字段**:

- **股权登记日** (`date`)
- **除权除息日** (`exDate`)
- **分红金额(每份)** (`dividend`)

**文档**: `lixinger-api-docs/docs/cn_fund_dividend.md`

<!-- 搜索关键词: dividend exDate date 股权登记日 除权除息日 分红 分红金额(每份) -->

---

### 基金回撤 | drawdown

**API 路径**: `cn/fund/drawdown`

**说明**: 获取基金回撤数据。

**返回字段**:

- **数据时间** (`date`)
- **回撤** (`value`)

**文档**: `lixinger-api-docs/docs/cn_fund_drawdown.md`

<!-- 搜索关键词: date 回撤 数据时间 基金回撤 drawdown value -->

---

### 场内基金收盘价 | exchange-traded-close-price

**API 路径**: `cn/fund/exchange-traded-close-price`

**说明**: 场内基金收盘价数据。

**返回字段**:

- **数据时间** (`date`)
- **开盘价** (`open`)
- **收盘价** (`close`)
- **最低价** (`low`)
- **最高价** (`high`)

**文档**: `lixinger-api-docs/docs/cn_fund_exchange-traded-close-price.md`

<!-- 搜索关键词: date close 开盘价 数据时间 exchange-traded-close-price low 最低价 最高价 场内基金收盘价 open 收盘价 high -->

---

### 费用 | fees

**API 路径**: `cn/fund/fees`

**说明**: 获取费用API

**返回字段**:

- **公告日期** (`date`)
- **管理报酬费用率** (`m_f_r`)
- **管理报酬** (`m_f`)
- **托管费用率** (`c_f_r`)
- **托管费用** (`c_f`)

**文档**: `lixinger-api-docs/docs/cn_fund_fees.md`

<!-- 搜索关键词: c_f date fees 公告日期 管理报酬费用率 托管费用 托管费用率 管理报酬 m_f_r m_f 费用 c_f_r -->

---

### 最新收盘价溢价率信息 | f_nlacan

**API 路径**: `cn/fund/hot/f_nlacan`

**说明**: 获取最新收盘价溢价率信息数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **价格时间** (`f_c_d`)
- **收盘价格** (`f_c_c`)
- **收盘价涨跌幅** (`f_c_cr`)
- **成交金额** (`f_c_a`)
- **净值估算日期** (`f_nv_eicpd`)
- **净值估算前值** (`f_nv_esnv`)
- **净值估算前值时间** (`f_nv_esvd`)
- **净值估算对应的指数涨跌幅** (`f_nv_eicpcr`)
- **净值估算值** (`f_nv_env`)
- **净值日期** (`f_nv_d`)
- **基金净值** (`f_nv`)
- **净值涨跌幅** (`f_nv_cr`)
- **收盘价溢价率** (`f_pnv_pr`)
- **最近5个交易日平均溢价率** (`f_pnv_pr_avg_d5`)
- **最近10个交易日平均溢价率** (`f_pnv_pr_avg_d10`)
- **最近20个交易日平均溢价率** (`f_pnv_pr_avg_d20`)

**文档**: `lixinger-api-docs/docs/cn_fund_hot_f_nlacan.md`

<!-- 搜索关键词: f_nv_eicpcr 基金净值 f_pnv_pr_avg_d10 f_c_a f_nv_esvd 净值估算值 f_pnv_pr 净值估算对应的指数涨跌幅 f_pnv_pr_avg_d5 最近20个交易日平均溢价率 f_nv_d f_nlacan 最新收盘价溢价率信息 f_nv 净值估算前值 成交金额 净值估算日期 净值日期 收盘价溢价率 收盘价格 最近5个交易日平均溢价率 f_c_c f_nv_esnv 净值涨跌幅 f_nv_eicpd 价格时间 f_pnv_pr_avg_d20 净值估算前值时间 stockCode f_c_cr f_nv_cr 收盘价涨跌幅 f_nv_env 股票代码 f_c_d 最近10个交易日平均溢价率 -->

---

### 基金经理 | manager

**API 路径**: `cn/fund/manager`

**说明**: 获取该基金历史上所有的基金经理任职信息。 说明: 主基金代码和子基金代码获取相同的数据。

**返回字段**:

- **基金代码** (`stockCode`)
- **基金经理数组。 子字段: 基金经理姓名: name: (String) 基金经理代码: managerCode: (String) 任职日期: appointmentDate: (Date) 离任日期: departureDate: (Date)** (`managers`)

**文档**: `lixinger-api-docs/docs/cn_fund_manager.md`

<!-- 搜索关键词: 基金经理 基金代码 基金经理数组。 子字段: 基金经理姓名: name: (String) 基金经理代码: managerCode: (String) 任职日期: appointmentDate: (Date) 离任日期: departureDate: (Date) stockCode manager managers -->

---

### 理杏仁分红再投入净值 | net-value-of-dividend-reinvestment

**API 路径**: `cn/fund/net-value-of-dividend-reinvestment`

**说明**: 获取理杏仁分红再投入净值数据。

**返回字段**:

- **数据时间** (`date`)
- **理杏仁分红再投入净值** (`netValue`)

**文档**: `lixinger-api-docs/docs/cn_fund_net-value-of-dividend-reinvestment.md`

<!-- 搜索关键词: net-value-of-dividend-reinvestment netValue date 数据时间 理杏仁分红再投入净值 -->

---

### 净值 | net-value

**API 路径**: `cn/fund/net-value`

**说明**: 获取净值数据。

**返回字段**:

- **数据时间** (`date`)
- **净值** (`netValue`)

**文档**: `lixinger-api-docs/docs/cn_fund_net-value.md`

<!-- 搜索关键词: 净值 date netValue 数据时间 net-value -->

---

### 基金概况 | profile

**API 路径**: `cn/fund/profile`

**说明**: 获取基金概况数据。比如，投资目标、投资策略、子基金等。 说明: 主基金代码和子基金代码获取相同的数据。

**返回字段**:

- **财报日期** (`date`)
- **基金托管人** (`c_name`)
- **场内简称** (`e_t_short_name`)
- **基金公司** (`f_c_name`)
- **合同生效日** (`inception_date`)
- **运作方式** (`op_mode`)
- **基金主代码** (`m_stock_code`)
- **投资目标** (`investment_o`)
- **投资策略** (`investment_s`)
- **业绩比较基准** (`p_c_benchmark`)
- **风险收益特征** (`risk_r_c`)
- **上市日期** (`ipo_date`)
- **子基金代码** (`s_f_stock_codes`)
- **联接基金** (`feeder_funds`)

**文档**: `lixinger-api-docs/docs/cn_fund_profile.md`

<!-- 搜索关键词: inception_date 基金托管人 profile 风险收益特征 risk_r_c s_f_stock_codes 子基金代码 investment_s op_mode c_name 场内简称 投资目标 基金公司 上市日期 e_t_short_name 业绩比较基准 date 投资策略 investment_o 联接基金 基金概况 运作方式 ipo_date f_c_name m_stock_code p_c_benchmark feeder_funds 财报日期 合同生效日 基金主代码 -->

---

### 持有人结构 | shareholders-structure

**API 路径**: `cn/fund/shareholders-structure`

**说明**: 获取基金持有人结构数据。

**返回字段**:

- **数据时间** (`date`)
- **持有人户数** (`h_a`)
- **持有人平均份额** (`h_s_a`)
- **机构持有份额** (`ins_h_s`)
- **机构投资占比** (`ins_h_s_r`)
- **个人持有份额** (`ind_h_s`)
- **个人持有份额占比** (`ind_h_s_r`)
- **联接基金份额** (`f_f_s`)
- **联接基金份额占比** (`f_f_s_r`)

**文档**: `lixinger-api-docs/docs/cn_fund_shareholders-structure.md`

<!-- 搜索关键词: 机构持有份额 ind_h_s ind_h_s_r f_f_s 持有人户数 个人持有份额占比 联接基金份额 数据时间 持有人平均份额 持有人结构 机构投资占比 ins_h_s shareholders-structure 个人持有份额 f_f_s_r date h_s_a 联接基金份额占比 ins_h_s_r h_a -->

---

### 基金持仓 | shareholdings

**API 路径**: `cn/fund/shareholdings`

**说明**: 获取基金持仓数据。 说明: 主基金代码和子基金代码获取相同的数据。

**返回字段**:

- **持仓股票代码** (`stockCode`)
- **股票地区代码** (`stockAreaCode`)
- **持股数量** (`holdings`)
- **持仓市值** (`marketCap`)
- **持仓占比** (`netValueRatio`)

**文档**: `lixinger-api-docs/docs/cn_fund_shareholdings.md`

<!-- 搜索关键词: marketCap shareholdings 持股数量 基金持仓 持仓占比 股票地区代码 stockCode stockAreaCode 持仓市值 holdings netValueRatio 持仓股票代码 -->

---

### 基金份额 | shares

**API 路径**: `cn/fund/shares`

**说明**: 获取基金份额及规模数据。 说明: LOF基金和一些封闭式基金有场内份额和场外份额。

**返回字段**:

- **数据时间** (`date`)
- **基金份额** (`s`)
- **基金规模** (`as`)
- **场内基金份额** (`et_shares`)
- **场内基金规模** (`et_as`)

**文档**: `lixinger-api-docs/docs/cn_fund_shares.md`

<!-- 搜索关键词: 场内基金规模 as date et_shares 数据时间 场内基金份额 基金规模 et_as s shares 基金份额 -->

---

### 拆分 | split

**API 路径**: `cn/fund/split`

**说明**: 获取拆分数据。

**返回字段**:

- **拆分折算日** (`date`)
- **拆分折算比例** (`splitRatio`)

**文档**: `lixinger-api-docs/docs/cn_fund_split.md`

<!-- 搜索关键词: date 拆分折算比例 split splitRatio 拆分折算日 拆分 -->

---

### 基金累积净值 | total-net-value

**API 路径**: `cn/fund/total-net-value`

**说明**: 获取基金累计净值数据。

**返回字段**:

- **数据时间** (`date`)
- **基金累积净值** (`totalNetValue`)

**文档**: `lixinger-api-docs/docs/cn_fund_total-net-value.md`

<!-- 搜索关键词: totalNetValue date 数据时间 total-net-value 基金累积净值 -->

---

### 换手率 | turnover-rate

**API 路径**: `cn/fund/turnover-rate`

**说明**: 获取换手率信息。

**返回字段**:

- **数据时间** (`date`)
- **数额** (`value`)

**文档**: `lixinger-api-docs/docs/cn_fund_turnover-rate.md`

<!-- 搜索关键词: date 数据时间 数额 value turnover-rate 换手率 -->

---

## 港股公司

### 股票信息 | company

**API 路径**: `hk/company`

**说明**: 获取股票详细信息。

**返回字段**:

- **公司总数** (`total`)
- **公司名称** (`name`)
- **股票代码** (`stockCode`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **交易所** (`exchange`)
- **财报类型** (`fsTableType`)
- **互联互通** (`mutualMarkets`)
- **是否是互联互通标的** (`mutualMarketFlag`)
- **上市时间** (`ipoDate`)
- **退市时间** (`delistedDate`)
- **每手股数** (`sharesPerLot`)
- **AH同时上市公司对应的A股代码** (`stockCodeA`)

**文档**: `lixinger-api-docs/docs/hk_company.md`

<!-- 搜索关键词: name mutualMarketFlag exchange 公司总数 areaCode AH同时上市公司对应的A股代码 互联互通 地区代码 上市时间 sharesPerLot 财报类型 股票信息 market 退市时间 市场 mutualMarkets stockCodeA 每手股数 delistedDate fsTableType total company 公司名称 交易所 stockCode 是否是互联互通标的 ipoDate 股票代码 -->

---

### 配股 | allotment

**API 路径**: `hk/company/allotment`

**说明**: 获取配股信息。

**返回字段**:

- **公告日期** (`date`)
- **除权除息日** (`exDate`)
- **货币** (`currency`)
- **配股比例** (`allotmentRatio`)
- **配股价格** (`allotmentPrice`)
- **实际配股数量** (`allotmentShares`)

**文档**: `lixinger-api-docs/docs/hk_company_allotment.md`

<!-- 搜索关键词: allotmentPrice exDate date currency 公告日期 配股 配股比例 allotmentShares 除权除息日 配股价格 实际配股数量 allotmentRatio 货币 allotment -->

---

### 公告 | announcement

**API 路径**: `hk/company/announcement`

**说明**: 获取公告信息。

**返回字段**:

- **公告日期** (`date`)
- **链接文本** (`linkText`)
- **链接地址** (`linkUrl`)
- **链接类型** (`linkType`)
- **种类 全部 :all 财务报表 :fs 配售 :spo 供股 :sa 回购 :srp 会议及表决 :m_a_v 翌日披露报表—其他 :ndd_r 月报表 :mr IPO :ipo** (`types`)

**文档**: `lixinger-api-docs/docs/hk_company_announcement.md`

<!-- 搜索关键词: 种类 全部 :all 财务报表 :fs 配售 :spo 供股 :sa 回购 :srp 会议及表决 :m_a_v 翌日披露报表—其他 :ndd_r 月报表 :mr IPO :ipo 链接类型 date 公告日期 链接文本 链接地址 announcement types 公告 linkUrl linkType linkText -->

---

### K线数据 | candlestick

**API 路径**: `hk/company/candlestick`

**说明**: 获取K线数据。 说明: 复权计算仅对所选时间段的价格进行复权 成交量不进行复权计算

**返回字段**:

- **数据时间** (`date`)
- **股票代码** (`stockCode`)
- **开盘价** (`open`)
- **收盘价** (`close`)
- **最高价** (`high`)
- **最低价** (`low`)
- **成交量** (`volume`)
- **金额** (`amount`)
- **涨跌幅** (`change`)
- **换手率** (`to_r`)

**文档**: `lixinger-api-docs/docs/hk_company_candlestick.md`

<!-- 搜索关键词: volume amount high change close 开盘价 数据时间 K线数据 涨跌幅 candlestick 换手率 open date 最高价 最低价 stockCode 金额 low to_r 股票代码 成交量 收盘价 -->

---

### 分红 | dividend

**API 路径**: `hk/company/dividend`

**说明**: 获取分红信息。

**返回字段**:

- **公告日期** (`date`)
- **内容** (`content`)
- **送股(股)** (`bonusSharesFromProfit`)
- **转增(股)** (`bonusSharesFromCapitalReserve`)
- **分红** (`dividend`)
- **货币** (`currency`)
- **分红金额（港币）** (`dividendAmount`)
- **年度净利润（港币）** (`annualNetProfit`)
- **年度净利润分红比例** (`annualNetProfitDividendRatio`)
- **股权登记日** (`registerDate`)
- **除权除息日** (`exDate`)
- **分红到账日** (`paymentDate`)
- **财报时间** (`fsEndDate`)

**文档**: `lixinger-api-docs/docs/hk_company_dividend.md`

<!-- 搜索关键词: exDate bonusSharesFromProfit annualNetProfit 股权登记日 currency annualNetProfitDividendRatio content 分红 分红到账日 dividendAmount 年度净利润分红比例 dividend 送股(股) date paymentDate 分红金额（港币） 转增(股) 财报时间 内容 registerDate 公告日期 bonusSharesFromCapitalReserve 年度净利润（港币） 除权除息日 fsEndDate 货币 -->

---

### 员工信息 | employee

**API 路径**: `hk/company/employee`

**说明**: 获取员工数据。

**返回字段**:

- **公告日期** (`date`)
- **数据列表 子字段: 项目名称: itemName: (String) 父项名称: parentItemName: (String) 数据显示类型: displayType: (String) 数额: value: (Number)** (`dataList`)

**文档**: `lixinger-api-docs/docs/hk_company_employee.md`

<!-- 搜索关键词: date 公告日期 员工信息 数据列表 子字段: 项目名称: itemName: (String) 父项名称: parentItemName: (String) 数据显示类型: displayType: (String) 数额: value: (Number) employee dataList -->

---

### 股本变动 | equity-change

**API 路径**: `hk/company/equity-change`

**说明**: 获取股本变动数据。

**返回字段**:

- **变动日期** (`date`)
- **总股本** (`capitalization`)
- **H股股本** (`capitalizationH`)

**文档**: `lixinger-api-docs/docs/hk_company_equity-change.md`

<!-- 搜索关键词: date 总股本 H股股本 股本变动 变动日期 capitalizationH equity-change capitalization -->

---

### 财报数据 | non_financial

**API 路径**: `hk/company/fs/non_financial`

**说明**: 获取财务数据，如营业收入、ROE等。

**返回字段**:

- **财报日期** (`date`)
- **公告时间** (`reportDate`)
- **标准财年时间（不同公司的财年不一样，有的年报12月结束，有的却是3月结束，还有的7月结束。例如2017-01-01到2017-06-30结束的年报，调整到2016-Q4，其余的季报和中报都相应的做类似调整。调整后具有通用性。）** (`standardDate`)
- **股票代码** (`stockCode`)
- **财报类型** (`reportType`)
- **货币类型** (`currency`)
- **审计意见 无保留意见 :unqualified_opinion 保留意见 :qualified_opinion 保留意见与解释性说明 :qualified_opinion_with_explanatory_notes 否定意见 :adverse_opinion 拒绝表示意见 :disclaimer_of_opinion 解释性说明 :explanatory_statement 无法表示意见 :unable_to_express_an_opinion 带强调事项段的无保留意见 :unqualified_opinion_with_highlighted_matter_paragraph** (`auditOpinionType`)

**文档**: `lixinger-api-docs/docs/hk_company_fs_non_financial.md`

<!-- 搜索关键词: 财报类型 财报数据 date non_financial 审计意见 无保留意见 :unqualified_opinion 保留意见 :qualified_opinion 保留意见与解释性说明 :qualified_opinion_with_explanatory_notes 否定意见 :adverse_opinion 拒绝表示意见 :disclaimer_of_opinion 解释性说明 :explanatory_statement 无法表示意见 :unable_to_express_an_opinion 带强调事项段的无保留意见 :unqualified_opinion_with_highlighted_matter_paragraph currency auditOpinionType 公告时间 standardDate 标准财年时间（不同公司的财年不一样，有的年报12月结束，有的却是3月结束，还有的7月结束。例如2017-01-01到2017-06-30结束的年报，调整到2016-Q4，其余的季报和中报都相应的做类似调整。调整后具有通用性。） stockCode 货币类型 财报日期 reportDate reportType 股票代码 -->

---

### 内资基金公司持股 | fund-collection-shareholders

**API 路径**: `hk/company/fund-collection-shareholders`

**说明**: 获取内资基金公司持股信息。

**返回字段**:

- **数据时间** (`date`)
- **市值** (`marketCap`)
- **姓名** (`name`)
- **持仓** (`holdings`)
- **基金公司代码** (`fundCollectionCode`)

**文档**: `lixinger-api-docs/docs/hk_company_fund-collection-shareholders.md`

<!-- 搜索关键词: name date marketCap 数据时间 fund-collection-shareholders 基金公司代码 持仓 fundCollectionCode holdings 内资基金公司持股 市值 姓名 -->

---

### 内资基金持股 | fund-shareholders

**API 路径**: `hk/company/fund-shareholders`

**说明**: 获取内资基金持股信息。

**返回字段**:

- **数据时间** (`date`)
- **基金代码** (`fundCode`)
- **市值** (`marketCap`)
- **当前股票所在基金持仓排名** (`marketCapRank`)
- **持仓** (`holdings`)
- **基金持仓占基金规模比例** (`netValueRatio`)

**文档**: `lixinger-api-docs/docs/hk_company_fund-shareholders.md`

<!-- 搜索关键词: marketCapRank date 内资基金持股 marketCap 基金代码 fundCode 数据时间 当前股票所在基金持仓排名 持仓 holdings netValueRatio 基金持仓占基金规模比例 市值 fund-shareholders -->

---

### 基本面数据 | non_financial

**API 路径**: `hk/company/fundamental/non_financial`

**说明**: 获取基本面数据，如PE、PB等。

**文档**: `lixinger-api-docs/docs/hk_company_fundamental_non_financial.md`

<!-- 搜索关键词: 基本面数据 non_financial -->

---

### 分红再投入收益率 | tr_dri

**API 路径**: `hk/company/hot/tr_dri`

**说明**: 获取分红再投入收益率数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **指定时间段投资收益率** (`p_r`)
- **今年以来投资收益率** (`cagr_p_r_fys`)
- **近7日投资收益率** (`cagr_p_r_d7`)
- **近14日投资收益率** (`cagr_p_r_d14`)
- **近30日投资收益率** (`cagr_p_r_d30`)
- **近60日投资收益率** (`cagr_p_r_d60`)
- **近90日投资收益率** (`cagr_p_r_d90`)
- **近一年投资收益率** (`cagr_p_r_y1`)
- **近三年年化投资收益率** (`cagr_p_r_y3`)
- **近五年年化投资收益率** (`cagr_p_r_y5`)
- **近十年年化投资收益率** (`cagr_p_r_y10`)
- **上市至今年化投资收益率** (`cagr_p_r_fs`)
- **投资收益率计算起始日期** (`period_date`)

**文档**: `lixinger-api-docs/docs/hk_company_hot_tr_dri.md`

<!-- 搜索关键词: cagr_p_r_d7 cagr_p_r_d30 p_r cagr_p_r_y1 股票代码 今年以来投资收益率 近90日投资收益率 数据时间 cagr_p_r_d14 cagr_p_r_d90 近30日投资收益率 分红再投入收益率 近60日投资收益率 cagr_p_r_fs 近7日投资收益率 投资收益率计算起始日期 cagr_p_r_fys 近五年年化投资收益率 上市至今年化投资收益率 近一年投资收益率 last_data_date tr_dri 近三年年化投资收益率 cagr_p_r_d60 stockCode 近十年年化投资收益率 period_date 近14日投资收益率 指定时间段投资收益率 cagr_p_r_y5 cagr_p_r_y3 cagr_p_r_y10 -->

---

### 股票所属指数信息 | indices

**API 路径**: `hk/company/indices`

**说明**: 获取股票所属指数信息。

**返回字段**:

- **指数名称** (`name`)
- **地区代码** (`areaCode`)
- **指数代码** (`stockCode`)
- **指数来源 中证 :csi 国证 :cni 恒生 :hsi 美指 :usi 理杏仁 :lxri** (`source`)

**文档**: `lixinger-api-docs/docs/hk_company_indices.md`

<!-- 搜索关键词: name indices 指数名称 指数来源 中证 :csi 国证 :cni 恒生 :hsi 美指 :usi 理杏仁 :lxri source stockCode areaCode 股票所属指数信息 地区代码 指数代码 -->

---

### 股票所属行业信息 | industries

**API 路径**: `hk/company/industries`

**说明**: 获取股票所属行业信息。

**返回字段**:

- **行业名称** (`name`)
- **地区代码** (`areaCode`)
- **行业代码** (`stockCode`)
- **行业来源 申万 :sw 申万2021版 :sw_2021 国证 :cni** (`source`)

**文档**: `lixinger-api-docs/docs/hk_company_industries.md`

<!-- 搜索关键词: name industries 行业代码 source 股票所属行业信息 stockCode areaCode 行业来源 申万 :sw 申万2021版 :sw_2021 国证 :cni 行业名称 地区代码 -->

---

### 最新股东 | latest-shareholders

**API 路径**: `hk/company/latest-shareholders`

**说明**: 获取最新股东数据。

**返回字段**:

- **最后申报有关通知之日期** (`date`)
- **姓名** (`name`)
- **持有权益的股份数目 子字段: 数额: value: (Number) 股份类型: sharesType: (String)** (`numOfSharesInterestedList`)
- **占已发行的有投票权股份百分比 子字段: 数额: value: (Number) 股份类型: sharesType: (String)** (`percentageOfIssuedVotingShares`)

**文档**: `lixinger-api-docs/docs/hk_company_latest-shareholders.md`

<!-- 搜索关键词: name date percentageOfIssuedVotingShares numOfSharesInterestedList 持有权益的股份数目 子字段: 数额: value: (Number) 股份类型: sharesType: (String) 占已发行的有投票权股份百分比 子字段: 数额: value: (Number) 股份类型: sharesType: (String) 最后申报有关通知之日期 最新股东 latest-shareholders 姓名 -->

---

### 互联互通 | mutual-market

**API 路径**: `hk/company/mutual-market`

**说明**: 获取互联互通数据。

**返回字段**:

- **持股数量** (`shareholdings`)

**文档**: `lixinger-api-docs/docs/hk_company_mutual-market.md`

<!-- 搜索关键词: shareholdings 持股数量 互联互通 mutual-market -->

---

### 营收构成 | operation-revenue-constitution

**API 路径**: `hk/company/operation-revenue-constitution`

**说明**: 获取营收构成数据。

**返回字段**:

- **数据时间** (`date`)
- **公告日期** (`declarationDate`)
- **货币** (`currency`)

**文档**: `lixinger-api-docs/docs/hk_company_operation-revenue-constitution.md`

<!-- 搜索关键词: date currency 数据时间 公告日期 营收构成 货币 operation-revenue-constitution declarationDate -->

---

### 公司概况 | profile

**API 路径**: `hk/company/profile`

**说明**: 获取公司概况数据

**返回字段**:

- **股票代码** (`stockCode`)
- **上市日期** (`listingDate`)
- **董事长** (`chairman`)
- **A股** (`classAdescription`)
- **B股** (`classBdescription`)
- **A股股本结构** (`capitalStructureClassA`)
- **B股股本结构** (`capitalStructureClassB`)
- **财政年度结算日期** (`fiscalYearEnd`)
- **公司概况** (`summary`)
- **上市类型** (`listingCategory`)
- **过户处** (`registrar`)
- **公司网址** (`website`)
- **注册地址** (`registeredAddress`)
- **办公地址** (`officeAddress`)

**文档**: `lixinger-api-docs/docs/hk_company_profile.md`

<!-- 搜索关键词: profile classBdescription listingCategory fiscalYearEnd 上市类型 公司网址 财政年度结算日期 B股股本结构 注册地址 summary 上市日期 capitalStructureClassA 办公地址 listingDate A股 chairman 过户处 A股股本结构 B股 公司概况 董事长 classAdescription stockCode registrar registeredAddress officeAddress 股票代码 website capitalStructureClassB -->

---

### 回购 | repurchase

**API 路径**: `hk/company/repurchase`

**说明**: 获取回购数据。 说明: 计算股本为总H股

**返回字段**:

- **回购方式** (`methodOfRepurchase`)
- **最高价** (`highestPrice`)
- **最低价** (`lowestPrice`)
- **成交均价** (`avgPrice`)
- **回购股数** (`num`)
- **总金额** (`totalPaid`)
- **本年内至今（自决议案通过以来）在交易所购回的股数** (`numPurchasedInYearSinceResolution`)
- **自决议通过以来回购股数占通过决议时股本百分比** (`ratioPurchasedSinceResolution`)

**文档**: `lixinger-api-docs/docs/hk_company_repurchase.md`

<!-- 搜索关键词: lowestPrice 自决议通过以来回购股数占通过决议时股本百分比 repurchase 本年内至今（自决议案通过以来）在交易所购回的股数 ratioPurchasedSinceResolution highestPrice methodOfRepurchase 回购 最高价 最低价 totalPaid avgPrice 回购方式 成交均价 回购股数 总金额 numPurchasedInYearSinceResolution num -->

---

### 股东权益变动 | shareholders-equity-change

**API 路径**: `hk/company/shareholders-equity-change`

**说明**: 获取股东权益变动数据。

**返回字段**:

- **日期** (`date`)
- **姓名** (`name`)
- **持有权益的股份数量 子字段: 数额: value: (Number) 股份类型: sharesType: (String)** (`numOfSharesInvolvedList`)
- **持有权益的股份数目 子字段: 数额: value: (Number) 股份类型: sharesType: (String)** (`numOfSharesInterestedList`)
- **占已发行的有投票权股份百分比 子字段: 数额: value: (Number) 股份类型: sharesType: (String)** (`percentageOfIssuedVotingShares`)

**文档**: `lixinger-api-docs/docs/hk_company_shareholders-equity-change.md`

<!-- 搜索关键词: name shareholders-equity-change date percentageOfIssuedVotingShares 日期 numOfSharesInterestedList 持有权益的股份数目 子字段: 数额: value: (Number) 股份类型: sharesType: (String) 占已发行的有投票权股份百分比 子字段: 数额: value: (Number) 股份类型: sharesType: (String) 股东权益变动 持有权益的股份数量 子字段: 数额: value: (Number) 股份类型: sharesType: (String) numOfSharesInvolvedList 姓名 -->

---

### 做空 | short-selling

**API 路径**: `hk/company/short-selling`

**说明**: 获取做空数据。 说明: 计算股本为总H股

**返回字段**:

- **日期** (`date`)
- **做空股数** (`shares`)
- **做空金额** (`shareMoney`)

**文档**: `lixinger-api-docs/docs/hk_company_short-selling.md`

<!-- 搜索关键词: shareMoney 做空金额 date 日期 做空 short-selling shares 做空股数 -->

---

### 拆分 | split

**API 路径**: `hk/company/split`

**说明**: 获取拆分数据。

**返回字段**:

- **公告日期** (`date`)
- **除权除息日** (`exDate`)
- **内容** (`content`)
- **拆分折算比例** (`splitRatio`)

**文档**: `lixinger-api-docs/docs/hk_company_split.md`

<!-- 搜索关键词: 内容 exDate date 公告日期 拆分折算比例 除权除息日 content split splitRatio 拆分 -->

---

## 港股指数

### 指数信息 | index

**API 路径**: `hk/index`

**说明**: 获取指数详细信息。

**返回字段**:

- **指数名称** (`name`)
- **指数代码** (`stockCode`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid** (`fsTableType`)
- **指数来源 恒生 :hsi** (`source`)
- **货币** (`currency`)
- **类型 规模 :size 综合 :composite 行业 :sector 风格 :style 主题 :thematic 策略 :strategy** (`series`)
- **发布时间** (`launchDate`)
- **调样频率 年度 :annually 半年 :semi-annually 季度 :quarterly 月度 :monthly 不定期 :irregularly 定期 :aperiodically** (`rebalancingFrequency`)
- **计算方式 派氏加权 :paasche 分级靠档加权 :grading_weighted 股息率加权 :dividend_grading 等权 :equal 自由流通市值加权 :free_float_cap 修正资本化加权 :modified_cap_weighted 流通市值加权 :negotiable_mc_weighted 债券成分券流通金额加权 :circulation_amount_of_constituent_bonds** (`caculationMethod`)

**文档**: `lixinger-api-docs/docs/hk_index.md`

<!-- 搜索关键词: name 指数来源 恒生 :hsi areaCode 类型 规模 :size 综合 :composite 行业 :sector 风格 :style 主题 :thematic 策略 :strategy 计算方式 派氏加权 :paasche 分级靠档加权 :grading_weighted 股息率加权 :dividend_grading 等权 :equal 自由流通市值加权 :free_float_cap 修正资本化加权 :modified_cap_weighted 流通市值加权 :negotiable_mc_weighted 债券成分券流通金额加权 :circulation_amount_of_constituent_bonds series 地区代码 财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid caculationMethod market currency 发布时间 市场 launchDate 指数名称 调样频率 年度 :annually 半年 :semi-annually 季度 :quarterly 月度 :monthly 不定期 :irregularly 定期 :aperiodically index source rebalancingFrequency fsTableType 指数代码 stockCode 货币 指数信息 -->

---

### K线数据 | candlestick

**API 路径**: `hk/index/candlestick`

**说明**: 获取K线数据。 说明: 中证指数全收益率2016年以前没有数据。

**返回字段**:

- **数据时间** (`date`)
- **开盘价** (`open`)
- **收盘价** (`close`)
- **最高价** (`high`)
- **最低价** (`low`)
- **成交量** (`volume`)
- **金额** (`amount`)
- **涨跌幅** (`change`)

**文档**: `lixinger-api-docs/docs/hk_index_candlestick.md`

<!-- 搜索关键词: change volume date close 开盘价 数据时间 K线数据 金额 low amount 最高价 candlestick 最低价 涨跌幅 成交量 open 收盘价 high -->

---

### 样本信息 | constituents

**API 路径**: `hk/index/constituents`

**说明**: 获取样本信息。

**返回字段**:

- **指数代码** (`stockCode`)

**文档**: `lixinger-api-docs/docs/hk_index_constituents.md`

<!-- 搜索关键词: 指数代码 stockCode 样本信息 constituents -->

---

### 指数回撤 | drawdown

**API 路径**: `hk/index/drawdown`

**说明**: 获取指数回撤数据。

**返回字段**:

- **数据时间** (`date`)
- **回撤** (`value`)

**文档**: `lixinger-api-docs/docs/hk_index_drawdown.md`

<!-- 搜索关键词: date 回撤 数据时间 drawdown value 指数回撤 -->

---

### 财报数据 | hybrid

**API 路径**: `hk/index/fs/hybrid`

**说明**: 获取财务数据，如营业收入、ROE等。 说明: 指标计算请参考指数财务数据计算

**文档**: `lixinger-api-docs/docs/hk_index_fs_hybrid.md`

<!-- 搜索关键词: 财报数据 hybrid -->

---

### 基本面数据 | fundamental

**API 路径**: `hk/index/fundamental`

**说明**: 获取基本面数据，如PE、PB等。 说明: 指标计算请参考指数估值计算

**文档**: `lixinger-api-docs/docs/hk_index_fundamental.md`

<!-- 搜索关键词: 基本面数据 fundamental -->

---

### 互联互通 | mm_ah

**API 路径**: `hk/index/hot/mm_ah`

**说明**: 获取互联互通数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **涨跌幅** (`cpc`)
- **港股通持仓金额** (`mm_sha`)
- **港股通持仓金额占市值比例** (`mm_sha_mc_r`)
- **港股通过去1个交易日净买入金额** (`mm_sh_nba_d1`)
- **港股通过去5个交易日净买入金额** (`mm_sh_nba_d5`)
- **港股通过去20个交易日净买入金额** (`mm_sh_nba_d20`)
- **港股通过去60个交易日净买入金额** (`mm_sh_nba_d60`)
- **港股通过去120个交易日净买入金额** (`mm_sh_nba_d120`)
- **港股通过去240个交易日净买入金额** (`mm_sh_nba_d240`)
- **港股通今年以来净买入金额** (`mm_sh_nba_ys`)
- **港股通过去1个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d1`)
- **港股通过去5个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d5`)
- **港股通过去20个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d20`)
- **港股通过去60个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d60`)
- **港股通过去120个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d120`)
- **港股通过去240个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d240`)
- **港股通今年以來持股金额占市值变化比例** (`mm_sha_mc_rc_ys`)

**文档**: `lixinger-api-docs/docs/hk_index_hot_mm_ah.md`

<!-- 搜索关键词: mm_sh_nba_d1 港股通持仓金额占市值比例 mm_sha_mc_rc_ys mm_sha_mc_rc_d120 港股通今年以來持股金额占市值变化比例 mm_sha_mc_r 互联互通 mm_sh_nba_d20 港股通今年以来净买入金额 港股通过去240个交易日持股金额占市值变化比例 mm_sha_mc_rc_d20 港股通过去60个交易日持股金额占市值变化比例 港股通过去20个交易日净买入金额 mm_sha_mc_rc_d1 港股通过去1个交易日净买入金额 数据时间 mm_sh_nba_d240 港股通过去60个交易日净买入金额 涨跌幅 港股通过去120个交易日持股金额占市值变化比例 港股通过去5个交易日净买入金额 mm_sh_nba_d60 mm_ah 港股通过去5个交易日持股金额占市值变化比例 mm_sh_nba_d5 cpc mm_sha_mc_rc_d5 mm_sha_mc_rc_d60 last_data_date 港股通过去240个交易日净买入金额 mm_sha_mc_rc_d240 港股通过去1个交易日持股金额占市值变化比例 港股通过去20个交易日持股金额占市值变化比例 mm_sh_nba_d120 港股通过去120个交易日净买入金额 mm_sha stockCode mm_sh_nba_ys 股票代码 港股通持仓金额 -->

---

### 互联互通 | mutual-market

**API 路径**: `hk/index/mutual-market`

**说明**: 获取互联互通数据。

**返回字段**:

- **数据时间** (`date`)
- **持股金额** (`shareholdingsMoney`)
- **内资持仓金额占市值比例** (`shareholdingsMoneyToMarketCap`)

**文档**: `lixinger-api-docs/docs/hk_index_mutual-market.md`

<!-- 搜索关键词: date mutual-market 持股金额 数据时间 shareholdingsMoneyToMarketCap 互联互通 shareholdingsMoney 内资持仓金额占市值比例 -->

---

### 指数跟踪基金信息 | tracking-fund

**API 路径**: `hk/index/tracking-fund`

**说明**: 获取指数跟踪基金数据。

**返回字段**:

- **基金名称** (`name`)
- **基金代码** (`stockCode`)
- **简称** (`shortName`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **交易所** (`exchange`)

**文档**: `lixinger-api-docs/docs/hk_index_tracking-fund.md`

<!-- 搜索关键词: name market 基金代码 交易所 市场 指数跟踪基金信息 stockCode 基金名称 shortName exchange areaCode 地区代码 简称 tracking-fund -->

---

## 港股行业

### 股票信息 | industry

**API 路径**: `hk/industry`

**说明**: 获取股票详细信息。

**返回字段**:

- **行业代码** (`stockCode`)
- **行业名称** (`name`)
- **发布时间** (`launchDate`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid** (`fsTableType`)
- **行业分类等级** (`level`)
- **行业来源 恒生 :hsi** (`source`)
- **货币** (`currency`)

**文档**: `lixinger-api-docs/docs/hk_industry.md`

<!-- 搜索关键词: name areaCode 行业名称 地区代码 财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid 股票信息 market currency 发布时间 市场 launchDate 行业代码 source level 行业来源 恒生 :hsi fsTableType 行业分类等级 stockCode 货币 industry -->

---

### 样本信息 | hsi

**API 路径**: `hk/industry/constituents/hsi`

**说明**: 获取样本信息。

**返回字段**:

- **指数代码** (`stockCode`)

**文档**: `lixinger-api-docs/docs/hk_industry_constituents_hsi.md`

<!-- 搜索关键词: hsi 指数代码 stockCode 样本信息 -->

---

### 财报数据 | hybrid

**API 路径**: `hk/industry/fs/hsi/hybrid`

**说明**: 获取财务数据，如营业收入、ROE等。 说明: 指标计算请参考行业财务数据计算

**文档**: `lixinger-api-docs/docs/hk_industry_fs_hsi_hybrid.md`

<!-- 搜索关键词: 财报数据 hybrid -->

---

### 基本面数据 | hsi

**API 路径**: `hk/industry/fundamental/hsi`

**说明**: 获取基本面数据，如PE、PB等。 说明: 指标计算请参考行业估值计算

**文档**: `lixinger-api-docs/docs/hk_industry_fundamental_hsi.md`

<!-- 搜索关键词: 基本面数据 hsi -->

---

### 互联互通 | hsi

**API 路径**: `hk/industry/hot/mm_ah/hsi`

**说明**: 获取互联互通数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **港股通持仓金额** (`mm_sha`)
- **港股通持仓金额占市值比例** (`mm_sha_mc_r`)
- **港股通过去1个交易日净买入金额** (`mm_sh_nba_d1`)
- **港股通过去5个交易日净买入金额** (`mm_sh_nba_d5`)
- **港股通过去20个交易日净买入金额** (`mm_sh_nba_d20`)
- **港股通过去60个交易日净买入金额** (`mm_sh_nba_d60`)
- **港股通过去120个交易日净买入金额** (`mm_sh_nba_d120`)
- **港股通过去240个交易日净买入金额** (`mm_sh_nba_d240`)
- **港股通今年以来净买入金额** (`mm_sh_nba_ys`)
- **港股通过去1个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d1`)
- **港股通过去5个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d5`)
- **港股通过去20个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d20`)
- **港股通过去60个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d60`)
- **港股通过去120个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d120`)
- **港股通过去240个交易日持股金额占市值变化比例** (`mm_sha_mc_rc_d240`)
- **港股通今年以來持股金额占市值变化比例** (`mm_sha_mc_rc_ys`)

**文档**: `lixinger-api-docs/docs/hk_industry_hot_mm_ah_hsi.md`

<!-- 搜索关键词: mm_sh_nba_d1 港股通持仓金额占市值比例 mm_sha_mc_rc_ys mm_sha_mc_rc_d120 港股通今年以來持股金额占市值变化比例 mm_sha_mc_r 互联互通 mm_sh_nba_d20 港股通今年以来净买入金额 港股通过去240个交易日持股金额占市值变化比例 mm_sha_mc_rc_d20 港股通过去60个交易日持股金额占市值变化比例 港股通过去20个交易日净买入金额 mm_sha_mc_rc_d1 港股通过去1个交易日净买入金额 数据时间 mm_sh_nba_d240 港股通过去60个交易日净买入金额 港股通过去120个交易日持股金额占市值变化比例 港股通过去5个交易日净买入金额 mm_sh_nba_d60 港股通过去5个交易日持股金额占市值变化比例 mm_sh_nba_d5 mm_sha_mc_rc_d5 mm_sha_mc_rc_d60 last_data_date 港股通过去240个交易日净买入金额 mm_sha_mc_rc_d240 港股通过去1个交易日持股金额占市值变化比例 港股通过去20个交易日持股金额占市值变化比例 hsi mm_sh_nba_d120 mm_sha stockCode 港股通过去120个交易日净买入金额 mm_sh_nba_ys 股票代码 港股通持仓金额 -->

---

### 互联互通 | hsi

**API 路径**: `hk/industry/mutual-market/hsi`

**说明**: 获取互联互通数据。

**返回字段**:

- **数据时间** (`date`)
- **持股金额** (`shareholdingsMoney`)
- **内资持仓金额占市值比例** (`shareholdingsMoneyToMarketCap`)

**文档**: `lixinger-api-docs/docs/hk_industry_mutual-market_hsi.md`

<!-- 搜索关键词: date 持股金额 hsi 数据时间 shareholdingsMoneyToMarketCap 互联互通 shareholdingsMoney 内资持仓金额占市值比例 -->

---

## 美股指数

### 指数信息 | index

**API 路径**: `us/index`

**说明**: 获取指数详细信息。

**返回字段**:

- **指数名称** (`name`)
- **指数代码** (`stockCode`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid** (`fsTableType`)
- **指数来源 美指 :usi** (`source`)
- **货币** (`currency`)
- **类型 规模 :size 综合 :composite 行业 :sector 风格 :style 主题 :thematic 策略 :strategy** (`series`)
- **发布时间** (`launchDate`)
- **调样频率 年度 :annually 半年 :semi-annually 季度 :quarterly 月度 :monthly 不定期 :irregularly 定期 :aperiodically** (`rebalancingFrequency`)
- **计算方式 派氏加权 :paasche 分级靠档加权 :grading_weighted 股息率加权 :dividend_grading 等权 :equal 自由流通市值加权 :free_float_cap 修正资本化加权 :modified_cap_weighted 流通市值加权 :negotiable_mc_weighted 债券成分券流通金额加权 :circulation_amount_of_constituent_bonds** (`caculationMethod`)

**文档**: `lixinger-api-docs/docs/us_index.md`

<!-- 搜索关键词: name areaCode 类型 规模 :size 综合 :composite 行业 :sector 风格 :style 主题 :thematic 策略 :strategy 计算方式 派氏加权 :paasche 分级靠档加权 :grading_weighted 股息率加权 :dividend_grading 等权 :equal 自由流通市值加权 :free_float_cap 修正资本化加权 :modified_cap_weighted 流通市值加权 :negotiable_mc_weighted 债券成分券流通金额加权 :circulation_amount_of_constituent_bonds series 地区代码 财务报表类型 非金融 :non_financial 银行 :bank 证券 :security 保险 :insurance 房地产投资信托 :reit 其他金融 :other_financial 混合 :hybrid caculationMethod market currency 发布时间 市场 launchDate 指数来源 美指 :usi 指数名称 调样频率 年度 :annually 半年 :semi-annually 季度 :quarterly 月度 :monthly 不定期 :irregularly 定期 :aperiodically index source rebalancingFrequency fsTableType 指数代码 stockCode 货币 指数信息 -->

---

### K线数据 | candlestick

**API 路径**: `us/index/candlestick`

**说明**: 获取K线数据。 说明: 中证指数全收益率2016年以前没有数据。

**返回字段**:

- **数据时间** (`date`)
- **开盘价** (`open`)
- **收盘价** (`close`)
- **最高价** (`high`)
- **最低价** (`low`)
- **成交量** (`volume`)
- **金额** (`amount`)
- **涨跌幅** (`change`)

**文档**: `lixinger-api-docs/docs/us_index_candlestick.md`

<!-- 搜索关键词: change volume date close 开盘价 数据时间 K线数据 金额 low amount 最高价 candlestick 最低价 涨跌幅 成交量 open 收盘价 high -->

---

### 样本信息 | constituents

**API 路径**: `us/index/constituents`

**说明**: 获取样本信息。

**返回字段**:

- **指数代码** (`stockCode`)

**文档**: `lixinger-api-docs/docs/us_index_constituents.md`

<!-- 搜索关键词: 指数代码 stockCode 样本信息 constituents -->

---

### 指数回撤 | drawdown

**API 路径**: `us/index/drawdown`

**说明**: 获取指数回撤数据。

**返回字段**:

- **数据时间** (`date`)
- **回撤** (`value`)

**文档**: `lixinger-api-docs/docs/us_index_drawdown.md`

<!-- 搜索关键词: date 回撤 数据时间 drawdown value 指数回撤 -->

---

### 财报数据 | non_financial

**API 路径**: `us/index/fs/non_financial`

**说明**: 获取财务数据，如营业收入、ROE等。 说明: 指标计算请参考指数财务数据计算

**文档**: `lixinger-api-docs/docs/us_index_fs_non_financial.md`

<!-- 搜索关键词: 财报数据 non_financial -->

---

### 基本面数据 | fundamental

**API 路径**: `us/index/fundamental`

**说明**: 获取基本面数据，如PE、PB等。 说明: 指标计算请参考指数估值计算

**文档**: `lixinger-api-docs/docs/us_index_fundamental.md`

<!-- 搜索关键词: 基本面数据 fundamental -->

---

### 收盘点位 | cp

**API 路径**: `us/index/hot/cp`

**说明**: 获取收盘点位数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **涨跌幅** (`cpc`)
- **今年以来涨跌幅** (`cpc_fys`)
- **近一周涨跌幅** (`cpc_w1`)
- **近二周涨跌幅** (`cpc_w2`)
- **近一月涨跌幅** (`cpc_m1`)
- **近三月涨跌幅** (`cpc_m3`)
- **近六月涨跌幅** (`cpc_m6`)
- **近一年涨跌幅** (`cpc_y1`)
- **近二年年化涨跌幅** (`cp_cac_y2`)
- **近三年年化涨跌幅** (`cp_cac_y3`)
- **近五年年化涨跌幅** (`cp_cac_y5`)
- **近十年年化涨跌幅** (`cp_cac_y10`)
- **发布以来年化涨跌幅** (`cp_cac_fs`)

**文档**: `lixinger-api-docs/docs/us_index_hot_cp.md`

<!-- 搜索关键词: cp_cac_y3 近二年年化涨跌幅 cp_cac_y2 收盘点位 cpc_w1 cp_cac_fs 近一周涨跌幅 cpc_m1 数据时间 cp_cac_y10 涨跌幅 近一月涨跌幅 cpc_y1 近三年年化涨跌幅 近五年年化涨跌幅 cpc_fys cpc_m3 近六月涨跌幅 近三月涨跌幅 cpc last_data_date 发布以来年化涨跌幅 cpc_w2 今年以来涨跌幅 cp 近十年年化涨跌幅 stockCode 近一年涨跌幅 近二周涨跌幅 股票代码 cp_cac_y5 cpc_m6 -->

---

### 场内基金认购净流入 | ifet_sni

**API 路径**: `us/index/hot/ifet_sni`

**说明**: 获取场内基金认购净流入数据。

**返回字段**:

- **股票代码** (`stockCode`)
- **数据时间** (`last_data_date`)
- **涨跌幅** (`cpc`)
- **场内基金资产规模** (`ifet_as`)
- **过去1天场内基金认购净流入** (`ifet_sni_ytd`)
- **过去1周场内基金认购净流入** (`ifet_sni_w1`)
- **过去2周场内基金认购净流入** (`ifet_sni_w2`)
- **过去1个月场内基金认购净流入** (`ifet_ssni_m1`)
- **过去3个月场内基金认购净流入** (`ifet_sni_m3`)
- **过去6个月场内基金认购净流入** (`ifet_sni_m6`)
- **过去1年场内基金认购净流入** (`ifet_sni_y1`)
- **过去2年场内基金认购净流入** (`ifet_sni_y2`)
- **今年以来场内基金认购净流入** (`ifet_sni_fys`)

**文档**: `lixinger-api-docs/docs/us_index_hot_ifet_sni.md`

<!-- 搜索关键词: ifet_sni_fys 过去2周场内基金认购净流入 ifet_as ifet_sni 过去3个月场内基金认购净流入 数据时间 ifet_sni_m6 涨跌幅 过去1个月场内基金认购净流入 过去1周场内基金认购净流入 cpc 过去6个月场内基金认购净流入 场内基金认购净流入 last_data_date ifet_ssni_m1 ifet_sni_ytd ifet_sni_w2 过去2年场内基金认购净流入 ifet_sni_y1 ifet_sni_w1 ifet_sni_m3 stockCode 过去1年场内基金认购净流入 ifet_sni_y2 过去1天场内基金认购净流入 股票代码 场内基金资产规模 今年以来场内基金认购净流入 -->

---

### 指数跟踪基金信息 | tracking-fund

**API 路径**: `us/index/tracking-fund`

**说明**: 获取指数跟踪基金数据。

**返回字段**:

- **基金名称** (`name`)
- **基金代码** (`stockCode`)
- **简称** (`shortName`)
- **地区代码** (`areaCode`)
- **市场** (`market`)
- **交易所** (`exchange`)

**文档**: `lixinger-api-docs/docs/us_index_tracking-fund.md`

<!-- 搜索关键词: name market 基金代码 交易所 市场 指数跟踪基金信息 stockCode 基金名称 shortName exchange areaCode 地区代码 简称 tracking-fund -->

---

## 宏观数据

### 国际收支平衡 | bop

**API 路径**: `macro/bop`

**说明**: 获取国际收支平衡数据，如资本账户差额等。

**文档**: `lixinger-api-docs/docs/macro_bop.md`

<!-- 搜索关键词: 国际收支平衡 bop -->

---

### 央行资产负债表 | central-bank-balance-sheet

**API 路径**: `macro/central-bank-balance-sheet`

**说明**: 获取央行资产负债表数据，如总资产等。

**文档**: `lixinger-api-docs/docs/macro_central-bank-balance-sheet.md`

<!-- 搜索关键词: central-bank-balance-sheet 央行资产负债表 -->

---

### 信用证券账户 | credit-securities-account

**API 路径**: `macro/credit-securities-account`

**说明**: 获取信用证券账户数据，如新增信用证券账户等。

**文档**: `lixinger-api-docs/docs/macro_credit-securities-account.md`

<!-- 搜索关键词: credit-securities-account 信用证券账户 -->

---

### 原油 | crude-oil

**API 路径**: `macro/crude-oil`

**说明**: 获取原油数据，如WTI原油现货价格,布伦特原油现货价格等。

**文档**: `lixinger-api-docs/docs/macro_crude-oil.md`

<!-- 搜索关键词: crude-oil 原油 -->

---

### 汇率 | currency-exchange-rate

**API 路径**: `macro/currency-exchange-rate`

**说明**: 获取汇率数据。

**文档**: `lixinger-api-docs/docs/macro_currency-exchange-rate.md`

<!-- 搜索关键词: currency-exchange-rate 汇率 -->

---

### 国内各类债券 | domestic-debt-securities

**API 路径**: `macro/domestic-debt-securities`

**说明**: 获取国内各类债券数据，如政府债券发行金额等。

**文档**: `lixinger-api-docs/docs/macro_domestic-debt-securities.md`

<!-- 搜索关键词: 国内各类债券 domestic-debt-securities -->

---

### 社会消费品零售 | domestic-trade

**API 路径**: `macro/domestic-trade`

**说明**: 获取社会消费品零售数据，如社会消费品零售总额等。

**文档**: `lixinger-api-docs/docs/macro_domestic-trade.md`

<!-- 搜索关键词: domestic-trade 社会消费品零售 -->

---

### 能源 | energy

**API 路径**: `macro/energy`

**说明**: 获取能源数据，如电力生产量等。

**文档**: `lixinger-api-docs/docs/macro_energy.md`

<!-- 搜索关键词: 能源 energy -->

---

###  | foreign-assets

**API 路径**: `macro/foreign-assets`

**说明**: 获取国外资产数据，如外汇等。

**文档**: `lixinger-api-docs/docs/macro_foreign-assets.md`

<!-- 搜索关键词:  foreign-assets -->

---

### 对外贸易 | foreign-trade

**API 路径**: `macro/foreign-trade`

**说明**: 获取对外贸易数据，如进出口总额(人民币)等。

**文档**: `lixinger-api-docs/docs/macro_foreign-trade.md`

<!-- 搜索关键词: 对外贸易 foreign-trade -->

---

### Gdp  | gdp

**API 路径**: `macro/gdp`

**说明**: 获取GDP数据，如GDP等。

**文档**: `lixinger-api-docs/docs/macro_gdp.md`

<!-- 搜索关键词: Gdp  gdp -->

---

### 黄金 | gold-price

**API 路径**: `macro/gold-price`

**说明**: 获取黄金数据，如上海金价格等。

**文档**: `lixinger-api-docs/docs/macro_gold-price.md`

<!-- 搜索关键词: gold-price 黄金 -->

---

### 工业 | industrialization

**API 路径**: `macro/industrialization`

**说明**: 获取工业数据，如工业企业利润总额等。

**文档**: `lixinger-api-docs/docs/macro_industrialization.md`

<!-- 搜索关键词: 工业 industrialization -->

---

### 利率 | interest-rates

**API 路径**: `macro/interest-rates`

**说明**: 获取利率数据，如活期存款等。

**文档**: `lixinger-api-docs/docs/macro_interest-rates.md`

<!-- 搜索关键词: 利率 interest-rates -->

---

### 全社会固定资产投资 | investment-in-fixed-assets

**API 路径**: `macro/investment-in-fixed-assets`

**说明**: 获取全社会固定资产投资数据，如固定资产投资(不含农户)等。

**文档**: `lixinger-api-docs/docs/macro_investment-in-fixed-assets.md`

<!-- 搜索关键词: investment-in-fixed-assets 全社会固定资产投资 -->

---

### 投资者 | investor

**API 路径**: `macro/investor`

**说明**: 获取投资者数据，如自然人等。

**文档**: `lixinger-api-docs/docs/macro_investor.md`

<!-- 搜索关键词: investor 投资者 -->

---

### 杠杆率 | leverage-ratio

**API 路径**: `macro/leverage-ratio`

**说明**: 获取杠杆率数据

**文档**: `lixinger-api-docs/docs/macro_leverage-ratio.md`

<!-- 搜索关键词: 杠杆率 leverage-ratio -->

---

### 货币供应 | money-supply

**API 路径**: `macro/money-supply`

**说明**: 获取货币供应数据，如M1等。

**文档**: `lixinger-api-docs/docs/macro_money-supply.md`

<!-- 搜索关键词: money-supply 货币供应 -->

---

### 国债 | national-debt

**API 路径**: `macro/national-debt`

**说明**: 获取国债数据，如十年期收益率等。

**文档**: `lixinger-api-docs/docs/macro_national-debt.md`

<!-- 搜索关键词: 国债 national-debt -->

---

### 天然气 | natural-gas

**API 路径**: `macro/natural-gas`

**说明**: 获取天然气数据，如亨利港天然气现货价格等。

**文档**: `lixinger-api-docs/docs/macro_natural-gas.md`

<!-- 搜索关键词: 天然气 natural-gas -->

---

### 有色金属 | non-ferrous-metals

**API 路径**: `macro/non-ferrous-metals`

**说明**: 获取有色金属数据，如伦敦铜价格等。

**文档**: `lixinger-api-docs/docs/macro_non-ferrous-metals.md`

<!-- 搜索关键词: 有色金属 non-ferrous-metals -->

---

###  | official-reserve-assets

**API 路径**: `macro/official-reserve-assets`

**说明**: 获取官方储备资产数据，如官方储备资产-合计等。

**文档**: `lixinger-api-docs/docs/macro_official-reserve-assets.md`

<!-- 搜索关键词:  official-reserve-assets -->

---

### 石油 | petroleum

**API 路径**: `macro/petroleum`

**说明**: 获取石油数据，如世界石油和其他液体库存等。

**文档**: `lixinger-api-docs/docs/macro_petroleum.md`

<!-- 搜索关键词: petroleum 石油 -->

---

### 铂金 | platinum-price

**API 路径**: `macro/platinum-price`

**说明**: 获取铂金数据，如伦敦铂金价格等。

**文档**: `lixinger-api-docs/docs/macro_platinum-price.md`

<!-- 搜索关键词: 铂金 platinum-price -->

---

### 人口 | population

**API 路径**: `macro/population`

**说明**: 获取人口数据，如总人口等。

**文档**: `lixinger-api-docs/docs/macro_population.md`

<!-- 搜索关键词: 人口 population -->

---

### 价格指数 | price-index

**API 路径**: `macro/price-index`

**说明**: 获取价格指数数据，如居民消费价格指数(CPI)等。

**文档**: `lixinger-api-docs/docs/macro_price-index.md`

<!-- 搜索关键词: 价格指数 price-index -->

---

### 房地产 | real-estate

**API 路径**: `macro/real-estate`

**说明**: 获取房地产数据，如房地产投资额等。

**文档**: `lixinger-api-docs/docs/macro_real-estate.md`

<!-- 搜索关键词: real-estate 房地产 -->

---

### 存款准备金率 | required-reserves

**API 路径**: `macro/required-reserves`

**说明**: 获取存款准备金率，如大型金融机构存款准备金率等。

**文档**: `lixinger-api-docs/docs/macro_required-reserves.md`

<!-- 搜索关键词: required-reserves 存款准备金率 -->

---

###  | rmb-deposits

**API 路径**: `macro/rmb-deposits`

**说明**: 获取人民币贷款数据，如人民币存款等。

**文档**: `lixinger-api-docs/docs/macro_rmb-deposits.md`

<!-- 搜索关键词:  rmb-deposits -->

---

###  | rmb-loans

**API 路径**: `macro/rmb-loans`

**说明**: 获取人民币贷款数据，如人民币贷款等。

**文档**: `lixinger-api-docs/docs/macro_rmb-loans.md`

<!-- 搜索关键词:  rmb-loans -->

---

### 人民币指数 | rmbidx

**API 路径**: `macro/rmbidx`

**说明**: 获取人民币指数数据

**文档**: `lixinger-api-docs/docs/macro_rmbidx.md`

<!-- 搜索关键词: 人民币指数 rmbidx -->

---

### 白银 | silver-price

**API 路径**: `macro/silver-price`

**说明**: 获取白银数据，如伦敦银价格等。

**文档**: `lixinger-api-docs/docs/macro_silver-price.md`

<!-- 搜索关键词: 白银 silver-price -->

---

### 社会融资 | social-financing

**API 路径**: `macro/social-financing`

**说明**: 获取社会融资数据，如社会融资等。

**文档**: `lixinger-api-docs/docs/macro_social-financing.md`

<!-- 搜索关键词: 社会融资 social-financing -->

---

### 印花税 | stamp-duty

**API 路径**: `macro/stamp-duty`

**说明**: 获取印花税数据，如沪市A股印花税等。

**文档**: `lixinger-api-docs/docs/macro_stamp-duty.md`

<!-- 搜索关键词: 印花税 stamp-duty -->

---

### 交通运输 | traffic-transportation

**API 路径**: `macro/traffic-transportation`

**说明**: 获取交通运输数据，如铁路货运量等。

**文档**: `lixinger-api-docs/docs/macro_traffic-transportation.md`

<!-- 搜索关键词: traffic-transportation 交通运输 -->

---

### 美元指数 | usdx

**API 路径**: `macro/usdx`

**说明**: 获取美元指数数据

**文档**: `lixinger-api-docs/docs/macro_usdx.md`

<!-- 搜索关键词: usdx 美元指数 -->

---
