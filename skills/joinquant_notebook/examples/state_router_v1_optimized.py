# 状态路由器 v1 设计验证（优化版）
# 使用批量数据获取提高效率

from jqdata import *
import pandas as pd
import numpy as np


def run_state_router_test():
    """
    状态路由器测试 - 批量获取数据提高效率
    """
    start_date = "2018-01-01"
    end_date = "2025-03-30"

    print("=" * 60)
    print("状态路由器 v1 设计验证")
    print("测试期间: {} 至 {}".format(start_date, end_date))
    print("=" * 60)

    # 批量获取沪深300历史数据
    print("\n[1] 批量获取沪深300数据...")
    hs300_prices = get_price(
        "000300.XSHG",
        start_date=start_date,
        end_date=end_date,
        frequency="daily",
        fields=["close", "open"],
        panel=False,
    )

    trade_days = hs300_prices.index.tolist()
    print("交易日数量: {}".format(len(trade_days)))

    # 批量获取沪深300成分股列表（每个季度更新一次即可）
    print("\n[2] 获取沪深300成分股历史...")
    hs300_components = {}
    for date in trade_days[::60]:  # 每60个交易日更新一次
        stocks = get_index_stocks("000300.XSHG", date)
        hs300_components[date] = stocks

    # 批量获取涨停数据
    print("\n[3] 批量获取市场情绪数据...")
    zt_data = []
    for i, date in enumerate(trade_days):
        if i % 50 == 0:
            print("  进度: {:.1f}%".format(i / len(trade_days) * 100))

        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
        ]

        if len(all_stocks) == 0:
            zt_data.append({"date": date, "zt_count": 0, "dt_count": 0})
            continue

        df = get_price(
            all_stocks[:500],
            end_date=date,
            frequency="daily",
            fields=["paused", "close", "high_limit", "low_limit"],
            count=1,
            panel=False,
            fill_paused=False,
        )

        if df.empty:
            zt_data.append({"date": date, "zt_count": 0, "dt_count": 0})
            continue

        df = df.dropna()
        df = df[df["paused"] == 0]

        zt_count = len(df[df["close"] == df["high_limit"]])
        dt_count = len(df[df["close"] == df["low_limit"]])

        zt_data.append({"date": date, "zt_count": zt_count, "dt_count": dt_count})

    zt_df = pd.DataFrame(zt_data)

    # 批量计算市场广度（简化：每5天计算一次）
    print("\n[4] 批量计算市场广度...")
    breadth_data = []
    for i, date in enumerate(trade_days[::5]):  # 每5天计算一次
        if i % 10 == 0:
            print("  进度: {:.1f}%".format(i / (len(trade_days) / 5) * 100))

        # 获取最近的成分股列表
        nearest_date = max([d for d in hs300_components.keys() if d <= date])
        stocks = hs300_components[nearest_date]

        if len(stocks) == 0:
            breadth_data.append({"date": date, "breadth_pct": 0})
            continue

        # 批量获取成分股20日线数据
        prices_batch = get_price(
            stocks,
            end_date=date,
            count=21,
            fields=["close"],
            panel=False,
            fill_paused=False,
        )

        if prices_batch.empty:
            breadth_data.append({"date": date, "breadth_pct": 0})
            continue

        count_above = 0
        for stock in stocks:
            stock_data = prices_batch[prices_batch["code"] == stock]
            if len(stock_data) < 21:
                continue
            ma20 = stock_data["close"].iloc[:20].mean()
            current = stock_data["close"].iloc[-1]
            if current > ma20:
                count_above += 1

        breadth_pct = count_above / len(stocks) * 100
        breadth_data.append({"date": date, "breadth_pct": breadth_pct})

    breadth_df = pd.DataFrame(breadth_data)

    # 合并数据
    print("\n[5] 合并数据并计算状态...")
    result_df = pd.DataFrame(
        {
            "date": trade_days,
            "hs300_close": hs300_prices["close"].values,
            "hs300_open": hs300_prices["open"].values,
        }
    )

    # 添加情绪数据（每天都有）
    result_df = result_df.merge(zt_df, on="date", how="left")

    # 添加广度数据（每5天有，用前值填充）
    result_df = result_df.merge(breadth_df, on="date", how="left")
    result_df["breadth_pct"] = result_df["breadth_pct"].fillna(method="ffill")
    result_df["breadth_pct"] = result_df["breadth_pct"].fillna(30)  # 默认值

    # 分类广度和情绪
    def classify_breadth(pct):
        if pct < 15:
            return 1
        elif pct < 25:
            return 2
        elif pct < 35:
            return 3
        else:
            return 4

    def classify_sentiment(count):
        if count < 30:
            return 1
        elif count < 50:
            return 2
        elif count < 80:
            return 3
        else:
            return 4

    result_df["breadth_level"] = result_df["breadth_pct"].apply(classify_breadth)
    result_df["sentiment_level"] = result_df["zt_count"].apply(classify_sentiment)

    # 状态路由器逻辑
    def get_state_position(breadth, sentiment):
        if breadth == 1:
            return ("关闭", 0)
        elif breadth == 2:
            if sentiment <= 2:
                return ("防守", 30)
            else:
                return ("轻仓", 50)
        elif breadth == 3:
            if sentiment == 2:
                return ("轻仓", 50)
            elif sentiment == 3:
                return ("正常", 70)
            elif sentiment == 4:
                return ("进攻", 100)
            else:
                return ("防守", 30)
        else:
            if sentiment == 4:
                return ("进攻", 100)
            elif sentiment == 3:
                return ("正常", 70)
            else:
                return ("轻仓", 50)

    positions = []
    states = []
    for _, row in result_df.iterrows():
        state, pos = get_state_position(row["breadth_level"], row["sentiment_level"])
        states.append(state)
        positions.append(pos)

    result_df["state"] = states
    result_df["position_router"] = positions
    result_df["position_baseline"] = 100  # 无路由器始终满仓

    # 计算净值
    print("\n[6] 计算净值...")
    result_df["daily_return_baseline"] = result_df["hs300_close"].pct_change()
    result_df["daily_return_router"] = (
        result_df["daily_return_baseline"] * result_df["position_router"] / 100
    )

    result_df["nav_baseline"] = (1 + result_df["daily_return_baseline"]).cumprod()
    result_df["nav_router"] = (1 + result_df["daily_return_router"]).cumprod()

    result_df["drawdown_baseline"] = (
        result_df["nav_baseline"].cummax() - result_df["nav_baseline"]
    ) / result_df["nav_baseline"].cummax()
    result_df["drawdown_router"] = (
        result_df["nav_router"].cummax() - result_df["nav_router"]
    ) / result_df["nav_router"].cummax()

    # 计算指标
    years = len(trade_days) / 252

    annual_return_baseline = (result_df["nav_baseline"].iloc[-1] - 1) / years
    annual_return_router = (result_df["nav_router"].iloc[-1] - 1) / years

    max_dd_baseline = result_df["drawdown_baseline"].max()
    max_dd_router = result_df["drawdown_router"].max()

    sharpe_baseline = (
        result_df["daily_return_baseline"].mean()
        / result_df["daily_return_baseline"].std()
        * np.sqrt(252)
    )
    sharpe_router = (
        result_df["daily_return_router"].mean()
        / result_df["daily_return_router"].std()
        * np.sqrt(252)
    )

    # 年度胜率
    result_df["year"] = pd.to_datetime(result_df["date"]).dt.year
    yearly_baseline = (
        result_df.groupby("year")["nav_baseline"].last()
        / result_df.groupby("year")["nav_baseline"].first()
        - 1
    )
    yearly_router = (
        result_df.groupby("year")["nav_router"].last()
        / result_df.groupby("year")["nav_router"].first()
        - 1
    )

    year_win_baseline = (yearly_baseline > 0).sum() / len(yearly_baseline)
    year_win_router = (yearly_router > 0).sum() / len(yearly_router)

    # 状态分布
    state_dist = result_df["state"].value_counts()

    # 输出结果
    print("\n" + "=" * 60)
    print("对比结果")
    print("=" * 60)

    print("\n【核心指标对比】")
    print("-" * 60)
    print("指标                  | 有路由器  | 无路由器  | 差异")
    print("-" * 60)
    print(
        "年化收益              | {:.2f}%    | {:.2f}%    | {:.2f}%".format(
            annual_return_router * 100,
            annual_return_baseline * 100,
            (annual_return_router - annual_return_baseline) * 100,
        )
    )
    print(
        "最大回撤              | {:.2f}%    | {:.2f}%    | {:.2f}%".format(
            max_dd_router * 100,
            max_dd_baseline * 100,
            (max_dd_router - max_dd_baseline) * 100,
        )
    )
    print(
        "夏普比率              | {:.2f}     | {:.2f}     | {:.2f}".format(
            sharpe_router, sharpe_baseline, sharpe_router - sharpe_baseline
        )
    )
    print(
        "年度胜率              | {:.1f}%    | {:.1f}%    | {:.1f}%".format(
            year_win_router * 100,
            year_win_baseline * 100,
            (year_win_router - year_win_baseline) * 100,
        )
    )
    print(
        "最终净值              | {:.2f}     | {:.2f}     | {:.2f}".format(
            result_df["nav_router"].iloc[-1],
            result_df["nav_baseline"].iloc[-1],
            result_df["nav_router"].iloc[-1] - result_df["nav_baseline"].iloc[-1],
        )
    )

    print("\n【状态分布】")
    print("-" * 60)
    total = len(result_df)
    for state in ["关闭", "防守", "轻仓", "正常", "进攻"]:
        count = state_dist.get(state, 0)
        pct = count / total * 100
        print("{}: {} 天 ({:.1f}%)".format(state, count, pct))

    # 关键问题回答
    print("\n" + "=" * 60)
    print("关键问题回答")
    print("=" * 60)

    dd_improve = (max_dd_baseline - max_dd_router) / max_dd_baseline * 100
    print("\n问题1：路由器能否显著降低回撤？")
    if dd_improve > 20:
        print("回答：YES - 回撤降低 {:.1f}%（>20%门槛）".format(dd_improve))
    else:
        print("回答：NO - 回撤降低 {:.1f}%（<20%门槛）".format(dd_improve))

    ann_cost = (
        abs(annual_return_router - annual_return_baseline)
        / abs(annual_return_baseline)
        * 100
    )
    print("\n问题2：路由器是否会牺牲过多收益？")
    if ann_cost < 20:
        print("回答：NO - 收益差异 {:.1f}%（<20%门槛）".format(ann_cost))
    else:
        print("回答：YES - 收益差异 {:.1f}%（>20%门槛）".format(ann_cost))

    close_pct = state_dist.get("关闭", 0) / total * 100
    print("\n问题3：是否存在过度择时导致错过机会？")
    if close_pct > 30:
        print("回答：YES - 关闭状态占比 {:.1f}%（>30%门槛）".format(close_pct))
    else:
        print("回答：NO - 关闭状态占比 {:.1f}%（<30%门槛）".format(close_pct))

    # 最终评估
    print("\n" + "=" * 60)
    print("最终评估")
    print("=" * 60)

    score = 0
    if dd_improve > 20:
        score += 1
        print("✓ 回撤改善显著")
    else:
        print("✗ 回撤改善不足")

    if ann_cost < 20:
        score += 1
        print("✓ 收益影响可控")
    else:
        print("✗ 收益影响过大")

    if close_pct < 30:
        score += 1
        print("✓ 无过度择时")
    else:
        print("✗ 过度择时风险")

    if score >= 2:
        print("\n最终结论: Go - 状态路由器有效")
    elif score == 1:
        print("\n最终结论: Watch - 状态路由器需优化")
    else:
        print("\n最终结论: No-Go - 状态路由器效果不佳")

    print("\n分析完成")

    return {
        "annual_return_router": annual_return_router,
        "annual_return_baseline": annual_return_baseline,
        "max_dd_router": max_dd_router,
        "max_dd_baseline": max_dd_baseline,
        "sharpe_router": sharpe_router,
        "sharpe_baseline": sharpe_baseline,
        "state_dist": state_dist.to_dict(),
        "score": score,
    }


result = run_state_router_test()
