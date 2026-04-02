# 实验 1D: 纯A股池（删除所有跨市场资产）
# 研究: ETF Pool Optimization - Experiment 1D

print("=" * 80)
print("【实验 1D】纯A股池版本 - 8只ETF")
print("=" * 80)
print()

try:
    from jqdata import *
    import pandas as pd
    import numpy as np
    import warnings

    warnings.filterwarnings("ignore")

    # 纯A股池
    ETF_POOL = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "科创50ETF": "588000.XSHG",
        "中证1000ETF": "512100.XSHG",
        # "纳指ETF": "513100.XSHG",  # 删除
        # "标普500ETF": "513500.XSHG",  # 删除
        # "黄金ETF": "518880.XSHG",  # 删除
        # "国债ETF": "511010.XSHG",  # 删除
        "医疗ETF": "512170.XSHG",
        "消费ETF": "159928.XSHE",
        "新能源ETF": "516160.XSHG",
    }

    print(f"池子规模: {len(ETF_POOL)} 只ETF (纯A股)")
    print("成分:", list(ETF_POOL.keys()))
    print()

    # 回测参数
    START = "2020-01-01"
    END = "2024-12-31"
    COST = 0.001
    MOM_WINDOW = 20
    HOLD_DAYS = 10
    TOP_N = 3

    print(f"回测区间: {START} ~ {END}")
    print(f"策略: 动量{MOM_WINDOW}日 / 持有{HOLD_DAYS}日 / Top{TOP_N}")
    print()

    # 回测函数
    def get_rebal_dates(start, end, freq_days):
        all_days = get_trade_days(start, end)
        result = [all_days[0]]
        for d in all_days[1:]:
            if (d - result[-1]).days >= freq_days:
                result.append(d)
        return result

    dates = get_rebal_dates(START, END, HOLD_DAYS)
    codes = list(ETF_POOL.values())
    rets = []
    prev_holdings = []

    print(f"开始回测，共 {len(dates) - 1} 个调仓周期...")

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
            pivot = prices.pivot(index="time", columns="code", values="close").dropna(
                axis=1
            )

            if len(pivot) < MOM_WINDOW:
                continue

            mom = pivot.iloc[-1] / pivot.iloc[0] - 1
            selected = mom.nlargest(TOP_N).index.tolist()

            # 计算收益
            p0 = get_price(
                selected, end_date=d_str, count=1, fields=["close"], panel=False
            )
            p1 = get_price(
                selected, end_date=next_d_str, count=1, fields=["close"], panel=False
            )

            if len(p0) == 0 or len(p1) == 0:
                continue

            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]

            gross_ret = ((p1 / p0) - 1).mean()
            turnover = len(set(selected) - set(prev_holdings)) / TOP_N
            net_ret = gross_ret - turnover * COST * 2

            rets.append(net_ret)
            prev_holdings = selected
        except Exception as e:
            continue

    # 计算指标
    s = pd.Series(rets)
    cum = (1 + s).cumprod()
    periods_per_year = 252 / HOLD_DAYS
    ann = cum.iloc[-1] ** (periods_per_year / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * np.sqrt(periods_per_year) if s.std() > 0 else 0
    win = (s > 0).mean()

    print()
    print("=" * 80)
    print("【实验结果】")
    print("=" * 80)
    print(f"年化收益: {ann:.2%}")
    print(f"最大回撤: {dd:.2%}")
    print(f"夏普比率: {sharpe:.2f}")
    print(f"胜率: {win:.1%}")
    print(f"样本数: {len(s)}")
    print()
    print("=" * 80)
    print("实验 1D 完成!")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
