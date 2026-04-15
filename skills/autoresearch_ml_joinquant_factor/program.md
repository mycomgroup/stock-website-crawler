# ML 弱因子自动研究执行说明

## 目标
- 在 JoinQuant 环境下对弱因子组合进行自动化迭代。
- 降低过拟合与虚假收益风险：去相关、对齐纪律、平滑权重、成本入模。

## 执行流程
1. 运行 `setup.py` 创建实验目录。
2. 检查 baseline 的 `search_notes.md` 与 `seed_config.json`。
3. 每轮只改少量因子或少量参数，记录结果。
4. 对于高分结果，优先复验换手与成本惩罚后分数。

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
