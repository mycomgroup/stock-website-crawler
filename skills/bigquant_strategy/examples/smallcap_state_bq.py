"""
小市值状态分层研究 - BigQuant 版本（优化版 v2）
对应 JoinQuant: smallcap_state_baseline.py

修复：
- 广度计算改为向量化，避免日期对齐 bug
- 预取足够历史数据用于 MA20 计算

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
END_DATE = "2023-06-30"  # 先跑半年验证
BAR_START = "2022-11-01"  # K线起始日（往前推用于MA20预热）
CAP_MIN = 5e8  # 5亿元
CAP_MAX = 30e8  # 30亿元
TOP_N = 10
HS300_N = 50  # 用市值最大的50只近似HS300

# ── 获取交易日列表 ────────────────────────────────────
print("获取交易日列表...")
dates_df = dai.query(
    """
    SELECT DISTINCT date FROM cn_stock_bar1d
    WHERE date >= '{s}' AND date <= '{e}'
    ORDER BY date
""".format(s=START_DATE, e=END_DATE)
).df()
trade_dates = dates_df["date"].tolist()
# 统一日期格式为 YYYY-MM-DD 字符串
trade_dates = [str(d)[:10] for d in trade_dates]
print("交易日数:", len(trade_dates))

# ── 获取 HS300 近似成分股 ─────────────────────────────
print("获取HS300近似成分股...")
mid_date = trade_dates[len(trade_dates) // 2]
hs300_df = dai.query(
    """
    SELECT instrument FROM cn_stock_valuation
    WHERE date = '{date}'
      AND total_market_cap > 0
    ORDER BY total_market_cap DESC
    LIMIT {n}
""".format(date=mid_date, n=HS300_N)
).df()
hs300_stocks = hs300_df["instrument"].tolist()
print("成分股数:", len(hs300_stocks))

# ── 预取成分股日K线（含预热期）────────────────────────
print("预取成分股日K线...")
inst_str = "','".join(hs300_stocks)
bar_df = dai.query(
    """
    SELECT instrument, date, close
    FROM cn_stock_bar1d
    WHERE date >= '{s}' AND date <= '{e}'
      AND instrument IN ('{insts}')
    ORDER BY instrument, date ASC
""".format(s=BAR_START, e=END_DATE, insts=inst_str)
).df()
print("K线数据行数:", len(bar_df))

# ── 预取全市场涨停数据 ────────────────────────────────
print("预取全市场涨停数据...")
zt_df = dai.query(
    """
    SELECT date, COUNT(*) as zt_count
    FROM cn_stock_bar1d
    WHERE date >= '{s}' AND date <= '{e}'
      AND close >= upper_limit * 0.999
      AND instrument NOT LIKE '688%'
      AND instrument NOT LIKE '8%'
      AND instrument NOT LIKE '4%'
    GROUP BY date
""".format(s=START_DATE, e=END_DATE)
).df()
zt_map = dict(zip(zt_df["date"], zt_df["zt_count"]))
print("有涨停数据的天数:", len(zt_map))

# ── 预取估值数据 ──────────────────────────────────────
print("预取估值数据...")
val_df = dai.query(
    """
    SELECT date, instrument, float_market_cap
    FROM cn_stock_valuation
    WHERE date >= '{s}' AND date <= '{e}'
      AND float_market_cap >= {cmin}
      AND float_market_cap <= {cmax}
      AND pe_ttm > 0
    ORDER BY date, float_market_cap ASC
