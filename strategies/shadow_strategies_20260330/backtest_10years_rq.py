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


def get_limit_up_count(date, stock_list, max_count=300):
    """获取涨停股票数量"""
    limit_up_count = 0
    tested = 0
    errors = []

    for stock in stock_list[:max_count]:
        try:
            # RiceQuant Notebook 使用 get_price
            df = get_price(
                stock, end_date=date, frequency="1d", fields=["close"], count=2
            )
            if df is not None and len(df) >= 2:
                prev_close = df["close"].iloc[-2]
                curr_close = df["close"].iloc[-1]
                if prev_close > 0:
                    pct_change = (curr_close - prev_close) / prev_close
                    if pct_change >= 0.095:
                        limit_up_count += 1
                tested += 1
            else:
                if len(errors) < 3:
                    errors.append(f"{stock}: df={df}")
        except Exception as e:
            if len(errors) < 3:
                errors.append(f"{stock}: {str(e)[:50]}")
            continue

    print(f"[{date}] 涨停统计: 测试{tested}只, 涨停{limit_up_count}只")
    if errors:
        print(f"  错误示例: {errors[:2]}")
    return limit_up_count


def is_fake_weak_high_open(stock, date):
    """判断是否为假弱高开"""
    try:
        bars = history_bars(stock, 2, "1d", ["close", "open", "high"], end_dt=date)
        if bars is None or len(bars) < 2:
            return False

        prev_close = bars["close"][-2]
        open_price = bars["open"][-1]
        high_price = bars["high"][-1]

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


def get_stock_position_pct(stock, date):
    """获取位置（相对历史最高）"""
    try:
        bars = history_bars(stock, 250, "1d", "high", end_dt=date)
        if bars is None or len(bars) < 250:
            return None

        high_max = max(bars["high"])
        current_high = bars["high"][-1]

        if high_max > 0:
            return current_high / high_max - 1
        return None
    except:
        return None


def has_consecutive_boards(stock, date):
    """判断是否有连板"""
    try:
        bars = history_bars(stock, 5, "1d", "close", end_dt=date)
        if bars is None or len(bars) < 5:
            return False

        closes = bars["close"]

        for i in range(len(closes) - 2):
            if closes[i] > 0 and closes[i + 1] > 0:
                pct = (closes[i + 1] - closes[i]) / closes[i]
                if pct >= 0.095:
                    return True
        return False
    except:
        return False


def is_second_board(stock, date):
    """判断是否为二板"""
    try:
        bars = history_bars(stock, 5, "1d", "close", end_dt=date)
        if bars is None or len(bars) < 5:
            return False

        closes = bars["close"]
        consecutive = 0

        for i in range(len(closes) - 1):
            if closes[i] > 0:
                pct = (closes[i + 1] - closes[i]) / closes[i]
                if pct >= 0.095:
                    consecutive += 1
                else:
                    break

        return consecutive == 2
    except:
        return False


def is_limit_up_today(stock, date):
    """判断今日是否涨停"""
    try:
        bars = history_bars(stock, 2, "1d", "close", end_dt=date)
        if bars is None or len(bars) < 2:
            return False

        prev_close = bars["close"][-2]
        curr_close = bars["close"][-1]

        if prev_close > 0:
            pct = (curr_close - prev_close) / prev_close
            return pct >= 0.095
        return False
    except:
        return False


def generate_mainline_signals(date, stock_list):
    """生成主线信号"""
    limit_up_count = get_limit_up_count(date, stock_list, max_count=200)

    if limit_up_count < MAINLINE_PARAMS["emotion_threshold"]:
        print(f"[{date}] 情绪不足: 涨停{limit_up_count}<30, 无信号")
        return []

    signals = []

    for stock in stock_list[:150]:
        try:
            market_cap = get_stock_market_cap(stock, date)
            if (
                market_cap is None
                or market_cap < MAINLINE_PARAMS["market_cap_min"]
                or market_cap > MAINLINE_PARAMS["market_cap_max"]
            ):
                continue

            position_pct = get_stock_position_pct(stock, date)
            if (
                position_pct is not None
                and position_pct > MAINLINE_PARAMS["position_limit"]
            ):
                continue

            if has_consecutive_boards(stock, date):
                continue

            if is_fake_weak_high_open(stock, date):
                signals.append(
                    {
                        "stock": stock,
                        "market_cap": market_cap,
                        "position_pct": position_pct,
                        "signal_type": "fake_weak_high_open",
                    }
                )
        except:
            continue

    print(f"[{date}] 主线信号: {len(signals)}只")
    return signals


def generate_observation_signals(date, stock_list):
    """生成观察线信号"""
    signals = []

    for stock in stock_list[:150]:
        try:
            if is_second_board(stock, date):
                if not is_limit_up_today(stock, date):
                    signals.append({"stock": stock, "signal_type": "second_board"})
        except:
            continue

    print(f"[{date}] 观察线信号: {len(signals)}只")
    return signals


