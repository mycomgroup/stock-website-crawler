# BigQuant 迁移任务提示词

参考文档：`docs/backtest_guide/bigquant_migration_guide.md`

运行命令：
```bash
cd skills/bigquant_strategy
node run-skill.js --strategy examples/<文件名>.py --start-date 2023-01-01 --end-date 2023-12-31
```

---

## 任务一：小市值选股验证（难度：低）

**目标**：把 `skills/joinquant_strategy/smallcap_state_baseline.py` 的核心选股逻辑迁移到 BigQuant，验证数据可用性。

**不需要**：完整回测框架、市场状态分层、情绪统计（这些留给后续任务）。

**只需要**：
1. 用 DAI 查询某一天流通市值在 5~30 亿之间的股票
2. 打印选出的股票列表和数量
3. 验证数据正确性

**写一个 Python 文件** `skills/bigquant_strategy/examples/smallcap_select_bq.py`，内容如下：

```python
"""
小市值选股 - BigQuant 版本
对应 JoinQuant: smallcap_state_baseline.py 的 select_and_buy 逻辑
验证 cn_stock_valuation 数据可用性
"""
import dai
import pandas as pd

DATE = "2024-01-02"
CAP_MIN = 5e8    # 5亿（注意：BigQuant 单位是元，JoinQuant 是亿元）
CAP_MAX = 30e8   # 30亿
TOP_N = 10

print("=== 小市值选股验证 ===")
print("日期:", DATE)

# 获取估值数据
val_df = dai.query("""
    SELECT instrument, float_market_cap, total_market_cap, pe_ttm, pb
    FROM cn_stock_valuation
    WHERE date = '{date}'
      AND float_market_cap >= {cap_min}
      AND float_market_cap <= {cap_max}
      AND pe_ttm > 0
    ORDER BY float_market_cap ASC
    LIMIT {n}
""".format(date=DATE, cap_min=CAP_MIN, cap_max=CAP_MAX, n=TOP_N)).df()

print("选出股票数:", len(val_df))
print(val_df.to_string())
```

然后运行：
```bash
node run-skill.js --strategy examples/smallcap_select_bq.py
```

**验证点**：
- 能正常输出股票列表
- float_market_cap 单位确认（元还是亿元）
- 如果单位不对，调整 CAP_MIN/CAP_MAX

---

## 任务二：首板低开选股（难度：中）

**目标**：把 `skills/joinquant_strategy/simple_first_board.py` 的选股逻辑迁移到 BigQuant。

**核心逻辑**：
1. 找前一天涨停的股票（`close == upper_limit`）
2. 今天开盘价在前一天涨停价的 100.5%~101.5% 之间（假弱高开）
3. 流通市值 50~150 亿

**写一个 Python 文件** `skills/bigquant_strategy/examples/first_board_bq.py`：

```python
"""
首板低开选股 - BigQuant 版本
对应 JoinQuant: simple_first_board.py
数据来源：cn_stock_bar1d（含 upper_limit、lower_limit）
"""
import dai
import pandas as pd

PREV_DATE = "2024-01-02"   # 前一天（涨停日）
TODAY = "2024-01-03"       # 今天（开盘观察日）
CAP_MIN = 50e8             # 50亿（元）
CAP_MAX = 150e8            # 150亿（元）

print("=== 首板低开选股 ===")
print("涨停日:", PREV_DATE, "  观察日:", TODAY)

# 1. 找前一天涨停的股票
prev_df = dai.query("""
    SELECT instrument, close, upper_limit, lower_limit
    FROM cn_stock_bar1d
    WHERE date = '{date}'
      AND close >= upper_limit * 0.999
""".format(date=PREV_DATE)).df()

print("前一天涨停股票数:", len(prev_df))
zt_stocks = prev_df["instrument"].tolist()

if not zt_stocks:
    print("没有涨停股票，退出")
else:
    # 2. 获取今天开盘数据
    inst_str = "','".join(zt_stocks[:200])  # 限制数量
    today_df = dai.query("""
        SELECT b.instrument, b.open, b.upper_limit as today_upper,
               v.float_market_cap
        FROM cn_stock_bar1d b
        LEFT JOIN cn_stock_valuation v
          ON b.instrument = v.instrument AND b.date = v.date
        WHERE b.date = '{today}'
          AND b.instrument IN ('{insts}')
    """.format(today=TODAY, insts=inst_str)).df()

    # 3. 合并，计算开盘比例
    df = today_df.merge(
        prev_df[["instrument", "upper_limit"]].rename(columns={"upper_limit": "prev_upper"}),
        on="instrument"
    )

    # 前一天涨停价 / 1.1 = 前一天收盘价（近似）
    df["prev_close_approx"] = df["prev_upper"] / 1.1
    df["open_ratio"] = df["open"] / df["prev_close_approx"]

    # 4. 筛选假弱高开 + 市值
    qualified = df[
        (df["open_ratio"] >= 1.005) &
        (df["open_ratio"] <= 1.015) &
        (df["float_market_cap"] >= CAP_MIN) &
        (df["float_market_cap"] <= CAP_MAX)
    ]

    print("符合条件股票数:", len(qualified))
    if len(qualified) > 0:
        print(qualified[["instrument", "open", "prev_upper", "open_ratio", "float_market_cap"]].to_string())
    else:
        print("当日无符合条件股票（正常，需要找有涨停的日期）")
        print("\n前一天涨停股票样本（前5只）:")
        print(prev_df.head().to_string())
```

