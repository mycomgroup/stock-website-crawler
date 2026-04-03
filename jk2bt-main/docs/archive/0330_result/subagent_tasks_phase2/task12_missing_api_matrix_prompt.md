# 任务 12：缺失 API 矩阵与实现优先级

## 任务目标

基于真实策略使用情况，生成一份“缺失 API 矩阵”，明确还缺什么、影响多少策略、应该先做什么。

## 负责范围

- `jqdata_akshare_backtrader_utility/strategy_scanner.py`
- 可新增 `api_gap_analyzer.py` 之类的辅助脚本

## 建议写入目录

- 代码写入：
  - 仓库根目录
  - `jqdata_akshare_backtrader_utility/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task12_missing_api_matrix_result.md`

## 给子 Agent 的提示词

你负责产出一份针对 txt 策略的 API 缺口矩阵。请直接做扫描和统计，不要只写建议。

要求：

- 统计真实策略中调用到的 API
- 区分：
  - 已完整支持
  - 部分支持
  - 仅占位支持
  - 完全未支持
- 对每个 API 统计：
  - 命中策略数
  - 代表策略样本
  - 当前支持状态
  - 建议优先级
- 最后给出 Top 20 最值得优先补的 API

## 任务验证

- 输出 Markdown 报告
- 输出 JSON/CSV 矩阵
- 至少人工抽查若干 API 与策略样本的一致性

## 任务成功总结模板

```md
# Task 12 Result

## 修改文件
- ...

## 完成内容
- ...

## 输出文件
- ...

## 验证方式
- ...

## 已知边界
- ...
```
