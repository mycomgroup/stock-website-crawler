# 任务03：二板接力卖出规则设计与测试 - 标准流程

**任务编号**: 03
**创建日期**: 2026-04-01
**执行方式**: 四阶段流程（优先 RiceQuant Notebook）

---

## 一、策略阶段判断

### 阶段判定

| 判断项 | 结果 |
|--------|------|
| 策略类型 | 新策略开发（卖出规则测试） |
| 因子复杂度 | **简单因子**（市值、涨停数、涨跌幅等基础因子） |
| 平台选择 | **RiceQuant Notebook**（阶段2）⭐ |
| 开发阶段 | 阶段2：新策略开发 |

**判定依据**：
- ✅ 因子简单：仅使用市值、涨停数、开盘价、收盘价等基础数据
- ✅ 新策略开发：测试不同卖出规则的效果
- ✅ 推荐平台：**RiceQuant Notebook**（Session自动管理，快速验证）

---

## 二、四阶段执行计划

### 阶段2：RiceQuant Notebook 快速验证（当前阶段）⭐

**目标**：快速测试不同卖出规则的效果

**执行步骤**：
```bash
# 1. 进入 RiceQuant Skill 目录
cd skills/ricequant_strategy

# 2. 运行测试脚本（按顺序）
# 2.1 卖出时机测试（预计5分钟）
node run-strategy.js --strategy ./examples/task03/sell_timing_test.py --create-new --timeout-ms 300000

# 2.2 止盈规则测试（预计5分钟）
node run-strategy.js --strategy ./examples/task03/profit_target_test.py --create-new --timeout-ms 300000

# 2.3 止损规则测试（预计5分钟）
node run-strategy.js --strategy ./examples/task03/stop_loss_test.py --create-new --timeout-ms 300000

# 2.4 持仓周期测试（预计5分钟）
node run-strategy.js --strategy ./examples/task03/holding_period_test.py --create-new --timeout-ms 300000

# 2.5 熔断规则测试（预计5分钟）
node run-strategy.js --strategy ./examples/task03/circuit_breaker_test.py --create-new --timeout-ms 300000

# 3. 查看结果
cat data/ricequant-notebook-result-*.json
```

**预期时间**：约25分钟（5个测试 × 5分钟）

### 阶段3：RiceQuant 策略编辑器完整回测（后续）

**目标**：获得完整的风险指标

**执行步骤**：
```bash
# 1. 进入目录
cd skills/ricequant_strategy

# 2. 查看策略列表
node list-strategies.js

# 3. 上传并运行策略
node run-skill.js --id <strategyId> --file ./strategy.py --start 2021-01-01 --end 2024-12-31

# 4. 获取完整报告
node fetch-report.js --id <backtestId> --full
```

### 阶段4：JoinQuant Strategy 最终验证（后续）

**目标**：最权威的验证结果

**执行方式**：在 JoinQuant 网页平台运行

---

## 三、RiceQuant Notebook 格式要求

### 格式规范

```python
# ✅ 正确格式（Notebook格式）
print("=== 策略测试开始 ===")

try:
    # 1. 获取数据
    date = "2024-03-20"
    stocks = all_instruments("CS")  # RiceQuant API
    
    # 2. 选股逻辑
    selected = your_logic(stocks)
    print(f"选中股票: {len(selected)}")
    
    # 3. 计算收益
    results = []
    for stock in selected:
        ret = calculate_return(stock, date)
        results.append(ret)
    
    # 4. 输出结果
    print(f"平均收益: {np.mean(results):.2f}%")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("=== 测试完成 ===")
```

### API 差异对照

| JoinQuant | RiceQuant |
|-----------|-----------|
| `get_all_securities("stock", date)` | `all_instruments("CS")` |
| `get_price(stocks, end_date, count, fields)` | `history_bars(stock, count, unit, fields)` |
| `get_trade_days(start, end)` | `get_trading_dates(start, end)` |
| `valuation.circulating_market_cap` | `fundamentals.eod_derivative_indicator.market_cap` |
| `get_current_data()[stock].high_limit` | `history_bars(stock, 1, "1d", "limit_up")` |

---

## 四、测试脚本文件清单

### 创建目录结构
```
skills/ricequant_strategy/examples/task03/
├── sell_timing_test.py           # 卖出时机测试
├── profit_target_test.py         # 止盈规则测试
├── stop_loss_test.py             # 止损规则测试
├── holding_period_test.py        # 持仓周期测试
└── circuit_breaker_test.py       # 熔断规则测试
```

### 脚本特点
- ✅ RiceQuant Notebook 格式
- ✅ 直接执行 + print 输出
- ✅ 自动 Session 管理
- ✅ 异常处理完善
- ✅ 测试期间：2024年Q1（快速验证）

---

## 五、执行优先级

### 高优先级（P0）
1. ✅ 创建 RiceQuant Notebook 格式测试脚本
2. ⏳ 运行卖出时机测试
3. ⏳ 运行止盈规则测试
4. ⏳ 运行止损规则测试

### 中优先级（P1）
5. ⏳ 运行持仓周期测试
6. ⏳ 运行熔断规则测试

### 低优先级（P2）
7. ⏳ 转换为策略编辑器格式（阶段3）
8. ⏳ JoinQuant 最终验证（阶段4）

---

## 六、下一步操作

### 立即执行
```bash
# 确认脚本文件已创建
ls -la skills/ricequant_strategy/examples/task03/

# 运行第一个测试（卖出时机）
cd skills/ricequant_strategy
node run-strategy.js --strategy ./examples/task03/sell_timing_test.py --create-new --timeout-ms 300000
```

---

**文档状态**: 待脚本创建
**下一步**: 创建 RiceQuant Notebook 格式的测试脚本