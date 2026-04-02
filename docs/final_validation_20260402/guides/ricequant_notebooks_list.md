# RiceQuant Notebook 列表

**用户**: user_497381  
**主页**: https://www.ricequant.com/research/user/user_497381/tree

---

## 📊 最新运行的 Notebook

### 1. RiceQuant_容量与滑点简化测试_20260331_153741.ipynb

**策略文件**: `examples/ricequant_capacity_test.py`  
**Notebook URL**: https://www.ricequant.com/research/user/user_497381/notebooks/RiceQuant_%E5%AE%B9%E9%87%8F%E4%B8%8E%E6%BB%91%E7%82%B9%E7%AE%80%E5%8C%96%E6%B5%8B%E8%AF%95_20260331_153741.ipynb  
**创建时间**: 2026-03-31 15:37:41  
**类型**: Notebook 格式（直接执行）  
**状态**: ✅ 成功执行

**因子来源**:
- `all_securities()` - 所有股票列表
- `get_price()` - 价格数据（开盘、收盘、涨停价）

---

### 2. 策略测试_20260331_154024.ipynb

**策略文件**: `examples/task08_mini_test.py`  
**Notebook URL**: https://www.ricequant.com/research/user/user_497381/notebooks/%E7%AD%96%E7%95%A5%E6%B5%8B%E8%AF%95_20260331_154024.ipynb  
**创建时间**: 2026-03-31 15:40:24  
**类型**: Notebook 格式  
**状态**: ✅ 成功执行

**因子来源**:
- `get_all_securities()` - 所有股票列表
- `get_trading_dates()` - 交易日历
- `history_bars()` - 历史K线数据

**输出示例**:
```
=== RiceQuant 二板策略简化测试 ===
2025Q1交易日数: 57
测试日期: 2025-03-25
```

---

### 3. 策略测试_20260331_154403.ipynb

**策略文件**: `examples/rfscore_simple_notebook.py`  
**Notebook URL**: https://www.ricequant.com/research/user/user_497381/notebooks/%E7%AD%96%E7%95%A5%E6%B5%8B%E8%AF%95_20260331_154403.ipynb  
**创建时间**: 2026-03-31 15:44:03  
**类型**: Notebook 格式  
**状态**: ✅ 成功执行

**因子来源**:
- `index_components("000300.XSHG")` - 沪深300成分股
- `history_bars()` - 历史K线数据（收盘价、成交量）

**计算因子**:
```python
# 动量因子
momentum = (close[-1] / close[0] - 1) * 100

# 量比因子
vol_ratio = np.mean(volume[-5:]) / np.mean(volume)

# 价格位置因子
price_pos = (close[-1] - np.min(close)) / (np.max(close) - np.min(close))

# FScore综合评分
fscore = min(7, max(1, score + 1))
```

**输出示例**:
```
=== RFScore 简化策略 Notebook 测试 ===
获取沪深300成分股...
测试股票数: 30

成功计算 0 只股票的评分
```

---

### 4. 策略测试_20260331_154807.ipynb

**策略文件**: `examples/second_board_simple_rq.py`  
**Notebook URL**: https://www.ricequant.com/research/user/user_497381/notebooks/%E7%AD%96%E7%95%A5%E6%B5%8B%E8%AF%95_20260331_154807.ipynb  
**创建时间**: 2026-03-31 15:48:07  
**类型**: Notebook 格式  
**状态**: ✅ 成功执行

**因子来源**:
- `get_all_securities()` - 所有股票列表
- `get_price()` - 价格数据
- `get_trading_dates()` - 交易日历

**输出示例**:
```
============================================================
二板策略简化测试 - 2022年
============================================================
```

---

### 5. 策略测试_20260331_155250.ipynb ⭐

**策略文件**: `examples/mainline_exit_rules_recent_rq.py`  
**Notebook URL**: https://www.ricequant.com/research/user/user_497381/notebooks/%E7%AD%96%E7%95%A5%E6%B5%8B%E8%AF%95_20260331_155250.ipynb  
**创建时间**: 2026-03-31 15:52:50  
**类型**: Notebook 格式（最完整）  
**状态**: ✅ 成功执行并返回完整回测结果

**因子来源**:

**1. RiceQuant API 数据**:
```python
# 股票列表
get_all_securities(["stock"])

# 历史K线数据
history_bars(stock, 1, "1d", ["close", "limit_up", "open"])

# 财务数据
get_fundamentals(
    query(fundamentals.eod_market_cap).filter(fundamentals.stockcode == stock),
    date
)
```

