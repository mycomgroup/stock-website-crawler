#!/usr/bin/env python3
"""快速验证扫描器核心修复点的脚本"""
import os
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_scanresult_to_dict():
    """测试1: ScanResult.to_dict() 方法"""
    print("=" * 80)
    print("测试1: ScanResult.to_dict() 序列化")
    print("=" * 80)

    from jk2bt.strategy.scanner import StrategyScanner, StrategyStatus

    scanner = StrategyScanner()

    # 测试一个非策略文件
    test_file = "strategies/92 配套资料说明.txt"
    if not os.path.exists(test_file):
        print(f"警告: 测试文件不存在 {test_file}")
        return False

    result = scanner.scan_file(test_file)
    print(f"  扫描结果: {result.status.name} - {result.error_message}")

    # 测试 to_dict()
    result_dict = result.to_dict()
    print(f"  ✓ to_dict() 成功")

    # 测试JSON序列化
    json_str = json.dumps(result_dict, ensure_ascii=False)
    print(f"  ✓ JSON序列化成功 (长度: {len(json_str)})")

    # 验证字段
    assert "status" in result_dict
    assert "file_path" in result_dict
    assert "is_executable" in result_dict
    assert isinstance(result_dict["status"], str)  # 应该是字符串value
    print(f"  ✓ 所有必需字段存在且类型正确")

    print(f"  结果预览: status={result_dict['status']}, is_executable={result_dict['is_executable']}")
    return True

def test_enum_fix():
    """测试2: 枚举值修复"""
    print("\n" + "=" * 80)
    print("测试2: StrategyStatus枚举值检查")
    print("=" * 80)

    from jk2bt.strategy.scanner import StrategyStatus

    # 检查所有存在的枚举值
    existing_statuses = [
        StrategyStatus.VALID,
        StrategyStatus.NO_INITIALIZE,
        StrategyStatus.MISSING_API,
        StrategyStatus.NOT_STRATEGY,
        StrategyStatus.SYNTAX_ERROR,
        StrategyStatus.EMPTY_FILE,
    ]

    print(f"  ✓ 存在的枚举值:")
    for s in existing_statuses:
        print(f"    - {s.name}: {s.value}")

    # 检查 VALID_WITH_HANDLE 不存在
    try:
        _ = StrategyStatus.VALID_WITH_HANDLE
        print(f"  ✗ 错误: VALID_WITH_HANDLE 仍然存在")
        return False
    except AttributeError:
        print(f"  ✓ VALID_WITH_HANDLE 正确不存在")
        return True

def test_import_path():
    """测试3: run_strategies_parallel.py 的导入路径"""
    print("\n" + "=" * 80)
    print("测试3: run_strategies_parallel.py 导入路径")
    print("=" * 80)

    # 检查源文件中的导入
    with open("run_strategies_parallel.py", "r") as f:
        content = f.read()

    # 查找导入语句
    import_lines = []
    for line in content.split("\n"):
        if "from" in line and "scanner" in line:
            import_lines.append(line.strip())

    if not import_lines:
        print(f"  ✗ 未找到scanner导入语句")
        return False

    print(f"  找到的导入语句:")
    for line in import_lines:
        print(f"    {line}")
        # 应该使用正确的导入路径
        if "jk2bt.strategy.scanner" in line or "strategy_scanner" in line:
            print(f"  ✓ 导入路径正确")
            return True
        else:
            print(f"  ✗ 导入路径可能有问题")

    return False

def test_code_logic():
    """测试4: run_strategies_parallel.py 中的扫描逻辑"""
    print("\n" + "=" * 80)
    print("测试4: run_strategies_parallel.py 扫描逻辑")
    print("=" * 80)

    with open("run_strategies_parallel.py", "r") as f:
        content = f.read()

    # 检查关键修复点
    checks = {
        "VALID_WITH_HANDLE已移除": "VALID_WITH_HANDLE" not in content,
        "使用is_executable判断": "is_executable" in content,
        "SKIPPED状态处理": "SKIPPED_NOT_STRATEGY" in content,
        "scan_results合并到results": "results.extend(skipped_results)" in content,
    }

    all_passed = True
    for check_name, check_result in checks.items():
        status = "✓" if check_result else "✗"
        print(f"  {status} {check_name}")
        all_passed = all_passed and check_result

    return all_passed

def main():
    """运行所有快速测试"""
    print("\n开始快速验证扫描器修复...\n")

    results = {
        "to_dict序列化": test_scanresult_to_dict(),
        "枚举值修复": test_enum_fix(),
        "导入路径检查": test_import_path(),
        "扫描逻辑检查": test_code_logic(),
    }

    print("\n" + "=" * 80)
    print("快速测试结果汇总")
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