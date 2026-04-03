"""
小市值防守线 v3 本地回测脚本
使用akshare获取数据，不依赖JoinQuant API

回测期间：
- IS期：2018-01-01 ~ 2022-04-01
- OOS期：2022-04-01 ~ 2025-03-30

策略逻辑：
- 完全复制v1参数（市值15-60亿，PB<1.5，PE<20，持仓15只）
- 新增：个股止损15%，组合止损20%
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import time
from pathlib import Path

# ============================================================
# 配置参数
# ============================================================

# 策略参数（v1基础 + v3止损）
STRATEGY_PARAMS = {
    "min_cap": 15,  # 最小市值（亿）
    "max_cap": 60,  # 最大市值（亿）
    "ipo_days": 180,  # 上市天数过滤
    "max_pb": 1.5,  # PB上限
    "max_pe": 20,  # PE上限
    "hold_num": 15,  # 持仓数量
    "stop_loss_individual": -0.15,  # 个股止损
    "stop_loss_portfolio": -0.20,  # 组合止损
}

# 回测配置
BACKTEST_CONFIG = {
    "start_date": "2018-01-01",
    "end_date": "2025-03-30",
    "oos_start": "2022-04-01",
    "initial_capital": 1000000,
    "commission": 0.0003,
    "stamp_tax": 0.001,
    "slippage": 0.002,
}

# 缓存目录
CACHE_DIR = Path("./cache/smallcap_v3")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 数据获取模块
# ============================================================


def get_all_a_stocks():
    """获取全A股列表"""
    cache_file = CACHE_DIR / "all_a_stocks.csv"
    if cache_file.exists():
        return pd.read_csv(cache_file, dtype={"code": str})

    try:
        # 获取沪深A股列表
        df_sh = ak.stock_info_sh_name_code(symbol="主板A股")
        df_sz = ak.stock_info_sz_name_code(symbol="A股列表")

        all_stocks = []
        for _, row in df_sh.iterrows():
            code = row.get("证券代码", row.get("CON_CODE", ""))
            name = row.get("证券简称", row.get("CON_NAME", ""))
            if code and not code.startswith("688"):
                all_stocks.append({"code": code, "name": name, "market": "SH"})

        for _, row in df_sz.iterrows():
            code = row.get("证券代码", row.get("CON_CODE", ""))
            name = row.get("证券简称", row.get("CON_NAME", ""))
            if code:
                all_stocks.append({"code": code, "name": name, "market": "SZ"})

        df = pd.DataFrame(all_stocks)
        df.to_csv(cache_file, index=False)
        return df
    except Exception as e:
        print(f"获取A股列表失败: {e}")
        return pd.DataFrame()


def get_stock_info(stock_code):
    """获取个股基本信息（上市日期等）"""
    cache_file = CACHE_DIR / f"info_{stock_code}.csv"
    if cache_file.exists():
        return pd.read_csv(cache_file)

    try:
        # 获取历史数据（包含上市信息）
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date="20000101",
            end_date="20250330",
            adjust="qfq",
        )
        if len(df) > 0:
            df.to_csv(cache_file, index=False)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"获取{stock_code}信息失败: {e}")
        return pd.DataFrame()


def get_stock_market_cap(stock_code, date):
    """获取个股在指定日期的市值（亿）"""
    try:
        # 使用akshare获取实时行情数据
        df = ak.stock_zh_a_spot_em()
        stock_row = df[df["代码"] == stock_code]
        if len(stock_row) > 0:
            return stock_row.iloc[0]["流通市值"] / 1e8
        return None
    except:
        return None


def get_stock_fundamentals(stock_code):
    """获取个股财务数据（PE、PB等）"""
    cache_file = CACHE_DIR / f"fundamentals_{stock_code}.csv"
    if cache_file.exists():
        return pd.read_csv(cache_file)

    try:
        # 获取个股估值指标
        df = ak.stock_a_indicator_lg(symbol=stock_code)
        if len(df) > 0:
            df.to_csv(cache_file, index=False)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"获取{stock_code}财务数据失败: {e}")
        return pd.DataFrame()


def get_stock_price(stock_code, start_date, end_date):
    """获取个股历史价格"""
    cache_file = CACHE_DIR / f"price_{stock_code}_{start_date}_{end_date}.csv"
    if cache_file.exists():
        return pd.read_csv(cache_file, parse_dates=["日期"])

    try:
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date.replace("-", ""),
            end_date=end_date.replace("-", ""),
            adjust="qfq",
        )
        if len(df) > 0:
            df.to_csv(cache_file, index=False)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"获取{stock_code}价格失败: {e}")
        return pd.DataFrame()


# ============================================================
# 选股逻辑
# ============================================================


def screen_stocks(date):
    """
    选股逻辑（简化版，基于akshare）
    返回符合条件的股票列表
    """
    print(f"\n筛选日期: {date}")

    # 1. 获取全市场实时数据（包含市值、PE、PB）
    try:
        df = ak.stock_zh_a_spot_em()
        print(f"全市场股票数: {len(df)}")
    except Exception as e:
        print(f"获取实时数据失败: {e}")
        return []

    # 2. 过滤条件
    # 流通市值在15-60亿之间
    df = df[
        (df["流通市值"] >= STRATEGY_PARAMS["min_cap"] * 1e8)
        & (df["流通市值"] <= STRATEGY_PARAMS["max_cap"] * 1e8)
    ]
    print(f"市值过滤后: {len(df)}")

    # PE在0-20之间
    df = df[(df["市盈率-动态"] > 0) & (df["市盈率-动态"] < STRATEGY_PARAMS["max_pe"])]
    print(f"PE过滤后: {len(df)}")

    # PB在0-1.5之间
    df = df[(df["市净率"] > 0) & (df["市净率"] < STRATEGY_PARAMS["max_pb"])]
    print(f"PB过滤后: {len(df)}")

    # 3. 过滤ST、科创板
    df = df[~df["名称"].str.contains("ST|退", na=False)]
    df = df[~df["代码"].str.startswith("688")]
    print(f"ST/科创板过滤后: {len(df)}")

    if len(df) == 0:
        return []

    # 4. 按PB+PE综合排名
    df["pb_rank"] = df["市净率"].rank(pct=True)
    df["pe_rank"] = df["市盈率-动态"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    # 5. 选择最低估的hold_num只
    df = df.sort_values("value_score", ascending=True)
    selected = df.head(STRATEGY_PARAMS["hold_num"])

    print(f"最终选股: {len(selected)}")
    return selected[
        ["代码", "名称", "流通市值", "市盈率-动态", "市净率", "value_score"]
    ].to_dict("records")


# ============================================================
# 回测引擎
# ============================================================


def run_backtest():
    """运行完整回测"""
    print("=" * 70)
    print("小市值防守线 v3 本地回测")
    print("=" * 70)
    print(f"策略参数: {STRATEGY_PARAMS}")
    print(f"回测配置: {BACKTEST_CONFIG}")

    # 初始化
    capital = BACKTEST_CONFIG["initial_capital"]
    initial_capital = capital
    max_capital = capital
    positions = {}  # {stock_code: {"shares": x, "cost": y, "date": z}}
    daily_records = []
    trade_records = []
    stop_loss_records = []

    # 获取交易日
    start_date = BACKTEST_CONFIG["start_date"]
    end_date = BACKTEST_CONFIG["end_date"]
    oos_start = BACKTEST_CONFIG["oos_start"]

    print(f"\n回测期间: {start_date} ~ {end_date}")
    print(f"OOS期间: {oos_start} ~ {end_date}")

    # 简化回测：月度调仓
    # 获取2018-2025年每月第一个交易日
    trade_dates = pd.bdate_range(start=start_date, end=end_date, freq="MS")
    print(f"调仓次数: {len(trade_dates)}")

    for i, date in enumerate(trade_dates):
        date_str = date.strftime("%Y-%m-%d")
        print(f"\n{'=' * 50}")
        print(f"调仓日 {i + 1}/{len(trade_dates)}: {date_str}")

        # 1. 检查止损
        for stock_code in list(positions.keys()):
            pos = positions[stock_code]
            try:
                # 获取最新价格
                price_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=date_str.replace("-", ""),
                    end_date=date_str.replace("-", ""),
                    adjust="qfq",
                )
                if len(price_df) > 0:
                    current_price = price_df.iloc[0]["收盘"]
                    pnl = (current_price - pos["cost"]) / pos["cost"]

                    # 个股止损
                    if pnl < STRATEGY_PARAMS["stop_loss_individual"]:
                        # 卖出
                        sell_value = pos["shares"] * current_price
                        sell_cost = sell_value * (
                            BACKTEST_CONFIG["commission"] + BACKTEST_CONFIG["stamp_tax"]
                        )
                        capital += sell_value - sell_cost

                        stop_loss_records.append(
                            {
                                "date": date_str,
                                "stock": stock_code,
                                "pnl": pnl,
                                "type": "individual_stop_loss",
                            }
                        )
                        print(f"  个股止损: {stock_code}, 亏损: {pnl:.2%}")
                        del positions[stock_code]
            except Exception as e:
                print(f"  检查{stock_code}止损失败: {e}")

        # 组合止损
        total_value = capital
        for stock_code, pos in positions.items():
            try:
                price_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=date_str.replace("-", ""),
                    end_date=date_str.replace("-", ""),
                    adjust="qfq",
                )
                if len(price_df) > 0:
                    current_price = price_df.iloc[0]["收盘"]
                    total_value += pos["shares"] * current_price
            except:
                pass

        if total_value < max_capital:
            portfolio_drawdown = (total_value - max_capital) / max_capital
            if portfolio_drawdown < STRATEGY_PARAMS["stop_loss_portfolio"]:
                print(f"  组合止损触发: {portfolio_drawdown:.2%}")
                for stock_code in list(positions.keys()):
                    pos = positions[stock_code]
                    try:
                        price_df = ak.stock_zh_a_hist(
                            symbol=stock_code,
                            period="daily",
                            start_date=date_str.replace("-", ""),
                            end_date=date_str.replace("-", ""),
                            adjust="qfq",
                        )
                        if len(price_df) > 0:
                            current_price = price_df.iloc[0]["收盘"]
                            sell_value = pos["shares"] * current_price
                            sell_cost = sell_value * (
                                BACKTEST_CONFIG["commission"]
                                + BACKTEST_CONFIG["stamp_tax"]
                            )
                            capital += sell_value - sell_cost

                            stop_loss_records.append(
                                {
                                    "date": date_str,
                                    "stock": stock_code,
                                    "pnl": (current_price - pos["cost"]) / pos["cost"],
                                    "type": "portfolio_stop_loss",
                                }
                            )
                    except:
                        pass
                positions.clear()

        if total_value > max_capital:
            max_capital = total_value

        # 2. 选股
        try:
            selected = screen_stocks(date_str)
        except Exception as e:
            print(f"  选股失败: {e}")
            selected = []

        if len(selected) == 0:
            print(f"  无符合条件股票，跳过调仓")
            continue

        # 3. 调仓
        # 卖出不在目标列表的股票
        target_codes = [s["代码"] for s in selected]
        for stock_code in list(positions.keys()):
            if stock_code not in target_codes:
                pos = positions[stock_code]
                try:
                    price_df = ak.stock_zh_a_hist(
                        symbol=stock_code,
                        period="daily",
                        start_date=date_str.replace("-", ""),
                        end_date=date_str.replace("-", ""),
                        adjust="qfq",
                    )
                    if len(price_df) > 0:
                        current_price = price_df.iloc[0]["收盘"]
                        sell_value = pos["shares"] * current_price
                        sell_cost = sell_value * (
                            BACKTEST_CONFIG["commission"] + BACKTEST_CONFIG["stamp_tax"]
                        )
                        capital += sell_value - sell_cost

                        pnl = (current_price - pos["cost"]) / pos["cost"]
                        trade_records.append(
                            {
                                "date": date_str,
                                "stock": stock_code,
                                "type": "sell",
                                "price": current_price,
                                "pnl": pnl,
                            }
                        )
                        print(f"  卖出: {stock_code}, 盈亏: {pnl:.2%}")
                except Exception as e:
                    print(f"  卖出{stock_code}失败: {e}")
                del positions[stock_code]

        # 买入目标股票
        per_stock_value = capital / len(selected)
        for stock_info in selected:
            stock_code = stock_info["代码"]
            try:
                price_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=date_str.replace("-", ""),
                    end_date=date_str.replace("-", ""),
                    adjust="qfq",
                )
                if len(price_df) > 0:
                    current_price = price_df.iloc[0]["收盘"]
                    buy_value = per_stock_value
                    buy_cost = buy_value * (
                        BACKTEST_CONFIG["commission"] + BACKTEST_CONFIG["slippage"]
                    )
                    actual_value = buy_value - buy_cost
                    shares = actual_value / current_price

                    if stock_code in positions:
                        # 加仓
                        old_shares = positions[stock_code]["shares"]
                        old_cost = positions[stock_code]["cost"]
                        total_shares = old_shares + shares
                        avg_cost = (
                            old_shares * old_cost + shares * current_price
                        ) / total_shares
                        positions[stock_code] = {
                            "shares": total_shares,
                            "cost": avg_cost,
                            "date": date_str,
                        }
                    else:
                        positions[stock_code] = {
                            "shares": shares,
                            "cost": current_price,
                            "date": date_str,
                        }

                    capital -= buy_value + buy_cost
                    trade_records.append(
                        {
                            "date": date_str,
                            "stock": stock_code,
                            "type": "buy",
                            "price": current_price,
                            "value": buy_value,
                        }
                    )
            except Exception as e:
                print(f"  买入{stock_code}失败: {e}")

        # 4. 记录每日数据
        total_value = capital
        for stock_code, pos in positions.items():
            try:
                price_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=date_str.replace("-", ""),
                    end_date=date_str.replace("-", ""),
                    adjust="qfq",
                )
                if len(price_df) > 0:
                    total_value += pos["shares"] * price_df.iloc[0]["收盘"]
            except:
                pass

        daily_records.append(
            {
                "date": date_str,
                "capital": capital,
                "position_value": total_value - capital,
                "total_value": total_value,
                "holdings_count": len(positions),
                "holdings": list(positions.keys()),
            }
        )

        print(f"  组合净值: {total_value / 1e6:.2f}百万, 持仓: {len(positions)}只")

        # 避免请求过快
        time.sleep(0.5)

    # ============================================================
    # 计算绩效
    # ============================================================
    print("\n" + "=" * 70)
    print("回测完成，计算绩效")
    print("=" * 70)

    df_daily = pd.DataFrame(daily_records)
    df_daily["date"] = pd.to_datetime(df_daily["date"])
    df_daily = df_daily.set_index("date")

    # 收益率
    df_daily["return"] = df_daily["total_value"].pct_change()

    # 年化收益率
    total_return = (
        df_daily["total_value"].iloc[-1] / df_daily["total_value"].iloc[0] - 1
    )
    days = len(df_daily)
    annual_return = (1 + total_return) ** (252 / days) - 1

    # 最大回撤
    cummax = df_daily["total_value"].cummax()
    drawdown = (df_daily["total_value"] - cummax) / cummax
    max_drawdown = drawdown.min()

    # 夏普比率
    daily_returns = df_daily["return"].dropna()
    annual_volatility = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = (
        (annual_return - 0.03) / annual_volatility if annual_volatility > 0 else 0
    )

    # 胜率
    win_rate = (daily_returns > 0).mean()

    # 交易统计
    df_trades = pd.DataFrame(trade_records)
    buy_trades = df_trades[df_trades["type"] == "buy"]
    sell_trades = df_trades[df_trades["type"] == "sell"]

    # 止损统计
    df_stop_loss = pd.DataFrame(stop_loss_records)

    # IS/OOS分割
    is_mask = df_daily.index < pd.Timestamp(oos_start)
    oos_mask = ~is_mask

    is_return = (
        df_daily[is_mask]["total_value"].iloc[-1]
        / df_daily[is_mask]["total_value"].iloc[0]
        - 1
        if is_mask.any()
        else 0
    )
    oos_return = (
        df_daily[oos_mask]["total_value"].iloc[-1]
        / df_daily[oos_mask]["total_value"].iloc[0]
        - 1
        if oos_mask.any()
        else 0
    )

    # 打印结果
    print(f"\n【整体绩效】")
    print(f"总收益率: {total_return:.2%}")
    print(f"年化收益率: {annual_return:.2%}")
    print(f"最大回撤: {max_drawdown:.2%}")
    print(f"夏普比率: {sharpe_ratio:.2f}")
    print(f"胜率: {win_rate:.2%}")
    print(f"交易次数: {len(df_trades)}")
    print(f"止损次数: {len(df_stop_loss)}")

    print(f"\n【IS期绩效】({start_date} ~ {oos_start})")
    print(f"总收益率: {is_return:.2%}")

    print(f"\n【OOS期绩效】({oos_start} ~ {end_date})")
    print(f"总收益率: {oos_return:.2%}")

    # 保存结果
    results = {
        "strategy": "smallcap_defense_v3",
        "params": STRATEGY_PARAMS,
        "backtest_config": BACKTEST_CONFIG,
        "performance": {
            "total_return": total_return,
            "annual_return": annual_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "win_rate": win_rate,
            "trade_count": len(df_trades),
            "stop_loss_count": len(df_stop_loss),
        },
        "is_performance": {
            "start": start_date,
            "end": oos_start,
            "total_return": is_return,
        },
        "oos_performance": {
            "start": oos_start,
            "end": end_date,
            "total_return": oos_return,
        },
        "daily_records": df_daily.reset_index().to_dict("records"),
        "trade_records": df_trades.to_dict("records") if len(df_trades) > 0 else [],
        "stop_loss_records": df_stop_loss.to_dict("records")
        if len(df_stop_loss) > 0
        else [],
    }

    # 保存JSON
    output_file = (
        CACHE_DIR / f"backtest_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n结果已保存: {output_file}")

    return results


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    results = run_backtest()
