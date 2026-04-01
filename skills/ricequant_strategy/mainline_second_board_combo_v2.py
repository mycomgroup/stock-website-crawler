"""
主线二板组合测试 - 策略编辑器版本 (RiceQuant)
验证主线（假弱高开）与二板的组合使用效果
"""

import numpy as np
import pandas as pd
from datetime import datetime


def init(context):
    """初始化策略"""
    print("=" * 80)
    print("主线二板组合测试 - 策略编辑器版本")
    print("=" * 80)

    # 策略参数
    context.mainline_weight = 0.5  # 主线仓位
    context.second_board_weight = 0.5  # 二板仓位
    context.scheme = "C"  # 组合方案：A-主线优先，B-二板优先，C-并行独立，D-收益优先

    # 全局状态
    context.mainline_trades = []
    context.second_board_trades = []
    context.combo_trades = []
    context.portfolio_value = 1.0
    context.daily_signals = {}

    # 每日运行
    scheduler.run_daily(rebalance, time_rule=market_open(minute=1))

    print(f"组合方案: {context.scheme}")
    print(f"主线仓位: {context.mainline_weight * 100}%")
    print(f"二板仓位: {context.second_board_weight * 100}%")
    print("=" * 80)


def get_mainline_signals(context, bar_dict):
    """获取主线信号（假弱高开）"""
    signals = []

    try:
        # 获取所有股票
        all_stocks = all_instruments("CS")

        # 简化：取前200只股票检查
        check_stocks = all_stocks[:200]

        for stock in check_stocks:
            try:
                # 获取昨日数据
                prices = history_bars(stock, 2, "1d", ["close", "high_limit"])
                if prices is None or len(prices) < 2:
                    continue

                prev_close = prices[-2]["close"]
                prev_limit = prices[-2]["high_limit"]

                # 判断是否涨停（接近涨停价）
                if abs(prev_close - prev_limit) / prev_limit > 0.005:
                    continue

                # 今日开盘价
                if stock not in bar_dict:
                    continue
                curr_open = bar_dict[stock].open

                # 计算开盘涨幅
                open_pct = (curr_open - prev_close) / prev_close * 100

                # 假弱高开条件：+0.5% ~ +1.5%
                if 0.5 <= open_pct <= 1.5:
                    curr_close = bar_dict[stock].close
                    curr_high = bar_dict[stock].high

                    # 计算日内收益
                    intra_return = (curr_close - curr_open) / curr_open * 100
                    max_return = (curr_high - curr_open) / curr_open * 100

                    signals.append(
                        {
                            "stock": stock,
                            "open_pct": open_pct,
                            "return": intra_return,
                            "max_return": max_return,
                        }
                    )
            except:
                continue

        return signals
    except Exception as e:
        print(f"主线信号获取错误: {e}")
        return []


def get_second_board_signals(context, bar_dict):
    """获取二板信号"""
    signals = []

    try:
        all_stocks = all_instruments("CS")
        check_stocks = all_stocks[:200]

        for stock in check_stocks:
            try:
                # 获取近3日数据
                prices = history_bars(
                    stock, 3, "1d", ["close", "high_limit", "low", "high"]
                )
                if prices is None or len(prices) < 3:
                    continue

                # 检查是否为二板
                d1_close = prices[-2]["close"]  # 昨日
                d1_limit = prices[-2]["high_limit"]
                d2_close = prices[-3]["close"]  # 前日
                d2_limit = prices[-3]["high_limit"]

                # 昨日涨停
                if abs(d1_close - d1_limit) / d1_limit > 0.005:
                    continue

                # 前日也涨停
                if abs(d2_close - d2_limit) / d2_limit > 0.005:
                    continue

                # 非一字板
                d1_low = prices[-2]["low"]
                d1_high = prices[-2]["high"]
                if d1_low == d1_high:
                    continue

                # 今日开盘价
                if stock not in bar_dict:
                    continue
                curr_open = bar_dict[stock].open
                curr_limit = bar_dict[stock].limit_up

                # 非涨停开盘
                if curr_open >= curr_limit * 0.99:
                    continue

                # 计算收益
                buy_price = curr_open * 1.005
                curr_high = bar_dict[stock].high
                curr_close = bar_dict[stock].close
                sell_price = max(curr_high, curr_close)

                profit_pct = (sell_price / buy_price - 1) * 100

                signals.append(
                    {
                        "stock": stock,
                        "return": profit_pct,
                    }
                )
            except:
                continue

        return signals
    except Exception as e:
        print(f"二板信号获取错误: {e}")
        return []