**2. 计算因子**:
```python
# 开盘涨幅
open_change = (open_price - prev_close) / prev_close

# 流通市值（亿元）
market_cap = cap_data["eod_market_cap"].iloc[0] / 100000000

# 涨停判断
is_limit_up = close >= limit_up * 0.995

# 情绪指标（涨停家数）
limit_up_count = count_limit_up_stocks(date)
```

**输出示例**:
```
【最近6个月实测结果】
卖出规则          交易数  胜率   平均收益  最大回撤  卡玛比率
当日尾盘卖         30   50.0%   0.26%    9.34%    6.96
次日开盘卖         30   30.0%  -1.26%   41.55%    0.00
次日冲高条件卖      30   70.0%   1.63%    5.96%   68.34
持有2天固定卖      30   60.0%   1.57%   12.80%   30.59

主推荐卖法: 次日冲高条件卖
  卡玛比率: 68.34
  胜率: 70.0%
  平均收益: 1.63%
```

---

## 📈 因子来源汇总

### RiceQuant API 提供的数据

| API | 说明 | 用途 |
|-----|------|------|
| `get_all_securities()` | 所有股票列表 | 构建股票池 |
| `index_components()` | 指数成分股 | 选股范围 |
| `history_bars()` | 历史K线数据 | 价格、成交量、涨停价 |
| `get_price()` | 价格数据 | 开盘、收盘、最高、最低 |
| `get_fundamentals()` | 财务数据 | 市值、估值指标 |
| `get_trading_dates()` | 交易日历 | 时间筛选 |

### 本地计算的因子

| 因子名称 | 计算公式 | 说明 |
|---------|---------|------|
| **动量因子** | `(close[-1] / close[0] - 1) * 100` | 一段时间的涨跌幅 |
| **量比因子** | `mean(volume[-5:]) / mean(volume)` | 近期成交量放大倍数 |
| **价格位置** | `(close[-1] - min) / (max - min)` | 当前价格在区间中的位置 |
| **开盘涨幅** | `(open - prev_close) / prev_close` | 今日开盘相对昨收的涨幅 |
| **流通市值** | `market_cap / 1e8` | 流通市值（亿元） |
| **涨停判断** | `close >= limit_up * 0.995` | 是否涨停（允许0.5%误差） |
| **情绪指标** | `count(limit_up_stocks)` | 当日涨停家数 |

---

## 🔍 如何查看 Notebook

### 方法 1: 直接访问链接

点击上面的 Notebook URL，直接在 RiceQuant 平台查看和编辑。

### 方法 2: 从主页导航

1. 访问: https://www.ricequant.com/research/user/user_497381/tree
2. 在文件列表中找到对应的 `.ipynb` 文件
3. 点击打开

### 方法 3: 本地下载

```bash
# 查看所有 notebook 文件
ls -lht /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/data/ricequant-notebook-*.ipynb

# 下载最新的 notebook
# 可以上传到 RiceQuant 或本地 Jupyter 环境运行
```

---

## 📝 Notebook 命名规则

Notebook 名称格式：`{任务名}_{日期}_{时间}.ipynb`

**示例**:
- `RiceQuant_容量与滑点简化测试_20260331_153741.ipynb`
- `策略测试_20260331_154024.ipynb`

**说明**:
- 任务名：从策略文件第一行注释提取（如无注释，默认"策略测试"）
- 日期时间：YYYYMMDD_HHMMSS 格式
- 每次运行都会创建新的 notebook，便于对比不同时间的结果

---

## 🎯 推荐查看顺序

1. **策略测试_20260331_155250.ipynb** ⭐⭐⭐
   - 最完整的回测结果
   - 包含详细的数据分析和策略对比

2. **RiceQuant_容量与滑点简化测试_20260331_153741.ipynb**
   - 基础 API 测试
   - 验证 RiceQuant 连接

3. **策略测试_20260331_154403.ipynb**
   - RFScore 选股逻辑
   - 因子计算示例

---

## 💡 使用提示

### 在 RiceQuant 平台上运行

这些 notebook 已经上传到 RiceQuant 平台，你可以：

1. **直接运行**: 点击 "Cell" → "Run All" 执行所有代码
2. **逐步调试**: 选择单个 cell，点击 "Run" 逐个执行
3. **修改参数**: 修改代码中的参数，重新运行验证
4. **保存结果**: 运行结果会自动保存在 notebook 中

### 注意事项

- ⚠️ RiceQuant API 只在平台环境中可用
- ⚠️ 本地运行的 notebook 会提示 `name 'xxx' is not defined`
- ✅ 在 RiceQuant 平台上运行可以看到完整结果

---

**更新时间**: 2026-03-31 15:55  
**状态**: ✅ 所有 notebook 已成功创建并上传