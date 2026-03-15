#!/bin/bash

# 循环运行爬虫直到没有新链接
# Loop crawler until no new links are found

CONFIG="config/serpapi.json"
PROJECT_DIR="output/serpapi-ai-overview"
LINKS_FILE="$PROJECT_DIR/links.txt"

echo "========================================"
echo "SerpApi 爬虫循环运行脚本"
echo "========================================"
echo ""

# 记录初始链接数
get_link_count() {
    if [ -f "$LINKS_FILE" ]; then
        wc -l < "$LINKS_FILE" | tr -d ' '
    else
        echo "0"
    fi
}

# 获取已抓取的链接数
get_fetched_count() {
    if [ -f "$LINKS_FILE" ]; then
        grep -c '"status":"fetched"' "$LINKS_FILE" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

round=1
prev_fetched=0

while true; do
    echo "----------------------------------------"
    echo "第 $round 轮"
    echo "----------------------------------------"

    # 运行爬虫
    node src/index.js "$CONFIG" 2>&1

    # 检查当前链接数
    current_total=$(get_link_count)
    current_fetched=$(get_fetched_count)

    echo ""
    echo "统计: 总链接数=$current_total, 已抓取=$current_fetched"

    # 如果已抓取数没有变化，说明没有新链接了
    if [ "$current_fetched" -eq "$prev_fetched" ]; then
        echo ""
        echo "========================================"
        echo "没有发现新链接，停止运行"
        echo "总共运行 $round 轮"
        echo "抓取页面数: $current_fetched"
        echo "========================================"
        break
    fi

    prev_fetched=$current_fetched
    round=$((round + 1))

    # 等待一段时间再继续
    echo "等待 3 秒后继续..."
    sleep 3
done