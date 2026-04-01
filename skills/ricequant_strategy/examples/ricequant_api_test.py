"""
RiceQuant API 测试 - Notebook 版本

测试 RiceQuant Notebook 中的量化 API
"""

print("=== RiceQuant Notebook API 测试 ===")

from datetime import datetime
print(f"当前时间: {datetime.now()}")

# 测试 RiceQuant 特有导入
try:
    # 尝试不同的导入方式
    import ricequant
    print(f"✓ ricequant 模块可用")
except ImportError:
    print("✗ ricequant 模块不可用")

# 测试基本 Python
test_data = [i for i in range(10)]
print(f"✓ 基本Python功能正常: {test_data}")

# 测试是否在 RiceQuant Notebook 环境
import os
print(f"当前目录: {os.getcwd()}")

# RiceQuant Notebook 应该有特殊的全局变量或环境
print("\n检查全局变量...")
globals_list = [name for name in globals() if not name.startswith('_')]
print(f"全局变量数量: {len(globals_list)}")

print("\n=== 测试完成 ===")
