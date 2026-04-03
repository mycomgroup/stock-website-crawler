from jqdata import *
from jqlib.technical_analysis import *
import numpy as np
import datetime

print("=== 稳健型ETF策略 核心逻辑验证 V2 ===")

test_date = "2026-03-28"

etfs = {
    "159949.XSHE": "创业板50",
    "513100.XSHG": "纳斯达克100",
    "510880.XSHG": "红利ETF",
    "511010.XSHG": "国债ETF",
    "518880.XSHG": "黄金ETF",
}

print(f"\n1. MACD月线信号 ({test_date})")
print("-" * 50)

macd_signals = {}
for code, name in etfs.items():
    try:
        macd_dif, macd_dea, macd_macd = MACD(
            code,
            check_date=test_date,
            SHORT=12,
            LONG=26,
            MID=9,
            unit="1M",
            include_now=False,
        )
        # 处理numpy类型
        macd_val = (
            float(macd_macd[code][-1])
            if hasattr(macd_macd[code][-1], "__float__")
            else 0
        )
        signal = "多头" if macd_val > 0 else "空头"
        macd_signals[code] = macd_val
        print(f"{name}({code}): MACD={macd_val:.4f} [{signal}]")
    except Exception as e:
        print(f"{name}({code}): 获取失败 - {e}")
        macd_signals[code] = 0

# 年度收益率
print(f"\n2. 年度收益率判断")
print("-" * 50)
etf = "510880.XSHG"
year = 2026
start_date = datetime.datetime(year - 1, 12, 20).strftime("%Y-%m-%d")
end_date = datetime.datetime(year - 1, 12, 31).strftime("%Y-%m-%d")

try:
    df_all = attribute_history(etf, 25, "1d", ["close"])
    current_price = float(df_all["close"].iloc[-1])
    df_old = get_price(
        etf, start_date=start_date, end_date=end_date, frequency="1d", panel=False
    )
    old_price = float(df_old["close"].iloc[-1])
    yearly_return = round((current_price - old_price) * 100 / old_price, 2)
    print(
        f"红利ETF: 去年={old_price:.4f}, 当前={current_price:.4f}, 年度收益={yearly_return}%"
    )
except Exception as e:
    yearly_return = 0
    print(f"获取失败: {e}")

# 策略选择
print(f"\n3. 策略选择逻辑")
print("-" * 50)

# #1
if macd_signals.get("159949.XSHE", 0) > 0:
    stock_fund_1 = "159949.XSHE 创业板50"
elif macd_signals.get("513100.XSHG", 0) > 0:
    stock_fund_1 = "513100.XSHG 纳斯达克"
elif yearly_return > -6:
    stock_fund_1 = "510880.XSHG 红利"
else:
    stock_fund_1 = "511010.XSHG 国债ETF"

# #2
stock_fund_2 = "510880.XSHG 红利" if yearly_return > -6 else "511010.XSHG 国债ETF"

# #3
if macd_signals.get("518880.XSHG", 0) > 0:
    stock_fund_3 = "518880.XSHG 黄金"
elif macd_signals.get("510880.XSHG", 0) > 0 and yearly_return > -6:
    stock_fund_3 = "510880.XSHG 红利"
else:
    stock_fund_3 = "518880.XSHG 黄金"

print(f"#1: {stock_fund_1}")
print(f"#2: {stock_fund_2}")
print(f"#3: {stock_fund_3}")
print(f"#4: 511010.XSHG 国债ETF")
print(f"#5: 511880.XSHG 银华日利")

# 仓位
print(f"\n4. 仓位分配")
print("-" * 50)
print("ETF1: 12.5%  |  ETF2: 12.5%  |  ETF3: 25%  |  ETF4: 25%  |  ETF5: 25%")

# 策略评估
print(f"\n5. 当前市场判断")
print("-" * 50)
bullish_etfs = sum(1 for v in macd_signals.values() if v > 0)
print(f"MACD多头信号数: {bullish_etfs}/5")
print(f"红利年度收益: {yearly_return}% (牛市阈值>0, 正常>-6%)")

if yearly_return > 0:
    market_state = "强势市场"
elif yearly_return > -6:
    market_state = "中性/震荡市场"
else:
    market_state = "弱势市场"
print(f"市场状态: {market_state}")

# 结论
print(f"\n=== 结论 ===")
print(f"当前配置: 红利ETF(25%) + 黄金(25%) + 国债ETF(25%) + 银华日利(25%)")
print(f"策略特点: {'偏防御' if bullish_etfs < 3 else '偏进攻'}")
print(f"适合当前市场: {market_state}")

print("\n=== 验证完成 ===")
