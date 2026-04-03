# 任务 21：因子兼容层导入回归修复

## 任务目标

修复 `factors` 兼容层的导入回归，让 `tests/test_api_compatibility.py` 中因子相关测试重新通过。

## 负责范围

- `jqdata_akshare_backtrader_utility/factors/`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 与因子导入直接相关的测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/factors/`
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task21_factor_import_regression_result.md`

## 给子 Agent 的提示词

你负责修复因子兼容层的导入回归。当前问题是：包入口模式可以工作，但 `tests/test_api_compatibility.py` 通过 `from factors import ...` 的兼容路径会失败，导致大量因子测试报 `attempted relative import beyond top-level package`。

要求：

- 修复 `factors` 目录及其子模块在以下两种模式下都能工作：
  - 包内导入：`import jqdata_akshare_backtrader_utility`
  - 兼容导入：`from factors import get_factor_values_jq`
- 重点检查：
  - `factors/__init__.py`
  - `factors/valuation.py`
  - `factors/technical.py`
  - `factors/fundamentals.py`
  - `factors/growth.py`
  - `factors/quality.py`
  - `factors/factor_zoo.py`
  - `backtrader_base_strategy.get_factor_values_jq`
- 不要只改一个文件凑过去，要确保整条因子导入链一致。
- 保持现有因子接口签名不变。

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_api_compatibility.py
```

如果全部跑太慢，至少要覆盖因子相关分组并在结果文档里写清楚。

## 任务成功总结模板

```md
# Task 21 Result

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
