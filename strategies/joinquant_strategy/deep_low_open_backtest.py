# 深度低开专项验证 - 策略编辑器格式
# 深度低开：-5%~-3%

from jqdata import *
import pandas as pd


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.test_dates = ["2024-01-15", "2024-07-15"]
    g.signals = []
    g.current_test_idx = 0

    run_daily(test_deep_low_open, "09:35")


def test_deep_low_open(context):
    if g.current_test_idx >= len(g.test_dates):
        return

    test_date = g.test_dates[g.current_test_idx]
    g.current_test_idx += 1

    log.info(f"处理日期: {test_date}")

    # 获取所有股票
    all_stocks = get_all_securities("stock", test_date)
    log.info(f"股票总数: {len(all_stocks)}")

    # 只测试前100只股票
    stocks_sample = all_stocks.index.tolist()[:100]

    for stock in stocks_sample:
        try:
            # 获取前一日数据
            prev_data = get_price(
                stock,
                end_date=test_date,
                count=2,
                frequency="daily",
                fields=["close", "high_limit"],
                panel=False,
            )
            if prev_data is None or len(prev_data) < 2:
                continue

            prev_close = prev_data.iloc[0]["close"]
            prev_limit = prev_data.iloc[0]["high_limit"]

            # 检查昨日是否涨停
            if abs(prev_close - prev_limit) / prev_limit > 0.01:
                continue

            # 获取当日开盘价
            curr_data = get_price(
                stock,
                end_date=test_date,
                count=1,
                frequency="daily",
                fields=["open", "close", "high"],
                panel=False,
            )
            if curr_data is None or len(curr_data) < 1:
                continue

            curr_open = curr_data.iloc[0]["open"]
            curr_close = curr_data.iloc[0]["close"]
            curr_high = curr_data.iloc[0]["high"]

            # 计算开盘涨跌幅
            open_pct = (curr_open - prev_close) / prev_close * 100

            # 筛选深度低开：-5%~-3%
            if -5.0 <= open_pct < -3.0:
                intra_return = (curr_close - curr_open) / curr_open * 100
                max_return = (curr_high - curr_open) / curr_open * 100

                g.signals.append(
                    {
                        "date": test_date,
                        "stock": stock,
                        "open_pct": open_pct,
                        "intra_return": intra_return,
                        "max_return": max_return,
                        "is_win": intra_return > 0,
                    }
                )

                log.info(
                    f"  找到深度低开: {stock}, 开盘{open_pct:.2f}%, 日内{intra_return:.2f}%"
                )

        except Exception as e:
            continue


def on_strategy_end(context):
    log.info("=" * 80)
    log.info("结果汇总")
    log.info("=" * 80)

    if len(g.signals) == 0:
        log.info("未找到深度低开样本")
    else:
        df = pd.DataFrame(g.signals)
        log.info(f"深度低开样本数: {len(df)}")
        log.info(f"平均日内收益: {df['intra_return'].mean():.2f}%")
        log.info(f"胜率: {df['is_win'].sum() / len(df) * 100:.1f}%")
        log.info(
            f"开盘涨跌幅范围: {df['open_pct'].min():.2f}% ~ {df['open_pct'].max():.2f}%"
        )
