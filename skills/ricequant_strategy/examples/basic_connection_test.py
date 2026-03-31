"""
基本连接测试 - RiceQuant Notebook

只测试 Python 基础功能，不使用量化 API
"""

print("=== RiceQuant Notebook 基本连接测试 ===")

from datetime import datetime
print(f"当前时间: {datetime.now()}")

import sys
print(f"Python 版本: {sys.version}")

import os
print(f"当前目录: {os.getcwd()}")

# 测试基本计算
test_list = [1, 2, 3, 4, 5]
print(f"列表计算: sum={sum(test_list)}, avg={sum(test_list)/len(test_list)}")

print("\n✓ 基本连接测试成功！")
print("=== 测试完成 ===")
