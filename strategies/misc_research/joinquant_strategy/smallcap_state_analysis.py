from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.state_data = []
    g.trade_data = []

    g.market_breadth_bins = {
        "极弱": (0, 0.15),
        "弱": (0.15, 0.25),
        "中": (0.25, 0.35),
        "强": (0.35, 1.0),
    }

    g.sentiment_bins = {
        "冰点": (0, 30),
        "启动": (30, 50),
        "发酵": (50, 80),
        "高潮": (80, 9999),
    }

    run_daily(record_market_state, time="09:00")
    run_daily(analyze_smallcap, time="15:00")

    set_benchmark("000300.XSHG")


def record_market_state(context):
    date = context.current_dt.strftime("%Y-%m-%d")
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    hs300_stocks = get_index_stocks("000300.XSHG")

    above_ma20_count = 0
    total_count = 0

    for stock in hs300_stocks:
        try:
            prices = get_price(
                stock,
                end_date=prev_date,
                count=20,
                fields=["close"],
                panel=False,
                fill_paused=False,
            )
            if len(prices) >= 20:
                ma20 = prices["close"].mean()
                last_close = prices["close"].iloc[-1]
                if last_close >= ma20:
                    above_ma20_count += 1
                total_count += 1
        except:
            continue

    market_breadth = above_ma20_count / max(total_count, 1)

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    try:
        df = get_price(
            all_stocks,
            end_date=prev_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        if not df.empty:
            df = df.dropna()
            zt_count = len(df[df["close"] == df["high_limit"]])
        else:
            zt_count = 0
    except:
        zt_count = 0

    breadth_state = get_state_name(market_breadth, g.market_breadth_bins)
    sentiment_state = get_state_name(zt_count, g.sentiment_bins)

    g.state_data.append(
        {
            "date": date,
            "market_breadth": market_breadth,
            "breadth_state": breadth_state,
            "zt_count": zt_count,
            "sentiment_state": sentiment_state,
        }
    )

    g.current_date = date
    g.current_breadth = market_breadth
    g.current_breadth_state = breadth_state
    g.current_zt_count = zt_count
    g.current_sentiment_state = sentiment_state

    log.info(
        f"{date}: 广度={market_breadth:.2%}({breadth_state}), 涨停={zt_count}({sentiment_state})"
    )


def get_state_name(value, bins):
    for name, (low, high) in bins.items():
        if low <= value < high:
            return name
    return list(bins.keys())[-1]


def analyze_smallcap(context):
    date = context.current_dt.strftime("%Y-%m-%d")

    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.circulating_market_cap >= 5, valuation.circulating_market_cap <= 30
    )

    df = get_fundamentals(q, date=date)

    if df.empty:
        return

    smallcap_stocks = list(df["code"])[:30]

    try:
        prices_today = get_price(
            smallcap_stocks,
            end_date=date,
            count=1,
            fields=["close"],
            panel=False,
            fill_paused=False,
        )

        next_date = get_next_trade_date(date)
        prices_next = get_price(
            smallcap_stocks,
            end_date=next_date,
            count=1,
            fields=["open", "close"],
            panel=False,
            fill_paused=False,
        )

        if prices_today.empty or prices_next.empty:
            return

        returns_list = []

        for stock in smallcap_stocks:
            try:
                today_close = prices_today[prices_today["code"] == stock]["close"].iloc[
                    0
                ]

                next_open = prices_next[prices_next["code"] == stock]["open"].iloc[0]
                next_close = prices_next[prices_next["code"] == stock]["close"].iloc[0]

                return_open = (next_open - today_close) / today_close * 100
                return_close = (next_close - today_close) / today_close * 100

                returns_list.append(
                    {
                        "stock": stock,
                        "return_open": return_open,
                        "return_close": return_close,
                    }
                )

                g.trade_data.append(
                    {
                        "date": date,
                        "stock": stock,
                        "breadth_state": g.current_breadth_state,
                        "sentiment_state": g.current_sentiment_state,
                        "market_breadth": g.current_breadth,
                        "zt_count": g.current_zt_count,
                        "return_open": return_open,
                        "return_close": return_close,
                    }
                )
            except:
                continue

        if returns_list:
            avg_return_open = np.mean([r["return_open"] for r in returns_list])
            avg_return_close = np.mean([r["return_close"] for r in returns_list])
            log.info(
                f"{date}: 小市值平均收益 次日开盘={avg_return_open:.2f}%, 次日收盘={avg_return_close:.2f}%"
            )

    except Exception as e:
        log.info(f"{date}: 分析失败 - {str(e)}")


