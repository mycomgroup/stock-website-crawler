# 任务 25：策略资源依赖落地

## 任务目标

把依赖 `read_file/write_file`、CSV、JSON、模型文件的策略，从“有资源框架”推进到“真实资源能落地”。

## 负责范围

- `jqdata_akshare_backtrader_utility/runtime_resource_pack.py`
- `jqdata_akshare_backtrader_utility/runtime_io.py`
- 真实策略中的资源依赖扫描与映射脚本

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - 仓库根目录
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task25_resource_dependency_seeding_result.md`

## 给子 Agent 的提示词

你负责让依赖外部资源文件的策略真正可跑。

要求：

- 扫描真实策略中：
  - `read_file(...)`
  - `write_file(...)`
  - `open(...)`
  - 可能的相对路径资源依赖
- 产出：
  - 已解析出的资源依赖清单
  - 无法解析的依赖清单
  - 可自动落地的资源包目录
- 至少拿几个真实依赖文件资源的策略做验证
- 区分：
  - 资源机制可用
  - 资源文件真实存在
  - 资源内容足以让策略跑通

## 任务验证

- 至少验证 3 到 5 个真实依赖资源的策略样本
- 输出成功与失败样本

## 任务成功总结模板

```md
# Task 25 Result

## 修改文件
- ...

## 资源依赖清单
- ...

## 成功样本
- ...

## 失败样本
- ...

## 已知边界
- ...
```
