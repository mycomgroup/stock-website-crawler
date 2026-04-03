# 任务 29：期货交易模型与合约 API

## 任务目标

补齐股指期货/期货策略真正需要的最小交易模型与合约信息 API。

## 负责范围

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `jqdata_akshare_backtrader_utility/asset_router.py`
- 可新增 `futures_*` 模块
- 相关测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task29_futures_trading_model_result.md`

## 给子 Agent 的提示词

你负责期货策略所需的最小交易模型和合约 API。

要求：

- 优先补齐：
  - `get_future_contracts`
  - `get_dominant_contract`
  - `get_contract_multiplier`
- 梳理并尽量落地：
  - 保证金
  - 合约乘数
  - 主力合约切换
  - 结算价/持仓价值计算
- 不要求一次做完整期货交易系统，但要建立最小可运行路径

## 任务验证

- 至少选取几个真实期货相关策略样本
- 至少验证若干合约 API 返回值

## 任务成功总结模板

```md
# Task 29 Result

## 修改文件
- ...

## 已实现 API
- ...

## 验证样本
- ...

## 验证方式
- ...

## 已知边界
- ...
```
