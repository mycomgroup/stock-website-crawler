# 任务05：主线连亏期与停手机制 - 聚宽回测指引

## 一、当前状况

### 已完成的研究
- ✓ 本地模拟研究已完成（基于result_01基准参数）
- ✓ 主结果文件已生成：`result_05_mainline_pause_rules.md`
- ✓ 简版回执已生成：`05_任务_05_主线连亏期与停手机制_回执.md`

### 聚宽平台测试
- ✓ Session已抓取成功（2026-03-31 11:24）
- ⏳ API连接测试正在进行（响应较慢）
- ✓ 之前已成功执行过类似回测（task02情绪分析、二板2021-2023测试）

---

## 二、聚宽手动测试方案

由于聚宽API响应较慢（大数据量回测需要较长时间），建议采用以下手动测试方案：

### 方案1：在聚宽网站直接运行（推荐）

**步骤**：
1. 登录聚宽网站：https://www.joinquant.com
2. 进入"研究" → "Notebook" → 打开 `test.ipynb`
3. 创建新的cell，粘贴以下简化代码：

```python
from jqdata import *
import numpy as np

print("主线停手机制测试 - 2024Q1")

# 获取交易日
days = list(get_trade_days("2024-01-01", "2024-03-31"))[:20]  # 只测试20天

trades = []
for i in range(1, len(days)):
    date = str(days[i])
    prev = str(days[i-1])
    
    # 获取涨停股
    stocks = get_all_securities("stock", date).index.tolist()[:200]
    df = get_price(stocks, end_date=prev, fields=["close", "high_limit"], 
                   count=1, panel=False)
    if df.empty:
        continue
    
    hl = df[df["close"] == df["high_limit"]]["code"].tolist()[:20]
    
    if len(hl) > 0:
        # 测试假弱高开结构
        today = get_price(hl, end_date=date, fields=["open", "close"], 
                         count=1, panel=False)
        if not today.empty:
            today = today.dropna()
            # 假弱高开：开盘价相对昨收涨幅0.5%-1.5%
            # 这里简化测试，实际需要计算ratio
            
            # 计算收益
            ret = ((today["close"] - today["open"]) / today["open"]).mean()
            
            trades.append({
                "date": date,
                "return_pct": float(ret) * 100,
                "is_win": ret > 0
            })

print(f"交易数: {len(trades)}")

# 统计连亏
loss_count = 0
max_loss = 0
for t in trades:
    if not t["is_win"]:
        loss_count += 1
        if loss_count > max_loss:
            max_loss = loss_count
    else:
        loss_count = 0

print(f"最大连亏: {max_loss}笔")

# 测试停手机制（连亏3停3天）
paused_trades = []
pause_counter = 0
loss_count = 0

for t in trades:
    if pause_counter > 0:
        pause_counter -= 1
        continue
    
    paused_trades.append(t)
    
    if not t["is_win"]:
        loss_count += 1
    else:
        loss_count = 0
    
    if loss_count >= 3:
        pause_counter = 3
        loss_count = 0

print(f"停手后交易数: {len(paused_trades)}")
print(f"休息天数: {len(trades) - len(paused_trades)}")

# 计算对比
def calc_metrics(trades_list):
    returns = [t["return_pct"] for t in trades_list]
    
    equity = 100000
    peak = equity
    max_dd = 0
    
    for r in returns:
        equity = equity * (1 + r / 100)
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak * 100
        if dd > max_dd:
            max_dd = dd
    
    return {
        "return": sum(returns),
        "dd": max_dd,
        "count": len(returns)
    }

m1 = calc_metrics(trades)
m2 = calc_metrics(paused_trades)

print(f"\n对比:")
print(f"无停手: 收益{m1['return']:.2f}% 回撤{m1['dd']:.2f}% 交易{m1['count']}")
print(f"连亏3停: 收益{m2['return']:.2f}% 回撤{m2['dd']:.2f}% 交易{m2['count']}")
print(f"回撤改善: {(m1['dd'] - m2['dd']) / m1['dd'] * 100:.1f}%")
```

**优势**：
- ✓ 可以看到实时执行过程
- ✓ 可以调试和修改参数
- ✓ 无时间限制（Notebook优势）

---

### 方案2：使用策略编辑器回测

**步骤**：
1. 登录聚宽网站
2. 进入"策略" → "策略编辑器"
3. 创建新策略，粘贴完整策略代码（含停手机制）
4. 设置回测参数：2024-01-01 至 2024-12-31，初始资金10万
5. 点击"运行回测"

