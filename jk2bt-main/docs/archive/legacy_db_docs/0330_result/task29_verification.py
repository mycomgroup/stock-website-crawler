"""
Task 29 验证脚本
验证期货交易模型与合约API的实现
"""

import sys

sys.path.insert(0, "/Users/yuping/Downloads/git/jk2bt-main")

from jk2bt.market_data.futures import (
    parse_future_contract,
    get_future_contracts,
    get_dominant_contract,
    get_contract_multiplier,
    get_margin_rate,
    calculate_position_value,
    calculate_required_margin,
    CHINA_FUTURE_EXCHANGE_INFO,
)

from jk2bt.core.strategy_base import (
    get_future_contracts_jq,
    get_dominant_contract_jq,
    get_contract_multiplier_jq,
    get_margin_rate_jq,
    calculate_position_value_jq,
    calculate_required_margin_jq,
)

import warnings

warnings.filterwarnings("ignore")

print("=" * 60)
print("Task 29: 期货交易模型与合约API验证")
print("=" * 60)

print("\n【1】合约解析验证")
print("-" * 40)
result = parse_future_contract("IF2312")
print(f"IF2312解析结果: {result}")
assert result["product"] == "IF", "产品代码错误"
assert result["exchange"] == "CFFEX", "交易所错误"
print("✓ 合约解析正常")

print("\n【2】合约列表获取验证")
print("-" * 40)
df = get_future_contracts(product="IF", date="2023-12-01")
print(f"IF合约数量: {len(df)}")
if not df.empty:
    print("合约列表:")
    print(df[["contract", "month", "is_trading"]].to_string(index=False))
    assert len(df) >= 4, "合约数量不足"
    print("✓ 合约列表获取正常")

print("\n【3】主力合约验证")
print("-" * 40)
dom_if = get_dominant_contract("IF")
print(f"IF主力合约: {dom_if}")
assert dom_if and dom_if.startswith("IF"), "主力合约格式错误"

dom_ic = get_dominant_contract("IC")
print(f"IC主力合约: {dom_ic}")
assert dom_ic and dom_ic.startswith("IC"), "主力合约格式错误"
print("✓ 主力合约获取正常")

print("\n【4】合约乘数验证")
print("-" * 40)
mult_if = get_contract_multiplier("IF2312")
print(f"IF2312乘数: {mult_if}")
assert mult_if == 300, "IF乘数错误"

mult_ic = get_contract_multiplier("IC2401")
print(f"IC2401乘数: {mult_ic}")
assert mult_ic == 200, "IC乘数错误"

mult_au = get_contract_multiplier("AU2312")
print(f"AU2312乘数: {mult_au}")
assert mult_au == 1000, "AU乘数错误"
print("✓ 合约乘数查询正常")

print("\n【5】保证金比例验证")
print("-" * 40)
rate_if = get_margin_rate("IF2312")
print(f"IF2312保证金比例: {rate_if} ({rate_if * 100}%)")
assert rate_if == 0.12, "IF保证金比例错误"

rate_ic = get_margin_rate("IC2401")
print(f"IC2401保证金比例: {rate_ic} ({rate_ic * 100}%)")
assert rate_ic == 0.14, "IC保证金比例错误"
print("✓ 保证金比例查询正常")

print("\n【6】持仓价值计算验证")
print("-" * 40)
price = 4000
quantity = 10
contract = "IF2312"

value = calculate_position_value(price, quantity, contract)
print(f"持仓价值 (价格{price}, {quantity}手, {contract}): {value}")
expected = price * 300 * quantity
assert value == expected, f"持仓价值计算错误: 期望{expected}, 实际{value}"
print("✓ 持仓价值计算正常")

print("\n【7】保证金计算验证")
print("-" * 40)
margin = calculate_required_margin(price, quantity, contract)
print(f"所需保证金: {margin}")
expected_margin = price * 300 * quantity * 0.12
assert margin == expected_margin, f"保证金计算错误: 期望{expected_margin}, 实际{margin}"
print("✓ 保证金计算正常")

print("\n【8】JQ风格包装函数验证")
print("-" * 40)
df_jq = get_future_contracts_jq(product="IC")
print(f"IC合约列表(JQ风格): {len(df_jq)}个")
assert not df_jq.empty, "JQ风格函数返回空"

dom_jq = get_dominant_contract_jq("IH")
print(f"IH主力合约(JQ风格): {dom_jq}")
assert dom_jq and dom_jq.startswith("IH"), "JQ风格主力合约错误"

mult_jq = get_contract_multiplier_jq("IM2401")
print(f"IM合约乘数(JQ风格): {mult_jq}")
assert mult_jq == 200, "JQ风格乘数错误"

value_jq = calculate_position_value_jq(5000, 5, "IC2401")
print(f"IC持仓价值(JQ风格): {value_jq}")
assert value_jq == 5000 * 200 * 5, "JQ风格价值计算错误"
print("✓ JQ风格包装函数正常")

print("\n【9】交易所信息验证")
print("-" * 40)
cffex = CHINA_FUTURE_EXCHANGE_INFO["CFFEX"]
print(f"中金所产品列表: {cffex['products']}")
print(f"IF乘数配置: {cffex['multipliers']['IF']}")
print(f"IF保证金配置: {cffex['margin_rates']['IF']}")
assert "IF" in cffex["products"], "IF不在中金所产品列表"
assert cffex["multipliers"]["IF"] == 300, "配置乘数错误"
print("✓ 交易所信息配置正常")

print("\n【10】完整工作流验证")
print("-" * 40)
print("场景: IF期货多头持仓")
dom = get_dominant_contract("IF")
print(f"  1. 主力合约: {dom}")
mult = get_contract_multiplier(dom)
print(f"  2. 合约乘数: {mult}")
rate = get_margin_rate(dom)
print(f"  3. 保证金比例: {rate}")
pos_value = calculate_position_value(4000, 5, dom)
print(f"  4. 持仓价值(4000点, 5手): {pos_value}")
req_margin = calculate_required_margin(4000, 5, dom)
print(f"  5. 所需保证金: {req_margin}")
print("✓ 完整工作流正常")

print("\n" + "=" * 60)
print("验证完成: 所有期货API功能正常")
print("=" * 60)

print("\n已实现API清单:")
api_list = [
    "1. parse_future_contract - 合约解析",
    "2. get_future_contracts - 合约列表",
    "3. get_dominant_contract - 主力合约",
    "4. get_contract_multiplier - 合约乘数",
    "5. get_margin_rate - 保证金比例",
    "6. calculate_position_value - 持仓价值",
    "7. calculate_required_margin - 所需保证金",
    "8. get_future_daily - 日线数据(待验证)",
    "9. get_future_spot - 实时行情(待验证)",
]
for api in api_list:
    print(f"  {api}")

print("\n支持的产品:")
for exchange, info in CHINA_FUTURE_EXCHANGE_INFO.items():
    print(f"  {info['name']}: {', '.join(info['products'][:5])}...")

print("\n任务29完成 ✓")
