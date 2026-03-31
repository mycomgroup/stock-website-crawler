from jqdata import *

print("=" * 60)
print("主线停手机制测试 - JoinQuant真实回测")
print("=" * 60)

# 测试2024年1月的5个交易日
days = list(get_trade_days("2024-01-01", "2024-01-10"))[:5]
print(f"测试日期: {len(days)}个交易日")
print(f"日期列表: {[str(d) for d in days]}")

trades = []
max_dd = 0

for i in range(1, len(days)):
    date = str(days[i])
    prev = str(days[i - 1])

    print(f"\n处理: {date}")

    # 获取涨停股（限制数量）
    stocks = get_all_securities("stock", date).index.tolist()[:100]
    print(f"  股票数: {len(stocks)}")

    # 昨日数据
    df_prev = get_price(
        stocks, end_date=prev, fields=["close", "high_limit"], count=1, panel=False
    )

    if not df_prev.empty:
        df_prev = df_prev.dropna()
        hl = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()[:10]
        print(f"  涨停股: {len(hl)}只")

        if len(hl) > 0:
            # 今日数据
            df_today = get_price(
                hl, end_date=date, fields=["open", "close"], count=1, panel=False
            )

            if not df_today.empty:
                df_today = df_today.dropna()
                print(f"  今日数据: {len(df_today)}只")

                # 计算收益
                ret = ((df_today["close"] - df_today["open"]) / df_today["open"]).mean()
                print(f"  日收益: {float(ret) * 100:.2f}%")

                trades.append(
                    {"date": date, "return_pct": float(ret) * 100, "is_win": ret > 0}
                )

print(f"\n" + "=" * 60)
print(f"交易总数: {len(trades)}")

if len(trades) > 0:
    # 统计连亏
    loss_count = 0
    max_consecutive = 0

    for t in trades:
        if not t["is_win"]:
            loss_count += 1
            if loss_count > max_consecutive:
                max_consecutive = loss_count
        else:
            loss_count = 0

    print(f"最大连亏: {max_consecutive}笔")

    # 计算回撤
    equity = 100000
    peak = equity
    max_dd = 0

    for t in trades:
        equity = equity * (1 + t["return_pct"] / 100)
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak * 100
        if dd > max_dd:
            max_dd = dd

    print(f"最大回撤: {max_dd:.2f}%")
    print(f"总收益: {sum([t['return_pct'] for t in trades]):.2f}%")

    # 测试停手机制
    print("\n测试停手机制（连亏3停3天）:")

    paused_trades = []
    pause_counter = 0
    loss_count = 0

    for t in trades:
        if pause_counter > 0:
            pause_counter -= 1
            print(f"  {t['date']}: 停手中")
            continue

        paused_trades.append(t)

        if not t["is_win"]:
            loss_count += 1
        else:
            loss_count = 0

        if loss_count >= 3:
            pause_counter = 3
            loss_count = 0
            print(f"  触发停手!")

    print(f"停手后交易: {len(paused_trades)}笔")
    print(f"休息天数: {len(trades) - len(paused_trades)}")

    # 计算停手后的回撤
    equity2 = 100000
    peak2 = equity2
    max_dd2 = 0

    for t in paused_trades:
        equity2 = equity2 * (1 + t["return_pct"] / 100)
        if equity2 > peak2:
            peak2 = equity2
        dd2 = (peak2 - equity2) / peak2 * 100
        if dd2 > max_dd2:
            max_dd2 = dd2

    print(f"停手后回撤: {max_dd2:.2f}%")
    print(f"停手后收益: {sum([t['return_pct'] for t in paused_trades]):.2f}%")

    if max_dd > 0 and max_dd2 > 0:
        dd_improve = (max_dd - max_dd2) / max_dd * 100
        print(f"回撤改善: {dd_improve:.1f}%")

print("\n=" * 60)
print("回测完成")
print("=" * 60)
