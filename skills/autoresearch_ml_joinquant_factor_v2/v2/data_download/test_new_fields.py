"""
测试新增字段的脚本
验证 download_factors_with_price.py 修改后的功能
"""
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from v2.data_download.download_factors_with_price import (
    get_price_for_date,
    convert_stock_code,
    DUCKDB_PATH
)

def test_get_price_for_date():
    """测试获取价格数据的新字段"""
    print("=" * 60)
    print("测试 get_price_for_date 函数")
    print("=" * 60)
    
    # 测试日期：2026-04-21（昨天，应该有数据）
    test_date = "2026-04-21"
    print(f"\n测试日期: {test_date}")
    
    price_dict = get_price_for_date(test_date, DUCKDB_PATH)
    
    if not price_dict:
        print("❌ 未获取到数据")
        return False
    
    print(f"\n✓ 获取到 {len(price_dict)} 只股票的数据")
    
    # 检查第一只股票的数据结构
    first_stock = list(price_dict.keys())[0]
    first_data = price_dict[first_stock]
    
    print(f"\n示例股票: {first_stock}")
    print(f"数据字段: {list(first_data.keys())}")
    print(f"\n详细数据:")
    for key, value in first_data.items():
        print(f"  {key:20s}: {value}")
    
    # 验证所有必需字段都存在
    required_fields = ['name', 'open', 'high', 'low', 'close', 'volume', 
                      'amount', 'outstanding_share', 'turnover', 'adjust']
    
    missing_fields = [f for f in required_fields if f not in first_data]
    if missing_fields:
        print(f"\n❌ 缺少字段: {missing_fields}")
        return False
    
    print(f"\n✓ 所有必需字段都存在")
    
    # 检查数据类型
    print(f"\n数据类型检查:")
    print(f"  name (str): {type(first_data['name']).__name__}")
    print(f"  open (float): {type(first_data['open']).__name__}")
    print(f"  high (float): {type(first_data['high']).__name__}")
    print(f"  low (float): {type(first_data['low']).__name__}")
    print(f"  close (float): {type(first_data['close']).__name__}")
    print(f"  volume (float): {type(first_data['volume']).__name__}")
    
    return True


def test_convert_stock_code():
    """测试股票代码转换"""
    print("\n" + "=" * 60)
    print("测试 convert_stock_code 函数")
    print("=" * 60)
    
    test_cases = [
        ("600000.XSHG", "sh600000"),
        ("000001.XSHE", "sz000001"),
        ("300001.XSHE", "sz300001"),
        ("834599.XBSE", "bj834599"),
    ]
    
    all_passed = True
    for jq_code, expected in test_cases:
        result = convert_stock_code(jq_code)
        status = "✓" if result == expected else "❌"
        print(f"{status} {jq_code:15s} → {result:15s} (期望: {expected})")
        if result != expected:
            all_passed = False
    
    return all_passed


def main():
    print("\n" + "=" * 60)
    print("测试 download_factors_with_price.py 新增字段")
    print("=" * 60)
    
    # 测试1: 股票代码转换
    test1_passed = test_convert_stock_code()
    
    # 测试2: 获取价格数据
    test2_passed = test_get_price_for_date()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"股票代码转换: {'✓ 通过' if test1_passed else '❌ 失败'}")
    print(f"获取价格数据: {'✓ 通过' if test2_passed else '❌ 失败'}")
    
    if test1_passed and test2_passed:
        print("\n✓ 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
