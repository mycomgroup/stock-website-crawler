# RiceQuant 因子大全 (向导式策略)

本项目支持的所有 RiceQuant 因子列表。你可以直接在策略配置文件的 `filters` 或 `sorting` 中使用这些因子的 `name`。

## 1. 基本面因子 (fundamental)

### 估值指标 (valuation)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `pe_ratio` | 市盈率(PE) | 股价/每股收益 |
| `pb_ratio` | 市净率(PB) | 股价/每股净资产 |
| `ps_ratio` | 市销率(PS) | 股价/每股销售额 |
| `pcf_ratio` | 市现率(PCF) | 股价/每股现金流 |
| `market_cap` | 总市值 | 总股本×股价 |
| `circulating_market_cap` | 流通市值 | 流通股本×股价 |
| `capitalization` | 总股本 | 公司总股本 |
| `circulating_cap` | 流通股本 | 可交易股本 |

### 盈利能力 (profitability)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `roe` | 净资产收益率(ROE) | 净利润/净资产 |
| `roa` | 总资产收益率(ROA) | 净利润/总资产 |
| `gross_profit_margin` | 毛利率 | 毛利/营业收入 |
| `net_profit_margin` | 净利率 | 净利润/营业收入 |
| `operating_profit_margin` | 营业利润率 | 营业利润/营业收入 |
| `ebit_margin` | EBIT利润率 | EBIT/营业收入 |
| `net_profit_after_tax` | 税后净利润 | 扣除税收后的净利润 |

### 成长能力 (growth)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `revenue_growth_rate` | 营业收入增长率 | 营收同比增长 |
| `net_profit_growth_rate` | 净利润增长率 | 净利润同比增长 |
| `operating_profit_growth_rate` | 营业利润增长率 | 营业利润同比增长 |
| `total_profit_growth_rate` | 利润总额增长率 | 利润总额同比增长 |
| `total_assets_growth_rate` | 总资产增长率 | 总资产同比增长 |
| `net_profit_growth_rate_1y` | 净利润增长率(1年) | 过去一年净利润同比增长 |
| `revenue_growth_rate_1y` | 营收增长率(1年) | 过去一年营收同比增长 |

### 财务健康 (financialHealth)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `debt_ratio` | 资产负债率 | 总负债/总资产 |
| `current_ratio` | 流动比率 | 流动资产/流动负债 |
| `quick_ratio` | 速动比率 | (流动资产-存货)/流动负债 |
| `equity_ratio` | 产权比率 | 总负债/股东权益 |
| `tangible_asset_ratio` | 有形资产比率 | 有形资产/总资产 |
| `interest_coverage_ratio` | 利息保障倍数 | 息税前利润/利息支出 |

### 营运能力 (efficiency)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `inventory_turnover` | 存货周转率 | 销货成本/平均存货余额 |
| `accounts_receivable_turnover` | 应收账款周转率 | 营收/平均应收账款余额 |
| `asset_turnover` | 总资产周转率 | 营收/平均总资产 |

### 现金流 (cashFlow)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `operating_cash_flow_per_share` | 每股经营现金流 | 经营现金流/股本 |
| `free_cash_flow_per_share` | 每股自由现金流 | 自由现金流/股本 |
| `cash_flow_to_debt` | 现金流债务比 | 经营现金流/总负债 |
| `operating_cash_flow_growth_rate` | 经营现金流增长率 | 经营现金流同比增长 |

### 分红指标 (dividend)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `dividend_yield` | 股息率 | 每股股利/股价 |
| `dividend_payout_ratio` | 股利支付率 | 股利/净利润 |

### 每股指标 (perShare)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `eps` | 每股收益(EPS) | 净利润/股本 |
| `book_value_per_share` | 每股净资产 | 净资产/股本 |
| `revenue_per_share` | 每股营业收入 | 营业收入/股本 |
| `operating_profit_per_share` | 每股营业利润 | 营业利润/股本 |

### 分析师预测 (analyst)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `target_price` | 分析师目标价 | 分析师一致预测目标价 |
| `rating` | 分析师评级 | 1-买入, 2-增持, 3-持有, 4-减持, 5-卖出 |
| `eps_forecast` | 预测每股收益 | 未来一年预测EPS |
| `revenue_forecast_growth` | 预测营收增长率 | 未来一年预测营收增长 |
| `net_profit_forecast_growth` | 预测净利润增长率 | 未来一年预测净利润增长 |

---

## 2. 量价因子 (pricing)

### 价格指标 (price)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `open` | 开盘价 | 当日开盘价 |
| `close` | 收盘价 | 当日收盘价 |
| `high` | 最高价 | 当日最高价 |
| `low` | 最低价 | 当日最低价 |
| `last` | 最新价 | 最新成交价 |
| `limit_up` | 涨停价 | 当日涨停价 |
| `limit_down` | 跌停价 | 当日跌停价 |

### 成交量指标 (volume)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `volume` | 成交量 | 成交股数 |
| `turnover` | 成交额 | 成交金额 |
| `turnover_rate` | 换手率 | 成交量/流通股本 |

### 涨跌指标 (performance)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `change_rate` | 涨跌幅 | 今日涨跌幅 |
| `n_day_gain_rate` | N日涨幅 | N日累计涨幅 (带参数 `days`) |
| `high_52w` | 52周最高 | 过去52周最高价 |
| `low_52w` | 52周最低 | 过去52周最低价 |

---

## 3. 技术指标 (technical)

### 趋势指标 (trend)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `MA` | 移动平均线 | 简单移动平均 (带参数 `time_period`) |
| `EMA` | 指数移动平均 | 指数移动平均 (带参数 `time_period`) |
| `MACD` | MACD | 指数平滑异同移动平均线 |
| `ADX` | 平均趋向指标 | 衡量趋势强度 |
| `TRIX` | 三重指数平滑平均线 | 衡量价格动量 |

### 动量指标 (momentum)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `RSI` | 相对强弱指标 | 相对强弱指标 (带参数 `time_period`) |
| `CCI` | 顺势指标 | 顺势指标 |
| `KDJ` | KDJ指标 | 随机指标 |
| `WILLR` | 威廉指标 | 威廉指标 |
| `MFI` | 资金流量指标 | 结合价格和成交量 |

### 波动率指标 (volatility)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `ATR` | 真实波幅 | 平均真实波幅 |
| `BOLL` | 布林带 | 布林带 |
| `STDDEV` | 标准差 | 标准差 |
| `SAR` | 抛物线转向 | 抛物线指标 |

### 成交量类指标 (volume)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `OBV` | 能量潮 | 累积成交量指标 |

---

## 4. 元数据 (extra)
| 因子名 (name) | 界面标签 (label) | 说明 |
| :--- | :--- | :--- |
| `listed_days` | 上市天数 | 上市至今天数 |
| `industry` | 所属行业 | 所属行业 |
| `board_type` | 板块类型 | 主板/创业板/科创板 |
