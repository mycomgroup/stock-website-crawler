# 任务 8：指数成分股与权重对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“指数成分股及权重”相关接口，重点保证成分股、权重、历史变更的统一入口可用和字段稳定。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/index_components.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有必要：
  - `jqdata_akshare_backtrader_utility/market_data/__init__.py`
- 测试：
  - `tests/test_index_components_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task08_index_components_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 指数成分股与权重接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10291_overview_指数成分股及权重.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_index_components`
  - `get_index_weights`
  - `get_index_component_history`
  - `finance.STK_INDEX_COMPONENTS`
  - `finance.STK_INDEX_WEIGHTS`
- 确保模块内 `FinanceQuery` 和全局 `finance` 查询一致
- 稳定字段至少包括：
  - `index_code`
  - `code`
  - `weight`
  - `effective_date`
  - 历史变更相关日期字段
- 不要顺手改股票行情主逻辑

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_index_components_api.py
```

建议额外覆盖：

- 权重表和成分表两种入口
- 历史日期查询
- 指数代码别名兼容

## 任务成功总结模板

```md
# Task 08 Result

## 修改文件
- ...

## 完成内容
- ...

## 验证命令
```bash
...
```

## 验证结果
- ...

## 已知边界
- ...
```
