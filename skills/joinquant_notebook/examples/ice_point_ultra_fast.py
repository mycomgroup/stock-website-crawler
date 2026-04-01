"""
情绪冰点捕捉测试 - 超快版
只测试最近10天数据，快速验证冰点捕捉效果
"""

from jqdata import *
import pandas as pd

print("=" * 80)
print("情绪冰点捕捉测试 - 超快版")
print("=" * 80)

START_DATE = "2025-12-01"
END_DATE = "2025-12-31"

print(f"测试范围: {START_DATE} 至 {END_DATE}")

trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日: {len(trade_days)}个")

if len(trade_days) < 2:
    print("交易日不足")
else:
    print("\n【1】快速统计涨停数")
    zt_list = []

    for date in trade_days[:15]:
        stocks = get_all_securities(types=["stock"], date=date)
        stock_list = [
            s
            for s in stocks.index.tolist()
            if not (
                s.startswith("688")
                or s.startswith("300")
                or s.startswith("4")
                or s.startswith("8")
            )
        ][:300]

        df = get_price(
            stock_list,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        df = df.dropna()

        zt_count = len(df[df["close"] == df["high_limit"]])
        zt_list.append({"date": date, "zt_count": zt_count})
        print(f"  {date}: 涨停数={zt_count}")

    df_zt = pd.DataFrame(zt_list)

    print(f"\n【2】冰点识别")
    ice_days = df_zt[df_zt["zt_count"] < 10]["date"].tolist()
    print(f"冰点日（涨停<10）: {len(ice_days)}个")

    if len(ice_days) > 0:
        print(f"冰点日列表: {[str(d) for d in ice_days[:5]]}")

    print(f"\n【3】冰点次日收益测试")

    if len(ice_days) > 0:
        ice_next_rets = []
        normal_rets = []

        for i, date in enumerate(trade_days[:15]):
            prev_dates = get_trade_days(end_date=date, count=2)
            if len(prev_dates) < 2:
                continue

            prev_date = prev_dates[0]
            is_ice_next = i > 0 and trade_days[i - 1] in ice_days

            stocks = get_all_securities(types=["stock"], date=date)
            stock_list = [
                s
                for s in stocks.index.tolist()
                if not (
                    s.startswith("688")
                    or s.startswith("300")
                    or s.startswith("4")
                    or s.startswith("8")
                )
            ][:100]

            df_prev = get_price(
                stock_list,
                end_date=prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            df_prev = df_prev.dropna()

            zt_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]][
                "code"
            ].tolist()

            if len(zt_stocks) > 0:
                df_today = get_price(
                    zt_stocks,
                    end_date=date,
                    frequency="daily",
                    fields=["open", "close", "pre_close"],
                    count=1,
                    panel=False,
                )
                df_today = df_today.dropna()

                low_open = df_today[(df_today["open"] < df_today["pre_close"])]

                if len(low_open) > 0:
                    for stock in low_open["code"].tolist()[:3]:
                        stock_df = df_today[df_today["code"] == stock]
                        ret = (
                            (stock_df["close"].iloc[0] - stock_df["open"].iloc[0])
                            / stock_df["open"].iloc[0]
                            * 100
                        )

                        if is_ice_next:
                            ice_next_rets.append(ret)
                        else:
                            normal_rets.append(ret)

        print(f"\n冰点次日交易:")
        if ice_next_rets:
            print(f"  交易次数: {len(ice_next_rets)}")
            print(f"  平均收益: {pd.Series(ice_next_rets).mean():.2f}%")
            print(
                f"  胜率: {len([r for r in ice_next_rets if r > 0]) / len(ice_next_rets) * 100:.1f}%"
            )

        print(f"\n正常日交易:")
        if normal_rets:
            print(f"  交易次数: {len(normal_rets)}")
            print(f"  平均收益: {pd.Series(normal_rets).mean():.2f}%")
            print(
                f"  胜率: {len([r for r in normal_rets if r > 0]) / len(normal_rets) * 100:.1f}%"
            )

    print(f"\n【4】反弹统计")
    if len(ice_days) > 0:
        rebound_count = 0
        for i in range(len(trade_days[:15])):
            if i > 0 and trade_days[i - 1] in ice_days:
                prev_zt = df_zt[df_zt["date"] == trade_days[i - 1]]["zt_count"].iloc[0]
                curr_zt = df_zt[df_zt["date"] == trade_days[i]]["zt_count"].iloc[0]

                if curr_zt > prev_zt:
                    rebound_count += 1
                    print(f"  {trade_days[i]}: {prev_zt}->{curr_zt} ✓反弹")
                else:
                    print(f"  {trade_days[i]}: {prev_zt}->{curr_zt} ✗继续下跌")

        print(f"冰点次日反弹成功率: {rebound_count}/{len(ice_days)}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
