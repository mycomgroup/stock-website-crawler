"""
RFScore 防守组合策略测试 - Defensive V2版本
特点：动态防守层配置
测试日期：2024-03-20
"""

print("=== RFScore Defensive V2 策略测试开始 ===")

try:
    from jqdata import *
    import pandas as pd
    import numpy as np

    # 测试参数
    test_date = "2024-03-20"

    # 组合配置
    offensive_ratio = 0.40  # 进攻层40%
    defensive_ratio = 0.30  # 防守层30%
    cash_ratio = 0.30  # 现金30%

    print(f"\n测试日期: {test_date}")
    print(f"\n组合配置:")
    print(f"  进攻层（RFScore）: {offensive_ratio * 100}%")
    print(f"  防守层（固收组合）: {defensive_ratio * 100}%")
    print(f"  现金缓冲: {cash_ratio * 100}%")

    # ===== 第一部分：进攻层（RFScore选股）=====
    print("\n" + "=" * 60)
    print("第一部分：进攻层选股")
    print("=" * 60)

    # 1. 获取股票池
    print("\n1. 获取股票池...")
    hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
    stocks = list(hs300 | zz500)
    print(f"   初始股票数: {len(stocks)}")

    # 2. 基础过滤
    print("\n2. 基础过滤...")
    is_st = get_extras("is_st", stocks, end_date=test_date, count=1)
    if not is_st.empty:
        st_stocks = is_st.iloc[-1][is_st.iloc[-1] == True].index.tolist()
        stocks = [s for s in stocks if s not in st_stocks]

    paused = get_price(
        stocks, end_date=test_date, count=1, fields=["paused"], panel=False
    )
    if not paused.empty:
        paused_stocks = paused[paused["paused"] == 1]["code"].tolist()
        stocks = [s for s in stocks if s not in paused_stocks]

    print(f"   基础过滤后: {len(stocks)}")

    # 3. 估值筛选
    print("\n3. 估值筛选...")
    q = query(
        valuation.code, valuation.pb_ratio, valuation.pe_ratio, valuation.market_cap
    ).filter(
        valuation.code.in_(stocks),
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 1.0,
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 30,
    )

    df_val = get_fundamentals(q, date=test_date)
    if df_val is None or df_val.empty:
        print("   警告: 无估值数据")
        offensive_stocks = []
    else:
        stocks = df_val["code"].tolist()
        print(f"   PB+PE筛选后: {len(stocks)}")

        # 4. 财务筛选
        print("\n4. 财务筛选...")
        q_factor = query(indicator.code, indicator.roa, indicator.roe).filter(
            indicator.code.in_(stocks), indicator.roa > 5, indicator.roe > 10
        )

        df_factor = get_fundamentals(q_factor, date=test_date)

        if df_factor is not None and not df_factor.empty:
            df = pd.merge(df_val, df_factor, on="code", how="left")
            df = df.dropna()
            df = df.sort_values("roa", ascending=False)

            offensive_stocks = df["code"].tolist()[:5]  # 选5只
            print(f"   进攻层选股: {len(offensive_stocks)}")

            print("\n   进攻层股票:")
            for i, code in enumerate(offensive_stocks, 1):
                row = df[df["code"] == code].iloc[0]
                print(
                    f"   {i}. {code} - PB: {row['pb_ratio']:.2f}, ROA: {row['roa']:.2f}%, ROE: {row['roe']:.2f}%"
                )
        else:
            print("   警告: 无符合财务条件的股票")
            offensive_stocks = []

    # ===== 第二部分：防守层（固收组合）=====
    print("\n" + "=" * 60)
    print("第二部分：防守层配置")
    print("=" * 60)

    # 防守层配置（使用ETF替代）
    defensive_assets = {
        "国债ETF": {"code": "511010.XSHG", "weight": 0.75},
        "黄金ETF": {"code": "518880.XSHG", "weight": 0.10},
        "红利ETF": {"code": "510880.XSHG", "weight": 0.08},
        "纳指ETF": {"code": "513100.XSHG", "weight": 0.04},
        "现金": {"code": "CASH", "weight": 0.03},
    }

    print("\n防守层配置:")
    total_weight = 0
    for name, asset in defensive_assets.items():
        weight = asset["weight"] * defensive_ratio
        total_weight += weight
        print(
            f"  {name}: {asset['weight'] * 100:.0f}% × {defensive_ratio * 100:.0f}% = {weight * 100:.1f}%"
        )

    print(f"\n  防守层总权重: {total_weight * 100:.1f}%")

    # ===== 第三部分：市场状态判断 =====
    print("\n" + "=" * 60)
    print("第三部分：市场状态判断")
    print("=" * 60)

    # 简单的市场状态判断
    print("\n获取市场数据...")

    # 获取沪深300近期表现
    hs300_price = get_price(
        "000300.XSHG", end_date=test_date, count=20, fields=["close"], panel=False
    )
    if not hs300_price.empty:
        ma20 = hs300_price["close"].mean()
        current = hs300_price["close"].iloc[-1]
        trend = (current / ma20 - 1) * 100

        print(f"  沪深300 当前价: {current:.2f}")
        print(f"  沪深300 MA20: {ma20:.2f}")
        print(f"  偏离度: {trend:.2f}%")

        # 动态调整仓位
        if trend > 5:
            market_state = "强势"
            offensive_adj = 0.50
            defensive_adj = 0.20
            cash_adj = 0.30
        elif trend < -5:
            market_state = "弱势"
            offensive_adj = 0.30
            defensive_adj = 0.40
            cash_adj = 0.30
        else:
            market_state = "震荡"
            offensive_adj = offensive_ratio
            defensive_adj = defensive_ratio
            cash_adj = cash_ratio

        print(f"\n  市场状态: {market_state}")
        print(f"\n  调整后仓位:")
        print(f"    进攻层: {offensive_adj * 100:.0f}%")
        print(f"    防守层: {defensive_adj * 100:.0f}%")
        print(f"    现金: {cash_adj * 100:.0f}%")
    else:
        print("  警告: 无法获取市场数据")
        offensive_adj = offensive_ratio
        defensive_adj = defensive_ratio
        cash_adj = cash_ratio

    # ===== 第四部分：组合总结 =====
    print("\n" + "=" * 60)
    print("第四部分：组合总结")
    print("=" * 60)

    print("\n最终组合配置:")
    print(f"\n1. 进攻层（{offensive_adj * 100:.0f}%）:")
    if len(offensive_stocks) > 0:
        each_weight = offensive_adj / len(offensive_stocks)
        for i, code in enumerate(offensive_stocks, 1):
            print(f"   {i}. {code}: {each_weight * 100:.1f}%")
    else:
        print("   无符合条件的股票，转为现金")

    print(f"\n2. 防守层（{defensive_adj * 100:.0f}%）:")
    for name, asset in defensive_assets.items():
        weight = asset["weight"] * defensive_adj
        print(f"   {name} ({asset['code']}): {weight * 100:.1f}%")

    print(f"\n3. 现金（{cash_adj * 100:.0f}%）")

    print(f"\n✓ 策略执行成功")
    print(f"\n组合特点:")
    print(f"  - 动态调整仓位（基于市场状态）")
    print(f"  - 进攻层: RFScore选股，追求收益")
    print(f"  - 防守层: 多资产配置，降低风险")
    print(f"  - 现金缓冲: 应对波动")

except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== RFScore Defensive V2 策略测试完成 ===")
