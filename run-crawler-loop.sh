#!/usr/bin/env bash

# 并行爬虫执行脚本
# 遍历 config 下所有任务，每个任务跑 10 轮，每次并行跑 5 个任务

# 确保 bash 版本
if [ -z "$BASH_VERSION" ]; then
    echo "错误: 此脚本需要 bash 运行"
    exit 1
fi

set -e

# ==================== 配置区 ====================
WORK_DIR="/Users/yuping/Downloads/git/stock-website-crawler/stock-crawler"
CONFIG_DIR="config"
ROUNDS_PER_TASK=10      # 每个任务跑的轮数
PARALLEL_JOBS=5         # 并行任务数
INTERVAL_SECONDS=60     # 每轮之间的间隔时间(秒)
LOG_DIR="$WORK_DIR/logs"

# ==================== 初始化 ====================
echo "========================================"
echo "并行爬虫任务启动器"
echo "========================================"
echo "工作目录: $WORK_DIR"
echo "并行数: $PARALLEL_JOBS"
echo "每任务轮数: $ROUNDS_PER_TASK"
echo "轮次间隔: ${INTERVAL_SECONDS}秒"
echo "开始时间: $(date)"
echo "========================================"

# 检查工作目录
if [ ! -d "$WORK_DIR" ]; then
    echo "错误: 工作目录不存在: $WORK_DIR"
    exit 1
fi

# 创建日志目录
mkdir -p "$LOG_DIR"

# 获取所有配置文件（递归遍历 config 下所有 json）
CONFIG_FILES=()
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    if [ "$filename" != "example.json" ]; then
        CONFIG_FILES+=("$file")
    fi
done < <(find "$WORK_DIR/$CONFIG_DIR" -type f -name "*.json" -print0)

TOTAL_TASKS=${#CONFIG_FILES[@]}
echo "发现配置文件: $TOTAL_TASKS 个"
echo ""

# 打印配置文件列表
idx=0
for config_file in "${CONFIG_FILES[@]}"; do
    idx=$((idx + 1))
    config_name=$(basename "$config_file")
    echo "  [$idx] $config_name"
done
echo ""

# ==================== 任务执行函数 ====================
run_task() {
    local config_file="$1"
    local round="$2"
    local total_rounds="$3"
    local task_name=$(basename "$config_file" .json)
    local log_file="$LOG_DIR/${task_name}_round${round}.log"

    echo "[开始] $task_name 第 $round/$total_rounds 轮 - $(date '+%H:%M:%S')"

    cd "$WORK_DIR" && npm run crawl "$config_file" > "$log_file" 2>&1

    if [ $? -eq 0 ]; then
        echo "[成功] $task_name 第 $round/$total_rounds 轮 - $(date '+%H:%M:%S')"
    else
        echo "[失败] $task_name 第 $round/$total_rounds 轮 - 查看日志: $log_file"
    fi
}

export -f run_task
export WORK_DIR LOG_DIR

# ==================== 主循环 ====================
echo "========================================"
echo "开始执行任务..."
echo "========================================"

START_TIME=$(date +%s)

# 对每个配置文件执行多轮
for round in $(seq 1 $ROUNDS_PER_TASK); do
    echo ""
    echo "###### 第 $round/$ROUNDS_PER_TASK 轮 ######"
    echo "开始时间: $(date)"

    # 并行执行所有配置文件，每次最多 PARALLEL_JOBS 个
    # 分批处理，兼容旧版 bash
    total_configs=${#CONFIG_FILES[@]}
    batch=0
    while [ $batch -lt $total_configs ]; do
        # 启动一批任务
        pids=()
        for i in $(seq 1 $PARALLEL_JOBS); do
            idx=$((batch + i - 1))
            if [ $idx -lt $total_configs ]; then
                config_file="${CONFIG_FILES[$idx]}"
                task_name=$(basename "$config_file" .json)
                log_file="$LOG_DIR/${task_name}_round${round}.log"

                (
                    echo "[开始] $task_name 第 $round 轮 - $(date '+%H:%M:%S')"
                    cd "$WORK_DIR" && npm run crawl "$config_file" > "$log_file" 2>&1
                    if [ $? -eq 0 ]; then
                        echo "[成功] $task_name 第 $round 轮 - $(date '+%H:%M:%S')"
                    else
                        echo "[失败] $task_name 第 $round 轮 - 日志: $log_file"
                    fi
                ) &
                pids+=($!)
            fi
        done

        # 等待这批任务完成
        for pid in "${pids[@]}"; do
            wait $pid
        done

        batch=$((batch + PARALLEL_JOBS))
    done

    echo ""
    echo "第 $round 轮完成: $(date)"

    # 如果不是最后一轮，等待间隔时间
    if [ $round -lt $ROUNDS_PER_TASK ]; then
        echo "等待 ${INTERVAL_SECONDS} 秒后开始下一轮..."
        sleep $INTERVAL_SECONDS
    fi
done

# ==================== 统计信息 ====================
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))
SECONDS=$((DURATION % 60))

echo ""
echo "========================================"
echo "所有任务已完成!"
echo "========================================"
echo "结束时间: $(date)"
echo "总耗时: ${HOURS}小时 ${MINUTES}分钟 ${SECONDS}秒"
echo "总任务数: $TOTAL_TASKS 个配置"
echo "每任务轮数: $ROUNDS_PER_TASK 轮"
echo "总执行次数: $((TOTAL_TASKS * ROUNDS_PER_TASK)) 次"
echo "日志目录: $LOG_DIR"
echo "========================================"
