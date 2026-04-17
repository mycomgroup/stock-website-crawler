# 任务 9：资产路由与子账户模型

## 任务目标

补齐资产识别、子账户路由和 `transfer_cash` 的最小可用实现，先让股票、ETF、基金、股指期货这几类路径清晰可用。

## 负责范围

- `jqdata_akshare_backtrader_utility/asset_router.py`
- `jqdata_akshare_backtrader_utility/subportfolios.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 对应测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task09_asset_router_subportfolio_result.md`

## 给子 Agent 的提示词

你负责资产识别和子账户最小模型，请直接开发。

重点要求：

- 识别并区分：
  - 股票
  - ETF
  - LOF/OF
  - 指数
  - 股指期货
- 修复或改进：
  - `context.subportfolios`
  - `set_subportfolios`
  - `transfer_cash`
- 避免使用脆弱的非相对导入
- 重点是建立清晰边界和最小可用行为，不要求一次做完整券商级账户系统
- 不要去扩展分钟数据或 finance

## 任务验证

至少完成以下验证：

- 不同资产代码能被正确识别
- `set_subportfolios` 能构建多个子账户
- `transfer_cash` 有基本校验和状态变更
- 普通包导入路径下不因为导入方式报错

建议命令：

```bash
python3 -m pytest -q tests/test_context_simulation.py
```

## 任务成功总结模板

```md
# Task 09 Result

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
