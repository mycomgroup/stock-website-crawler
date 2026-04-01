#!/bin/bash

# 5个代表性策略批量测试脚本
# 测试米筐平台是否可以替代聚宽

echo "============================================================"
echo "5个代表性策略批量测试"
echo "测试目的: 验证米筐完全可以替代聚宽"
echo "============================================================"

cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy

strategies=(
    "01_pure_cash_defense"
    "02_pure_treasury_defense"
    "03_smallcap_low_pb_defense"
    "04_rfscore_pure_offensive"
    "05_combo_rfscore_dividend"
)

strategy_dir="../../strategies/Ricequant/migrated_5representative"

for strategy in "${strategies[@]}"; do
    echo ""
    echo "============================================================"
    echo "测试策略: ${strategy}"
    echo "============================================================"
    
    node run-strategy.js \
        --strategy "${strategy_dir}/${strategy}.py" \
        --create-new \
        --timeout-ms 300000
    
    echo ""
    echo "策略 ${strategy} 测试完成"
    echo "============================================================"
    
    sleep 5
done

echo ""
echo "============================================================"
echo "全部测试完成"
echo "============================================================"
echo ""
echo "测试结果目录: /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/data"
echo ""
echo "查看测试结果:"
echo "  cat data/ricequant-notebook-result-*.json | jq '.executions[0].textOutput'"
echo ""
echo "============================================================"