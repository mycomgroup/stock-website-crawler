#!/bin/bash
# 持续运行爬虫直到所有URL抓取完成

CONFIG="config/investoday.json"
MAX_RUNS=50
RUN=0

while [ $RUN -lt $MAX_RUNS ]; do
  RUN=$((RUN + 1))
  echo ""
  echo "=========================================="
  echo "第 $RUN 次运行"
  echo "=========================================="
  
  # 运行爬虫
  OUTPUT=$(node src/index.js "$CONFIG" 2>&1)
  echo "$OUTPUT" | grep -E "(Total URLs|Crawled:|Files Generated|unfetched URLs remaining)"
  
  # 检查是否还有未抓取的URL
  UNFETCHED=$(grep -c '"status":"unfetched"' ./output/investoday-data-api-docs/links.txt 2>/dev/null || echo "0")
  FETCHED=$(grep -c '"status":"fetched"' ./output/investoday-data-api-docs/links.txt 2>/dev/null || echo "0")
  
  echo ""
  echo "当前状态: 已抓取 $FETCHED, 未抓取 $UNFETCHED"
  
  # 如果没有未抓取的URL，退出
  if [ "$UNFETCHED" = "0" ]; then
    echo ""
    echo "=========================================="
    echo "所有URL已抓取完成!"
    echo "=========================================="
    break
  fi
  
  # 如果这次运行没有抓取任何页面，也退出（可能遇到问题）
  CRAWLED=$(echo "$OUTPUT" | grep "Crawled:" | awk '{print $4}')
  if [ "$CRAWLED" = "0" ]; then
    echo "本次没有抓取新页面，退出循环"
    break
  fi
  
  sleep 2
done

echo ""
echo "=== 最终统计 ==="
FETCHED=$(grep -c '"status":"fetched"' ./output/investoday-data-api-docs/links.txt)
UNFETCHED=$(grep -c '"status":"unfetched"' ./output/investoday-data-api-docs/links.txt)
FILES=$(find ./output/investoday-data-api-docs/pages-* -name "*.md" 2>/dev/null | wc -l)
SIZE=$(find ./output/investoday-data-api-docs/pages-* -name "*.md" -exec du -ch {} + 2>/dev/null | tail -1)

echo "已抓取URL: $FETCHED"
echo "未抓取URL: $UNFETCHED"
echo "生成文件数: $FILES"
echo "总大小: $SIZE"
