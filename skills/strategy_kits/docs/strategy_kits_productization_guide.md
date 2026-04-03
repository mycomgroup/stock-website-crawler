# Strategy Kits 产品化落地指南（阶段 1-4）

## 1. 目标

将 `strategy_kits` 从“可读骨架”升级为“可复用基础能力层”，支持后续以 `skill.md` 驱动大模型完成策略增强。

本指南覆盖：

1. 第 1-2 周：核心闭环稳定化  
2. 第 3-4 周：工程化与契约冻结

---

## 2. 已落地范围

### 2.1 核心闭环能力

1. `universe/stock_pool_filters/`：`st/paused/new_stock/limitup/limitdown` 已从 TODO 骨架改为可运行实现。
2. `universe/trade_calendar/`：支持 `set_trade_cal_source`、`init_trade_cal_from_gateway`、`init_trade_cal_from_csv`。
3. `signals/factor_preprocess/pipeline.py`：`fit()` 统计量已被 `transform()` 实际消费，避免训练-测试统计泄露。
4. `strategy_templates/presets/weighting_strategies.py`：接入预测面板 contract 校验。
5. `portfolio/runtime_state/rebalance_diff.py`：接入输入 contract 校验与统一日志。

### 2.2 工程化能力

1. `tests/unit`：过滤器、交易日历、预处理、contract 与调仓差分单测。
2. `tests/smoke`：单策略端到端 smoke（输入池 -> 打分 -> 配仓 -> 回测）。
3. `core/errors.py`：统一错误码。
4. `core/logging_utils.py`：统一日志事件格式。
5. `contracts/dataframe_contracts.py`：统一 DataFrame 输入输出契约。

---

## 3. 冻结的 DataFrame Contract

### 3.1 预测面板 `prediction_frame`

必需列：

1. `date`（可被 `pd.to_datetime` 解析）  
2. `code`（标准化为字符串代码）

默认补齐：

1. `weight`（缺失时默认为 `1.0`）

### 3.2 目标权重 `target_weights`

必需列：

1. `code`
2. `target_weight`

### 3.3 当前权重 `current_weights`

必需列：

1. `code`
2. `weight`

### 3.4 时序池面板 `pool_panel`（FactorHub 对接）

必需列：

1. `date`
2. `code`
3. `score`
4. `rank`

---

## 4. 错误码规范

| code | 含义 |
|---|---|
| `SK_CONTRACT_001` | 合同缺字段 |
| `SK_CONTRACT_002` | 合同值非法 |
| `SK_CAL_001` | 交易日历未初始化 |
| `SK_CAL_002` | 交易日历越界 |
| `SK_FILTER_001` | 过滤器关键数据缺失 |
| `SK_PRE_001` | 预处理器未 fit 就 transform |

---

## 5. 日志事件规范

统一格式：

`event_name | key1=value1 key2=value2 ...`

示例事件：

1. `filter_stage_done`
2. `filter_pipeline_done`
3. `trade_calendar_set_source`
4. `factor_pipeline_fitted`
5. `factor_pipeline_transformed`
6. `rebalance_diff_computed`

---

## 6. 运行测试

在仓库根目录执行：

```bash
uv run pytest skills/strategy_kits/tests
```

说明：

1. 单元测试默认全部可运行。  
2. smoke 测试依赖 `backtrader`，环境缺失时会自动 skip。  

---

## 7. 下一步建议（衔接 skill.md 自动化）

1. 增加 `integrations/factorhub/contracts.py` 与 `pool_panel -> pred_df` 适配器。  
2. 新增一份 `skill.md` 的输入规范模板：把 `pool_panel`、`strategy intent`、`risk profile` 映射到统一任务参数。  
3. 把 smoke 测试升级为 CI gating：PR 必须通过 unit + smoke 才允许合并。  

