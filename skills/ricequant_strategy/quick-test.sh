#!/bin/bash
# RiceQuant Notebook 快速测试脚本

echo "=== RiceQuant Notebook 功能测试 ==="
echo ""

# 测试 1: 基础连接
echo "测试 1: 基础连接测试"
node run-strategy.js --cell-source "print('连接成功！时间:', datetime.datetime.now())"
echo ""

# 测试 2: 创建独立 notebook
echo "测试 2: 创建独立 notebook"
node run-strategy.js --strategy examples/simple_backtest.py --create-new
echo ""

# 测试 3: 创建临时 notebook（自动清理）
echo "测试 3: 创建临时 notebook（自动清理）"
node run-strategy.js --strategy examples/ma_strategy_notebook.py --create-new --cleanup
echo ""

echo "=== 测试完成 ==="
echo "查看结果文件："
ls -lh data/ricequant-notebook-*.json | tail -5
ls -lh data/ricequant-notebook-*.ipynb | tail -5