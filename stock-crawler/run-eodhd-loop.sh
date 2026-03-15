#!/bin/bash

# EODHD 爬虫循环脚本
# 持续运行直到没有新链接被抓取

CONFIG_FILE="config/eodhd.json"
PROJECT_NAME="eodhd-api-docs"
OUTPUT_DIR="output/${PROJECT_NAME}"
LINKS_FILE="${OUTPUT_DIR}/links.txt"

echo "=========================================="
echo "EODHD API 爬虫循环启动"
echo "配置文件: ${CONFIG_FILE}"
echo "链接文件: ${LINKS_FILE}"
echo "=========================================="

# 检查配置文件是否存在
if [ ! -f "${CONFIG_FILE}" ]; then
    echo "错误: 配置文件不存在: ${CONFIG_FILE}"
    exit 1
fi

round=0

while true; do
    round=$((round + 1))
    echo ""
    echo "=========================================="
    echo "第 ${round} 轮爬取开始"
    echo "=========================================="

    # 记录爬取前的链接数量
    before_count=0
    before_unfetched=0
    if [ -f "${LINKS_FILE}" ]; then
        before_count=$(wc -l < "${LINKS_FILE}" | tr -d ' ')
        before_unfetched=$(grep -c '"status":"unfetched"' "${LINKS_FILE}" 2>/dev/null || echo "0")
    fi

    echo "爬取前: 总链接 ${before_count}, 待抓取 ${before_unfetched}"

    # 运行爬虫
    node src/index.js "${CONFIG_FILE}"

    # 检查退出状态
    exit_code=$?
    if [ ${exit_code} -ne 0 ]; then
        echo "爬虫运行出错，退出码: ${exit_code}"
        sleep 5
        continue
    fi

    # 记录爬取后的链接数量
    after_count=0
    after_unfetched=0
    if [ -f "${LINKS_FILE}" ]; then
        after_count=$(wc -l < "${LINKS_FILE}" | tr -d ' ')
        after_unfetched=$(grep -c '"status":"unfetched"' "${LINKS_FILE}" 2>/dev/null || echo "0")
    fi

    echo ""
    echo "=========================================="
    echo "第 ${round} 轮爬取完成"
    echo "爬取后: 总链接 ${after_count}, 待抓取 ${after_unfetched}"
    echo "新增链接: $((after_count - before_count))"
    echo "=========================================="

    # 检查是否还有待抓取的链接
    if [ "${after_unfetched}" -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "所有链接已抓取完成！"
        echo "总计 ${round} 轮，共 ${after_count} 个链接"
        echo "=========================================="
        break
    fi

    # 如果没有新链接产生且待抓取数量没变，可能卡住了
    new_links=$((after_count - before_count))
    if [ ${new_links} -eq 0 ] && [ "${after_unfetched}" -eq "${before_unfetched}" ]; then
        echo ""
        echo "警告: 本轮没有新增链接，待抓取数量未变化"
        echo "可能所有可达链接已抓取完毕，或遇到问题"
        echo "继续下一轮..."
    fi

    # 等待一段时间再开始下一轮
    echo "等待 3 秒后开始下一轮..."
    sleep 3
done

echo ""
echo "爬取任务完成！"
echo "结果保存在: ${OUTPUT_DIR}"