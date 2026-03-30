# -*- coding: utf-8 -*-
"""
任务07：多策略组合与仓位分配研究
在聚宽研究环境中运行此代码
"""

import numpy as np
import pandas as pd
import datetime as dt
from jqdata import *
from jqfactor import *
import warnings

warnings.filterwarnings("ignore")

# ============================================================================
# 第一部分：四个子策略的简化版本（用于组合分析）
# ============================================================================


def transform_date(date, date_type):
    """日期转换"""
    if type(date) == str:
        str_date = date
        dt_date = dt.datetime.strptime(date, "%Y-%m-%d")
        d_date = dt_date.date()
    elif type(date) == dt.datetime:
        str_date = date.strftime("%Y-%m-%d")
        dt_date = date
        d_date = dt_date.date()
    elif type(date) == dt.date:
        str_date = date.strftime("%Y-%m-%d")
        dt_date = dt.datetime.strptime(str_date, "%Y-%m-%d")
        d_date = date
    return {"str": str_date, "dt": dt_date, "d": d_date}[date_type]


def get_shifted_date(date, days, days_type="T"):
    """获取偏移日期"""
    d_date = transform_date(date, "d")
    yesterday = d_date + dt.timedelta(-1)
    if days_type == "N":
        shifted_date = yesterday + dt.timedelta(days + 1)
    if days_type == "T":
        all_trade_days = [i.strftime("%Y-%m-%d") for i in list(get_all_trade_days())]
        if str(yesterday) in all_trade_days:
            shifted_date = all_trade_days[
                all_trade_days.index(str(yesterday)) + days + 1
            ]
        else:
            for i in range(100):
                last_trade_date = yesterday - dt.timedelta(i)
                if str(last_trade_date) in all_trade_days:
                    shifted_date = all_trade_days[
                        all_trade_days.index(str(last_trade_date)) + days + 1
                    ]
                    break
    return str(shifted_date)


# ============================================================================
# 子策略1：首板低开
# ============================================================================
def strategy_first_board_low_open(date_str):
    """首板低开策略选股"""
    date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()

    try:
        # 基础股票池
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in ["4", "8"] and s[:2] != "68"]

        # 过滤新股
        all_stocks = [
            s for s in all_stocks if (date - get_security_info(s).start_date).days > 60
        ]

        # 过滤ST
        is_st = get_extras(
            "is_st", all_stocks, start_date=date, end_date=date, df=True
        ).T
        is_st.columns = ["is_st"]
        all_stocks = is_st[is_st["is_st"] == False].index.tolist()

        # 获取昨日涨停股
        yesterday = get_trade_days(end_date=date, count=2)[0]
        df = get_price(
            all_stocks,
            end_date=yesterday,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        ).dropna()
        limit_up_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

        # 过滤前日曾涨停
        day_before = get_trade_days(end_date=yesterday, count=2)[0]
        df_prev = get_price(
            limit_up_stocks,
            end_date=day_before,
            frequency="daily",
            fields=["high", "high_limit"],
            count=1,
            panel=False,
        ).dropna()
        ever_limit_prev = df_prev[df_prev["high"] == df_prev["high_limit"]][
            "code"
        ].tolist()
        limit_up_stocks = [s for s in limit_up_stocks if s not in ever_limit_prev]

        # 今日低开筛选 (0% ~ 1%)
        today_data = get_price(
            limit_up_stocks,
            start_date=date,
            end_date=date,
            frequency="daily",
            fields=["open", "pre_close"],
        ).dropna()
        selected = []
        for s in limit_up_stocks:
            if s in today_data.index.get_level_values("code"):
                open_price = today_data.loc[
                    today_data.index.get_level_values("code") == s, "open"
                ].values[0]
                pre_close = today_data.loc[
                    today_data.index.get_level_values("code") == s, "pre_close"
                ].values[0]
                open_ratio = (open_price - pre_close) / pre_close * 100
                if 0 <= open_ratio <= 1:
                    selected.append(s)

        # 相对位置过滤
        final_selected = []
        for s in selected:
            try:
                hist_data = get_price(
                    s, end_date=yesterday, count=15, fields=["high", "low", "close"]
                )
                max_high = hist_data["high"].max()
                min_low = hist_data["low"].min()
                close_price = hist_data["close"].iloc[-1]
                rel_pos = (close_price - min_low) / (max_high - min_low)
                if 0 <= rel_pos <= 0.3:
                    final_selected.append(s)
            except:
                pass

        return final_selected
    except Exception as e:
        print(f"首板低开策略错误: {e}")
        return []


