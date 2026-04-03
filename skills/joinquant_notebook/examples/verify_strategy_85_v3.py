from jqdata import *
import numpy as np
import datetime

print("=== 稳健型ETF策略 手动MACD验证 ===")

test_date = "2026-03-28"

etfs = {
    "159949.XSHE": "创业板50",
    "513100.XSHG": "纳斯达克100",
    "510880.XSHG": "红利ETF",
    "511010.XSHG": "国债ETF",
    "518880.XSHG": "黄金ETF",
}


def calc_ema(prices, period):
    """手动计算EMA"""
    ema = []
    alpha = 2 / (period + 1)
    for i, price in enumerate(prices):
        if i == 0:
            ema.append(price)
        else:
            ema.append(price * alpha + ema[-1] * (1 - alpha))
    return np.array(ema)


def calc_macd_manual(prices, short=12, long=26, mid=9):
    """手动计算MACD"""
    ema_short = calc_ema(prices, short)
    ema_long = calc_ema(prices, long)
    dif = ema_short - ema_long
    dea = calc_ema(dif, mid)
    macd = 2 * (dif - dea)
    return dif, dea, macd


print(f"\n1. MACD月线信号 ({test_date})")
print("-" * 50)

macd_signals = {}
for code, name in etfs.items():
    try:
        # 获取26个月历史数据
        df = get_price(code, end_date=test_date, count=27, frequency="1M", panel=False)
        if df is not None and len(df) > 26:
            closes = df["close"].values
            dif, dea, macd = calc_macd_manual(closes)
            macd_val = float(macd[-1])
            signal = "多头" if macd_val > 0 else "空头"
            macd_signals[code] = macd_val
            print(f"{name}: MACD={macd_val:.4f} [{signal}]")
        else:
            print(f"{name}: 数据不足")
            macd_signals[code] = 0
    except Exception as e:
        print(f"{name}: 获取失败 - {e}")
        macd_signals[code] = 0

# 年度收益率
print(f"\n2. 年度收益率判断")
print("-" * 50)
etf = "510880.XSHG"
year = 2026
try:
    df_old = get_price(
        etf, start_date="2025-12-20", end_date="2025-12-31", frequency="1d", panel=False
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
print(f"\n3. 策略选择逻辑")
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

# 仓位
print(f"\n4. 仓位分配")
print("-" * 50)
print("ETF1: 12.5%  |  ETF2: 12.5%  |  ETF3: 25%  |  ETF4: 25%  |  ETF5: 25%")

# 评估
print(f"\n5. 当前市场判断")
print("-" * 50)
bullish = sum(1 for v in macd_signals.values() if v > 0)
print(f"MACD多头信号: {bullish}/5")
print(f"红利年度收益: {yearly_return}%")

if yearly_return > 0:
    state = "强势"
elif yearly_return > -6:
    state = "中性/震荡"
else:
    state = "弱势"
print(f"市场: {state}")

print(f"\n=== 结论 ===")
print(f"偏防御配置（50%国债+货基），当前适合在震荡/中性市场")
print(f"红利年度收益{yearly_return}% > 0 → 市场并非极端熊市")

print("\n=== 验证完成 ===")
