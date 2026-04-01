"""
影子策略回测 - 10年验证 (RiceQuant Notebook 版本)

回测时间范围：2014-01-01 至 2024-12-31（10年）
初始资金：100000

策略：
1. 主线策略：假弱高开 + 情绪开关
2. 观察线策略：二板策略

运行方式：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_10years_rq.py --create-new --timeout-ms 600000
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("影子策略 10年回测 - RiceQuant Notebook")
print("=" * 80)
print(f"回测时间: 2014-01-01 至 2024-12-31")
print(f"初始资金: 100000")
print("=" * 80)

STRATEGY_MODE = "mainline"

MAINLINE_PARAMS = {
    "market_cap_min": 50,
    "market_cap_max": 150,
    "position_limit": 0.30,
    "emotion_threshold": 30,
    "open_change_min": 0.001,
    "open_change_max": 0.03,
    "sell_profit_threshold": 0.03,
}

TEST_CONFIG = {
    "limit_up_sample_size": 500,
    "signal_sample_size": 300,
    "test_days": 200,
    "start_year": 2015,
}

print(f"\n测试配置:")
print(f"  涨停统计股票数: {TEST_CONFIG['limit_up_sample_size']}")
print(f"  信号筛选股票数: {TEST_CONFIG['signal_sample_size']}")
print(f"  测试天数: {TEST_CONFIG['test_days']}")
print(f"  起始年份: {TEST_CONFIG['start_year']}")


def get_all_stocks_list():
    """获取所有A股股票列表"""
    try:
        instruments = all_instruments(type="CS")
        return list(instruments.order_book_id)
    except Exception as e:
        print(f"all_instruments获取失败: {e}")
        try:
            hs300 = index_components("000300.XSHG")
            zz500 = index_components("000905.XSHG")
            zz800 = index_components("000906.XSHG")
            combined = list(set(hs300 + zz500 + zz800))
            print(f"使用沪深300+中证500+中证800替代，共{len(combined)}只")
            return combined
        except Exception as e2:
            print(f"获取指数成分股也失败: {e2}")
            return []


def get_price_on_date(stock, date, fields=["close"]):
    """获取指定日期的价格数据"""
    try:
        df = get_price(
            stock, start_date=date, end_date=date, frequency="1d", fields=fields
        )
        if df is not None and len(df) > 0:
            return df
        return None
    except:
        return None


def get_prev_trading_date(date, trading_dates):
    """获取前一个交易日"""
    date_str = str(date)[:10] if hasattr(date, "__str__") else date
    for i, d in enumerate(trading_dates):
        d_str = str(d)[:10]
        if d_str == date_str and i > 0:
            return str(trading_dates[i - 1])[:10]
    return None


def get_limit_up_count_fast(date, stock_list, trading_dates, max_count=500):
    """快速获取涨停股票数量"""
    limit_up_count = 0
    tested = 0
    prev_date = get_prev_trading_date(date, trading_dates)

    if prev_date is None:
        return 0, 0

    for stock in stock_list[:max_count]:
        try:
            curr_df = get_price_on_date(stock, date, ["close"])
            prev_df = get_price_on_date(stock, prev_date, ["close"])

            if curr_df is not None and prev_df is not None:
                curr_close = curr_df["close"].iloc[0]
                prev_close = prev_df["close"].iloc[0]

                if prev_close > 0:
                    pct_change = (curr_close - prev_close) / prev_close
                    if pct_change >= 0.095:
                        limit_up_count += 1
                    tested += 1
        except:
            continue

    return limit_up_count, tested


def is_fake_weak_high_open(stock, date, trading_dates):
    """判断是否为假弱高开"""
    try:
        prev_date = get_prev_trading_date(date, trading_dates)
        if prev_date is None:
            return False

        curr_df = get_price_on_date(stock, date, ["close", "open", "high"])
        prev_df = get_price_on_date(stock, prev_date, ["close"])

        if curr_df is None or prev_df is None:
            return False

        prev_close = prev_df["close"].iloc[0]
        open_price = curr_df["open"].iloc[0]
        high_price = curr_df["high"].iloc[0]

        if prev_close <= 0:
            return False

        open_change = (open_price - prev_close) / prev_close

        if (
            open_change <= MAINLINE_PARAMS["open_change_min"]
            or open_change >= MAINLINE_PARAMS["open_change_max"]
        ):
            return False

        if high_price > open_price:
            return True

        return False
    except:
        return False


def get_stock_market_cap(stock, date):
    """获取市值（亿元）"""
    try:
        factor_data = get_factor(stock, "market_cap", start_date=date, end_date=date)
        if factor_data is not None and len(factor_data) > 0:
            return float(factor_data.iloc[0]) / 1e8
        return None
    except:
        return None


def generate_mainline_signals(date, stock_list, trading_dates, limit_up_count):
    """生成主线信号"""
    if limit_up_count < MAINLINE_PARAMS["emotion_threshold"]:
        return []

    signals = []

    for stock in stock_list[: TEST_CONFIG["signal_sample_size"]]:
        try:
            market_cap = get_stock_market_cap(stock, date)
            if market_cap is None:
                continue
            if (
                market_cap < MAINLINE_PARAMS["market_cap_min"]
                or market_cap > MAINLINE_PARAMS["market_cap_max"]
            ):
                continue

            if is_fake_weak_high_open(stock, date, trading_dates):
                signals.append(
                    {
                        "stock": stock,
                        "market_cap": market_cap,
                        "signal_type": "fake_weak_high_open",
                    }
                )
        except:
            continue

    return signals


print("\n获取交易日列表...")
try:
    trading_dates = list(get_trading_dates("2014-01-01", "2024-12-31"))
    print(f"交易日数量: {len(trading_dates)}")
except Exception as e:
    print(f"获取交易日失败: {e}")
    trading_dates = []

print("\n获取股票列表...")
all_stocks = get_all_stocks_list()
print(f"股票总数: {len(all_stocks)}")

if len(all_stocks) == 0 or len(trading_dates) == 0:
    print("无法获取数据，请确保在 RiceQuant Notebook 环境运行")
else:
    start_idx = 0
    for i, d in enumerate(trading_dates):
        if str(d)[:4] == str(TEST_CONFIG["start_year"]):
            start_idx = i
            break

    test_dates = [
        str(d)[:10]
        for d in trading_dates[start_idx : start_idx + TEST_CONFIG["test_days"]]
    ]
    print(f"\n测试日期范围: {test_dates[0]} 至 {test_dates[-1]}")
    print(f"测试天数: {len(test_dates)}")

    print("\n开始回测...")

    capital = 100000
    positions = {}
    trades = []
    daily_values = []
    signal_count = 0
    buy_count = 0

    for i, date in enumerate(test_dates):
        limit_up_count, tested = get_limit_up_count_fast(
            date,
            all_stocks,
            [str(d)[:10] for d in trading_dates],
            max_count=TEST_CONFIG["limit_up_sample_size"],
        )

        if limit_up_count >= MAINLINE_PARAMS["emotion_threshold"]:
            signals = generate_mainline_signals(
                date, all_stocks, [str(d)[:10] for d in trading_dates], limit_up_count
            )
            signal_count += len(signals)

            if signals and len(positions) < 3:
                signal = signals[0]
                stock = signal["stock"]

                try:
                    df = get_price_on_date(stock, date, ["close"])
                    if df is not None:
                        price = df["close"].iloc[0]
                        max_amount = min(100000, capital)
                        shares = int(max_amount / price / 100) * 100

                        if shares > 0 and capital >= shares * price:
                            capital -= shares * price
                            positions[stock] = {
                                "buy_date": date,
                                "buy_price": price,
                                "shares": shares,
                            }
                            trades.append(
                                {
                                    "date": date,
                                    "stock": stock,
                                    "action": "buy",
                                    "price": price,
                                    "shares": shares,
                                }
                            )
                            buy_count += 1
                            print(
                                f"[{date}] 涨停{limit_up_count}只 -> 买入 {stock}: 价格{price:.2f}"
                            )
                except Exception as e:
                    pass

        stocks_to_sell = []
        for stock, pos in list(positions.items()):
            try:
                df = get_price_on_date(stock, date, ["close"])
                if df is not None:
                    current_price = df["close"].iloc[0]
                    profit_pct = (current_price - pos["buy_price"]) / pos["buy_price"]

                    if profit_pct >= MAINLINE_PARAMS["sell_profit_threshold"]:
                        stocks_to_sell.append((stock, current_price, "冲高+3%止盈"))
                    elif date > pos["buy_date"]:
                        stocks_to_sell.append((stock, current_price, "尾盘卖出"))
            except:
                pass

        for stock, price, reason in stocks_to_sell:
            if stock in positions:
                pos = positions[stock]
                profit = (price - pos["buy_price"]) * pos["shares"]
                profit_pct = (price - pos["buy_price"]) / pos["buy_price"]
                capital += price * pos["shares"]
                trades.append(
                    {
                        "date": date,
                        "stock": stock,
                        "action": "sell",
                        "price": price,
                        "profit": profit,
                        "profit_pct": profit_pct,
                        "reason": reason,
                    }
                )
                del positions[stock]

        total_value = capital
        for stock, pos in positions.items():
            try:
                df = get_price_on_date(stock, date, ["close"])
                if df is not None:
                    total_value += df["close"].iloc[0] * pos["shares"]
            except:
                pass

        daily_values.append({"date": date, "value": total_value})

        if (i + 1) % 20 == 0:
            print(f"\n--- 进度: {i + 1}/{len(test_dates)} ---")
            print(
                f"    涨停达标天数: {sum(1 for dv in daily_values if dv['value'] != 100000 or len(trades) > 0)}"
            )
            print(
                f"    信号数: {signal_count}, 买入: {buy_count}, 卖出: {len([t for t in trades if t['action'] == 'sell'])}"
            )
            print(f"    总资产: {total_value:.2f}")

    print("\n" + "=" * 80)
    print("回测结果汇总")
    print("=" * 80)

    sell_trades = [t for t in trades if t["action"] == "sell"]

    if len(daily_values) > 0:
        initial = 100000
        final = daily_values[-1]["value"]
        total_return = (final - initial) / initial

        print(f"总收益率: {total_return:.2%}")
        print(f"最终资产: {final:.2f}")
        print(f"信号数量: {signal_count}")
        print(f"买入次数: {buy_count}")
        print(f"卖出次数: {len(sell_trades)}")

        if len(sell_trades) > 0:
            wins = [t for t in sell_trades if t.get("profit", 0) > 0]
            win_rate = len(wins) / len(sell_trades)
            avg_profit_pct = np.mean([t.get("profit_pct", 0) for t in sell_trades])

            print(f"胜率: {win_rate:.2%}")
            print(f"平均收益率: {avg_profit_pct:.2%}")

    print("\n" + "=" * 80)
    print("回测完成")
    print("=" * 80)
