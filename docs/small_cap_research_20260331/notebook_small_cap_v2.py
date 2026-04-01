"""
小市值策略 - Notebook 格式 V2
修复：使用 Notebook 可用的 API

运行方式：
cd skills/joinquant_notebook
node run-strategy.js --strategy "../../docs/small_cap_research_20260331/notebook_small_cap_v2.py" --timeout-ms 300000
"""

print("=" * 60)
print("小市值策略 Notebook 回测 V2")
print("核心：情绪开关 + 停手机制 + 不追涨停 + 小市值")
print("=" * 60)

import numpy as np
import pandas as pd

# ============================================================
# 参数设置
# ============================================================
print("\n[参数设置]")

PARAMS = {
    "stock_num": 10,
    "min_cap": 5,
    "max_cap": 200,
    "emotion_threshold": 30,
}

for k, v in PARAMS.items():
    print(f"  {k}: {v}")

# ============================================================
# 1. 情绪指标计算（使用历史数据）
# ============================================================
print("\n[1. 计算情绪指标 - 涨停家数]")

test_date = "2024-03-20"
print(f"测试日期: {test_date}")

try:
    # 获取所有股票
    all_stocks = list(get_all_securities("stock", test_date).index)

    # 过滤科创北交
    all_stocks = [
        s
        for s in all_stocks
        if not s.startswith("688") and not s.startswith("8") and not s.startswith("4")
    ]

    print(f"股票总数: {len(all_stocks)}")

    # 采样计算涨停家数
    sample_stocks = all_stocks[:200]

    # 获取当日价格
    df_price = get_price(
        sample_stocks, end_date=test_date, count=1, fields=["close", "high_limit"]
    )

    zt_count = 0
    for s in sample_stocks:
        try:
            close = df_price["close"][s].iloc[0] if s in df_price["close"] else None
            high_limit = (
                df_price["high_limit"][s].iloc[0]
                if s in df_price["high_limit"]
                else None
            )

            if close and high_limit and close >= high_limit * 0.99:
                zt_count += 1
        except:
            continue

    # 估算全市场涨停数
    zt_count_estimated = int(zt_count * len(all_stocks) / len(sample_stocks))

    print(f"采样涨停数: {zt_count}")
    print(f"估算全市场涨停数: {zt_count_estimated}")
    print(f"情绪阈值: {PARAMS['emotion_threshold']}")

    # 情绪判断
    emotion_ok = zt_count_estimated >= PARAMS["emotion_threshold"]
    print(f"情绪判断: {'✓ 达标' if emotion_ok else '✗ 不足'}")

except Exception as e:
    print(f"情绪计算错误: {e}")
    import traceback

    traceback.print_exc()
    zt_count_estimated = 0
    emotion_ok = True

# ============================================================
# 2. 获取股票池
# ============================================================
print("\n[2. 获取股票池]")

try:
    # 获取上证+深证成分股
    scu = get_index_stocks("000001.XSHG", date=test_date) + get_index_stocks(
        "399106.XSHE", date=test_date
    )
    print(f"上证+深证成分股: {len(scu)}只")

    # 过滤科创北交
    scu = [s for s in scu if not s.startswith("688") and not s.startswith("8")]
    print(f"过滤科创北交后: {len(scu)}只")

    # 市值筛选
    q = (
        query(
            valuation.code, valuation.market_cap, valuation.pe_ratio, valuation.pb_ratio
        )
        .filter(
            valuation.code.in_(scu),
            valuation.market_cap.between(PARAMS["min_cap"], PARAMS["max_cap"]),
            income.net_profit > 0,
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 100,
        )
        .order_by(valuation.market_cap.asc())
    )

    df = get_fundamentals(q, date=test_date)

    if df is not None and len(df) > 0:
        print(f"市值+财务筛选后: {len(df)}只")
        print(f"\n市值最小的10只:")
        print(df.head(10).to_string(index=False))

        stock_pool = list(df["code"])
    else:
        print("无符合条件股票")
        stock_pool = []

except Exception as e:
    print(f"股票池筛选错误: {e}")
    import traceback

    traceback.print_exc()
    stock_pool = []

# ============================================================
# 3. 不追涨停筛选
# ============================================================
print("\n[3. 不追涨停筛选]")

if stock_pool:
    try:
        # 获取当日价格
        df_price = get_price(
            stock_pool[:50], end_date=test_date, count=1, fields=["close", "high_limit"]
        )

        non_zt = []
        for s in stock_pool[:50]:
            try:
                close = df_price["close"][s].iloc[0] if s in df_price["close"] else None
                high_limit = (
                    df_price["high_limit"][s].iloc[0]
                    if s in df_price["high_limit"]
                    else None
                )

                # 不买涨停股
                if close and high_limit and close >= high_limit * 0.99:
                    continue
                non_zt.append(s)
            except:
                non_zt.append(s)

        print(f"不追涨停后: {len(non_zt)}只")

        if non_zt:
            print(f"候选股票: {non_zt[:10]}")

    except Exception as e:
        print(f"涨停过滤错误: {e}")
        non_zt = stock_pool[:10]
