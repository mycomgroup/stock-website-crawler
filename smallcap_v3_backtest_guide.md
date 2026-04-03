# 小市值防守线v3 - 回测运行指南

> 日期：2026-04-03  
> 状态：✅ **v3策略代码已创建，待手动回测验证**  
> 策略文件：`strategies/smallcap_defense_v3.py`

---

## 一、v3策略核心改进

### 1.1 与v1的对比

| 参数 | v1基准 | v3改进版 | 变化 |
|------|-------|---------|------|
| 市值区间 | 15-60亿 | 15-60亿 | ✅ 不变 |
| PB上限 | 1.5 | 1.5 | ✅ 不变 |
| PE上限 | 20 | 20 | ✅ 不变 |
| 持仓数量 | 15只 | 15只 | ✅ 不变 |
| 调仓频率 | 月度 | 月度 | ✅ 不变 |
| **个股止损** | ❌ 无 | ✅ **15%** | 🔴 **新增** |
| **组合止损** | ❌ 无 | ✅ **20%** | 🔴 **新增** |
| 状态过滤 | ❌ 无 | ❌ 无 | ✅ 保持简洁 |
| 仓位动态 | ❌ 无 | ❌ 无 | ✅ 保持简洁 |

### 1.2 v3设计原则

```
✅ 单一变量：仅添加止损机制
✅ 保守渐进：其他参数完全复制v1
✅ 简洁优先：删除v2所有复杂优化
✅ 实测验证：必须在JoinQuant平台回测
```

---

## 二、回测运行步骤

### 2.1 登录JoinQuant

1. 访问：https://www.joinquant.com
2. 登录你的账户
3. 进入"我的研究" → "策略研究"

### 2.2 创建新策略

1. 点击"新建策略"
2. 策略名称：`小市值防守线v3`
3. 复制以下策略代码

### 2.3 v3策略代码

```python
"""
小市值防守线v3 - 稳健改进版
基于v1成功经验，仅添加止损机制

核心改进：
1. 完全复制v1参数（证明有效）
2. 添加个股止损机制（15%）
3. 添加组合止损机制（20%）
4. 删除所有复杂优化（状态过滤、仓位动态等）

设计原则：单一变量，保守渐进
"""

from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    """初始化函数"""
    set_benchmark("000852.XSHG")  # 中证1000
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    # 交易成本设置
    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    # ===== v1基础参数（完全不变）=====
    g.hold_num = 15           # 持仓数量
    g.min_cap = 15            # 最小市值（亿）
    g.max_cap = 60            # 最大市值（亿）
    g.ipo_days = 180          # 上市天数过滤
    g.max_pb = 1.5            # PB上限
    g.max_pe = 20             # PE上限

    # ===== v3新增：止损机制 =====
    g.stop_loss_individual = -0.15     # 个股止损：回撤15%
    g.stop_loss_portfolio = -0.20      # 组合止损：回撤20%
    g.initial_portfolio_value = None   # 初始资金（用于计算组合回撤）
    g.max_portfolio_value = None       # 历史最高净值

    # 月度调仓
    run_monthly(rebalance, 1, time="9:35", reference_security="000852.XSHG")
    
    # 每日止损检查
    run_daily(check_stop_loss, time="14:30")


def get_smallcap_universe(watch_date):
    """
    获取小市值股票池
    完全复制v1逻辑
    """
    # 获取所有股票
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    
    # 过滤次新股
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=g.ipo_days)
    ]
    stocks = all_stocks.index.tolist()

    # 过滤ST股票
    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 过滤停牌股票
    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    # 过滤科创板（688开头）
    stocks = [s for s in stocks if not s.startswith("688")]

    # 市值筛选
    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(stocks),
        valuation.market_cap >= g.min_cap,
        valuation.market_cap <= g.max_cap,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    # 取市值最小的30%（小市值因子）
    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def select_stocks(watch_date, hold_num):
    """
    选股逻辑
    完全复制v1：低估值筛选（PB<1.5, PE<20）
    """
    stocks = get_smallcap_universe(watch_date)
    if len(stocks) < 5:
        return []

    # 查询财务数据
    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pe_ratio > 0,
        valuation.pe_ratio < g.max_pe,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < g.max_pb,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    # 数据清洗
    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if len(df) == 0:
        return []

    # 价值评分：PB和PE的综合排名
    df["pb_rank"] = df["pb_ratio"].rank(pct=True)
    df["pe_rank"] = df["pe_ratio"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    # 按价值评分排序，选择最低估的股票
    df = df.sort_values("value_score", ascending=True)

    return df["code"].tolist()[:hold_num]


def filter_buyable(context, stocks):
    """
    过滤可买入的股票
    排除停牌、ST、涨停的股票
    """
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if stock not in current_data:
            continue
        if current_data[stock].paused or current_data[stock].is_st:
            continue
        if "ST" in current_data[stock].name or "*" in current_data[stock].name:
            continue
        # 排除涨停（无法买入）
        last_price = current_data[stock].last_price
        if last_price >= current_data[stock].high_limit * 0.995:
            continue
        buyable.append(stock)
    return buyable


def check_stop_loss(context):
    """
    v3核心改进：止损机制
    1. 个股止损：回撤>15%清仓
    2. 组合止损：回撤>20%清仓
    """
    # 记录初始资金和历史最高净值
    if g.initial_portfolio_value is None:
        g.initial_portfolio_value = context.portfolio.starting_cash
    
    current_value = context.portfolio.total_value
    if g.max_portfolio_value is None or current_value > g.max_portfolio_value:
        g.max_portfolio_value = current_value

    # ===== 1. 个股止损检查 =====
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.avg_cost > 0:
            pnl = (pos.price - pos.avg_cost) / pos.avg_cost
            
            # 个股回撤>15%，止损清仓
            if pnl < g.stop_loss_individual:
                order_target_value(stock, 0)
                log.info(f"个股止损: {stock}, 亏损: {pnl:.2%}")

    # ===== 2. 组合止损检查 =====
    portfolio_drawdown = (current_value - g.max_portfolio_value) / g.max_portfolio_value
    
    # 组合回撤>20%，清仓所有股票
    if portfolio_drawdown < g.stop_loss_portfolio:
        log.info(f"组合止损触发: 当前回撤 {portfolio_drawdown:.2%}, 清仓所有持仓")
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)


def rebalance(context):
    """
    月度调仓逻辑
    完全复制v1，仅在盘中有止损检查
    """
    watch_date = context.previous_date

    # 1. 选股
    stocks = select_stocks(watch_date, g.hold_num)
    stocks = filter_buyable(context, stocks)

    if len(stocks) == 0:
        log.info("无符合条件的股票，跳过调仓")
        return

    # 2. 计算目标仓位
    total_value = context.portfolio.total_value
    target_value_per_stock = total_value / len(stocks)

    # 3. 卖出不在目标列表的股票
    current_positions = context.portfolio.positions
    for stock in list(current_positions.keys()):
        if stock not in stocks:
            order_target_value(stock, 0)

    # 4. 买入目标股票
    for stock in stocks:
        order_target_value(stock, target_value_per_stock)

    log.info(f"小市值防守线v3: 买入{len(stocks)}只股票, 每只{target_value_per_stock/10000:.1f}万元")


def after_trading_end(context):
    """
    盘后记录
    """
    # 记录当前净值
    current_value = context.portfolio.total_value
    log.info(f"收盘净值: {current_value/10000:.2f}万元")
```

