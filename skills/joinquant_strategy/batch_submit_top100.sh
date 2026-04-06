#!/bin/bash
# 批量提交筛选出的Top100策略
# 使用方法: ./batch_submit_top100.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 读取筛选结果
SELECTED_FILE="data/selected_top100.json"
if [ ! -f "$SELECTED_FILE" ]; then
  echo "错误: 找不到筛选结果文件 $SELECTED_FILE"
  echo "请先运行: node select_top_strategies.js"
  exit 1
fi

# 创建临时文件列表
TEMP_LIST=$(mktemp)
node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$SELECTED_FILE', 'utf8'));
const files = data.strategies.map(s => s.file).join('\n');
fs.writeFileSync('$TEMP_LIST', files, 'utf8');
"

echo "=========================================="
echo "准备提交Top100策略"
echo "=========================================="
echo ""
cat "$SELECTED_FILE" | node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync(0, 'utf8'));
console.log('总候选策略:', data.totalCandidates);
console.log('本次提交:', data.selected);
console.log('  - 新策略:', data.statistics.newStrategies);
console.log('  - 重试失败:', data.statistics.retryFailed);
console.log('  - 平均分数:', data.statistics.avgScore);
"
echo ""
echo "=========================================="
echo ""

# 提示用户确认
read -p "是否开始提交? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "已取消"
  rm "$TEMP_LIST"
  exit 0
fi

# 执行批量提交
echo ""
echo "开始提交..."
echo ""

node batch_submit_jq558_async.js \
  --source-dir "$(pwd)/../../jk2bt-main/strategies" \
  --start "2025-04-03" \
  --end "2026-04-03" \
  --capital 100000 \
  --freq day \
  --sleep 5000 \
  --limit 100 \
  --maxConcurrent 10

# 清理
rm "$TEMP_LIST"

echo ""
echo "=========================================="
echo "提交完成！"
echo "=========================================="
