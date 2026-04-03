# 任务 22：执行模式统一

## 任务目标

统一“包模式、脚本模式、pytest 模式”三种运行路径，减少相对导入和运行入口不一致导致的问题。

## 负责范围

- `jqdata_akshare_backtrader_utility/`
- 仓库根目录下的运行脚本
- 相关测试脚本

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - 仓库根目录
  - `tests/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task22_execution_mode_unification_result.md`

## 给子 Agent 的提示词

你负责统一项目的执行模式。当前项目既有包导入，也有把子目录塞进 `sys.path` 的脚本运行方式，导致很多模块“在一种模式下能跑，在另一种模式下会炸”。

要求：

- 梳理并统一以下模式：
  - 包内导入运行
  - 仓库根目录脚本运行
  - pytest 运行
- 重点模块：
  - `jq_strategy_runner.py`
  - `run_strategies_parallel.py`
  - `run_daily_strategy_batch.py`
  - `validate_strategies.py`
  - `market_data/*`
  - `finance_data/*`
  - `db/*`
- 不要求强行删除所有 fallback，但要求行为一致、错误明确。
- 结果文档中明确说明推荐的标准运行方式。

## 任务验证

至少验证：

```bash
python3 -m pytest -q tests/test_package_import.py tests/test_jq_runner.py
```

并至少用 1 到 2 个根目录脚本做实际执行验证。

## 任务成功总结模板

```md
# Task 22 Result

## 修改文件
- ...

## 完成内容
- ...

## 标准运行方式
- ...

## 验证方式
- ...

## 已知边界
- ...
```