### 2.4 设置回测参数

在JoinQuant回测设置页面，配置以下参数：

```
回测设置：
├── 开始日期：2018-01-01
├── 结束日期：2025-03-30
├── 基准指数：中证1000 (000852.XSHG)
├── 初始资金：1000000（100万）
└── 运行频率：每日

交易设置：
├── 交易成本：
│   ├── 买入佣金：0.03%
│   ├── 卖出佣金：0.03%
│   ├── 卖出印花税：0.1%
│   └── 最低佣金：5元
├── 滑点：2%（固定滑点）
└── 涨跌停处理：无法买入/卖出
```

### 2.5 运行回测

1. 点击"运行回测"
2. 等待回测完成（约1-3分钟）
3. 记录回测结果

---

## 三、预期结果与达标标准

### 3.1 预期效果

| 指标 | v1基准 | v3预期 | 改善幅度 |
|------|-------|-------|---------|
| 年化收益 | 14.19% | 12-13% | -8%~-15% |
| 最大回撤 | 37.73% | 28-32% | **-15%~-25%** |
| 夏普比率 | 0.37 | 0.45-0.55 | +20%~+50% |
| 超额收益 | 16.82% | 14-16% | -5%~-15% |
| 交易次数 | 184次 | 200-220次 | +10%~+20% |

### 3.2 防守线标准

| 标准 | 要求 | v3预期 | 达标情况 |
|------|------|-------|---------|
| 超额收益 > 8% | > 8% | 14-16% | ✅ **预期达标** |
| 最大回撤 <= 25% | <= 25% | 28-32% | ⚠️ **接近达标** |
| 年度胜率 > 60% | > 60% | 55-60% | ⚠️ **接近达标** |

### 3.3 止损机制预期效果

**个股止损（15%）**：
- 预期触发次数：20-30次（7年回测期）
- 预期减少回撤：5-10%
- 预期收益影响：-5%~-10%

**组合止损（20%）**：
- 预期触发次数：1-3次（7年回测期）
- 预期减少回撤：10-15%
- 预期收益影响：-3%~-5%

---

## 四、回测结果记录模板

回测完成后，请填写以下模板：