# ============================================================================
# 子策略2：弱转强竞价
# ============================================================================
def strategy_weak_to_strong(date_str):
    """弱转强竞价策略选股"""
    date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()

    try:
        # 基础股票池
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if s[0] not in ["4", "8"] and s[:2] != "68" and s[0] != "3"
        ]

        # 过滤新股
        all_stocks = [
            s for s in all_stocks if (date - get_security_info(s).start_date).days > 50
        ]

        # 过滤ST
        is_st = get_extras(
            "is_st", all_stocks, start_date=date, end_date=date, df=True
        ).T
        is_st.columns = ["is_st"]
        all_stocks = is_st[is_st["is_st"] == False].index.tolist()

        # 获取昨日涨停股
        yesterday = get_trade_days(end_date=date, count=2)[0]
        df = get_price(
            all_stocks,
            end_date=yesterday,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        ).dropna()
        limit_up_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

        # 排除前两日曾涨停
        two_days_ago = get_trade_days(end_date=yesterday, count=3)[0]
        three_days_ago = get_trade_days(end_date=yesterday, count=4)[0]

        df_2d = get_price(
            limit_up_stocks,
            end_date=two_days_ago,
            frequency="daily",
            fields=["high", "high_limit"],
            count=1,
            panel=False,
        ).dropna()
        ever_limit_2d = df_2d[df_2d["high"] == df_2d["high_limit"]]["code"].tolist()

        df_3d = get_price(
            limit_up_stocks,
            end_date=three_days_ago,
            frequency="daily",
            fields=["high", "high_limit"],
            count=1,
            panel=False,
        ).dropna()
        ever_limit_3d = df_3d[df_3d["high"] == df_3d["high_limit"]]["code"].tolist()

        limit_up_stocks = [
            s
            for s in limit_up_stocks
            if s not in ever_limit_2d and s not in ever_limit_3d
        ]

        # 市值和成交额过滤
        final_selected = []
        for s in limit_up_stocks:
            try:
                prev_data = get_price(
                    s,
                    end_date=yesterday,
                    count=1,
                    frequency="daily",
                    fields=["close", "volume", "money"],
                )
                money = prev_data["money"].iloc[0]

                q = query(valuation.market_cap).filter(valuation.code == s)
                mkt_cap = get_fundamentals(q, date=yesterday)

                if (
                    money >= 7e8
                    and not mkt_cap.empty
                    and mkt_cap["market_cap"].iloc[0] >= 70
                ):
                    # 模拟竞价条件
                    volume_data = get_price(
                        s, end_date=yesterday, count=10, fields=["volume"]
                    )
                    if len(volume_data) >= 2:
                        if (
                            volume_data["volume"].iloc[-1]
                            > max(volume_data["volume"].iloc[:-1]) * 0.9
                        ):
                            final_selected.append(s)
            except:
                pass

        return final_selected
    except Exception as e:
        print(f"弱转强策略错误: {e}")
        return []


