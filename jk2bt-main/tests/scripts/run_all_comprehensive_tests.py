#!/usr/bin/env python3
"""
tests/run_all_comprehensive_tests.py
运行所有综合测试
"""

import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_test_file(test_file):
    """运行单个测试文件"""
    print(f"\n{'='*70}")
    print(f"运行: {test_file}")
    print('='*70)
    
    start_time = time.time()
    
    try:
        # 导入并运行测试
        module_name = test_file.replace('.py', '')
        module = __import__(f"tests.{module_name}", fromlist=['run_all_tests'])
        
        if hasattr(module, 'run_all_tests'):
            module.run_all_tests()
        
        elapsed = time.time() - start_time
        print(f"\n完成时间: {elapsed:.2f}秒")
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 70)
    print("聚宽数据 API 综合测试套件")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    test_files = [
        "test_company_info_api_comprehensive",
        "test_shareholder_api_comprehensive",
        "test_dividend_api_comprehensive",
        "test_unlock_api_comprehensive",
        "test_macro_api_comprehensive",
        "test_index_components_api_comprehensive",
        "test_industry_sw_api_comprehensive",
        "test_bond_option_api_comprehensive",
    ]
    
    results = {}
    total_start = time.time()
    
    for test_file in test_files:
        results[test_file] = run_test_file(test_file)
    
    total_elapsed = time.time() - total_start
    
    # 打印总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_file, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status}: {test_file}")
    
    print("\n" + "=" * 70)
    print(f"总计: {passed}/{total} 测试套件通过")
    print(f"总耗时: {total_elapsed:.2f}秒")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
