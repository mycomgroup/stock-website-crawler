# 任务 20：包入口与对外接口清理

## 任务目标

把包入口、导出符号、对外使用方式清理一致，避免“内部能跑、外部导入却不对”的问题。

## 负责范围

- `jqdata_akshare_backtrader_utility/__init__.py`
- 与对外导出直接相关的模块
- 简单导入验证脚本或测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task20_package_entrypoint_result.md`

## 给子 Agent 的提示词

你负责包入口与对外导出清理。

要求：

- 修正 `__init__.py` 中“文档写了但实际没导出”的符号
- 统一包入口的对外能力
- 补最小导入测试，确保：
  - `import jqdata_akshare_backtrader_utility as pkg`
  - 包入口导出的函数/类真实存在
- 不要顺手做大重构，只收口接口边界

## 任务验证

- 至少补导入测试
- 验证 `run_jq_strategy/load_jq_strategy/JQStrategyWrapper` 等对外符号状态真实一致

## 任务成功总结模板

```md
# Task 20 Result

## 修改文件
- ...

## 完成内容
- ...

## 验证方式
- ...

## 已知边界
- ...
```
