# BigQuant 迁移任务提示词

> 参考文档：
> - `docs/backtest_guide/bigquant_api_reference.md` — 完整 API 参考
> - `docs/backtest_guide/bigquant_migration_guide.md` — 迁移指南

## 运行方式

```bash
cd skills/bigquant_strategy

# 基本运行（自动命名）
node run-skill.js --strategy examples/<文件名>.py

# 指定业务名称（推荐）
node run-skill.js --strategy examples/<文件名>.py --name <业务名称>

# 完整参数
node run-skill.js --strategy examples/<文件名>.py \
  --name <业务名称> \
  --start-date 2023-01-01 \
  --end-date 2023-12-31 \
  --timeout-ms 300000
```

**重要规则**：
1. 每次提交都是新 Task，历史 Task 不删除
2. `--name` 要有业务含义，如 `小市值选股_2023` `首板低开_验证`
3. 结果数据保存在 `skills/bigquant_strategy/data/bigquant-result-*.json`
4. 策略代码用 `print()` 输出结果，系统会自动解析指标

---

## 任务一：小市值选股验证（难度：低）

**目标**：验证 `cn_stock_valuation` 数据可用性，对应 JoinQuant 的 `smallcap_state_baseline.py` 选股逻辑。

**创建文件** `skills/bigquant_strategy/examples/smallcap_select_bq.py`：

```python
"""
小市值选股验证 - BigQuant DAI 版本
对应 JoinQuant: smallcap_state_baseline.py select_and_buy 逻辑

数据说明：
- cn_stock_valuation.float_market_cap 单位是元（不是亿元）
- 5亿 = 5e8，30亿 = 30e8
"""
import dai
import pandas as pd

DATE = "2024-01-02"
CAP_MIN = 5e8    # 5亿元
CAP_MAX = 30e8   # 30亿元
TOP_N = 10

print("=== 小市值选股验证 ===")
print("日期: " + DATE)
print("市值范围: " + str(CAP_MIN/1e8) + "亿 ~ " + str(CAP_MAX/1e8) + "亿")

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

# 转换单位显示
val_df["float_cap_亿"] = (val_df["float_market_cap"] / 1e8).round(2)

print("选出股票数: " + str(len(val_df)))
print(val_df[["instrument", "float_cap_亿", "pe_ttm", "pb"]].to_string())

# 统计信息
if len(val_df) > 0:
    print("\n--- 统计 ---")
    print("平均流通市值: " + str(round(val_df["float_cap_亿"].mean(), 2)) + "亿")
    print("平均PE: " + str(round(val_df["pe_ttm"].mean(), 2)))
    print("平均PB: " + str(round(val_df["pb"].mean(), 2)))
    print("股票数: " + str(len(val_df)))
```

**运行**：
```bash
node run-skill.js --strategy examples/smallcap_select_bq.py --name 小市值选股_数据验证
```

**验证点**：
- 能正常输出股票列表
- float_cap_亿 在 5~30 之间（确认单位正确）
- PE/PB 数值合理

---

## 任务二：首板低开选股（难度：中）

**目标**：迁移 `skills/joinquant_strategy/simple_first_board.py` 的选股逻辑。

**核心逻辑**：
1. 找前一天涨停的股票（`close >= upper_limit * 0.999`）
2. 今天开盘价在前一天收盘价的 100.5%~101.5%（假弱高开）
3. 流通市值 50~150 亿

**创建文件** `skills/bigquant_strategy/examples/first_board_bq.py`：

