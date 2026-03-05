#!/bin/bash
# HAR 提取快速开始脚本

echo "================================"
echo "HAR API 提取工具 - 快速开始"
echo "================================"
echo ""

# 检查参数
if [ $# -lt 2 ]; then
    echo "使用方法:"
    echo "  ./quick-start-har.sh <url> <name>"
    echo ""
    echo "示例:"
    echo "  ./quick-start-har.sh https://api.example.com/users users"
    echo ""
    exit 1
fi

URL=$1
NAME=$2

echo "URL: $URL"
echo "名称: $NAME"
echo ""

# 执行完整工作流
echo "开始提取..."
node scripts/auto-extract-workflow.js "$URL" "$NAME"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ 提取完成！"
    echo "================================"
    echo ""
    echo "输出目录: output/har-extraction/$NAME/"
    echo ""
    echo "查看文档:"
    echo "  cat output/har-extraction/$NAME/SUMMARY.md"
    echo ""
    echo "测试 Python 代码:"
    echo "  cd output/har-extraction/$NAME/apis/python"
    echo "  python api_1_*.py"
    echo ""
    echo "测试 Node.js 代码:"
    echo "  cd output/har-extraction/$NAME/apis/node"
    echo "  node api_1_*.js"
    echo ""
else
    echo ""
    echo "❌ 提取失败"
    exit 1
fi
