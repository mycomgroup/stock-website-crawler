# QuantsPlaybook 策略验证进度

> 更新时间: 2026-04-03
> 验证框架: RiceQuant 策略编辑器 API
> 策略目录: quantsplaybook_validation/strategies/

---

## 验证进度

### C-择时类（指数择时）

| # | 策略文件 | 来源 | 状态 | 回测ID |
|---|----------|------|------|--------|
| 01 | 01_icu_ma.py | ICU均线 | ✅ 完成 | 7965369 |
| 02 | 02_time_varying_sharpe.py | 时变夏普 | ✅ 完成 | 7965353 |
| 03 | 03_diffusion_indicator.py | 扩散指标 | ✅ 完成 | 7965351 |
| 04 | 04_ma_channel.py | 均线通道 | ✅ 完成 | 7965376 |
| 05 | 05_rsrs_optimized.py | RSRS择时 | ✅ 完成 | 7965363 |
| 06 | 06_qrs.py | QRS择时 | ✅ 完成 | 7965415 |
| 07 | 07_low_lag_trend.py | 低延迟趋势线 | ✅ 完成 | 7965416 |
| 08 | 08_bull_bear_indicator.py | 牛熊指标 | ✅ 完成 | 7965419 |
| 09 | 09_price_volume_resonance.py | 价量共振 | 🔄 重试中 | 7965424(失败) |
| 10 | 10_alligator.py | 鳄鱼线 | 🔄 重试中 | 7965430(失败) |
| 11 | 11_unidirectional_volatility.py | 单向波动差值 | ⏳ 待验证 | - |
| 12 | 12_higher_moments.py | 指数高阶矩 | ⏳ 待验证 | - |
| 13 | 13_herd_effect.py | 羊群效应CCK | ⏳ 待验证 | - |
| 14 | 14_trend_momentum.py | 趋与势 | ⏳ 待验证 | - |
| 15 | 15_northbound_fund.py | 北向资金 | ⏳ 待验证 | - |
| 16 | 16_volatility_factor.py | 波动率因子择时 | ⏳ 待验证 | - |
| 17 | 17_point_efficiency.py | 点位效率 | ⏳ 待验证 | - |
| 18 | 18_investor_sentiment.py | 投资者情绪 | ⏳ 待验证 | - |
| 19 | 19_new_high_low.py | 新高新低 | ⏳ 待验证 | - |
| 20 | 20_wavelet_analysis.py | 小波分析 | ⏳ 待验证 | - |
| 21 | 21_cvix.py | 中国VIX | ⏳ 待验证 | - |
| 22 | 22_distribution_model.py | 特征分布建模 | ⏳ 待验证 | - |
| 23 | 23_trader_company.py | Trader-Company | ⏳ 待验证 | - |
| 24 | 24_pattern_recognition.py | 技术分析框架一 | ⏳ 待验证 | - |
| 25 | 25_hht_model.py | HHT模型 | ⏳ 待验证 | - |
| 26 | 26_etf_intraday_momentum.py | ETF日内动量 | ⏳ 待验证 | - |
| 27 | 27_industry_top_bottom.py | 行业顶底信号 | ⏳ 待验证 | - |
| 28 | 28_rounding_bottom_pattern.py | 圆弧底形态 | ⏳ 待验证 | - |

### B-因子构建类（选股+月度调仓）

