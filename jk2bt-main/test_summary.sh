#!/bin/bash
# 测试汇总脚本

echo "========================================"
echo "测试汇总报告"
echo "========================================"

# 运行新增的测试文件
echo ""
echo "1. 运行 finance 缺失模块测试..."
.venv/bin/python -m pytest tests/test_finance_missing.py -v --tb=no -q 2>&1 | tail -5

echo ""
echo "2. 运行 market 缺失模块测试..."
.venv/bin/python -m pytest tests/test_market_missing.py -v --tb=no -q 2>&1 | tail -5

echo ""
echo "3. 运行主要 API 测试..."
.venv/bin/python -m pytest \
    tests/test_company_info_api.py \
    tests/test_dividend_api.py \
    tests/test_unlock_api.py \
    tests/test_macro_api.py \
    -v --tb=no -q 2>&1 | tail -10

echo ""
echo "========================================"
echo "测试汇总完成"
echo "========================================"