# ============================================================================
# 子策略3：234板接力
# ============================================================================
def strategy_234_board(date_str):
    """234板接力策略选股"""
    date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()

    try:
        # 基础股票池
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if s[0] not in ["4", "8"] and s[:2] != "68" and s[0] != "3"
        ]

        # 过滤新股(250天)
        all_stocks = [
            s for s in all_stocks if (date - get_security_info(s).start_date).days > 250
        ]

        # 过滤ST
        is_st = get_extras(
            "is_st", all_stocks, start_date=date, end_date=date, df=True
        ).T
        is_st.columns = ["is_st"]
        all_stocks = is_st[is_st["is_st"] == False].index.tolist()

        # 获取近5日涨停数据
        yesterday = get_trade_days(end_date=date, count=6)

        def get_limit_up_stocks(end_date):
            df = get_price(
                all_stocks,
                end_date=end_date,
                frequency="daily",
                fields=["close", "high_limit", "low"],
                count=1,
                panel=False,
            ).dropna()
            limit_up = df[df["close"] == df["high_limit"]]["code"].tolist()
            # 排除一字板
            result = []
            for s in limit_up:
                try:
                    d = get_price(s, end_date=end_date, count=1, fields=["high", "low"])
                    if d["high"].iloc[0] != d["low"].iloc[0]:
                        result.append(s)
                except:
                    pass
            return result

        hl_1d = get_limit_up_stocks(yesterday[-2])  # 昨日
        hl_2d = get_limit_up_stocks(yesterday[-3])  # 前日
        hl_3d = get_limit_up_stocks(yesterday[-4])  # 三日前
        hl_4d = get_limit_up_stocks(yesterday[-5])  # 四日前
        hl_5d = get_limit_up_stocks(yesterday[-6])  # 五日前

        # 二三四板（不含五板）
        stock_list = []
        stock_list.extend(
            list(
                set(hl_1d)
                .intersection(set(hl_2d))
                .intersection(set(hl_3d))
                .intersection(set(hl_4d))
                - set(hl_5d)
            )
        )
        stock_list.extend(
            list(
                set(hl_1d).intersection(set(hl_2d)).intersection(set(hl_3d))
                - set(hl_4d)
                - set(hl_5d)
            )
        )
        stock_list.extend(
            list(
                set(hl_1d).intersection(set(hl_2d))
                - set(hl_3d)
                - set(hl_4d)
                - set(hl_5d)
            )
        )
        stock_list = list(set(stock_list))

        # 换手率过滤
        final_selected = []
        for s in stock_list:
            try:
                yesterday_str = yesterday[-2].strftime("%Y-%m-%d")
                hsl_data = HSL([s], yesterday_str)
                if hsl_data and s in hsl_data[0] and hsl_data[0][s] < 30:
                    # 流通市值过滤
                    q = query(valuation.circulating_market_cap).filter(
                        valuation.code == s
                    )
                    mkt_cap = get_fundamentals(q, date=yesterday[-2])
                    if (
                        not mkt_cap.empty
                        and mkt_cap["circulating_market_cap"].iloc[0] < 50
                    ):
                        final_selected.append(s)
            except:
                pass

        return final_selected
    except Exception as e:
        print(f"234板策略错误: {e}")
        return []


