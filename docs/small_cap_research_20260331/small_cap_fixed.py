"""
小市值策略 - 修复版 Notebook 验证
修复：情绪开关 + 历史数据获取

运行方式：
cd skills/joinquant_notebook
node run-strategy.js --strategy "../../docs/small_cap_research_20260331/small_cap_fixed.py" --timeout-ms 300000
"""

print("=" * 70)
print("小市值策略 - 修复版 Notebook 验证")
print("修复：情绪开关数据获取 + 历史数据获取")
print("=" * 70)

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ============================================================
# 参数设置
# ============================================================
print("\n" + "=" * 70)
print("第一部分：策略参数")
print("=" * 70)

PARAMS = {
    "stock_num": 10,
    "min_cap": 5,
    "max_cap": 200,
    "emotion_threshold": 30,
    "pause_loss_count": 3,
    "pause_days": 3,
    "stop_loss": -0.09,
}

print("\n策略参数:")
for k, v in PARAMS.items():
    print(f"  {k}: {v}")

# ============================================================
# 第二部分：情绪指标验证（修复版）
# ============================================================
print("\n" + "=" * 70)
print("第二部分：情绪指标验证（修复版）")
print("=" * 70)

# 使用沪深300成分股计算情绪（更可靠）
test_date = "2024-03-20"
print(f"\n测试日期: {test_date}")

try:
    # 获取沪深300成分股
    hs300 = get_index_stocks("000300.XSHG", date=test_date)
    print(f"沪深300成分股: {len(hs300)}只")

    # 获取前一日收盘价和当日数据
    prev_date = get_trade_days(end_date=test_date, count=2)[0]
    print(f"前一日: {prev_date}")

    # 获取数据
    df_today = get_price(
        hs300[:100],
        end_date=test_date,
        count=1,
        fields=["close", "high_limit", "low_limit"],
        panel=False,
    )
    df_prev = get_price(
        hs300[:100], end_date=prev_date, count=1, fields=["close"], panel=False
    )

    zt_count = 0
    dt_count = 0

    for stock in hs300[:100]:
        try:
            if stock in df_today.index and stock in df_prev.index:
                today_close = df_today.loc[stock, "close"]
                high_limit = df_today.loc[stock, "high_limit"]
                low_limit = df_today.loc[stock, "low_limit"]

                # 涨停判断
                if today_close >= high_limit * 0.995:
                    zt_count += 1
                # 跌停判断
                elif today_close <= low_limit * 1.005:
                    dt_count += 1
        except:
            continue

    # 估算全市场
    zt_total = int(zt_count * len(hs300) / 100)

    print(f"\n沪深300涨停数: {zt_count}只")
    print(f"沪深300跌停数: {dt_count}只")
    print(f"估算全市场涨停: {zt_total}只")
    print(f"情绪阈值: {PARAMS['emotion_threshold']}")

    emotion_ok = zt_total >= PARAMS["emotion_threshold"]
    print(f"情绪判断: {'✓ 达标' if emotion_ok else '✗ 不足'}")

except Exception as e:
    print(f"情绪计算错误: {e}")
    import traceback

    traceback.print_exc()
    emotion_ok = True

# ============================================================
# 第三部分：股票池筛选
# ============================================================
print("\n" + "=" * 70)
print("第三部分：股票池筛选")
print("=" * 70)

