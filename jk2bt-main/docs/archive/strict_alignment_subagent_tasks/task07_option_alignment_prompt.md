# 任务 7：期权数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“期权列表 / 期权交易标的 / 期权交易列表 / 期权基础表 / 期权日行情表”相关接口。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/option.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有必要：
  - `jqdata_akshare_backtrader_utility/market_data/__init__.py`
- 测试：
  - `tests/test_option_api.py`
  - 如关联则看 `tests/test_bond_option_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task07_option_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 期权数据接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10030_overview_期权列表.md`
- `doc_JQDatadoc_10251_overview_期权交易标的列表.md`
- `doc_JQDatadoc_10252_overview_获取期权交易列表.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_option_list`
  - `get_option_quote`
  - `get_option_greeks`
  - `get_option_chain`
  - `get_option_info`
  - `finance.STK_OPTION_BASIC`
  - `finance.STK_OPTION_DAILY`
- 确保模块内查询能力和全局 `finance` 查询一致
- 注意期权代码、标的代码、行权价、到期日等关键字段命名
- 空结果和非法代码要返回稳定 schema

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_option_api.py
```

建议额外覆盖：

- `STK_OPTION_BASIC` / `STK_OPTION_DAILY` 的统一入口查询
- `underlying_code` 过滤
- 期权链结构完整性

## 任务成功总结模板

```md
# Task 07 Result

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