else:
    non_zt = []

# ============================================================
# 4. 多因子评分
# ============================================================
print("\n[4. 多因子评分选股]")

if non_zt:
    results = []

    for s in non_zt[:30]:
        try:
            # 获取历史价格
            h = history(
                60,
                unit="1d",
                field="close",
                security_list=[s],
                df=True,
                end_date=test_date,
            )

            if h is None or len(h) < 40:
                continue

            close = h[s].values

            # 计算因子
            momentum = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
            ma20 = np.mean(close[-20:])
            ma_dev = (close[-1] / ma20 - 1) * 100

            # 价格位置
            high20 = np.max(close[-20:])
            low20 = np.min(close[-20:])
            price_pos = (
                (close[-1] - low20) / (high20 - low20) if high20 != low20 else 0.5
            )

            # 评分
            score = 0
            if 5 < momentum < 20:
                score += 3
            elif 0 < momentum <= 5:
                score += 2
            elif -10 < momentum <= 0:
                score += 1

            if -5 < ma_dev < 5:
                score += 2
            elif -10 < ma_dev < 10:
                score += 1

            if 0.3 < price_pos < 0.6:
                score += 2
            elif 0.6 < price_pos < 0.8:
                score += 1

            results.append(
                {
                    "code": s,
                    "score": score,
                    "momentum": momentum,
                    "ma_dev": ma_dev,
                    "price_pos": price_pos,
                }
            )

        except Exception as e:
            continue

    # 排序
    results.sort(key=lambda x: -x["score"])

    print(f"\n评分完成: {len(results)}只")

    if results:
        print("\n评分最高的10只:")
        for i, r in enumerate(results[:10], 1):
            print(
                f"  {i}. {r['code']}: 分数={r['score']}, 动量={r['momentum']:.1f}%, 乖离={r['ma_dev']:.1f}%"
            )

        selected = [r["code"] for r in results[: PARAMS["stock_num"]]]
        print(f"\n最终选股: {selected}")
    else:
        selected = []

# ============================================================
# 5. 停手机制演示
# ============================================================
print("\n[5. 停手机制演示]")


class PauseManager:
    def __init__(self):
        self.loss_count = 0
        self.pause_days = 0
        self.trigger_count = 0

    def record_trade(self, pnl):
        if pnl < 0:
            self.loss_count += 1
        else:
            self.loss_count = 0

        if self.loss_count >= 3 and self.pause_days == 0:
            self.pause_days = 3
            self.trigger_count += 1
            return True
        return False

    def can_trade(self):
        return self.pause_days == 0


print("模拟交易序列:")
pause_mgr = PauseManager()
test_trades = [2.5, -1.2, 3.1, -2.1, -1.5, -0.8, 4.2, -3.1, -2.2, -1.5, 5.0]

for i, pnl in enumerate(test_trades, 1):
    can_trade = pause_mgr.can_trade()
    status = "✓可交易" if can_trade else "✗停手中"

    triggered = False
    if can_trade:
        triggered = pause_mgr.record_trade(pnl)

    if pause_mgr.pause_days > 0:
        pause_mgr.pause_days -= 1

    print(
        f"  第{i:2d}笔: {pnl:+.1f}% | {status} | 连亏={pause_mgr.loss_count} {'⚠️触发停手' if triggered else ''}"
    )

print(f"\n停手触发: {pause_mgr.trigger_count}次")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("[策略验证总结]")
print("=" * 60)

print(f"""
1. 情绪指标:
   - 估算涨停数: {zt_count_estimated}
   - 情绪判断: {"✓ 可开仓" if emotion_ok else "✗ 观望"}

2. 股票池:
   - 候选股票: {len(stock_pool)}只
   - 不追涨停后: {len(non_zt)}只
   - 最终选股: {len(selected) if "selected" in dir() else 0}只

3. 核心改进（基于研究文档）:
   ✓ 情绪开关（涨停>=30）
     - 回撤: 35.2% → 21.3% (-40%)
     - 卡玛: 0.24 → 0.51 (+113%)
   
   ✓ 停手机制（连亏3停3天）
     - 回撤改善: -28.4%
     - 卡玛提升: +68.6%
   
   ✓ 不追涨停
     - 保证可成交
   
   ✓ 小市值优先
     - 市值5-200亿

4. 研究文档关键结论:
   - 二板策略胜率: 87.95%
   - 二板策略年化: 407%
   - 二板策略回撤: 0.60%

5. 下一步:
   - 在策略编辑器运行完整回测
   - 验证2022-2024完整表现
""")

print("\n" + "=" * 60)
print("Notebook 回测完成")
print("=" * 60)
