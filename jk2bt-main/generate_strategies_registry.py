#!/usr/bin/env python3
"""
策略范围分类清单生成脚本

功能:
1. 扫描strategies目录下的所有文件
2. 区分可执行策略、研究文档、notebook等
3. 生成CSV和JSON清单，用于批量运行入口
4. 支持矩阵统计，避免混淆分母

使用方法:
    python generate_strategies_registry.py [--dir STRATEGIES_DIR] [--output OUTPUT_DIR]
"""

import sys
import os
import csv
import json
import argparse
from pathlib import Path
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

sys.path.insert(0, str(PROJECT_ROOT))

from jk2bt.strategy.scanner import StrategyScanner, StrategyStatus


def generate_strategies_registry(
    strategies_dir: Path,
    output_dir: Path,
    scan_all_extensions: bool = True,
) -> dict:
    """
    生成策略范围分类清单

    参数:
        strategies_dir: 策略目录路径
        output_dir: 输出目录路径
        scan_all_extensions: 是否扫描所有文件类型（True则包括ipynb/md等）

    返回:
        统计信息字典
    """
    scanner = StrategyScanner()

    # 扫描文件
    if scan_all_extensions:
        all_files = []
        for ext in ["*.txt", "*.py", "*.ipynb", "*.md"]:
            all_files.extend(strategies_dir.glob(ext))
    else:
        all_files = list(strategies_dir.glob("*.txt"))

    print(f"扫描目录: {strategies_dir}")
    print(f"总文件数: {len(all_files)}")

    # 构建清单
    registry = []
    stats = {
        "total_files": len(all_files),
        "by_kind": {},
        "by_in_scope": {"in_scope": 0, "out_of_scope": 0},
        "by_scan_status": {},
        "by_run_status": {"executable": 0, "non_executable": 0, "not_applicable": 0},
    }

    for file_path in sorted(all_files):
        file_path_str = str(file_path)
        file_name = file_path.name
        ext = file_path.suffix.lower()

        # 确定kind（文件类型）
        if ext == ".ipynb":
            kind = "notebook"
            in_scope = False
            scan_status = "excluded_notebook"
            run_status = "not_applicable"
            root_cause = "研究文档/notebook，非可执行策略"
        elif ext == ".md":
            kind = "documentation"
            in_scope = False
            scan_status = "excluded_documentation"
            run_status = "not_applicable"
            root_cause = "说明文档/研究报告"
        elif ext == ".py":
            # py文件需要特殊判断
            if (
                "test" in file_name.lower()
                or "__pycache__" in file_path_str
                or file_name.startswith(".")
            ):
                kind = "test_or_cache"
                in_scope = False
                scan_status = "excluded_test"
                run_status = "not_applicable"
                root_cause = "测试文件或缓存"
            else:
                # 其他py文件，交给scanner判断
                scan_result = scanner.scan_file(file_path_str)
                kind = "python_strategy"
                in_scope = scan_result.is_executable
                scan_status = scan_result.status.value
                run_status = "executable" if scan_result.is_executable else "non_executable"
                root_cause = scan_result.error_message or "OK"
        elif ext == ".txt":
            # txt文件交给scanner判断
            scan_result = scanner.scan_file(file_path_str)
            kind = "jq_strategy_txt"
            in_scope = scan_result.is_executable
            scan_status = scan_result.status.value
            run_status = "executable" if scan_result.is_executable else "non_executable"
            root_cause = scan_result.error_message or "OK"
        else:
            kind = "other"
            in_scope = False
            scan_status = "excluded_other"
            run_status = "not_applicable"
            root_cause = "非策略文件类型"

        entry = {
            "path": file_path_str,
            "file_name": file_name,
            "kind": kind,
            "in_scope": in_scope,
            "scan_status": scan_status,
            "run_status": run_status,
            "root_cause": root_cause,
            "scan_timestamp": datetime.now().isoformat(),
        }

        registry.append(entry)

        # 统计
        stats["by_kind"][kind] = stats["by_kind"].get(kind, 0) + 1
        stats["by_in_scope"]["in_scope" if in_scope else "out_of_scope"] += 1
        stats["by_scan_status"][scan_status] = stats["by_scan_status"].get(scan_status, 0) + 1
        stats["by_run_status"][run_status] = stats["by_run_status"].get(run_status, 0) + 1

    # 输出CSV
    csv_path = output_dir / "strategies_registry.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "path",
                "file_name",
                "kind",
                "in_scope",
                "scan_status",
                "run_status",
                "root_cause",
                "scan_timestamp",
            ],
        )
        writer.writeheader()
        writer.writerows(registry)

    print(f"\n✅ CSV清单已生成: {csv_path}")

    # 输出JSON
    json_path = output_dir / "strategies_registry.json"
    output_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "generator": "jk2bt.generate_strategies_registry",
            "version": "1.0",
            "description": "策略范围分类清单 - 区分可执行策略与研究文档",
            "strategies_dir": str(strategies_dir),
            "output_dir": str(output_dir),
        },
        "statistics": stats,
        "strategies": registry,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON清单已生成: {json_path}")

    # 打印统计报告
    print(f"\n{'=' * 80}")
    print("策略范围分类统计报告")
    print(f"{'=' * 80}")
    print(f"总文件数: {stats['total_files']}")

    print(f"\n【产品支持范围矩阵】")
    print(f"  ✅ 可执行策略 (in_scope): {stats['by_in_scope']['in_scope']}")
    print(f"  ❌ 非策略范围 (out_of_scope): {stats['by_in_scope']['out_of_scope']}")

    print(f"\n【按文件类型分布】")
    for kind, count in sorted(stats["by_kind"].items(), key=lambda x: -x[1]):
        pct = count / stats["total_files"] * 100
        print(f"  {kind:20s}: {count:4d} ({pct:5.1f}%)")

    print(f"\n【按扫描状态分布】")
    for status, count in sorted(stats["by_scan_status"].items(), key=lambda x: -x[1]):
        pct = count / stats["total_files"] * 100
        print(f"  {status:25s}: {count:4d} ({pct:5.1f}%)")

    print(f"\n【按运行状态分布】")
    for status, count in sorted(stats["by_run_status"].items(), key=lambda x: -x[1]):
        pct = count / stats["total_files"] * 100
        print(f"  {status:20s}: {count:4d} ({pct:5.1f}%)")

    print(f"\n【需隔离的非策略文件】")
    out_of_scope_files = [r for r in registry if not r["in_scope"]]
    by_kind_excluded = {}
    for r in out_of_scope_files:
        kind = r["kind"]
        by_kind_excluded[kind] = by_kind_excluded.get(kind, 0) + 1

    for kind, count in sorted(by_kind_excluded.items(), key=lambda x: -x[1]):
        print(f"  {kind:20s}: {count:4d}")

    print(f"\n{'=' * 80}")

    # 计算可跑率（只基于in_scope）
    in_scope_count = stats["by_in_scope"]["in_scope"]
    executable_count = stats["by_run_status"]["executable"]
    if in_scope_count > 0:
        success_rate = executable_count / in_scope_count * 100
        print(f"\n【可跑率】")
        print(f"  可执行策略 / 可跑策略总数: {executable_count}/{in_scope_count} = {success_rate:.1f}%")
        print(f"  注意: 分母不再包含notebook、md等非策略文件")

    print(f"{'=' * 80}\n")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="生成策略范围分类清单",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 默认扫描strategies目录
  python generate_strategies_registry.py

  # 指定目录
  python generate_strategies_registry.py --dir ./my_strategies --output ./output

  # 只扫描txt文件（排除ipynb/md）
  python generate_strategies_registry.py --txt-only
        """,
    )

    parser.add_argument(
        "--dir",
        type=Path,
        default=PROJECT_ROOT / "strategies",
        help="策略目录路径 (默认: ./strategies)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="输出目录路径 (默认: 与策略目录相同)",
    )
    parser.add_argument(
        "--txt-only",
        action="store_true",
        help="只扫描txt文件，不扫描ipynb/md等",
    )

    args = parser.parse_args()

    strategies_dir = args.dir
    output_dir = args.output or strategies_dir

    if not strategies_dir.exists():
        print(f"错误: 策略目录不存在: {strategies_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    generate_strategies_registry(
        strategies_dir=strategies_dir,
        output_dir=output_dir,
        scan_all_extensions=not args.txt_only,
    )


if __name__ == "__main__":
    main()