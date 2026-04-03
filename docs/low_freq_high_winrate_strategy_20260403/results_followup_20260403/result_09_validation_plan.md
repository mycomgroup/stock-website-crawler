# 8因子短名单 RiceQuant 轻量验证方案

**版本**: v1.0  
**日期**: 2026-04-03  
**目标**: 确认短名单因子在 RiceQuant 上可工程化，3个新因子单因子有效

---

## 一、验证范围调整

### 1.1 短名单修正

原短名单 8 因子 → **修正为 7 因子**：

**剔除 FFScore**，原因：
- result_11 已验证：与 ROE/ROA 高度重叠（2指标完全相同，2指标高度相关）
- 预期改善 < 0.5%，增量贡献不显著
- 财报数据获取成本高（需5个指标跨期比较）

### 1.2 最终 7 因子

| 序号 | 因子 | 获取方式 | 验证优先级 |
|------|------|----------|------------|
| 1 | PE | `get_factor("pe_ratio")` | 基线，跳过 |
| 2 | PB | `get_factor("pb_ratio")` | 基线，跳过 |
| 3 | ROE | `get_factor("roe")` | 基线，跳过 |
| 4 | ROA | `get_factor("roa")` | 基线，跳过 |
| 5 | **STR（凸显性收益因子）** | 从日收益率手动计算 | **P0 - 最高** |
| 6 | **理想振幅 V(λ=25%)** | 从 OHLC 手动计算 | **P0 - 最高** |
| 7 | **二阶动量** | 从收盘价手动计算 | **P1 - 次高** |

---

## 二、验证策略

### 2.1 阶段划分

```
阶段 A（立即执行）: RiceQuant Notebook — 因子可计算性验证
  ├─ 验证 3 个新因子能否在 RiceQuant 上正确计算
  └─ 输出：每个因子的描述性统计 + 与基线因子的相关性

阶段 B（2周内）: RiceQuant Notebook — 单因子 IC 验证
  ├─ 对 3 个新因子分别做单因子 IC 测试
  └─ 输出：IC 均值、ICIR、胜率，与文献值对比

阶段 C（1个月内）: RiceQuant 策略编辑器 — 7因子 LR 回测
  ├─ 7因子逻辑回归 walk-forward 回测
  └─ 输出：与 4 因子基线对比的增量收益
```

### 2.2 当前执行：阶段 A

**目标**：确认 3 个新因子在 RiceQuant 上可计算，输出描述性统计。

**股票池**：中证500成分股（约500只）  
**时间窗口**：2024-01-01 ~ 2024-12-31（1年，足够验证可计算性）  
**平台**：RiceQuant Notebook（阶段2，推荐）

---

## 三、验证脚本

### 3.1 因子计算验证脚本