print("\n获取交易日列表...")
try:
    trading_dates = get_trading_dates("2014-01-01", "2024-12-31")
    trading_dates = list(trading_dates)
    print(f"交易日数量: {len(trading_dates)}")
except Exception as e:
    print(f"获取交易日失败: {e}")
    trading_dates = []

print("\n获取股票列表...")
all_stocks = get_all_stocks_list()
print(f"股票总数: {len(all_stocks)}")

if len(all_stocks) == 0:
    print("无法获取股票列表，请确保在 RiceQuant Notebook 环境运行")
else:
    print("\n开始回测...")

    capital = 100000
    positions = {}
    trades = []
    daily_values = []
    consecutive_losses = 0
    stop_trading_until = None

    test_dates = trading_dates[:50] if len(trading_dates) > 50 else trading_dates

    for i, date in enumerate(test_dates):
        date_str = str(date)[:10]

        if stop_trading_until is not None and date_str < stop_trading_until:
            print(f"[{date_str}] 停手期间，跳过")
            continue
        else:
            stop_trading_until = None

        total_value = capital
        for stock, pos in positions.items():
            try:
                bars = history_bars(stock, 1, "1d", "close", end_dt=date_str)
                if bars is not None:
                    total_value += bars["close"][-1] * pos["shares"]
            except:
                pass

        daily_values.append({"date": date_str, "value": total_value})

        stocks_to_sell = []
        for stock, pos in positions.items():
            try:
                bars = history_bars(stock, 1, "1d", "close", end_dt=date_str)
                if bars is None:
                    continue
                current_price = bars["close"][-1]
                profit_pct = (current_price - pos["buy_price"]) / pos["buy_price"]

                if STRATEGY_MODE == "mainline":
                    if profit_pct >= MAINLINE_PARAMS["sell_profit_threshold"]:
                        stocks_to_sell.append((stock, current_price, "冲高+3%止盈"))
                    elif i > pos["buy_index"]:
                        stocks_to_sell.append((stock, current_price, "尾盘卖出"))
                else:
                    if i > pos["buy_index"]:
                        stocks_to_sell.append((stock, current_price, "次日卖出"))
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
                        "date": date_str,
                        "stock": stock,
                        "action": "sell",
                        "price": price,
                        "profit": profit,
                        "profit_pct": profit_pct,
                        "reason": reason,
                    }
                )

                if profit < 0:
                    consecutive_losses += 1
                else:
                    consecutive_losses = 0

                del positions[stock]
                print(f"[{date_str}] 卖出 {stock}: {reason}, 盈亏 {profit_pct:.2%}")

        if consecutive_losses >= 3:
            stop_trading_until = date_str
            consecutive_losses = 0
            print(f"[{date_str}] 连亏3笔，停手至 {stop_trading_until}")

        if STRATEGY_MODE == "mainline":
            signals = generate_mainline_signals(date_str, all_stocks)
        else:
            signals = generate_observation_signals(date_str, all_stocks)

        if signals and len(positions) < 3:
            signal = signals[0]
            stock = signal["stock"]

            try:
                bars = history_bars(stock, 1, "1d", "close", end_dt=date_str)
                if bars is None:
                    continue
                price = bars["close"][-1]

                max_amount = min(100000, capital)
                shares = int(max_amount / price / 100) * 100

                if shares > 0 and capital >= shares * price:
                    capital -= shares * price
                    positions[stock] = {
                        "buy_date": date_str,
                        "buy_price": price,
                        "shares": shares,
                        "buy_index": i,
                    }
                    trades.append(
                        {
                            "date": date_str,
                            "stock": stock,
                            "action": "buy",
                            "price": price,
                            "shares": shares,
                        }
                    )
                    print(f"[{date_str}] 买入 {stock}: 价格{price:.2f}, 数量{shares}")
            except:
                pass

        if (i + 1) % 10 == 0:
            print(f"\n--- 进度: {i + 1}/{len(test_dates)} ---")
            print(f"总资产: {total_value:.2f}")
            print(f"持仓数: {len(positions)}")
            print(f"交易数: {len(trades)}")

    print("\n" + "=" * 80)
    print("回测结果汇总")
    print("=" * 80)

    if len(daily_values) > 0:
        initial = 100000
        final = daily_values[-1]["value"]
        total_return = (final - initial) / initial

        print(f"总收益率: {total_return:.2%}")
        print(f"最终资产: {final:.2f}")

    sell_trades = [t for t in trades if t["action"] == "sell"]
    if len(sell_trades) > 0:
        wins = [t for t in sell_trades if t["profit"] > 0]
        win_rate = len(wins) / len(sell_trades)
        avg_profit_pct = np.mean([t["profit_pct"] for t in sell_trades])

        print(f"胜率: {win_rate:.2%}")
        print(f"平均收益率: {avg_profit_pct:.2%}")
        print(f"交易次数: {len(sell_trades)}")

    print("\n" + "=" * 80)
    print("回测完成")
    print("=" * 80)
