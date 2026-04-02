# 深度低开专项验证 - JoinQuant Strategy编辑器
# 阶段4：成熟策略最终验证
# 修复版：收盘后处理，避免盘中获取数据

from jqdata import *
import pandas as pd


def initialize(context):
    set_option("use_real_price", True)
    # 关闭avoid_future_data以便获取历史数据
    # set_option("avoid_future_data", True)
    log.set_level("system", "error")

    # 测试2024年全年
    g.test_year = 2024
    g.signals = []
    g.total_zt = 0
    g.processed_dates = set()

    # 收盘后处理
    run_daily(check_deep_low_open, "15:05")


def check_deep_low_open(context):
    # 只处理2024年
    curr_date = context.current_dt.strftime("%Y-%m-%d")
    if not curr_date.startswith(str(g.test_year)):
        return

    # 避免重复处理
    if curr_date in g.processed_dates:
        return
    g.processed_dates.add(curr_date)

    # 获取前一个交易日
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    # 获取所有股票
    all_stocks = get_all_securities("stock", prev_date)

    # 批量获取涨停板
    price_prev = get_price(
        all_stocks.index.tolist()[:1000],  # 限制数量提高速度
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
    )

    if price_prev.empty:
        return

    # 筛选涨停板（收盘价接近涨停价）
    limit_stocks = price_prev[
        abs(price_prev["close"] - price_prev["high_limit"]) / price_prev["high_limit"]
        < 0.01
    ]["code"].tolist()

    g.total_zt += len(limit_stocks)

    if len(limit_stocks) == 0:
        return

    # 获取当日数据（收盘后可以获取）
    price_curr = get_price(
        limit_stocks,
        end_date=curr_date,
        count=1,
        fields=["open", "close", "high"],
        panel=False,
    )

    if price_curr.empty:
        return

    # 检查深度低开
    for stock in limit_stocks:
        try:
            prev_row = price_prev[price_prev["code"] == stock].iloc[0]
            curr_row = price_curr[price_curr["code"] == stock].iloc[0]

            prev_close = float(prev_row["close"])
            curr_open = float(curr_row["open"])
            curr_close = float(curr_row["close"])
            curr_high = float(curr_row["high"])

            # 计算开盘涨跌幅
            open_pct = (curr_open - prev_close) / prev_close * 100

            # 深度低开：-5% ~ -3%
            if -5.0 <= open_pct < -3.0:
                intra_return = (curr_close - curr_open) / curr_open * 100
                max_return = (curr_high - curr_open) / curr_open * 100

                g.signals.append(
                    {
                        "date": curr_date,
                        "stock": stock,
                        "open_pct": open_pct,
                        "intra_return": intra_return,
                        "max_return": max_return,
                        "is_win": intra_return > 0,
                    }
                )

        except Exception as e:
            continue


def on_strategy_end(context):
    log.info("=" * 80)
    log.info("阶段4：JoinQuant Strategy最终验证")
    log.info("=" * 80)

    log.info(f"总涨停板数: {g.total_zt}")
    log.info(f"深度低开样本数: {len(g.signals)}")

    if len(g.signals) > 0:
        df = pd.DataFrame(g.signals)
        log.info(f"平均日内收益: {df['intra_return'].mean():.2f}%")
        log.info(f"平均最高收益: {df['max_return'].mean():.2f}%")
        log.info(f"胜率: {df['is_win'].sum() / len(df) * 100:.1f}%")
        log.info(
            f"开盘涨跌幅范围: {df['open_pct'].min():.2f}% ~ {df['open_pct'].max():.2f}%"
        )

        log.info("\n详细样本:")
        for idx, row in df.iterrows():
            log.info(
                f"  {row['date']} {row['stock']}: 开盘{row['open_pct']:.2f}%, 日内{row['intra_return']:.2f}%"
            )

        log.info("\n最终判定:")
        if len(df) < 30:
            if (
                df["intra_return"].mean() < 0
                and df["is_win"].sum() / len(df) * 100 < 30
            ):
                log.info("  删除 - 样本少且收益负、胜率极低")
            else:
                log.info("  需更多样本 - 样本不足")
        else:
            if (
                df["intra_return"].mean() > 0.5
                and df["is_win"].sum() / len(df) * 100 > 45
            ):
                log.info("  推荐保留 - 样本充足，收益正，胜率合理")
            else:
                log.info("  建议删除 - 收益或胜率不达标")
    else:
        log.info("未找到深度低开样本")
        log.info("最终判定: 删除")
