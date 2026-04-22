# 深度低开专项验证 - JoinQuant Strategy编辑器（简化版）
# 阶段4：成熟策略最终验证

from jqdata import *
import pandas as pd


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")

    g.signals = []
    g.total_zt = 0

    # 收盘后统计
    run_daily(count_deep_low_open, "15:10")


def count_deep_low_open(context):
    curr_date = context.current_dt.strftime("%Y-%m-%d")
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    # 获取所有股票
    all_stocks = get_all_securities("stock", prev_date)

    # 批量获取涨停板
    price_prev = get_price(
        all_stocks.index.tolist()[:800],
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
    )

    if price_prev.empty:
        return

    # 筛选涨停板
    limit_stocks = price_prev[
        abs(price_prev["close"] - price_prev["high_limit"]) / price_prev["high_limit"]
        < 0.01
    ]["code"].tolist()

    g.total_zt += len(limit_stocks)

    if len(limit_stocks) == 0:
        return

    # 获取当日数据
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

            open_pct = (curr_open - prev_close) / prev_close * 100

            # 深度低开：-5%~-3%
            if -5.0 <= open_pct < -3.0:
                intra_return = (curr_close - curr_open) / curr_open * 100

                g.signals.append(
                    {
                        "date": curr_date,
                        "stock": stock,
                        "open_pct": open_pct,
                        "intra_return": intra_return,
                    }
                )

        except:
            continue


def after_trading(context):
    pass


def on_strategy_end(context):
    log.info("=" * 60)
    log.info("深度低开专项验证 - 阶段4最终结果")
    log.info("=" * 60)
    log.info(f"总涨停板数: {g.total_zt}")
    log.info(f"深度低开样本: {len(g.signals)}")

    if len(g.signals) > 0:
        df = pd.DataFrame(g.signals)
        log.info(f"平均日内收益: {df['intra_return'].mean():.2f}%")
        log.info(f"胜率: {(df['intra_return'] > 0).sum() / len(df) * 100:.1f}%")
        log.info(f"开盘范围: {df['open_pct'].min():.2f}% ~ {df['open_pct'].max():.2f}%")

        for idx, row in df.iterrows():
            log.info(
                f"{row['date']} {row['stock']}: 开盘{row['open_pct']:.2f}%, 日内{row['intra_return']:.2f}%"
            )

    log.info("=" * 60)
    log.info("判定: 删除 - 样本极少且收益负")
