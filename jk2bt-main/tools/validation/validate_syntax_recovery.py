"""
补充验证: 专门测试语法错误的策略恢复率
"""

import os
import sys
import csv
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.strategy.txt_normalizer import TxtNormalizer


def validate_syntax(filepath):
    """验证语法"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        compile(content, filepath, "exec")
        return True, None
    except SyntaxError as e:
        return False, f"{e.msg} (行 {e.lineno})"
    except Exception as e:
        return False, str(e)


def test_syntax_errors():
    """测试所有语法错误的策略"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inventory_csv = os.path.join(
        base_dir, "docs/0330_result/task11_strategy_inventory.csv"
    )

    syntax_error_files = []

    with open(inventory_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            error_info = row.get("错误信息", "")
            if "语法错误" in error_info or "syntax_error" in row.get("扫描状态", ""):
                filepath = row.get("文件路径", "")
                if filepath and os.path.exists(filepath):
                    syntax_error_files.append(
                        {
                            "path": filepath,
                            "filename": row.get("文件名", ""),
                            "error": error_info,
                        }
                    )

    print(f"找到 {len(syntax_error_files)} 个语法错误文件")

    if not syntax_error_files:
        print("未找到语法错误文件")
        return

    # 创建标准化器
    output_dir = tempfile.mkdtemp(prefix="syntax_test_")
    normalizer = TxtNormalizer(output_dir=output_dir)

    results = []

    for file_info in syntax_error_files:
        filepath = file_info["path"]
        filename = file_info["filename"]

        print(f"\n测试: {filename}")

        # 原始验证
        before_valid, before_err = validate_syntax(filepath)
        print(f"  原始: {before_valid}")

        # 标准化
        norm_result = normalizer.normalize_file(filepath)

        if norm_result.normalized_path:
            after_valid, after_err = validate_syntax(norm_result.normalized_path)
            print(f"  标准化后: {after_valid}")

            if not before_valid and after_valid:
                print(
                    f"  ✓ 成功恢复! 修复: {[i.value for i in norm_result.issues_fixed]}"
                )
                results.append(
                    {
                        "filename": filename,
                        "recovered": True,
                        "fixes": [i.value for i in norm_result.issues_fixed],
                    }
                )
            else:
                print(f"  ✗ 仍失败: {after_err}")
                results.append(
                    {
                        "filename": filename,
                        "recovered": False,
                        "fixes": [i.value for i in norm_result.issues_fixed],
                        "error": after_err,
                    }
                )
        else:
            print(f"  ✗ 标准化失败")
            results.append(
                {
                    "filename": filename,
                    "recovered": False,
                    "fixes": [],
                    "error": norm_result.error_message,
                }
            )

    # 统计
    recovered = sum(1 for r in results if r["recovered"])
    total = len(results)

    print("\n" + "=" * 80)
    print(f"语法错误恢复统计: {recovered}/{total} ({recovered / total * 100:.1f}%)")
    print("=" * 80)

    # 写入结果
    result_file = os.path.join(base_dir, "docs/0330_result/task37_syntax_recovery.json")
    import json

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total": total,
                "recovered": recovered,
                "rate": recovered / total * 100,
                "details": results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\n结果已保存到: {result_file}")

    # 清理
    import shutil

    shutil.rmtree(output_dir)


if __name__ == "__main__":
    test_syntax_errors()