```python
# RiceQuant Notebook 格式 — 直接执行 + print
# 验证 3 个新因子在 RiceQuant 上的可计算性

print("=" * 70)
print("8因子短名单 — RiceQuant 可计算性验证")
print("=" * 70)

from rqdatac import *
import pandas as pd
import numpy as np
from datetime import datetime

# ============ 参数 ============
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
INDEX = "000905.XSHG"  # 中证500
LOOKBACK = 22  # 约1个月交易日

print(f"\n股票池: {INDEX}")
print(f"时间范围: {START_DATE} ~ {END_DATE}")
print(f"回望期: {LOOKBACK} 交易日")

# ============ 获取股票池 ============
print("\n[1/5] 获取股票池...")
stocks = index_components(INDEX, START_DATE)
print(f"  成分股数量: {len(stocks)}")

# 过滤：排除上市不足180天的
valid_stocks = []
for s in stocks:
    info = instruments(s)
    if info and info.listed_date:
        days_listed = (pd.Timestamp(START_DATE) - info.listed_date).days
        if days_listed > 180:
            valid_stocks.append(s)

print(f"  过滤后数量: {len(valid_stocks)}")

# 取前100只加速验证（Notebook模式性能限制）
test_stocks = valid_stocks[:100]
print(f"  测试数量: {len(test_stocks)}（加速验证）")

# ============ 基线因子验证 ============
print("\n[2/5] 验证基线因子（PE/PB/ROE/ROA）...")
try:
    factors = get_factor(test_stocks, ["pe_ratio", "pb_ratio", "roe", "roa"],
                         start_date=START_DATE, end_date=END_DATE)
    print(f"  ✅ 基线因子获取成功")
    print(f"  数据形状: {factors.shape}")
    print(f"  列: {factors.columns.tolist()}")
    
    # 描述性统计
    latest_date = factors.index.get_level_values(0).max()
    latest = factors.xs(latest_date, level=0)
    print(f"\n  最新日期 {latest_date} 的描述性统计:")
    for col in ["pe_ratio", "pb_ratio", "roe", "roa"]:
        if col in latest.columns:
            s = latest[col].dropna()
            print(f"    {col}: mean={s.mean():.4f}, std={s.std():.4f}, "
                  f"min={s.min():.4f}, max={s.max():.4f}, count={len(s)}")
    BASELINE_OK = True
except Exception as e:
    print(f"  ❌ 基线因子获取失败: {e}")
    BASELINE_OK = False

# ============ 获取价格数据（用于计算新因子） ============
print("\n[3/5] 获取价格数据...")
try:
    # 获取收盘价（用于STR和二阶动量）
    price_data = {}
    for stock in test_stocks:
        bars = history_bars(stock, LOOKBACK + 10, "1d", "close",
                           end_date=END_DATE, adjust_type="pre")
        if bars is not None and len(bars) >= LOOKBACK:
            price_data[stock] = bars
    
    print(f"  ✅ 价格数据获取成功")
    print(f"  有效股票数: {len(price_data)}")
    
    # 获取OHLC（用于理想振幅因子）
    ohlc_data = {}
    for stock in test_stocks:
        bars = history_bars(stock, LOOKBACK + 10, "1d",
                           ["open", "high", "low", "close"],
                           end_date=END_DATE, adjust_type="pre")
        if bars is not None and len(bars) >= LOOKBACK:
            ohlc_data[stock] = bars
    
    print(f"  ✅ OHLC数据获取成功")
    print(f"  有效股票数: {len(ohlc_data)}")
    PRICE_OK = True
except Exception as e:
    print(f"  ❌ 价格数据获取失败: {e}")
    PRICE_OK = False

# ============ 计算新因子 ============
if PRICE_OK:
    print("\n[4/5] 计算新因子...")
    
    # --- 5. STR（凸显性收益因子） ---
    print("\n  [5.1] 计算 STR 因子...")
    try:
        # 获取沪深300作为市场基准
        mkt_bars = history_bars("000300.XSHG", LOOKBACK + 10, "1d", "close",
                               end_date=END_DATE, adjust_type="pre")
        mkt_returns = np.diff(mkt_bars) / mkt_bars[:-1]
        mkt_returns = mkt_returns[-LOOKBACK:]  # 取最近LOOKBACK个
        
        str_values = {}
        for stock in test_stocks:
            if stock not in price_data:
                continue
            bars = price_data[stock][-LOOKBACK-1:]
            returns = np.diff(bars) / bars[:-1]
            returns = returns[-LOOKBACK:]
            
            if len(returns) != len(mkt_returns):
                min_len = min(len(returns), len(mkt_returns))
                returns = returns[-min_len:]
                mkt_ret = mkt_returns[-min_len:]
            else:
                mkt_ret = mkt_returns
            
            # STR = cov(w, r) where w = salience weight
            # salience = |r - mkt_ret| / (|r| + |mkt_ret| + theta)
            theta = 0.001
            salience = np.abs(returns - mkt_ret) / (np.abs(returns) + np.abs(mkt_ret) + theta)
            
            # rank by salience (highest salience = rank 1)
            salience_ranks = np.argsort(np.argsort(-salience)) + 1  # 1-based rank
            delta = 0.7  # cognitive parameter
            
            # weight = delta^rank / sum(delta^rank * pi)
            weights = delta ** salience_ranks
            weights = weights / (weights.mean())  # normalize so E[w] = 1
            
            # STR = cov(w, r)
            str_val = np.cov(weights, returns)[0, 1]
            str_values[stock] = str_val
        
        str_series = pd.Series(str_values)
        print(f"    ✅ STR 计算成功")
        print(f"    覆盖股票数: {len(str_series)}")
        print(f"    描述性统计:")
        print(f"      mean={str_series.mean():.6f}, std={str_series.std():.6f}")
        print(f"      min={str_series.min():.6f}, max={str_series.max():.6f}")
        print(f"      median={str_series.median():.6f}")
        STR_OK = True
    except Exception as e:
        print(f"    ❌ STR 计算失败: {e}")
        import traceback
        traceback.print_exc()
        STR_OK = False
    
    # --- 6. 理想振幅因子 V(λ=25%) ---
    print("\n  [6.1] 计算理想振幅因子 V(λ=25%)...")
    try:
        LAMBDA = 0.25
        amplitude_values = {}
        
        for stock in test_stocks:
            if stock not in ohlc_data:
                continue
            bars = ohlc_data[stock][-LOOKBACK:]
            
            # 计算每日振幅 = (high - low) / prev_close
            highs = bars["high"].values
            lows = bars["low"].values
            closes = bars["close"].values
            
            if len(closes) < 2:
                continue
            
            prev_closes = closes[:-1]
            current_highs = highs[1:]
            current_lows = lows[1:]
            
            amplitude = (current_highs - current_lows) / prev_closes
            
            if len(amplitude) < LOOKBACK * 0.5:
                continue
            
            # 按价格分位切割
            mid_prices = (current_highs + current_lows) / 2
            price_threshold_high = np.percentile(mid_prices, 100 - LAMBDA * 100)
            price_threshold_low = np.percentile(mid_prices, LAMBDA * 100)
            
            # 高价态振幅 vs 低价态振幅
            high_price_mask = mid_prices >= price_threshold_high
            low_price_mask = mid_prices <= price_threshold_low
            
            if high_price_mask.sum() > 0 and low_price_mask.sum() > 0:
                v_high = amplitude[high_price_mask].mean()
                v_low = amplitude[low_price_mask].mean()
                # 理想振幅 = V_high - V_low（标准化后作差）
                ideal_amplitude = (v_high - v_low) / (amplitude.std() + 1e-8)
                amplitude_values[stock] = ideal_amplitude
        
        amp_series = pd.Series(amplitude_values)
        print(f"    ✅ 理想振幅因子计算成功")
        print(f"    覆盖股票数: {len(amp_series)}")
        print(f"    描述性统计:")
        print(f"      mean={amp_series.mean():.6f}, std={amp_series.std():.6f}")
        print(f"      min={amp_series.min():.6f}, max={amp_series.max():.6f}")
        print(f"      median={amp_series.median():.6f}")
        AMP_OK = True
    except Exception as e:
        print(f"    ❌ 理想振幅因子计算失败: {e}")
        import traceback
        traceback.print_exc()
        AMP_OK = False
    
    # --- 7. 二阶动量 ---
    print("\n  [7.1] 计算二阶动量因子...")
    try:
        momentum_values = {}
        
        for stock in test_stocks:
            if stock not in price_data:
                continue
            bars = price_data[stock]
            
            if len(bars) < 40:
                continue
            
            closes = bars
            
            # 一阶动量（短期和长期）
            short_window = 5
            long_window = 20
            
            short_mom = closes[-1] / closes[-short_window-1] - 1
            long_mom = closes[-1] / closes[-long_window-1] - 1
            
            # 二阶动量 = 动量的变化率（加速度）
            # 或者用研报公式：EWMA(当前动量 - 过去动量)
            mom_series = []
            for i in range(long_window, len(closes)):
                mom_i = closes[i] / closes[i-long_window] - 1
                mom_series.append(mom_i)
            
            if len(mom_series) < 10:
                continue
            
            # 二阶动量 = 最新动量 - 过去动量的EWMA
            mom_arr = np.array(mom_series)
            ewma = np.average(mom_arr[:-1], weights=np.exp(np.linspace(-1, 0, len(mom_arr)-1)))
            second_order_mom = mom_arr[-1] - ewma
            
            momentum_values[stock] = second_order_mom
        
        mom_series = pd.Series(momentum_values)
        print(f"    ✅ 二阶动量因子计算成功")
        print(f"    覆盖股票数: {len(mom_series)}")
        print(f"    描述性统计:")
        print(f"      mean={mom_series.mean():.6f}, std={mom_series.std():.6f}")
        print(f"      min={mom_series.min():.6f}, max={mom_series.max():.6f}")
        print(f"      median={mom_series.median():.6f}")
        MOM_OK = True
    except Exception as e:
        print(f"    ❌ 二阶动量因子计算失败: {e}")
        import traceback
        traceback.print_exc()
        MOM_OK = False

# ============ 相关性分析 ============
print("\n[5/5] 因子相关性分析...")
try:
    # 收集所有因子值
    all_factors = {}
    
    if BASELINE_OK:
        latest_date = factors.index.get_level_values(0).max()
        latest = factors.xs(latest_date, level=0)
        for col in ["pe_ratio", "pb_ratio", "roe", "roa"]:
            if col in latest.columns:
                all_factors[col] = latest[col]
    
    if STR_OK:
        all_factors["STR"] = str_series
    
    if AMP_OK:
        all_factors["ideal_amplitude"] = amp_series
    
    if MOM_OK:
        all_factors["second_order_momentum"] = mom_series
    
    # 构建因子矩阵
    factor_df = pd.DataFrame(all_factors)
    factor_df = factor_df.dropna()
    
    print(f"\n  有效样本数: {len(factor_df)}")
    print(f"  因子列: {factor_df.columns.tolist()}")
    
    # 秩相关矩阵
    corr_matrix = factor_df.rank().corr()
    print(f"\n  因子秩相关矩阵:")
    print(corr_matrix.round(3).to_string())
    
    # 检查高相关因子对（>0.5）
    print(f"\n  高相关因子对（|r| > 0.5）:")
    high_corr_found = False
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            col_i = corr_matrix.columns[i]
            col_j = corr_matrix.columns[j]
            val = corr_matrix.iloc[i, j]
            if abs(val) > 0.5:
                print(f"    {col_i} vs {col_j}: r = {val:.3f}")
                high_corr_found = True
    
    if not high_corr_found:
        print(f"    无高相关因子对 ✅")
    
except Exception as e:
    print(f"  ❌ 相关性分析失败: {e}")
    import traceback
    traceback.print_exc()

# ============ 总结 ============
print("\n" + "=" * 70)
print("【验证结论】")
print("=" * 70)

results = {
    "基线因子(PE/PB/ROE/ROA)": BASELINE_OK,
    "STR因子": STR_OK if 'STR_OK' in dir() else False,
    "理想振幅因子": AMP_OK if 'AMP_OK' in dir() else False,
    "二阶动量因子": MOM_OK if 'MOM_OK' in dir() else False,
}

all_ok = True
for name, ok in results.items():
    status = "✅ 通过" if ok else "❌ 失败"
    print(f"  {name}: {status}")
    if not ok:
        all_ok = False

print()
if all_ok:
    print("结论: 所有7因子均可在 RiceQuant 上计算，进入阶段B（单因子IC验证）")
else:
    print("结论: 部分因子计算失败，需排查后再进入阶段B")

print("\n验证完成!")
```

