#!/bin/bash

#循环执行脚本
#循调用爬虫100次，每次间隔10分钟

echo "开始执行爬虫循环任务..."
echo "总次数: 100次"
echo "间隔时间: 10分钟"
echo "开始时间: $(date)"
echo "================================"

# 设置工作目录
WORK_DIR="/Users/yuping/Downloads/git/stock-website-crawler/stock-crawler"
CONFIG_FILE="config/eulerpool.json"

#检查工作目录是否存在
if [ ! -d "$WORK_DIR" ]; then
    echo "错误:工作目录不存在: $WORK_DIR"
    exit 1
fi

#检查配置文件是否存在
if [ ! -f "$WORK_DIR/$CONFIG_FILE" ]; then
    echo "错误:配置文件不存在: $WORK_DIR/$CONFIG_FILE"
    exit 1
fi

#循100次
for i in {1..100}; do
    echo "================================"
    echo "执行第 $i取 (总共100次)"
    echo "当前时间: $(date)"
    echo "================================"
    
    #切换到工作目录并执行爬虫
    cd "$WORK_DIR" && npm run crawl "$CONFIG_FILE"
    
    #检查执行结果
    if [ $? -eq 0 ]; then
        echo "第 $i取成功完成"
    else
        echo "警告: 第 $i次爬取执行失败"
    fi
    
    # 如果不是最后一次执行，则等待10分钟
    if [ $i -lt 100 ]; then
        echo "等待10分钟后再执行下一次..."
        echo "下次执行时间: $(date -v+10M)"
        sleep 600  # 600秒 = 10分钟
    fi
done

echo "================================"
echo "所有爬取任务已完成!"
echo "结束时间: $(date)"
echo "总共执行: 100次"
echo "================================"