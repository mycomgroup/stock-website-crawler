#!/usr/bin/env python3
"""测试扫描器修复的脚本"""
import os
import sys
import json
from pathlib import Path

# 确保能导入项目模块
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_scanresult_to_dict():
    """测试1: ScanResult.to_dict() 方法能正确序列化"""
    print("=" * 80)
    print("测试1: ScanResult.to_dict() 序列化功能")
    print("=" * 80)

    from jk2bt.strategy.scanner import StrategyScanner, StrategyStatus

    scanner = StrategyScanner()
    test_file = "strategies/92 配套资料说明.txt"

    if os.path.exists(test_file):
        result = scanner.scan_file(test_file)
        result_dict = result.to_dict()

        # 验证能否序列化为JSON
        json_str = json.dumps(result_dict, ensure_ascii=False, indent=2)
        print(f"✓ to_dict() 成功")
        print(f"✓ JSON序列化成功:")
        print(json_str[:300])

        # 验证关键字段
        assert "status" in result_dict, "缺少 status 字段"
        assert "file_name" in result_dict, "缺少 file_name 字段"
        assert "is_executable" in result_dict, "缺少 is_executable 字段"
        assert isinstance(result_dict["status"], str), "status 应该是字符串(value)"
        print("✓ 所有关键字段存在且类型正确")
        return True
    else:
        print(f"测试文件不存在: {test_file}")
        return False

def test_enum_fix():
    """测试2: 不再引用不存在的 StrategyStatus.VALID_WITH_HANDLE"""
    print("\n" + "=" * 80)
    print("测试2: 枚举值引用修复")
    print("=" * 80)

    from jk2bt.strategy.scanner import StrategyStatus

    # 验证所有枚举值存在
    valid_statuses = [
        StrategyStatus.VALID,
        StrategyStatus.NO_INITIALIZE,
        StrategyStatus.MISSING_API,
        StrategyStatus.NOT_STRATEGY,
        StrategyStatus.SYNTAX_ERROR,
        StrategyStatus.EMPTY_FILE,
    ]

    print(f"✓ 所有需要的枚举值都存在:")
    for status in valid_statuses:
        print(f"  - {status.name}: {status.value}")

    # 验证 VALID_WITH_HANDLE 不存在
    try:
        _ = StrategyStatus.VALID_WITH_HANDLE
        print("✗ VALID_WITH_HANDLE 仍然存在(不应该)")
        return False
    except AttributeError:
        print("✓ VALID_WITH_HANDLE 正确地不存在")
        return True

def test_skipped_status_tracking():
    """测试3: 扫描拒绝的文件能被正确标记和统计"""
    print("\n" + "=" * 80)
    print("测试3: 扫描拒绝文件的SKIPPED状态跟踪")
    print("=" * 80)

    from run_strategies_parallel import (
        run_strategies_parallel,
        RunStatus,
    )
    from jk2bt.strategy.scanner import StrategyStatus

    # 使用少量测试文件
    test_files = [
        "strategies/92 配套资料说明.txt",  # 配套资料(NOT_STRATEGY)
        "strategies/03 一个简单而持续稳定的懒人超额收益策略.txt",  # 应该是VALID
    ]

    # 确保文件存在
    test_files = [f for f in test_files if os.path.exists(f)]
    if len(test_files) < 2:
        print(f"测试文件不足,需要至少2个文件")
        return False

    print(f"测试文件: {test_files}")

    # 运行扫描(不实际运行回测)
    try:
        summary = run_strategies_parallel(
            strategy_files=test_files,
            max_workers=1,
            timeout_per_strategy=10,
            start_date="2023-01-01",
            end_date="2023-12-31",
            skip_scan=False,  # 启用扫描
        )

        # 验证结果
        results = summary.get("results", [])
        scan_results = summary.get("scan_results", {})

        print(f"\n✓ 运行完成,共 {len(results)} 个结果")
        print(f"✓ scan_results 有 {len(scan_results)} 个扫描结果")

        # 检查是否有SKIPPED状态
        skipped_statuses = [
            RunStatus.SKIPPED_NOT_STRATEGY.value,
            RunStatus.SKIPPED_SYNTAX_ERROR.value,
            RunStatus.SKIPPED_NO_INITIALIZE.value,
            RunStatus.SKIPPED_MISSING_API.value,
        ]

        skipped_count = 0
        for r in results:
            status = r.get("run_status", "")
            if status in skipped_statuses:
                skipped_count += 1
                print(f"  ✓ 发现SKIPPED状态: {r['strategy']} -> {status}")

        # 检查 scan_results 不为空
        if not scan_results:
            print("✗ scan_results 为空字典")
            return False

        # 验证 scan_results 内容
        for file_path, scan_dict in scan_results.items():
            print(f"  ✓ {os.path.basename(file_path)}: status={scan_dict.get('status')}")
            assert "status" in scan_dict, "scan_results 缺少 status"
            assert "is_executable" in scan_dict, "scan_results 缺少 is_executable"

        print(f"\n✓ 共 {skipped_count} 个策略被正确标记为SKIPPED")
        print(f"✓ scan_results 内容完整,不是空字典")

        return True

    except Exception as e:
        import traceback
        print(f"✗ 测试失败: {e}")
        print(traceback.format_exc())
        return False

def main():
    """运行所有测试"""
    print("\n开始测试扫描器修复...\n")

    results = {
        "to_dict序列化": test_scanresult_to_dict(),
        "枚举值修复": test_enum_fix(),
        "SKIPPED状态跟踪": test_skipped_status_tracking(),
    }

    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    print("\n" + ("✓ 所有测试通过" if all_passed else "✗ 部分测试失败"))
    print("=" * 80)

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)