然后运行：
```bash
node run-skill.js --strategy examples/first_board_bq.py
```

**验证点**：
- 涨停判断逻辑是否正确
- open_ratio 计算是否合理
- 如果当天没有符合条件的，换一个有涨停的日期测试

---

## 任务三：小市值状态分层回测（难度：高）

**目标**：把 `skills/joinquant_strategy/smallcap_state_baseline.py` 完整迁移到 BigQuant，实现：
1. 每日计算市场广度（HS300 成分股中高于20日均线的比例）
2. 每日统计涨停数量
3. 按状态分层统计小市值策略的收益

**注意**：BigQuant 免费账户没有指数K线，需要用 HS300 成分股的日K线来计算广度。

**写一个 Python 文件** `skills/bigquant_strategy/examples/smallcap_state_bq.py`：

```python
"""
小市值状态分层研究 - BigQuant 版本
对应 JoinQuant: smallcap_state_baseline.py

BigQuant 数据限制：
- 无指数K线（免费账户），用成分股日K线替代
- cn_stock_bar1d 含 upper_limit（涨停价）
- cn_stock_valuation 含 float_market_cap（流通市值，单位：元）
"""
import dai
import pandas as pd
import numpy as np

# ── 参数 ──────────────────────────────────────────────
START_DATE = "2023-01-01"
END_DATE   = "2023-06-30"   # 先跑半年验证
CAP_MIN    = 5e8            # 5亿元
CAP_MAX    = 30e8           # 30亿元
TOP_N      = 10

# ── 获取交易日列表 ────────────────────────────────────
dates_df = dai.query("""
    SELECT DISTINCT date FROM cn_stock_bar1d
    WHERE date >= '{s}' AND date <= '{e}'
    ORDER BY date
""".format(s=START_DATE, e=END_DATE)).df()
trade_dates = dates_df["date"].tolist()
print("交易日数:", len(trade_dates))

# ── HS300 成分股（用固定列表近似）────────────────────
# 注意：BigQuant 免费账户无指数成分股 API，用估值市值最大的300只近似
def get_hs300_approx(date):
    df = dai.query("""
        SELECT instrument FROM cn_stock_valuation
        WHERE date = '{date}'
          AND total_market_cap > 0
        ORDER BY total_market_cap DESC
        LIMIT 300
    """.format(date=date)).df()
    return df["instrument"].tolist()

# ── 计算市场广度 ──────────────────────────────────────
def calc_breadth(date, hs300_stocks):
    if not hs300_stocks:
        return 0.0
    inst_str = "','".join(hs300_stocks[:100])  # 限制查询量
    df = dai.query("""
        SELECT instrument, close
        FROM cn_stock_bar1d
        WHERE date <= '{date}'
          AND instrument IN ('{insts}')
        ORDER BY instrument, date DESC
    """.format(date=date, insts=inst_str)).df()

    above = 0
    total = 0
    for inst, g in df.groupby("instrument"):
        g = g.head(20)
        if len(g) >= 5:
            ma = g["close"].mean()
            last = g["close"].iloc[0]
            if last >= ma:
                above += 1
            total += 1
    return above / max(total, 1)

# ── 统计涨停数量 ──────────────────────────────────────
def count_zt(date):
    df = dai.query("""
        SELECT COUNT(*) as cnt FROM cn_stock_bar1d
        WHERE date = '{date}'
          AND close >= upper_limit * 0.999
          AND instrument NOT LIKE '688%'
          AND instrument NOT LIKE '8%'
          AND instrument NOT LIKE '4%'
    """.format(date=date)).df()
    return int(df["cnt"].iloc[0]) if len(df) > 0 else 0

# ── 选股 ─────────────────────────────────────────────
def select_stocks(date):
    df = dai.query("""
        SELECT instrument, float_market_cap
        FROM cn_stock_valuation
        WHERE date = '{date}'
          AND float_market_cap >= {cmin}
          AND float_market_cap <= {cmax}
          AND pe_ttm > 0
        ORDER BY float_market_cap ASC
        LIMIT {n}
    """.format(date=date, cmin=CAP_MIN, cmax=CAP_MAX, n=TOP_N)).df()
    return df["instrument"].tolist()

# ── 计算持仓收益 ──────────────────────────────────────
def calc_return(stocks, buy_date, sell_date):
    if not stocks:
        return 0.0
    inst_str = "','".join(stocks)
    df = dai.query("""
        SELECT instrument, date, open, close
        FROM cn_stock_bar1d
        WHERE date IN ('{b}', '{s}')
          AND instrument IN ('{insts}')
    """.format(b=buy_date, s=sell_date, insts=inst_str)).df()

    rets = []
    for inst, g in df.groupby("instrument"):
        g = g.sort_values("date")
        if len(g) == 2:
            buy_p = g["open"].iloc[0]   # 开盘买入
            sell_p = g["close"].iloc[1]  # 收盘卖出
            if buy_p > 0:
                rets.append(sell_p / buy_p - 1)
    return float(np.mean(rets)) if rets else 0.0

# ── 主循环 ────────────────────────────────────────────
print("\n开始回测...")
records = []
hs300 = get_hs300_approx(trade_dates[20])  # 用第20天的成分股

for i, date in enumerate(trade_dates[:-1]):
    next_date = trade_dates[i + 1]

    breadth = calc_breadth(date, hs300)
    zt_count = count_zt(date)
    stocks = select_stocks(date)
    ret = calc_return(stocks, date, next_date)

    # 状态分类
    if breadth < 0.15:
        breadth_state = "极弱"
    elif breadth < 0.25:
        breadth_state = "弱"
    elif breadth < 0.35:
        breadth_state = "中"
    else:
        breadth_state = "强"

    if zt_count < 30:
        sentiment = "冰点"
    elif zt_count < 50:
        sentiment = "启动"
    elif zt_count < 80:
        sentiment = "发酵"
    else:
        sentiment = "高潮"

    records.append({
        "date": date,
        "breadth": breadth,
        "breadth_state": breadth_state,
        "zt_count": zt_count,
        "sentiment": sentiment,
        "stock_count": len(stocks),
        "daily_return": ret * 100
    })

    if i % 10 == 0:
        print("进度 {}/{}: {} 广度={:.1%} 涨停={} 收益={:.2f}%".format(
            i+1, len(trade_dates)-1, date, breadth, zt_count, ret*100))

# ── 统计结果 ──────────────────────────────────────────
df = pd.DataFrame(records)
print("\n=== 回测结果 ===")
print("总交易日:", len(df))
print("平均日收益: {:.3f}%".format(df["daily_return"].mean()))

print("\n--- 市场广度分层 ---")
for state in ["极弱", "弱", "中", "强"]:
    sub = df[df["breadth_state"] == state]
    if len(sub) > 0:
        print("{}: 平均收益={:.3f}%, 天数={}, 胜率={:.1f}%".format(
            state,
            sub["daily_return"].mean(),
            len(sub),
            (sub["daily_return"] > 0).mean() * 100
        ))

print("\n--- 情绪分层 ---")
for state in ["冰点", "启动", "发酵", "高潮"]:
    sub = df[df["sentiment"] == state]
    if len(sub) > 0:
        print("{}: 平均收益={:.3f}%, 天数={}, 胜率={:.1f}%".format(
            state,
            sub["daily_return"].mean(),
            len(sub),
            (sub["daily_return"] > 0).mean() * 100
        ))

print("\n=== 完成 ===")
```

然后运行：
```bash
node run-skill.js --strategy examples/smallcap_state_bq.py --start-date 2023-01-01 --end-date 2023-06-30 --timeout-ms 300000
```

**验证点**：
- 广度计算是否合理（正常范围 0.1~0.6）
- 涨停数量是否合理（正常范围 10~200）
- 各状态的收益分层是否有规律
- 如果超时，缩短日期范围或减少 hs300 成分股数量