def after_trading_end(context):
    pass


def on_end(context):
    log.info("\n========== 最终统计结果 ==========")

    if not g.trade_data:
        log.info("没有交易数据")
        return

    df = pd.DataFrame(g.trade_data)

    log.info("\n【市场广度分层统计】")
    breadth_groups = df.groupby("breadth_state").agg(
        {"return_open": ["mean", "count"], "return_close": ["mean", "std"]}
    )

    for state in ["极弱", "弱", "中", "强"]:
        if state in breadth_groups.index:
            avg_open = breadth_groups.loc[state, ("return_open", "mean")]
            avg_close = breadth_groups.loc[state, ("return_close", "mean")]
            count = breadth_groups.loc[state, ("return_open", "count")]
            std_close = breadth_groups.loc[state, ("return_close", "std")]
            log.info(
                f"{state}: 平均收益={avg_close:.2f}%, 标准差={std_close:.2f}%, 样本数={count}"
            )

    log.info("\n【情绪分层统计】")
    sentiment_groups = df.groupby("sentiment_state").agg(
        {"return_open": ["mean", "count"], "return_close": ["mean", "std"]}
    )

    for state in ["冰点", "启动", "发酵", "高潮"]:
        if state in sentiment_groups.index:
            avg_open = sentiment_groups.loc[state, ("return_open", "mean")]
            avg_close = sentiment_groups.loc[state, ("return_close", "mean")]
            count = sentiment_groups.loc[state, ("return_open", "count")]
            std_close = sentiment_groups.loc[state, ("return_close", "std")]
            log.info(
                f"{state}: 平均收益={avg_close:.2f}%, 标准差={std_close:.2f}%, 样本数={count}"
            )

    log.info("\n【状态过滤效果对比】")

    all_avg_close = df["return_close"].mean()
    log.info(f"无过滤: 平均收益={all_avg_close:.2f}%, 样本数={len(df)}")

    breadth_filtered = df[df["market_breadth"] >= 0.25]
    if not breadth_filtered.empty:
        avg = breadth_filtered["return_close"].mean()
        log.info(
            f"广度过滤(≥25%): 平均收益={avg:.2f}%, 样本数={len(breadth_filtered)}, "
            f"提升={avg - all_avg_close:.2f}%"
        )

    sentiment_filtered = df[df["zt_count"] >= 50]
    if not sentiment_filtered.empty:
        avg = sentiment_filtered["return_close"].mean()
        log.info(
            f"情绪过滤(涨停≥50): 平均收益={avg:.2f}%, 样本数={len(sentiment_filtered)}, "
            f"提升={avg - all_avg_close:.2f}%"
        )

    both_filtered = df[(df["market_breadth"] >= 0.25) & (df["zt_count"] >= 50)]
    if not both_filtered.empty:
        avg = both_filtered["return_close"].mean()
        log.info(
            f"双过滤: 平均收益={avg:.2f}%, 样本数={len(both_filtered)}, "
            f"提升={avg - all_avg_close:.2f}%"
        )

    log.info("\n【极弱市场分析】")
    extreme_weak = df[df["breadth_state"] == "极弱"]
    if not extreme_weak.empty:
        avg = extreme_weak["return_close"].mean()
        win_rate = (extreme_weak["return_close"] > 0).sum() / len(extreme_weak) * 100
        log.info(
            f"极弱市场: 平均收益={avg:.2f}%, 胜率={win_rate:.1f}%, 样本数={len(extreme_weak)}"
        )

    log.info("\n【情绪冰点分析】")
    freeze = df[df["sentiment_state"] == "冰点"]
    if not freeze.empty:
        avg = freeze["return_close"].mean()
        win_rate = (freeze["return_close"] > 0).sum() / len(freeze) * 100
        log.info(
            f"情绪冰点: 平均收益={avg:.2f}%, 胜率={win_rate:.1f}%, 样本数={len(freeze)}"
        )

    log.info("\n========== 数据详情 ==========")
    state_summary = df.groupby(["breadth_state", "sentiment_state"]).agg(
        {"return_close": ["mean", "count"]}
    )

    for idx in state_summary.index:
        breadth, sentiment = idx
        avg = state_summary.loc[idx, ("return_close", "mean")]
        count = state_summary.loc[idx, ("return_close", "count")]
        log.info(f"{breadth}+{sentiment}: 平均收益={avg:.2f}%, 样本数={count}")
