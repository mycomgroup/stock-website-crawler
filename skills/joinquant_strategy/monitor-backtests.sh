#!/bin/bash

# RFScore回测监控脚本
# 每60秒检查一次回测状态

echo "开始监控6个RFScore策略回测..."
echo "按 Ctrl+C 停止监控"
echo ""

while true; do
    clear
    echo "=========================================="
    echo "  RFScore策略回测监控 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="
    echo ""
    
    cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
    node fetch-rfscore-results.js 2>&1 | grep -A 20 "RFScore策略回测结果摘要"
    
    echo ""
    echo "下次检查: 60秒后..."
    sleep 60
done
