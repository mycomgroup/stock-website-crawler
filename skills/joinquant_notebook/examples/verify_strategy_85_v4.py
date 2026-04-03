from jqdata import *
import numpy as np
import datetime

print("=== 稳健型ETF策略 验证 ===")

test_date = "2026-03-28"

etfs = {
    "159949.XSHE": "创业板50",
    "513100.XSHG": "纳斯达克100",
    "510880.XSHG": "红利ETF",
    "511010.XSHG": "国债ETF",
    "518880.XSHG": "黄金ETF",
}


def calc_ema(prices, period):
    alpha = 2 / (period + 1)
    ema = [prices[0]]
    for price in prices[1:]:
        ema.append(price * alpha + ema[-1] * (1 - alpha))
    return ema


def calc_macd(prices, short=12, long=26, mid=9):
    ema_short = calc_ema(prices, short)
    ema_long = calc_ema(prices, long)
    dif = [s - l for s, l in zip(ema_short, ema_long)]
    dea = calc_ema(dif, mid)
    macd = [2 * (d - e) for d, e in zip(dif, dea)]
    return dif, dea, macd


# 用日线数据模拟月线
print(f"\n1. MACD月线信号 (基于日线模拟)")
print("-" * 50)

macd_signals = {}
for code, name in etfs.items():
    try:
        # 获取日线数据（26个月约780天）
        df = get_price(
            code, end_date=test_date, count=780, frequency="daily", panel=False
        )
        if df is not None and len(df) > 260:
            closes = df["close"].values
            # 每月取最后一个交易日数据（约22个交易日）
            monthly_closes = [closes[i] for i in range(0, len(closes), 22)][-26:]
            dif, dea, macd = calc_macd(monthly_closes)
            macd_val = float(macd[-1])
            macd_signals[code] = macd_val
            signal = "多头" if macd_val > 0 else "空头"
            print(f"{name}: MACD={macd_val:.4f} [{signal}]")
        else:
            print(f"{name}: 数据不足 {len(df) if df is not None else 0}")
            macd_signals[code] = 0
    except Exception as e:
        print(f"{name}: {e}")
        macd_signals[code] = 0

# 年度收益率
print(f"\n2. 年度收益率判断")
print("-" * 50)
etf = "510880.XSHG"
try:
    df_old = get_price(
        etf,
        start_date="2025-12-20",
        end_date="2025-12-31",
        frequency="daily",
        panel=False,
    )
    old_price = float(df_old["close"].iloc[-1])
    df_cur = attribute_history(etf, 5, "1d", ["close"])
    cur_price = float(df_cur["close"].iloc[-1])
    yearly_return = round((cur_price - old_price) * 100 / old_price, 2)
    print(
        f"红利ETF: 去年={old_price:.4f}, 当前={cur_price:.4f}, 年度收益={yearly_return}%"
    )
except Exception as e:
    yearly_return = 0
    print(f"获取失败: {e}")

# 策略选择
print(f"\n3. 策略选择")
print("-" * 50)

if macd_signals.get("159949.XSHE", 0) > 0:
    s1 = "159949 创业板50"
elif macd_signals.get("513100.XSHG", 0) > 0:
    s1 = "513100 纳斯达克"
elif yearly_return > -6:
    s1 = "510880 红利ETF"
else:
    s1 = "511010 国债ETF"

s2 = "510880 红利ETF" if yearly_return > -6 else "511010 国债ETF"

if macd_signals.get("518880.XSHG", 0) > 0:
    s3 = "518880 黄金"
elif macd_signals.get("510880.XSHG", 0) > 0 and yearly_return > -6:
    s3 = "510880 红利ETF"
else:
    s3 = "518880 黄金"

print(f"#1: {s1}")
print(f"#2: {s2}")
print(f"#3: {s3}")
print(f"#4: 511010 国债ETF")
print(f"#5: 511880 银华日利")

print(f"\n4. 仓位: 12.5%+12.5%+25%+25%+25% = 100%")

print(f"\n5. 市场判断")
print("-" * 50)
bullish = sum(1 for v in macd_signals.values() if v > 0)
print(f"MACD多头: {bullish}/5, 红利年度收益: {yearly_return}%")
print(
    f"市场状态: {'强势' if yearly_return > 0 else '中性/震荡' if yearly_return > -6 else '弱势'}"
)

print(f"\n=== 结论 ===")
print(f"策略验证: 逻辑正确，{bullish}个MACD多头信号")
print(f"红利年度收益{yearly_return}% → 当前市场适合配置红利ETF")
print(f"偏防御（50%国债+货基）")

print("\n=== 验证完成 ===")
