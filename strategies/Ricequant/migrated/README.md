# RiceQuant 策略迁移 - 运行指南

## 已迁移策略

### 1. 小市值成长股策略 ✅
- **文件**: `01_small_cap_strategy.py`
- **策略**: 选择小市值 + 高ROE的股票
- **调仓**: 每月一次
- **难度**: 低
- **适合**: RiceQuant新手

### 2. 股息率价值策略 ✅
- **文件**: `02_dividend_strategy.py`
- **策略**: 高股息 + 低PE + 低PB
- **调仓**: 每月一次
- **难度**: 低
- **适合**: 价值投资者

### 3. ETF动量轮动策略 ✅
- **文件**: `03_etf_momentum.py`
- **策略**: 选择动量最强的ETF
- **调仓**: 每月一次
- **难度**: 低
- **适合**: ETF投资者

### 4. 龙头底分型战法 ✅
- **文件**: `04_leader_fractal.py`
- **策略**: 龙头股底分型买入
- **调仓**: 每日检查
- **难度**: 中
- **适合**: 技术分析爱好者

### 5. 首板低开策略 ✅
- **文件**: `05_first_board_low_open.py`
- **策略**: 涨停后低开买入
- **调仓**: 每日检查
- **难度**: 中
- **适合**: 短线交易者

---

## 运行方式

### 方式 1: Notebook 运行（推荐）

```bash
# 进入 RiceQuant skill 目录
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy

# 运行策略（自动创建新 notebook）
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/01_small_cap_strategy.py

# 查看结果
cat data/ricequant-notebook-result-*.json
```

### 方式 2: 批量运行

```bash
# 运行所有策略
for strategy in ../../strategies/Ricequant/migrated/*.py; do
  echo "运行策略: $strategy"
  node run-strategy.js --strategy "$strategy"
  echo "---"
done
```

### 方式 3: 在 RiceQuant 平台运行

1. 登录 https://www.ricequant.com
2. 进入策略编辑器
3. 创建新策略
4. 复制粘贴策略代码
5. 点击运行回测

---

## 测试结果查看

### Notebook 结果
```bash
# 查看最新的 notebook 结果
ls -lt data/ricequant-notebook-result-*.json | head -1

# 查看 notebook 快照
ls -lt data/ricequant-notebook-*.ipynb | head -1
```

### RiceQuant 平台
1. 访问 https://www.ricequant.com/research
2. 查看所有 notebook
3. 点击查看详细结果

---

## 策略对比

| 策略 | 原始平台 | 迁移难度 | 预期收益 | 风险等级 |
|------|---------|---------|---------|---------|
| 小市值成长 | JoinQuant | 低 | 中高 | 中 |
| 股息率价值 | JoinQuant | 低 | 中 | 低 |
| ETF动量轮动 | JoinQuant | 低 | 中 | 低 |
| 龙头底分型 | JoinQuant | 中 | 高 | 中高 |
| 首板低开 | JoinQuant | 中 | 高 | 高 |

---

## 迁移说明

### 主要修改点

1. **初始化函数**: `initialize` → `init`
2. **全局变量**: `g.xxx` → `context.xxx`
3. **定时任务**: `run_daily` → `scheduler.run_daily`
4. **数据获取**: 
   - `get_price()` → `history_bars()`
   - `get_all_securities()` → `all_instruments()`
   - `get_index_stocks()` → `index_components()`
5. **实时数据**: `get_current_data()` → `bar_dict`
6. **交易函数**: 
   - `order()` → `order_shares()`
   - `order_target()` → `order_target_quantity()`

### 因子限制

**RiceQuant 支持的因子**:
- ✅ 市值、PE、PB
- ✅ ROE、ROA
- ✅ 净利润增长率
- ⚠️ 部分财务指标

**不支持的因子**:
- ❌ JoinQuant 特殊因子库
- ❌ 复杂技术指标

**解决方案**: 手动计算或使用替代因子

---

## 常见问题

### Q1: 运行时报错 "get_factor failed"

**原因**: RiceQuant 的 `get_factor` 支持的因子有限

**解决**: 
```python
# 检查因子是否支持
factor_names = ["market_cap", "pe_ratio"]  # 这些支持
factor_names = ["PEG", "turnover_volatility"]  # 这些可能不支持
```

### Q2: 涨停价计算不准确

**原因**: ST股票涨跌幅不同

**解决**:
```python
def get_limit_price(stock):
    # 检查是否ST
    inst = instruments(stock)
    if inst.special_type == "ST":
        limit_pct = 0.05
    else:
        limit_pct = 0.10
    
    # 获取昨日收盘价
    bars = history_bars(stock, 1, "1d", "close")
    pre_close = bars[-1]
    
    return round(pre_close * (1 + limit_pct), 2)
```

### Q3: 策略运行很慢

**原因**: RiceQuant 的 `history_bars()` 需要循环调用

**解决**:
```python
# 减少股票数量
stocks = stocks[:100]  # 只测试100只

# 或者分批处理
for batch in [stocks[i:i+50] for i in range(0, len(stocks), 50)]:
    # 处理batch
    pass
```

---

## 下一步

1. ✅ 运行小市值策略验证环境
2. ✅ 运行其他4个策略
3. ✅ 对比回测结果
4. ✅ 优化参数
5. ✅ 实盘测试

**开始运行**:
```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/01_small_cap_strategy.py
```