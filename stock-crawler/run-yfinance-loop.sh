#!/bin/bash

# YFinance API 文档循环爬取脚本
# 持续运行直到没有新链接为止

CONFIG_FILE="config/yfinance.json"
PROJECT_DIR="output/yfinance-api-docs"
LINKS_FILE="$PROJECT_DIR/links.txt"

echo "=========================================="
echo "YFinance API 文档循环爬取"
echo "=========================================="
echo ""

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件 $CONFIG_FILE 不存在"
    exit 1
fi

# 初始化计数器
iteration=0
prev_link_count=0
no_new_links_count=0
max_no_new_links=3  # 连续3次没有新链接就停止

cd "$(dirname "$0")"

while true; do
    iteration=$((iteration + 1))
    echo ""
    echo "=========================================="
    echo "第 $iteration 轮爬取"
    echo "=========================================="

    # 获取当前链接数量
    if [ -f "$LINKS_FILE" ]; then
        prev_link_count=$(wc -l < "$LINKS_FILE" | tr -d ' ')
    else
        prev_link_count=0
    fi

    echo "当前链接数量: $prev_link_count"

    # 运行爬虫
    node src/index.js "$CONFIG_FILE"

    # 检查退出状态
    if [ $? -ne 0 ]; then
        echo ""
        echo "爬虫运行出错，等待 10 秒后重试..."
        sleep 10
        continue
    fi

    # 获取新的链接数量
    if [ -f "$LINKS_FILE" ]; then
        new_link_count=$(wc -l < "$LINKS_FILE" | tr -d ' ')
    else
        new_link_count=0
    fi

    # 计算新链接数
    new_links=$((new_link_count - prev_link_count))

    echo ""
    echo "本轮统计:"
    echo "  - 之前链接数: $prev_link_count"
    echo "  - 当前链接数: $new_link_count"
    echo "  - 新增链接数: $new_links"

    # 检查是否有未爬取的链接
    if [ -f "$LINKS_FILE" ]; then
        unfetched_count=$(grep -c '"status":"unfetched"' "$LINKS_FILE" 2>/dev/null || echo "0")
        echo "  - 待爬取链接: $unfetched_count"

        if [ "$unfetched_count" -eq 0 ] && [ "$new_links" -eq 0 ]; then
            no_new_links_count=$((no_new_links_count + 1))
            echo ""
            echo "没有新链接且没有待爬取链接 ($no_new_links_count/$max_no_new_links)"

            if [ "$no_new_links_count" -ge "$max_no_new_links" ]; then
                echo ""
                echo "=========================================="
                echo "爬取完成！"
                echo "=========================================="
                echo "总共运行 $iteration 轮"
                echo "最终链接数量: $new_link_count"
                echo ""
                break
            fi
        else
            no_new_links_count=0
        fi
    fi

    # 等待一段时间再继续
    echo ""
    echo "等待 5 秒后继续下一轮..."
    sleep 5
done

echo "爬取任务结束"