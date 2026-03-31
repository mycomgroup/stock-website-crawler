#!/bin/bash
# RiceQuant Notebook 测试套件运行脚本

set -e

echo "=========================================="
echo "RiceQuant Notebook 测试套件"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
TOTAL=0
PASSED=0
FAILED=0

# 运行测试函数
run_test() {
    local test_name=$1
    local test_file=$2
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "运行测试: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    TOTAL=$((TOTAL + 1))
    
    if node $test_file; then
        echo ""
        echo -e "${GREEN}✓ $test_name 通过${NC}"
        PASSED=$((PASSED + 1))
    else
        echo ""
        echo -e "${RED}✗ $test_name 失败${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# 检查环境
echo "检查测试环境..."
echo ""

if [ ! -f ".env" ]; then
    echo -e "${RED}错误: .env 文件不存在${NC}"
    echo "请创建 .env 文件并配置以下变量："
    echo "  RICEQUANT_USERNAME=your_username"
    echo "  RICEQUANT_PASSWORD=your_password"
    echo "  RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research"
    exit 1
fi

echo -e "${GREEN}✓ .env 文件存在${NC}"

if [ ! -d "node_modules" ]; then
    echo ""
    echo "安装依赖..."
    npm install
    echo -e "${GREEN}✓ 依赖安装完成${NC}"
fi

echo ""
echo "=========================================="
echo "开始运行测试套件"
echo "=========================================="

# 1. Session 管理测试
run_test "Session 管理测试" "test-session.js"

# 2. 功能验证测试
run_test "功能验证测试" "test-functionality.js"

# 3. 边界情况测试
run_test "边界情况测试" "test-boundary.js"

# 4. 错误场景测试
run_test "错误场景测试" "test-error.js"

# 5. 综合测试
run_test "综合测试" "test-comprehensive.js"

# 输出总结
echo ""
echo "=========================================="
echo "测试总结"
echo "=========================================="
echo ""
echo "总计: $TOTAL 个测试套件"
echo -e "通过: ${GREEN}$PASSED${NC} 个"
echo -e "失败: ${RED}$FAILED${NC} 个"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}所有测试通过！${NC}"
    echo ""
    echo "测试报告已保存到 data/ 目录"
    echo ""
    exit 0
else
    echo -e "${RED}部分测试失败，请查看详细日志${NC}"
    echo ""
    echo "失败的测试:"
    echo "  - 检查 data/ 目录下的错误报告"
    echo "  - 确认网络连接正常"
    echo "  - 验证环境变量配置"
    echo ""
    exit 1
fi