# ============================================================================
# 子策略4：龙头底分型
# ============================================================================
def strategy_leader_bottom_fractal(date_str):
    """龙头底分型策略选股（日级简化版）"""
    date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()

    try:
        # 基础股票池
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in ["4", "8"] and s[:2] != "68"]

        # 过滤新股(3年)
        all_stocks = [
            s
            for s in all_stocks
            if (date - get_security_info(s).start_date).days > 1080
        ]

        # 过滤ST
        is_st = get_extras(
            "is_st", all_stocks, start_date=date, end_date=date, df=True
        ).T
        is_st.columns = ["is_st"]
        all_stocks = is_st[is_st["is_st"] == False].index.tolist()

        # 获取昨日涨停股
        yesterday = get_trade_days(end_date=date, count=2)[0]

        final_selected = []
        for s in all_stocks[:500]:  # 限制检查数量以提高效率
            try:
                # 检查是否昨日涨停
                df = get_price(
                    s,
                    end_date=yesterday,
                    count=1,
                    frequency="daily",
                    fields=["close", "high_limit", "high", "low"],
                )
                if df["close"].iloc[0] != df["high_limit"].iloc[0]:
                    continue

                # 检查主升浪背景(40日涨幅>55%)
                df_40 = get_price(
                    s, end_date=yesterday, count=40, fields=["high", "low", "close"]
                )
                if len(df_40) < 40:
                    continue
                high_40 = df_40["high"].max()
                low_40 = df_40["low"].min()
                rate_40 = (high_40 - low_40) / low_40
                if rate_40 < 0.55 or rate_40 > 3.8:
                    continue

                # 检查80日涨幅
                df_80 = get_price(
                    s, end_date=yesterday, count=80, fields=["high", "low"]
                )
                if len(df_80) < 80:
                    continue
                high_80 = df_80["high"].max()
                low_80 = df_80["low"].min()
                rate_80 = (high_80 - low_80) / low_80
                if rate_80 > 3.8:
                    continue

                # 检查底分型（T-2为十字星）
                df_3 = get_price(
                    s,
                    end_date=yesterday,
                    count=3,
                    fields=["open", "close", "high", "low"],
                )
                if len(df_3) < 3:
                    continue

                close_t2 = df_3["close"].iloc[1]
                open_t2 = df_3["open"].iloc[1]
                high_t2 = df_3["high"].iloc[1]
                low_t2 = df_3["low"].iloc[1]

                # 十字星判断
                rate_body = abs(close_t2 - open_t2) / ((close_t2 + open_t2) / 2)
                rate_range = abs(high_t2 - low_t2) / ((high_t2 + low_t2) / 2)
                if rate_body >= 0.025 or rate_range >= 0.08:
                    continue

                # 60日均线
                df_60 = get_price(s, end_date=yesterday, count=60, fields=["close"])
                if len(df_60) < 60:
                    continue
                ma60 = df_60["close"].mean()
                if close_t2 <= ma60:
                    continue

                final_selected.append(s)
            except:
                pass

        return final_selected
    except Exception as e:
        print(f"龙头底分型策略错误: {e}")
        return []


# ============================================================================
# 第二部分：组合回测引擎
# ============================================================================


def calculate_daily_returns(strategies, start_date, end_date, initial_capital=1000000):
    """
    计算各策略的每日收益率
    strategies: dict, {策略名: 选股函数}
    """
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)

    results = {}
    for name in strategies.keys():
        results[name] = {"dates": [], "returns": [], "positions": [], "signals": []}

    for i in range(1, len(trade_days)):
        date = trade_days[i]
        date_str = date.strftime("%Y-%m-%d")

        for name, func in strategies.items():
            try:
                selected = func(date_str)

                if len(selected) == 0:
                    results[name]["dates"].append(date)
                    results[name]["returns"].append(0)
                    results[name]["positions"].append(0)
                    results[name]["signals"].append(0)
                    continue

                # 计算等权收益
                total_return = 0
                valid_count = 0
                for s in selected:
                    try:
                        # 买入价：今日开盘价
                        # 卖出价：今日收盘价（日内持有）
                        price_data = get_price(
                            s,
                            start_date=date,
                            end_date=date,
                            frequency="daily",
                            fields=["open", "close"],
                        )
                        if not price_data.empty and price_data["open"].iloc[0] > 0:
                            ret = (
                                price_data["close"].iloc[0] - price_data["open"].iloc[0]
                            ) / price_data["open"].iloc[0]
                            total_return += ret
                            valid_count += 1
                    except:
                        pass

                if valid_count > 0:
                    avg_return = total_return / valid_count
                else:
                    avg_return = 0

                results[name]["dates"].append(date)
                results[name]["returns"].append(avg_return)
                results[name]["positions"].append(valid_count)
                results[name]["signals"].append(1 if valid_count > 0 else 0)
            except Exception as e:
                results[name]["dates"].append(date)
                results[name]["returns"].append(0)
                results[name]["positions"].append(0)
                results[name]["signals"].append(0)

        if i % 20 == 0:
            print(f"处理进度: {i}/{len(trade_days)}")

    return results


def calculate_correlation_matrix(results):
    """计算策略间相关性矩阵"""
    returns_df = pd.DataFrame()
    for name, data in results.items():
        returns_df[name] = data["returns"]

    corr_matrix = returns_df.corr()
    return corr_matrix, returns_df