```python
"""
首板低开选股 - BigQuant DAI 版本
对应 JoinQuant: simple_first_board.py

关键优势：cn_stock_bar1d 直接包含 upper_limit（涨停价），无需手动计算
数据说明：价格已前复权，upper_limit 也是复权后的价格
"""
import dai
import pandas as pd

PREV_DATE = "2024-01-02"   # 涨停日
TODAY = "2024-01-03"       # 观察日
CAP_MIN = 50e8             # 50亿元
CAP_MAX = 150e8            # 150亿元

print("=== 首板低开选股 ===")
print("涨停日: " + PREV_DATE + "  观察日: " + TODAY)

# 1. 找前一天涨停的股票（排除科创板、北交所）
prev_df = dai.query("""
    SELECT instrument, close, upper_limit, pre_close
    FROM cn_stock_bar1d
    WHERE date = '{date}'
      AND close >= upper_limit * 0.999
      AND instrument NOT LIKE '688%'
      AND instrument NOT LIKE '8%'
      AND instrument NOT LIKE '4%'
""".format(date=PREV_DATE)).df()

print("前一天涨停股票数: " + str(len(prev_df)))

if len(prev_df) == 0:
    print("没有涨停股票，请换一个有涨停的日期")
else:
    zt_stocks = prev_df["instrument"].tolist()
    inst_str = "','".join(zt_stocks[:300])

    # 2. 获取今天开盘数据 + 估值
    today_df = dai.query("""
        SELECT b.instrument, b.open, b.close, b.upper_limit as today_upper,
               v.float_market_cap
        FROM cn_stock_bar1d b
        LEFT JOIN cn_stock_valuation v
          ON b.instrument = v.instrument AND b.date = v.date
        WHERE b.date = '{today}'
          AND b.instrument IN ('{insts}')
    """.format(today=TODAY, insts=inst_str)).df()

    # 3. 合并计算开盘比例
    df = today_df.merge(
        prev_df[["instrument", "upper_limit"]].rename(columns={"upper_limit": "prev_upper"}),
        on="instrument"
    )

    # 前一天收盘价 ≈ 前一天涨停价 / 1.1
    df["prev_close_approx"] = df["prev_upper"] / 1.1
    df["open_ratio"] = df["open"] / df["prev_close_approx"]
    df["float_cap_亿"] = (df["float_market_cap"] / 1e8).round(2)

    # 4. 筛选假弱高开 + 市值
    qualified = df[
        (df["open_ratio"] >= 1.005) &
        (df["open_ratio"] <= 1.015) &
        (df["float_market_cap"] >= CAP_MIN) &
        (df["float_market_cap"] <= CAP_MAX)
    ].copy()

    print("符合条件股票数: " + str(len(qualified)))

    if len(qualified) > 0:
        print(qualified[["instrument", "open", "prev_upper", "open_ratio", "float_cap_亿"]].to_string())
        print("\n--- 统计 ---")
        print("平均开盘比例: " + str(round(qualified["open_ratio"].mean(), 4)))
        print("平均流通市值: " + str(round(qualified["float_cap_亿"].mean(), 2)) + "亿")
        print("股票数: " + str(len(qualified)))
    else:
        print("当日无符合条件股票（正常，需要找有涨停的日期）")
        print("\n前一天涨停样本（前5只）:")
        print(prev_df.head().to_string())
        print("\n开盘比例分布（前10只）:")
        print(df[["instrument", "open_ratio", "float_cap_亿"]].head(10).to_string())
```

**运行**：
```bash
node run-skill.js --strategy examples/first_board_bq.py --name 首板低开_选股验证_20240103
```

**验证点**：
- 涨停判断逻辑正确
- open_ratio 在合理范围（0.9~1.2）
- 如果当天没有符合条件的，换一个有涨停的日期

---

## 任务三：小市值状态分层回测（难度：高）

**目标**：完整迁移 `skills/joinquant_strategy/smallcap_state_baseline.py`，实现市场状态分层研究。

**BigQuant 限制**：
- 无指数K线（免费账户），用市值最大的 300 只股票近似 HS300
- 无指数成分股 API，用估值排名替代

**创建文件** `skills/bigquant_strategy/examples/smallcap_state_bq.py`：

