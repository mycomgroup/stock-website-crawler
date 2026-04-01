"""
影子策略回测 - 10年验证 (RiceQuant Notebook 版本)

回测时间范围：2014-01-01 至 2024-12-31（10年）
初始资金：100000

策略：
1. 主线策略：假弱高开 + 情绪开关
2. 观察线策略：二板策略

运行方式：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_10years_rq.py --timeout-ms 600000
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

OBSERVATION_PARAMS = {
    "board_count": 2,
}


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
            combined = list(set(hs300 + zz500))
            print(f"使用沪深300+中证500替代，共{len(combined)}只")
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


def get_limit_up_count(date, stock_list, trading_dates, max_count=200):
    """获取涨停股票数量"""
    limit_up_count = 0
    tested = 0
    prev_date = get_prev_trading_date(date, trading_dates)

    if prev_date is None:
        print(f"[{date}] 无法获取前一交易日")
        return 0

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

    print(f"[{date}] 涨停统计: 测试{tested}只, 涨停{limit_up_count}只")
    return limit_up_count


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


def has_consecutive_boards(stock, date, trading_dates):
    """判断是否有连板（简化版：检查最近2天是否有涨停）"""
    try:
        dates = []
        for d in trading_dates:
            d_str = str(d)[:10]
            if d_str <= date:
                dates.append(d_str)

        if len(dates) < 3:
            return False

        recent_dates = dates[-3:]

        for i in range(len(recent_dates) - 1):
            curr_df = get_price_on_date(stock, recent_dates[i + 1], ["close"])
            prev_df = get_price_on_date(stock, recent_dates[i], ["close"])

            if curr_df is not None and prev_df is not None:
                curr_close = curr_df["close"].iloc[0]
                prev_close = prev_df["close"].iloc[0]

                if prev_close > 0:
                    pct = (curr_close - prev_close) / prev_close
                    if pct >= 0.095:
                        return True
        return False
    except:
        return False


def generate_mainline_signals(date, stock_list, trading_dates):
    """生成主线信号"""
    limit_up_count = get_limit_up_count(date, stock_list, trading_dates, max_count=100)

    if limit_up_count < MAINLINE_PARAMS["emotion_threshold"]:
        print(f"[{date}] 情绪不足: 涨停{limit_up_count}<30, 无信号")
        return []

    signals = []

    for stock in stock_list[:80]:
        try:
            if is_fake_weak_high_open(stock, date, trading_dates):
                signals.append({"stock": stock, "signal_type": "fake_weak_high_open"})
        except:
            continue

    print(f"[{date}] 主线信号: {len(signals)}只")
    return signals


def generate_observation_signals(date, stock_list, trading_dates):
    """生成观察线信号（简化版）"""
    print(f"[{date}] 观察线策略待实现")
    return []


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
    print("\n开始回测（测试前30个交易日）...")

    capital = 100000
    positions = {}
    trades = []
    daily_values = []

    test_dates = [str(d)[:10] for d in trading_dates[:30]]

    for i, date in enumerate(test_dates):
        if STRATEGY_MODE == "mainline":
            signals = generate_mainline_signals(
                date, all_stocks, [str(d)[:10] for d in trading_dates]
            )
        else:
            signals = generate_observation_signals(
                date, all_stocks, [str(d)[:10] for d in trading_dates]
            )

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
                        print(f"[{date}] 买入 {stock}: 价格{price:.2f}, 数量{shares}")
            except Exception as e:
                print(f"买入失败: {e}")

        daily_values.append({"date": date, "value": capital})

        if (i + 1) % 10 == 0:
            print(f"\n--- 进度: {i + 1}/{len(test_dates)} ---")

    print("\n" + "=" * 80)
    print("回测结果汇总")
    print("=" * 80)

    if len(daily_values) > 0:
        print(f"最终资产: {capital:.2f}")
        print(f"交易次数: {len([t for t in trades if t['action'] == 'buy'])}")

    print("\n" + "=" * 80)
    print("回测完成")
    print("=" * 80)