def execute_combo_strategy(context, bar_dict, mainline_signals, second_board_signals):
    """执行组合策略"""
    scheme = context.scheme

    if scheme == "A":  # 主线优先
        if len(mainline_signals) > 0:
            best = max(mainline_signals, key=lambda x: x["return"])
            return best["return"], "mainline"
        elif len(second_board_signals) > 0:
            best = max(second_board_signals, key=lambda x: x["return"])
            return best["return"], "second_board"

    elif scheme == "B":  # 二板优先
        if len(second_board_signals) > 0:
            best = max(second_board_signals, key=lambda x: x["return"])
            return best["return"], "second_board"
        elif len(mainline_signals) > 0:
            best = max(mainline_signals, key=lambda x: x["return"])
            return best["return"], "mainline"

    elif scheme == "C":  # 并行独立（等权）
        returns = []
        if len(mainline_signals) > 0:
            ml_avg = np.mean([s["return"] for s in mainline_signals])
            returns.append(ml_avg * context.mainline_weight)
        if len(second_board_signals) > 0:
            sb_avg = np.mean([s["return"] for s in second_board_signals])
            returns.append(sb_avg * context.second_board_weight)

        if len(returns) > 0:
            total_return = sum(returns)
            return total_return, "both"

    elif scheme == "D":  # 收益优先
        ml_best = None
        sb_best = None

        if len(mainline_signals) > 0:
            ml_best = max(mainline_signals, key=lambda x: x["return"])
        if len(second_board_signals) > 0:
            sb_best = max(second_board_signals, key=lambda x: x["return"])

        if ml_best and sb_best:
            if ml_best["return"] >= sb_best["return"]:
                return ml_best["return"], "mainline"
            else:
                return sb_best["return"], "second_board"
        elif ml_best:
            return ml_best["return"], "mainline"
        elif sb_best:
            return sb_best["return"], "second_board"

    return None, None


def rebalance(context, bar_dict):
    """每日调仓"""
    current_date = context.now.strftime("%Y-%m-%d")

    # 获取信号
    mainline_signals = get_mainline_signals(context, bar_dict)
    second_board_signals = get_second_board_signals(context, bar_dict)

    # 记录每日信号
    context.daily_signals[current_date] = {
        "mainline": len(mainline_signals),
        "second_board": len(second_board_signals),
    }

    # 执行组合策略
    trade_return, source = execute_combo_strategy(
        context, bar_dict, mainline_signals, second_board_signals
    )

    if trade_return is not None:
        # 记录交易
        trade = {
            "date": current_date,
            "return": trade_return,
            "source": source,
        }
        context.combo_trades.append(trade)

        # 更新组合价值
        context.portfolio_value *= 1 + trade_return / 100

        # 记录各策略的交易
        if source in ["mainline", "both"]:
            for s in mainline_signals:
                context.mainline_trades.append(
                    {
                        "date": current_date,
                        "stock": s["stock"],
                        "return": s["return"],
                    }
                )

        if source in ["second_board", "both"]:
            for s in second_board_signals:
                context.second_board_trades.append(
                    {
                        "date": current_date,
                        "stock": s["stock"],
                        "return": s["return"],
                    }
                )


def after_trading(context):
    """盘后统计"""
    current_date = context.now.strftime("%Y-%m-%d")

    # 每30天打印一次统计
    if len(context.combo_trades) > 0 and len(context.combo_trades) % 30 == 0:
        print(f"\n{'=' * 60}")
        print(f"日期: {current_date}")
        print(f"组合交易次数: {len(context.combo_trades)}")
        print(f"当前组合价值: {context.portfolio_value:.2f}")

        if len(context.combo_trades) > 0:
            returns = [t["return"] for t in context.combo_trades]
            win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
            avg_return = np.mean(returns)
            print(f"胜率: {win_rate:.2f}%")
            print(f"平均收益: {avg_return:.2f}%")
        print(f"{'=' * 60}\n")


