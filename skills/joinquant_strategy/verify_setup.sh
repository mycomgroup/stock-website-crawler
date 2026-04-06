#!/bin/bash
# 项目完整性验证脚本

echo "=========================================="
echo "聚宽策略批量提交系统 - 完整性验证"
echo "=========================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_file() {
  if [ -f "$1" ]; then
    echo -e "${GREEN}✓${NC} $1"
    return 0
  else
    echo -e "${RED}✗${NC} $1 (缺失)"
    return 1
  fi
}

check_dir() {
  if [ -d "$1" ]; then
    echo -e "${GREEN}✓${NC} $1"
    return 0
  else
    echo -e "${RED}✗${NC} $1 (缺失)"
    return 1
  fi
}

check_count() {
  local actual=$1
  local expected=$2
  local name=$3
  
  if [ "$actual" -eq "$expected" ]; then
    echo -e "${GREEN}✓${NC} $name: $actual (预期: $expected)"
    return 0
  else
    echo -e "${YELLOW}⚠${NC} $name: $actual (预期: $expected)"
    return 1
  fi
}

# 1. 检查核心目录
echo "1. 检查核心目录"
echo "---"
check_dir "browser"
check_dir "request"
check_dir "data"
check_dir "node_modules"
echo ""

# 2. 检查数据目录
echo "2. 检查数据目录"
echo "---"
check_dir "data/jq558_batch_20260403"
check_dir "data/jq558_batch_20260404"
check_dir "data/jq558_top100_20260405"
check_file "data/selected_top100.json"
check_file "data/session.json"
echo ""

# 3. 检查核心脚本
echo "3. 检查核心脚本"
echo "---"
check_file "select_top_strategies.js"
check_file "batch_submit_jq558_async.js"
check_file "batch_submit_selected.js"
check_file "batch_submit_top100.sh"
check_file "collect_jq558_results.js"
check_file "analyze_all_batches.js"
echo ""

# 4. 检查会话和API
echo "4. 检查会话和API"
echo "---"
check_file "browser/capture-session.js"
check_file "request/ensure-session.js"
check_file "request/joinquant-strategy-client.js"
echo ""

# 5. 检查文档
echo "5. 检查文档"
echo "---"
check_file "README.md"
check_file "PROJECT_STRUCTURE.md"
check_file "CHECKLIST.md"
check_file "data/THREE_BATCHES_SUMMARY.md"
check_file "data/TOP100_README.md"
echo ""

# 6. 检查外部依赖
echo "6. 检查外部依赖"
echo "---"
if [ -d "../../jk2bt-main/strategies" ]; then
  STRATEGY_COUNT=$(find ../../jk2bt-main/strategies -name "*.txt" -o -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
  check_count "$STRATEGY_COUNT" 489 "策略源文件"
else
  echo -e "${RED}✗${NC} ../../jk2bt-main/strategies (缺失)"
fi
echo ""

# 7. 检查提交数据
echo "7. 检查提交数据"
echo "---"

if [ -f "data/jq558_batch_20260403/submissions.jsonl" ]; then
  BATCH1_COUNT=$(wc -l < data/jq558_batch_20260403/submissions.jsonl | tr -d ' ')
  check_count "$BATCH1_COUNT" 21 "批次1提交"
  
  BATCH1_SUCCESS=$(grep -c '"status":"submitted"' data/jq558_batch_20260403/submissions.jsonl)
  check_count "$BATCH1_SUCCESS" 16 "批次1成功"
fi

if [ -f "data/jq558_batch_20260404/submissions.jsonl" ]; then
  BATCH2_COUNT=$(wc -l < data/jq558_batch_20260404/submissions.jsonl | tr -d ' ')
  check_count "$BATCH2_COUNT" 585 "批次2提交"
  
  BATCH2_SUCCESS=$(grep -c '"status":"submitted"' data/jq558_batch_20260404/submissions.jsonl)
  check_count "$BATCH2_SUCCESS" 211 "批次2成功"
fi

if [ -f "data/jq558_top100_20260405/submissions.jsonl" ]; then
  BATCH3_COUNT=$(wc -l < data/jq558_top100_20260405/submissions.jsonl | tr -d ' ')
  check_count "$BATCH3_COUNT" 100 "批次3提交"
  
  BATCH3_SUCCESS=$(grep -c '"status":"submitted"' data/jq558_top100_20260405/submissions.jsonl)
  check_count "$BATCH3_SUCCESS" 76 "批次3成功"
fi
echo ""

# 8. 检查路径配置
echo "8. 检查路径配置"
echo "---"
PATH_CHECK=$(grep "jk2bt-main/strategies" select_top_strategies.js batch_submit_selected.js 2>/dev/null | wc -l | tr -d ' ')
if [ "$PATH_CHECK" -ge 2 ]; then
  echo -e "${GREEN}✓${NC} 脚本路径配置正确 (找到 $PATH_CHECK 处引用)"
else
  echo -e "${YELLOW}⚠${NC} 脚本路径配置: 找到 $PATH_CHECK 处引用"
fi
echo ""

# 9. 检查Node.js依赖
echo "9. 检查Node.js依赖"
echo "---"
if [ -f "package.json" ]; then
  echo -e "${GREEN}✓${NC} package.json"
  
  if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js: $NODE_VERSION"
  else
    echo -e "${RED}✗${NC} Node.js 未安装"
  fi
  
  if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules (依赖已安装)"
  else
    echo -e "${YELLOW}⚠${NC} node_modules (需要运行 npm install)"
  fi
else
  echo -e "${RED}✗${NC} package.json (缺失)"
fi
echo ""

# 10. 总结
echo "=========================================="
echo "验证完成"
echo "=========================================="
echo ""
echo "项目位置: $SCRIPT_DIR"
echo ""

# 检查环境变量
if [ -f ".env" ]; then
  echo -e "${GREEN}✓${NC} .env 文件存在"
else
  echo -e "${YELLOW}⚠${NC} .env 文件不存在（需要手动创建）"
  echo ""
  echo "创建 .env 文件："
  echo "---"
  echo "JOINQUANT_USERNAME=your_username"
  echo "JOINQUANT_PASSWORD=your_password"
  echo "---"
fi

echo ""
echo "快速命令："
echo "  查看README:     cat README.md"
echo "  查看结构:       cat PROJECT_STRUCTURE.md"
echo "  查看检查清单:   cat CHECKLIST.md"
echo "  查看三批次总结: cat data/THREE_BATCHES_SUMMARY.md"
echo ""