def calculate_strategy_metrics(returns_list, dates_list):
    """计算策略指标"""
    returns = np.array(returns_list)

    # 累计收益
    cum_returns = (1 + returns).cumprod()
    total_return = cum_returns[-1] - 1

    # 年化收益
    trading_days = len(returns)
    annual_return = (1 + total_return) ** (252 / trading_days) - 1

    # 最大回撤
    cum_max = np.maximum.accumulate(cum_returns)
    drawdowns = (cum_max - cum_returns) / cum_max
    max_drawdown = np.max(drawdowns)

    # 夏普比率
    daily_rf = 0.03 / 252  # 假设无风险利率3%
    excess_returns = returns - daily_rf
    sharpe = np.mean(excess_returns) / (np.std(returns) + 1e-10) * np.sqrt(252)

    # 胜率
    win_rate = np.sum(returns > 0) / (np.sum(returns != 0) + 1e-10)

    # 信号频率
    signal_days = np.sum(returns != 0)
    signal_freq = signal_days / trading_days

    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "win_rate": win_rate,
        "signal_freq": signal_freq,
        "trading_days": trading_days,
        "signal_days": signal_days,
    }


# ============================================================================
# 第三部分：组合方案设计
# ============================================================================


def portfolio_fixed_weight(returns_df, weights):
    """
    固定权重组合
    weights: dict, {策略名: 权重}
    """
    portfolio_returns = np.zeros(len(returns_df))

    for name, weight in weights.items():
        if name in returns_df.columns:
            portfolio_returns += returns_df[name].values * weight

    return portfolio_returns


def portfolio_dynamic_weight(returns_df, lookback=60):
    """
    动态权重组合（基于近期表现）
    """
    n_strategies = len(returns_df.columns)
    portfolio_returns = np.zeros(len(returns_df))
    weights_history = []

    for i in range(lookback, len(returns_df)):
        # 使用过去lookback天的数据计算权重
        recent_returns = returns_df.iloc[i - lookback : i]

        # 计算每个策略的夏普比率作为权重依据
        sharpe_scores = []
        for col in returns_df.columns:
            ret = recent_returns[col].values
            if np.std(ret) > 1e-10:
                sharpe = np.mean(ret) / np.std(ret)
            else:
                sharpe = 0
            sharpe_scores.append(max(sharpe, 0))  # 只保留正夏普

        # 归一化权重
        total_score = sum(sharpe_scores)
        if total_score > 0:
            weights = [s / total_score for s in sharpe_scores]
        else:
            weights = [1 / n_strategies] * n_strategies

        weights_history.append(dict(zip(returns_df.columns, weights)))

        # 计算当日组合收益
        for j, col in enumerate(returns_df.columns):
            portfolio_returns[i] += returns_df[col].iloc[i] * weights[j]

    return portfolio_returns, weights_history


def portfolio_emotion_based(returns_df, emotion_scores, emotion_thresholds):
    """
    基于情绪的动态切换组合
    emotion_scores: 每日情绪得分
    emotion_thresholds: 情绪阈值配置
    """
    portfolio_returns = np.zeros(len(returns_df))

    # 定义不同情绪状态下的权重
    high_emotion_weights = {
        "first_board": 0.1,
        "weak_to_strong": 0.3,
        "board_234": 0.4,
        "bottom_fractal": 0.2,
    }
    mid_emotion_weights = {
        "first_board": 0.25,
        "weak_to_strong": 0.25,
        "board_234": 0.2,
        "bottom_fractal": 0.3,
    }
    low_emotion_weights = {
        "first_board": 0.3,
        "weak_to_strong": 0.1,
        "board_234": 0.1,
        "bottom_fractal": 0.5,
    }

    for i in range(len(returns_df)):
        if i >= len(emotion_scores):
            emotion = "mid"
        elif emotion_scores[i] > emotion_thresholds["high"]:
            emotion = "high"
        elif emotion_scores[i] < emotion_thresholds["low"]:
            emotion = "low"
        else:
            emotion = "mid"

        weights = {
            "high": high_emotion_weights,
            "mid": mid_emotion_weights,
            "low": low_emotion_weights,
        }[emotion]

        for j, col in enumerate(returns_df.columns):
            if col in weights:
                portfolio_returns[i] += returns_df[col].iloc[i] * weights[col]

    return portfolio_returns


