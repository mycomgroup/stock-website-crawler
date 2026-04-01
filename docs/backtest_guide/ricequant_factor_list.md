# RiceQuant 因子列表速查表

> 更新时间：2026-03-31
> 来源：RiceQuant 官方 API 文档 + 实测验证

## 使用方法

```python
# 获取单个因子
data = get_factor(stocks, "pe_ratio", start_date="2024-01-01", end_date="2024-01-31")

# 获取多个因子
factors = ["pe_ratio", "pb_ratio", "roa", "roe"]
data = get_factor(stocks, factors, start_date="2024-01-01", end_date="2024-01-31")
```

---

## 一、估值类因子

| 因子名 | 中文名 | 计算方式 | 说明 |
|--------|--------|----------|------|
| `pe_ratio` | 市盈率 | 股价/每股收益 | 越低越便宜 |
| `pb_ratio` | 市净率 | 股价/每股净资产 | 越低越便宜 |
| `ps_ratio` | 市销率 | 股价/每股销售额 | 越低越便宜 |
| `pcf_ratio` | 市现率 | 股价/每股现金流 | 越低越便宜 |
| `ev` | 企业价值 | 市值+净债务 | 并购估值用 |
| `ebitda` | 息税折旧摊销前利润 | | 通用盈利指标 |
| `market_cap` | 总市值 | | 大盘/小盘区分 |
| `circulating_market_cap` | 流通市值 | | 实际可交易市值 |
| `capitalization` | 总股本 | | |
| `circulating_cap` | 流通股本 | | |

---

## 二、盈利能力因子

| 因子名 | 中文名 | 计算方式 | 说明 |
|--------|--------|----------|------|
| `roa` | 资产收益率 | 净利润/总资产 | 资产利用效率 |
| `roe` | 净资产收益率 | 净利润/净资产 | 股东回报率 |
| `roic` | 投入资本回报率 | | 资本使用效率 |
| `gross_profit_margin` | 毛利率 | (营收-成本)/营收 | 产品盈利能力 |
| `net_profit_margin` | 净利率 | 净利润/营收 | 最终盈利能力 |
| `operating_profit_margin` | 营业利润率 | 营业利润/营收 | 主业盈利能力 |
| `ebit` | 息税前利润 | | 剔除财务影响 |

---

## 三、成长能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `or_yoy` | 营业收入同比增长 | |
| `op_yoy` | 营业利润同比增长 | |
| `net_profit_yoy` | 净利润同比增长 | |
| `dt_net_profit_yoy` | 归母净利润同比增长 | |
| `ebit_yoy` | EBIT同比增长 | |
| `ocf_yoy` | 经营现金流同比增长 | |

---

## 四、现金流因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `net_operate_cash_flow` | 经营活动现金流净额 | 造血能力 |
| `net_invest_cash_flow` | 投资活动现金流净额 | 扩张/收缩 |
| `net_financing_cash_flow` | 筹资活动现金流净额 | 融资/分红 |
| `free_cash_flow` | 自由现金流 | 真实可分配现金 |

---

## 五、偿债能力因子

| 因子名 | 中文名 | 计算方式 | 说明 |
|--------|--------|----------|------|
| `current_ratio` | 流动比率 | 流动资产/流动负债 | 短期偿债能力 |
| `quick_ratio` | 速动比率 | (流动资产-存货)/流动负债 | 更严格的偿债能力 |
| `debt_to_asset_ratio` | 资产负债率 | 总负债/总资产 | 财务风险 |
| `equity_ratio` | 产权比率 | 总负债/净资产 | 财务杠杆 |

---

## 六、每股指标因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `eps` | 每股收益 | 净利润/总股本 |
| `bps` | 每股净资产 | 净资产/总股本 |
| `cfps` | 每股现金流 | 现金流/总股本 |
| `ocfps` | 每股经营现金流 | 经营现金流/总股本 |

---

## 七、资产负债因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `total_assets` | 总资产 | |
| `total_liability` | 总负债 | |
| `total_non_current_liability` | 非流动负债 | 长期债务 |
| `total_current_liability` | 流动负债 | 短期债务 |
| `total_owner_equities` | 所有者权益 | 净资产 |
| `book_value` | 账面价值 | |

---

## 八、营运能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `turnover_ratio` | 换手率 | 交易活跃度 |
| `operating_revenue` | 营业收入 | |
| `operating_cost` | 营业成本 | |
| `total_profit` | 利润总额 | |
| `net_profit` | 净利润 | |

---

## 九、其他因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `dividend_yield` | 股息率 | 年度分红/股价 |
| `beta` | Beta系数 | 系统风险 |
| `alpha` | Alpha系数 | 超额收益 |

---

## 十、RFScore 策略常用因子

本策略使用以下因子计算 RFScore：

| 因子名 | 用途 | 权重 |
|--------|------|------|
| `roa` | 盈利能力 | +1 |
| `net_operate_cash_flow` | 现金流质量 | +1 |
| `total_assets` | 资产规模（计算OCFOA） | - |
| `total_non_current_liability` | 杠杆变化 | +1 |
| `gross_profit_margin` | 毛利率变化 | +1 |
| `operating_revenue` | 周转率变化 | +1 |
| `pb_ratio` | 估值筛选 | 分组用 |

---

## 十一、JoinQuant 迁移速查

### valuation 模块

```python
# JoinQuant
valuation.pe_ratio
valuation.pb_ratio
valuation.market_cap

# RiceQuant
get_factor(stocks, "pe_ratio", ...)
get_factor(stocks, "pb_ratio", ...)
get_factor(stocks, "market_cap", ...)
```

### indicator 模块

```python
# JoinQuant
indicator.roa
indicator.roe
indicator.gross_profit_margin

# RiceQuant
get_factor(stocks, "roa", ...)
get_factor(stocks, "roe", ...)
get_factor(stocks, "gross_profit_margin", ...)
```

### cash_flow 模块

```python
# JoinQuant
cash_flow.net_operate_cash_flow

# RiceQuant
get_factor(stocks, "net_operate_cash_flow", ...)
```

### balance 模块

```python
# JoinQuant
balance.total_assets
balance.total_liability

# RiceQuant
get_factor(stocks, "total_assets", ...)
get_factor(stocks, "total_liability", ...)
```

---

## 十二、注意事项

1. **因子不存在**: 部分因子可能对某些股票不存在，需要 try-catch
2. **日期范围**: 使用 `start_date` 和 `end_date` 指定日期范围
3. **返回格式**: 返回 DataFrame 或 dict，通过键访问具体因子
4. **性能优化**: 一次获取多个因子比多次调用更高效

```python
# 推荐：一次获取多个因子
factors = ["pe_ratio", "pb_ratio", "roa", "roe"]
data = get_factor(stocks, factors, start_date, end_date)

# 不推荐：多次调用
pe = get_factor(stocks, "pe_ratio", start_date, end_date)
pb = get_factor(stocks, "pb_ratio", start_date, end_date)
roa = get_factor(stocks, "roa", start_date, end_date)
```

---

*参考文档: https://www.ricequant.com/api/python/chn#get_factor*
*最后更新: 2026-03-31*