```python
"""
小市值状态分层研究 - BigQuant DAI 版本
对应 JoinQuant: smallcap_state_baseline.py

研究目标：
- 市场广度（大盘股高于20日均线比例）对小市值策略的影响
- 涨停数量（市场情绪）对小市值策略的影响
- 找出最优的市场状态过滤条件

BigQuant 适配：
- 用市值最大300只股票近似HS300成分股
- cn_stock_bar1d 直接提供 upper_limit（涨停价）
- 流通市值单位：元（5亿=5e8）
"""
import dai
import pandas as pd
import numpy as np

# ── 参数 ──────────────────────────────────────────────
START_DATE = "2023-01-01"
END_DATE   = "2023-06-30"
CAP_MIN    = 5e8    # 5亿元
CAP_MAX    = 30e8   # 30亿元
TOP_N      = 10

# ── 获取交易日 ────────────────────────────────────────
dates_df = dai.query("""
    SELECT DISTINCT date FROM cn_stock_bar1d
    WHERE date >= '{s}' AND date <= '{e}'
    ORDER BY date
""".format(s=START_DATE, e=END_DATE)).df()
trade_dates = dates_df["date"].tolist()
print("交易日数: " + str(len(trade_dates)))

# ── 获取大盘股列表（近似HS300）────────────────────────
def get_large_cap_stocks(date, n=100):
    df = dai.query("""
        SELECT instrument FROM cn_stock_valuation
        WHERE date = '{date}' AND total_market_cap > 0
        ORDER BY total_market_cap DESC
        LIMIT {n}
    """.format(date=date, n=n)).df()
    return df["instrument"].tolist()

# ── 计算市场广度 ──────────────────────────────────────
def calc_breadth(date, large_stocks):
    if not large_stocks:
        return 0.5
    inst_str = "','".join(large_stocks[:50])
    df = dai.query("""
        SELECT instrument, date, close
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
            buy_p = g["open"].iloc[0]
            sell_p = g["close"].iloc[1]
            if buy_p > 0:
                rets.append(sell_p / buy_p - 1)
    return float(np.mean(rets)) if rets else 0.0

# ── 主循环 ────────────────────────────────────────────
print("\n开始回测...")
large_stocks = get_large_cap_stocks(trade_dates[10], n=100)
records = []

for i, date in enumerate(trade_dates[:-1]):
    next_date = trade_dates[i + 1]

    breadth = calc_breadth(date, large_stocks)
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
        "breadth": round(breadth, 4),
        "breadth_state": breadth_state,
        "zt_count": zt_count,
        "sentiment": sentiment,
        "stock_count": len(stocks),
        "daily_return": round(ret * 100, 4)
    })

    if i % 10 == 0:
        print("进度 {}/{}: {} 广度={:.1%} 涨停={} 收益={:.2f}%".format(
            i+1, len(trade_dates)-1, date, breadth, zt_count, ret*100))

# ── 统计结果 ──────────────────────────────────────────
df = pd.DataFrame(records)
print("\n=== 小市值状态分层研究结果 ===")
print("回测区间: " + START_DATE + " ~ " + END_DATE)
print("总交易日: " + str(len(df)))
print("平均日收益: " + str(round(df["daily_return"].mean(), 3)) + "%")
print("胜率: " + str(round((df["daily_return"] > 0).mean() * 100, 1)) + "%")

print("\n--- 市场广度分层 ---")
for state in ["极弱", "弱", "中", "强"]:
    sub = df[df["breadth_state"] == state]
    if len(sub) > 0:
        print("{}: 平均收益={:.3f}%, 天数={}, 胜率={:.1f}%".format(
            state, sub["daily_return"].mean(), len(sub),
            (sub["daily_return"] > 0).mean() * 100))

print("\n--- 情绪分层 ---")
for state in ["冰点", "启动", "发酵", "高潮"]:
    sub = df[df["sentiment"] == state]
    if len(sub) > 0:
        print("{}: 平均收益={:.3f}%, 天数={}, 胜率={:.1f}%".format(
            state, sub["daily_return"].mean(), len(sub),
            (sub["daily_return"] > 0).mean() * 100))

print("\n--- 过滤效果对比 ---")
no_filter = df["daily_return"].mean()
print("无过滤: 平均收益={:.3f}%, 天数={}".format(no_filter, len(df)))

breadth_filter = df[df["breadth"] >= 0.25]
if len(breadth_filter) > 0:
    bf_avg = breadth_filter["daily_return"].mean()
    print("广度过滤(>=25%): 平均收益={:.3f}%, 天数={}, 提升={:.3f}%".format(
        bf_avg, len(breadth_filter), bf_avg - no_filter))

sentiment_filter = df[df["zt_count"] >= 50]
if len(sentiment_filter) > 0:
    sf_avg = sentiment_filter["daily_return"].mean()
    print("情绪过滤(涨停>=50): 平均收益={:.3f}%, 天数={}, 提升={:.3f}%".format(
        sf_avg, len(sentiment_filter), sf_avg - no_filter))

both_filter = df[(df["breadth"] >= 0.25) & (df["zt_count"] >= 50)]
if len(both_filter) > 0:
    both_avg = both_filter["daily_return"].mean()
    print("双过滤: 平均收益={:.3f}%, 天数={}, 提升={:.3f}%".format(
        both_avg, len(both_filter), both_avg - no_filter))

print("\n=== 完成 ===")
```

**运行**：
```bash
node run-skill.js \
  --strategy examples/smallcap_state_bq.py \
  --name 小市值状态分层_2023H1 \
  --start-date 2023-01-01 \
  --end-date 2023-06-30 \
  --timeout-ms 300000
```

**验证点**：
- 广度值在 0.1~0.8 之间（合理范围）
- 涨停数量在 10~200 之间（合理范围）
- 各状态的收益分层有规律
- 如果超时，缩短日期范围（先跑 1 个月验证）
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
