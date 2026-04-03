# 实验 1A: 旧池完整版（基准对照组）- RiceQuant 兼容版

print("=" * 80)
print("【实验 1A】旧池完整版 - 12只ETF（基准对照组）- RiceQuant版")
print("=" * 80)
print()

print("正在导入依赖...")

# RiceQuant API
stocks = all_instruments("CS")
print(f"✅ 成功导入 RiceQuant API，获取到 {len(stocks)} 只股票")

# 由于 RiceQuant 的 ETF 数据可能不完整，我们将使用指数代替 ETF 进行概念验证
# 实际 ETF 数据需要从外部导入或使用 JoinQuant

ETF_POOL = {
    "沪深300": "000300.XSHG",  # 沪深300指数
    "中证500": "000905.XSHG",  # 中证500指数
    "创业板指": "399006.XSHE",  # 创业板指数
    "科创50": "000688.XSHG",  # 科创50指数
    "中证1000": "000852.XSHG",  # 中证1000指数
    "纳斯达克": "IXIC",  # 纳斯达克指数（美股）
    "标普500": "SPX",  # 标普500指数（美股）
    "黄金": "AU9999",  # 黄金现货
    "国债": "H11077",  # 中证国债指数
    "医疗": "H30177",  # 中证医疗指数
    "消费": "H30076",  # 中证消费指数
    "新能源": "H11080",  # 中证新能源指数
}

print(f"\n池子规模: {len(ETF_POOL)} 个标的")
print("成分:", list(ETF_POOL.keys()))
print()

# 由于 RiceQuant 的数据限制，我们先做数据质量检查
print("=" * 80)
print("【数据质量检查】")
print("=" * 80)

for name, code in ETF_POOL.items():
    try:
        # 获取最近5日数据测试
        data = history_bars(code, 5, "1d", "close")
        if data is not None and len(data) > 0:
            print(f"✅ {name} ({code}): 数据正常，最新价 {data[-1]:.2f}")
        else:
            print(f"⚠️  {name} ({code}): 无数据")
    except Exception as e:
        print(f"❌ {name} ({code}): 错误 - {e}")

print()
print("=" * 80)
print("注意: RiceQuant 平台 ETF 数据有限，建议使用 JoinQuant 进行完整回测")
print("此实验用于验证平台连接和数据可用性")
print("=" * 80)