def after_backtest(context, indicator):
    """回测结束后统计"""
    print("\n" + "=" * 80)
    print("主线二板组合测试 - 回测结果")
    print("=" * 80)

    # 主线统计
    print("\n【主线（假弱高开）统计】")
    print(f"  交易次数: {len(context.mainline_trades)}")
    if len(context.mainline_trades) > 0:
        returns = [t["return"] for t in context.mainline_trades]
        win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
        avg_return = np.mean(returns)
        print(f"  胜率: {win_rate:.2f}%")
        print(f"  平均收益: {avg_return:.2f}%")
        print(f"  累计收益: {sum(returns):.2f}%")

    # 二板统计
    print("\n【二板统计】")
    print(f"  交易次数: {len(context.second_board_trades)}")
    if len(context.second_board_trades) > 0:
        returns = [t["return"] for t in context.second_board_trades]
        win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
        avg_return = np.mean(returns)
        print(f"  胜率: {win_rate:.2f}%")
        print(f"  平均收益: {avg_return:.2f}%")
        print(f"  累计收益: {sum(returns):.2f}%")

    # 组合统计
    print("\n【组合策略统计】")
    print(f"  交易次数: {len(context.combo_trades)}")
    print(f"  组合方案: {context.scheme}")
    print(f"  最终组合价值: {context.portfolio_value:.2f}")

    if len(context.combo_trades) > 0:
        returns = [t["return"] for t in context.combo_trades]
        win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
        avg_return = np.mean(returns)
        total_return = (context.portfolio_value - 1.0) * 100

        # 计算最大回撤
        cumulative = []
        cum = 1.0
        for r in returns:
            cum *= 1 + r / 100
            cumulative.append(cum)

        peak = 1.0
        max_dd = 0
        for c in cumulative:
            peak = max(peak, c)
            dd = (peak - c) / peak * 100
            max_dd = max(max_dd, dd)

        # 计算卡玛比率
        calmar = total_return / max_dd if max_dd > 0 else 0

        print(f"  胜率: {win_rate:.2f}%")
        print(f"  平均收益: {avg_return:.2f}%")
        print(f"  累计收益: {total_return:.2f}%")
        print(f"  最大回撤: {max_dd:.2f}%")
        print(f"  卡玛比率: {calmar:.2f}")

        # 信号来源分布
        ml_count = len([t for t in context.combo_trades if t["source"] == "mainline"])
        sb_count = len(
            [t for t in context.combo_trades if t["source"] == "second_board"]
        )
        both_count = len([t for t in context.combo_trades if t["source"] == "both"])

        print(f"\n  信号来源分布:")
        print(
            f"    主线: {ml_count} ({ml_count / len(context.combo_trades) * 100:.1f}%)"
        )
        print(
            f"    二板: {sb_count} ({sb_count / len(context.combo_trades) * 100:.1f}%)"
        )
        print(
            f"    两者: {both_count} ({both_count / len(context.combo_trades) * 100:.1f}%)"
        )

    # 每日信号统计
    print("\n【每日信号统计】")
    total_days = len(context.daily_signals)
    ml_signal_days = len(
        [d for d in context.daily_signals.values() if d["mainline"] > 0]
    )
    sb_signal_days = len(
        [d for d in context.daily_signals.values() if d["second_board"] > 0]
    )

    print(f"  总交易日: {total_days}")
    print(
        f"  有主线信号天数: {ml_signal_days} ({ml_signal_days / total_days * 100:.1f}%)"
    )
    print(
        f"  有二板信号天数: {sb_signal_days} ({sb_signal_days / total_days * 100:.1f}%)"
    )

    print("\n【RiceQuant 系统指标】")
    print(f"  总收益: {indicator.get('total_returns', 0):.2f}%")
    print(f"  年化收益: {indicator.get('annualized_returns', 0):.2f}%")
    print(f"  最大回撤: {indicator.get('max_drawdown', 0):.2f}%")
    print(f"  夏普比率: {indicator.get('sharpe', 0):.2f}")

    print("\n" + "=" * 80)
    print("回测完成")
    print("=" * 80)