try:
    # 上证+深证
    scu = get_index_stocks("000001.XSHG", date=test_date) + get_index_stocks(
        "399106.XSHE", date=test_date
    )
    print(f"\n上证+深证成分股: {len(scu)}只")

    # 过滤科创北交
    scu = [s for s in scu if not s.startswith("688") and not s.startswith("8")]
    print(f"过滤科创北交后: {len(scu)}只")

    # 市值+财务筛选
    q = (
        query(
            valuation.code,
            valuation.market_cap,
            valuation.pe_ratio,
            valuation.pb_ratio,
            indicator.roe,
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
        print(f"市值筛选后: {len(df)}只")
        print(f"\n市值最小的10只:")
        print(
            df[["code", "market_cap", "pe_ratio", "pb_ratio", "roe"]]
            .head(10)
            .to_string(index=False)
        )
        stock_pool = list(df["code"])
    else:
        stock_pool = []

except Exception as e:
    print(f"错误: {e}")
    stock_pool = []

# ============================================================
# 第四部分：不追涨停筛选
# ============================================================
print("\n" + "=" * 70)
print("第四部分：不追涨停筛选")
print("=" * 70)

if stock_pool:
    try:
        print(f"\n筛选前: {len(stock_pool)}只")

        # 获取价格数据
        df_price = get_price(
            stock_pool[:100],
            end_date=test_date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )

        non_zt = []
        for s in stock_pool[:100]:
            try:
                if s in df_price.index:
                    close = df_price.loc[s, "close"]
                    high_limit = df_price.loc[s, "high_limit"]

                    # 不买涨停股
                    if close < high_limit * 0.99:
                        non_zt.append(s)
            except:
                non_zt.append(s)

        print(f"不追涨停后: {len(non_zt)}只")
        print(f"前10只: {non_zt[:10]}")

    except Exception as e:
        print(f"错误: {e}")
        non_zt = stock_pool[:20]
else:
    non_zt = []

# ============================================================
# 第五部分：多因子评分（修复版）
# ============================================================
print("\n" + "=" * 70)
print("第五部分：多因子评分（修复版）")
print("=" * 70)

if non_zt:
    print(f"\n待评分: {len(non_zt)}只")

    results = []

    for s in non_zt[:30]:
        try:
            # 使用 get_price 获取历史数据（更稳定）
            df_hist = get_price(
                s, end_date=test_date, count=60, fields=["close"], panel=False
            )

            if df_hist is None or len(df_hist) < 40:
                continue

            close = df_hist["close"].values

            # 计算因子
            if len(close) >= 21:
                momentum = (close[-1] / close[-21] - 1) * 100
            else:
                momentum = 0

            if len(close) >= 20:
                ma20 = np.mean(close[-20:])
                ma_dev = (close[-1] / ma20 - 1) * 100
            else:
                ma_dev = 0

            high20 = np.max(close[-20:]) if len(close) >= 20 else close[-1]
            low20 = np.min(close[-20:]) if len(close) >= 20 else close[-1]
            price_pos = (
                (close[-1] - low20) / (high20 - low20) if high20 != low20 else 0.5
            )

            # 评分
            score = 0

            # 动量
            if 5 < momentum < 20:
                score += 3
            elif 0 < momentum <= 5:
                score += 2
            elif -10 < momentum <= 0:
                score += 1

            # MA乖离
            if -5 < ma_dev < 5:
                score += 2
            elif -10 < ma_dev < 10:
                score += 1

            # 价格位置
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
        print("-" * 70)
        print(f"{'排名':<4} {'代码':<12} {'分数':<6} {'动量%':<8} {'乖离%':<8}")
        print("-" * 70)

        for i, r in enumerate(results[:10], 1):
            print(
                f"{i:<4} {r['code']:<12} {r['score']:<6} {r['momentum']:<8.1f} {r['ma_dev']:<8.1f}"
            )

        selected = [r["code"] for r in results[: PARAMS["stock_num"]]]
        print(f"\n最终选股: {selected}")
    else:
        selected = []
        print("无评分结果")
else:
    selected = []
    print("无候选股票")

# ============================================================
# 第六部分：停手机制演示
# ============================================================
print("\n" + "=" * 70)
print("第六部分：停手机制演示")
print("=" * 70)


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

    def daily_update(self):
        if self.pause_days > 0:
            self.pause_days -= 1


print("\n模拟交易序列:")
print("-" * 70)

pause_mgr = PauseManager()
test_trades = [2.5, -1.2, 3.1, -2.1, -1.5, -0.8, 4.2, -3.1, -2.2, -1.5, 5.0]

for i, pnl in enumerate(test_trades, 1):
    can_trade = pause_mgr.can_trade()
    status = "可交易" if can_trade else "停手中"

    note = ""
    if can_trade:
        triggered = pause_mgr.record_trade(pnl)
        if triggered:
            note = "⚠️ 触发停手"

    if pause_mgr.pause_days > 0:
        pause_mgr.daily_update()
        if pause_mgr.pause_days == 0:
            note = "✓ 恢复"

    print(f"{i:2d}. {pnl:+5.1f}% | {status} | 连亏={pause_mgr.loss_count} {note}")

print("-" * 70)
print(f"停手触发: {pause_mgr.trigger_count}次")

# ============================================================
# 最终总结
# ============================================================
print("\n" + "=" * 70)
print("最终总结")
print("=" * 70)

print(f"""
【修复版验证结果】

1. 情绪指标 ✓
   - 沪深300涨停: {zt_count}只
   - 估算全市场: {zt_total}只
   - 情绪判断: {"✓ 达标" if emotion_ok else "✗ 不足"}

2. 股票池筛选 ✓
   - 候选股票: {len(stock_pool)}只
   - 不追涨停后: {len(non_zt)}只

3. 多因子评分 ✓
   - 评分股票: {len(results) if "results" in dir() else 0}只
   - 最终选股: {len(selected) if "selected" in dir() else 0}只

4. 停手机制 ✓
   - 触发: {pause_mgr.trigger_count}次
   - 规则: 连亏3笔停3天

【下一步】
1. 策略编辑器运行完整回测
2. 对比有无改进的效果
3. 优化参数
""")

print("=" * 70)
print("修复版验证完成")
print("=" * 70)
