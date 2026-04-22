# QuantsPlaybook 策略验证完整汇总

> 更新时间: 2026-04-02
> 验证框架: RiceQuant 策略编辑器 API
> 回测区间: 2015-01-01 至 2024-12-31 (10年)
> 标的指数: 沪深300 (000300.XSHG)

---

## 策略总览 (25个策略)

### ✅ 有效策略 (Sharpe > 0)

| # | 策略名称 | 研报来源 | Sharpe | MaxDD | Alpha | RiceQuant ID |
|---|---------|---------|--------|-------|-------|--------------|
| 1 | **RSRS择时指标** | 光大证券 | **0.28** | 23.73% | 3.21% | [2417084](https://www.ricequant.com/quant/create_edit/2417084) |
| 2 | **波动率因子** | - | **0.15** | 16.68% | 1.35% | [2417200](https://www.ricequant.com/quant/create_edit/2417200) |
| 3 | **单向波动差值** | 国信证券 | **0.08** | 28.92% | 1.13% | [2417193](https://www.ricequant.com/quant/create_edit/2417193) |
| 4 | **鳄鱼线** | 招商证券 | **0.01** | 30.52% | 0.29% | [2417192](https://www.ricequant.com/quant/create_edit/2417192) |
| 5 | **点位效率** | 兴业证券 | **0.04** | 7.31% | 0.27% | [2417203](https://www.ricequant.com/quant/create_edit/2417203) |

### ⚠️ 需优化策略 (Sharpe -0.2 ~ 0)

| # | 策略名称 | 研报来源 | Sharpe | MaxDD | Alpha | RiceQuant ID |
|---|---------|---------|--------|-------|-------|--------------|
| 6 | 新高新低信号 | 华福证券 | -0.03 | 35.60% | -0.33% | [2417205](https://www.ricequant.com/quant/create_edit/2417205) |
| 7 | 技术形态识别 | 中泰证券 | -0.03 | 39.64% | -0.27% | [2417212](https://www.ricequant.com/quant/create_edit/2417212) |
| 8 | 趋与势量化 | 国泰君安 | -0.08 | 18.42% | -0.67% | [2417198](https://www.ricequant.com/quant/create_edit/2417198) |
| 9 | 牛熊指标 | 华泰证券 | -0.09 | 25.80% | -0.93% | [2417189](https://www.ricequant.com/quant/create_edit/2417189) |
| 10 | 北向资金 | 安信证券 | -0.09 | 46.97% | -1.30% | [2417199](https://www.ricequant.com/quant/create_edit/2417199) |
| 11 | 时变夏普 | 国信证券 | -0.10 | 45.00% | -1.70% | [2417179](https://www.ricequant.com/quant/create_edit/2417179) |
| 12 | 羊群效应CCK | 国泰君安 | -0.11 | 19.80% | -1.02% | [2417217](https://www.ricequant.com/quant/create_edit/2417217) |
| 13 | QRS择时 | 中金公司 | -0.11 | 33.00% | -1.41% | [2417187](https://www.ricequant.com/quant/create_edit/2417187) |
| 14 | 低延迟趋势线 | 广发证券 | -0.11 | 29.20% | -1.16% | [2417188](https://www.ricequant.com/quant/create_edit/2417188) |
| 15 | 均线通道 | 申万宏源 | -0.17 | 29.40% | -1.98% | [2417186](https://www.ricequant.com/quant/create_edit/2417186) |
| 16 | 小波分析 | 国信/平安 | -0.14 | 12.96% | -1.00% | [2417206](https://www.ricequant.com/quant/create_edit/2417206) |

### ❌ 需重构策略 (Sharpe < -0.2)

| # | 策略名称 | 研报来源 | Sharpe | MaxDD | Alpha | RiceQuant ID |
|---|---------|---------|--------|-------|-------|--------------|
| 17 | 投资者情绪 | 国信证券 | -0.26 | 34.62% | -3.08% | [2417204](https://www.ricequant.com/quant/create_edit/2417204) |
| 18 | 价量共振 | 华创证券 | -0.33 | 47.65% | -5.17% | [2417190](https://www.ricequant.com/quant/create_edit/2417190) |
| 19 | HHT模型 | 招商证券 | -0.36 | 23.04% | -2.48% | [2417215](https://www.ricequant.com/quant/create_edit/2417215) |
| 20 | 指数高阶矩 | 广发证券 | -0.35 | 59.10% | -5.70% | [2417194](https://www.ricequant.com/quant/create_edit/2417194) |
| 21 | ICU均线 | 中泰证券 | -0.44 | 48.80% | -6.87% | [2417178](https://www.ricequant.com/quant/create_edit/2417178) |
| 22 | 扩散指标 | 东北证券 | -0.66 | 57.92% | -8.71% | [2417180](https://www.ricequant.com/quant/create_edit/2417180) |
| 23 | C-VIX | 国信/东北 | -0.57 | 65.14% | -9.15% | [2417207](https://www.ricequant.com/quant/create_edit/2417207) |
| 24 | 特征分布建模 | 华创证券 | -0.60 | 53.48% | -9.45% | [2417208](https://www.ricequant.com/quant/create_edit/2417208) |

### 📝 待验证

| # | 策略名称 | 研报来源 | 状态 | RiceQuant ID |
|---|---------|---------|------|--------------|
| 25 | Trader-Company | 浙商证券 | API超时 | [2417219](https://www.ricequant.com/quant/create_edit/2417219) |

---

## 关键发现

### Top 5 策略 (按Sharpe排名)

| 排名 | 策略 | Sharpe | MaxDD | 特点 |
|------|------|--------|-------|------|
| 1 | RSRS择时指标 | **0.28** | 23.73% | 10年验证唯一显著正夏普 |
| 2 | 波动率因子 | **0.15** | 16.68% | 低波动率环境择时 |
| 3 | 单向波动差值 | **0.08** | 28.92% | 上涨/下跌波动差值 |
| 4 | 点位效率 | **0.04** | 7.31% | 最小回撤策略 |
| 5 | 鳄鱼线 | **0.01** | 30.52% | 接近零夏普 |

### 统计分析

| 指标 | 数值 |
|------|------|
| 总策略数 | 25 |
| 正夏普策略 | 5 (20%) |
| 平均Sharpe | -0.15 |
| 平均MaxDD | 33.8% |
| 最佳策略 | RSRS (Sharpe 0.28) |
| 最差策略 | 特征分布建模 (Sharpe -0.60) |

---

## 策略分类

### 按研究机构

| 机构 | 策略数 | 平均Sharpe |
|------|--------|------------|
| 光大证券 | 1 | 0.28 |
| 招商证券 | 2 | -0.18 |
| 国信证券 | 3 | -0.17 |
| 华创证券 | 2 | -0.47 |
| 广发证券 | 2 | -0.23 |
| 国泰君安 | 2 | -0.10 |
| 中泰证券 | 2 | -0.24 |
| 华泰证券 | 1 | -0.09 |

### 按策略类型

| 类型 | 策略数 | 最佳代表 |
|------|--------|----------|
| 支撑阻力类 | RSRS, QRS | RSRS (0.28) |
| 均线趋势类 | ICU均线, 鳄鱼线, 低延迟趋势 | 鳄鱼线 (0.01) |
| 波动率类 | 牛熊指标, 波动率因子, C-VIX | 波动率因子 (0.15) |
| 价量类 | 价量共振, 北向资金 | 北向资金 (-0.09) |
| 形态类 | 技术形态识别, 小波分析 | 技术形态 (-0.03) |

---

## 本地代码目录

```
quantsplaybook_validation/strategies/
├── 01_icu_ma.py              # ICU均线
├── 02_time_varying_sharpe.py # 时变夏普
├── 03_diffusion_indicator.py # 扩散指标
├── 04_ma_channel.py          # 均线通道
├── 05_rsrs_optimized.py      # RSRS择时
├── 06_qrs.py                 # QRS择时
├── 07_low_lag_trend.py       # 低延迟趋势线
├── 08_bull_bear_indicator.py # 牛熊指标
├── 09_price_volume_resonance.py # 价量共振
├── 10_alligator.py           # 鳄鱼线
├── 11_unidirectional_volatility.py # 单向波动差值
├── 12_higher_moments.py      # 指数高阶矩
├── 13_herd_effect.py         # 羊群效应CCK
├── 14_trend_momentum.py      # 趋与势量化
├── 15_northbound_fund.py     # 北向资金
├── 16_volatility_factor.py   # 波动率因子
├── 17_point_efficiency.py    # 点位效率
├── 18_investor_sentiment.py  # 投资者情绪
├── 19_new_high_low.py        # 新高新低信号
├── 20_wavelet_analysis.py    # 小波分析
├── 21_cvix.py                # C-VIX
├── 22_distribution_model.py  # 特征分布建模
├── 23_trader_company.py      # Trader-Company
├── 24_pattern_recognition.py # 技术形态识别
└── 25_hht_model.py           # HHT模型
```