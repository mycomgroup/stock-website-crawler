# 低频高胜率 - 下一轮独立开发目录（V1）

这个目录是“下一轮独立文件夹”，直接对应你指定的 5 个子任务，并提供可执行代码骨架与最小可运行流程。

## 结构

- `src/task01_baseline_freeze.py`：子任务1，主仓底座统一与冻结
- `src/task02_dynamic_router_v1.py`：子任务2，主仓动态路由V1工程化
- `src/task03_rsrs_filter.py`：子任务3，RSRS过滤层收口
- `src/task04_rfscore_whitelist.py`：子任务4，RFScore增强因子白名单化
- `src/task05_etf_macro_mapping.py`：子任务5，低频ETF/宏观慢变量并入主账户结构
- `src/run_next_round.py`：一键串联五个任务
- `examples/`：最小样例输入
- `outputs/`：默认输出目录

## 运行

```bash
python research/low_freq_highwinrate_next_round_v1/src/run_next_round.py \
  --market-csv research/low_freq_highwinrate_next_round_v1/examples/market_snapshots.csv \
  --factor-csv research/low_freq_highwinrate_next_round_v1/examples/factor_incremental_metrics.csv \
  --prototype-csv research/low_freq_highwinrate_next_round_v1/examples/prototype_strategies.csv \
  --out-dir research/low_freq_highwinrate_next_round_v1/outputs
```

## 说明

- 当前为工程化 V1：先保证接口清晰、规则可执行、输出可审计。
- 若你确认，我下一步可接着补：
  1) 回测引擎适配层（接你现有框架）
  2) 真数据字段映射
  3) 分任务单测与回归样例
