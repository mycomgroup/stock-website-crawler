#!/bin/bash

# RiceQuant 回测脚本 - 带重试和改进配置

STRATEGY_ID=${1:-2415370}
STRATEGY_FILE=${2:-examples/mainline_simple_test.py}
START_DATE=${3:-2024-06-01}
END_DATE=${4:-2024-06-30}

echo "=========================================="
echo "RiceQuant Enhanced Backtest Runner"
echo "=========================================="
echo "Strategy ID: $STRATEGY_ID"
echo "File: $STRATEGY_FILE"
echo "Period: $START_DATE to $END_DATE"
echo "=========================================="
echo ""

# 运行增强版
node run-skill-enhanced.js \
  --id "$STRATEGY_ID" \
  --file "$STRATEGY_FILE" \
  --start "$START_DATE" \
  --end "$END_DATE"

# 如果失败，提供替代方案
if [ $? -ne 0 ]; then
  echo ""
  echo "=========================================="
  echo "⚠️  RiceQuant backtest failed"
  echo "=========================================="
  echo ""
  echo "Alternative options:"
  echo "1. Wait 5 minutes and retry (server may be busy)"
  echo "2. Use shorter time range"
  echo "3. Use JoinQuant Notebook instead:"
  echo "   cd ../joinquant_notebook"
  echo "   node run-strategy.js --strategy examples/mainline_simple_test_jq.py"
  echo ""
fi