# 使用 JoinQuant 并行运行所有实验
# 由于 RiceQuant 不支持 jqdata，我们使用 JoinQuant Notebook

import subprocess
import time
import threading

experiments = [
    {
        "name": "实验 1A - 基准对照组",
        "file": "/Users/fengzhi/Downloads/git/testlixingren/etf_pool_rebuild/exp_1a_baseline.py",
        "desc": "旧池完整版12只ETF",
    },
    {
        "name": "实验 1B - 删除国债",
        "file": "/Users/fengzhi/Downloads/git/testlixingren/etf_pool_rebuild/exp_1b_no_bond.py",
        "desc": "删除国债ETF后的11只ETF",
    },
    {
        "name": "实验 1C - 删除跨市场保留国债",
        "file": "/Users/fengzhi/Downloads/git/testlixingren/etf_pool_rebuild/exp_1c_no_crossmarket.py",
        "desc": "删除美股和黄金但保留国债",
    },
    {
        "name": "实验 1D - 纯A股",
        "file": "/Users/fengzhi/Downloads/git/testlixingren/etf_pool_rebuild/exp_1d_pure_a_shares.py",
        "desc": "纯A股8只ETF",
    },
]


def run_experiment(exp):
    print(f"\n{'=' * 80}")
    print(f"启动: {exp['name']}")
    print(f"描述: {exp['desc']}")
    print(f"文件: {exp['file']}")
    print("=" * 80)

    cmd = [
        "node",
        "run-strategy.js",
        "--strategy",
        exp["file"],
        "--create-new",
        "--timeout-ms",
        "300000",
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd="/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook",
            capture_output=True,
            text=True,
            timeout=360,
        )

        print(f"\n{exp['name']} 完成!")
        print(f"返回码: {result.returncode}")

        # 提取 Notebook URL
        for line in result.stdout.split("\n"):
            if "notebook" in line.lower() and "http" in line:
                print(f"Notebook: {line}")

        return {
            "name": exp["name"],
            "success": result.returncode == 0,
            "stdout": result.stdout[-1000:],  # 最后1000字符
            "stderr": result.stderr[-500:],
        }
    except Exception as e:
        print(f"\n{exp['name']} 失败: {e}")
        return {"name": exp["name"], "success": False, "error": str(e)}


print("=" * 80)
print("ETF池优化实验 - 批量运行")
print("=" * 80)
print(f"共 {len(experiments)} 个实验")
print()

# 串行运行（因为 JoinQuant 可能需要共享 session）
results = []
for exp in experiments:
    result = run_experiment(exp)
    results.append(result)
    time.sleep(5)  # 间隔5秒避免冲突

# 汇总结果
print("\n\n" + "=" * 80)
print("【实验结果汇总】")
print("=" * 80)

for r in results:
    print(f"\n{r['name']}:")
    print(f"  状态: {'✅ 成功' if r['success'] else '❌ 失败'}")
    if not r["success"] and "error" in r:
        print(f"  错误: {r['error']}")
    print(f"  输出: {r.get('stdout', '')[:200]}...")

print("\n" + "=" * 80)
print("所有实验运行完成!")
