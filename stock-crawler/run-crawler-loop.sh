#!/bin/bash

# 循环运行爬虫直到没有新链接
# 用法: ./run-crawler-loop.sh <config_file>

if [ -z "$1" ]; then
    echo "Usage: $0 <config_file>"
    echo "Example: $0 config/qveris.json"
    exit 1
fi

CONFIG_FILE="$1"
PROJECT_NAME=$(basename "$CONFIG_FILE" .json)
OUTPUT_DIR="output/${PROJECT_NAME}"
LINKS_FILE="${OUTPUT_DIR}/links.txt"

echo "=== 开始循环爬取 ==="
echo "配置文件: $CONFIG_FILE"
echo "项目名称: $PROJECT_NAME"
echo ""

ITERATION=0

while true; do
    ITERATION=$((ITERATION + 1))
    echo "=== 第 ${ITERATION} 轮爬取 ==="

    # 记录当前链接数量
    if [ -f "$LINKS_FILE" ]; then
        BEFORE_COUNT=$(wc -l < "$LINKS_FILE" | tr -d ' ')
        BEFORE_PENDING=$(grep -c "pending" "$LINKS_FILE" 2>/dev/null || echo "0")
    else
        BEFORE_COUNT=0
        BEFORE_PENDING=0
    fi

    echo "当前链接总数: ${BEFORE_COUNT}"
    echo "待处理链接数: ${BEFORE_PENDING}"

    # 检查是否还有待处理的链接
    if [ "$BEFORE_PENDING" -eq 0 ] && [ "$ITERATION" -gt 1 ]; then
        echo ""
        echo "=== 没有待处理的链接，爬取完成 ==="
        break
    fi

    # 运行爬虫
    echo ""
    node --input-type=module -e "
import CrawlerMain from './src/crawler-main.js';
const crawler = new CrawlerMain();
await crawler.initialize('${CONFIG_FILE}');
await crawler.start();
" 2>&1 | grep -E "\[INFO\]|Error|error"

    echo ""

    # 检查运行后的链接数量
    if [ -f "$LINKS_FILE" ]; then
        AFTER_COUNT=$(wc -l < "$LINKS_FILE" | tr -d ' ')
        AFTER_PENDING=$(grep -c "pending" "$LINKS_FILE" 2>/dev/null || echo "0")
        NEW_LINKS=$((AFTER_COUNT - BEFORE_COUNT))
    else
        AFTER_COUNT=0
        AFTER_PENDING=0
        NEW_LINKS=0
    fi

    echo "爬取后链接总数: ${AFTER_COUNT}"
    echo "剩余待处理: ${AFTER_PENDING}"
    echo "新增链接: ${NEW_LINKS}"

    # 如果没有新增链接且没有待处理的，停止
    if [ "$NEW_LINKS" -eq 0 ] && [ "$AFTER_PENDING" -eq 0 ]; then
        echo ""
        echo "=== 没有新链接且无待处理，爬取完成 ==="
        break
    fi

    # 等待一段时间再继续
    echo ""
    echo "等待 3 秒后继续..."
    sleep 3
    echo ""
done

echo ""
echo "=== 爬取统计 ==="
if [ -f "$LINKS_FILE" ]; then
    TOTAL=$(wc -l < "$LINKS_FILE" | tr -d ' ')
    COMPLETED=$(grep -c "completed" "$LINKS_FILE" 2>/dev/null || echo "0")
    FAILED=$(grep -c "failed" "$LINKS_FILE" 2>/dev/null || echo "0")
    echo "总链接数: ${TOTAL}"
    echo "已完成: ${COMPLETED}"
    echo "失败: ${FAILED}"
fi

# 列出生成的文件
echo ""
echo "=== 生成的文件 ==="
ls -la "${OUTPUT_DIR}/pages-"* 2>/dev/null | head -20