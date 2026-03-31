#!/bin/bash
# JoinQuant Notebook 策略运行示例脚本
# 演示从零开始运行策略的完整流程

echo "=========================================="
echo "JoinQuant Notebook 策略运行示例"
echo "=========================================="

# 配置
NOTEBOOK_URL="https://www.joinquant.com/user/notebook?url=/user/21333940833/notebooks/test.ipynb"
SKILL_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook"

cd "$SKILL_DIR"

echo ""
echo "步骤1: 检查 session 文件"
if [ -f "data/session.json" ]; then
    echo "  ✓ Session 文件存在"
else
    echo "  ✗ Session 文件不存在，需要抓取"
    echo "  运行: node browser/capture-joinquant-session.js --notebook-url \"$NOTEBOOK_URL\" --headed"
    exit 1
fi

echo ""
echo "步骤2: 运行最小化测试"
echo "  命令: node run-strategy.js --strategy examples/test_mini.py --notebook-url \"$NOTEBOOK_URL\""
read -p "  按回车继续..."

node run-strategy.js \
    --strategy examples/test_mini.py \
    --notebook-url "$NOTEBOOK_URL" \
    --timeout-ms 60000

echo ""
echo "步骤3: 运行单日选股测试"
echo "  命令: node run-strategy.js --strategy examples/rfscore_simple_test.py"
read -p "  按回车继续..."

node run-strategy.js \
    --strategy examples/rfscore_simple_test.py \
    --notebook-url "$NOTEBOOK_URL" \
    --timeout-ms 120000

echo ""
echo "步骤4: 查看输出文件"
echo "  输出目录: output/"
ls -lh output/ | tail -5

echo ""
echo "=========================================="
echo "完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "  1. 查看 output/ 目录中的结果文件"
echo "  2. 修改 examples/test_mini.py 进行自己的测试"
echo "  3. 运行完整策略: node run-strategy.js --strategy examples/rfscore_full_comparison.py"
echo ""
echo "详细文档: cat README.md"
echo "快速参考: cat QUICK_REFERENCE.md"