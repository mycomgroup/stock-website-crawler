# autoresearch_ml_joinquant_factor

独立于 `skills/autoresearch_joinquant_factor` 的新实现。

## 特点
- 初始化实验目录并生成独立 `strategy.py`。
- 策略模板内置防过拟合约束：
  - 去相关后组合
  - `t -> t+1` 标签对齐
  - IC/IR 驱动的动态缩放与平滑
  - 交易成本惩罚
- 新增完整的弱因子组合框架实现：`weak_factor_portfolio.py`，覆盖技术方案中的所有核心函数。
- 技术方案文档已迁移到当前目录：`弱因子组合量化策略技术方案.md`。

## 快速开始
```bash
cd skills/autoresearch_ml_joinquant_factor
python setup.py --name demo --pool small
```

## 一键并行计算 200 个 JQ 因子
```bash
python main.py \
  --start-date 2020-01-01 \
  --end-date 2024-12-31 \
  --pool small \
  --freq weekly \
  --n-factors 200 \
  --workers 4 \
  --chunk-size 12 \
  --max-retries 2 \
  --flush-every 8 \
  --sleep-sec 0.15 \
  --output ./artifacts/jq_200_factors.parquet
```

## JQ 爆掉时建议（分片跑）
```bash
# 200 因子拆 4 片跑（第0片）
python main.py --start-date 2020-01-01 --end-date 2024-12-31 \
  --n-factors 200 --shard-count 4 --shard-index 0 \
  --workers 3 --chunk-size 10 --output ./artifacts/jq_200_factors.parquet
```
