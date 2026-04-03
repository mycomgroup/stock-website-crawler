"""
随机测试10个聚宽策略文件
"""

import os
import random
import glob

try:
    from jk2bt.core.runner import load_jq_strategy
except ImportError:
    print("请在仓库根目录运行此脚本")
    import sys

    sys.exit(1)

# 策略文件目录
strategy_dir = "/Users/yuping/Downloads/git/jk2bt-main/jkcode/jkcode"

# 获取所有txt文件
txt_files = glob.glob(os.path.join(strategy_dir, "*.txt"))
print(f"找到 {len(txt_files)} 个策略文件")

# 随机选择10个
selected_files = random.sample(txt_files, min(10, len(txt_files)))

print("\n" + "=" * 80)
print("随机选择的10个策略文件:")
print("=" * 80)
for i, f in enumerate(selected_files, 1):
    print(f"{i}. {os.path.basename(f)}")

print("\n" + "=" * 80)
print("开始加载测试...")
print("=" * 80)

# 测试结果统计
results = {
    "success": [],
    "failed": [],
}

# 测试每个文件
for i, strategy_file in enumerate(selected_files, 1):
    filename = os.path.basename(strategy_file)
    print(f"\n[{i}/10] 测试: {filename}")
    print("-" * 80)

    try:
        # 尝试加载策略
        functions, source = load_jq_strategy(strategy_file)

        if functions:
            # 检查关键函数
            has_init = "initialize" in functions
            has_handle = any(
                f.startswith("handle_") or f.startswith("trading_") for f in functions
            )

            print(f"  ✅ 加载成功")
            print(f"     - initialize: {'有' if has_init else '无'}")
            print(f"     - handle函数: {'有' if has_handle else '无'}")
            print(f"     - 函数数量: {len(functions)}")
            print(f"     - 函数列表: {list(functions.keys())[:5]}...")

            results["success"].append(
                {
                    "file": filename,
                    "functions": list(functions.keys()),
                }
            )
        else:
            print(f"  ❌ 加载失败: 返回None")
            results["failed"].append(
                {
                    "file": filename,
                    "error": "返回None",
                }
            )

    except Exception as e:
        error_msg = str(e)[:100]
        print(f"  ❌ 加载失败: {error_msg}")
        results["failed"].append(
            {
                "file": filename,
                "error": error_msg,
            }
        )

# 打印总结
print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print(f"总计测试: {len(selected_files)} 个策略")
print(f"✅ 成功: {len(results['success'])} 个")
print(f"❌ 失败: {len(results['failed'])} 个")

if results["success"]:
    print("\n✅ 成功的策略:")
    for item in results["success"]:
        print(f"  - {item['file']}")

if results["failed"]:
    print("\n❌ 失败的策略:")
    for item in results["failed"]:
        print(f"  - {item['file']}: {item['error']}")

# 分析常见问题
print("\n" + "=" * 80)
print("问题分析")
print("=" * 80)

if results["failed"]:
    print("\n主要失败原因:")
    error_types = {}
    for item in results["failed"]:
        error_key = (
            item["error"].split(":")[0] if ":" in item["error"] else item["error"][:30]
        )
        error_types[error_key] = error_types.get(error_key, 0) + 1

    for error, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {error}: {count} 次")

print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