""".format(s=START_DATE, e=END_DATE, cmin=CAP_MIN, cmax=CAP_MAX)
).df()
print("估值数据行数:", len(val_df))

# ── 预取选股价格数据 ──────────────────────────────────
print("预取选股价格数据...")
selected_stocks = set()
for date in trade_dates[:-1]:
    day_val = val_df[val_df["date"] == date].head(TOP_N)
    selected_stocks.update(day_val["instrument"].tolist())
selected_stocks = list(selected_stocks)
print("候选股票数:", len(selected_stocks))

if selected_stocks:
    sel_inst_str = "','".join(selected_stocks)
    price_df = dai.query(
        """
        SELECT instrument, date, open, close
        FROM cn_stock_bar1d
        WHERE date >= '{s}' AND date <= '{e}'
          AND instrument IN ('{insts}')
        ORDER BY instrument, date ASC
    """.format(s=START_DATE, e=END_DATE, insts=sel_inst_str)
    ).df()
    print("价格数据行数:", len(price_df))
else:
    price_df = pd.DataFrame()

# ═══════════════════════════════════════════════════════
# 计算阶段（全部在内存中）
# ═══════════════════════════════════════════════════════
print("\n开始计算...")

# ── 向量化计算每日市场广度 ────────────────────────────
bar_df = bar_df.sort_values(["instrument", "date"]).reset_index(drop=True)

# 计算 MA20（每只股票滚动20日均值，最少需要20天）
bar_df["ma20"] = bar_df.groupby("instrument")["close"].transform(
    lambda x: x.rolling(20, min_periods=20).mean()
)

# 标记是否高于MA20
bar_df["above_ma"] = bar_df["close"] >= bar_df["ma20"]

# 只保留目标交易日范围的数据（但 MA20 已用预热数据计算）
bar_df["date"] = pd.to_datetime(bar_df["date"])
target_mask = bar_df["date"] >= pd.to_datetime(START_DATE)
bar_target = bar_df[target_mask].copy()

# 按日期分组计算广度
breadth_by_date = (
    bar_target.groupby("date")
    .agg(
        total=("ma20", lambda x: x.notna().sum()),
        above=(
            "above_ma",
            lambda x: x[x.notna()].sum() if x[x.notna()].shape[0] > 0 else 0,
        ),
    )
    .reset_index()
)
breadth_by_date["breadth"] = breadth_by_date["above"] / breadth_by_date[
    "total"
].replace(0, 1)
breadth_map = dict(
    zip(breadth_by_date["date"].dt.strftime("%Y-%m-%d"), breadth_by_date["breadth"])
)

print("广度计算完成，有效天数:", len(breadth_map))
# 打印前5天广度用于验证
for d in sorted(breadth_map.keys())[:5]:
    print("  {} 广度={:.1%}".format(d, breadth_map[d]))

# ── 主循环 ────────────────────────────────────────────
records = []

for i, date in enumerate(trade_dates[:-1]):
    next_date = trade_dates[i + 1]

    breadth = breadth_map.get(date, 0.0)
    zt_count = int(zt_map.get(date, 0))

    # 选股
    day_val = val_df[val_df["date"] == date].head(TOP_N)
    stocks = day_val["instrument"].tolist()

    # 计算收益
    ret = 0.0
    if stocks and not price_df.empty:
        stock_prices = price_df[
            (price_df["instrument"].isin(stocks))
            & (price_df["date"].isin([date, next_date]))
        ]
        rets = []
        for inst, g in stock_prices.groupby("instrument"):
            g = g.sort_values("date")
            if len(g) == 2:
                buy_p = g["open"].iloc[0]
                sell_p = g["close"].iloc[1]
                if buy_p > 0:
                    rets.append(sell_p / buy_p - 1)
        if rets:
            ret = float(np.mean(rets))

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

    records.append(
        {
            "date": date,
            "breadth": breadth,
            "breadth_state": breadth_state,
            "zt_count": zt_count,
            "sentiment": sentiment,
            "stock_count": len(stocks),
            "daily_return": ret * 100,
        }
    )

    if i % 20 == 0:
        print(
            "进度 {}/{}: {} 广度={:.1%} 涨停={} 收益={:.2f}%".format(
                i + 1, len(trade_dates) - 1, date, breadth, zt_count, ret * 100
            )
        )

# ── 统计结果 ──────────────────────────────────────────
df = pd.DataFrame(records)
print("\n=== 回测结果 ===")
print("总交易日:", len(df))
print("平均日收益: {:.3f}%".format(df["daily_return"].mean()))

print("\n--- 市场广度分层 ---")
for state in ["极弱", "弱", "中", "强"]:
    sub = df[df["breadth_state"] == state]
    if len(sub) > 0:
        print(
            "{}: 平均收益={:.3f}%, 天数={}, 胜率={:.1f}%".format(
                state,
                sub["daily_return"].mean(),
                len(sub),
                (sub["daily_return"] > 0).mean() * 100,
            )
        )

print("\n--- 情绪分层 ---")
for state in ["冰点", "启动", "发酵", "高潮"]:
    sub = df[df["sentiment"] == state]
    if len(sub) > 0:
        print(
            "{}: 平均收益={:.3f}%, 天数={}, 胜率={:.1f}%".format(
                state,
                sub["daily_return"].mean(),
                len(sub),
                (sub["daily_return"] > 0).mean() * 100,
            )
        )

print("\n=== 完成 ===")