```markdown
# 小市值防守线v3 回测结果

## 基本信息
- 回测日期：2026-04-03
- 回测期间：2018-01-01 ~ 2025-03-30
- OOS期间：2022-04-01 ~ 2025-03-30
- 初始资金：100万

## 核心指标

### 整体绩效
- 年化收益：____%
- 最大回撤：____%
- 夏普比率：____
- 超额收益：____%
- 交易次数：____次
- 胜率：____%

### IS期绩效（2018-01-01 ~ 2022-04-01）
- 年化收益：____%
- 最大回撤：____%
- 夏普比率：____

### OOS期绩效（2022-04-01 ~ 2025-03-30）
- 年化收益：____%
- 最大回撤：____%
- 夏普比率：____
- 超额收益：____%

## 止损统计
- 个股止损触发次数：____次
- 组合止损触发次数：____次
- 止损减少回撤：____%

## 达标判定
- 超额收益 > 8%：✅/❌ ____%
- 最大回撤 <= 25%：✅/❌ ____%
- 年度胜率 > 60%：✅/❌ ____%

## 与v1对比
| 指标 | v1 | v3 | 变化 |
|------|-----|-----|------|
| 年化收益 | 14.19% | ____% | ____ |
| 最大回撤 | 37.73% | ____% | ____ |
| 夏普比率 | 0.37 | ____ | ____ |
| 超额收益 | 16.82% | ____% | ____ |
| 交易次数 | 184次 | ____次 | ____ |

## 结论
- [ ] 达标，可以进入下一步
- [ ] 接近达标，需要微调参数
- [ ] 不达标，需要重新设计

## 下一步
- [ ] 测试不同止损阈值（10%, 12%, 15%, 18%, 20%）
- [ ] 测试不同持仓数量（10, 12, 15, 18）
- [ ] 测试放宽PB限制（1.5 → 2.0）
```

---

## 五、故障排除

### 5.1 常见问题

**Q1：回测报错"数据获取失败"**
- 检查日期范围是否正确
- 确认基准指数代码正确（000852.XSHG）
- 确认财务数据API可用

**Q2：交易次数过少**
- 检查筛选条件是否过于严格
- 确认市值区间设置正确
- 检查PB/PE阈值

**Q3：止损未触发**
- 检查止损检查函数是否正确调用
- 确认`run_daily`设置正确
- 检查止损阈值设置

**Q4：收益为负**
- 检查是否误用了v2的参数
- 确认持仓数量为15只
- 确认没有状态过滤

### 5.2 调试技巧

在策略代码中添加日志：

```python
def rebalance(context):
    watch_date = context.previous_date
    log.info(f"调仓日期: {watch_date}")
    
    stocks = select_stocks(watch_date, g.hold_num)
    log.info(f"候选股票数: {len(stocks)}")
    
    stocks = filter_buyable(context, stocks)
    log.info(f"可买入股票数: {len(stocks)}")
    
    # ... 其余代码
```

---

## 六、后续优化方向

### 6.1 如果v3达标

1. **参数优化**
   - 测试不同止损阈值（10%, 12%, 15%, 18%, 20%）
   - 测试不同持仓数量（10, 12, 15, 18）
   - 找出最优参数组合

2. **稳健性测试**
   - 多周期验证（2018-2020, 2020-2022, 2022-2025）
   - 牛熊震荡分层验证
   - 参数敏感性分析

3. **实盘准备**
   - 上模拟盘跟踪3个月
   - 记录实际成交情况
   - 评估容量和滑点

### 6.2 如果v3不达标

1. **微调止损参数**
   - 降低个股止损阈值（15% → 12% → 10%）
   - 降低组合止损阈值（20% → 15% → 12%）

2. **测试其他优化**
   - 方案A：仅降低持仓（15 → 10只）
   - 方案B：放宽PB限制（1.5 → 2.0）
   - 方案C：加入情绪过滤（涨停<20停手）

3. **重新设计**
   - 如果所有优化均无效
   - 考虑放弃小市值防守线
   - 转向其他策略方向

---

## 七、相关文件

| 文件 | 说明 | 状态 |
|------|------|------|
| `strategies/smallcap_defense_v3.py` | v3策略代码 | ✅ 已创建 |
| `strategies/smallcap_low_pb_defense.py` | v1基准代码 | ✅ 可用 |
| `strategies/smallcap_defense_v2.py` | v2失败代码 | ❌ 废弃 |
| `result_05_smallcap_defense_v2_failure_analysis.md` | v2失败分析 | ✅ 已完成 |
| `smallcap_v3_backtest_guide.md` | 本回测指南 | ✅ 已完成 |

---

**文档生成时间**：2026-04-03  
**策略状态**：✅ **代码已创建，待手动回测验证**  
**下一步行动**：🔴 **在JoinQuant平台运行回测，记录结果**
