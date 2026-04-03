# 并行策略运行器

并行运行txt格式的策略文件，支持：
- 每个策略超时1小时（可配置）
- 最多5个策略同时运行（可配置）
- 详细日志记录到logs目录

## 使用方法

### 基本用法

```bash
# 运行所有策略（默认最多5个并行，每个超时1小时）
python3 run_strategies_parallel.py

# 查看找到的策略文件列表
python3 run_strategies_parallel.py --list-only

# 限制运行策略数量（测试用）
python3 run_strategies_parallel.py --limit 10 --no-confirm
```

### 常用参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--strategies-dir` | `jkcode/jkcode` | 策略文件目录 |
| `--pattern` | `*.txt` | 策略文件匹配模式 |
| `--max-workers` | `5` | 最大并行数 |
| `--timeout` | `3600` | 单策略超时时间（秒，默认1小时） |
| `--start-date` | `2022-01-01` | 回测开始日期 |
| `--end-date` | `2022-03-31` | 回测结束日期 |
| `--capital` | `1000000` | 初始资金 |
| `--limit` | `0` | 限制运行策略数量（0不限制） |
| `--list-only` | - | 仅列出策略文件 |
| `--no-confirm` | - | 跳过确认直接运行 |

### 示例命令

```bash
# 运行所有策略，自定义参数
python3 run_strategies_parallel.py \
  --max-workers 3 \
  --timeout 7200 \
  --start-date 2020-01-01 \
  --end-date 2023-12-31 \
  --no-confirm

# 测试运行前5个策略
python3 run_strategies_parallel.py --limit 5 --timeout 300 --no-confirm

# 运行特定目录的策略
python3 run_strategies_parallel.py --strategies-dir my_strategies --no-confirm
```

## 日志输出

每次运行会在 `logs/strategy_runs/<运行ID>/` 目录生成以下文件：

1. **main.log** - 主运行日志
   - 运行配置信息
   - 策略提交和完成状态
   - 总体汇总信息

2. **summary.json** - JSON格式汇总结果
   - 运行配置
   - 成功/失败统计
   - 每个策略的详细结果（包含错误堆栈）

3. **report.txt** - 文本格式运行报告
   - 成功策略列表（包含收益率）
   - 失败策略列表（包含错误信息）

4. **strategies/<策略名>.log** - 每个策略的详细日志
   - 策略加载过程
   - 运行过程中的错误、警告
   - 性能分析数据

## 日志示例

```
logs/strategy_runs/
└── 20260330_131814/
    ├── main.log
    ├── summary.json
    ├── report.txt
    └── strategies/
        ├── 20260330_131814_策略1.log
        └── 20260330_131814_策略2.log
```

## 注意事项

### DuckDB并发访问问题

当多个进程同时访问同一个DuckDB数据库文件时，可能会出现锁冲突错误。如果遇到此问题：
- 可以减少并行数（`--max-workers 1`）
- 或者确保数据库使用支持并发访问的配置

### 资源消耗

运行大量策略会消耗较多资源：
- 网络带宽：下载股票数据
- 内存：每个进程加载策略和数据
- CPU：回测计算

建议先用少量策略测试（如 `--limit 10`），再逐步增加。

### 错误诊断

查看失败策略的详细信息：
```bash
# 查看JSON汇总中的错误堆栈
cat logs/strategy_runs/<运行ID>/summary.json | jq '.results[] | select(.success==false)'

# 查看策略详细日志
cat logs/strategy_runs/<运行ID>/strategies/*.log
```

## 典型工作流程

1. 先列出策略文件确认数量：
   ```bash
   python3 run_strategies_parallel.py --list-only
   ```

2. 测试少量策略验证配置：
   ```bash
   python3 run_strategies_parallel.py --limit 5 --timeout 180 --no-confirm
   ```

3. 检查测试结果：
   ```bash
   cat logs/strategy_runs/<最新运行ID>/report.txt
   ```

4. 运行全部策略：
   ```bash
   python3 run_strategies_parallel.py --no-confirm
   ```

5. 分析结果：
   ```bash
   # 查看成功率和统计
   cat logs/strategy_runs/<运行ID>/summary.json | jq '.summary'
   
   # 查看失败的策略
   cat logs/strategy_runs/<运行ID>/report.txt | grep -A 3 "失败策略"
   ```