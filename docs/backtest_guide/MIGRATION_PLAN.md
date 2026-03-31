# 聚宽策略迁移到 RiceQuant - 选定5个策略

## 迁移策略列表

根据 RiceQuant API 能力评估，选择以下5个策略进行迁移：

### 1. 首板低开策略 ✅
**策略文件**: `01 首板低开策略.txt`
**迁移难度**: 中
**所需API**:
- `history_bars()` - 历史数据 ✅
- `bar_dict` - 实时数据 ✅  
- 涨停价判断 - 需手动计算 ⚠️
- 涨停板筛选 - 需手动实现 ⚠️

**迁移要点**:
- 涨停价需要通过 `history_bars(stock, 1, "1d", "limit_up")` 获取
- 涨停股票需要遍历股票池判断

### 2. 龙头底分型战法 ✅
**策略文件**: `02 龙头底分型战法-两年23倍.txt`
**迁移难度**: 中
**所需API**:
- `history_bars()` - 历史K线 ✅
- `bar_dict` - 实时数据 ✅
- 形态识别 - 手动实现 ⚠️

**迁移要点**:
- 底分型识别逻辑完全可用
- 定时任务改为 scheduler

### 3. ETF动量轮动策略 ✅
**策略文件**: `02 ETF动量轮动RSRS择时-魔改3小优化.txt`
**迁移难度**: 低
**所需API**:
- `history_bars()` - 历史数据 ✅
- `index_components()` - ETF列表 ⚠️
- 动量计算 - 手动实现 ⚠️

**迁移要点**:
- ETF交易支持
- RSRS指标需要手动计算

### 4. 股息率策略 ✅
**策略文件**: `04 高股息低市盈率高增长的价投策略.txt`
**迁移难度**: 低
**所需API**:
- `get_fundamentals()` - 财务数据 ✅
- `get_factor()` - 估值因子 ✅

**迁移要点**:
- 股息率因子可用
- PE、PB因子可用

### 5. 小市值策略 ✅
**策略文件**: `01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt`
**迁移难度**: 低
**所需API**:
- `get_factor(["market_cap"])` - 市值因子 ✅
- `get_fundamentals()` - 财务指标 ✅

**迁移要点**:
- 市值因子直接支持
- 财务指标支持良好

---

## 迁移优先级

| 优先级 | 策略 | 迁移难度 | 预计时间 |
|--------|------|---------|---------|
| 1 | 小市值策略 | 低 | 1小时 |
| 2 | 股息率策略 | 低 | 1小时 |
| 3 | ETF动量轮动 | 低 | 1.5小时 |
| 4 | 龙头底分型 | 中 | 2小时 |
| 5 | 首板低开 | 中 | 2.5小时 |

**总计**: 约 8 小时

---

## 迁移脚本

为每个策略创建：
1. RiceQuant 版本策略文件 (`.py`)
2. Notebook 测试文件 (`.ipynb`)
3. 迁移说明文档

### 目录结构

```
strategies/Ricequant/migrated/
├── 01_small_cap_strategy.py
├── 02_dividend_strategy.py
├── 03_etf_momentum.py
├── 04_leader_fractal.py
├── 05_first_board_low_open.py
└── README.md
```

---

## 测试计划

### Notebook 测试流程

```bash
# 1. 小市值策略测试
node run-strategy.js --strategy migrated/01_small_cap_strategy.py

# 2. 股息率策略测试
node run-strategy.js --strategy migrated/02_dividend_strategy.py

# 3. ETF动量轮动测试
node run-strategy.js --strategy migrated/03_etf_momentum.py

# 4. 龙头底分型测试
node run-strategy.js --strategy migrated/04_leader_fractal.py

# 5. 首板低开测试
node run-strategy.js --strategy migrated/05_first_board_low_open.py
```

---

## 注意事项

### 1. 数据获取差异
```python
# JoinQuant
stocks = get_all_securities("stock", date).index

# RiceQuant
all_stocks = all_instruments("CS")
stocks = [s.order_book_id for s in all_stocks]
```

### 2. 实时数据差异
```python
# JoinQuant
current_data = get_current_data()
price = current_data[stock].last_price

# RiceQuant (在 handle_bar 中)
price = bar_dict[stock].close
```

### 3. 涨停价差异
```python
# JoinQuant
high_limit = get_current_data()[stock].high_limit

# RiceQuant
bars = history_bars(stock, 1, "1d", "limit_up")
high_limit = bars[-1]['limit_up'] if bars is not None else None

# 或手动计算
bars = history_bars(stock, 1, "1d", "close")
pre_close = bars[-1]
high_limit = round(pre_close * 1.1, 2)  # 简化版
```

### 4. 定时任务差异
```python
# JoinQuant
run_daily(buy, '09:35')

# RiceQuant
scheduler.run_daily(buy, time_rule=market_open(minute=35))
```

---

## 开始迁移

执行顺序：
1. ✅ 创建迁移目录
2. ✅ 迁移小市值策略
3. ✅ 迁移股息率策略
4. ✅ 迁移ETF动量策略
5. ✅ 迁移龙头底分型
6. ✅ 迁移首板低开策略
7. ✅ Notebook测试
8. ✅ 结果对比

**下一步**: 执行 `node run-strategy.js --strategy migrated/01_small_cap_strategy.py`