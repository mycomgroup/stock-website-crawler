"""
测试覆盖率报告生成器
分析现有测试文件和模块的覆盖情况
"""
import os
import re
from pathlib import Path

BASE_DIR = Path("/Users/yuping/Downloads/git/jk2bt-main")
FINANCE_DIR = BASE_DIR / "src" / "finance_data"
MARKET_DIR = BASE_DIR / "src" / "market_data"
TEST_DIR = BASE_DIR / "tests"

def get_exported_functions(init_file):
    """从 __init__.py 提取导出的函数"""
    if not init_file.exists():
        return []
    
    content = init_file.read_text()
    # 提取 __all__ 列表
    match = re.search(r'__all__\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if match:
        all_str = match.group(1)
        functions = re.findall(r"'([^']+)'", all_str)
        return functions
    return []

def get_module_functions(py_file):
    """从 .py 文件提取函数定义"""
    if not py_file.exists():
        return []
    
    content = py_file.read_text()
    # 提取 def 开头的函数
    functions = re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE)
    return list(set(functions))

def find_test_file(module_name):
    """查找对应的测试文件"""
    test_patterns = [
        f"test_{module_name}.py",
        f"test_{module_name}_api.py",
        f"test_{module_name}_api_comprehensive.py",
    ]
    
    for pattern in test_patterns:
        test_file = TEST_DIR / pattern
        if test_file.exists():
            return test_file
    
    return None

print("=" * 80)
print("测试覆盖率报告")
print("=" * 80)

# 分析 finance_data 模块
print("\n## Finance Data 模块")
print("-" * 80)

finance_modules = list(FINANCE_DIR.glob("*.py"))
finance_modules = [m for m in finance_modules if m.name != "__init__.py"]

for module in sorted(finance_modules):
    module_name = module.stem
    functions = get_module_functions(module)
    
    test_file = find_test_file(module_name)
    test_status = "✅ 有测试" if test_file else "❌ 无测试"
    
    print(f"\n{module_name}.py {test_status}")
    print(f"  函数数量: {len(functions)}")
    
    if test_file:
        test_functions = get_module_functions(test_file)
        test_count = len([f for f in test_functions if f.startswith('test_')])
        print(f"  测试文件: {test_file.name}")
        print(f"  测试函数: {test_count} 个")

# 分析 market_data 模块
print("\n\n## Market Data 模块")
print("-" * 80)

market_modules = list(MARKET_DIR.glob("*.py"))
market_modules = [m for m in market_modules if m.name != "__init__.py"]

for module in sorted(market_modules):
    module_name = module.stem
    functions = get_module_functions(module)
    
    test_file = find_test_file(module_name)
    test_status = "✅ 有测试" if test_file else "❌ 无测试"
    
    print(f"\n{module_name}.py {test_status}")
    print(f"  函数数量: {len(functions)}")
    
    if test_file:
        test_functions = get_module_functions(test_file)
        test_count = len([f for f in test_functions if f.startswith('test_')])
        print(f"  测试文件: {test_file.name}")
        print(f"  测试函数: {test_count} 个")

# 统计测试文件
print("\n\n## 测试文件统计")
print("-" * 80)

test_files = list(TEST_DIR.glob("test_*.py"))
print(f"总测试文件数: {len(test_files)}")

# 统计测试函数总数
total_tests = 0
for test_file in test_files:
    test_funcs = get_module_functions(test_file)
    test_count = len([f for f in test_funcs if f.startswith('test_')])
    total_tests += test_count

print(f"总测试函数数: {total_tests}")

# 找出缺少测试的模块
print("\n\n## 缺少测试的模块")
print("-" * 80)

missing_tests = []

for module in sorted(finance_modules):
    module_name = module.stem
    test_file = find_test_file(module_name)
    if not test_file:
        missing_tests.append(f"finance_data/{module_name}.py")

for module in sorted(market_modules):
    module_name = module.stem
    test_file = find_test_file(module_name)
    if not test_file:
        missing_tests.append(f"market_data/{module_name}.py")

if missing_tests:
    for m in missing_tests:
        print(f"  - {m}")
else:
    print("  所有模块都有对应的测试文件 ✅")

print("\n" + "=" * 80)
