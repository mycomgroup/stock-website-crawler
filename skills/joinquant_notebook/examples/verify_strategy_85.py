from jqdata import *
from jqlib.technical_analysis import *
import numpy as np
import datetime

print("=== 稳健型ETF策略 核心逻辑验证 ===")

# 测试日期（使用最近交易日）
test_date = "2026-03-28"

# 1. 获取各ETF的MACD月线信号
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
        macd_val = macd_macd[code][-1] if len(macd_macd[code]) > 0 else 0
        signal = "多头" if macd_val > 0 else "空头"
        macd_signals[code] = macd_val
        print(f"{name}({code}): MACD={macd_val:.4f} [{signal}]")
    except Exception as e:
        print(f"{name}({code}): 获取失败 - {e}")
        macd_signals[code] = 0

# 2. 获取红利ETF年度收益率
print(f"\n2. 年度收益率判断 ({test_date})")
print("-" * 50)

etf = "510880.XSHG"
year = 2026
start_date = datetime.datetime(year - 1, 12, 20).strftime("%Y-%m-%d")
end_date = datetime.datetime(year - 1, 12, 31).strftime("%Y-%m-%d")

try:
    df_all = attribute_history(etf, 25, "1d", ["close"])
    df_close = df_all["close"]
    current_price = df_close[-1]

    df_old = get_price(
        etf, start_date=start_date, end_date=end_date, frequency="1d", panel=False
    )
    old_price = df_old["close"][-1]

    yearly_return = round((current_price - old_price) * 100 / old_price, 2)
    print(
        f"红利ETF 去年收盘: {old_price:.4f}, 当前: {current_price:.4f}, 年度收益率: {yearly_return}%"
    )
except Exception as e:
    yearly_return = 0
    print(f"获取年度收益失败: {e}")

# 3. 模拟策略选择逻辑
print(f"\n3. 策略选择逻辑 ({test_date})")
print("-" * 50)

# #1 选择
if macd_signals.get("159949.XSHE", 0) > 0:
    stock_fund_1 = "159949.XSHE 创业板50"
else:
    if macd_signals.get("513100.XSHG", 0) > 0:
        stock_fund_1 = "513100.XSHG 纳斯达克"
    else:
        if yearly_return > -6:
            stock_fund_1 = "510880.XSHG 红利"
        else:
            stock_fund_1 = "511010.XSHG 国债ETF"

# #2 选择
if yearly_return > -6:
    stock_fund_2 = "510880.XSHG 红利"
else:
    stock_fund_2 = "511010.XSHG 国债ETF"

# #3 选择
if macd_signals.get("518880.XSHG", 0) > 0:
    stock_fund_3 = "518880.XSHG 黄金"
else:
    if macd_signals.get("510880.XSHG", 0) > 0 and yearly_return > -6:
        stock_fund_3 = "510880.XSHG 红利"
    else:
        stock_fund_3 = "518880.XSHG 黄金"

print(f"#1 选择: {stock_fund_1}")
print(f"#2 选择: {stock_fund_2}")
print(f"#3 选择: {stock_fund_3}")
print(f"#4 选择: 511010.XSHG 国债ETF")
print(f"#5 选择: 511880.XSHG 银华日利")

# 4. 权重分配
print(f"\n4. 仓位权重")
print("-" * 50)
print("ETF1 (创业板/纳斯达克/红利/国债): 12.5%")
print("ETF2 (红利/国债): 12.5%")
print("ETF3 (黄金/红利): 25%")
print("ETF4 (国债ETF): 25%")
print("ETF5 (银华日利): 25%")

# 5. 策略评估
print(f"\n5. 策略评估")
print("-" * 50)
print(
    f"当前国债ETF信号: {'多头' if macd_signals.get('511010.XSHG', 0) > 0 else '空头'}"
)
print(f"当前黄金信号: {'多头' if macd_signals.get('518880.XSHG', 0) > 0 else '空头'}")
print(f"红利年度收益: {yearly_return}% (阈值-6%)")

if macd_signals.get("511010.XSHG", 0) > 0:
    print("→ 国债ETF处于多头，继续持有或加仓")
else:
    print("→ 国债ETF空头信号，但策略会根据其他ETF表现分配仓位")

print("\n=== 验证完成 ===")
