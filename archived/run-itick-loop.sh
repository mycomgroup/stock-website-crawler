#!/bin/bash

# iTick 爬虫循环脚本
# 持续运行直到没有新链接被抓取

CONFIG="config/itick.json"
OUTPUT_DIR="./output"
MAX_ITERATIONS=50  # 最大迭代次数，防止无限循环

echo "========================================"
echo "iTick 爬虫循环抓取"
echo "========================================"
echo "配置文件: $CONFIG"
echo "输出目录: $OUTPUT_DIR"
echo "最大迭代: $MAX_ITERATIONS"
echo "========================================"

# 检查配置文件是否存在
if [ ! -f "$CONFIG" ]; then
    echo "错误: 配置文件不存在: $CONFIG"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

iteration=0
prev_count=0

while [ $iteration -lt $MAX_ITERATIONS ]; do
    iteration=$((iteration + 1))
    echo ""
    echo "========================================"
    echo "第 $iteration 次迭代"
    echo "========================================"

    # 统计当前文件数量
    curr_count=$(find "$OUTPUT_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    echo "当前已抓取文件数: $curr_count"

    # 运行爬虫
    node src/crawler-main.js "$CONFIG"

    # 统计运行后的文件数量
    new_count=$(find "$OUTPUT_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

    echo ""
    echo "迭代完成: 抓取前 $curr_count 个文件 -> 抓取后 $new_count 个文件"

    # 计算新增数量
    added=$((new_count - curr_count))
    echo "本次新增: $added 个文件"

    # 如果没有新文件，停止循环
    if [ $new_count -eq $prev_count ] && [ $iteration -gt 1 ]; then
        echo ""
        echo "========================================"
        echo "没有新的链接被抓取，停止循环"
        echo "总共迭代 $iteration 次"
        echo "总共抓取 $new_count 个文件"
        echo "========================================"
        break
    fi

    prev_count=$new_count

    # 等待一段时间再继续
    if [ $iteration -lt $MAX_ITERATIONS ]; then
        echo "等待 5 秒后继续..."
        sleep 5
    fi
done

echo ""
echo "========================================"
echo "爬取完成!"
echo "最终文件数: $(find "$OUTPUT_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "========================================"