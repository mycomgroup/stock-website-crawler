# RFScore7 + PB10% 策略回测报告

**日期**: 2026-04-01
**平台**: RiceQuant
**回测期间**: 2023-01-01 至 2024-06-30
**初始资金**: 100,000 元

---

## 一、背景

### 目标
测试增强策略（四档仓位）是否优于原始策略（等权）：
- **原始策略**: 所有股票等权分配
- **增强策略**: 根据 RFScore 分配仓位
  - RFScore=2: 满仓（100%）
  - RFScore=1: 七成仓（70%）

### 策略逻辑
1. **股票池**: 沪深300 + 中证500
2. **筛选条件**: 
   - RFScore 基于 ROA 和 ROE
   - PB 分组低估值（最低10%）
3. **市场风控**: 市场宽度 < 25% 时减仓，< 15% 时清仓

---

## 二、RiceQuant API 修复

### 发现的问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `get_factor()` 报错 | 不接受 `start_date`/`end_date` 关键字参数 | 改用位置参数或省略日期 |
| 因子名称错误 | `roa`、`roe` 不存在 | 使用 `return_on_asset`、`return_on_equity` |
| `bar_dict` 无个股数据 | RiceQuant 不预加载个股数据 | 使用 `history_bars()` 替代 |
| `context.portfolio.available_cash` 报错 | 属性名不同 | 改用 `context.portfolio.cash` |
| `instruments(stock)` 循环慢 | 单独调用太慢 | 预加载 `all_instruments()` 批量处理 |

### RiceQuant 正确 API

```python
# 获取因子
factor_data = get_factor(stocks, ["return_on_asset", "return_on_equity", "pb_ratio"])

# 获取历史价格
hist = history_bars(stock, 20, "1d", "close")

# 指数成分股
stocks = index_components("000300.XSHG")

# 交易
order_target_value(stock, target_value)

# 定时任务
scheduler.run_monthly(rebalance, monthday=1)
```

---

## 三、回测结果

### 结果对比

| 指标 | 原始策略 | 增强策略 | 差异 |
|------|----------|----------|------|
| **Total Return** | 6.69% | **7.30%** | +0.61% |
| **Annual Return** | 17.71% | **19.44%** | +1.73% |
| **Max Drawdown** | **10.61%** | 10.84% | -0.23% |
| **Sharpe Ratio** | 0.93 | **0.97** | +0.04 |
| **Alpha** | 19.86% | **20.85%** | +0.99% |
| **Beta** | 0.68 | 0.69 | +0.01 |
| **Sortino** | 1.42 | 1.48 | +0.06 |
| **Information Ratio** | 1.94 | 2.01 | +0.07 |

### 结论

✅ **增强策略优于原始策略**

- 收益提升 0.61%
- 年化收益提升 1.73%
- Sharpe 提升 0.04
- Alpha 提升 0.99%
- 回撤仅增加 0.23%

四档仓位策略（RFScore=2 满仓，RFScore=1 七成仓）有效提升了风险调整后收益。

---

## 四、文件说明

```
rfscore_backtest_20260401/
├── README.md                          # 本文档
├── API_FIX_NOTES.md                   # RiceQuant API 修复记录
├── strategies/
│   ├── rfscore7_pb10_final_v2.py      # 原始策略（等权）
│   └── rfscore7_pb10_enhanced_v2.py   # 增强策略（四档仓位）
├── results/
│   ├── original_strategy.json         # 原始策略回测结果
│   └── enhanced_strategy.json         # 增强策略回测结果
└── tools/
    ├── test-backtest.js               # 回测运行脚本
    ├── ricequant-client.js            # RiceQuant API 客户端
    └── auto-login.js                  # 自动登录脚本
```

---

## 五、后续工作

1. **JoinQuant API 修复**: 用户要求暂不处理
2. **更长回测期间**: 可扩展至 2018-2024 测试完整牛熊周期
3. **参数优化**: 可测试不同的仓位比例（如 80%/60%）
4. **实盘验证**: 模拟盘测试

---

## 六、技术要点

### RiceQuant vs JoinQuant API 对照

| 功能 | JoinQuant | RiceQuant |
|------|-----------|-----------|
| 入口函数 | `initialize(context)` | `init(context)` |
| 定时任务 | `run_monthly(func, 1)` | `scheduler.run_monthly(func, monthday=1)` |
| 指数成分股 | `get_index_stocks()` | `index_components()` |
| 历史价格 | `get_price()` | `history_bars()` |
| 因子数据 | `get_factor_values()` | `get_factor()` |
| 当前数据 | `get_current_data()` | `bar_dict` 参数传入 |
| 可用现金 | `portfolio.available_cash` | `portfolio.cash` |

### 注意事项

1. RiceQuant 的 `bar_dict` 不包含个股数据，需要用 `history_bars()`
2. 因子名称使用全称（如 `return_on_asset` 而非 `roa`）
3. `get_factor()` 不接受日期参数，返回当前日期数据
4. 预加载 `all_instruments()` 避免循环调用 `instruments()`

---

**报告生成时间**: 2026-04-01