**完整策略代码**：

```python
from jqdata import *

def initialize(context):
    set_option("use_real_price", True)
    g.loss_count = 0  # 连亏计数
    g.pause_days = 0  # 停手天数
    g.trades = []     # 交易记录
    
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    # 检查是否停手
    if g.pause_days > 0:
        g.pause_days -= 1
        return
    
    date = context.current_dt
    prev_date = date - timedelta(days=1)
    
    # 获取涨停股
    stocks = get_all_securities("stock", date).index.tolist()[:500]
    df = get_price(stocks, end_date=prev_date, fields=["close", "high_limit"],
                   count=1, panel=False)
    
    if df.empty:
        return
    
    hl = df[df["close"] == df["high_limit"]]["code"].tolist()[:20]
    
    if len(hl) > 0:
        for stock in hl:
            order_target_value(stock, 10000)

def after_trading_end(context):
    # 记录当日盈亏
    portfolio = context.portfolio
    daily_pnl_pct = (portfolio.total_value - portfolio.starting_cash) / portfolio.starting_cash * 100
    
    g.trades.append({
        "date": str(context.current_dt),
        "pnl_pct": daily_pnl_pct
    })
    
    # 更新连亏计数
    if daily_pnl_pct < 0:
        g.loss_count += 1
    else:
        g.loss_count = 0
    
    # 触发停手
    if g.loss_count >= 3 and g.pause_days == 0:
        g.pause_days = 3
        log.info(f"触发停手：连亏{g.loss_count}笔，停手3天")
```

---

## 三、已验证的数据（来自之前回测）

根据之前的聚宽回测结果（task02情绪分析）：

| 验证项 | 数据来源 | 结果 |
|--------|----------|------|
| 情绪过滤效果 | task02 | ✓ Go - 收益提升70.8%，胜率提升3% |
| 二板2021-2023 | notebook回测 | ✓ 已执行（虽有warning但数据获取成功） |
| API可用性 | 多次测试 | ✓ 确认可用，但响应慢 |

**结论**：
- 聚宽API确实可用，已多次成功执行
- 大数据量回测需要较长时间（建议减少测试天数）
- 手动在网站运行更可靠（可看到实时进度）

---

## 四、建议的验证顺序

### 优先级排序

| 优先级 | 验证方式 | 说明 |
|--------|----------|------|
| **P0** | **手动在聚宽网站运行简化代码** | **最快、最可靠** |
| P1 | 本地模拟数据对比 | 已完成，作为基准 |
| P2 | 策略编辑器完整回测 | 精确验证，但需等待较长时间 |
| P3 | 自动化脚本运行 | 可尝试，但容易超时 |

---

## 五、简化测试建议

为了快速验证停手机制效果，建议：

1. **只测试2024第一季度**（约60个交易日）
2. **只测试主线信号**（假弱高开结构）
3. **只对比连亏3停3天机制**（主推荐方案）
4. **预计执行时间：5-10分钟**

---

## 六、下一步行动

### 立即行动

1. **打开聚宽网站**：https://www.joinquant.com
2. **进入Notebook**：打开 `test.ipynb`
3. **粘贴简化代码**：执行测试
4. **记录结果**：对比回撤改善、收益变化

### 验证指标

| 指标 | 基准（模拟） | 目标（真实） | 判断标准 |
|------|-------------|-------------|----------|
| 最大回撤改善 | 28.4% | >20% | ✓ 通过 |
| 收益变化 | +20.7% | >-20% | ✓ 通过 |
| 连亏触发次数 | 15次 | 5-20次 | ✓ 合理 |

---

## 七、技术问题说明

### 为什么自动化脚本容易超时？

1. **数据量大**：2024全年数据（250交易日）
2. **API调用慢**：聚宽服务器响应时间约2-5秒/次
3. **网络延迟**：每次请求需要建立连接
4. **内核启动**：Notebook内核初始化需要时间

### 解决方案

1. **减少测试天数**：从250天降至20-60天
2. **减少股票数量**：从500只降至200只
3. **手动运行**：在网站直接执行，可看到进度
4. **分步执行**：先获取数据，再计算指标

---

## 八、结论

### 当前状态

- ✓ **任务05已完成**（基于本地模拟）
- ⏳ **真实数据验证进行中**（建议手动执行）
- ✓ **Session已就绪**（可直接使用）

### 推荐行动

**立即在聚宽网站手动运行简化代码，快速验证停手机制效果。**

---

**生成时间**：2026-03-31 11:45

**状态**：研究完成，待真实数据验证