# ============================================================================
# 第四部分：滚动训练与样本外验证
# ============================================================================


def rolling_validation(strategies, start_date, end_date, train_months=24, val_months=6):
    """
    滚动训练与验证
    """
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)

    # 计算训练和验证的日期边界
    train_days = int(train_months * 21)  # 约21个交易日/月
    val_days = int(val_months * 21)

    rolling_results = []

    i = 0
    while i + train_days + val_days <= len(trade_days):
        train_start = trade_days[i].strftime("%Y-%m-%d")
        train_end = trade_days[i + train_days - 1].strftime("%Y-%m-%d")
        val_start = trade_days[i + train_days].strftime("%Y-%m-%d")
        val_end = trade_days[
            min(i + train_days + val_days - 1, len(trade_days) - 1)
        ].strftime("%Y-%m-%d")

        print(f"\n=== 滚动窗口 {i // val_days + 1} ===")
        print(f"训练期: {train_start} ~ {train_end}")
        print(f"验证期: {val_start} ~ {val_end}")

        # 训练期分析
        train_results = calculate_daily_returns(strategies, train_start, train_end)
        corr_matrix, train_returns = calculate_correlation_matrix(train_results)

        # 计算训练期最优固定权重（基于夏普比率）
        sharpe_scores = {}
        for name in strategies.keys():
            metrics = calculate_strategy_metrics(
                train_returns[name].values, list(range(len(train_returns)))
            )
            sharpe_scores[name] = max(metrics["sharpe"], 0)

        total_sharpe = sum(sharpe_scores.values())
        if total_sharpe > 0:
            optimal_weights = {k: v / total_sharpe for k, v in sharpe_scores.items()}
        else:
            optimal_weights = {k: 1 / len(strategies) for k in strategies.keys()}

        # 验证期测试
        val_results = calculate_daily_returns(strategies, val_start, val_end)
        _, val_returns = calculate_correlation_matrix(val_results)

        # 计算各方案在验证期的表现
        # 方案1：单策略最优
        best_strategy = max(sharpe_scores, key=sharpe_scores.get)
        single_best_returns = val_returns[best_strategy].values
        single_best_metrics = calculate_strategy_metrics(
            single_best_returns, list(range(len(single_best_returns)))
        )

        # 方案2：固定权重
        equal_weights = {k: 1 / len(strategies) for k in strategies.keys()}
        fixed_weight_returns = portfolio_fixed_weight(val_returns, equal_weights)
        fixed_metrics = calculate_strategy_metrics(
            fixed_weight_returns, list(range(len(fixed_weight_returns)))
        )

        # 方案3：动态权重
        if len(val_returns) > 60:
            dynamic_returns, _ = portfolio_dynamic_weight(
                val_returns, lookback=min(60, len(val_returns) // 2)
            )
            dynamic_metrics = calculate_strategy_metrics(
                dynamic_returns, list(range(len(dynamic_returns)))
            )
        else:
            dynamic_returns = fixed_weight_returns
            dynamic_metrics = fixed_metrics

        rolling_results.append(
            {
                "train_start": train_start,
                "train_end": train_end,
                "val_start": val_start,
                "val_end": val_end,
                "correlation": corr_matrix,
                "optimal_weights": optimal_weights,
                "single_best": {"name": best_strategy, "metrics": single_best_metrics},
                "fixed_weight": {"metrics": fixed_metrics},
                "dynamic_weight": {"metrics": dynamic_metrics},
            }
        )

        i += val_days

    return rolling_results


# ============================================================================
# 第五部分：主程序
# ============================================================================

print("=" * 80)
print("任务07：多策略组合与仓位分配研究")
print("=" * 80)

# 定义策略
strategies = {
    "first_board": strategy_first_board_low_open,
    "weak_to_strong": strategy_weak_to_strong,
    "board_234": strategy_234_board,
    "bottom_fractal": strategy_leader_bottom_fractal,
}

# 测试日期范围
start_date = "2021-01-01"
end_date = "2025-12-31"

print(f"\n测试日期范围: {start_date} ~ {end_date}")

# 第一阶段：全样本分析
print("\n" + "=" * 80)
print("第一阶段：全样本相关性分析")
print("=" * 80)

full_results = calculate_daily_returns(strategies, start_date, end_date)
corr_matrix, returns_df = calculate_correlation_matrix(full_results)

print("\n策略相关性矩阵:")
print(corr_matrix)

# 计算各策略指标
print("\n各策略独立表现:")
strategy_metrics = {}
for name in strategies.keys():
    metrics = calculate_strategy_metrics(
        returns_df[name].values, list(range(len(returns_df)))
    )
    strategy_metrics[name] = metrics
    print(f"\n{name}:")
    print(f"  年化收益: {metrics['annual_return'] * 100:.2f}%")
    print(f"  最大回撤: {metrics['max_drawdown'] * 100:.2f}%")
    print(f"  夏普比率: {metrics['sharpe']:.2f}")
    print(f"  胜率: {metrics['win_rate'] * 100:.2f}%")
    print(f"  信号频率: {metrics['signal_freq'] * 100:.2f}%")

# 第二阶段：组合方案测试
print("\n" + "=" * 80)
print("第二阶段：组合方案测试")
print("=" * 80)

# 方案1：等权组合
equal_weights = {k: 0.25 for k in strategies.keys()}
equal_weight_returns = portfolio_fixed_weight(returns_df, equal_weights)
equal_metrics = calculate_strategy_metrics(
    equal_weight_returns, list(range(len(equal_weight_returns)))
)

print("\n方案1：等权组合 (25% × 4)")
print(f"  年化收益: {equal_metrics['annual_return'] * 100:.2f}%")
print(f"  最大回撤: {equal_metrics['max_drawdown'] * 100:.2f}%")
print(f"  夏普比率: {equal_metrics['sharpe']:.2f}")

# 方案2：基于夏普比率的固定权重
sharpe_weights = {}
for name, metrics in strategy_metrics.items():
    sharpe_weights[name] = max(metrics["sharpe"], 0)
total = sum(sharpe_weights.values())
if total > 0:
    sharpe_weights = {k: v / total for k, v in sharpe_weights.items()}

sharpe_weight_returns = portfolio_fixed_weight(returns_df, sharpe_weights)
sharpe_metrics = calculate_strategy_metrics(
    sharpe_weight_returns, list(range(len(sharpe_weight_returns)))
)

print("\n方案2：夏普比率加权组合")
print(f"  权重: {sharpe_weights}")
print(f"  年化收益: {sharpe_metrics['annual_return'] * 100:.2f}%")
print(f"  最大回撤: {sharpe_metrics['max_drawdown'] * 100:.2f}%")
print(f"  夏普比率: {sharpe_metrics['sharpe']:.2f}")

# 方案3：动态权重组合
if len(returns_df) > 60:
    dynamic_returns, weights_history = portfolio_dynamic_weight(returns_df, lookback=60)
    dynamic_metrics = calculate_strategy_metrics(
        dynamic_returns, list(range(len(dynamic_returns)))
    )

    print("\n方案3：动态权重组合 (60日滚动)")
    print(f"  年化收益: {dynamic_metrics['annual_return'] * 100:.2f}%")
    print(f"  最大回撤: {dynamic_metrics['max_drawdown'] * 100:.2f}%")
    print(f"  夏普比率: {dynamic_metrics['sharpe']:.2f}")

# 第三阶段：滚动验证
print("\n" + "=" * 80)
print("第三阶段：滚动训练与样本外验证")
print("=" * 80)

rolling_results = rolling_validation(
    strategies, start_date, end_date, train_months=24, val_months=6
)

# 汇总滚动验证结果
print("\n" + "=" * 80)
print("滚动验证汇总")
print("=" * 80)

for i, result in enumerate(rolling_results):
    print(
        f"\n--- 滚动窗口 {i + 1}: 验证期 {result['val_start']} ~ {result['val_end']} ---"
    )
    print(
        f"单策略最优 ({result['single_best']['name']}): "
        f"年化 {result['single_best']['metrics']['annual_return'] * 100:.2f}%, "
        f"回撤 {result['single_best']['metrics']['max_drawdown'] * 100:.2f}%"
    )
    print(
        f"等权组合: "
        f"年化 {result['fixed_weight']['metrics']['annual_return'] * 100:.2f}%, "
        f"回撤 {result['fixed_weight']['metrics']['max_drawdown'] * 100:.2f}%"
    )
    print(
        f"动态组合: "
        f"年化 {result['dynamic_weight']['metrics']['annual_return'] * 100:.2f}%, "
        f"回撤 {result['dynamic_weight']['metrics']['max_drawdown'] * 100:.2f}%"
    )

# 第四阶段：2024年后样本外结果
print("\n" + "=" * 80)
print("第四阶段：2024-01-01之后样本外结果")
print("=" * 80)

oos_results = calculate_daily_returns(strategies, "2024-01-01", "2025-12-31")
oos_corr, oos_returns = calculate_correlation_matrix(oos_results)

print("\n样本外相关性矩阵:")
print(oos_corr)

print("\n样本外各策略表现:")
for name in strategies.keys():
    metrics = calculate_strategy_metrics(
        oos_returns[name].values, list(range(len(oos_returns)))
    )
    print(f"\n{name}:")
    print(f"  年化收益: {metrics['annual_return'] * 100:.2f}%")
    print(f"  最大回撤: {metrics['max_drawdown'] * 100:.2f}%")
    print(f"  夏普比率: {metrics['sharpe']:.2f}")

# 样本外组合测试
oos_equal_returns = portfolio_fixed_weight(oos_returns, equal_weights)
oos_equal_metrics = calculate_strategy_metrics(
    oos_equal_returns, list(range(len(oos_equal_returns)))
)

print("\n样本外等权组合:")
print(f"  年化收益: {oos_equal_metrics['annual_return'] * 100:.2f}%")
print(f"  最大回撤: {oos_equal_metrics['max_drawdown'] * 100:.2f}%")
print(f"  夏普比率: {oos_equal_metrics['sharpe']:.2f}")

# 保存结果
import json

output_data = {
    "full_sample": {
        "correlation": corr_matrix.to_dict(),
        "strategy_metrics": {
            k: {kk: float(vv) for kk, vv in v.items()}
            for k, v in strategy_metrics.items()
        },
        "equal_weight_metrics": {k: float(v) for k, v in equal_metrics.items()},
        "sharpe_weight_metrics": {k: float(v) for k, v in sharpe_metrics.items()},
    },
    "rolling_validation": [
        {
            "train_period": f"{r['train_start']} ~ {r['train_end']}",
            "val_period": f"{r['val_start']} ~ {r['val_end']}",
            "single_best": {
                "name": r["single_best"]["name"],
                "metrics": {
                    k: float(v) for k, v in r["single_best"]["metrics"].items()
                },
            },
            "fixed_weight": {
                "metrics": {
                    k: float(v) for k, v in r["fixed_weight"]["metrics"].items()
                }
            },
            "dynamic_weight": {
                "metrics": {
                    k: float(v) for k, v in r["dynamic_weight"]["metrics"].items()
                }
            },
        }
        for r in rolling_results
    ],
    "out_of_sample_2024": {
        "correlation": oos_corr.to_dict(),
        "equal_weight_metrics": {k: float(v) for k, v in oos_equal_metrics.items()},
    },
}

with open("/home/jquser/portfolio_combination_07_results.json", "w") as f:
    json.dump(output_data, f, indent=2)

print("\n" + "=" * 80)
print("分析完成！结果已保存。")
print("=" * 80)
