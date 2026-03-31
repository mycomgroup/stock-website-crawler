#!/bin/bash

# 国九条+机器学习小市值策略 - 执行脚本
# 使用RiceQuant Notebook进行技术研究验证

echo "============================================================"
echo "国九条+机器学习小市值策略 - 技术研究验证"
echo "============================================================"

# 检查环境
if [ ! -f ".env" ]; then
    echo "错误：未找到.env文件"
    echo "请创建.env文件并配置："
    echo "  RICEQUANT_USERNAME=your_username"
    echo "  RICEQUANT_PASSWORD=your_password"
    echo "  RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research"
    exit 1
fi

# 切换到ricequant_strategy目录
cd skills/ricequant_strategy

echo ""
echo "当前目录: $(pwd)"
echo ""

# 执行步骤
echo "============================================================"
echo "Step 1: 国九条筛选有效性验证"
echo "============================================================"
echo "预计时间: 1-2分钟"
echo ""

node run-strategy.js \
    --strategy "../../docs/small_cap_research_20260331/step1_guojutiao_filter.py" \
    --timeout-ms 300000 \
    --create-new

if [ $? -ne 0 ]; then
    echo "Step 1 执行失败，请检查错误信息"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 2: 因子有效性测试"
echo "============================================================"
echo "预计时间: 3-5分钟"
echo ""

node run-strategy.js \
    --strategy "../../docs/small_cap_research_20260331/step2_factor_test.py" \
    --timeout-ms 600000 \
    --create-new

if [ $? -ne 0 ]; then
    echo "Step 2 执行失败，请检查错误信息"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 3: 机器学习因子选择模型"
echo "============================================================"
echo "预计时间: 3-5分钟"
echo ""

node run-strategy.js \
    --strategy "../../docs/small_cap_research_20260331/step3_ml_model.py" \
    --timeout-ms 600000 \
    --create-new

if [ $? -ne 0 ]; then
    echo "Step 3 执行失败，请检查错误信息"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 4: 策略回测验证"
echo "============================================================"
echo "预计时间: 5-10分钟"
echo ""

node run-strategy.js \
    --strategy "../../docs/small_cap_research_20260331/step4_backtest.py" \
    --timeout-ms 600000 \
    --create-new

if [ $? -ne 0 ]; then
    echo "Step 4 执行失败，请检查错误信息"
    exit 1
fi

echo ""
echo "============================================================"
echo "技术研究验证完成"
echo "============================================================"
echo ""
echo "输出文件位置: skills/ricequant_strategy/data/"
echo ""
echo "下一步："
echo "1. 查看各步骤的输出结果"
echo "2. 分析因子有效性"
echo "3. 优化策略参数"
echo "4. 在策略编辑器中进行精确回测"
echo ""