| # | 策略文件 | 来源 | 状态 | 回测ID |
|---|----------|------|------|--------|
| 29 | 29_high_quality_momentum.py | 高质量动量因子 | ⏳ 待验证 | - |
| 30 | 30_smart_money_v2.py | 聪明钱因子2.0 | ⏳ 待验证 | - |
| 31 | 31_momentum_a_share.py | A股动量因子 | ⏳ 待验证 | - |
| 32 | 32_chip_distribution_factor.py | 筹码分布因子 | ⏳ 待验证 | - |
| 33 | 33_disposal_effect_factor.py | 处置效应CGO | ⏳ 待验证 | - |
| 34 | 34_cpv_factor.py | 高频价量相关性CPV | ⏳ 待验证 | - |
| 35 | 35_industry_rotation_pv.py | 行业量价轮动 | ⏳ 待验证 | - |
| 36 | 36_gold_stock_enhanced.py | 金股增强 | ⏳ 待验证 | - |
| 37 | 37_buy_sell_pressure.py | 买卖压力因子 | ⏳ 待验证 | - |
| 38 | 38_overnight_intraday_network.py | 隔夜日间网络因子 | ⏳ 待验证 | - |
| 39 | 39_fund_overweight_factor.py | 基金超配因子 | ⏳ 待验证 | - |
| 40 | 40_stock_network_centrality.py | 股票网络中心度 | ⏳ 待验证 | - |
| 41 | 41_fund_manager_alpha.py | 基金经理超额 | ⏳ 待验证 | - |
| 42 | 42_enterprise_lifecycle.py | 企业生命周期 | ⏳ 待验证 | - |
| 43 | 43_upper_lower_shadow.py | 上下影线因子 | ⏳ 待验证 | - |
| 44 | 44_pure_volatility_factor.py | 纯真波动率IVOL | ⏳ 待验证 | - |
| 45 | 45_salience_str_factor.py | 凸显理论STR | ⏳ 待验证 | - |
| 46 | 46_factor_timing.py | 因子择时 | ⏳ 待验证 | - |
| 47 | 47_revisit_momentum.py | 再论动量因子 | ⏳ 待验证 | - |
| 48 | 48_amplitude_hidden_structure.py | 振幅隐藏结构 | ⏳ 待验证 | - |
| 49 | 49_apm_factor.py | APM因子 | ⏳ 待验证 | - |
| 50 | 50_team_coin_momentum.py | 球队硬币因子 | ⏳ 待验证 | - |
| 51 | 51_microstructure_reversal.py | 微观结构反转 | ⏳ 待验证 | - |
| 52 | 52_multifactor_index_enhance.py | 多因子指数增强 | ⏳ 待验证 | - |

### A-量化基本面（财务选股）

| # | 策略文件 | 来源 | 状态 | 回测ID |
|---|----------|------|------|--------|
| 53 | 53_ffscore_selection.py | 华泰FFScore | ⏳ 待验证 | - |
| 54 | 54_sw_cashflow_selection.py | 申万超额现金流 | ⏳ 待验证 | - |

### D-组合优化

| # | 策略文件 | 来源 | 状态 | 回测ID |
|---|----------|------|------|--------|
| 55 | 55_de_portfolio_optimization.py | DE算法组合优化 | ⏳ 待验证 | - |
| 56 | 56_mlt_tsmom.py | MLT-TSMOM | ⏳ 待验证 | - |

---

## 策略分类说明

- **C-择时类（01-28）**：指数择时策略，标的为沪深300/中证500等宽基指数，日频调仓
- **B-因子构建类（29-52）**：选股因子策略，月度调仓，持仓30-50只股票
- **A-量化基本面（53-54）**：财务指标选股，季度调仓，需要 fundamentals 数据
- **D-组合优化（55-56）**：ETF组合优化，季度调仓

> 注：B/A类策略中，部分原版使用 JoinQuant/qlib 专有API（如 `jqdata`、`jqfactor`），
> 已转换为 RiceQuant 兼容的日线量价数据实现，核心逻辑保持一致。

---

## 已验证结果摘要

| 策略 | Sharpe | MaxDD | Alpha | 评价 |
|------|--------|-------|-------|------|
| RSRS择时指标 | **0.28** | 23.7% | 3.2% | ✅ 唯一有效 |
| 牛熊指标 | -0.09 | 25.8% | -0.93% | ⚠️ 接近零 |
| 均线通道 | -0.17 | 29.4% | -1.98% | ⚠️ 需优化 |
| 低延迟趋势线 | -0.11 | 29.2% | -1.16% | ⚠️ 需优化 |
| QRS择时 | -0.11 | 33.0% | -1.41% | ⚠️ 需优化 |
| 时变夏普 | -0.10 | 45.0% | -1.7% | ⚠️ 需优化 |
| ICU均线 | -0.44 | 48.8% | -6.87% | ❌ 需重构 |
| 扩散指标 | -0.67 | 58.7% | -8.9% | ❌ 需重构 |

---

## 关键发现

1. **RSRS择时策略**是10年检验中唯一正夏普策略
2. **牛熊指标**回撤最小(25.8%)，接近零夏普
3. **扩散指标、ICU均线**回撤超45%，风险过大
4. 多数策略在10年检验中表现不佳，研报参数需适配优化

---

## 使用说明

### 运行单个策略验证
```bash
cd /Users/yuping/Downloads/git/jk2bt-main/lib/stock-website-crawler/skills/ricequant_strategy
node run-skill.js --id 2416771 --file quantsplaybook_validation/strategies/01_icu_ma.py --start 2015-01-01 --end 2024-12-31
```

### 查看结果
```bash
ls -t data/ricequant-backtest-*.json | head -1 | xargs cat
```

---

## RiceQuant API限制

- **并发限制**: 最多3个同时运行
- **超时问题**: API高峰期可能504错误
- **建议**: 分批顺序执行，避免并发