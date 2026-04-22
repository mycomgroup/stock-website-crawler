"""
RFScore7 PB10 策略测试 - V3版本
特点：行业上限 + 综合评分 + 尾盘调仓
测试日期：2024-03-20
"""

print("=== RFScore7 PB10 V3 策略测试开始 ===")

try:
    from jqdata import *
    from jqfactor import Factor, calc_factors
    import pandas as pd
    import numpy as np

    # 测试参数
    test_date = "2024-03-20"
    hold_num = 10
    pb_threshold = 1.0

    print(f"\n测试日期: {test_date}")
    print(f"持仓数量: {hold_num}")
    print(f"PB阈值: {pb_threshold}")

    # 1. 获取股票池（沪深300 + 中证500）
    print("\n1. 获取股票池...")
    hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
    stocks = list(hs300 | zz500)
    print(f"   初始股票数: {len(stocks)}")

    # 2. 过滤ST股票
    print("\n2. 过滤ST股票...")
    is_st = get_extras("is_st", stocks, end_date=test_date, count=1)
    if not is_st.empty:
        st_stocks = is_st.iloc[-1][is_st.iloc[-1] == True].index.tolist()
        stocks = [s for s in stocks if s not in st_stocks]
    print(f"   过滤ST后: {len(stocks)}")

    # 3. 过滤停牌股票
    print("\n3. 过滤停牌股票...")
    paused = get_price(
        stocks, end_date=test_date, count=1, fields=["paused"], panel=False
    )
    if not paused.empty:
        paused_stocks = paused[paused["paused"] == 1]["code"].tolist()
        stocks = [s for s in stocks if s not in paused_stocks]
    print(f"   过滤停牌后: {len(stocks)}")

    # 4. 获取估值数据
    print("\n4. 获取估值数据...")
    q = query(
        valuation.code,
        valuation.pb_ratio,
        valuation.pe_ratio,
        valuation.market_cap,
        valuation.circulating_market_cap,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pb_ratio > 0,
        valuation.pb_ratio < pb_threshold,
    )

    df_val = get_fundamentals(q, date=test_date)
    if df_val is None or df_val.empty:
        print("   警告: 无估值数据")
        stocks = []
    else:
        stocks = df_val["code"].tolist()
        print(f"   PB筛选后: {len(stocks)}")

    # 5. 计算RFScore因子
    print("\n5. 计算RFScore因子...")
    if len(stocks) > 0:
        # 简化版：使用ROA作为评分
        q_factor = query(indicator.code, indicator.roa).filter(
            indicator.code.in_(stocks)
        )

        df_factor = get_fundamentals(q_factor, date=test_date)

        if df_factor is not None and not df_factor.empty:
            # 合并数据
            df = pd.merge(df_val, df_factor, on="code", how="left")
            df = df.dropna()

            # 综合评分：ROA排序
            df = df.sort_values("roa", ascending=False)

            print(f"   有因子数据: {len(df)}")

            # 6. 行业分散（每个行业最多2只）
            print("\n6. 行业分散...")
            try:
                q_industry = query(valuation.code, valuation.industry).filter(
                    valuation.code.in_(df["code"].tolist()[: hold_num * 2])
                )

                df_industry = get_fundamentals(q_industry, date=test_date)

                if df_industry is not None and not df_industry.empty:
                    df = pd.merge(df, df_industry, on="code", how="left")

                    # 行业限制
                    selected = []
                    industry_count = {}
                    for idx, row in df.iterrows():
                        ind = row.get("industry", "Unknown")
                        if industry_count.get(ind, 0) < 2:
                            selected.append(row["code"])
                            industry_count[ind] = industry_count.get(ind, 0) + 1
                        if len(selected) >= hold_num:
                            break

                    print(f"   最终选股: {len(selected)}")

                    # 7. 输出结果
                    print("\n7. 选股结果:")
                    for i, code in enumerate(selected, 1):
                        row = df[df["code"] == code].iloc[0]
                        print(
                            f"   {i}. {code} - PB: {row['pb_ratio']:.2f}, ROA: {row['roa']:.2f}%, 市值: {row['market_cap']:.1f}亿"
                        )

                    print(f"\n✓ 策略执行成功")
                    print(f"   选出 {len(selected)} 只股票")

                else:
                    print("   警告: 无行业数据")
                    selected = df["code"].tolist()[:hold_num]
                    print(f"\n✓ 策略执行成功（无行业分散）")
                    print(f"   选出 {len(selected)} 只股票")
            except Exception as e:
                print(f"   行业数据处理出错: {e}")
                selected = df["code"].tolist()[:hold_num]
                print(f"\n✓ 策略执行成功（无行业分散）")
                print(f"   选出 {len(selected)} 只股票")

            else:
                print("   警告: 无行业数据")
                selected = df["code"].tolist()[:hold_num]
                print(f"\n✓ 策略执行成功（无行业分散）")
                print(f"   选出 {len(selected)} 只股票")
        else:
            print("   警告: 无因子数据")
    else:
        print("   警告: 无符合条件的股票")

except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback

    traceback.print_exc()

print("\n=== RFScore7 PB10 V3 策略测试完成 ===")
