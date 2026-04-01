# 纯 A 股 ETF 池对比 - 简化版（快速运行）

print("=" * 80)
print("【纯 A 股 ETF 池对比 - 简化版】")
print("=" * 80)
print()

try:
    from jqdata import *
    import pandas as pd
    import numpy as np

    # 池子定义
    OLD_POOL = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "科创50ETF": "588000.XSHG",
        "中证1000ETF": "512100.XSHG",
        "纳指ETF": "513100.XSHG",
        "标普500ETF": "513500.XSHG",
        "黄金ETF": "518880.XSHG",
        "国债ETF": "511010.XSHG",
        "医疗ETF": "512170.XSHG",
        "消费ETF": "159928.XSHE",
        "新能源ETF": "516160.XSHG",
    }

    NEW_POOL = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "科创50ETF": "588000.XSHG",
        "中证1000ETF": "512100.XSHG",
        "医疗ETF": "512170.XSHG",
        "消费ETF": "159928.XSHE",
        "新能源ETF": "516160.XSHG",
        "半导体ETF": "512480.XSHG",
        "军工ETF": "512660.XSHG",
        "银行ETF": "512800.XSHG",
        "计算机ETF": "512720.XSHG",
    }

    print("池子对比:")
    print("旧池:", list(OLD_POOL.keys()))
    print("新池:", list(NEW_POOL.keys()))
    print()

    # 参数
    START = "2020-01-01"
    END = "2024-12-31"
    COST = 0.001
    MOM_WINDOW = 20
    HOLD_DAYS = 10
    TOP_N = 3

    print(f"回测区间: {START} ~ {END}")
    print(f"策略: 动量{MOM_WINDOW}日 / 持有{HOLD_DAYS}日 / Top{TOP_N}")
    print()

    # 获取调仓日
    def get_rebal_dates(start, end, freq_days):
        all_days = get_trade_days(start, end)
        result = [all_days[0]]
        for d in all_days[1:]:
            if (d - result[-1]).days >= freq_days:
                result.append(d)
        return result

    dates = get_rebal_dates(START, END, HOLD_DAYS)
    print(f"总调仓次数: {len(dates) - 1}")
    print()

    # 运行回测
    def run_backtest(pool, pool_name):
        print(f"\n运行 {pool_name}...")
        codes = list(pool.values())
        rets = []
        prev_holdings = []

        for i, d in enumerate(dates[:-1]):
            if i % 20 == 0:
                print(f"  进度: {i}/{len(dates) - 1}")

            d_str = str(d)
            next_d_str = str(dates[i + 1])

            try:
                # 计算动量
                prices = get_price(
                    codes,
                    end_date=d_str,
                    count=MOM_WINDOW + 1,
                    fields=["close"],
                    panel=False,
                )
                pivot = prices.pivot(
                    index="time", columns="code", values="close"
                ).dropna(axis=1)

                if len(pivot) < MOM_WINDOW:
                    continue

                mom = pivot.iloc[-1] / pivot.iloc[0] - 1
                selected = mom.nlargest(TOP_N).index.tolist()

                # 计算收益
                p0 = get_price(
                    selected, end_date=d_str, count=1, fields=["close"], panel=False
                )
                p1 = get_price(
                    selected,
                    end_date=next_d_str,
                    count=1,
                    fields=["close"],
                    panel=False,
                )

                if len(p0) == 0 or len(p1) == 0:
                    continue

                p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
                p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]

                gross_ret = ((p1 / p0) - 1).mean()
                turnover = len(set(selected) - set(prev_holdings)) / TOP_N
                net_ret = gross_ret - turnover * COST * 2

                rets.append(
                    {
                        "date": d_str,
                        "ret": net_ret,
                        "gross": gross_ret,
                        "turnover": turnover,
                        "holdings": selected,
                    }
                )
                prev_holdings = selected

            except Exception as e:
                continue

        if not rets:
            return None

        df = pd.DataFrame(rets)
        df["cum"] = (1 + df["ret"]).cumprod()

        periods_per_year = 252 / HOLD_DAYS
        ann = df["cum"].iloc[-1] ** (periods_per_year / len(df)) - 1
        dd = (df["cum"] / df["cum"].cummax() - 1).min()
        sharpe = (
            df["ret"].mean() / df["ret"].std() * np.sqrt(periods_per_year)
            if df["ret"].std() > 0
            else 0
        )
        win = (df["ret"] > 0).mean()

        return {
            "name": pool_name,
            "df": df,
            "ann": ann,
            "dd": dd,
            "sharpe": sharpe,
            "win": win,
        }

    old_res = run_backtest(OLD_POOL, "旧池")
    new_res = run_backtest(NEW_POOL, "新池")

    print("\n" + "=" * 80)
    print("【回测结果对比】")
    print("=" * 80)

    if old_res and new_res:
        print(f"\n{'指标':<20s} {'旧池':<15s} {'新池':<15s} {'差异':<15s}")
        print("-" * 65)
        print(
            f"{'年化收益':<20s} {old_res['ann']:<15.2%} {new_res['ann']:<15.2%} {new_res['ann'] - old_res['ann']:<+15.2%}"
        )
        print(
            f"{'最大回撤':<20s} {old_res['dd']:<15.2%} {new_res['dd']:<15.2%} {new_res['dd'] - old_res['dd']:<+15.2%}"
        )
        print(
            f"{'夏普比率':<20s} {old_res['sharpe']:<15.2f} {new_res['sharpe']:<15.2f} {new_res['sharpe'] - old_res['sharpe']:<+15.2f}"
        )
        print(
            f"{'胜率':<20s} {old_res['win']:<15.1%} {new_res['win']:<15.1%} {new_res['win'] - old_res['win']:<+15.1%}"
        )

        # 最近5期持仓
        print("\n【最近5期持仓对比】")
        print("\n旧池:")
        for _, row in old_res["df"].tail(5).iterrows():
            holdings = [k for k, v in OLD_POOL.items() if v in row["holdings"]]
            print(f"  {row['date']}: {holdings}")

        print("\n新池:")
        for _, row in new_res["df"].tail(5).iterrows():
            holdings = [k for k, v in NEW_POOL.items() if v in row["holdings"]]
            print(f"  {row['date']}: {holdings}")

    print("\n" + "=" * 80)
    print("分析完成！")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
