# 任务 28：多资产数据接入

## 任务目标

把 LOF、场外基金、股指期货的数据接入从“梳理阶段”推进到“最小可用”。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/`
- `jqdata_akshare_backtrader_utility/asset_router.py`
- 与多资产数据接入直接相关的测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/market_data/`
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task28_multi_asset_data_result.md`

## 给子 Agent 的提示词

你负责多资产数据接入，不是交易撮合，而是先解决“有没有数据、能不能读”。

要求：

- 补齐或验证：
  - LOF 数据
  - OF 净值数据
  - CCFX/期货行情数据
- 输出标准化后的字段和接口
- 不要在结果文档里把“理论可接”写成“已支持”，必须按真实状态区分
- 优先做最小可用数据读取，不要一开始就追求完整交易链

## 任务验证

- 至少每类资产验证 1 到 2 个样本
- 明确记录：
  - 数据可读取
  - 数据不可读
  - 仅有接口未验证

## 任务成功总结模板

```md
# Task 28 Result

## 修改文件
- ...

## 已接入资产
- ...

## 未接入资产
- ...

## 验证样本
- ...

## 已知边界
- ...
```
