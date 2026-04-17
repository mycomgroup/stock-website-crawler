# 任务 16：策略资源文件与本地运行包

## 任务目标

解决 `read_file/write_file`、模型文件、参数文件、研究产物等资源依赖问题，让依赖本地资源的策略能统一管理。

## 负责范围

- `jqdata_akshare_backtrader_utility/runtime_io.py`
- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- 如有需要，可新增资源打包/映射模块

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task16_runtime_resource_pack_result.md`

## 给子 Agent 的提示词

你负责把策略依赖的本地资源管理做成统一机制。

要求：

- 识别策略中对 `read_file/write_file` 的典型使用模式
- 设计并落地一个本地资源目录约定
- 支持：
  - 文本参数文件
  - CSV/JSON 数据文件
  - 模型文件
  - 运行时输出文件
- 明确路径映射策略，避免不同策略互相污染
- 尽量让批量运行时也可安全落地资源

## 任务验证

- 至少挑选几个依赖 `read_file/write_file` 的真实策略样本
- 验证资源可读、输出可回写、路径不越界

## 任务成功总结模板

```md
# Task 16 Result

## 修改文件
- ...

## 完成内容
- ...

## 资源目录方案
- ...

## 验证方式
- ...

## 已知边界
- ...
```
