---
id: "url-364972e4"
type: "website"
title: "JQData数据范围及更新时间"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10261"
description: "数据介绍"
source: ""
tags: []
crawl_time: "2026-03-27T07:29:00.730Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10261"
  headings:
    - {"level":3,"text":"JQData数据范围及更新时间","id":""}
  paragraphs:
    - "数据介绍"
    - "</body> </html>"
  lists:
    - {"type":"ul","items":["为了满足用户的需求，聚宽数据团队在JQData中不仅提供了全面的基础金融数据，包括沪深A股行情数据，上市公司财务数据，场内基金数据，场外基金数据，指数数据，期货数据，期权数据、债券数据、可转债数据以及宏观经济数据；除此之外，JQData还针对因子数据和特色数据，引进了聚宽因子库，舆情数据，Alpha特色因子，技术分析指标因子，tick数据，助您更好的完成量化研究和投资决策。详细数据清单如下表所示："]}
    - {"type":"ul","items":["有关财务数据更新：一般是这样的情况，譬如财报公布的发布日期是date，实际上一般会在date前一个交易日的晚上发布出来，我们程序也会在date前一天晚上和date这天早上更新财报；","期货结算价更新时间：17:00后；"]}
  tables:
    - {"caption":"","headers":["数据品种","API接口","时间范围","更新频率"],"rows":[["通用接口"],["将标的代码转化成聚宽标准格式","normalize_code()","",""],["获取指定范围交易日","get_trade_days()","上市至今","8:00更新"],["获取交易列表","get_all_securities()","上市至今","8:00更新"],["获取单支标的信息","get_security_info()","上市至今","8:00更新"],["查询数据库数据","run_query()","",""],["批量查询数据库","run_offset_query()","",""],["沪深A股"],["股票ST信息","get_extras()","2005年至今","盘前9:15更新"],["上市公司状态变动","finance.STK_STATUS_CHANGE","2005年至今","交易日24:00更新"],["获取股票的融资融券信息","get_mtss()","2010年至今","下一个交易日9点之前更新"],["融资标的列表","get_margincash_stocks()","2010年至今","每天21:00更新下一交易日"],["融券标的列表","get_marginsec_stocks()","2010年至今","每天21:00更新下一交易日"],["融资融券汇总数据","finance.STK_MT_TOTAL","2010年至今","下一个交易日9点之前更新"],["股票资金流向","get_money_flow_pro()","2010年至今","盘后19:00更新"],["股票龙虎榜数据","get_billboard_list()","2005年至今","盘后20:00和22:00更新"],["沪深市场每日成交概况","finance.STK_EXCHANGE_TRADE_INFO)","2005年至今","交易日20:30-24:00更新"],["行业列表","get_industries()","2005年至今","8:00更新"],["行业成份股","get_industry_stocks()","2005年至今","8:00更新"],["查询股票所属行业","get_industry()","2005年至今","8:00更新"],["查询股票所属行业","get_industry()","2005年至今","8:00更新"],["获取某个行业的所有历史成分股纳入剔除记录（新）","get_history_industry","上市至今","8:00更新"],["概念成分股","get_concept_stocks()","2005年至今","8:00更新"],["股票所属概念板块","get_concept()","2005年至今","8:00更新"],["市场通交易日历","finance.STK_EXCHANGE_LINK_CALENDAR","上市至今","交易日20:30-06:30更新"],["市场通AH股价格对比","finance.STK_AH_PRICE_COMP","上市至今","交易日20:30-06:30更新"],["市场通合格证券变动记录","finance.STK_EL_CONST_CHANGE","上市至今","交易日20:30-06:30更新"],["沪深港通持股数据","finance.STK_HK_HOLD_INFO","上市至今","交易日20:30-06:30更新"],["市场通十大成交活跃股","finance.STK_EL_TOP_ACTIVATE","上市至今","交易日20:30-06:30更新"],["市场通成交与额度信息","finance.STK_ML_QUOTA","上市至今","交易日20:30-06:30更新"],["市场通汇率","finance.STK_EXCHANGE_LINK_RATE","上市至今","交易日20:30-06:30更新"],["获取股票当日盘前交易信息","get_preopen_infos()","当天","更新时间：盘前交易日 09:15 后可获取到数据"],["get_price 移动行情窗口","get_price()","2005年至今","盘后15:00更新，24:00校对完成入库"],["get_bars固定行情窗口","get_bars()","2005年至今","盘后15:00更新，24:00校对完成入库"],["获取集合竞价数据","get_call_auction()","2010年至今","盘后15:00更新，24:00校对完成入库"],["股票tick数据","get_ticks()","2010年至今","盘后15:00更新，24:00校对完成入库"],["股票-单季度/年度财务数据"],["查询财务数据(附综合案例)","get_fundamentals()","2005年至今","每天24:00更新（\"24:00\"是指夜间持续更新, 一般最后一个更新时间为次日盘前 09:00）"],["多日财务数据","get_fundamentals_continuously()","2005年至今","每天24:00更新"],["获取多个季度/年度的财务数据","get_history_fundamentals()","2005年至今","每天24:00更新"],["获取多个标的在指定交易日范围内的市值表数据","get_valuation()","2005年至今","每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空； 每天盘后(16:30)更新全部指标"],["估值数据（市值、市盈率、市净率等）","valuation","2005年至今","每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空； 每天盘后(16:30)更新全部指标"],["财务指标数据","indicator","2005年至今","每天24:00更新"],["现金流量表","cash_flow","2005年至今","每天24:00更新"],["利润表","income","2005年至今","每天24:00更新"],["资产负债表","balance","2005年至今","每天24:00更新"],["银行业","bank_indicator","2005年至今","每天24:00更新"],["券商","security_indicator","2005年至今","每天24:00更新"],["保险","insurance_indicator","2005年至今","每天24:00更新"],["股票报告期财务数据"],["审计报告","finance.STK_AUDIT_OPINION","2005年至今","每天24:00更新"],["定期报告预约披露时间表(新上线数据)","STK_REPORT_DISCLOSURE","2005年至今","每天24:00更新"],["上市公司业绩快报（新）","finance.STK_PERFORMANCE_LETTERS","2005年至今","每天24:00更新"],["上市公司业绩预告","finance.STK_FIN_FORCAST","2005年至今","每天24:00更新"],["利润表","income","2005年至今","每天24:00更新"],["现金流量表","cash_flow","2005年至今","每天24:00更新"],["资产负债表","balance","2005年至今","每天24:00更新"],["利润表金融类","finance.FINANCE_INCOME_STATEMENT","2005年至今","每天24:00更新"],["现金流量表金融类","finance.FINANCE_CASHFLOW_STATEMENT","2005年至今","每天24:00更新"],["资产负债表金融类","finance.FINANCE_BALANCE_SHEET_PARENT","2005年至今","每天24:00更新"],["上市公司相关信息"],["上市公司状态变动","finance.STK_STATUS_CHANGE","2005年至今","交易日24:00更新"],["上市公司基本信息","finance.STK_COMPANY_INFO","2005年至今","交易日24:00更新"],["上市信息","finance.STK_LIST","2005年至今","交易日24:00更新"],["简称变更情况","finance.STK_NAME_HISTORY","2005年至今","交易日24:00更新"],["员工情况","finance.STK_EMPLOYEE_INFO","2005年至今","交易日24:00更新"],["公司管理人员任职情况","finance.STK_MANAGEMENT_INFO","2005年至今","交易日24:00更新"],["十大股东","finance.STK_SHAREHOLDER_TOP10","2005年至今","交易日24:00更新"],["十大流通股东","finance.STK_SHAREHOLDER_FLOATING_TOP10","2005年至今","交易日24:00更新"],["股东股份质押","finance.STK_SHARES_PLEDGE","2005年至今","交易日24:00更新"],["股东股份冻结","finance.STK_SHARES_FROZEN","2005年至今","交易日24:00更新"],["股东户数","finance.STK_HOLDER_NUM","2005年至今","交易日24:00更新"],["大股东增减持","finance.STK_SHAREHOLDERS_SHARE_CHANGE","2005年至今","交易日24:00更新"],["上市公司股本变动","finance.STK_CAPITAL_CHANGE","2005年至今","交易日24:00更新"],["受限股份上市公告日期","finance.STK_LIMITED_SHARES_LIST","2005年至今","交易日24:00更新"],["受限股份实际解禁日期","finance.STK_LIMITED_SHARES_UNLIMIT","2005年至今","交易日24:00更新"],["限售解禁股","get_locked_shares()","2005年至今","交易日24:00更新"],["上市公司分红送股（除权除息）","finance.STK_XR_XD","2005年至今","交易日24:00更新"],["期货"],["指定日期的期货列表数据","get_future_contracts()","2005年至今","8:00更新"],["期货主力合约","get_dominant_future()","2005年至今","19点更新下一交易日"],["期货合约信息","get_futures_info()","2005年至今","8点更新"],["获取期货保证金(结算参数)","finance.FUT_MARGIN","2013年至今","17:00 更新"],["期货手续费","finance.FUT_CHARGE","2013年至今","17:00 按实际披露更新当天, 20:30按公告推算填充下一交易日"],["期货龙虎榜数据(会员持仓)","finance.FUT_MEMBER_POSITION_RANK","2005年至今","盘后19:00更新"],["期货仓单数据","finance.FUT_WAREHOUSE_RECEIPT","2005年至今","盘后20:00更新"],["期货结算价","get_extras()","2005年至今","盘后17:00 更新"],["外盘期货日行情数据","finance.FUT_GLOBAL_DAILY","上市至今","盘前09:00更新"],["商品期货分钟/日行情数据","get_price()/get_bars()","2005年至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["商品期货&金融期货tick数据","get_ticks()","2010年至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["获取当月/次月/当季/隔季等合约拼接而成的bar行情","get_order_future_bar","2005年至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["期货主力和品种指数的定义","","2005年至今",""],["期货列表（支持广期所）","","2005年至今",""],["期权"],["期权列表","期权列表","上市至今","盘后08:30和20:30"],["期权合约资料","opt.OPT_CONTRACT_INFO","上市至今","盘后18:00更新"],["期权日行情(查表)","opt.OPT_DAILY_PRICE","上市至今","盘后更新20:10更新"],["期权风险指标","opt.OPT_RISK_INDICATOR","上市至今","下一交易日盘前8:05更新"],["股票期权交易和持仓排名统计","opt.OPT_TRADE_RANK_STK","上市至今","下一交易日盘前8:05更新"],["期权行权交收信息","opt.OPT_EXERCISE_INFO","上市至今","每日10:45更新"],["期权合约调整记录","opt.OPT_ADJUSTMENT","上市至今","盘后18:00更新"],["期权每日盘前静态文件","opt.OPT_DAILY_PREOPEN","上市至今","盘前9:05更新"],["期权集合竞价数据","get_call_auction()","上市至今","盘后15点更新"],["商品期权分钟/日行情数据","get_price/get_bars","上市至今","盘后15点更新，24点入库"],["金融期权分钟/日行情数据","get_price/get_bars","上市至今","盘后15点更新，24点入库"],["商品期权&金融期权tick数据","get_ticks()","上市至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["基金"],["基金的主体信息","finance.FUND_MAIN_INFO","上市至今","盘后24点更新"],["基金持股信息","finance.FUND_PORTFOLIO_STOCK","上市至今","盘后24:00更新"],["基金持有的债券信息","finance.FUND_PORTFOLIO_BOND","上市至今","盘后24:00更新"],["基金资产组合概况","finance.FUND_PORTFOLIO","上市至今","盘后24:00更新"],["基金财务指标表","finance.FUND_FIN_INDICATOR","上市至今","盘后24:00更新"],["基金分红、拆分和合并的方案","finance.FUND_DIVIDEND","上市至今","盘后24:00更新"],["场内基金份额数据","finance.FUND_SHARE_DAILY","2005-02-23至今","下一个交易日9点20之前更新"],["基金收益日报信息","finance.FUND_MF_DAILY_PROFIT","上市至今","盘后17点到下一交易日9点"],["基金净值信息","finance.FUND_NET_VALUE","上市至今","盘后17点到下一交易日9点"],["基金累计净值/基金单位净值/场外基金的复权净值","get_extras()","上市至今","盘后17点到下一交易日9点"],["获取ETF跟踪指数信息","FUND_INVEST_TARGET","上市年至今","24点更新"],["get_price移动行情窗口","get_price()","2005年至今","盘后15点更新，24点入库"],["get_bars固定行情窗口","get_bars()","2005年至今","盘后15点更新，24点入库"],["获取集合竞价数据","get_call_auction()","2019年至今","盘后15点更新，24点入库"],["基金tick数据","get_ticks()","2010年至今","盘后15点更新，24点入库"],["获取基金的融资融券信息","get_mtss()","2010年至今","下一个交易日9点之前更新"],["基金融资标的列表","get_margincash_stocks()","2010年至今","下一个交易日9点之前更新"],["基金融券标的列表","get_marginsec_stocks()","2010年至今","下一个交易日9点之前更新"],["基金融资融券汇总数据","STK_MT_TOTAL","2010年至今","下一个交易日9点之前更新"],["指数"],["指数估值","get_index_valuation","2005年至今","9点更新总股本、流通股本数据等股本数据，盘后 17:00 更新剩余字段"],["指数成分股数据","get_index_stocks()","2005年至今","每天8点检查更新"],["指数成分股权重(月度)","get_index_weights()","2005年至今","每天8点检查更新；注意该数据是月度的，中证指数公司一般只在月末/月初披露"],["get_price移动行情窗口","get_price()","2005年至今","盘后15点更新，24点入库"],["get_bars固定行情窗口","get_bars()","2005年至今","盘后15点更新，24点入库"],["获取集合竞价数据","get_call_acution()","2017年至今","盘后15点更新，24点入库"],["指数tick数据","get_ticks()","2017年至今","盘后15点更新，24点入库"],["聚宽特色指数（新）"],["聚宽特色指数交易标的列表","get_index_valuation","2010年至今","每日8:00更新"],["聚宽特色指数成分股","get_index_stocks()","2010年至今","每日8:00更新"],["get_price移动行情窗口","get_price()","2010年至今","凌晨3:00更新"],["get_bars固定行情窗口","get_bars()","2010年至今","凌晨3:00更新"],["债券&可转债"],["债券基本信息","bond.BOND_BASIC_INFO","上市至今","每日19：00、22:00更新"],["债券票面利率","bond.BOND_COUPON","上市至今","每日19：00、22:00更新"],["债券付息事件","bond.BOND_INTEREST_PAYMENT","上市至今","每日19：00、22:00更新"],["国债逆回购日行情数据","bond.REPO_DAILY_PRICE","上市至今","每日19：00、22:00更新"],["可转债基本资料","bond.CONBOND_BASIC_INFO","上市至今","每日19：00、22:00更新"],["可转债转股价格调整","bond.CONBOND_CONVERT_PRICE_ADJUST","上市至今","每日19：00、22:00更新"],["可转债每日转股统计","bond.CONBOND_DAILY_CONVERT","2000/7/12至今","下一交易日 8:30、12：30更新"],["可转债日行情数据（查表）","bond.CONBOND_DAILY_PRICE","2018/9/13至今","每日19：00、22:00更新"],["get_price移动行情窗口","get_price()","2019年至今","盘后15点更新，24点入库"],["get_bars固定行情窗口","get_bars()","2019年至今","盘后15点更新，24点入库"],["获取集合竞价数据","get_call_auction()","2019年至今","盘后15:00更新，24:00校对完成入库"],["可转债tick数据","get_ticks()","2019年至今","盘后15点更新，24点入库"],["Tick快照数据（仅限机构用户）"],["股票Tick","get_ticks()","2010-01-01至今","盘后15:00更新，24:00入库"],["商品期货Tick","get_ticks()","2010-01-01至今","盘后15:00更新，24:00入库"],["金融期货Tick","get_ticks()","2010-01-01至今","盘后15:00更新，24:00入库"],["商品期权Tick","get_ticks()","上市至今","盘后15:00更新，24:00入库"],["金融期权Tick","get_ticks()","上市至今","盘后15:00更新，24:00入库"],["指数Tick","get_ticks()","2010-01-01 至今","盘后15:00更新，24:00入库"],["基金Tick","get_ticks()","2010年至今","盘后15:00更新，24:00入库"],["可转债Tick","get_ticks()","2019-01-01 至今","盘后15:00更新，24:00入库"],["风格因子CNE5"],["获取聚宽因子名称","get_all_factors","",""],["风险模型 - 风格因子（CNE5）","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["获取重点宽基指数的风格暴露（新）","get_index_style_exposure","2011-08-31至今","9:00更新前一交易日"],["因子看板列表数据","get_factor_kanban_values","2005至今","9:00更新前一交易日"],["因子看板分位数历史收益率","get_factor_stats","2005至今","9:00更新前一交易日"],["获取风格因子暴露收益率","get_factor_style_returns","2005至今","9:00更新前一交易日"],["获取特异收益率","get_factor_specific_returns","2005至今","9:00更新前一交易日"],["获取风格因子协方差矩阵","get_factor_cov","2005至今","9:00更新前一交易日"],["风格因子pro(CNE6)"],["获取聚宽因子名称","get_all_factors","",""],["风险模型 - 风格因子pro（CNE6）","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["获取重点宽基指数的风格暴露（新）","get_index_style_exposure","2011-08-31至今","9:00更新前一交易日"],["因子看板列表数据","get_factor_kanban_values","2005至今","9:00更新前一交易日"],["因子看板分位数历史收益率","get_factor_stats","2005至今","9:00更新前一交易日"],["获取风格因子pro(CNE6)暴露收益率","get_factor_style_returns","2005至今","9:00更新前一交易日"],["获取特异收益率","get_factor_specific_returns","2005至今","9:00更新前一交易日"],["获取风格因子pro(CNE6)协方差矩阵","get_factor_cov","2005至今","9:00更新前一交易日"],["资金流向因子"],["股票日分钟资金流向","get_money_flow_pro","2015年至今","分钟级别在每日15:00更新、天行情每日19：00更新"],["聚宽因子"],["获取聚宽因子名称","get_all_factors","",""],["获取因子看板列表数据","get_factor_kanban_values","2005至今","9:00更新前一交易日"],["获取因子看板分位数历史收益率","get_factor_stats","2005至今","9:00更新前一交易日"],["质量类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["基础类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["成长类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["每股类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["情绪类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["风险类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["动量类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["技术类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["行业因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["Alpha特色因子"],["Alpha 101 因子","get_all_alpha_101","2005至今","次日08:00更新，动态复权"],["Alpha 191 因子","get_all_alpha_191","2005至今","次日08:00更新，动态复权"],["技术指标因子"],["超买超卖型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["趋势型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["能量型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["成交量型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["均线型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["路径型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["其他","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["宏观数据"],["国民经济","macro.MAC_SALE_RETAIL_MONTH","统计局统计开始至今","交易日盘前8：30之前更新"],["保险业","macro.MAC_INSURANCE_AREA_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["人民生活","macro.MAC_AREA_CONSUME_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["人口","macro.MAC_POPULATION_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["国内贸易","macro.MAC_SALE_RETAIL_MONTH","统计局统计开始至今","交易日盘前8：30之前更新"],["就业与工资","macro.MAC_AREA_UNEMPLOY","统计局统计开始至今","交易日盘前8：30之前更新"],["资源环境","macro.MAC_RESOURCES_AREA_FOREST","统计局统计开始至今","交易日盘前8：30之前更新"],["房地产行业","macro.MAC_INDUSTRY_ESTATEINVEST_MONTH","统计局统计开始至今","交易日盘前8：30之前更新"],["财政政策","macro.MAC_FISCAL_TOTAL_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["固定资产投资","macro.MAC_FIXED_INVESTMENT","统计局统计开始至今","交易日盘前8：30之前更新"],["对外经济贸易","macro.MAC_TRADE_VALUE_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["景气指数","macro.MAC_ECONOMIC_BOOM_IDX","统计局统计开始至今","交易日盘前8：30之前更新"],["工业","macro.MAC_INDUSTRY_GROWTH","统计局统计开始至今","交易日盘前8：30之前更新"],["农林牧渔业","macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER","统计局统计开始至今","交易日盘前8：30之前更新"],["金融业","macro.MAC_RMB_EXCHANGE_RATE","统计局统计开始至今","交易日盘前8：30之前更新"],["舆情数据"],["新闻联播文本数据","finance.CCTV_NEWS","2009年6月至今","每日21:30前更新"]]}
  codeBlocks: []
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"JQData数据范围及更新时间"}
    - {"type":"paragraph","content":"数据介绍"}
    - {"type":"list","listType":"ul","items":["为了满足用户的需求，聚宽数据团队在JQData中不仅提供了全面的基础金融数据，包括沪深A股行情数据，上市公司财务数据，场内基金数据，场外基金数据，指数数据，期货数据，期权数据、债券数据、可转债数据以及宏观经济数据；除此之外，JQData还针对因子数据和特色数据，引进了聚宽因子库，舆情数据，Alpha特色因子，技术分析指标因子，tick数据，助您更好的完成量化研究和投资决策。详细数据清单如下表所示："]}
    - {"type":"list","listType":"ul","items":["有关财务数据更新：一般是这样的情况，譬如财报公布的发布日期是date，实际上一般会在date前一个交易日的晚上发布出来，我们程序也会在date前一天晚上和date这天早上更新财报；","期货结算价更新时间：17:00后；"]}
    - {"type":"table","headers":["数据品种","API接口","时间范围","更新频率"],"rows":[["通用接口"],["将标的代码转化成聚宽标准格式","normalize_code()","",""],["获取指定范围交易日","get_trade_days()","上市至今","8:00更新"],["获取交易列表","get_all_securities()","上市至今","8:00更新"],["获取单支标的信息","get_security_info()","上市至今","8:00更新"],["查询数据库数据","run_query()","",""],["批量查询数据库","run_offset_query()","",""],["沪深A股"],["股票ST信息","get_extras()","2005年至今","盘前9:15更新"],["上市公司状态变动","finance.STK_STATUS_CHANGE","2005年至今","交易日24:00更新"],["获取股票的融资融券信息","get_mtss()","2010年至今","下一个交易日9点之前更新"],["融资标的列表","get_margincash_stocks()","2010年至今","每天21:00更新下一交易日"],["融券标的列表","get_marginsec_stocks()","2010年至今","每天21:00更新下一交易日"],["融资融券汇总数据","finance.STK_MT_TOTAL","2010年至今","下一个交易日9点之前更新"],["股票资金流向","get_money_flow_pro()","2010年至今","盘后19:00更新"],["股票龙虎榜数据","get_billboard_list()","2005年至今","盘后20:00和22:00更新"],["沪深市场每日成交概况","finance.STK_EXCHANGE_TRADE_INFO)","2005年至今","交易日20:30-24:00更新"],["行业列表","get_industries()","2005年至今","8:00更新"],["行业成份股","get_industry_stocks()","2005年至今","8:00更新"],["查询股票所属行业","get_industry()","2005年至今","8:00更新"],["查询股票所属行业","get_industry()","2005年至今","8:00更新"],["获取某个行业的所有历史成分股纳入剔除记录（新）","get_history_industry","上市至今","8:00更新"],["概念成分股","get_concept_stocks()","2005年至今","8:00更新"],["股票所属概念板块","get_concept()","2005年至今","8:00更新"],["市场通交易日历","finance.STK_EXCHANGE_LINK_CALENDAR","上市至今","交易日20:30-06:30更新"],["市场通AH股价格对比","finance.STK_AH_PRICE_COMP","上市至今","交易日20:30-06:30更新"],["市场通合格证券变动记录","finance.STK_EL_CONST_CHANGE","上市至今","交易日20:30-06:30更新"],["沪深港通持股数据","finance.STK_HK_HOLD_INFO","上市至今","交易日20:30-06:30更新"],["市场通十大成交活跃股","finance.STK_EL_TOP_ACTIVATE","上市至今","交易日20:30-06:30更新"],["市场通成交与额度信息","finance.STK_ML_QUOTA","上市至今","交易日20:30-06:30更新"],["市场通汇率","finance.STK_EXCHANGE_LINK_RATE","上市至今","交易日20:30-06:30更新"],["获取股票当日盘前交易信息","get_preopen_infos()","当天","更新时间：盘前交易日 09:15 后可获取到数据"],["get_price 移动行情窗口","get_price()","2005年至今","盘后15:00更新，24:00校对完成入库"],["get_bars固定行情窗口","get_bars()","2005年至今","盘后15:00更新，24:00校对完成入库"],["获取集合竞价数据","get_call_auction()","2010年至今","盘后15:00更新，24:00校对完成入库"],["股票tick数据","get_ticks()","2010年至今","盘后15:00更新，24:00校对完成入库"],["股票-单季度/年度财务数据"],["查询财务数据(附综合案例)","get_fundamentals()","2005年至今","每天24:00更新（\"24:00\"是指夜间持续更新, 一般最后一个更新时间为次日盘前 09:00）"],["多日财务数据","get_fundamentals_continuously()","2005年至今","每天24:00更新"],["获取多个季度/年度的财务数据","get_history_fundamentals()","2005年至今","每天24:00更新"],["获取多个标的在指定交易日范围内的市值表数据","get_valuation()","2005年至今","每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空； 每天盘后(16:30)更新全部指标"],["估值数据（市值、市盈率、市净率等）","valuation","2005年至今","每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空； 每天盘后(16:30)更新全部指标"],["财务指标数据","indicator","2005年至今","每天24:00更新"],["现金流量表","cash_flow","2005年至今","每天24:00更新"],["利润表","income","2005年至今","每天24:00更新"],["资产负债表","balance","2005年至今","每天24:00更新"],["银行业","bank_indicator","2005年至今","每天24:00更新"],["券商","security_indicator","2005年至今","每天24:00更新"],["保险","insurance_indicator","2005年至今","每天24:00更新"],["股票报告期财务数据"],["审计报告","finance.STK_AUDIT_OPINION","2005年至今","每天24:00更新"],["定期报告预约披露时间表(新上线数据)","STK_REPORT_DISCLOSURE","2005年至今","每天24:00更新"],["上市公司业绩快报（新）","finance.STK_PERFORMANCE_LETTERS","2005年至今","每天24:00更新"],["上市公司业绩预告","finance.STK_FIN_FORCAST","2005年至今","每天24:00更新"],["利润表","income","2005年至今","每天24:00更新"],["现金流量表","cash_flow","2005年至今","每天24:00更新"],["资产负债表","balance","2005年至今","每天24:00更新"],["利润表金融类","finance.FINANCE_INCOME_STATEMENT","2005年至今","每天24:00更新"],["现金流量表金融类","finance.FINANCE_CASHFLOW_STATEMENT","2005年至今","每天24:00更新"],["资产负债表金融类","finance.FINANCE_BALANCE_SHEET_PARENT","2005年至今","每天24:00更新"],["上市公司相关信息"],["上市公司状态变动","finance.STK_STATUS_CHANGE","2005年至今","交易日24:00更新"],["上市公司基本信息","finance.STK_COMPANY_INFO","2005年至今","交易日24:00更新"],["上市信息","finance.STK_LIST","2005年至今","交易日24:00更新"],["简称变更情况","finance.STK_NAME_HISTORY","2005年至今","交易日24:00更新"],["员工情况","finance.STK_EMPLOYEE_INFO","2005年至今","交易日24:00更新"],["公司管理人员任职情况","finance.STK_MANAGEMENT_INFO","2005年至今","交易日24:00更新"],["十大股东","finance.STK_SHAREHOLDER_TOP10","2005年至今","交易日24:00更新"],["十大流通股东","finance.STK_SHAREHOLDER_FLOATING_TOP10","2005年至今","交易日24:00更新"],["股东股份质押","finance.STK_SHARES_PLEDGE","2005年至今","交易日24:00更新"],["股东股份冻结","finance.STK_SHARES_FROZEN","2005年至今","交易日24:00更新"],["股东户数","finance.STK_HOLDER_NUM","2005年至今","交易日24:00更新"],["大股东增减持","finance.STK_SHAREHOLDERS_SHARE_CHANGE","2005年至今","交易日24:00更新"],["上市公司股本变动","finance.STK_CAPITAL_CHANGE","2005年至今","交易日24:00更新"],["受限股份上市公告日期","finance.STK_LIMITED_SHARES_LIST","2005年至今","交易日24:00更新"],["受限股份实际解禁日期","finance.STK_LIMITED_SHARES_UNLIMIT","2005年至今","交易日24:00更新"],["限售解禁股","get_locked_shares()","2005年至今","交易日24:00更新"],["上市公司分红送股（除权除息）","finance.STK_XR_XD","2005年至今","交易日24:00更新"],["期货"],["指定日期的期货列表数据","get_future_contracts()","2005年至今","8:00更新"],["期货主力合约","get_dominant_future()","2005年至今","19点更新下一交易日"],["期货合约信息","get_futures_info()","2005年至今","8点更新"],["获取期货保证金(结算参数)","finance.FUT_MARGIN","2013年至今","17:00 更新"],["期货手续费","finance.FUT_CHARGE","2013年至今","17:00 按实际披露更新当天, 20:30按公告推算填充下一交易日"],["期货龙虎榜数据(会员持仓)","finance.FUT_MEMBER_POSITION_RANK","2005年至今","盘后19:00更新"],["期货仓单数据","finance.FUT_WAREHOUSE_RECEIPT","2005年至今","盘后20:00更新"],["期货结算价","get_extras()","2005年至今","盘后17:00 更新"],["外盘期货日行情数据","finance.FUT_GLOBAL_DAILY","上市至今","盘前09:00更新"],["商品期货分钟/日行情数据","get_price()/get_bars()","2005年至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["商品期货&金融期货tick数据","get_ticks()","2010年至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["获取当月/次月/当季/隔季等合约拼接而成的bar行情","get_order_future_bar","2005年至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["期货主力和品种指数的定义","","2005年至今",""],["期货列表（支持广期所）","","2005年至今",""],["期权"],["期权列表","期权列表","上市至今","盘后08:30和20:30"],["期权合约资料","opt.OPT_CONTRACT_INFO","上市至今","盘后18:00更新"],["期权日行情(查表)","opt.OPT_DAILY_PRICE","上市至今","盘后更新20:10更新"],["期权风险指标","opt.OPT_RISK_INDICATOR","上市至今","下一交易日盘前8:05更新"],["股票期权交易和持仓排名统计","opt.OPT_TRADE_RANK_STK","上市至今","下一交易日盘前8:05更新"],["期权行权交收信息","opt.OPT_EXERCISE_INFO","上市至今","每日10:45更新"],["期权合约调整记录","opt.OPT_ADJUSTMENT","上市至今","盘后18:00更新"],["期权每日盘前静态文件","opt.OPT_DAILY_PREOPEN","上市至今","盘前9:05更新"],["期权集合竞价数据","get_call_auction()","上市至今","盘后15点更新"],["商品期权分钟/日行情数据","get_price/get_bars","上市至今","盘后15点更新，24点入库"],["金融期权分钟/日行情数据","get_price/get_bars","上市至今","盘后15点更新，24点入库"],["商品期权&金融期权tick数据","get_ticks()","上市至今","夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库"],["基金"],["基金的主体信息","finance.FUND_MAIN_INFO","上市至今","盘后24点更新"],["基金持股信息","finance.FUND_PORTFOLIO_STOCK","上市至今","盘后24:00更新"],["基金持有的债券信息","finance.FUND_PORTFOLIO_BOND","上市至今","盘后24:00更新"],["基金资产组合概况","finance.FUND_PORTFOLIO","上市至今","盘后24:00更新"],["基金财务指标表","finance.FUND_FIN_INDICATOR","上市至今","盘后24:00更新"],["基金分红、拆分和合并的方案","finance.FUND_DIVIDEND","上市至今","盘后24:00更新"],["场内基金份额数据","finance.FUND_SHARE_DAILY","2005-02-23至今","下一个交易日9点20之前更新"],["基金收益日报信息","finance.FUND_MF_DAILY_PROFIT","上市至今","盘后17点到下一交易日9点"],["基金净值信息","finance.FUND_NET_VALUE","上市至今","盘后17点到下一交易日9点"],["基金累计净值/基金单位净值/场外基金的复权净值","get_extras()","上市至今","盘后17点到下一交易日9点"],["获取ETF跟踪指数信息","FUND_INVEST_TARGET","上市年至今","24点更新"],["get_price移动行情窗口","get_price()","2005年至今","盘后15点更新，24点入库"],["get_bars固定行情窗口","get_bars()","2005年至今","盘后15点更新，24点入库"],["获取集合竞价数据","get_call_auction()","2019年至今","盘后15点更新，24点入库"],["基金tick数据","get_ticks()","2010年至今","盘后15点更新，24点入库"],["获取基金的融资融券信息","get_mtss()","2010年至今","下一个交易日9点之前更新"],["基金融资标的列表","get_margincash_stocks()","2010年至今","下一个交易日9点之前更新"],["基金融券标的列表","get_marginsec_stocks()","2010年至今","下一个交易日9点之前更新"],["基金融资融券汇总数据","STK_MT_TOTAL","2010年至今","下一个交易日9点之前更新"],["指数"],["指数估值","get_index_valuation","2005年至今","9点更新总股本、流通股本数据等股本数据，盘后 17:00 更新剩余字段"],["指数成分股数据","get_index_stocks()","2005年至今","每天8点检查更新"],["指数成分股权重(月度)","get_index_weights()","2005年至今","每天8点检查更新；注意该数据是月度的，中证指数公司一般只在月末/月初披露"],["get_price移动行情窗口","get_price()","2005年至今","盘后15点更新，24点入库"],["get_bars固定行情窗口","get_bars()","2005年至今","盘后15点更新，24点入库"],["获取集合竞价数据","get_call_acution()","2017年至今","盘后15点更新，24点入库"],["指数tick数据","get_ticks()","2017年至今","盘后15点更新，24点入库"],["聚宽特色指数（新）"],["聚宽特色指数交易标的列表","get_index_valuation","2010年至今","每日8:00更新"],["聚宽特色指数成分股","get_index_stocks()","2010年至今","每日8:00更新"],["get_price移动行情窗口","get_price()","2010年至今","凌晨3:00更新"],["get_bars固定行情窗口","get_bars()","2010年至今","凌晨3:00更新"],["债券&可转债"],["债券基本信息","bond.BOND_BASIC_INFO","上市至今","每日19：00、22:00更新"],["债券票面利率","bond.BOND_COUPON","上市至今","每日19：00、22:00更新"],["债券付息事件","bond.BOND_INTEREST_PAYMENT","上市至今","每日19：00、22:00更新"],["国债逆回购日行情数据","bond.REPO_DAILY_PRICE","上市至今","每日19：00、22:00更新"],["可转债基本资料","bond.CONBOND_BASIC_INFO","上市至今","每日19：00、22:00更新"],["可转债转股价格调整","bond.CONBOND_CONVERT_PRICE_ADJUST","上市至今","每日19：00、22:00更新"],["可转债每日转股统计","bond.CONBOND_DAILY_CONVERT","2000/7/12至今","下一交易日 8:30、12：30更新"],["可转债日行情数据（查表）","bond.CONBOND_DAILY_PRICE","2018/9/13至今","每日19：00、22:00更新"],["get_price移动行情窗口","get_price()","2019年至今","盘后15点更新，24点入库"],["get_bars固定行情窗口","get_bars()","2019年至今","盘后15点更新，24点入库"],["获取集合竞价数据","get_call_auction()","2019年至今","盘后15:00更新，24:00校对完成入库"],["可转债tick数据","get_ticks()","2019年至今","盘后15点更新，24点入库"],["Tick快照数据（仅限机构用户）"],["股票Tick","get_ticks()","2010-01-01至今","盘后15:00更新，24:00入库"],["商品期货Tick","get_ticks()","2010-01-01至今","盘后15:00更新，24:00入库"],["金融期货Tick","get_ticks()","2010-01-01至今","盘后15:00更新，24:00入库"],["商品期权Tick","get_ticks()","上市至今","盘后15:00更新，24:00入库"],["金融期权Tick","get_ticks()","上市至今","盘后15:00更新，24:00入库"],["指数Tick","get_ticks()","2010-01-01 至今","盘后15:00更新，24:00入库"],["基金Tick","get_ticks()","2010年至今","盘后15:00更新，24:00入库"],["可转债Tick","get_ticks()","2019-01-01 至今","盘后15:00更新，24:00入库"],["风格因子CNE5"],["获取聚宽因子名称","get_all_factors","",""],["风险模型 - 风格因子（CNE5）","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["获取重点宽基指数的风格暴露（新）","get_index_style_exposure","2011-08-31至今","9:00更新前一交易日"],["因子看板列表数据","get_factor_kanban_values","2005至今","9:00更新前一交易日"],["因子看板分位数历史收益率","get_factor_stats","2005至今","9:00更新前一交易日"],["获取风格因子暴露收益率","get_factor_style_returns","2005至今","9:00更新前一交易日"],["获取特异收益率","get_factor_specific_returns","2005至今","9:00更新前一交易日"],["获取风格因子协方差矩阵","get_factor_cov","2005至今","9:00更新前一交易日"],["风格因子pro(CNE6)"],["获取聚宽因子名称","get_all_factors","",""],["风险模型 - 风格因子pro（CNE6）","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["获取重点宽基指数的风格暴露（新）","get_index_style_exposure","2011-08-31至今","9:00更新前一交易日"],["因子看板列表数据","get_factor_kanban_values","2005至今","9:00更新前一交易日"],["因子看板分位数历史收益率","get_factor_stats","2005至今","9:00更新前一交易日"],["获取风格因子pro(CNE6)暴露收益率","get_factor_style_returns","2005至今","9:00更新前一交易日"],["获取特异收益率","get_factor_specific_returns","2005至今","9:00更新前一交易日"],["获取风格因子pro(CNE6)协方差矩阵","get_factor_cov","2005至今","9:00更新前一交易日"],["资金流向因子"],["股票日分钟资金流向","get_money_flow_pro","2015年至今","分钟级别在每日15:00更新、天行情每日19：00更新"],["聚宽因子"],["获取聚宽因子名称","get_all_factors","",""],["获取因子看板列表数据","get_factor_kanban_values","2005至今","9:00更新前一交易日"],["获取因子看板分位数历史收益率","get_factor_stats","2005至今","9:00更新前一交易日"],["质量类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["基础类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["成长类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["每股类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["情绪类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["风险类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["动量类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["技术类因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["行业因子","get_factor_values","2005年至今","下一自然日5:00、8:00更新"],["Alpha特色因子"],["Alpha 101 因子","get_all_alpha_101","2005至今","次日08:00更新，动态复权"],["Alpha 191 因子","get_all_alpha_191","2005至今","次日08:00更新，动态复权"],["技术指标因子"],["超买超卖型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["趋势型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["能量型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["成交量型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["均线型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["路径型技术指标","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["其他","from jqdatasdk.technical_analysis import *","2005至今","根据传入的参数计算"],["宏观数据"],["国民经济","macro.MAC_SALE_RETAIL_MONTH","统计局统计开始至今","交易日盘前8：30之前更新"],["保险业","macro.MAC_INSURANCE_AREA_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["人民生活","macro.MAC_AREA_CONSUME_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["人口","macro.MAC_POPULATION_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["国内贸易","macro.MAC_SALE_RETAIL_MONTH","统计局统计开始至今","交易日盘前8：30之前更新"],["就业与工资","macro.MAC_AREA_UNEMPLOY","统计局统计开始至今","交易日盘前8：30之前更新"],["资源环境","macro.MAC_RESOURCES_AREA_FOREST","统计局统计开始至今","交易日盘前8：30之前更新"],["房地产行业","macro.MAC_INDUSTRY_ESTATEINVEST_MONTH","统计局统计开始至今","交易日盘前8：30之前更新"],["财政政策","macro.MAC_FISCAL_TOTAL_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["固定资产投资","macro.MAC_FIXED_INVESTMENT","统计局统计开始至今","交易日盘前8：30之前更新"],["对外经济贸易","macro.MAC_TRADE_VALUE_YEAR","统计局统计开始至今","交易日盘前8：30之前更新"],["景气指数","macro.MAC_ECONOMIC_BOOM_IDX","统计局统计开始至今","交易日盘前8：30之前更新"],["工业","macro.MAC_INDUSTRY_GROWTH","统计局统计开始至今","交易日盘前8：30之前更新"],["农林牧渔业","macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER","统计局统计开始至今","交易日盘前8：30之前更新"],["金融业","macro.MAC_RMB_EXCHANGE_RATE","统计局统计开始至今","交易日盘前8：30之前更新"],["舆情数据"],["新闻联播文本数据","finance.CCTV_NEWS","2009年6月至今","每日21:30前更新"]]}
    - {"type":"paragraph","content":"</body> </html>"}
  suggestedFilename: "doc_JQDatadoc_10261_overview_JQData数据范围及更新时间"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10261"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# JQData数据范围及更新时间

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10261

## 描述

数据介绍

## 内容

#### JQData数据范围及更新时间

数据介绍

- 为了满足用户的需求，聚宽数据团队在JQData中不仅提供了全面的基础金融数据，包括沪深A股行情数据，上市公司财务数据，场内基金数据，场外基金数据，指数数据，期货数据，期权数据、债券数据、可转债数据以及宏观经济数据；除此之外，JQData还针对因子数据和特色数据，引进了聚宽因子库，舆情数据，Alpha特色因子，技术分析指标因子，tick数据，助您更好的完成量化研究和投资决策。详细数据清单如下表所示：

- 有关财务数据更新：一般是这样的情况，譬如财报公布的发布日期是date，实际上一般会在date前一个交易日的晚上发布出来，我们程序也会在date前一天晚上和date这天早上更新财报；
- 期货结算价更新时间：17:00后；

| 数据品种 | API接口 | 时间范围 | 更新频率 |
| --- | --- | --- | --- |
| 通用接口 |
| 将标的代码转化成聚宽标准格式 | normalize_code() |  |  |
| 获取指定范围交易日 | get_trade_days() | 上市至今 | 8:00更新 |
| 获取交易列表 | get_all_securities() | 上市至今 | 8:00更新 |
| 获取单支标的信息 | get_security_info() | 上市至今 | 8:00更新 |
| 查询数据库数据 | run_query() |  |  |
| 批量查询数据库 | run_offset_query() |  |  |
| 沪深A股 |
| 股票ST信息 | get_extras() | 2005年至今 | 盘前9:15更新 |
| 上市公司状态变动 | finance.STK_STATUS_CHANGE | 2005年至今 | 交易日24:00更新 |
| 获取股票的融资融券信息 | get_mtss() | 2010年至今 | 下一个交易日9点之前更新 |
| 融资标的列表 | get_margincash_stocks() | 2010年至今 | 每天21:00更新下一交易日 |
| 融券标的列表 | get_marginsec_stocks() | 2010年至今 | 每天21:00更新下一交易日 |
| 融资融券汇总数据 | finance.STK_MT_TOTAL | 2010年至今 | 下一个交易日9点之前更新 |
| 股票资金流向 | get_money_flow_pro() | 2010年至今 | 盘后19:00更新 |
| 股票龙虎榜数据 | get_billboard_list() | 2005年至今 | 盘后20:00和22:00更新 |
| 沪深市场每日成交概况 | finance.STK_EXCHANGE_TRADE_INFO) | 2005年至今 | 交易日20:30-24:00更新 |
| 行业列表 | get_industries() | 2005年至今 | 8:00更新 |
| 行业成份股 | get_industry_stocks() | 2005年至今 | 8:00更新 |
| 查询股票所属行业 | get_industry() | 2005年至今 | 8:00更新 |
| 查询股票所属行业 | get_industry() | 2005年至今 | 8:00更新 |
| 获取某个行业的所有历史成分股纳入剔除记录（新） | get_history_industry | 上市至今 | 8:00更新 |
| 概念成分股 | get_concept_stocks() | 2005年至今 | 8:00更新 |
| 股票所属概念板块 | get_concept() | 2005年至今 | 8:00更新 |
| 市场通交易日历 | finance.STK_EXCHANGE_LINK_CALENDAR | 上市至今 | 交易日20:30-06:30更新 |
| 市场通AH股价格对比 | finance.STK_AH_PRICE_COMP | 上市至今 | 交易日20:30-06:30更新 |
| 市场通合格证券变动记录 | finance.STK_EL_CONST_CHANGE | 上市至今 | 交易日20:30-06:30更新 |
| 沪深港通持股数据 | finance.STK_HK_HOLD_INFO | 上市至今 | 交易日20:30-06:30更新 |
| 市场通十大成交活跃股 | finance.STK_EL_TOP_ACTIVATE | 上市至今 | 交易日20:30-06:30更新 |
| 市场通成交与额度信息 | finance.STK_ML_QUOTA | 上市至今 | 交易日20:30-06:30更新 |
| 市场通汇率 | finance.STK_EXCHANGE_LINK_RATE | 上市至今 | 交易日20:30-06:30更新 |
| 获取股票当日盘前交易信息 | get_preopen_infos() | 当天 | 更新时间：盘前交易日 09:15 后可获取到数据 |
| get_price 移动行情窗口 | get_price() | 2005年至今 | 盘后15:00更新，24:00校对完成入库 |
| get_bars固定行情窗口 | get_bars() | 2005年至今 | 盘后15:00更新，24:00校对完成入库 |
| 获取集合竞价数据 | get_call_auction() | 2010年至今 | 盘后15:00更新，24:00校对完成入库 |
| 股票tick数据 | get_ticks() | 2010年至今 | 盘后15:00更新，24:00校对完成入库 |
| 股票-单季度/年度财务数据 |
| 查询财务数据(附综合案例) | get_fundamentals() | 2005年至今 | 每天24:00更新（"24:00"是指夜间持续更新, 一般最后一个更新时间为次日盘前 09:00） |
| 多日财务数据 | get_fundamentals_continuously() | 2005年至今 | 每天24:00更新 |
| 获取多个季度/年度的财务数据 | get_history_fundamentals() | 2005年至今 | 每天24:00更新 |
| 获取多个标的在指定交易日范围内的市值表数据 | get_valuation() | 2005年至今 | 每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空； 每天盘后(16:30)更新全部指标 |
| 估值数据（市值、市盈率、市净率等） | valuation | 2005年至今 | 每天盘前(08:30)更新当日总股本及流通股本数据，便于用户盘中计算各类指标，其他字段置空； 每天盘后(16:30)更新全部指标 |
| 财务指标数据 | indicator | 2005年至今 | 每天24:00更新 |
| 现金流量表 | cash_flow | 2005年至今 | 每天24:00更新 |
| 利润表 | income | 2005年至今 | 每天24:00更新 |
| 资产负债表 | balance | 2005年至今 | 每天24:00更新 |
| 银行业 | bank_indicator | 2005年至今 | 每天24:00更新 |
| 券商 | security_indicator | 2005年至今 | 每天24:00更新 |
| 保险 | insurance_indicator | 2005年至今 | 每天24:00更新 |
| 股票报告期财务数据 |
| 审计报告 | finance.STK_AUDIT_OPINION | 2005年至今 | 每天24:00更新 |
| 定期报告预约披露时间表(新上线数据) | STK_REPORT_DISCLOSURE | 2005年至今 | 每天24:00更新 |
| 上市公司业绩快报（新） | finance.STK_PERFORMANCE_LETTERS | 2005年至今 | 每天24:00更新 |
| 上市公司业绩预告 | finance.STK_FIN_FORCAST | 2005年至今 | 每天24:00更新 |
| 利润表 | income | 2005年至今 | 每天24:00更新 |
| 现金流量表 | cash_flow | 2005年至今 | 每天24:00更新 |
| 资产负债表 | balance | 2005年至今 | 每天24:00更新 |
| 利润表金融类 | finance.FINANCE_INCOME_STATEMENT | 2005年至今 | 每天24:00更新 |
| 现金流量表金融类 | finance.FINANCE_CASHFLOW_STATEMENT | 2005年至今 | 每天24:00更新 |
| 资产负债表金融类 | finance.FINANCE_BALANCE_SHEET_PARENT | 2005年至今 | 每天24:00更新 |
| 上市公司相关信息 |
| 上市公司状态变动 | finance.STK_STATUS_CHANGE | 2005年至今 | 交易日24:00更新 |
| 上市公司基本信息 | finance.STK_COMPANY_INFO | 2005年至今 | 交易日24:00更新 |
| 上市信息 | finance.STK_LIST | 2005年至今 | 交易日24:00更新 |
| 简称变更情况 | finance.STK_NAME_HISTORY | 2005年至今 | 交易日24:00更新 |
| 员工情况 | finance.STK_EMPLOYEE_INFO | 2005年至今 | 交易日24:00更新 |
| 公司管理人员任职情况 | finance.STK_MANAGEMENT_INFO | 2005年至今 | 交易日24:00更新 |
| 十大股东 | finance.STK_SHAREHOLDER_TOP10 | 2005年至今 | 交易日24:00更新 |
| 十大流通股东 | finance.STK_SHAREHOLDER_FLOATING_TOP10 | 2005年至今 | 交易日24:00更新 |
| 股东股份质押 | finance.STK_SHARES_PLEDGE | 2005年至今 | 交易日24:00更新 |
| 股东股份冻结 | finance.STK_SHARES_FROZEN | 2005年至今 | 交易日24:00更新 |
| 股东户数 | finance.STK_HOLDER_NUM | 2005年至今 | 交易日24:00更新 |
| 大股东增减持 | finance.STK_SHAREHOLDERS_SHARE_CHANGE | 2005年至今 | 交易日24:00更新 |
| 上市公司股本变动 | finance.STK_CAPITAL_CHANGE | 2005年至今 | 交易日24:00更新 |
| 受限股份上市公告日期 | finance.STK_LIMITED_SHARES_LIST | 2005年至今 | 交易日24:00更新 |
| 受限股份实际解禁日期 | finance.STK_LIMITED_SHARES_UNLIMIT | 2005年至今 | 交易日24:00更新 |
| 限售解禁股 | get_locked_shares() | 2005年至今 | 交易日24:00更新 |
| 上市公司分红送股（除权除息） | finance.STK_XR_XD | 2005年至今 | 交易日24:00更新 |
| 期货 |
| 指定日期的期货列表数据 | get_future_contracts() | 2005年至今 | 8:00更新 |
| 期货主力合约 | get_dominant_future() | 2005年至今 | 19点更新下一交易日 |
| 期货合约信息 | get_futures_info() | 2005年至今 | 8点更新 |
| 获取期货保证金(结算参数) | finance.FUT_MARGIN | 2013年至今 | 17:00 更新 |
| 期货手续费 | finance.FUT_CHARGE | 2013年至今 | 17:00 按实际披露更新当天, 20:30按公告推算填充下一交易日 |
| 期货龙虎榜数据(会员持仓) | finance.FUT_MEMBER_POSITION_RANK | 2005年至今 | 盘后19:00更新 |
| 期货仓单数据 | finance.FUT_WAREHOUSE_RECEIPT | 2005年至今 | 盘后20:00更新 |
| 期货结算价 | get_extras() | 2005年至今 | 盘后17:00 更新 |
| 外盘期货日行情数据 | finance.FUT_GLOBAL_DAILY | 上市至今 | 盘前09:00更新 |
| 商品期货分钟/日行情数据 | get_price()/get_bars() | 2005年至今 | 夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库 |
| 商品期货&金融期货tick数据 | get_ticks() | 2010年至今 | 夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库 |
| 获取当月/次月/当季/隔季等合约拼接而成的bar行情 | get_order_future_bar | 2005年至今 | 夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库 |
| 期货主力和品种指数的定义 |  | 2005年至今 |  |
| 期货列表（支持广期所） |  | 2005年至今 |  |
| 期权 |
| 期权列表 | 期权列表 | 上市至今 | 盘后08:30和20:30 |
| 期权合约资料 | opt.OPT_CONTRACT_INFO | 上市至今 | 盘后18:00更新 |
| 期权日行情(查表) | opt.OPT_DAILY_PRICE | 上市至今 | 盘后更新20:10更新 |
| 期权风险指标 | opt.OPT_RISK_INDICATOR | 上市至今 | 下一交易日盘前8:05更新 |
| 股票期权交易和持仓排名统计 | opt.OPT_TRADE_RANK_STK | 上市至今 | 下一交易日盘前8:05更新 |
| 期权行权交收信息 | opt.OPT_EXERCISE_INFO | 上市至今 | 每日10:45更新 |
| 期权合约调整记录 | opt.OPT_ADJUSTMENT | 上市至今 | 盘后18:00更新 |
| 期权每日盘前静态文件 | opt.OPT_DAILY_PREOPEN | 上市至今 | 盘前9:05更新 |
| 期权集合竞价数据 | get_call_auction() | 上市至今 | 盘后15点更新 |
| 商品期权分钟/日行情数据 | get_price/get_bars | 上市至今 | 盘后15点更新，24点入库 |
| 金融期权分钟/日行情数据 | get_price/get_bars | 上市至今 | 盘后15点更新，24点入库 |
| 商品期权&金融期权tick数据 | get_ticks() | 上市至今 | 夜盘交易数据凌晨2点30后更新,日盘交易数据盘后15点更新；24点入库 |
| 基金 |
| 基金的主体信息 | finance.FUND_MAIN_INFO | 上市至今 | 盘后24点更新 |
| 基金持股信息 | finance.FUND_PORTFOLIO_STOCK | 上市至今 | 盘后24:00更新 |
| 基金持有的债券信息 | finance.FUND_PORTFOLIO_BOND | 上市至今 | 盘后24:00更新 |
| 基金资产组合概况 | finance.FUND_PORTFOLIO | 上市至今 | 盘后24:00更新 |
| 基金财务指标表 | finance.FUND_FIN_INDICATOR | 上市至今 | 盘后24:00更新 |
| 基金分红、拆分和合并的方案 | finance.FUND_DIVIDEND | 上市至今 | 盘后24:00更新 |
| 场内基金份额数据 | finance.FUND_SHARE_DAILY | 2005-02-23至今 | 下一个交易日9点20之前更新 |
| 基金收益日报信息 | finance.FUND_MF_DAILY_PROFIT | 上市至今 | 盘后17点到下一交易日9点 |
| 基金净值信息 | finance.FUND_NET_VALUE | 上市至今 | 盘后17点到下一交易日9点 |
| 基金累计净值/基金单位净值/场外基金的复权净值 | get_extras() | 上市至今 | 盘后17点到下一交易日9点 |
| 获取ETF跟踪指数信息 | FUND_INVEST_TARGET | 上市年至今 | 24点更新 |
| get_price移动行情窗口 | get_price() | 2005年至今 | 盘后15点更新，24点入库 |
| get_bars固定行情窗口 | get_bars() | 2005年至今 | 盘后15点更新，24点入库 |
| 获取集合竞价数据 | get_call_auction() | 2019年至今 | 盘后15点更新，24点入库 |
| 基金tick数据 | get_ticks() | 2010年至今 | 盘后15点更新，24点入库 |
| 获取基金的融资融券信息 | get_mtss() | 2010年至今 | 下一个交易日9点之前更新 |
| 基金融资标的列表 | get_margincash_stocks() | 2010年至今 | 下一个交易日9点之前更新 |
| 基金融券标的列表 | get_marginsec_stocks() | 2010年至今 | 下一个交易日9点之前更新 |
| 基金融资融券汇总数据 | STK_MT_TOTAL | 2010年至今 | 下一个交易日9点之前更新 |
| 指数 |
| 指数估值 | get_index_valuation | 2005年至今 | 9点更新总股本、流通股本数据等股本数据，盘后 17:00 更新剩余字段 |
| 指数成分股数据 | get_index_stocks() | 2005年至今 | 每天8点检查更新 |
| 指数成分股权重(月度) | get_index_weights() | 2005年至今 | 每天8点检查更新；注意该数据是月度的，中证指数公司一般只在月末/月初披露 |
| get_price移动行情窗口 | get_price() | 2005年至今 | 盘后15点更新，24点入库 |
| get_bars固定行情窗口 | get_bars() | 2005年至今 | 盘后15点更新，24点入库 |
| 获取集合竞价数据 | get_call_acution() | 2017年至今 | 盘后15点更新，24点入库 |
| 指数tick数据 | get_ticks() | 2017年至今 | 盘后15点更新，24点入库 |
| 聚宽特色指数（新） |
| 聚宽特色指数交易标的列表 | get_index_valuation | 2010年至今 | 每日8:00更新 |
| 聚宽特色指数成分股 | get_index_stocks() | 2010年至今 | 每日8:00更新 |
| get_price移动行情窗口 | get_price() | 2010年至今 | 凌晨3:00更新 |
| get_bars固定行情窗口 | get_bars() | 2010年至今 | 凌晨3:00更新 |
| 债券&可转债 |
| 债券基本信息 | bond.BOND_BASIC_INFO | 上市至今 | 每日19：00、22:00更新 |
| 债券票面利率 | bond.BOND_COUPON | 上市至今 | 每日19：00、22:00更新 |
| 债券付息事件 | bond.BOND_INTEREST_PAYMENT | 上市至今 | 每日19：00、22:00更新 |
| 国债逆回购日行情数据 | bond.REPO_DAILY_PRICE | 上市至今 | 每日19：00、22:00更新 |
| 可转债基本资料 | bond.CONBOND_BASIC_INFO | 上市至今 | 每日19：00、22:00更新 |
| 可转债转股价格调整 | bond.CONBOND_CONVERT_PRICE_ADJUST | 上市至今 | 每日19：00、22:00更新 |
| 可转债每日转股统计 | bond.CONBOND_DAILY_CONVERT | 2000/7/12至今 | 下一交易日 8:30、12：30更新 |
| 可转债日行情数据（查表） | bond.CONBOND_DAILY_PRICE | 2018/9/13至今 | 每日19：00、22:00更新 |
| get_price移动行情窗口 | get_price() | 2019年至今 | 盘后15点更新，24点入库 |
| get_bars固定行情窗口 | get_bars() | 2019年至今 | 盘后15点更新，24点入库 |
| 获取集合竞价数据 | get_call_auction() | 2019年至今 | 盘后15:00更新，24:00校对完成入库 |
| 可转债tick数据 | get_ticks() | 2019年至今 | 盘后15点更新，24点入库 |
| Tick快照数据（仅限机构用户） |
| 股票Tick | get_ticks() | 2010-01-01至今 | 盘后15:00更新，24:00入库 |
| 商品期货Tick | get_ticks() | 2010-01-01至今 | 盘后15:00更新，24:00入库 |
| 金融期货Tick | get_ticks() | 2010-01-01至今 | 盘后15:00更新，24:00入库 |
| 商品期权Tick | get_ticks() | 上市至今 | 盘后15:00更新，24:00入库 |
| 金融期权Tick | get_ticks() | 上市至今 | 盘后15:00更新，24:00入库 |
| 指数Tick | get_ticks() | 2010-01-01 至今 | 盘后15:00更新，24:00入库 |
| 基金Tick | get_ticks() | 2010年至今 | 盘后15:00更新，24:00入库 |
| 可转债Tick | get_ticks() | 2019-01-01 至今 | 盘后15:00更新，24:00入库 |
| 风格因子CNE5 |
| 获取聚宽因子名称 | get_all_factors |  |  |
| 风险模型 - 风格因子（CNE5） | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 获取重点宽基指数的风格暴露（新） | get_index_style_exposure | 2011-08-31至今 | 9:00更新前一交易日 |
| 因子看板列表数据 | get_factor_kanban_values | 2005至今 | 9:00更新前一交易日 |
| 因子看板分位数历史收益率 | get_factor_stats | 2005至今 | 9:00更新前一交易日 |
| 获取风格因子暴露收益率 | get_factor_style_returns | 2005至今 | 9:00更新前一交易日 |
| 获取特异收益率 | get_factor_specific_returns | 2005至今 | 9:00更新前一交易日 |
| 获取风格因子协方差矩阵 | get_factor_cov | 2005至今 | 9:00更新前一交易日 |
| 风格因子pro(CNE6) |
| 获取聚宽因子名称 | get_all_factors |  |  |
| 风险模型 - 风格因子pro（CNE6） | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 获取重点宽基指数的风格暴露（新） | get_index_style_exposure | 2011-08-31至今 | 9:00更新前一交易日 |
| 因子看板列表数据 | get_factor_kanban_values | 2005至今 | 9:00更新前一交易日 |
| 因子看板分位数历史收益率 | get_factor_stats | 2005至今 | 9:00更新前一交易日 |
| 获取风格因子pro(CNE6)暴露收益率 | get_factor_style_returns | 2005至今 | 9:00更新前一交易日 |
| 获取特异收益率 | get_factor_specific_returns | 2005至今 | 9:00更新前一交易日 |
| 获取风格因子pro(CNE6)协方差矩阵 | get_factor_cov | 2005至今 | 9:00更新前一交易日 |
| 资金流向因子 |
| 股票日分钟资金流向 | get_money_flow_pro | 2015年至今 | 分钟级别在每日15:00更新、天行情每日19：00更新 |
| 聚宽因子 |
| 获取聚宽因子名称 | get_all_factors |  |  |
| 获取因子看板列表数据 | get_factor_kanban_values | 2005至今 | 9:00更新前一交易日 |
| 获取因子看板分位数历史收益率 | get_factor_stats | 2005至今 | 9:00更新前一交易日 |
| 质量类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 基础类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 成长类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 每股类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 情绪类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 风险类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 动量类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 技术类因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| 行业因子 | get_factor_values | 2005年至今 | 下一自然日5:00、8:00更新 |
| Alpha特色因子 |
| Alpha 101 因子 | get_all_alpha_101 | 2005至今 | 次日08:00更新，动态复权 |
| Alpha 191 因子 | get_all_alpha_191 | 2005至今 | 次日08:00更新，动态复权 |
| 技术指标因子 |
| 超买超卖型技术指标 | from jqdatasdk.technical_analysis import * | 2005至今 | 根据传入的参数计算 |
| 趋势型技术指标 | from jqdatasdk.technical_analysis import * | 2005至今 | 根据传入的参数计算 |
| 能量型技术指标 | from jqdatasdk.technical_analysis import * | 2005至今 | 根据传入的参数计算 |
| 成交量型技术指标 | from jqdatasdk.technical_analysis import * | 2005至今 | 根据传入的参数计算 |
| 均线型技术指标 | from jqdatasdk.technical_analysis import * | 2005至今 | 根据传入的参数计算 |
| 路径型技术指标 | from jqdatasdk.technical_analysis import * | 2005至今 | 根据传入的参数计算 |
| 其他 | from jqdatasdk.technical_analysis import * | 2005至今 | 根据传入的参数计算 |
| 宏观数据 |
| 国民经济 | macro.MAC_SALE_RETAIL_MONTH | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 保险业 | macro.MAC_INSURANCE_AREA_YEAR | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 人民生活 | macro.MAC_AREA_CONSUME_YEAR | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 人口 | macro.MAC_POPULATION_YEAR | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 国内贸易 | macro.MAC_SALE_RETAIL_MONTH | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 就业与工资 | macro.MAC_AREA_UNEMPLOY | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 资源环境 | macro.MAC_RESOURCES_AREA_FOREST | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 房地产行业 | macro.MAC_INDUSTRY_ESTATEINVEST_MONTH | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 财政政策 | macro.MAC_FISCAL_TOTAL_YEAR | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 固定资产投资 | macro.MAC_FIXED_INVESTMENT | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 对外经济贸易 | macro.MAC_TRADE_VALUE_YEAR | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 景气指数 | macro.MAC_ECONOMIC_BOOM_IDX | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 工业 | macro.MAC_INDUSTRY_GROWTH | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 农林牧渔业 | macro.MAC_INDUSTRY_AREA_AGR_OUTPUT_VALUE_QUARTER | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 金融业 | macro.MAC_RMB_EXCHANGE_RATE | 统计局统计开始至今 | 交易日盘前8：30之前更新 |
| 舆情数据 |
| 新闻联播文本数据 | finance.CCTV_NEWS | 2009年6月至今 | 每日21:30前更新 |

</body> </html>
