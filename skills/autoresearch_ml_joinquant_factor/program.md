# ML 多策略弱因子自动研究执行说明

## 目标
- 在 JoinQuant 环境下对弱因子组合进行自动化迭代。
- 每轮生成**多组候选因子组合**，并维护 Top-K 策略池（而不是只保留一组）。
- 降低过拟合与虚假收益风险：去相关、对齐纪律、平滑权重、成本入模。

## 执行流程
1. 运行 `setup.py` 创建实验目录（初始化）。
2. 进入实验目录，运行 `run_iteration.py` 做单轮多策略迭代。
3. 重复第 2 步，持续扩展候选并更新 Top-K。
4. 读取 `strategy_pool.json`（Top-K）和 `search_notes.md`（摘要）做策略筛选。

## 单轮迭代命令（核心）
```bash
AUTORESEARCH_DIR="/path/to/skills/autoresearch_ml_joinquant_factor"
python ${AUTORESEARCH_DIR}/run_iteration.py \
  --base . \
  --batch-size 8 \
  --top-k 5
```

- `--batch-size`：每轮生成并评估的候选组合数
- `--top-k`：保留的策略组数量
- 迭代后会更新：
  - `strategy_pool.json`（Top-K 详细结果）
  - `search_notes.md`（概览）
  - `iteration_history.jsonl`（每轮明细）
  - `strategy.py`（同步为当前第一名组合）

## 一键算 200 因子（并行）
```bash
python main.py --start-date 2020-01-01 --end-date 2024-12-31 \
  --pool small --freq weekly --n-factors 200 --workers 4 \
  --chunk-size 12 --max-retries 2 --flush-every 8 --sleep-sec 0.15 \
  --output ./artifacts/jq_200_factors.parquet
```

## JQ 容量不足时（推荐）
- 用 `--shard-count` / `--shard-index` 把 200 因子分片跑
- 降低 `--workers`（2~4）和 `--chunk-size`（8~12）
- 保留 `--sleep-sec` 节流，降低接口峰值

## 最小验收
- 有有效 JSON 输出（含 score）。
- 数据点数量充足（`data_points` 非极小值）。
- `selected_after_prune` 非空。
- `turnover_mean` 在可控范围。
- `strategy_pool.json` 至少有 2 组以上有效候选（多策略模式）。