---

## 四、运行方式

### 4.1 平台选择

**RiceQuant Notebook**（阶段2，推荐）

- 因子简单（PE/PB/ROE/ROE 直取 + 3个手动计算因子）
- Notebook 格式快速验证可计算性
- Session 自动管理

### 4.2 运行命令

```bash
# 1. 将上述脚本保存为策略文件
# 2. 进入 RiceQuant skill 目录
cd skills/ricequant_strategy

# 3. 运行验证脚本
node run-strategy.js --strategy /path/to/factor_validation.py --create-new --timeout-ms 300000

# 4. 查看结果
cat data/ricequant-notebook-result-*.json
```

### 4.3 预期输出

成功时应看到：
1. 基线因子描述性统计（PE/PB/ROE/ROA）
2. STR 因子描述性统计（mean ≈ 1.15, 有正有负）
3. 理想振幅因子描述性统计（有正有负）
4. 二阶动量因子描述性统计（有正有负）
5. 7因子秩相关矩阵
6. 高相关因子对检查

---

## 五、阶段 B 规划（单因子 IC 验证）

阶段 A 通过后，进入阶段 B：

| 因子 | 验证目标 | 文献参考值 | 通过标准 |
|------|----------|------------|----------|
| STR | IC均值 | -0.065（全A） | IC < -0.03 |
| 理想振幅 V(λ=25%) | IC均值 | -0.067（全A） | IC < -0.03 |
| 二阶动量 | IC均值 | 0.044（行业） | IC > 0.02（个股可能衰减） |

**注意**：二阶动量原报告在行业层面测试，个股层面预期 IC 会衰减，通过标准放宽。

---

## 六、阶段 C 规划（7因子 LR 回测）

阶段 B 通过后，进入阶段 C：

- 使用 RiceQuant 策略编辑器（阶段3）
- Walk-forward 回测，2020-01-01 ~ 2025-12-31
- 对比 4 因子基线 vs 7 因子模型
- 目标：确认新增 3 因子是否带来显著增量收益

---

**决策树**：

```
阶段 A（可计算性）
  ├─ 全部通过 → 进入阶段 B
  └─ 部分失败 → 排查失败因子，修复后重试

阶段 B（单因子 IC）
  ├─ 3 因子均通过 → 进入阶段 C（7因子回测）
  ├─ 2 因子通过 → 进入阶段 C（6因子回测）
  └─ 1 因子通过 → 重新评估短名单

阶段 C（7因子 LR 回测）
  ├─ 7因子显著优于4因子 → 确认短名单
  ├─ 7因子与4因子无显著差异 → 缩减到5-6因子
  └─ 7因子劣于4因子 → 回退到4因子基线
```
